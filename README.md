# Biological Foundation Models — Researcher Index

A filterable, public index of foundation models for biological sequences, molecules, structures, omics, cells, and tissue images. For each model: what it operates on, what goes in/out, how accessible it is today, and what it's for.

**Live site:** https://michalie.github.io/bio-foundation-models-wiki/

264 entries across 10 categories (DNA, RNA, protein, structure/complex, small-molecule, single-cell, spatial/pathology, multimodal, platforms, benchmarks).

---

## How to update it

**`models_final.json` is the single source of truth. Edit it, rebuild, push — the live site (served from `docs/`) updates.** Never hand-edit the `.html`/`.md` — they are generated.

### Option A — let an agent do it (your default)
Point Claude/Codex at this repo:
- **Add one model:** "Add `<name>` to `models_final.json` (modality, links, in/out, access), then run `python3 build_html.py models_final.json docs/index.html`, commit and push."
- **Re-sweep the whole field:** re-run the model-discovery sweep, regenerate `models_final.json` via `merge.py`, rebuild into `docs/`, commit, push. The field moves weekly, so a periodic re-sweep keeps it current.

### Option B — dump it in an Issue
Open a new Issue with the **"Add / fix a model"** template, fill the fields, submit. You (or an agent) turn it into a JSON entry — handy when you're on your phone or mid-thought.

### Option C — local
```bash
# edit models_final.json, then rebuild into the published folder and push:
python3 build_html.py models_final.json docs/index.html
python3 build_md.py
git commit -am "update models" && git push
```

### Optional upgrade — browser-only editing
Want to edit `models_final.json` in GitHub's web editor and have the site rebuild itself (no local build)? That needs a one-time token-scope grant, then switching on the bundled Action:
```bash
~/.local/bin/gh auth refresh -h github.com -s workflow   # ~20s, opens browser
mkdir -p .github/workflows && mv optional-github-action.yml .github/workflows/deploy.yml
# then in repo Settings → Pages, set Source = GitHub Actions, and push.
```

---

## Record schema (`models_final.json`)

```json
{
  "name": "AlphaGenome",
  "modality": "dna",
  "description": "One-sentence what-it-is.",
  "io": "DNA up to 1 Mb -> regulatory tracks + variant scores",
  "status": "Web/API/commercial",
  "use_cases": "Regulatory variant effect, splicing/expression impact",
  "year": "2025",
  "paper_links": [{"label": "Nature", "url": "https://..."}],
  "code_links":  [{"label": "GitHub", "url": "https://..."}],
  "canonical": false,
  "noncommercial": false
}
```

- `modality`: one of `dna rna protein complex molecule singlecell spatial multimodal platform benchmark`.
- `status`: free text; the build derives a colour-coded access bucket from it (open / partial / hub / api / platform / paper).
- `canonical`: `true` for the 1–3 anchor models in an area (gets a ⭐).
- `noncommercial`: `true` if the licence is non-commercial (gets an "NC" tag).

---

## What's in here

| File | Role |
| --- | --- |
| `models_final.json` | **Source of truth** — the model data |
| `build_html.py` | Generates the interactive HTML site |
| `build_md.py` | Generates the Markdown version |
| `merge.py` | Combines model sources into `models_final.json` (re-sweep reference) |
| `docs/` | The published site (Pages serves `docs/index.html`) |
| `optional-github-action.yml` | Opt-in auto-build Action (see upgrade above) |

## Caveats

Access tags reflect **code/weight availability, not licence terms** — verify the licence before commercial use. Params, max-context, and training scale live in the description prose (not yet filterable fields). A licence-resolution pass is the highest-value next step.
