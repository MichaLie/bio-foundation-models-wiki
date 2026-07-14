Foundation source-level audit completed read-only at frozen commit `e79a48cb7caa70555d0e6cb0a0838d849297c57e`. Working tree remains clean.

Coverage is exactly **100/100 assigned records**. No records were `not_checked`.

- Priority totals: P1 20, P2 12, P3 21, P4 47.
- Status totals: verified 47, verified_with_limits 42, provisional 11.
- Assigned modalities: 16 protein, 14 molecule, 12 DNA, 12 complex, 11 single-cell, 11 spatial, 7 multimodal, 7 benchmark, 6 RNA, 4 platform.
- 96 records have paper links. The paperless records are the three platform/project aggregations plus provisional Mistral-DNA.
- 98 have an artifact link; ScDiVa and xTrimoGene have none.
- 83 distinct official GitHub repositories and 19 direct Hugging Face records were checked live.
- Existing dated link evidence covers 216 unique assigned URLs: 159 reachable and 57 access-restricted, with no missing/network-error URLs.
- All 100 assigned records currently have zero entries in `sources`; the current checks therefore need to be persisted before their `verified` dates are advanced.

In the table, `R(id)` means the exact object in [models_final.json](../../models_final.json) whose `id` equals that value. “Persist” means add the current primary paper, official artifact and exact licence/terms URLs to `sources`, then set the real verification date after the correction is applied.

## Rechecked P1 findings

Nineteen records have `noncommercial:false` despite explicit first-party non-commercial terms:

