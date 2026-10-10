#!/usr/bin/env python3
"""Apply the source-reviewed October 2026 local preview refresh, idempotently.

The payload (evidence/refresh-2026-10-10/reviewed_changes.json) records complete,
adversarially reviewed decisions, not a discovery algorithm. Re-run only to
reproduce this refresh. It never fetches sources, publishes, invents
verification dates, or edits generated distributions.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/refresh-2026-10-10/reviewed_changes.json"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert(existing: list[dict], replacements: list[dict], key) -> list[dict]:
    updates = {key(row): row for row in replacements}
    if len(updates) != len(replacements):
        raise ValueError("duplicate IDs in reviewed migration payload")
    result = [updates.pop(key(row), row) for row in existing]
    result.extend(updates.values())
    return result


def main() -> None:
    payload = read(EVIDENCE)
    date = payload["date"]
    before = {row["id"] for row in read(ROOT / "models_final.json")}
    removed = set(payload.get("catalog_remove_ids", []))
    data = upsert([row for row in read(ROOT / "models_final.json") if row["id"] not in removed],
                  payload["catalog_upserts"], lambda row: row["id"])
    register = read(ROOT / "records_under_review.json")
    held_before = {entry["record"]["id"] for entry in register["entries"]}
    register["entries"] = upsert(
        [entry for entry in register["entries"] if entry["record"]["id"] not in set(payload["held_remove_ids"])],
        payload["held_upserts"], lambda entry: entry["record"]["id"])
    if {row["id"] for row in data} & {entry["record"]["id"] for entry in register["entries"]}:
        raise ValueError("a stable ID cannot be displayed and held")
    register["record_count"] = len(register["entries"])
    register["date_modified"] = date

    # Counts come from the payload, not the current files, so a re-run writes identical metadata.
    promoted_ids = {row["id"] for row in payload["catalog_upserts"]} & set(payload["held_remove_ids"])
    added = sum(1 for row in payload["catalog_upserts"] if row["date_added"] == date and row["id"] not in promoted_ids)
    promoted = len(promoted_ids)
    new_holds = sum(1 for entry in payload["held_upserts"] if entry["review"]["hold_since"] == date and entry["record"]["id"] not in removed)
    counts = Counter(row["audit_state"] for row in data)
    metadata = read(ROOT / "resource_metadata.json")
    metadata.update(
        resource_version="2.3.0",
        modified=date,
        evidence_review_date=date,
        baseline_data_date=date,
        baseline_commit=payload["baseline_commit"],
        baseline_commit_url=metadata["repository"] + "/commit/" + payload["baseline_commit"],
        release_ref=None,
    )
    metadata["provenance"] = (
        "Curated from primary papers, official repositories, model hubs, project pages, and explicit licence or access terms. "
        f"The {date} local preview follows the September catalog with discovery lanes for all ten modalities, a calibrated-uncertainty "
        "lane and a candidate-feed/watchlist lane, followed by a separate adversarial review of every proposed addition and promotion. "
        f"It adds {added} records, promotes {promoted} previously held records whose reconsideration conditions are now met, "
        f"moves {len(removed)} record whose official code was withdrawn to the under-review register, corrects stale access, "
        "repository and publication details on existing records, and re-reviews every held record. "
        f"The canonical displayed catalog contains {len(data)} records; {len(register['entries'])} unresolved candidates remain "
        "in the separate under-review register. Unchanged rows retain their prior verification dates. "
        "Generated distributions come from canonical JSON through a deterministic build. This preview has no published release reference."
    )
    metadata["evidence_statement"] = (
        f"{len(data)} records: {counts['verified']} verified and {counts['verified_with_limits']} with visible limitations. "
        f"October review covers new and promoted entries, targeted corrections and all previously held records; older verification "
        f"dates are preserved. {len(register['entries'])} candidates remain under review. "
        "Check each record's access and licence limitations before use."
    )
    write(ROOT / "models_final.json", data)
    write(ROOT / "records_under_review.json", register)
    write(ROOT / "resource_metadata.json", metadata)
    print(f"Applied {date}: {len(data)} displayed ({added} added, {promoted} promoted, {len(removed)} moved to hold), "
          f"{len(register['entries'])} held ({new_holds} new); local preview 2.3.0")


if __name__ == "__main__":
    main()
