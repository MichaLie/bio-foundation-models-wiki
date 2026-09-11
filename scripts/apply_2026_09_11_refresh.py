#!/usr/bin/env python3
"""Apply the source-reviewed September 2026 local preview refresh, idempotently.

The frozen payload records complete decisions, not a discovery algorithm. Re-run
this dated migration only to reproduce this refresh. It never fetches sources,
publishes, invents verification dates, or edits generated distributions.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/refresh-2026-09-11/reviewed_changes.json"


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
    catalog_removed = set(payload.get("catalog_remove_ids", []))
    data = upsert(
        [row for row in read(ROOT / "models_final.json") if row["id"] not in catalog_removed],
        payload["catalog_upserts"],
        lambda row: row["id"],
    )
    register = read(ROOT / "records_under_review.json")
    removed = set(payload["held_remove_ids"])
    register["entries"] = upsert(
        [entry for entry in register["entries"] if entry["record"]["id"] not in removed],
        payload["held_upserts"],
        lambda entry: entry["record"]["id"],
    )
    if {row["id"] for row in data} & {entry["record"]["id"] for entry in register["entries"]}:
        raise ValueError("a stable ID cannot be displayed and held")
    register["record_count"] = len(register["entries"])
    register["date_modified"] = date

    metadata = read(ROOT / "resource_metadata.json")
    metadata.update(
        resource_version="2.2.0",
        modified=date,
        baseline_data_date=date,
        baseline_commit=payload["baseline_commit"],
        baseline_commit_url=metadata["repository"] + "/commit/" + payload["baseline_commit"],
        release_ref=None,
    )
    counts = Counter(row["audit_state"] for row in data)
    metadata["provenance"] = (
        "Curated from primary papers, official repositories, model hubs, project pages, and explicit licence or access terms. "
        "The 2026-09-11 local preview follows the August catalog with discovery across all ten modalities and condition-focused "
        "re-review of all 39 previously held records. It adds 11 displayed records including two resolved family promotions "
        "and a separately evidenced family member, makes a targeted GPN-MSA lifecycle/publication update, "
        "and returns ALICE to HOLD after current official access could no longer be verified. "
        f"The canonical displayed catalog contains {len(data)} records; {len(register['entries'])} unresolved candidates remain "
        "in the separate under-review register. Unchanged rows retain their prior verification dates. "
        "Generated distributions come from canonical JSON through a deterministic build. This preview has no published release reference."
    )
    metadata["evidence_statement"] = (
        f"{len(data)} records: {counts['verified']} verified and {counts['verified_with_limits']} with visible limitations. "
        "September review covers new entries and all 39 previous holds; older verification dates are preserved. "
        f"{len(register['entries'])} candidates remain under review. "
        "Check each record's access and licence limitations before use."
    )
    write(ROOT / "models_final.json", data)
    write(ROOT / "records_under_review.json", register)
    write(ROOT / "resource_metadata.json", metadata)
    print(f"Applied {date}: {len(data)} displayed, {len(register['entries'])} held; local preview 2.2.0")


if __name__ == "__main__":
    main()
