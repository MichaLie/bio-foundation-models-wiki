# Biological Foundation Models discovery audit — 2026-07-13

## Scope and method

This is the durable evidence summary for the protected local FAIR preview. Three independent discovery lanes covered sequence/genomics/RNA/protein, structure/interaction/chemistry, and omics/spatial/multimodal/platforms/benchmarks. Candidate sets were then shuffled to a different reviewer for adversarial checks of identity, deduplication, scope, paper/project matching, public artifacts, access, and licence wording. The primary editor adjudicated disagreements conservatively and applied the accepted set through `scripts/apply_2026_07_13_discovery_refresh.py`.

Acceptance means that the record is decision-relevant and its identity and cited sources were verified. It is not an endorsement of benchmark claims, scientific superiority, safety, or fitness for a particular analysis. `verified: 2026-07-13` records the evidence-review date.

## Result

- Baseline records: 323.
- Added after discovery and cross-review: 54.
- Current preview records: 377.
- Existing records materially updated by the dated migration: 12.
- Additional existing-record corrections already made in this preview: ProteinGym and ProteinBench, plus earlier URL/status corrections documented in the project decision log.
- Deterministic build: pass, 10 byte-stable generated artifacts.
- Preview validation: pass, 0 errors; resource licence and formal publisher remain explicit warnings and release blockers.
- Post-refresh link audit: 828 unique URLs / 863 occurrences; 607 reachable, 221 access-restricted, 0 missing, and 0 network errors. Restricted responses are authentication, bot-protection, rate-limit, or redirect-gate outcomes and are not classified as broken.

## Accepted additions

### Sequence, genomics, RNA, protein and cross-modal protein

SPACE; BMFM-DNA; Omni-DNA; NucEL; D3LM; OneGenome-Rice; HydraRNA; structRFM; CodonFM / EnCodon; Ankh3; ESM-S; Proust; Ab-RoBERTa; OneProt; ProtDAT.

### Structure, interaction, chemistry, platforms and benchmarks

ESMFold2; OpenDDE Preview; PocketXMol; Suiren-1.0; UBio-MolFM; UMA; SeedFold / SeedFold-Linear; BoltzGen; PXDesign; BoltzMol-1; BoltzProt-1; SeedProteo; AlphaProteo; Rosetta Foundry; FoldBench; PXMeter; PFMBench; Protein-SE(3); ESM Atlas.

RoseTTAFold3 was not added separately: it was merged into the existing RoseTTAFold All-Atom family record. RFdiffusion3/RFD3 was likewise represented by updating the existing RFdiffusion family record.

### Omics, single-cell, spatial, multimodal, platforms and benchmarks

BioMatrix; GeneJEPA; EVA (Scienta); GenBio-PathFM; SQUALL; SpatialWhisperer; DeepSpot-M; H2O; LEMON; MuPD; BioAIrepo; VCBench; SCMBench; SpaPath-Bench; GPT-Rosalind; MIMIC; HoloCell; CellOS; OmniCell; BioReason-Pro.

BioReason-Pro was retained as a separate sibling because it is a protein-function reasoning system, while the existing BioReason record is DNA-focused. HoloCell, CellOS, and OmniCell were retained separately because they are unrelated model families with different modalities and artifacts.

## Existing-record updates accepted

- ESM-C / ESM Cambrian: current Biohub repository and open ESMC/ESMFold2 release.
- RFdiffusion: family name and aliases now cover RFdiffusion3/RFD3; preprint updated to v2.
- RoseTTAFold All-Atom: family record now covers RoseTTAFold3/RF3 and Foundry artifacts.
- AlphaGenome: research code, gated public weights, non-commercial terms, and API boundary distinguished.
- PlantCaduceus / PlantCAD / PlantCAD2: successor scope and public artifacts updated without claiming resolved checkpoint reuse terms.
- ProGen3, PoET-2, xTrimoPGLM, Chroma: current public artifacts and non-commercial restrictions made explicit.
- AbLingua: current public checkpoint reflected without claiming unreleased family models or training code.
- CAPTAIN: public checkpoints/data reflected; checkpoint terms remain qualified.
- CZI Virtual Cells Platform: current Biohub operator/branding reflected with legacy aliases preserved.
- ProteinGym: corrected to open benchmark code and data with a public leaderboard.
- ProteinBench: unsupported open-code/weights claim removed; project leaderboard retained and repository absence stated.

## Held or rejected leads

The following were deliberately not added or not upgraded:

- CELLama — hold: peer-reviewed method and open implementation, but no dedicated released pretrained CELLama checkpoint was confirmed; it currently wraps external SentenceTransformer weights.
- MACH — reject from the index: useful FAIR discovery infrastructure, but it is a catalog rather than a model, model platform, or benchmark. Its Zenodo access/licence metadata also conflicts with the live repository.
- LDARNet — hold: paper identity confirmed, but independent artifact verification was insufficient at the decision point.
- RibonanzaNet — hold: reusable implementation exists, but it remains a specialized Kaggle-derived RNA-reactivity/structure predictor; inclusion would require an explicit scope decision.
- JEPA-DNA — hold: no released pretrained checkpoint confirmed.
- S2ALM — hold: the declared repository was unavailable.
- HybriDNA status upgrade — hold: model-hub artifacts appeared public, but paper/project-to-account provenance was not sufficiently confirmed.
- A-CODE, DCFold, Proteo-R1, Uni-Mol3, OpenComplex, IsoDDE, BindCraft, Interformer, GEMS, DualBind, RFDpoly, AnthroAb, AntibodyDesignBFN, AgForce, RNARL, RNA-Design-LM, and other narrow or artifact-poor leads — rejected or deferred for scope, maturity, duplication, or evidence reasons.

## Adjudicated evidence disagreements

- SQUALL: one cross-check initially reported paper-only. Direct review of the official repository showed model source, pretrained-weight and Zenodo pretraining-data links. The repository licence is CC BY-NC-ND 4.0, so the record is open to inspect but explicitly non-commercial and non-derivative.
- H2O: the repository README claims a bundled checkpoint at `code/example/best_epoch.pth`, but that referenced file returned 404 during direct verification. The repository says “All rights reserved.” The record therefore says public source, absent referenced checkpoint, and no reuse licence.
- OmniCell: later primary-source review found a public source repository and a public ModelScope checkpoint; the final record reflects these artifacts rather than the earlier paper-only assessment.
- MuPD: the canonical paper name is MuPD; MuPaD and MUPAD are retained as aliases.

## Primary evidence

Every accepted record stores its paper and official project/repository/model links directly in `models_final.json`. The dated migration is the exact machine-readable decision set. Full post-refresh URL-resolution results are stored in `evidence/link_audit.tsv`.
