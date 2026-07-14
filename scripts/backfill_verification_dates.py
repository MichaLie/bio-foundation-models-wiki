#!/usr/bin/env python3
"""Backfill explicit verification dates from documented catalog audits.

The 2026-06-16 release was produced by a 25-agent coverage, adversarial
candidate-verification, and existing-entry fact-check workflow. The 2026-06-20
release added 59 verified records under the repository update protocol. Records
reviewed again later keep their newer explicit date.
"""
from __future__ import annotations

import json
from pathlib import Path


path = Path("models_final.json")
records = json.loads(path.read_text(encoding="utf-8"))
allowed = {"2026-06-16", "2026-06-20"}
changed = 0
for record in records:
    if record.get("verified"):
        continue
    if record.get("date_added") not in allowed:
        raise SystemExit(f"no documented audit date for {record['id']}")
    record["verified"] = record["date_added"]
    changed += 1

path.write_text(json.dumps(records, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"backfilled {changed} historical verification dates")
