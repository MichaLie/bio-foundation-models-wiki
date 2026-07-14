#!/usr/bin/env python3
"""Validate catalog structure, FAIR artifacts, and release gates without dependencies."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, urlsplit

from fair_metadata import load_resource_metadata


SENSITIVE_PAIR_RE = re.compile(
    r"(?i)(?:^|[?&;\s])(?:auth_token|access_token|token|api[_-]?key|apikey|secret|"
    r"password|passwd|session|cookie|state|ip_address)="
)


class FairScriptParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.capture = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if (
            tag == "script"
            and values.get("id") == "fair-metadata"
            and values.get("type") == "application/ld+json"
        ):
            self.capture = True

    def handle_data(self, data: str) -> None:
        if self.capture:
            self.parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.capture:
            self.capture = False


def is_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    if any(character.isspace() for character in value):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def normalized_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.replace("+", " plus ").casefold()).strip()


def main(release: bool = False) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    metadata = load_resource_metadata()
    profile = metadata.get("profile")
    data_path = Path(metadata["data_file"])
    schema_path = Path(metadata["schema_file"])
    records = json.loads(data_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    if not isinstance(records, list) or not records:
        errors.append(f"{data_path}: expected a non-empty JSON array")
        records = []

    item_schema = schema["items"]
    required = set(item_schema["required"])
    properties = item_schema["properties"]
    allowed = set(properties)
    seen_ids: dict[str, int] = {}
    seen_names: dict[str, tuple[int, str]] = {}
    missing_verified = 0
    hold_records: list[str] = []
    expected_link_urls: set[str] = set()

    for index, record in enumerate(records):
        where = f"{data_path}[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{where}: record is not an object")
            continue
        missing = sorted(required - set(record))
        unknown = sorted(set(record) - allowed)
        if missing:
            errors.append(f"{where}: missing {', '.join(missing)}")
        if unknown:
            errors.append(f"{where}: unknown fields {', '.join(unknown)}")
        if "new" in record:
            errors.append(f"{where}: obsolete relative field 'new' is not allowed")

        record_id = record.get("id")
        pattern = properties["id"].get("pattern")
        if not isinstance(record_id, str) or not re.fullmatch(pattern, record_id):
            errors.append(f"{where}.id: invalid or missing stable ID")
        elif record_id in seen_ids:
            errors.append(f"{where}.id: duplicate of record {seen_ids[record_id]}")
        else:
            seen_ids[record_id] = index

        date_added = record.get("date_added")
        if not isinstance(date_added, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_added):
            errors.append(f"{where}.date_added: expected YYYY-MM-DD")

        name = record.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{where}.name: required non-empty string")
        else:
            identities = [("name", name)] + [
                (f"aliases[{alias_index}]", alias)
                for alias_index, alias in enumerate(record.get("aliases", []))
            ]
            local: set[str] = set()
            for field, value in identities:
                key = normalized_name(value)
                if not key:
                    errors.append(f"{where}.{field}: empty normalized identity")
                    continue
                if key in local:
                    errors.append(f"{where}.{field}: duplicates another identity in the same record")
                    continue
                local.add(key)
                if key in seen_names:
                    other_index, other_field = seen_names[key]
                    errors.append(f"{where}.{field}: normalized duplicate of record {other_index}.{other_field}")
                else:
                    seen_names[key] = (index, field)

        for key, spec in properties.items():
            if key in record and "enum" in spec and record[key] not in spec["enum"]:
                errors.append(f"{where}.{key}: {record[key]!r} is outside the controlled vocabulary")

        if not record.get("verified"):
            missing_verified += 1

        for field in ("date_added", "date_modified", "verified"):
            value = record.get(field)
            if not value:
                continue
            try:
                from datetime import date
                date.fromisoformat(value)
            except (TypeError, ValueError):
                errors.append(f"{where}.{field}: invalid calendar date")

        visible_hold = str(record.get("status", "")).startswith("HOLD")
        if record.get("audit_state") == "hold" or visible_hold:
            hold_records.append(str(record_id))
            if record.get("audit_state") != "hold" or not visible_hold:
                errors.append(f"{where}: audit_state hold requires a visible HOLD status")
        if record.get("audit_state") == "verified" and record.get("audit_priority") != "P4":
            errors.append(f"{where}: verified records must have P4 audit priority")
        if not record.get("sources"):
            errors.append(f"{where}.sources: at least one evidence URL is required")
        for source_index, source in enumerate(record.get("sources", [])):
            if not is_http_url(source):
                errors.append(f"{where}.sources[{source_index}]: invalid URL")
            else:
                expected_link_urls.add(source)

        if profile == "foundation-models":
            for field in ("paper_links", "code_links"):
                for link_index, link in enumerate(record.get(field, [])):
                    if not isinstance(link, dict) or not link.get("label"):
                        errors.append(f"{where}.{field}[{link_index}]: missing label")
                    if not is_http_url(link.get("url") if isinstance(link, dict) else None):
                        errors.append(f"{where}.{field}[{link_index}]: invalid URL")
                    else:
                        expected_link_urls.add(link["url"])
        elif profile == "autonomous-agents":
            for field in ("paper_links", "repo_links"):
                for link_index, link in enumerate(record.get(field, [])):
                    if not isinstance(link, dict) or not link.get("label"):
                        errors.append(f"{where}.{field}[{link_index}]: missing label")
                    if not is_http_url(link.get("url") if isinstance(link, dict) else None):
                        errors.append(f"{where}.{field}[{link_index}]: invalid URL")
        elif profile == "coding-agents":
            links = record.get("links", {})
            for field in ("docs", "privacy"):
                if not is_http_url(links.get(field) if isinstance(links, dict) else None):
                    errors.append(f"{where}.links.{field}: invalid URL")
            pricing = links.get("pricing") if isinstance(links, dict) else None
            if pricing and not is_http_url(pricing):
                errors.append(f"{where}.links.pricing: invalid URL")
            for source_index, source in enumerate(record.get("sources", [])):
                if not is_http_url(source):
                    errors.append(f"{where}.sources[{source_index}]: invalid URL")
            special = (record.get("suitability") or {}).get("special")
            if special != "no" and not record.get("runs_locally"):
                errors.append(
                    f"{where}: special-category {special!r} requires a local/self-hosted path"
                )
        else:
            errors.append(f"resource_metadata.json: unknown profile {profile!r}")

    if missing_verified:
        message = f"{missing_verified}/{len(records)} records lack an explicit evidence-verification date"
        if release:
            errors.append(message)
        else:
            warnings.append(message)

    if hold_records:
        errors.append(
            f"{len(hold_records)} editorial HOLD records leaked into the displayed catalog; "
            "move them to records_under_review.json"
        )

    under_review_path = Path(metadata.get("under_review_file", "records_under_review.json"))
    under_review_schema_path = Path(metadata.get("under_review_schema_file", "records_under_review.schema.json"))
    under_review_ids: set[str] = set()
    if not under_review_path.is_file():
        errors.append(f"missing under-review register: {under_review_path}")
        under_review = {}
    else:
        under_review = json.loads(under_review_path.read_text(encoding="utf-8"))
        if not isinstance(under_review, dict):
            errors.append(f"{under_review_path}: expected a JSON object")
            under_review = {}
    if not under_review_schema_path.is_file():
        errors.append(f"missing under-review schema: {under_review_schema_path}")
    entries = under_review.get("entries", []) if isinstance(under_review, dict) else []
    if under_review.get("record_count") != len(entries):
        errors.append(f"{under_review_path}: record_count does not match entries")
    if (under_review.get("policy") or {}).get("displayed_in_index") is not False:
        errors.append(f"{under_review_path}: policy.displayed_in_index must be false")
    if (under_review.get("policy") or {}).get("stable_ids_reserved") is not True:
        errors.append(f"{under_review_path}: policy.stable_ids_reserved must be true")
    for index, entry in enumerate(entries):
        where = f"{under_review_path}.entries[{index}]"
        record = entry.get("record", {}) if isinstance(entry, dict) else {}
        review = entry.get("review", {}) if isinstance(entry, dict) else {}
        record_id = record.get("id")
        if not isinstance(record_id, str) or not re.fullmatch(properties["id"]["pattern"], record_id):
            errors.append(f"{where}.record.id: invalid or missing stable ID")
            continue
        if record_id in seen_ids:
            errors.append(f"{where}.record.id: also appears in the displayed catalog")
        if record_id in under_review_ids:
            errors.append(f"{where}.record.id: duplicate under-review stable ID")
        under_review_ids.add(record_id)
        missing = sorted(required - set(record))
        unknown = sorted(set(record) - allowed)
        if missing:
            errors.append(f"{where}.record: missing {', '.join(missing)}")
        if unknown:
            errors.append(f"{where}.record: unknown fields {', '.join(unknown)}")
        if record.get("audit_state") != "hold" or not str(record.get("status", "")).startswith("HOLD"):
            errors.append(f"{where}.record: under-review records must retain audit_state/status HOLD")
        if review.get("status") != "under_review":
            errors.append(f"{where}.review.status: expected under_review")
        for field in ("hold_since", "reason_code", "reason", "source", "reconsider_when"):
            if not review.get(field):
                errors.append(f"{where}.review.{field}: required")

    link_audit_path = Path("evidence/link_audit.tsv")
    if not link_audit_path.is_file():
        errors.append(f"missing link-audit evidence: {link_audit_path}")
    else:
        observed_link_urls: set[str] = set()
        unsafe_rows = 0
        with link_audit_path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                if row.get("url"):
                    observed_link_urls.add(row["url"])
                final_url = row.get("final_url", "")
                if final_url:
                    parsed = urlsplit(final_url)
                    if parsed.query or parsed.fragment:
                        unsafe_rows += 1
                if any(SENSITIVE_PAIR_RE.search(row.get(field, "")) for field in ("url", "final_url", "error")):
                    unsafe_rows += 1
        missing_urls = sorted(expected_link_urls - observed_link_urls)
        stale_urls = sorted(observed_link_urls - expected_link_urls)
        if missing_urls or stale_urls:
            errors.append(
                f"{link_audit_path}: URL coverage differs from canonical catalog "
                f"({len(missing_urls)} missing, {len(stale_urls)} stale)"
            )
        if unsafe_rows:
            errors.append(f"{link_audit_path}: {unsafe_rows} row(s) retain unsafe URL/error material")

    docs = Path("docs")
    pairs = [
        (data_path, docs / metadata["data_file"]),
        (schema_path, docs / metadata["schema_file"]),
        (Path("metadata.jsonld"), docs / "metadata.jsonld"),
        (Path("biological_foundation_models_wiki.md"), docs / "biological_foundation_models_wiki.md"),
        (under_review_path, docs / under_review_path.name),
        (under_review_schema_path, docs / under_review_schema_path.name),
        (Path("UNDER_REVIEW.md"), docs / "UNDER_REVIEW.md"),
        (Path("assets/fonts/SourceSans3-Variable.ttf"), docs / "assets/fonts/SourceSans3-Variable.ttf"),
        (Path("assets/fonts/OFL.txt"), docs / "assets/fonts/OFL.txt"),
    ]
    for source, published in pairs:
        if not source.is_file():
            errors.append(f"missing generated/source artifact: {source}")
        if not published.is_file():
            errors.append(f"missing public distribution: {published}")
        elif source.is_file() and source.read_bytes() != published.read_bytes():
            errors.append(f"public distribution differs from source: {published}")

    metadata_path = Path("metadata.jsonld")
    if metadata_path.is_file():
        jsonld = json.loads(metadata_path.read_text(encoding="utf-8"))
        required_terms = {
            "dct:identifier",
            "dct:title",
            "dct:description",
            "dct:accessRights",
            "dcat:landingPage",
            "dcat:distribution",
            "dct:provenance",
            "prov:wasDerivedFrom",
            "dct:conformsTo",
        }
        absent = sorted(required_terms - set(jsonld))
        if absent:
            errors.append(f"metadata.jsonld: missing FAIR terms {', '.join(absent)}")
        if jsonld.get("schema:numberOfItems") != len(records):
            errors.append("metadata.jsonld: record count does not match canonical data")
        relation = jsonld.get("dct:relation", {})
        if relation.get("schema:numberOfItems") != len(entries):
            errors.append("metadata.jsonld: under-review relation count does not match register")
        if metadata.get("license"):
            if "dct:license" not in jsonld:
                errors.append("metadata.jsonld: configured licence was not emitted")
        else:
            message = "reuse licence is unresolved; FAIR R1.1 and legal reuse remain blocked"
            (errors if release else warnings).append(message)

        index_path = docs / "index.html"
        if not index_path.is_file():
            errors.append(f"missing generated page: {index_path}")
        else:
            parser = FairScriptParser()
            parser.feed(index_path.read_text(encoding="utf-8"))
            if not parser.parts:
                errors.append("docs/index.html: embedded FAIR JSON-LD not found")
            else:
                embedded = json.loads("".join(parser.parts))
                if embedded != jsonld:
                    errors.append("docs/index.html: embedded JSON-LD differs from metadata.jsonld")

    if not metadata.get("publisher"):
        message = "formal publisher identity is unresolved"
        (errors if release else warnings).append(message)
    if not metadata.get("release_ref"):
        message = "published release reference is unresolved (expected a human-created tag or release URL)"
        (errors if release else warnings).append(message)
    elif not is_http_url(metadata["release_ref"]):
        errors.append("resource_metadata.json: release_ref must be an HTTP(S) URL")
    elif release:
        expected_release_ref = metadata["repository"].rstrip("/") + "/releases/tag/v" + metadata["resource_version"]
        if metadata["release_ref"].rstrip("/") != expected_release_ref:
            errors.append(
                "resource_metadata.json: release_ref must match the repository and resource_version "
                f"(expected {expected_release_ref})"
            )
    if release and ("preview" in metadata["resource_version"].casefold() or "-rc" in metadata["resource_version"].casefold()):
        errors.append("resource_version is still a preview/release candidate")
    print(f"VALIDATION profile={profile} records={len(records)}")
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--release",
        action="store_true",
        help="Turn unresolved governance and evidence coverage into hard failures.",
    )
    args = parser.parse_args()
    raise SystemExit(main(release=args.release))
