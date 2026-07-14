# Foundation under-review separation — 2026-07-14

## Decision

The source-reviewed 377-candidate set was separated into:

- **345 canonical displayed records** in `models_final.json`;
- **32 non-displayed candidates under review** in `records_under_review.json`.

No scope or reuse-term exception was granted. The 32 complete records were moved losslessly rather than deleted or reduced to names. Their stable IDs remain reserved, and each entry carries its original evidence fields plus a structured reason class and an explicit `reconsider_when` condition.

This is an under-review register, not a tombstone list: the records were not part of an immutable public release and may be promoted later when their recorded condition is satisfied.

## Release and maintenance behavior

- The interactive HTML, Markdown index, canonical JSON count, JSON-LD `schema:numberOfItems`, and portal count include only the 345 release-policy records.
- The review register is machine-readable and schema-described, but its records are not rendered, searchable, or filterable in the main index.
- `validate_catalog.py` and the public maintenance harness fail if a HOLD appears in `models_final.json`, if an ID appears in both stores, or if the register/schema/distributions drift.
- The isolated maintenance simulation now injects a held record into the public catalog and proves that the gate blocks it.
- The Research Tool Trial Agent reads the register only as a blocklist, so an explicitly requested under-review ID remains `blocked/catalog_hold` rather than becoming an unknown or testable candidate.

## Verification

- Deterministic build: **PASS**, 14 byte-stable generated artifacts.
- Preview validation: **PASS**, zero errors; only the intentionally null immutable release reference remains a warning.
- Full JSON Schema/invariant maintenance: **PASS**, including all 32 review entries and public/review ID disjointness.
- Fault injection: **8/8 PASS** for Foundation, including held-record leakage; the real canonical data stayed unchanged during simulation.
- Full live-link audit: **735 reachable, 97 access-restricted, 0 missing, 0 HTTP error, 0 network error** across displayed Foundation link occurrences.
- Strict release validation: passes for the v2.0.0 package and its structurally exact planned release reference; after authorized publication, the exact URL must resolve before announcement.

## Exact local hashes

- `models_final.json`: `092214913cbe3b0651d46b541ebe8809bac78faada0ade6b879750c8ba9ac7ad`
- `records_under_review.json`: `f44c21cd8037bcc4085c2baeb826fb166390e886374003384b7614cdefe22b88`

## Promotion rule

A record may move into `models_final.json` only after its stated reconsideration condition is met, primary evidence is refreshed, the stable ID is preserved, the dated decision is logged, and the full maintenance gate passes. Publication still requires a separate explicit human authorization.
