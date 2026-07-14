# Claude adapter — Biological Foundation Models

Read [MAINTENANCE.md](MAINTENANCE.md) completely before acting. It is the canonical protocol for scope, evidence, schema, deterministic builds, FAIR metadata, release validation, and publication authority.

For discovery work, also use `.claude/skills/update-bio-fm-wiki/SKILL.md`; that skill is subordinate to `MAINTENANCE.md`.

Key boundary: edit `models_final.json` or a reviewed dated migration, never generated distributions. Run `python3 build.py`, preview validation, and the full link audit. Do not push, deploy, mint a DOI, or publish a FAIR badge without explicit human approval after `python3 validate_catalog.py --release` passes.
