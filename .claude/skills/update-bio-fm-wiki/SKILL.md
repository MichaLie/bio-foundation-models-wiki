---
name: update-bio-fm-wiki
description: Find biological/molecular/omics foundation models not yet in the wiki, verify them, add them to models_final.json, rebuild the site, and push. Use when asked to update, grow, maintain, refresh, or re-sweep the biological foundation models wiki, add new models, fix entries, or keep the repo current and live.
---

# Update the Biological Foundation Models Wiki

Keep this repo (`MichaLie/bio-foundation-models-wiki`, working dir `~/Desktop/wiki`) **complete, correct, and live**. Two modes: **quick add** (a handful of known models) and **full re-sweep** (comprehensive periodic refresh). Read `CLAUDE.md` first — it has the schema, rules, and build/deploy commands.

## 0. Orient
- Read `CLAUDE.md`; load `models_final.json`.
- Build the set of existing model names **and aliases**, normalized (lowercase, strip punctuation/parentheses). Check every candidate against this to avoid duplicates.

## 1. Discover — find what's missing
Search per modality for foundation models NOT already present. A *foundation model* = pretrained, reusable, general-purpose (embeddings / generation / prediction), **not** a one-off task classifier or a dataset.
- Prioritize: canonical/widely-used models, **2024–2026 releases**, models with public code/weights.
- Cover every modality: DNA/genome, RNA (incl. structure), protein (sequence / fitness / design / antibody), structure & complex, small-molecule/chemistry, single-cell/omics, **spatial + pathology/cell-imaging**, multimodal/bio-LLM, platforms, benchmarks.
- Use **web search** to confirm each model exists and to get the correct paper + code/weights URLs and access model.
- **Full re-sweep:** use the **Workflow tool** (multi-agent) — fan out one agent per modality to find missing models, then a verification stage that adversarially checks each candidate. This is the pattern that built the wiki; it's token-heavy but thorough. For a quick add, do it inline.

## 2. Verify — adversarial, do not skip
For each candidate:
- Confirm it **actually exists** and is a genuine pretrained foundation model (not a benchmark mislabeled as a model, not a single-task tool).
- Confirm it is **not already covered** under any name/alias.
- Confirm the **paper URL and code/weights URL resolve** and belong to it. Correct wrong links. If unconfirmable, use `"none found"` — **never guess a URL**. (Past audits found links pointing to entirely unrelated papers — always click through.)
- Determine the correct **access status** (open / gated / hub / web-API / paper-only) and whether the licence is **non-commercial**.
- Default to dropping/uncertain when you can't confirm.

## 3. Classify
- Assign `modality` from the controlled vocabulary in `CLAUDE.md`.
- Route: pathology/histology/WSI/cell-imaging/spatial → `spatial`; datasets/benchmarks/leaderboards → `benchmark`; serving layers/toolkits/hubs → `platform`.
- Set `canonical: true` only for true anchor models; `noncommercial: true` for CC-BY-NC etc.; derive `year` from the paper.

## 4. Write entries
- Append each verified model to `models_final.json` following the schema in `CLAUDE.md`.
- Convert single paper/code URLs into `paper_links` / `code_links` arrays with a short label (`Nature`, `bioRxiv`, `GitHub`, `Hugging Face`, …).
- **Dedupe by normalized name.** Do **not** add "new" tags or any audit/process framing — the public site stays clean.

## 5. Rebuild, validate, publish
```bash
python3 build_html.py models_final.json docs/index.html
python3 build_html.py models_final.json biological_foundation_models_wiki.html
python3 build_md.py
```
- Validate: `models_final.json` parses; every record has `name`/`modality`/`description`; sanity-check per-modality counts.
- Confirm it renders (open `docs/index.html`, or curl the live URL after deploy).
- Commit with a clean message and push. **Poll the live URL** until it serves the new content (first deploy of a change takes ~1–2 min; a 404 then 200 is normal).

## 6. Maintenance — keep it alive
- Re-verify links periodically; fix dead/incorrect ones.
- Upgrade `status` when gated weights become public.
- Add canonical markers as the field's consensus anchors emerge; prune duplicates and retired models.
- Highest-value next pass: **licence resolution** — make `status` trustworthy for commercial/grant decisions.

## Guardrails
Only real, verifiable foundation models. Verified links only. Clean public copy — no internal notes, no NEW tags. Keep the licence caveat. `models_final.json` is the only file you edit by hand; everything else is generated.
