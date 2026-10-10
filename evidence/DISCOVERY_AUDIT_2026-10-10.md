# Biological Foundation Models discovery audit — 2026-10-10

## Local preview and result

This is an unpublished **2.3.0 preview** on branch `agent/v2.3.0-2026-10-refresh`, derived from commit `1d07d78` (full SHA in `refresh-2026-10-10/reviewed_changes.json`). `release_ref` remains null. No push, release, tag or remote write was performed.

- Baseline: 400 displayed records, 44 under review.
- Added: 80 displayed records (79 from discovery plus RCLM, split out of the DRfold hold).
- Promoted from the under-review register: 7 (HybriDNA, mRNA-FM, NeuralPLexer, Tabula, RudolfV 2, OpenProtein.AI, JUMP-lite).
- Moved to the register: Molexar (official code withdrawn).
- Corrected existing records: 32.
- Current catalog: **486 displayed records**, **37 under review**.

| Modality | Added this cycle |
|---|---|
| DNA (12) | BOTANIC-1, Cerberus, Evo2HiC, GENERanno, LOAM, MicroGlot, Minerva, NTv3, RAGenome, RegFM, TomatoPGFM, gLM2 |
| RNA (6) | CodonMamba, EukaUTR, La-Ribo, RCLM, Trias, mRNA-GPT (Kitasato) |
| Protein (8) | AAMFM, GearNet, IDiom, InstaNovo-FM, Profluent-E1, Prot-LAMBDA / LambdaFold, ProteinSage, ProteomeLM |
| Complex (3) | AtlasFold / AtlasLM, BioKinema, ODesign |
| Molecule (14) | AIMNet2, AceFF, Atom-JEPA, DPA4 / DPA4C, DreaMS, GRACE-OFF, GRASP, KERMT, LDDM, MACE-OFF, ShEPhERD-2, Zatom-1, ether0, nach0 |
| Single cell (7) | CellMSA, CytoBERT, EpiZoo, InstructCell, LucaCell, scMaize, scRep |
| Spatial / pathology (12) | AIDO.Tissue, CELL-FM (virtual microscopy), CROWN, CTransPath, CytoFormer, DistillPath, ELF, HEIST, HIPT, NexuST, OpenMidnight, stFormer |
| Multimodal (4) | Evolla, InsilicoCell, OmicsFM, PertMind |
| Platform (4) | BioLLM, BioPipelines, gReLU, scUnify |
| Benchmark (10) | BEACON, HEST-1k, MUBen, Riptides, Runs N' Poses, SABLE, Synthetic Genomes Benchmark, UKBBGym, ViroBench, mRNABench |

Part of this volume is catch-up rather than new releases. Canonical older models that the index lacked (for example GearNet, HIPT, CTransPath, AIMNet2, MACE-OFF, gLM2) surfaced through the candidate feed and the modality lanes and passed the same gates.

New and promoted records carry `verified: 2026-10-10`. Corrected records carry `date_modified: 2026-10-10` and keep their earlier verification date unless every claim was re-checked (UMA). Of the 80 additions, 78 are `verified_with_limits`. Their audit notes name the limit: access terms, gating, missing licence text, or maturity.

## Method

Twelve independent lanes ran: one per modality, a calibrated-uncertainty lane, and a lane for the bio.rodeo candidate feed plus the carried watchlist. Each lane checked candidates against a normalized identity baseline of all 444 displayed and held names, aliases and URLs. The main window was 2026-09-11 to 2026-10-10, with a second sweep back to 2026-08-13. Channels were the arXiv API and web search, bioRxiv by date and category, Europe PMC, newest Hugging Face models, new GitHub repositories, and targeted reads. Web search was rationed. Lanes report about 81,500 screened metadata items; queries overlap, so this is not a count of distinct papers.

Every proposed addition and every promotion went to a separate agent instructed to refute it. That agent re-fetched the primary sources and checked identity (including same-name collisions), scope, released artifact, exact terms for code, weights, data and API, every URL, and the wording. Of 89 such reviews, 87 confirmed the proposal (every one with corrections, which were applied) and 2 sent it back to hold (Protein UQ benchmark, VISTA-PATH). A refuted proposal was never admitted. Corrections proposed for existing records went to a third agent per record, which accepted 30, made no change to 3, and rejected anything it could not confirm.

All 44 held records were re-reviewed against their recorded `reconsider_when` conditions, and every promotion had its own adversarial review. No weights were downloaded or run.

