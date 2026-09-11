# Foundation Models discovery and verification audit — 2026-09-11

> Historical review-stage snapshot. Publication was subsequently authorized; see [release packaging](RELEASE_2026-09-11.md).

This is a **local, unpublished 2.2.0 preview** against baseline commit `66cef15df536f57c6e3ac0f581638d952493a5da`. No remote repository, release, tag or deployment was changed. Review and acquisition dates below refer to **11 September 2026**, not a future planned release.

The baseline contained 390 displayed records and 39 held candidates. The final preview contains **400 displayed records (258 verified, 142 with limits) and 44 held candidates**: 11 additions/promotions, the existing ALICE record returned to HOLD, and one targeted GPN-MSA publication/lifecycle update. The original 39 HOLD conditions were all reconsidered. Two family holds became three independently described displayed members plus two residual held members; four further discoveries were held. The ALICE demotion is an additional current-access finding.

## Scope, discovery and identity control

The sweep targets the interval after the 13 August refresh through 11 September, with deliberate overlap for previous gaps, older family holds and the prior watchlist. Names and aliases were normalized before discovery across both stores; the 429-record identity baseline is in [normalized_identity_baseline.json](refresh-2026-09-11/normalized_identity_baseline.json). Discovery used broad and date-qualified searches followed by primary paper, author repository, archive and model-hub reads. Search often ignored date/domain hints or resurfaced older work. This is a bounded discovery sweep across every modality, **not a systematic literature review or an assurance that every release was found**.

[discovery_coverage.json](refresh-2026-09-11/discovery_coverage.json) preserves representative executed queries, outcomes and overlap. No-addition lanes are explicit:

| Modality | Displayed change | Reviewed leads and outcome |
|---|---|---|
| DNA | +GPN-Star, +MicroGenomer; GPN-MSA targeted update | September GPN-Star paper; older MicroGenomer ownership/artifact gap resolved. SUCCEED remains held for exact terms; HybriDNA/GeneMamba concerns remain. |
| RNA | +RIBOSPAN, +NucleicBERT, +PlantRNA-FM | August RIBOSPAN release; September NucleicBERT article with 2025 archived weights; older plant/mRNA family split. Residual mRNA-FM held. |
| Protein | +MultiFlow, +FrameFlow | Older family ambiguity resolved for two members. FrameDiff remains scope-held. IgGM2 and AINN-P1 have primary manuscripts but unresolved current reusable artifacts. |
| Complex | No addition | DeCAF-Pearl not separately identified in current release files; held structural families reviewed. KinConfBench classified as benchmark. |
| Molecule | +Monroe, +Mol-JEPA | August encoders with public artifacts; downstream predictor and noncommercial terms separated. |
| Single cell | No addition | Unify is a dataset-trained integration/perturbation method; ScDiVa now has weights but loader usability remains unresolved. OmicsLM and the existing holds revisited. |
| Spatial / tissue | ALICE → HOLD | RudolfV-2 exact gated terms unreadable; Virchow2G release not newly established; nnMIL is aggregation; TissueFormer already present. |
| Multimodal | No addition | CAPTAIN already present; Intern-S2-Preview routed to the agent-index reviewer as a general scientific agent lead. X-Cell remains release-held. |
| Platform | No addition | Genesis Open Models Initiative is an announcement, not a released biological-model artifact. PoET-2 already has a separate displayed record. |
| Benchmark | +LAMBDA, +KinConfBench | Reusable evaluation artifacts and distinct code/data terms verified. JUMP-lite compressed-image release condition remains unmet. |

## Decisions and evidence boundaries

All 27 candidate/watchlist/correction decisions are in [candidate_decisions.json](refresh-2026-09-11/candidate_decisions.json); all 39 original hold-condition reviews, with their original reconsideration wording and acquisition references, are in [hold_reviews.json](refresh-2026-09-11/hold_reviews.json). Compact locators, excerpts, artifact fields and observations are in [claim_evidence.json](refresh-2026-09-11/claim_evidence.json). Individual `*manifest.json` files preserve exact requested URLs, timestamps, access levels, HTTP outcomes and response hashes. Raw third-party page/code/PDF bodies remain only in ignored `.maintenance-output/fm-source-cache`, not in the public evidence bundle. No weights or large data archives were downloaded or executed. Hashes refer to acquired response bytes; local cached text may be decoded from a GitHub API envelope or extracted from a PDF.

