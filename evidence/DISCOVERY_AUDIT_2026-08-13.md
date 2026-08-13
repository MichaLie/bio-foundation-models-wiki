# Biological Foundation Models discovery audit — 2026-08-13

## Scope and method

This is the durable evidence summary for the protected local FAIR workspace. It covers the v2.1.0 content refresh: a discovery sweep over the 2026-06-15 to 2026-08-13 window, a per-candidate verification wave, and a full re-review of the under-review register.

- **Discovery.** Ten delegated lanes, one per modality (dna, rna, protein, complex, molecule, singlecell, spatial, multimodal, platform, benchmark), each deduplicating candidates against the current normalized name and alias set of the displayed catalog and the hold register before proposing anything.
- **Verification.** Candidates were shuffled into thirteen independent verification slices under an anti-fabrication contract: every claim had to come from a primary paper record, an official repository or model hub, or an official project page, with per-claim source URLs recorded and the exact licence sentence quoted. Lanes were instructed to hold rather than guess, and to record UNVERIFIED explicitly instead of inferring.
- **Register re-review.** All 32 under-review entries were re-checked in four slices against their recorded `reconsider_when` conditions, again with quoted licence evidence.
- **Adjudication.** The primary editor resolved cross-slice disagreements conservatively and applied the result through the dated idempotent migration `scripts/apply_2026_08_13_refresh.py`.

Acceptance means the model or resource is real, in scope, and supported by the cited sources on this date. It is not an endorsement of performance, clinical fitness, or legal reuse. `verified: 2026-08-13` records the evidence-review date.

### Honest constraints

- The shared web-search quota was exhausted part-way through the sweep. Later lanes ran on direct fetches and public APIs (arXiv, bioRxiv, Crossref, Europe PMC, PubMed, GitHub, Hugging Face, Kaggle, Zenodo, OSF) instead of search, which narrows discovery breadth but not verification depth.
- bioRxiv HTML responses returned 403 or 429 for several lanes; those checks were completed through the bioRxiv API, the JATS source XML, or the bioRxiv MCP server.
- Several publisher and vendor pages (RSC, ChemRxiv landing pages, Nature author gateways, OpenReview) blocked automated fetches; where a claim depended on them it was verified through Crossref or PubMed registration records instead, or recorded as UNVERIFIED.
- One verification wave was interrupted and relaunched; the relaunched agents re-verified their slices from primary sources rather than inheriting partial state.
- Two lanes reviewed RibonanzaNet2 and scMamba independently and reached opposite verdicts. Both disagreements are documented under "Cross-slice adjudications" below.

## Result

- Displayed catalog before: 345 records. After: 390 records.
- Under-review register before: 32 entries. After: 39 entries (32 − 3 promoted + 10 new holds).
- Candidate verdicts: 44 accept, 11 hold, 10 reject, 1 already-held match, across 66 verdict rows in `evidence/additions-2026-08-13/fm_result_{1..13}.json`.
- Applied: **42 new displayed records** (two accepts were overridden conservatively, see below), **3 promotions** from the register, **10 new hold entries**, **14 refreshed hold reviews**, and 2 materially corrected existing records.
- Deterministic build: pass, 16 byte-stable generated artifacts.
- Preview validation: pass, 0 errors, 1 warning (the intentionally null immutable release reference).
- Post-refresh link audit: 967 unique URLs across 1,978 displayed link occurrences; 1,611 reachable and 363 access-restricted occurrences, with 2 http_error and 2 missing occurrences (2 unique URLs), both on pre-existing records. New and changed records resolved with 0 missing and 0 network errors. Restricted responses are authentication, bot-protection, rate-limit, or redirect-gate outcomes and are not classified as broken.

## Accepted additions (42)

**dna (6)** — MarinDNA; CENO; LDARNet; Carbon (Carbon-500M / 3B / 8B); ModernGENA (base / large); BOTANIC-0 (Botanic0-S / -M / -L).

**rna (7)** — UTRGen; Shifu-LMR; NUMonomer; RNAPro; RNAElectra; DGRNA; RibonanzaNet2.

**protein (3)** — ProtGPT3; MSA Pairformer; ProLLaMA.

**complex (3)** — Nesso-1; Promera; DeCAF (DeCAF-Boltz).

