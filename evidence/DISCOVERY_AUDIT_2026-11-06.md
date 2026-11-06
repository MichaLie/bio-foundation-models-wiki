# Biological Foundation Models discovery audit — 2026-11-06

## Local preview and result

This is an unpublished **2.4.0 preview** on branch `agent/v2.4.0-2026-11-refresh`, derived from commit `dd48d49` (the published 2.3.0 release; full SHA in `refresh-2026-11-06/reviewed_changes.json`). `release_ref` remains null. No push, release, tag or remote write was performed.

- Baseline: 486 displayed records, 37 under review.
- Added: 52 displayed records (41 from this cycle's discovery lanes, 11 from the re-review of October's discovery leads).
- Promoted from the under-review register: none.
- Placed on the under-review register: 40 October leads that a second agent judged substantive and in scope, each with a specific open condition.
- Corrected existing records: 18.
- Current catalog: **538 displayed records**, **77 under review**.

| Modality | Added this cycle |
|---|---|
| DNA (6) | Bolero, DeepD, DNABERT-S, ProkBERT family, Shorkie, USM-AA |
| RNA (7) | CaLM, LIMBER, mRNA-LM, ProtRNA, RESM, RiboGRAM, SynCodonLM |
| Protein (14) | AbBFN2, AlphaEnzyme, AlphaProtein Novo, Ares, AtomWeaver, BacPT, GenCDR, InstructPro2, Prompteina, RFD4-Proteina, RigidSSL, S-PLM, TriProRep, recAMPLIFY |
| Complex (1) | K-Fold |
| Molecule (2) | SO3LR, Zatom-2 |
| Single cell (4) | BMFM-RNA, CellNet, ChromFound, ProtCell |
| Spatial / pathology (8) | CIFM, CONCH-Z, DeepCellMorpho, OMNI, QuiltNet, TERRA, XMAG, spaGFM |
| Platform (1) | Protify |
| Benchmark (9) | BEND 2.0, BILBY-PRO, FLIP, Patho-Bench, PLINDER, PoseBusters, PRISM benchmark (pathology), spora, THUNDER |

Some additions are established resources the index lacked (FLIP, PoseBusters, PLINDER, DNABERT-S, QuiltNet, CaLM). The new pathology benchmark called PRISM is a different resource from the displayed Paige slide model `bfm-prism`, so it is listed as "PRISM benchmark (pathology)".

New records carry `verified: 2026-11-06`; all 52 are `verified_with_limits`, and 23 carry non-commercial terms on at least one artifact or access route. Corrected records carry `date_modified: 2026-11-06` and keep their earlier verification date.

## Method

Twelve independent lanes ran: one per modality, a calibrated-uncertainty lane, and a lane for the bio.rodeo feed, the watchlist and a rename/new-version sweep over the 40 most-cited model families. Each lane checked candidates against a normalized identity baseline of the 486 displayed records, the 37 held records and October's 91 discovery leads (names, aliases, URLs). The main window was 2026-10-10 to 2026-11-06, with a second sweep back to 2026-09-11 because October's arXiv access had been throttled. Channels were the arXiv API and listing pages, bioRxiv by date and category, Europe PMC (including preprints), OpenAlex, newest Hugging Face models, new GitHub repositories, and targeted reads. Lanes report about 100,000 screened metadata items; queries overlap, so this is not a count of distinct papers.

Every proposed addition went to a separate agent instructed to refute it. It re-fetched the primary sources and checked identity (including same-name collisions), scope, released artifact, exact terms for code, weights, data and API, every URL, and the wording. All 58 real proposals were confirmed, 57 of them with corrections, which were applied. Corrections proposed for existing records (23 records, including two broken links from the pre-change link audit) went to a further agent per record. It corrected 18 records, made no change to 5, and rejected what it could not confirm. The ODesign agent was cut off before writing its file; the orchestrator applied its reported findings, marked as such in `candidate_decisions.json`.

The refuters were tested with three planted known-bad proposals taken from October's own rejects (a single-task detector presented as a DNA language model, a model whose README promises a checkpoint behind a placeholder DOI, and a pathology model sourced only from an aggregator page). All three were caught: one rejected on scope, two sent back to hold. They are not in any payload. The test shows the refuters catch clear errors; it does not measure subtle ones.

After review, every arXiv and bioRxiv identifier and every GitHub repository cited by an addition was resolved again at the source by a script (all resolve, titles match), and the cited Hugging Face model repositories were resolved through the Hub API.

October's 91 discovery leads were each re-checked by a second agent against the blocker recorded in October: 11 accepted (each then adversarially reviewed), 40 placed on the register, 34 kept as leads and 6 rejected. Two lead batches were cut off mid-write and re-run in full.