Primary-source access is not inferred from HTTP success alone. Fifteen direct responses were identified as challenge pages despite HTTP 200. Selected NucleicBERT, GPN-Star and KinConfBench article sections were obtained separately through web retrieval; those observations have their own access provenance and no fabricated response hash. LAMBDA's inspected full text is the March preprint, while September journal identity is metadata-level evidence. AINN-P1's 12-page document is a vendor-hosted March technical manuscript; it was not independently verified as a deposited bioRxiv version. API metadata and file listings prove the observed terms/access state, not successful execution or model performance.

### Additions, family splits and corrections

- **RIBOSPAN:** Apache-2.0 implementation; distinct custom noncommercial model licence also restricts output-derived use and commercial R&D. Family landing repo is documentation-only. Two 1K checkpoints list public weights, 10K-15 is manually gated, and 10K-40 is not released. No access request or gated download was made.
- **Monroe:** MIT released encoder and checkpoint pointer; reusable 720-dimensional graph embeddings. The reported downstream TabPFN v3 weights require separate licence acceptance/access. Do not treat encoder MIT as permission for the complete external prediction stack.
- **NucleicBERT:** primary paper, Apache-2.0 implementation and Apache-2.0 Zenodo pretrained/task archive. The model year follows the 2 September 2025 archive; journal publication is 3 September 2026. RNA structure/contact/splicing/fitness capabilities are downstream tasks, not claims of universal zero-shot performance.
- **GPN-Star:** separate identity from GPN-MSA/PhyloGPN; MIT implementation and three independently inspected MIT human checkpoints. Whole-genome alignment and species context are required. The 2025 preprint determines the year; the September 2026 paper is the current journal record. No blanket licence statement for every dataset/species is made.
- **Mol-JEPA:** official corporate repository links the author-hosted safetensors release. README explicitly applies CC BY-NC 4.0 to the model **and source code**.
- **MicroGenomer:** official BGI repository directly links the 470M author-hosted checkpoint; code licence and model metadata specify MIT. Genome-labelled coding DNA CSV input, genomic embeddings and trait heads are distinguished from a general DNA chat model.
- **LAMBDA:** reusable genomic-model benchmark; MIT code, CC BY 4.0 archived data/results/probe heads. The public small checkpoint archive is not the underlying EVO2 weights. Non-EVO2 fine-tuned task checkpoints are separately author-request-only.
- **KinConfBench:** named benchmark, not a new foundation model. UC Regents code terms permit educational/research/not-for-profit use; Figshare inference data are CC BY 4.0. The published 2,225-chain count is the filtered human kinase benchmark, not a claim that every PDB kinase is covered.
- **PlantRNA-FM:** retains `bfm-mrna-fm-plantrna-fm` as stable successor of the old combined family. Primary paper and author-attributed MIT hub artifact support the plant member independently. Released base embeddings are distinguished from task predictions requiring fine-tuning. Residual `bfm-mrna-fm` stays held: its cited card says unofficial conversion and AGPL-3.0, which does not resolve original mRNA-specific provenance/terms.
- **MultiFlow / FrameFlow / FrameDiff:** original `bfm-framediff-frameflow-multiflow` follows MultiFlow; new `bfm-frameflow` covers FrameFlow. Both have MIT implementations and separately CC BY 4.0 weight archives. MultiFlow documents co-design, inverse folding and forward folding; FrameFlow documents unconditional generation and motif scaffolding. FrameDiff's independently identified release remains held under `bfm-framediff` because only unconditional backbone generation was established under the current broader-than-one-task boundary. No inclusion-policy exception was added.
- **GPN-MSA:** existing primary preprint identity is correct. Added the final Nature Biotechnology locator and official deprecation in favor of GPN-Star. This partial check retains the old `verified` date.
- **ALICE:** GitHub page and raw README return 404; the GitHub connector independently reports NOT_FOUND. Model API/card return 401. Historical cached search text cannot establish current usable access. Original ID, descriptive history, links and prior verification date are preserved in HOLD pending restored/replacement official access and readable terms. **No discontinuation is inferred.**

### Material HOLD findings

