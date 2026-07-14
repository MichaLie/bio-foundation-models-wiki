#!/usr/bin/env python3
"""Build human-readable and public copies of the non-displayed review register."""
from __future__ import annotations

import json
import shutil
from pathlib import Path


REGISTER = Path("records_under_review.json")
SCHEMA = Path("records_under_review.schema.json")
OUTPUT = Path("UNDER_REVIEW.md")
DOCS = Path("docs")


def cell(value: object) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ").strip()


def main() -> int:
    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    entries = register["entries"]
    lines = [
        "# Biological Foundation Models — records under review",
        "",
        register["description"],
        "",
        "These candidates are **not part of the displayed or canonical released index**. Their stable IDs are reserved so that decisions remain traceable. This register is a review queue, not a recommendation or tombstone list.",
        "",
        f"Register date: {register['date_modified']} · Records under review: {len(entries)}",
        "",
        "| Stable ID | Candidate | Reason class | Why held | Reconsider when |",
        "| --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        record = entry["record"]
        review = entry["review"]
        lines.append(
            f"| `{cell(record['id'])}` | {cell(record['name'])} | {cell(review['reason_code'])} | "
            f"{cell(review['reason'])} | {cell(review['reconsider_when'])} |"
        )
    lines.extend([
        "",
        "## Promotion rule",
        "",
        register["policy"]["promotion_rule"],
        "",
        "The machine-readable source is `records_under_review.json`; its contract is `records_under_review.schema.json`. The dated source-review ledgers remain the evidence authority.",
        "",
    ])
    payload = "\n".join(lines)
    OUTPUT.write_text(payload, encoding="utf-8")
    DOCS.mkdir(exist_ok=True)
    (DOCS / OUTPUT.name).write_text(payload, encoding="utf-8")
    shutil.copyfile(REGISTER, DOCS / REGISTER.name)
    shutil.copyfile(SCHEMA, DOCS / SCHEMA.name)
    print(f"Wrote under-review register ({len(entries)} records; excluded from displayed index)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