- AlphaFold 3 — [weight terms](https://github.com/google-deepmind/alphafold3/blob/main/WEIGHTS_TERMS_OF_USE.md)
- AgroNT — [model card](https://huggingface.co/InstaDeepAI/agro-nucleotide-transformer-1b)
- Ankh — [licence](https://github.com/agemagician/Ankh/blob/main/LICENSE.md)
- ChatNT — [model-card terms](https://huggingface.co/InstaDeepAI/ChatNT/blob/main/README.md)
- Galactica — [model licence](https://github.com/paperswithcode/galai/blob/main/LICENSE-MODEL.md)
- GET — [repository licence section](https://github.com/GET-Foundation/get_model#license)
- GPFM — [CC BY-NC-ND licence](https://github.com/birkhoffkiki/GPFM/blob/master/LICENSE)
- H-optimus-1 — [gated NC model](https://huggingface.co/bioptimus/H-optimus-1)
- HelixFold3 — [project terms](https://github.com/PaddlePaddle/PaddleHelix/tree/dev/apps/protein_folding/helixfold3)
- IgLM — [academic/non-commercial licence](https://github.com/Graylab/IgLM/blob/main/LICENSE.md)
- KRONOS — [CC BY-NC-ND licence](https://github.com/mahmoodlab/KRONOS/blob/main/LICENSE)
- mSTAR — [repository terms](https://github.com/Innse/mSTAR)
- OpenProtein/PoET-2 — [model licence](https://github.com/OpenProteinAI/PoET-2/blob/main/MODEL_LICENSE.md)
- Phikon family — [Phikon-v2 model card](https://huggingface.co/owkin/phikon-v2)
- PRISM family — [PRISM2 model card](https://huggingface.co/paige-ai/Prism2)
- SAFE-GPT — [code/data/model licence distinctions](https://github.com/datamol-io/safe#license)
- SegmentNT — [model card](https://huggingface.co/InstaDeepAI/segment_nt)
- Tabula — [custom non-commercial licence](https://github.com/aristoteleo/tabula/blob/main/LICENSE)
- TITAN — [gated NC terms](https://github.com/mahmoodlab/TITAN#license-and-terms-of-use)

The twentieth P1 is Protriever: its official repository currently contains only `README.md`, while the row claims “Open code.” There is no released code, checkpoint, or licence in the repository: [official repository](https://github.com/OATML-Markslab/Protriever).

## Rechecked P2 findings

- BioReason still says checkpoints will be released later: [official repository](https://github.com/bowang-lab/BioReason). Hold as a reusable model.
- The Mistral-DNA repository points to a Hugging Face checkpoint that currently returns unauthorized access and is absent from `code_links`: [repository](https://github.com/raphaelmourad/Mistral-DNA), [checkpoint URL](https://huggingface.co/RaphaelMourad/Mistral-DNA-v0.1).
- The combined mRNA-FM/PlantRNA-FM record has primary-paper evidence only for PlantRNA-FM and mixes MIT and AGPL model-card terms. Split or document both components explicitly.
- OpenProtein.AI platform duplicates the already updated `bfm-poet-2` model record and inherits PoET-2’s non-commercial model terms.
- Open Problems, PathBench, PEER, and scEval describe benchmark dependencies or external checkpoints as their own “weights.”
- PULSAR now has an official public checkpoint, so “unclear weights” is stale: [official repository](https://github.com/snap-stanford/PULSAR).
- SATURN provides training code, derived embeddings, and data, but no reusable pretrained SATURN checkpoint: [official repository](https://github.com/snap-stanford/SATURN).
- ScDiVa and xTrimoGene remain paper-only and fail the repository’s reusable-artifact inclusion gate.
- scPROTEIN is a task framework with dataset-specific checkpoints, not a broadly pretrained reusable foundation model: [official repository](https://github.com/TencentAILabHealthcare/scPROTEIN).

## Per-record results — 100/100

| # | ID | Priority | Status | Exact locator and action |
|---:|---|---|---|---|
| 1 | `bfm-ablang` | P4 | verified | `R(id).paper_links/code_links/status/noncommercial`; BSD code and released weights match. Persist; no substantive change. |
| 2 | `bfm-agront-agronomic-nucleotide-transformer` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true and record CC BY-NC-SA 4.0 model terms. |
| 3 | `bfm-aido-dna` | P4 | verified | `R(id).paper_links/code_links/noncommercial`; GenBio community terms are already conservatively represented. Persist. |
| 4 | `bfm-alphafold-3` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true and distinguish Apache code, gated NC parameters, and NC server. |
| 5 | `bfm-alphafold2` | P4 | verified | `R(id).paper_links/code_links/status`; Apache code and CC BY 4.0 parameters match. Persist. |
| 6 | `bfm-ankh` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true; weights are CC BY-NC-SA 4.0. |
| 7 | `bfm-antifold` | P4 | verified | `R(id).paper_links/code_links/status`; paper, BSD repository, and included weights match. Persist. |
| 8 | `bfm-atomica` | P4 | verified | `R(id).paper_links/code_links/status`; MIT code and official released checkpoints match. Persist. |
| 9 | `bfm-biobridge` | P4 | verified | `R(id).paper_links/code_links/status`; paper/repository/checkpoints and MIT licence match. Persist. |
| 10 | `bfm-bioreason` | P2 | provisional | `R(id).status/code_links`; repository still says checkpoints are forthcoming. HOLD until a reusable checkpoint is released. |
| 11 | `bfm-biot5-plus` | P4 | verified | `R(id).paper_links/code_links/status`; official code and pretrained/fine-tuned models are released. Persist. |
| 12 | `bfm-c2s-scale-cell2sentence-scale` | P3 | verified_with_limits | `R(id).code_links/status`; add direct 2B/27B model-card and model-term URLs; document why this remains separate from Cell2Sentence. |
| 13 | `bfm-cddd-continuous-and-data-driven-molecular-descriptors` | P4 | verified | `R(id).paper_links/code_links/status`; MIT implementation and pretrained model link match. Persist. |
| 14 | `bfm-cell2sentence` | P3 | verified_with_limits | `R(id).description/code_links`; document family boundary against C2S-Scale or merge under a family record. |
| 15 | `bfm-cellsam` | P4 | verified | `R(id).paper_links/code_links/status`; current Nature Methods paper, Apache inference code, and weights match. Persist. |
| 16 | `bfm-chai-1` | P4 | verified | `R(id).paper_links/code_links/status`; Apache code and weights are openly available. Persist. |
| 17 | `bfm-chatnt` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true and cite the model-card non-commercial licence. |
| 18 | `bfm-chemdfm` | P4 | verified | `R(id).paper_links/code_links/status`; current repository links released model variants. Persist. |
| 19 | `bfm-chemgpt` | P3 | verified_with_limits | `R(id).code_links/noncommercial`; model exists but its current model card has no explicit licence. State “licence not declared,” not implied open reuse. |
| 20 | `bfm-coati` | P3 | verified_with_limits | `R(id).status/description`; distinguish original COATI release from COATI2, whose training code is not released. |
| 21 | `bfm-cpgpt` | P4 | verified | `R(id).paper_links/code_links/status`; MIT code and pretrained models match. Persist. |
| 22 | `bfm-diffdock` | P4 | verified | `R(id).paper_links/code_links/status`; MIT code and weights remain available. Persist. |
| 23 | `bfm-dnabert-2` | P3 | verified_with_limits | `R(id).code_links/noncommercial`; checkpoint exists, but model card lacks exact licence. Add official repository/licence evidence. |
| 24 | `bfm-dplm` | P4 | verified | `R(id).paper_links/code_links/status`; Apache code and DPLM checkpoints match. Persist. |
| 25 | `bfm-enformer` | P4 | verified | `R(id).paper_links/code_links/status`; Nature Methods paper and DeepMind Apache research code match. Persist. |
| 26 | `bfm-esm-1b-esm-1v` | P3 | verified_with_limits | `R(id).status/code_links`; repository is archived. Mark historical/archived while retaining accessible MIT code and weights. |
| 27 | `bfm-esm3` | P3 | verified_with_limits | `R(id).code_links/status`; old URL redirects to Biohub’s ESMC/ESMFold2 repository. Add the specific ESM3 README/model-card locator and current MIT terms. |
| 28 | `bfm-eve` | P4 | verified | `R(id).paper_links/code_links/status`; Nature paper, MIT code, and released models match. Persist. |
| 29 | `bfm-evodiff` | P4 | verified | `R(id).paper_links/code_links/status`; official MIT code and pretrained models match. Persist. |
| 30 | `bfm-flowdock` | P4 | verified | `R(id).paper_links/code_links/status`; published paper, MIT code, and Zenodo checkpoints match. Persist. |
| 31 | `bfm-galactica` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true for model weights; retain Apache code and withdrawn-demo caution separately. |
| 32 | `bfm-genbench-genomic-foundation-models` | P3 | verified_with_limits | `R(id).status/modality`; say “open benchmark code/data/baseline assets,” not generically “weights.” |
| 33 | `bfm-geneformerv2` | P3 | verified_with_limits | `R(id).code_links/description`; add a version-specific GeneformerV2 artifact locator and document boundary from the Geneformer family record. |
| 34 | `bfm-generator` | P4 | verified | `R(id).paper_links/code_links/status`; MIT repository and current v1/v2 model cards match. Persist. |
| 35 | `bfm-genmol` | P3 | verified_with_limits | `R(id).status/noncommercial`; explicitly separate Apache-2.0 code from NVIDIA Open Model Licence weights. |
| 36 | `bfm-genos` | P4 | verified | `R(id).paper_links/code_links/status`; published paper, Apache code, and model artifacts match. Persist. |
| 37 | `bfm-get-general-expression-transformer` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true; repository is CC BY-NC 4.0. |
| 38 | `bfm-gpfm-generalizable-pathology-foundation-model` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true and change “gated weights” to directly downloadable NC weights. |
| 39 | `bfm-graphmvp` | P4 | verified | `R(id).paper_links/code_links/status`; MIT code and public pretrained weights match. Persist. |
| 40 | `bfm-h-optimus-0-h-optimus-1` | P1 | provisional | `R(id).paper_links/code_links/noncommercial/status`; “Paper” is a company announcement, H-optimus-1 is missing from artifacts and is gated CC BY-NC-ND. Add both model cards and accurate mixed terms. |
| 41 | `bfm-helixfold3` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true; code/parameters are non-commercial and server terms differ by free versus paid route. |
| 42 | `bfm-hugging-face-biology-orgs` | P3 | verified_with_limits | `R(id).code_links/modality`; platform classification is acceptable, but it is a curated org list rather than one official biological hub. Add explicit selection/provenance rationale. |
| 43 | `bfm-igbert-igt5` | P4 | verified | `R(id).paper_links/code_links/status`; paper and MIT model card match. Persist. |
| 44 | `bfm-iglm` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true and cite JHU Academic Software Licence for code and pretrained models. |
| 45 | `bfm-intellifold-2` | P4 | verified | `R(id).paper_links/code_links/status`; official Apache repository and IntelliFold weights match; upstream AF3 weights are explicitly excluded. Persist. |
| 46 | `bfm-kronos` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true and state gated CC BY-NC-ND weights. |
| 47 | `bfm-latch-bio` | P4 | verified | `R(id).modality/code_links/status`; commercial platform plus MIT SDK is correctly scoped. Persist project/licence sources. |
| 48 | `bfm-ligandmpnn` | P4 | verified | `R(id).paper_links/code_links/status`; Nature Methods paper, MIT code, and weights match. Persist. |
| 49 | `bfm-mammal` | P4 | verified | `R(id).paper_links/code_links/status`; IBM MAMMAL repository, Apache code, and official model artifact match. Persist. |
| 50 | `bfm-megalodon` | P3 | verified_with_limits | `R(id).status/noncommercial`; add exact code licence and NVIDIA model-weight licence instead of generic “open.” |
| 51 | `bfm-methylgpt` | P4 | verified | `R(id).paper_links/code_links/status`; Apache code and pretrained models match. Persist. |
| 52 | `bfm-mistral-dna` | P2 | provisional | `R(id).paper_links/code_links/status`; no primary paper, linked checkpoint currently unauthorized, and direct model-card URL is absent. HOLD until checkpoint and terms are verifiable. |
| 53 | `bfm-molclr` | P4 | verified | `R(id).paper_links/code_links/status`; MIT code and bundled pretrained checkpoints match. Persist. |
| 54 | `bfm-molfm` | P3 | verified_with_limits | `R(id).code_links/status`; generic OpenBioMed repository links a Baidu-hosted model. Add the direct official checkpoint and component-specific licence. |
| 55 | `bfm-molgpt` | P3 | verified_with_limits | `R(id).code_links/status`; MIT code is verified, but weights are externally hosted on Kaggle. Add the exact official artifact provenance/licence. |
| 56 | `bfm-mrna-fm-plantrna-fm` | P2 | provisional | `R(id).paper_links/code_links/status`; only PlantRNA-FM has a primary paper link and the two model cards carry different licences. Split or fully evidence both components. |
| 57 | `bfm-mstar` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true and state manually gated CC BY-NC-ND weights. |
| 58 | `bfm-nafm` | P4 | verified | `R(id).paper_links/code_links/status`; MIT code and Zenodo checkpoint match. Persist. |
| 59 | `bfm-neurosnap` | P3 | verified_with_limits | `R(id).modality/code_links/status`; platform identity is current, but add official product terms/pricing/API evidence; website availability alone is insufficient licence evidence. |
| 60 | `bfm-novae` | P4 | verified | `R(id).paper_links/code_links/status`; published paper, BSD code, and model card match. Persist. |
| 61 | `bfm-omegafold` | P3 | verified_with_limits | `R(id).status/code_links`; accessible Apache code/weights are historical and repository activity is dormant. Mark maintenance state. |
| 62 | `bfm-open-problems-in-single-cell-analysis` | P2 | verified_with_limits | `R(id).status/modality`; change to “open benchmark code, tasks, datasets and containers”; it has no proprietary model weights. |
| 63 | `bfm-openprotein-ai-poet-poet-2` | P1 | provisional | `R(id).noncommercial/status/description`; set NC true and resolve duplication with `bfm-poet-2`. Narrow to the commercial platform or merge. |
| 64 | `bfm-pathbench` | P2 | verified_with_limits | `R(id).status/modality`; change from “code + weights” to open benchmark application/data; evaluated models are external. |
| 65 | `bfm-peer-protein-sequence-understanding` | P2 | verified_with_limits | `R(id).status/modality`; change to open benchmark code/datasets/configurations, not own weights. |
| 66 | `bfm-phikon-phikon-v2` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true and cite separate Phikon and Phikon-v2 non-commercial model terms. |
| 67 | `bfm-placer` | P4 | verified | `R(id).paper_links/code_links/status`; BSD licence explicitly covers source and weights. Persist. |
| 68 | `bfm-prism` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true; PRISM and PRISM2 are gated CC BY-NC-ND models. |
| 69 | `bfm-prosst` | P4 | verified | `R(id).paper_links/code_links/status`; GPL-3.0 code and official checkpoints match. Persist. |
| 70 | `bfm-proteina` | P4 | verified | `R(id).noncommercial/status`; NC flag is already correct; official repository provides research-only weights. Persist. |
| 71 | `bfm-proteindt` | P4 | verified | `R(id).paper_links/code_links/status`; published paper, MIT code, and official checkpoints match. Persist. |
| 72 | `bfm-protenix` | P4 | verified | `R(id).paper_links/code_links/status`; Apache code and model parameters, including current family releases, match. Persist. |
| 73 | `bfm-protgpt2` | P4 | verified | `R(id).paper_links/code_links/status`; published paper and Apache model card match. Persist. |
| 74 | `bfm-protriever` | P1 | provisional | `R(id).status/code_links`; official repository contains only README, not open code or weights. HOLD and correct status to placeholder/paper only. |
| 75 | `bfm-prottrans-prott5-protbert` | P4 | verified | `R(id).paper_links/code_links/status`; MIT repository and Rostlab models match. Persist. |
| 76 | `bfm-pulsar` | P2 | verified_with_limits | `R(id).status/code_links`; public MIT checkpoints now exist. Change “unclear weights” to open code + weights and add model-card URLs. |
| 77 | `bfm-rinalmo` | P4 | verified | `R(id).paper_links/code_links/status`; published paper, Apache code, and Zenodo weights match. Persist. |
| 78 | `bfm-rnabert` | P3 | verified_with_limits | `R(id).code_links/noncommercial`; source and weights exist, but no reuse licence is declared. State “no licence found.” |
| 79 | `bfm-rnagym` | P3 | verified_with_limits | `R(id).status/modality`; describe open benchmark code/data/baseline checkpoints rather than generic own weights. |
| 80 | `bfm-safe-gpt` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true; code is Apache, data CC BY, model weights CC BY-NC. |
| 81 | `bfm-saturn` | P2 | provisional | `R(id).status/description`; repository provides training code, embeddings and derived macrogene weights, not a reusable pretrained SATURN checkpoint. HOLD or reclassify as method. |
| 82 | `bfm-sccello` | P4 | verified | `R(id).paper_links/code_links/status`; MIT project and official public checkpoint match. Persist. |
| 83 | `bfm-scdiva` | P2 | provisional | `R(id).code_links/status`; paper-only with no released code or checkpoint. HOLD under the reusable-artifact rule. |
| 84 | `bfm-sceval` | P2 | verified_with_limits | `R(id).status/modality`; benchmark code uses external models/checkpoints. Change status accordingly; also record that repository has no explicit licence. |
| 85 | `bfm-scgpt-spatial` | P4 | verified | `R(id).paper_links/code_links/status`; MIT code and Figshare weights match. Persist. |
| 86 | `bfm-sclong` | P3 | verified_with_limits | `R(id).code_links/status/noncommercial`; checkpoint is public via SharePoint, but no repository or weight licence was found. State this explicitly. |
| 87 | `bfm-scooby` | P4 | verified | `R(id).paper_links/code_links/status`; published paper, MIT code, and official model cards match. Persist. |
| 88 | `bfm-scprotein` | P2 | provisional | `R(id).description/status`; dataset-specific analysis framework/checkpoints do not substantiate a broadly pretrained foundation model. HOLD or reclassify outside scope. |
| 89 | `bfm-segmentnt` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true and cite CC BY-NC-SA 4.0 model terms. |
| 90 | `bfm-smi-ted-materials-smi-ted` | P4 | verified | `R(id).paper_links/code_links/status`; Apache FM4M repository and official SMI-TED model artifact match. Persist. |
| 91 | `bfm-splicebert` | P3 | verified_with_limits | `R(id).code_links/status`; original project is BSD-3-Clause while the MultiMolecule mirror is AGPL-3.0. Record component-specific licences. |
| 92 | `bfm-stofm` | P4 | verified | `R(id).paper_links/code_links/status`; MIT code, checkpoint, and released corpus match. Persist. |
| 93 | `bfm-tabula` | P1 | provisional | `R(id).noncommercial/status/code_links`; set NC true, but repository has training code only and no pretrained checkpoint. HOLD until reusable weights exist. |
| 94 | `bfm-tape-tasks-assessing-protein-embeddings` | P3 | verified_with_limits | `R(id).status/code_links`; benchmark, BSD code and baseline weights remain available, but README says training code is no longer maintained. Mark historical maintenance state. |
| 95 | `bfm-titan` | P1 | verified_with_limits | `R(id).noncommercial/status`; set NC true and state manual gating, CC BY-NC-ND terms, and decoder-weight omission. |
| 96 | `bfm-trrosettarna` | P4 | verified | `R(id).paper_links/code_links/status`; published paper, Apache code, downloadable parameters, and server match. Persist. |
| 97 | `bfm-umol` | P4 | verified | `R(id).paper_links/code_links/status`; Apache code and CC BY 4.0 parameters match. Persist. |
| 98 | `bfm-uni-mol2` | P4 | verified | `R(id).paper_links/code_links/status`; MIT family repository and Uni-Mol2 code/weights match. Persist. |
| 99 | `bfm-utr-lm` | P4 | verified | `R(id).paper_links/code_links/status`; published paper, GPL-3.0 code and public checkpoints match. Persist. |
| 100 | `bfm-xtrimogene` | P2 | provisional | `R(id).code_links/status`; paper-only with no official code or checkpoint. HOLD under the reusable-artifact rule. |

## Structural source-model issue

The recurrent errors are partly caused by [schema.json](../../schema.json): one `noncommercial` boolean cannot represent Apache code plus NC weights, gated access, absent licences, API-only access, or mixed family terms.

Recommended structured replacement:

- `code`: availability, licence, source URL
- `weights`: open/gated/unreleased/absent, licence, terms URL
- `data`: availability and licence
- `api_server`: availability and terms
- derived `noncommercial` display flag, rather than manually curated truth

The validator should reject a record claiming open code/weights without the corresponding structured artifact and official source.

Two global FAIR holds also remain visible:

- `resource_metadata.source_commit` points to `df1d18…`, not frozen audited commit `e79a48…`.
- Release validation correctly remains blocked by missing catalogue reuse licence, missing publisher, and preview version.

No files were edited.
