---
name: update-bio-fm-wiki
description: Safely update, verify, build, and locally validate the Biological Foundation Models index under the repository maintenance and FAIR release gates.
---

# Update the Biological Foundation Models index

1. Read `MAINTENANCE.md` completely. It is canonical and this skill cannot override it.
2. Read `schema.json`, load `models_final.json`, normalize all names and aliases, and inspect the latest `evidence/` note.
3. Select a bounded correction/addition or a full refresh. For a full refresh, use independent discovery lanes across all 10 modalities and a shuffled adversarial verification stage.
4. Verify each candidate from current primary paper, official repository/project/model hub, and licence/access evidence. Prefer HOLD over guessing or padding.
5. Preserve stable IDs and real evidence dates. Use a dated idempotent migration for a large change and add a dated audit note recording accepts, holds, rejections, merges, and corrections.
6. Run:

```bash
python3 build.py
python3 validate_catalog.py
python3 scripts/audit_links.py --workers 24 --timeout 20
git diff --check
```

7. Inspect the local rendered site and machine-readable distributions. Run `python3 validate_catalog.py --release` only as the final eligibility check.

Never push, deploy Pages, create a release/DOI, or publish a FAIR badge unless the human owner explicitly authorizes that action after reviewing the complete preview and a passing release gate.