Machine-readable decisions: [`candidate_decisions.json`](refresh-2026-10-10/candidate_decisions.json) (every candidate, lane, decision, sources and the reviewing agent's checks), [`hold_reviews.json`](refresh-2026-10-10/hold_reviews.json) (every held record) and [`reviewed_changes.json`](refresh-2026-10-10/reviewed_changes.json) (the migration payload).

## Gaps carried from August and September

- **Calibrated uncertainty.** The index had no record whose distinguishing feature is calibrated uncertainty. The lane added **MUBen**, a benchmark of uncertainty quantification on pretrained molecular models. A protein-engineering UQ benchmark was sent back to hold by its reviewer. Two in-window candidates are held: a confidence audit of single-cell foundation models, and RegimeFormer (weights on request). Methods without a reusable pretrained artifact (Kermut, RaCoon, DEGU, CalPro) and single-task predictors (AlphaMissense, popEVE) were rejected. Existing records now state their confidence outputs where a primary source supports it (AlphaFold2, AlphaFold 3, EVE); scTab, Monroe and Boltz were checked and left unchanged. This remains thin coverage. Calibrated uncertainty is still rare among released biological foundation models, and the index does not widen scope to single-task predictors to fill the gap.
- **bio.rodeo feed.** The feed stopped adding entries after 2026-09-14 (sitemap unchanged on 2026-10-10), so it covers only 11–14 September of the main window. The lane parsed 2,565 model cards and diffed them by name against the baseline. It screened the 179 entries dated from 2026-08-13 and opened 84 detail pages for plausible in-scope entries. The 2,160 older name-level "new" entries were not screened systematically; conspicuous gaps met during review were verified and several were added (above). Feed entries are leads only; every admission rests on primary sources.
- **Watchlist.** *Vilya* resolves to Vilya Inc.'s macrocycle models Vilya-1 and Vilya-2: no code, weights or access route, so rejected. Their public Riptides benchmark was added separately. *Unify* is unchanged and remains a rejected method. *MicroGenomer* (added in September) is still consistent. *NeuralPLexer3* now has a Crossref-registered NeurIPS 2025 article but still no released artifact; it remains held under the new ID `bfm-neuralplexer3` after the family split.

## Held records

- **Promoted (7):** HybriDNA (author ownership of the hub uploads now established), mRNA-FM (official loader and weights), Tabula (checkpoints linked from the official tutorials), RudolfV 2 (exact terms readable: CC BY-NC-ND 4.0 plus restrictive supplementary terms), JUMP-lite (stores now listable), OpenProtein.AI (narrowed to the platform), and NeuralPLexer v1 (split from NeuralPLexer3, keeping the family ID).
- **Split without changing ID meaning:** DRfold's pretrained RNA language model RCLM is a new displayed record (`bfm-rclm`). `bfm-drfold` stays held for the DRfold structure predictor.
- **Retired from the register (4), each documented in `hold_reviews.json`:** SATURN (a per-analysis method, not a reusable pretrained model), xTrimoGene (merged into scFoundation by its authors; now an alias of `bfm-scfoundation`), scPROTEIN (no broader pretraining) and SPgen (no released weights).
- **Kept on hold (33),** with refreshed reasons. Seven of them (DeepSEA, ChromBPNet, ProtGPS, ABodyBuilder3, FrameDiff, Uni-Mol Docking V2, DRfold) wait on a written structural or single-purpose model exception that MAINTENANCE.md does not contain. This is a curator decision, not an evidence gap.
- **New on the register:** Molexar (code and its required dependency withdrawn; weights still public but not loadable without them), NeuralPLexer3, and the two candidates sent back by their reviewers.

Discovery leads that a lane held, and that no reviewing agent examined, are recorded in `candidate_decisions.json` as leads (`lead_only`). They are not placed on the public register. The next cycle re-reviews them.

## Corrections to existing records

32 records changed. Most changes update moved repositories or hub organisations (GenBio's AIDO → GB renaming, NVIDIA-Digital-Bio → NVIDIA-BioNeMo, EvolutionaryScale → Biohub for ESM3, the GenomeOcean hub move), journal versions of preprints (PlantCAD2, CheMeleon, SpaPath-Bench, State), access and licence wording (OpenFold3's default OpenBind-0 parameters, BioReason-Pro's new code licence, MIMIC weights now released, Helical's AGPL code), and archived upstream repositories (Chemformer, IBM materials). The UMA documentation link moved to the new FAIR Chemistry docs host; this fixes the link audit that had failed weekly since 2026-09-14.

## Coverage limits

This is a bounded discovery sweep with adversarial verification of every admission. It is **not a systematic literature review and does not assure that every release was found**. In particular, the arXiv API returned HTTP 429 to several lanes, so they fell back to title-level web search. medRxiv and ChemRxiv were not harvested in every lane. Name-level feed diffing misses renamed models. Only records with a proposed correction were re-verified; the other displayed records keep their earlier verification dates.

## Local checks

- The dated migration (`scripts/apply_2026_10_10_refresh.py`) is idempotent: a second run left the catalog and register byte-identical.
- `build.py`: 16 generated artifacts byte-stable. `validate_catalog.py`: pass (one expected warning, null release reference). `git diff --check`: clean.
- Link audit: 1,503 unique URLs across 2,930 occurrences: 2,198 occurrences reachable and 693 restricted; none missing. The 39 occurrences that returned 503 or timed out under burst load were confirmed through the GitHub, Crossref, DataCite and Zenodo APIs. Hugging Face answered most audit requests with 429, so every Hugging Face repository URL was re-checked slowly through the Hub API; all resolve except the held ALICE repository. Restricted bioRxiv and publisher pages (bot blocks) were not re-checked and are not counted as verified. Details: [`refresh-2026-10-10/link_recheck.json`](refresh-2026-10-10/link_recheck.json).
- `validate_catalog.py --release` is expected to fail only on the null release reference. Governance was not weakened.

Publication remains a separate step that needs the owner's explicit approval.
