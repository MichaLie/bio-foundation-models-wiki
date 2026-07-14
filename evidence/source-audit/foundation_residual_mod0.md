Completed the frozen, read-only source audit at commit `e79a48cb7caa70555d0e6cb0a0838d849297c57e`.

- Selection: exactly 100 records where `verified < 2026-07-13`, sorted by `id`, index `% 3 == 0`.
- Coverage: `100/100`.
- Outcomes: `verified 56`, `verified_with_limits 33`, `provisional 11`, `not_checked 0`.
- Priorities: `P1 0`, `P2 40`, `P3 4`, `P4 56`.
- Link evidence: 222 cited URL occurrences; 172 directly reachable and 50 restricted/rate-limited. Restricted sources were resolved through DOI/Crossref metadata, official repositories/model cards, or final-paper pages.
- P1/P2 recheck: no P1 survived. All P2 findings below were confirmed against primary papers and official artifacts.
- Repository remains clean; no edits.

“Provisional” here means the model identity is known, but its catalogue eligibility, public artifact claim, or family grouping needs an editorial HOLD decision under the current “pretrained, reusable, broader than one task” rule.

## P2/P3 ledger

| ID | Outcome | Priority | Finding and exact source locators |
|---|---|---:|---|
| `bfm-3d-molt5` | verified_with_limits | P2 | Status is stale: official pretrained and fine-tuned weights now exist, including MIT-licensed `3d-molt5-base`. [Paper](https://openreview.net/forum?id=eGqQyTAbXC), [repo](https://github.com/qizhipei/3d-molt5), [weights](https://huggingface.co/QizhiPei/3d-molt5-base). |
| `bfm-abodybuilder3` | provisional | P2 | Identity and artifacts verify, but ABodyBuilder3 is a task-specific antibody structure predictor rather than a model broader than one task; HOLD or document a structural-model exception. [Paper](https://academic.oup.com/bioinformatics/article/40/10/btae576/7810444), [repo](https://github.com/Exscientia/abodybuilder3). |
| `bfm-aido-cell` | verified_with_limits | P2 | `noncommercial:false` and generic hub wording omit the GenBio AI Community License, which limits code, weights, derivatives, and outputs to non-commercial purposes. [Paper](https://www.biorxiv.org/content/10.1101/2024.11.28.625303v1), [model](https://huggingface.co/genbio-ai/AIDO.Cell-10M), [licence](https://github.com/genbio-ai/ModelGenerator/blob/main/LICENSE). |
| `bfm-aido-rna` | verified_with_limits | P2 | Same GenBio non-commercial restriction as AIDO.Cell. [Paper](https://www.biorxiv.org/content/10.1101/2024.11.28.625345), [model](https://huggingface.co/genbio-ai/AIDO.RNA-1.6B), [licence](https://github.com/genbio-ai/ModelGenerator/blob/main/LICENSE). |
| `bfm-alphafold-server` | verified_with_limits | P2 | Status says only “terms apply,” while use and outputs are explicitly non-commercial and additionally prohibit docking/screening and structure-model training. Set explicit NC wording/flag. [FAQ](https://alphafoldserver.com/faq), [output terms](https://alphafoldserver.com/output-terms). |
| `bfm-atlas-rudolfv-successor` | provisional | P2 | Listed HF artifact returns no model; official Aignostics materials now describe flexible commercial licensing and Atlas 2, not open/gated Atlas weights. Replace the dead artifact and avoid “open code, gated weights” unless a current public release is found. [Atlas paper](https://arxiv.org/abs/2501.05409), [dead listed artifact](https://huggingface.co/aignostics/atlas), [official model page](https://www.aignostics.com/products/foundation-models), [Atlas 2](https://www.aignostics.com/blog/atlas-2-setting-a-new-standard-for-pathology-foundation-models). |
| `bfm-bend` | verified_with_limits | P2 | Benchmark role is correct, but “Open code + weights” is not: BEND provides benchmark data/code and wrappers around third-party checkpoints. Link the final ICLR paper. [ICLR paper](https://proceedings.iclr.cc/paper_files/paper/2024/hash/429e7b31625a8b7839f9e4d6e2aa9bb9-Abstract-Conference.html), [repo](https://github.com/frederikkemarin/BEND). |
| `bfm-biomedgpt` | verified_with_limits | P2 | Replace arXiv with the final IEEE article; expose direct model artifacts and the BioMedGPT Acceptable Use Policy rather than only generic “open code + weights.” [Final paper](https://ieeexplore.ieee.org/document/10767279/), [repo](https://github.com/PharMolix/OpenBioMed), [AUP](https://github.com/PharMolix/OpenBioMed/blob/main/USE_POLICY.md). |
| `bfm-chatcell` | verified_with_limits | P2 | Repository is CC BY-NC-SA 4.0, but `noncommercial:false`. [Paper](https://arxiv.org/abs/2402.08303), [repo](https://github.com/zjunlp/ChatCell), [licence](https://github.com/zjunlp/ChatCell/blob/main/LICENSE). |
| `bfm-chemberta-chemberta-2` | verified_with_limits | P2 | Family record cites ChemBERTa-2 but links only the older ChemBERTa v1 repo/model. Add the official ChemBERTa-2 77M MLM/MTR artifacts or split versions. [ChemBERTa-2 paper](https://arxiv.org/abs/2209.01712), [v1 repo](https://github.com/seyonechithrananda/bert-loves-chemistry), [ChemBERTa-2 MTR](https://huggingface.co/DeepChem/ChemBERTa-77M-MTR), [MLM](https://huggingface.co/DeepChem/ChemBERTa-77M-MLM). |
| `bfm-chrombpnet` | provisional | P2 | Current paper/repo describe a bias-factorized chromatin-accessibility predictor trained per assay, not clearly a reusable multi-task foundation model. Reassess against the stated scope rule or document an exception. [Paper](https://www.biorxiv.org/content/10.1101/2024.12.25.630221v1), [repo](https://github.com/kundajelab/chrombpnet). |
| `bfm-conch` | verified_with_limits | P2 | Gated weights and code/model are CC BY-NC-ND 4.0 for non-commercial academic research; `noncommercial:false` is wrong. [Paper](https://www.nature.com/articles/s41591-024-02856-4), [repo terms](https://github.com/mahmoodlab/CONCH#license-and-terms-of-use). |
| `bfm-deepsea` | provisional | P2 | Identity is correct, but the linked artifact is the later Selene framework, and DeepSEA is a supervised regulatory predictor rather than an unambiguous reusable FM. Decide whether it is a documented historical/canonical exception. [Paper](https://www.nature.com/articles/nmeth.3547), [Selene](https://github.com/FunctionLab/selene). |
| `bfm-dnalongbench` | verified_with_limits | P2 | Benchmark provides datasets, evaluation code, and baselines, not released benchmark “weights.” Change status to code + benchmark data/baselines. [Paper](https://www.nature.com/articles/s41467-025-65077-4), [repo](https://github.com/wenduocheng/DNALongBench). |
| `bfm-drfold` | provisional | P2 | DRfold/DRfold2 are RNA structure predictors; DRfold2 contains a pretrained RCLM component, but the catalogue record itself remains one-task structure prediction. HOLD or define a structural-model exception. [DRfold paper](https://www.nature.com/articles/s41467-023-41303-9), [DRfold2 paper](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3003659), [DRfold](https://github.com/leeyang/DRfold), [DRfold2](https://github.com/leeyang/DRfold2). |
| `bfm-florabert` | provisional | P2 | Official description focuses on plant promoter modelling and tissue-specific gene-expression prediction; broad reusable FM scope is not established. [Paper](https://www.researchsquare.com/article/rs-1927200/v1), [repo](https://github.com/benlevyx/florabert). |
| `bfm-framediff-frameflow-multiflow` | verified_with_limits | P2 | Improperly merges three distinct methods while citing only Multiflow’s paper/repo. Either keep Multiflow alone or add separate FrameDiff and FrameFlow evidence/records. [Multiflow ICML](https://proceedings.mlr.press/v235/campbell24a.html), [Multiflow repo](https://github.com/jasonkyuyim/multiflow), [FrameDiff paper](https://arxiv.org/abs/2302.02277), [FrameDiff repo](https://github.com/jasonkyuyim/se3_diffusion), [FrameFlow paper](https://arxiv.org/abs/2310.05297), [FrameFlow repo](https://github.com/microsoft/frame-flow). |
| `bfm-genept` | verified_with_limits | P2 | GenePT releases code and precomputed OpenAI gene embeddings, not conventional trained model weights. Status should say code + precomputed embeddings. [Paper](https://www.nature.com/articles/s41551-024-01284-6), [repo](https://github.com/yiqunchen/GenePT), [embeddings DOI](https://doi.org/10.5281/zenodo.10833191). |
| `bfm-genomic-benchmarks` | verified_with_limits | P2 | Benchmark distributes datasets/package/baselines, not model weights. [Paper](https://link.springer.com/article/10.1186/s12863-023-01123-8), [repo](https://github.com/ML-Bioinfo-CEITEC/genomic_benchmarks). |
| `bfm-genslms` | verified_with_limits | P2 | Replace preprint-only primary source with the published article. [Final paper](https://journals.sagepub.com/doi/10.1177/10943420231201154), [repo](https://github.com/ramanathanlab/genslm). |
| `bfm-grover-dna-language-model` | verified_with_limits | P3 | Model hub and paper match, but the HF card exposes no explicit model licence. Preserve as accessible-with-unclear-reuse, not implicitly permissive. [Paper](https://www.nature.com/articles/s42256-024-00872-0), [model](https://huggingface.co/PoetschLab/GROVER). |
| `bfm-langcell` | verified_with_limits | P2 | Replace arXiv-only source with final ICML publication. [ICML paper](https://proceedings.mlr.press/v235/zhao24u.html), [repo](https://github.com/PharMolix/LangCell). |
| `bfm-lc-plm` | verified_with_limits | P2 | Repository explicitly uses CC BY-NC 4.0, but `noncommercial:false`; paper is now accepted/published in TMLR. [TMLR record](https://openreview.net/forum?id=dWvztQzfy4), [repo](https://github.com/amazon-science/LC-PLM), [licence](https://github.com/amazon-science/LC-PLM/blob/main/LICENSE). |
| `bfm-molgen` | verified_with_limits | P2 | Replace arXiv with final ICLR 2024 paper. [ICLR paper](https://proceedings.iclr.cc/paper_files/paper/2024/hash/ed7dd1e32cf9b0abf664bf0e891527e5-Abstract-Conference.html), [repo](https://github.com/zjunlp/MolGen). |
| `bfm-nabench` | verified_with_limits | P2 | Benchmark provides data, scores, and evaluation code; contributors are instructed to supply their own model checkpoints. Change status from “weights” to benchmark data/code/results. [Paper](https://arxiv.org/abs/2511.02888), [repo](https://github.com/mrzzmrzz/NABench). |
| `bfm-neuralplexer-and-neuralplexer3` | provisional | P2 | Family conflates v1 and NP3. V1 checkpoints are explicitly CC BY-NC-SA for non-commercial use, while linked repo/paper do not implement NP3. NP3 has a separate NeurIPS paper and no verified public code/weights in the cited artifact. [v1 paper](https://www.nature.com/articles/s42256-024-00792-z), [v1 repo](https://github.com/zrqiao/NeuralPLexer), [v1 checkpoints](https://doi.org/10.5281/zenodo.10373581), [NP3 paper](https://openreview.net/forum?id=BlLAmMFEzJ). |
| `bfm-pearl` | provisional | P2 | Only a paper is cited; “Web/API/commercial” lacks an official artifact locator. Official Genesis pages describe Pearl and an AI platform/partner access, not a public model endpoint. [Paper](https://arxiv.org/abs/2510.24670), [official Pearl page](https://www.genesis.ml/ai-research). |
| `bfm-pharmolixfm` | verified_with_limits | P3 | Identity and preview weights verify, but add the model download directly instead of relying on the umbrella OpenBioMed repo. [Paper](https://arxiv.org/abs/2503.21788), [repo](https://github.com/PharMolix/OpenBioMed), [model](https://cloud.tsinghua.edu.cn/f/8f337ed5b58f45138659/). |
| `bfm-poet` | verified_with_limits | P2 | PoET weights are CC BY-NC-SA for academic use; `noncommercial:false`. Replace arXiv with NeurIPS paper and resolve overlap with `bfm-poet-2` and platform record `bfm-openprotein-ai-poet-poet-2`. [NeurIPS paper](https://papers.nips.cc/paper_files/paper/2023/hash/f4366126eba252699b280e8f93c0ab2f-Abstract-Conference.html), [repo terms](https://github.com/OpenProteinAI/PoET#license), [weights](https://zenodo.org/records/10061322). |
| `bfm-prot2text` | verified_with_limits | P2 | Repository/model release is CC BY-NC-SA 4.0, but `noncommercial:false`. [Paper](https://ojs.aaai.org/index.php/AAAI/article/view/28948), [repo](https://github.com/hadi-abdine/Prot2Text). |
| `bfm-protgps` | provisional | P2 | Model is centred on one localization objective—12-compartment prediction and localization-conditioned generation. Reassess broad-FM eligibility. [Paper](https://www.science.org/doi/10.1126/science.adq2634), [repo](https://github.com/pgmikhael/protgps). |
| `bfm-protrek` | verified_with_limits | P2 | Replace bioRxiv with final Nature Biotechnology article. [Final paper](https://www.nature.com/articles/s41587-025-02836-0), [repo](https://github.com/westlake-repl/ProTrek), [model](https://huggingface.co/westlake-repl/ProTrek_650M). |
| `bfm-prott3` | verified_with_limits | P3 | Public code/checkpoints verify, but no explicit repository licence was found; mark reuse licence unclear. [Paper](https://aclanthology.org/2024.acl-long.324/), [repo](https://github.com/acharkq/ProtT3). |
| `bfm-scconcept` | verified_with_limits | P2 | “Paper/preprint only” is stale: official MIT code, PyPI package, and pretrained HF checkpoints now exist. [Preprint](https://doi.org/10.1101/2025.10.14.682419), [repo](https://github.com/theislab/scConcept), [model hub](https://huggingface.co/theislab/scConcept). |
| `bfm-sceptr` | verified_with_limits | P2 | Replace arXiv with final Cell Systems paper; weights are bundled/released and MIT. [Final paper](https://www.sciencedirect.com/science/article/pii/S2405471224003697), [repo](https://github.com/yutanagano/sceptr), [software DOI](https://doi.org/10.5281/zenodo.14286003). |
| `bfm-sclinguist` | verified_with_limits | P2 | “Paper/preprint only” is stale: official MIT repository, documentation, and three released checkpoints exist. [Preprint](https://doi.org/10.1101/2025.09.30.679123), [repo](https://github.com/OmicsML/scLinguist), [documentation](https://sclinguist.readthedocs.io/en/stable/install.html). |
| `bfm-scmulan` | verified_with_limits | P2 | Listed HF artifact is gone, but official repo still provides a checkpoint through Tsinghua Cloud. Replace the dead link; status remains code + weights. [Paper](https://link.springer.com/chapter/10.1007/978-1-0716-3989-4_57), [repo](https://github.com/SuperBianC/scMulan), [current checkpoint](https://cloud.tsinghua.edu.cn/f/2250c5df51034b2e9a85/?dl=1), [dead listed HF](https://huggingface.co/deeplife/scmulan_model). |
| `bfm-sctranslator` | provisional | P2 | Code/checkpoints are public but no licence file is present, and the model is a single RNA-to-protein translation task. HOLD or explicitly document both scope and no-licence limitations. [Paper](https://www.nature.com/articles/s41551-025-01528-z), [repo](https://github.com/TencentAILabHealthcare/scTranslator). |
| `bfm-subcell` | verified_with_limits | P3 | “Model hub” is supportable, but the record links only training code. Add the CZI Virtual Cells model card, which identifies MIT licensing and the usable model. [Preprint](https://www.biorxiv.org/content/10.1101/2024.12.06.627299v2), [repo](https://github.com/CellProfiling/subcell-embed), [model card](https://virtualcellmodels.cziscience.com/model/0193323e-ebd5-727c-bb32-87ed8f737213). |
| `bfm-therapeutics-data-commons-tdc` | verified_with_limits | P2 | Benchmark/platform supplies datasets, library, oracles, and leaderboards—not weights. Replace arXiv with NeurIPS Datasets and Benchmarks paper. [Final paper](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/hash/4c56ff4ce4aaf9573aa5dff913df997a-Abstract-round1.html), [repo](https://github.com/mims-harvard/TDC). |
| `bfm-uce` | verified_with_limits | P2 | UCE now has a final Nature article published July 2026; replace the preprint as primary while preserving it as history. [Nature paper](https://www.nature.com/articles/s41586-026-10689-z), [repo](https://github.com/snap-stanford/UCE). |
| `bfm-uni-mol-docking-v2` | provisional | P2 | Exact model is a dedicated docking predictor rather than an unambiguous broader-than-one-task FM. HOLD or document a structural/docking exception. [Paper](https://arxiv.org/abs/2405.11769), [repo](https://github.com/deepmodeling/Uni-Mol/tree/main/unimol_docking_v2). |
| `bfm-uni-uni2-h` | verified_with_limits | P2 | Gated weights and associated code/models are CC BY-NC-ND 4.0 for non-commercial academic use; `noncommercial:false` is wrong. [Paper](https://www.nature.com/articles/s41591-024-02857-3), [repo terms](https://github.com/mahmoodlab/UNI#license-and-terms-of-tuse). |
| `bfm-virtues` | verified_with_limits | P2 | Mixed access is flattened incorrectly: code is MIT, `virtues-sp32` and `virtues-imc14` weights are CC BY-NC 4.0, while `virtues-sp31` is MIT. Status must expose per-checkpoint terms instead of generic open + `noncommercial:false`. [Paper](https://arxiv.org/abs/2501.06039), [repo model table](https://github.com/bunnelab/virtues#models). |

## P4 verified ledger

For every row below, identity, modality, paper status, official artifact, access wording, catalogue role, and duplicate check were aligned; no material change was found.

| ID | Outcome | Priority | Primary paper · official artifact |
|---|---|---:|---|
| `bfm-amplify` | verified | P4 | [Paper](https://www.biorxiv.org/content/10.1101/2024.09.23.614603v1) · [repo](https://github.com/chandar-lab/AMPLIFY) |
| `bfm-antiberty` | verified | P4 | [Paper](https://arxiv.org/abs/2112.07782) · [repo](https://github.com/jeffreyruffolo/AntiBERTy) |
| `bfm-biot5` | verified | P4 | [Paper](https://aclanthology.org/2023.emnlp-main.70/) · [repo](https://github.com/QizhiPei/BioT5) |
| `bfm-borzoi` | verified | P4 | [Paper](https://www.nature.com/articles/s41588-024-02053-6) · [repo](https://github.com/calico/borzoi) |
| `bfm-carp` | verified | P4 | [Paper](https://www.cell.com/cell-systems/fulltext/S2405-4712(24)00029-2) · [repo](https://github.com/microsoft/protein-sequence-models) |
| `bfm-cell-painting-cnn-deepprofiler-model` | verified | P4 | [Paper](https://www.nature.com/articles/s41467-024-45999-1) · [repo](https://github.com/cytomining/DeepProfiler) |
| `bfm-cellplm` | verified | P4 | [Paper](https://openreview.net/forum?id=BKXvPDekud) · [repo](https://github.com/OmicsML/CellPLM) |
| `bfm-cellwhisperer` | verified | P4 | [Paper](https://www.nature.com/articles/s41587-025-02857-9) · [repo](https://github.com/epigen/cellwhisperer) |
| `bfm-chemformer-molbart` | verified | P4 | [Paper](https://iopscience.iop.org/article/10.1088/2632-2153/ac3ffb) · [repo](https://github.com/MolecularAI/Chemformer) |
| `bfm-dnabert` | verified | P4 | [Paper](https://academic.oup.com/bioinformatics/article/37/15/2112/6128680) · [repo](https://github.com/jerryji1993/DNABERT) |
| `bfm-ernie-rna` | verified | P4 | [Paper](https://www.nature.com/articles/s41467-025-64972-0) · [repo](https://github.com/Bruce-ywj/ERNIE-RNA) |
| `bfm-esm-if1` | verified | P4 | [Paper](https://www.biorxiv.org/content/10.1101/2022.04.10.487779v1) · [repo](https://github.com/facebookresearch/esm) |
| `bfm-eva` | verified | P4 | [Paper](https://www.biorxiv.org/content/10.64898/2026.03.17.712398v2) · [repo](https://github.com/GENTEL-lab/EVA) |
| `bfm-evo-2` | verified | P4 | [Paper](https://www.nature.com/articles/s41586-026-10176-5) · [repo](https://github.com/arcinstitute/evo2) |
| `bfm-gena-lm` | verified | P4 | [Paper](https://academic.oup.com/nar/article/53/2/gkae1310/7954523) · [repo](https://github.com/AIRI-Institute/GENA_LM) |
| `bfm-geneformer` | verified | P4 | [Paper](https://www.nature.com/articles/s41586-023-06139-9) · [model](https://huggingface.co/ctheodoris/Geneformer) |
| `bfm-genie-2` | verified | P4 | [Paper](https://arxiv.org/abs/2405.15489) · [repo](https://github.com/aqlaboratory/genie2) |
| `bfm-gp-molformer` | verified | P4 | [Paper](https://pubs.rsc.org/en/content/articlehtml/2025/dd/d5dd00122f) · [repo](https://github.com/IBM/gp-molformer) |
| `bfm-gpn-msa` | verified | P4 | [Final paper](https://www.nature.com/articles/s41587-024-02511-w) · [repo](https://github.com/songlab-cal/gpn) |
| `bfm-helix-mrna` | verified | P4 | [Paper](https://arxiv.org/abs/2502.13785) · [repo](https://github.com/helicalAI/helical) |
| `bfm-hicfoundation` | verified | P4 | [Paper](https://www.nature.com/articles/s41592-026-03097-8) · [repo](https://github.com/Noble-Lab/HiCFoundation) |
| `bfm-hyenadna` | verified | P4 | [Paper](https://proceedings.neurips.cc/paper_files/paper/2023/hash/86ab6927ee4ae9bde4247793c46797c7-Abstract-Conference.html) · [repo](https://github.com/HazyResearch/hyena-dna) |
| `bfm-iggm` | verified | P4 | [Paper](https://www.biorxiv.org/content/10.1101/2024.09.19.613838v2) · [repo](https://github.com/TencentAI4S/IgGM) |
| `bfm-instructprotein` | verified | P4 | [Paper](https://aclanthology.org/2024.acl-long.62/) · [repo](https://github.com/HICAI-ZJU/InstructProtein) |
| `bfm-kpgt-knowledge-guided-pre-training-of-graph-transformer` | verified | P4 | [Paper](https://www.nature.com/articles/s41467-023-43214-1) · [repo](https://github.com/lihan97/KPGT) |
| `bfm-lucaone` | verified | P4 | [Paper](https://www.nature.com/articles/s42256-025-01044-4) · [repo](https://github.com/LucaOne/LucaOne) |
| `bfm-megadna` | verified | P4 | [Paper](https://www.nature.com/articles/s41467-024-53759-4) · [repo](https://github.com/lingxusb/megaDNA) |
| `bfm-metagene-1` | verified | P4 | [Paper](https://arxiv.org/abs/2501.02045) · [model](https://huggingface.co/metagene-ai/METAGENE-1) |
| `bfm-mist` | verified | P4 | [Paper](https://arxiv.org/abs/2510.18900) · [repo](https://github.com/BattModels/mist-demo) |
| `bfm-molbert` | verified | P4 | [Paper](https://arxiv.org/abs/2011.13230) · [repo](https://github.com/BenevolentAI/MolBERT) |
| `bfm-mole-bert` | verified | P4 | [Paper](https://openreview.net/forum?id=jevY-DtiZTR) · [repo](https://github.com/junxia97/Mole-BERT) |
| `bfm-molt5` | verified | P4 | [Paper](https://aclanthology.org/2022.emnlp-main.26/) · [repo](https://github.com/blender-nlp/MolT5) |
| `bfm-msa-transformer` | verified | P4 | [Paper](https://www.biorxiv.org/content/10.1101/2021.02.12.430858v1) · [repo](https://github.com/facebookresearch/esm) |
| `bfm-nicheformer` | verified | P4 | [Paper](https://www.nature.com/articles/s41592-025-02814-z) · [repo](https://github.com/theislab/nicheformer) |
| `bfm-nvidia-bionemo` | verified | P4 | [framework](https://github.com/NVIDIA/bionemo-framework) · [docs](https://docs.nvidia.com/bionemo-framework/latest/) |
| `bfm-omnina` | verified | P4 | [Paper](https://academic.oup.com/nar/article/54/6/gkag083/8528802) · [repo](https://github.com/xilinshen/OmniNA) |
| `bfm-openmedlab` | verified | P4 | [Paper](https://arxiv.org/abs/2402.18028) · [official organization](https://github.com/openmedlab) |
| `bfm-p-iggen` | verified | P4 | [Paper](https://academic.oup.com/bioinformatics/article/40/11/btae659/7888884) · [repo](https://github.com/oxpig/p-IgGen) |
| `bfm-pinal-denovo-pinal` | verified | P4 | [Paper](https://www.biorxiv.org/content/10.1101/2024.08.01.606258v7) · [repo](https://github.com/westlake-repl/Denovo-Pinal) |
| `bfm-progen-progen2` | verified | P4 | [ProGen](https://www.nature.com/articles/s41587-022-01618-2) · [ProGen2](https://openreview.net/forum?id=ZOn4HXehSJ6) · [repo](https://github.com/salesforce/progen) |
| `bfm-proteinbert` | verified | P4 | [Paper](https://academic.oup.com/bioinformatics/article/38/8/2102/6502274) · [repo](https://github.com/nadavbra/protein_bert) |
| `bfm-proteinnpt` | verified | P4 | [Paper](https://proceedings.neurips.cc/paper_files/paper/2023/hash/6a4d5d85f7a52f062d23d98d544a5578-Abstract-Conference.html) · [repo](https://github.com/OATML-Markslab/ProteinNPT) |
| `bfm-ptm-mamba` | verified | P4 | [Paper](https://www.nature.com/articles/s41592-025-02656-9) · [repo](https://github.com/programmablebio/ptm-mamba) |
| `bfm-rfdiffusion2` | verified | P4 | [Paper](https://www.nature.com/articles/s41592-025-02975-x) · [repo](https://github.com/RosettaCommons/RFdiffusion2) |
| `bfm-rna-msm` | verified | P4 | [Paper](https://academic.oup.com/nar/article/52/1/e3/7369930) · [repo](https://github.com/yikunpku/RNA-MSM) |
| `bfm-rnagenesis` | verified | P4 | [Paper](https://www.biorxiv.org/content/10.1101/2024.12.30.630826v2) · [repo](https://github.com/zaixizhang/RNAGenesis) |
| `bfm-rosettafoldna` | verified | P4 | [Paper](https://www.nature.com/articles/s41592-023-02086-5) · [repo](https://github.com/uw-ipd/RoseTTAFold2NA) |
| `bfm-saprot` | verified | P4 | [Paper](https://openreview.net/forum?id=6MRm3G4NiU) · [repo](https://github.com/westlake-repl/SaProt) |
| `bfm-scbert` | verified | P4 | [Paper](https://www.nature.com/articles/s42256-022-00534-z) · [repo](https://github.com/TencentAILabHealthcare/scBERT) |
| `bfm-scgpt` | verified | P4 | [Paper](https://www.nature.com/articles/s41592-024-02201-0) · [repo](https://github.com/bowang-lab/scGPT) |
| `bfm-scprint-2` | verified | P4 | [Paper](https://www.biorxiv.org/content/10.64898/2025.12.11.693702v1) · [repo](https://github.com/cantinilab/scPRINT-2) |
| `bfm-smi-ssed-materials-smi-ssed` | verified | P4 | [Paper](https://research.ibm.com/publications/a-mamba-based-foundation-model-for-chemistry) · [repo](https://github.com/IBM/materials) |
| `bfm-specieslm-species-aware-dna-language-model` | verified | P4 | [Paper](https://link.springer.com/article/10.1186/s13059-024-03221-x) · [repo](https://github.com/gagneurlab/SpeciesLM) |
| `bfm-state-arc-institute` | verified | P4 | [Paper](https://www.biorxiv.org/content/10.1101/2025.06.26.661135v1) · [repo](https://github.com/ArcInstitute/state) |
| `bfm-tamarind-bio` | verified | P4 | [official platform](https://www.tamarind.bio/) |
| `bfm-transcriptformer` | verified | P4 | [Paper](https://www.science.org/doi/10.1126/science.aec8514) · [repo](https://github.com/czi-ai/transcriptformer) |

Recommended correction order:

1. Legal/access semantics: AIDO.Cell, AIDO.RNA, AlphaFold Server, ChatCell, CONCH, LC-PLM, NeuralPLexer, PoET, Prot2Text, UNI, VirTues.
2. Broken/stale artifacts: Atlas, scConcept, scLinguist, scMulan, ChemBERTa-2.
3. Benchmark/status vocabulary: BEND, DNALONGBENCH, Genomic Benchmarks, NABench, TDC, GenePT.
4. Family/duplicate repair: FrameDiff/FrameFlow/Multiflow, NeuralPLexer/NP3, PoET/PoET-2/platform.
5. Scope HOLD decisions: ABodyBuilder3, ChromBPNet, DeepSEA, DRfold, FloraBERT, ProtGPS, scTranslator, Uni-Mol Docking V2.
6. Final-paper upgrades: BioMedGPT, BEND, GenSLMs, LangCell, LC-PLM, MolGen, PoET, ProTrek, SCEPTR, TDC, UCE.
