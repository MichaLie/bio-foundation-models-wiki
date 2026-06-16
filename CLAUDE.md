# CLAUDE.md — Biological Foundation Models Wiki

Operating guide for any Claude/Codex instance working in this repo. **Read this first.**

## What this is
A public, filterable index of foundation models for biological sequences, molecules, structures, omics, cells, and tissue images. For each model: what it operates on, what goes in/out, how accessible it is, and what it's for.

- **Live site:** https://michalie.github.io/bio-foundation-models-wiki/
- **Repo:** https://github.com/MichaLie/bio-foundation-models-wiki
- **Scope:** 264 entries across 10 categories (DNA, RNA, protein, complex, molecule, singlecell, spatial, multimodal, platform, benchmark).
- **Owner:** Michaela (GitHub: `MichaLie`).

## Golden rules
1. **`models_final.json` is the only source of truth.** Edit it. **Never** hand-edit the generated `.html` or `.md`.
2. **Always rebuild after editing data, then push.** Pages serves `docs/`, so the rebuilt `docs/index.html` must be committed for the live site to change.
3. **Keep the public site clean.** No "NEW" tags, no audit/process framing, no internal notes on the rendered page — these were deliberately removed; do not reintroduce them. The only badges are the access pill, ⭐ (canonical), and NC (non-commercial).
4. **Verify every link.** Never invent paper/code URLs. If a link can't be confirmed, set the code link to "none found" rather than guessing.
5. **Don't commit the local-only files** `AUDIT_REPORT.md`, `workflow_result.json`, `existing_models.json` — they're gitignored provenance kept on Michaela's machine, not for the public repo.

## Build & deploy
```bash
python3 build_html.py models_final.json docs/index.html                          # the PUBLISHED site
python3 build_html.py models_final.json biological_foundation_models_wiki.html    # downloadable copy
python3 build_md.py                                                               # markdown copy
git add -A && git commit -m "update models" && git push
```
- Python 3 only, **no dependencies**.
- Hosting = GitHub Pages from `main:/docs` (branch deploy, **not** a GitHub Action — the token lacks the `workflow` scope; the unused Action sits in `optional-github-action.yml` with a one-line enable recipe in the README).
- On Michaela's machine `gh` is at `~/.local/bin/gh`, authenticated as `MichaLie`. From a fresh machine, run `gh auth status` first. After pushing, Pages redeploys in ~1–2 min — verify by curling the live URL.

## Data schema (one record in `models_final.json`)
```json
{ "name": "AlphaGenome", "modality": "dna", "description": "one sentence",
  "io": "DNA up to 1 Mb -> regulatory tracks + variant scores",
  "status": "Web/API/commercial", "use_cases": "...", "year": "2025",
  "paper_links": [{"label": "Nature", "url": "https://..."}],
  "code_links":  [{"label": "GitHub", "url": "https://..."}],
  "canonical": false, "noncommercial": false }
```
- `modality` ∈ `dna rna protein complex molecule singlecell spatial multimodal platform benchmark`.
- `status`: free text; `build_html.py::access_cat()` derives the colour bucket (open / partial / hub / api / platform / paper). Use phrasings like `Open code + weights`, `Open code, gated weights`, `Model hub`, `Web/API/commercial`, `Paper/preprint only`.
- `canonical: true` **only** for the 1–3 anchor / most-used models in an area (gets ⭐). Don't over-apply.
- `noncommercial: true` for CC-BY-NC / non-commercial licences (gets the NC tag).
- **Modality routing:** pathology / histology / WSI / cell-imaging / spatial-omics → `spatial`; datasets / benchmarks / leaderboards → `benchmark`; serving layers / toolkits / hubs → `platform`.

## Adding or maintaining models
For the recurring "find new models and add them" task, use the skill **`update-bio-fm-wiki`** (`.claude/skills/update-bio-fm-wiki/SKILL.md`). In short: discover → adversarially verify → classify → append to `models_final.json` (dedupe by name) → rebuild → push.

## Keeping it alive
- **Periodic re-sweep** to catch new releases — the field moves weekly. The skill covers both a quick manual add and a full multi-agent sweep.
- **Maintenance:** re-verify links, upgrade `status` when gated weights become open, fix dead/incorrect URLs, prune duplicates and retired models.
- **Highest-value next pass:** a licence audit — turn `status` into a trustworthy commercial vs non-commercial signal (currently access tags reflect availability, not licence terms).