- **ScDiVa:** prior absence of artifacts is now historical. Author-named code and linked Apache-labelled model files are public. Static inspection of `from_pretrained` finds that it selects `model.safetensors`, passes it to `torch.load`, and returns a model after warning/error messages on a failed load. This is a code-inspection concern about potentially random initialization; it was **not** a model execution test. Promotion requires a verified usable loader/checkpoint pair.
- **HybriDNA:** a purported 3B upload has Apache metadata but describes the 300M model and lacks established author-controlled provenance from the inspected preprint. It was not substituted for an official release.
- **GeneMamba:** the old repository locator currently returns 404; hub licence metadata does not resolve the earlier modified-licence concern. A restriction or missing locator is not proof that no copy exists elsewhere.
- **JUMP-lite:** bounded public S3 listing found a metadata-prefix README dated 3 September, but the exact compressed-image prefix had `KeyCount=0`. A public CC0 index archive does not meet the original image-and-metadata release condition.
- **SUCCEED, IgGM2, AINN-P1, RudolfV-2:** retained as explicit new HOLD candidates for the documented missing terms, release or readable gated conditions. AINN-P1's manuscript explicitly promises weights/evaluation code upon publication; vendor performance prose was not treated as artifact availability.

Other holds received condition-focused source review, not a fresh verification of every inherited claim. Their prior `verified` values are preserved. Family labels are not used to transfer one member's licence or release status to another.

## Reproducibility and narrow maintenance fixes

[apply_2026_09_11_refresh.py](../scripts/apply_2026_09_11_refresh.py) applies the frozen [reviewed_changes.json](refresh-2026-09-11/reviewed_changes.json) payload. Running it twice leaves canonical data, register and metadata byte-identical. Existing IDs survive corrections, demotion and named family successors; only genuinely separate records receive new IDs. Version is 2.2.0, metadata date is 2026-09-11, baseline is actual HEAD, and `release_ref` remains null. No global verification-date refresh was performed.

The old schema allowed only four historical `audit_source` paths. A backwards-compatible provenance fix now also accepts dated `evidence/refresh-YYYY-MM-DD/{candidate_decisions,hold_reviews}.json` paths; changed/new claims and current hold reviews point to their real September source. Preview validation also requires the referenced file to exist. Existing historical paths remain valid. This is a provenance repair, not a change in admission policy, publisher identity, catalogue licence or release approval. Fixture tests accept the new dated path and reject a schema-valid path to a missing evidence file.

The version badge tooltip now describes the catalog version and metadata modification date, so an unpublished preview does not imply a published update. Canonical status wording follows existing explicit open/hub conventions without conflating public weights, gating, use restrictions, downstream-model access or paper-only evidence. All HTML, Markdown, JSON copies and FAIR distributions were regenerated through the build.

## Validation and URL audit

The initial full live audit fetched **1,008 unique URLs across 2,063 occurrences**, using 12 workers and a maximum of two concurrent requests per host. It recorded 808 reachable, 199 restricted, and one missing URL (ALICE GitHub, appearing twice). Exact initial evidence is preserved in [full_link_audit_initial.tsv](refresh-2026-09-11/full_link_audit_initial.tsv), including the 404.

After ALICE was demoted, the canonical link TSV was mechanically reprojected from those same fetched observations onto the remaining canonical occurrences: **1,005 unique URLs / 2,057 occurrences, 807 reachable, 198 restricted, zero missing or network/server errors**. No outcome, status, timestamp or redirect was softened. The removed three ALICE URLs remain in the initial audit and the held record. [link_audit.tsv](link_audit.tsv) covers every current canonical URL. HTTP reachability is not semantic source verification; restricted responses and success-status challenge pages still need the access qualifications above.

- Migration idempotence: pass.
- Deterministic build and preview validation: pass; 16 generated artifacts byte-stable.
- Full JSON Schema, stable-ID/name/date invariants and canonical-data immutability: pass.
- Maintenance fault-injection suite: all ten scenarios pass, including the new valid/missing evidence-path cases; real catalogue unchanged by simulation.
- Strict release validation: intentionally blocked by null `release_ref`; publication remains unapproved.
- `git diff --check`: pass.

Independent reviewers checked a shuffled selection of admissions/terms/artifacts and the ScDiVa hold. PlantRNA-FM task-output wording and ScDiVa warning/error wording were corrected from that review. Root reviewer is responsible for final browser/integration assessment. This audit does not authorize publication.