All 37 held records were re-reviewed against their recorded `reconsider_when` conditions. None met its condition. No weights were downloaded or run.

Machine-readable decisions: [`candidate_decisions.json`](refresh-2026-11-06/candidate_decisions.json) (every candidate and lead, lane, decision, sources and the reviewing agent's checks), [`hold_reviews.json`](refresh-2026-11-06/hold_reviews.json) (every held record) and [`reviewed_changes.json`](refresh-2026-11-06/reviewed_changes.json) (the migration payload).

## Gaps carried from earlier cycles

- **Calibrated uncertainty.** The lane added two benchmarks that score calibration of pathology foundation models (THUNDER, and the PRISM benchmark). CellBridge, a pathology encoder with a calibrated confidence branch, is held. 24 candidates were rejected as single-task predictors (for example ProbJanusDDG, MetaSplice), methods without a pretrained artifact (for example PPI-Caliper, UPLiFT, scConform), materials-only methods, or general-LLM studies. ESMFold now states its per-residue confidence output. Coverage stays thin: calibrated uncertainty is still rare among released biological foundation models.
- **bio.rodeo feed.** Still frozen: the sitemap and newest entry (2026-09-14) are unchanged since October, so the feed added nothing this cycle. The lane spent its effort on the rename/new-version sweep instead, which proposed RFD4-Proteina and AlphaProtein Novo and several corrections to existing family records.
- **Watchlist.** NeuralPLexer3 still has no released artifact and stays held. Vilya has no new code or weights.

## Held records

- **Kept on hold (37),** with refreshed reasons. Seven still wait on a written exception for single-task structural or single-purpose models, which MAINTENANCE.md does not contain; the owner left that exception ungranted for this cycle.
- **New on the register (40),** from October's leads. Examples: Virtual Cell Challenge (the 2026 challenge runs until late November and has no post-challenge data release with an explicit licence yet), OFoldNA (code and weights still unreleased although the README promised October 2026), CheMeleon-Rxn (a checkpoint appeared on 3 November, but it is the first author's independent re-training, not the official release), scFoundry, Iona. Each entry records its reason and `reconsider_when`.

Discovery leads that a lane held this cycle, and that no second agent examined, stay in `candidate_decisions.json` as leads (`lead_only`) and are not placed on the public register. The next cycle re-reviews them.

## Corrections to existing records

18 records changed: journal versions of preprints (scEval in Advanced Science, MAMMAL, InstructBioMol, RFdiffusion3 in Science) and newer preprint versions (structRFM v3, NTv3 v2, an OpenMidnight 1.1 paper); new family members (Scooby-2, AceFF-2-OMOL with its own licence); access and licence wording (CodonBERT's academic-only licences now set the non-commercial flag, Protenix v2 weights are proprietary, MIST's weights host and terms, Proteina's non-commercial code licence, ESM Atlas dataset licence, RFdiffusion licence wording); BioEmu-1's archived repository and a corrected Science DOI; ESMFold's per-residue confidence output; the Carbon technical report, which moved from a deleted GitHub PDF to its bioRxiv record; and ODesign's web server, which failed TLS validation on 2026-11-06 and is now marked unverified.

## Coverage limits

This is a bounded discovery sweep with adversarial verification of every admission. It is **not a systematic literature review and does not assure that every release was found**. The arXiv API returned HTTP 429 to most lanes; they fell back to listing pages, OpenAlex and Europe PMC, which screen titles or keywords rather than full abstracts. GitHub repository search hit its rate limit in seven lanes, so new repositories without a paper or model-hub trace were under-sampled. bioRxiv was harvested in a subset of categories per lane. Only records with a proposed correction were re-verified; the other displayed records keep their earlier verification dates.

## Local checks

- The dated migration (`scripts/apply_2026_11_06_refresh.py`) is idempotent: a second run left every canonical JSON file, including the resource metadata, byte-identical.
- `build.py`: generated artifacts byte-stable. `validate_catalog.py`: pass (one expected warning, null release reference). `git diff --check`: clean.
- Link audit: 1,849 unique URLs across 3,512 occurrences: 2,555 occurrences reachable, 955 restricted, 0 missing and 2 network errors (ODesign's web server, see corrections). Hugging Face answered most audit requests with 429, so all 406 Hugging Face URLs were re-checked slowly through the Hub API: 405 resolve; the exception is the held ALICE repository (401, as in October). Restricted bioRxiv and publisher pages (bot blocks) were not re-checked and are not counted as verified. Details: [`refresh-2026-11-06/link_recheck.json`](refresh-2026-11-06/link_recheck.json).
- `validate_catalog.py --release` is expected to fail only on the null release reference. Governance was not weakened.

Publication remains a separate step that needs the owner's explicit approval.