**molecule (7)** — FeNNix-Bio1; CheMatE; Molexar; NovoMolGen; ReaSyn (NV-ReaSyn); MiniMol; CheMeleon.

**singlecell (1)** — PerturbGen.

**spatial (9)** — PRISM2; KRONOS2; GigaPath-Flash; ALICE; TissueFormer; CellWorld; SEAL; SpatialFusion; Path Foundation.

**multimodal (2)** — MKB (Monkey King Bang); MGM2.

**platform (2)** — NVIDIA BioNeMo Agent Toolkit; Boltz Lab / Boltz API.

**benchmark (2)** — GENEB; PG-LLM.

Access wording distinguishes code, weights, gating, non-commercial terms, and no-licence states per record. Fourteen of the new records are `verified_with_limits` because of a gate, a non-commercial licence, an undeclared licence, or checkpoints hosted on a personal cloud drive; the rest are `verified`.

Not all additions are in-window releases. Several are older catalog gaps closed by this sweep (MiniMol 2024, ProLLaMA 2024, DGRNA 2024, CheMeleon 2025, NovoMolGen 2025, MSA Pairformer 2025, FeNNix-Bio1 2025, RibonanzaNet2 2025, Path Foundation 2023). Their record years reflect the release, not the review date.

## Promotions from the under-review register (3)

- **ChemBERTa-3** — the recorded condition (platform scope plus explicit reuse terms) is met: the work is now published in Digital Discovery under DOI 10.1039/D5DD00348B, the framework repository is MIT, and the released c3 checkpoints carry MIT on their model cards. The paper link was upgraded from the ChemRxiv PDF to the journal DOI. Two smaller c3-MoLFormer repositories still contain no weight files and are not cited as artifacts.
- **Virchow / Virchow2 (and Virchow2G)** — the family-terms condition is met by encoding member-specific terms rather than one family-level flag: Virchow is Apache-2.0 behind an automatic gate, Virchow2 is CC BY-NC-ND-4.0 non-commercial behind an automatic gate, and Virchow2G (and Virchow2G-Mini) are commercial-licence-only with no public weights and no verified paper. Record-level `noncommercial` is therefore true and the status names the Apache-2.0 member explicitly.
- **H-optimus-0 / H-optimus-1** — both model cards were verified with distinct terms: H-optimus-0 Apache-2.0 auto-gated, H-optimus-1 CC BY-NC-ND-4.0 behind manual approval with an institutional email. No peer-reviewed paper or preprint exists for either model, so the listed "paper" was relabelled as a company announcement.

## Cross-slice adjudications

- **RibonanzaNet2 — accepted.** One slice held it after the Kaggle model page returned only a JavaScript shell; the RNA slice, tasked with settling its status, read the same model through the Kaggle public API (ungated, MIT on the released alpha instance) and corroborated ownership through the Das lab preprint's methods text and NVIDIA's official RNAPro repository. Identity, artifact and terms are therefore resolved and the record was added, with the alpha status and the absence of a dedicated RibonanzaNet2 paper stated in the record.
- **scMamba (multi-omics integration) — held.** One slice accepted it, another held it. Neither could enumerate the checkpoint files, which are offered only through a share page that does not render a listing, and the two lanes read the repository README differently. The conservative reading prevails and the candidate entered the register instead of the catalog.
- **GeneMamba — held.** A discovery lane proposed it as a new record on the strength of an Apache-2.0 header in the weights repository. The register re-review read the licence body and found it is not the verbatim Apache-2.0 text (altered patent grant, modified derivative-works definition), while the code repository carries no licence at all. The existing hold `bfm-genemamba` stands and no new record was created.
- **scMamba name collision** — two unrelated models share the name. Both are now held under disambiguated names (`bfm-scmamba-multiomics`, `bfm-scmamba-snrna`) so they can never be merged by a later sweep.
- **Tabula** — a rediscovered candidate was matched to the existing hold `bfm-tabula` rather than added. Its new evidence (a 2026 arXiv version under a different title, plus a federated-orchestration companion platform) was folded into that entry, which explains the title mismatch between the repository README and the cited preprint. Still no reusable checkpoint.
- **PRISM2** — accepted as its own record, and the existing PRISM record was narrowed to PRISM v1 in the same migration so the two do not carry duplicate links and descriptions.

