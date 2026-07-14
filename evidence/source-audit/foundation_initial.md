# Foundation Models initial adversarial audit

**Frozen target:** `e79a48cb7caa70555d0e6cb0a0838d849297c57e`  
**Role:** internal adversarial reviewer, read-only  
**Verdict:** not release-ready  
**Coverage:** structural checks 377/377; additions and material changes dated 2026-07-13 77/77; primary-source review 99/377 (all 77 changed plus 22 unchanged). Two P2 errors in the unchanged sample triggered the subsequent 300-record residual source audit.

## Findings

- **P1 — governance gates:** release validation correctly blocks an unresolved catalogue reuse licence, publisher identity, and preview resource version.
- **P1 — stale public Markdown:** `docs/biological_foundation_models_wiki.md` reports 264 records while the canonical root Markdown reports 377. `build_md.py` hard-codes 2026-06-16 and does not publish the docs copy, so the current determinism check can pass while preserving stale public output.
- **P2 — misleading provenance:** `source_commit` points to the production baseline rather than the audited preview content. This must become an explicit baseline/build provenance model rather than a manually maintained self-reference.
- **P2 — `bfm-openphenom-s-16-phenom-family`:** official project terms are non-commercial-only; `noncommercial` must be true and the official project hub should be cited.
- **P2 — `bfm-mupd`:** the official Hugging Face artifact is public rather than gated; preserve its CC BY-NC-ND terms and set the non-commercial flag.
- **P2 — `bfm-gpt-rosalind`:** availability was described too broadly. The official release scopes access to qualified Enterprise customers and initially to the United States.
- **P2 — `bfm-poet-2` and `bfm-openprotein-ai-poet-poet-2`:** operational duplicates share the same paper and repository. Retain a platform record only if it has official platform/API evidence and a clearly different identity; otherwise merge.
- **P2 — `bfm-ankh`:** official checkpoint is CC BY-NC-SA-4.0; set non-commercial and access status accordingly.
- **P2 — `bfm-prot2text`:** CC BY-NC-SA-4.0 conflicts with `noncommercial=false`.
- **P2 — `bfm-prism`:** gated CC BY-NC-ND-4.0 artifact is academic/non-commercial and excludes clinical use; update the flag and status.
- **P2 — incomplete decision evidence:** the discovery evidence note documents only 14 of 23 modified existing records. Add public evidence/decision entries for Orthrus, CodonBERT, BiRNA-BERT, RhoFold+, LAMAR, OmniGenome, OpenFold3, OpenPhenom, and Ginkgo.
- **P3 — validator coverage:** the custom validator does not fully enforce the JSON Schema, normalized aliases, semantic dates, provenance, or Markdown synchronization.
- **P4 — alias hygiene:** MuPaD has a case-normalized duplicate alias.

## Primary sources for corrections

- OpenPhenom: <https://www.rxrx.ai/phenom>
- MuPaD: <https://huggingface.co/xiangjx/MuPaD-256>
- GPT-Rosalind: <https://openai.com/index/introducing-gpt-rosalind/>
- OpenProtein: <https://www.openprotein.ai/> and <https://docs.openprotein.ai/rest-api/prompt.html>
- Ankh: <https://huggingface.co/ElnaggarLab/ankh-large> and <https://github.com/agemagician/Ankh>
- Prot2Text: <https://github.com/hadi-abdine/Prot2Text>
- PRISM: <https://huggingface.co/paige-ai/Prism>

The reviewer made no edits. Every P1/P2 above requires coordinator re-verification after remediation.