## Verification holds (10 new register entries)

JUMP-lite (with Nahual); AQAffinity; PlantHelixSeek; SeqLens v2 (with mgxLens v2); ScreenShot; SPgen; OmicsLM; X-Cell / X-Cell-Ultra; scMamba (snRNA-seq, neurodegeneration); scMamba (multi-omics integration).

Each carries a reserved `bfm-*` ID, quoted licence or availability evidence, a structured reason class, and an explicit `reconsider_when`. The dominant blockers are missing reusable artifacts (X-Cell, OmicsLM, SPgen, both scMamba entries, JUMP-lite's undelivered data bundle) and missing or absent licences (ScreenShot, SPgen, mgxLens v2).

## Notable rejections (10)

- **Cherimoya Accessibility aTlas (CATv1)** — real, officially owned artifacts, but the release is thousands of per-experiment supervised models with no general checkpoint; the card itself says a model reflects only the experiment it was trained on.
- **DrugGen 2** — a GPT-2/DrugGPT fine-tune rather than broad pretraining, by the model card's own base-model declaration.
- **WattmaMod** — genuine self-supervised pretraining and released weights, but all eleven heads perform the same nanopore modification-calling task; label extension is not task transfer.
- **CARTA** — a dearraying and tissue-masking utility (detector plus segmenter) supporting a spatial-proteomics pipeline, not a pretrained representation model, and with no dedicated paper.
- **CYP ranking benchmark** — one unnamed single-family ranking dataset, with no licence on the artifacts that carry it.
- **Ptarmigan-1**, **ProtBLIP2-SST** — verified preprints with no public code, weights, or endpoint anywhere in the manuscript.
- **PoreBERT-DNA-VQI** — no paper, unaffiliated individual account, empty training-data repository, self-contradictory licence.
- **Lingshu-Cell** — the official collection still contains only the paper; the sole hub upload carrying that name is unaffiliated. It also remains a hold-register entry.
- **scUNVEIL** — a data-preparation and from-scratch training pipeline with no released weights and no paper.

## Update checks

Both foundation-model items in `evidence/additions-2026-08-13/update_checks_result.json` resolved to no action:

- **OpenDDE** — the existing preview record already carries the full-release paper, the official repository, the ungated Apache-2.0 weights, and an accurate status string; re-verified, nothing to change.
- **IgGM2** — no official artifact exists (the expected successor repository returns not-found) and the reported successor preprint was not independently fetched, so no record note was added. Watchlist.

## Watchlist for the next cycle

- **IgGM2** — reconsider when an official repository or weights, or a verified preprint DOI, exists.
- **DeCAF-Pearl** — described in the DeCAF paper but not released; only DeCAF-Boltz weights ship.
- **Virchow2G / Virchow2G-Mini** — commercial-licence-only today; revisit if public weights or a technical report appear.
- **Aignostics RudolfV-2 family** — gated weights appeared on the vendor's hub organisation with unreadable terms; a separate candidate record, not evidence for the held Atlas entry.
- **PlantRNA-FM** — promotable standalone on today's evidence once the held mRNA-FM / PlantRNA-FM family record is split; mRNA-FM still lacks its own primary publication.
- **X-Atlas/Pisces** — the dataset repository accompanying X-Cell was not verified this cycle.
- **MicroGenomer**, **Unify** — named in the coordinating brief as leads for this cycle, but no supporting entry exists in the delivered 2026-08-13 evidence files. **UNVERIFIED**; carried forward only as names to check, with no claim attached.

## Evidence and reproducibility

Per-candidate verdicts, quoted licence sentences, and per-claim source URLs are stored in `evidence/additions-2026-08-13/` (thirteen verification slices plus the update checks) and `evidence/hold-review-2026-08-13/` (four register re-review slices). The exact applied set is `scripts/apply_2026_08_13_refresh.py`, which is idempotent: a second run leaves every data file byte-identical. Full post-refresh URL-resolution results are stored in `evidence/link_audit.tsv`.

Not checked in this cycle: whether the restricted (gated, rate-limited, or bot-protected) URLs would resolve for an authenticated user; the contents of checkpoints hosted on personal cloud-drive folders, which were confirmed to exist and be publicly listed but were not downloaded; and any non-public or partner-gated access route for commercial systems.
