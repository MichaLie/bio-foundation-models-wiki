#!/usr/bin/env python3
"""Apply the delegated 2026-08-13 discovery, verification, and hold-review refresh.

Dated, idempotent migration for the protected FAIR preview; it never publishes.
Every record claim comes from the evidence bundles written the same day:

- evidence/additions-2026-08-13/fm_result_{1..13}.json  (candidate verdicts)
- evidence/additions-2026-08-13/update_checks_result.json (watchlist checks)
- evidence/hold-review-2026-08-13/fm_hold_review_{1..4}.json (register re-review)

Held and rejected candidates stay out of the displayed catalog; the audit note
evidence/DISCOVERY_AUDIT_2026-08-13.md records every decision.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "models_final.json"
REGISTER = ROOT / "records_under_review.json"
METADATA = ROOT / "resource_metadata.json"

DATE = "2026-08-13"
BASELINE_COMMIT = "251736f36a9ee98ba2351f59acc02745701f0b1a"
BASELINE_COMMIT_URL = (
    "https://github.com/MichaLie/bio-foundation-models-wiki/commit/"
    "251736f36a9ee98ba2351f59acc02745701f0b1a"
)
RESOURCE_VERSION = "2.1.0"

# schema.json constrains audit_source to the four recorded source-audit files, so
# new records reuse the initial audit path and name the real 2026-08-13 evidence
# bundle inside audit_note / review.reason instead.
AUDIT_SOURCE = "evidence/source-audit/foundation_initial.md"
REREVIEW_MARK = "Re-reviewed 2026-08-13"


def links(items: list[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"label": label, "url": url} for label, url in items]


def dedupe(urls: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            ordered.append(url)
    return ordered


def record(
    record_id: str,
    modality: str,
    name: str,
    description: str,
    io: str,
    status: str,
    use_cases: str,
    year: str,
    papers: list[tuple[str, str]],
    codes: list[tuple[str, str]],
    *,
    audit_note: str,
    noncommercial: bool = False,
    aliases: list[str] | None = None,
    audit_state: str = "verified",
    audit_priority: str = "P4",
    extra_sources: list[str] | None = None,
) -> dict:
    sources = dedupe(
        [url for _, url in papers] + [url for _, url in codes] + list(extra_sources or [])
    )
    return {
        "id": record_id,
        "date_added": DATE,
        "modality": modality,
        "name": name,
        "description": description,
        "paper_links": links(papers),
        "code_links": links(codes),
        "status": status,
        "io": io,
        "use_cases": use_cases,
        "year": year,
        "canonical": False,
        "noncommercial": noncommercial,
        "verified": DATE,
        "sources": sources,
        "audit_state": audit_state,
        "audit_priority": audit_priority,
        "audit_note": audit_note,
        "audit_source": AUDIT_SOURCE,
        "aliases": aliases or [],
    }


def added(slice_file: str, extra: str = "") -> str:
    base = (
        f"Added in the 2026-08-13 delegated discovery refresh; paper or official release "
        f"document, artifact ownership, and exact licence/access wording verified from "
        f"primary sources in evidence/additions-2026-08-13/{slice_file}."
    )
    return f"{base} {extra}".strip()


NEW_RECORDS: list[dict] = [
    # --- Benchmarks -------------------------------------------------------
    record(
        "bfm-geneb", "benchmark", "GENEB",
        "Diagnostic benchmark that linear-probes frozen representations from 40 genomic foundation models across 100 DNA classification tasks in 13 functional categories, under full-data, 10-shot, and 1-shot regimes.",
        "Frozen genomic-model embeddings + DNA classification tasks -> per-task, per-category and overall MCC, accuracy and macro-F1 scores",
        "Open harness + task data (Apache-2.0); public ungated leaderboard",
        "Genomic model selection, head-to-head comparison of DNA language models, few-shot representation evaluation",
        "2026",
        [("arXiv", "https://arxiv.org/abs/2606.04525")],
        [
            ("GitHub", "https://github.com/darlednik/GENEB"),
            ("Hugging Face task data", "https://huggingface.co/datasets/darlednik/geneb-tasks"),
            ("Leaderboard", "https://huggingface.co/spaces/darlednik/geneb-leaderboard"),
        ],
        aliases=["Genomic Embedding Benchmark"],
        audit_note=added("fm_result_1.json", "Apache-2.0 covers harness and task data; no gating."),
    ),
    record(
        "bfm-pg-llm", "benchmark", "PG-LLM",
        "ProteinGym-derived benchmark of 217 protein-variant ranking tasks in which a model ranks mutant sequences from the wild-type sequence and an assay description alone, without MSAs or structures, plus a contamination-control panel of 59 assays released after January 2026.",
        "Wild-type sequence + assay description + shuffled mutant set -> ranked mutants scored by nested-macro Spearman",
        "Open harness + frozen evaluation bundle (MIT); data released for evaluation use only and the contamination panel is available from the authors on request",
        "Variant-effect ranking benchmarks for general-purpose and protein language models, contamination-controlled evaluation, leaderboard submission",
        "2026",
        [("bioRxiv", "https://doi.org/10.64898/2026.07.27.741045")],
        [
            ("GitHub", "https://github.com/rohitarorayyc/proteingym-llm"),
            ("Leaderboard", "https://proteingymllm.com"),
            ("Evaluation data release", "https://github.com/rohitarorayyc/proteingym-llm/releases/tag/eval-data-v1.2"),
        ],
        aliases=["ProteinGym-LLM"],
        audit_state="verified_with_limits", audit_priority="P3",
        audit_note=added(
            "fm_result_1.json",
            "MIT code; the released data bundle carries an evaluation-only use policy and the 59-assay contamination panel is request-only.",
        ),
    ),

    # --- Complexes and structure -----------------------------------------
    record(
        "bfm-nesso-1", "complex", "Nesso-1",
        "Coarse-grained cofolding model from Valence Labs / Recursion that jointly predicts protein-ligand structure and binding affinity in about one second per prediction on a single GPU.",
        "Protein sequence + ligand (SMILES, CCD code or SDF) in an input YAML -> binding-affinity scalar, binder/non-binder score and cofolded complex",
        "Open code + weights (Apache-2.0), ungated",
        "High-throughput virtual screening, binding-affinity prediction, hit triage, selectivity assessment, embedding extraction",
        "2026",
        [("bioRxiv", "https://doi.org/10.64898/2026.08.01.742196")],
        [
            ("GitHub", "https://github.com/recursionpharma/nesso"),
            ("Hugging Face", "https://huggingface.co/recursionpharma/nesso"),
        ],
        aliases=["Nesso"],
        audit_note=added("fm_result_1.json", "Apache-2.0 on both code and weights, no gating."),
    ),
    record(
        "bfm-promera", "complex", "Promera",
        "Unified all-atom generative model from the Berger lab (MIT) that combines biomolecular co-folding with binder filtering and controllable minibinder and nanobody design under optional epitope, paratope and template constraints.",
        "JSON specification of protein, nucleic-acid and ligand chains with optional constraints -> all-atom complex structures, confidence/filtering scores and designed binder sequences",
        "Open code + weights (MIT), ungated",
        "All-atom co-folding, de novo binder and nanobody design, binder filtering, epitope-targeted design",
        "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.06.07.729267v1")],
        [
            ("GitHub", "https://github.com/bjing2016/promera"),
            ("Hugging Face", "https://huggingface.co/bjing-mit/promera"),
        ],
        audit_note=added("fm_result_2.json", "MIT on code and weights, no gating."),
    ),
    record(
        "bfm-decaf", "complex", "DeCAF (DeCAF-Boltz)",
        "Flow-map distillation framework from Genesis Molecular AI that turns all-atom co-folding diffusion models into few-step generators; the released DeCAF-Boltz checkpoint distils Boltz-1 into a few-step sampler, while the DeCAF-Pearl variant is described but not released.",
        "Boltz-format complex specification of protein sequences and ligands -> all-atom complex structures generated in a few sampling steps, with confidence scores",
        "Open code + DeCAF-Boltz weights (MIT), ungated; DeCAF-Pearl weights not released",
        "Fast all-atom co-folding, protein-ligand pose prediction, large-scale structure-based virtual screening",
        "2026",
        [("arXiv", "https://arxiv.org/abs/2606.08375")],
        [
            ("GitHub", "https://github.com/genesistherapeutics/decaf"),
            ("Hugging Face", "https://huggingface.co/genesisml/decaf"),
        ],
        aliases=["DeCAF-Boltz"],
        audit_note=added("fm_result_2.json", "MIT on code and released weights; the teacher model Boltz-1 is itself MIT."),
    ),

    # --- Molecules --------------------------------------------------------
    record(
        "bfm-fennix-bio1", "molecule", "FeNNix-Bio1",
        "Machine-learning interatomic potential in two sizes (S and M) for atomistic simulation of organic and biological systems, from the Piquemal group, trained on an extension of the SPICE2 quantum-chemistry dataset.",
        "Atomic coordinates and element types -> potential energy and forces for molecular dynamics, optimization and free-energy calculations",
        "Public ungated weights under the Academic Software License: academic non-commercial use only",
        "Molecular dynamics of organic and biological systems, geometry optimization, hydration and binding free-energy calculation, scoring in drug design",
        "2025",
        [("ChemRxiv", "https://doi.org/10.26434/chemrxiv-2025-f1hgn")],
        [
            ("Hugging Face", "https://huggingface.co/fennol-tools/FeNNix-Bio1"),
            ("FeNNol library", "https://github.com/FeNNol-tools/FeNNol"),
            ("Model files", "https://github.com/FeNNol-tools/FeNNol-PMC/tree/main/FENNIX-BIO1"),
        ],
        noncommercial=True,
        aliases=["FeNNix-Bio1 S", "FeNNix-Bio1 M"],
        audit_state="verified_with_limits", audit_priority="P2",
        audit_note=added(
            "fm_result_2.json",
            "The Academic Software Licence explicitly forbids commercial use, so noncommercial is true.",
        ),
    ),
    record(
        "bfm-chemate", "molecule", "CheMatE",
        "ModernBERT-based chemistry encoder that places SMILES strings and chemistry natural language in one shared embedding space through continued masked-language pretraining followed by Matryoshka contrastive fine-tuning.",
        "SMILES string or chemistry text -> dense embedding vector",
        "Open code + weights (MIT), ungated; evaluation datasets available on request",
        "Molecular property prediction, chemistry text embedding and retrieval, clustering, frozen-encoder features",
        "2026",
        [("arXiv", "https://arxiv.org/abs/2608.03855")],
        [
            ("GitHub", "https://github.com/schwallergroup/CheMatE"),
            ("Hugging Face", "https://huggingface.co/SchwallerGroup/CheMatE-v0"),
            ("Hugging Face (MLM base)", "https://huggingface.co/SchwallerGroup/CheMatE-v0-MLM"),
        ],
        aliases=["CheMatE-v0"],
        audit_note=added("fm_result_5.json", "MIT on code and both checkpoints, no gating."),
    ),
    record(
        "bfm-molexar", "molecule", "Molexar",
        "Molecular generation model built on Fragment-SELFIES, a fragment-aware molecular language with validity-preserving decoding, pretrained on UniChem-derived fragment records and fine-tuned for property-, pharmacophore-, sequence- and pocket-conditioned generation.",
        "Optional condition block (scalar properties, pharmacophore fingerprint, protein sequence or pocket) -> generated Fragment-SELFIES molecules decodable to SMILES",
        "Open code + weights (MIT), ungated",
        "De novo and fragment-constrained molecule generation, property-conditioned design, pocket- and target-conditioned design",
        "2026",
        [("arXiv", "https://arxiv.org/abs/2606.25865")],
        [
            ("GitHub", "https://github.com/fairydance/Molexar"),
            ("Hugging Face (base)", "https://huggingface.co/fairydance/molexar-10m-base"),
            ("Hugging Face (omni)", "https://huggingface.co/fairydance/molexar-10m-omni"),
        ],
        audit_note=added("fm_result_5.json", "MIT on code and both checkpoints, no gating."),
    ),
    record(
        "bfm-novomolgen", "molecule", "NovoMolGen",
        "Family of Llama-architecture molecular language models (32M, 157M and 300M parameters) pretrained on 1.5 billion ZINC-22 molecules and released with both atom-wise and BPE SMILES tokenizers.",
        "Start token or partial SMILES -> generated molecule SMILES and hidden-state embeddings",
        "Public MIT-licensed weights on Hugging Face, ungated; the source repository carries no licence file",
        "De novo molecule generation, goal-directed molecular optimization, reinforcement-learning molecular design",
        "2025",
        [("arXiv", "https://arxiv.org/abs/2508.13408")],
        [
            ("GitHub", "https://github.com/chandar-lab/NovoMolGen"),
            ("Hugging Face collection", "https://huggingface.co/collections/chandar-lab/novomolgen-681bce8b0e73b5dc7a3b0ff1"),
            ("Hugging Face (157M SMILES AtomWise)", "https://huggingface.co/chandar-lab/NovoMolGen_157M_SMILES_AtomWise"),
        ],
        audit_state="verified_with_limits", audit_priority="P3",
        audit_note=added("fm_result_6.json", "Weights are MIT; no LICENSE file exists in the code repository."),
    ),
    record(
        "bfm-reasyn", "molecule", "ReaSyn (NV-ReaSyn)",
        "NVIDIA encoder-decoder model that generates a molecule's synthetic pathway as a sequence over known reactions and building blocks, returning pathways for the closest synthesizable analog when the target itself is not synthesizable; v2 adds an Edit Flow refinement model.",
        "Molecule SMILES -> synthetic pathway over building blocks for the target or its closest synthesizable analog",
        "Open code (Apache-2.0) + public weights under the NVIDIA Open Model License, ungated and commercially usable",
        "Synthesis planning, synthesizable analog generation, synthesizability-constrained property optimization",
        "2026",
        [("arXiv", "https://arxiv.org/abs/2509.16084")],
        [
            ("GitHub", "https://github.com/NVIDIA-Digital-Bio/ReaSyn"),
            ("Hugging Face (autoregressive v2)", "https://huggingface.co/nvidia/NV-ReaSyn-AR-166M-v2"),
            ("Hugging Face (Edit Flow v2)", "https://huggingface.co/nvidia/NV-ReaSyn-EB-174M-v2"),
        ],
        aliases=["NV-ReaSyn"],
        audit_note=added("fm_result_6.json", "Apache-2.0 code and NVIDIA Open Model License weights, both stated on the official card."),
    ),
    record(
        "bfm-minimol", "molecule", "MiniMol",
        "Parameter-efficient molecular graph model (about 10M parameters) pretrained on roughly 3,300 quantum and biological graph- and node-level tasks, used as a frozen featurizer producing 512-dimensional fingerprints.",
        "SMILES strings -> 512-dimensional molecular fingerprint embeddings",
        "Open code + weights (MIT); weights ship in the GitHub repository and the pip package",
        "ADMET and molecular property prediction, low-data transfer learning, molecular featurization",
        "2024",
        [("arXiv", "https://arxiv.org/abs/2404.14986")],
        [
            ("GitHub", "https://github.com/graphcore-research/minimol"),
            ("PyPI", "https://pypi.org/project/minimol/"),
        ],
        audit_note=added("fm_result_6.json", "One MIT grant covers code and the bundled weights."),
    ),
    record(
        "bfm-chemeleon", "molecule", "CheMeleon",
        "Molecular foundation model pretrained to predict classical RDKit descriptors rather than experimental or simulated labels, giving a transferable representation usable as a frozen fingerprint or fine-tuned through chemprop.",
        "SMILES string or RDKit molecule -> molecular embedding, or fine-tuned property prediction",
        "Open code + weights (MIT); weights on Zenodo and auto-downloaded by chemprop",
        "Molecular property prediction, ADMET modelling, small-data transfer learning, fingerprint generation",
        "2025",
        [("arXiv", "https://arxiv.org/abs/2506.15792")],
        [
            ("GitHub", "https://github.com/JacksonBurns/chemeleon"),
            ("Zenodo weights", "https://zenodo.org/records/15426600"),
        ],
        audit_note=added("fm_result_6.json", "MIT on the repository and on the Zenodo weights record."),
    ),

    # --- DNA --------------------------------------------------------------
    record(
        "bfm-marindna", "dna", "MarinDNA",
        "Nucleotide-level causal DNA language model family from Open Athena trained on curated vertebrate genome regions, comprising a 1.12B-parameter flagship and an eight-model 46M-4B scaling ladder.",
        "DNA sequence (256-token context) -> nucleotide likelihoods, embeddings and variant-effect scores",
        "Open code + weights (Apache-2.0), ungated; documented by an official release write-up rather than a paper",
        "Zero-shot variant-effect prediction, genomic representation learning, DNA model scaling research",
        "2026",
        [("Open Athena release write-up", "https://openathena.ai/blog/marin-dna/")],
        [
            ("GitHub", "https://github.com/Open-Athena/marin-dna"),
            ("Hugging Face (m5.1 1B)", "https://huggingface.co/marin-dna/marin-dna-exp135-m5.1"),
            ("Hugging Face org", "https://huggingface.co/marin-dna"),
        ],
        aliases=["marin-dna"],
        audit_note=added("fm_result_3.json", "Apache-2.0 on code and weights; no preprint or DOI exists, so the official blog release is the primary document."),
    ),
    record(
        "bfm-ceno", "dna", "CENO",
        "Long-context autoregressive DNA foundation model family from Shanghai Artificial Intelligence Laboratory built on a Mamba, sparse-attention and mixture-of-experts hybrid backbone at 80M-1B parameters, with CENO-P variants post-trained on multi-species alignments for variant-effect scoring.",
        "DNA sequence with contexts up to about one million tokens -> likelihoods, embeddings, variant-effect scores or generated DNA",
        "Open code + 15 checkpoints (Apache-2.0), ungated; documented by a self-hosted technical report with no DOI",
        "Variant-effect prediction, long-context genome modelling, regulatory sequence design, embedding extraction",
        "2026",
        [
            ("Technical report", "https://cladeteam.github.io/ceno.github.io/assets/paper/CENO_Technical_Report_Version.pdf"),
            ("Project page", "https://cladeteam.github.io/ceno.github.io/"),
        ],
        [
            ("GitHub", "https://github.com/CladeTeam/CENO"),
            ("Hugging Face (CENO-1B-base)", "https://huggingface.co/CladeTeam/CENO-1B-base"),
            ("Hugging Face org", "https://huggingface.co/CladeTeam"),
        ],
        aliases=["CENO-P"],
        audit_note=added("fm_result_3.json", "Apache-2.0 on code and weights, LICENSE and NOTICE present in the weight repositories."),
    ),
    record(
        "bfm-ldarnet", "dna", "LDARNet",
        "Hierarchical genomic representation model with learnable tokenization: dynamic chunking learns content-aware token boundaries, a bidirectional BiMamba-2 backbone processes the compressed sequence, and dechunking restores base resolution.",
        "DNA sequence -> learned token boundaries, nucleotide and sequence embeddings, masked-token predictions",
        "Open code + 2M and 110M weights (Apache-2.0), ungated; checkpoints load through the project's own loader",
        "Genomic representation learning, regulatory and histone-mark classification, tokenization research",
        "2026",
        [("arXiv", "https://arxiv.org/abs/2606.04552")],
        [
            ("GitHub", "https://github.com/darlednik/ICML-LDARNet"),
            ("Hugging Face (110M)", "https://huggingface.co/darlednik/LDARNet-110M"),
            ("Hugging Face (2M)", "https://huggingface.co/darlednik/LDARNet-2M"),
        ],
        aliases=["DNA Adaptive Representation Network"],
        audit_note=added("fm_result_3.json", "Apache-2.0 declared on the repository and both model cards."),
    ),
    record(
        "bfm-carbon", "dna", "Carbon (Carbon-500M / 3B / 8B)",
        "Family of open autoregressive genomic foundation models at 500M, 3B and 8B parameters from Hugging Face Biology with partners, pretrained on about one trillion 6-mer tokens with a 32,768-token native context extendable through YaRN.",
        "DNA or RNA sequence as 6-mer tokens with optional metadata tokens -> generated sequence and token likelihoods for zero-shot variant scoring",
        "Open code + weights (Apache-2.0), ungated; documented by an official technical report with no DOI",
        "Genomic sequence generation and recovery, zero-shot variant-effect prediction, long-context genomic retrieval",
        "2026",
        [("Technical report", "https://github.com/huggingface/carbon/blob/main/tech-report.pdf")],
        [
            ("GitHub", "https://github.com/huggingface/carbon"),
            ("Hugging Face (Carbon-3B)", "https://huggingface.co/HuggingFaceBio/Carbon-3B"),
            ("Hugging Face (Carbon-8B)", "https://huggingface.co/HuggingFaceBio/Carbon-8B"),
            ("Hugging Face (Carbon-500M)", "https://huggingface.co/HuggingFaceBio/Carbon-500M"),
        ],
        aliases=["Carbon", "Carbon-500M", "Carbon-3B", "Carbon-8B"],
        audit_note=added("fm_result_4.json", "Apache-2.0 on code and all three checkpoints, no gating."),
    ),
    record(
        "bfm-moderngena", "dna", "ModernGENA (base / large)",
        "DNA foundation model from AIRI that adapts the ModernBERT encoder to genomic sequence modelling, released as base and large checkpoints pretrained by masked language modelling on 443 vertebrate genome assemblies with the GENA-LM BPE vocabulary.",
        "DNA sequence tokenized with the GENA-LM BPE vocabulary -> contextual embeddings and masked-token predictions",
        "Public ungated weights with no licence stated on either model card; release and fine-tuning code under MIT",
        "Nucleotide Transformer benchmark tasks, sequence classification, per-token regression on signal tracks",
        "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.04.21.719816v1")],
        [
            ("GitHub", "https://github.com/AIRI-Institute/GENA_LM/tree/main/examples/modernGENA"),
            ("Hugging Face (base)", "https://huggingface.co/AIRI-Institute/moderngena-base"),
            ("Hugging Face (large)", "https://huggingface.co/AIRI-Institute/moderngena-large"),
        ],
        aliases=["ModernGENA"],
        audit_state="verified_with_limits", audit_priority="P2",
        audit_note=added(
            "fm_result_4.json",
            "Neither weight repository declares a licence; only the code repository is MIT, so checkpoint reuse terms are unresolved.",
        ),
    ),
    record(
        "bfm-botanic-0", "dna", "BOTANIC-0 (Botanic0-S / -M / -L)",
        "Family of plant genomic foundation models from Living Models spanning about 100M to 1B parameters, pretrained by masked language modelling on nuclear DNA from 43 phylogenetically diverse plant genomes.",
        "Plant DNA sequence as 6-mer tokens -> contextual embeddings and masked-token predictions for zero-shot scoring and fine-tuning",
        "Weights behind an automatic contact-sharing gate under a custom research-only, non-commercial licence",
        "Regulatory element annotation, gene expression inference, variant effect prediction, crop genotype-to-phenotype modelling",
        "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.02.23.706817v2")],
        [
            ("Hugging Face (Botanic0-L)", "https://huggingface.co/living-models/Botanic0-L"),
            ("Hugging Face (Botanic0-M)", "https://huggingface.co/living-models/Botanic0-M"),
            ("Hugging Face (Botanic0-S)", "https://huggingface.co/living-models/Botanic0-S"),
        ],
        noncommercial=True,
        aliases=["Botanic0"],
        audit_state="verified_with_limits", audit_priority="P2",
        audit_note=added(
            "fm_result_4.json",
            "Custom livingmodels-research licence is research-use only and all three repositories are auto-gated.",
        ),
    ),

    # --- Multimodal -------------------------------------------------------
    record(
        "bfm-mkb", "multimodal", "MKB (Monkey King Bang)",
        "Unified scientific multimodal model from the Shanghai Academy of AI for Science that wraps native scientific encoders and decoders around a shared vision-language backbone (about 11.7B parameters), covering protein, RNA, DNA, molecule, weather, medical-image and text modalities through one natural-language interface.",
        "Natural-language prompt plus a sequence, molecule, gridded weather field or medical image -> answers, generated RNA or SMILES, forecasts or segmentation masks",
        "Public ungated weights under a composite licence: Apache-2.0 for code and all weights except the SAM 3 medical-image branch, which follows Meta's SAM License",
        "Cross-modal scientific question answering, sequence understanding, text-to-molecule and RNA design, medical-image segmentation",
        "2026",
        [("Technical report", "https://github.com/Shanghai-Academy-of-AI-For-Science/MKB/blob/main/docs/MKB.pdf")],
        [
            ("GitHub", "https://github.com/Shanghai-Academy-of-AI-For-Science/MKB"),
            ("Hugging Face", "https://huggingface.co/sais-org/MKB"),
        ],
        aliases=["MKB", "Monkey King Bang"],
        audit_state="verified_with_limits", audit_priority="P3",
        audit_note=added(
            "fm_result_4.json",
            "Composite terms: the SAM 3 branch carries Meta's SAM License with acceptable-use restrictions; the card shows gating text while the hub API reports the repository as ungated.",
        ),
    ),
    record(
        "bfm-mgm2", "multimodal", "MGM2",
        "Multimodal microbiome foundation model pretrained on 1,821,291 MicrobeAtlas samples and 225,067 OTUs, coupling sequence embeddings with relative-abundance conditioning and community-semantic alignment; released in four scales.",
        "OTU/ASV abundance table with optional representative sequences -> microbial token embeddings and a community-level embedding",
        "Public ungated code and four checkpoints, but no licence is declared for either code or weights",
        "Biome classification, faecal microbiota transplantation response prediction, wastewater community forecasting",
        "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.07.20.739063v1")],
        [
            ("GitHub", "https://github.com/HUST-NingKang-Lab/MGM2"),
            ("Hugging Face", "https://huggingface.co/LudensZhang/MGM2"),
        ],
        noncommercial=True,
        aliases=["MGM v2"],
        audit_state="verified_with_limits", audit_priority="P2",
        audit_note=added(
            "fm_result_6.json",
            "No LICENSE file exists on GitHub and the model card declares no licence, so reuse rights are not granted; the preprint text is CC BY-NC 4.0.",
        ),
    ),

    # --- Platforms --------------------------------------------------------
    record(
        "bfm-bionemo-agent-toolkit", "platform", "NVIDIA BioNeMo Agent Toolkit",
        "NVIDIA toolkit that packages its life-science model and library stack as agent-callable skills, so an agent can select, run and interpret bio foundation models across single tasks and multi-step workflows.",
        "Agent skill invocation with biological inputs -> outputs of the underlying BioNeMo models with interpretation guidance",
        "Open source (Apache-2.0 code, CC BY 4.0 skills and docs); underlying models keep their own licences and hosted endpoints need an NVIDIA API key",
        "Structure prediction, docking, generative chemistry, protein and binder design, genomics analysis, agentic discovery workflows",
        "2026",
        [],
        [
            ("GitHub", "https://github.com/NVIDIA-BioNeMo/bionemo-agent-toolkit"),
            ("NVIDIA developer blog", "https://developer.nvidia.com/blog/build-an-ai-scientist-for-life-science-discovery-with-nvidia-bionemo-agent-toolkit/"),
        ],
        aliases=["BioNeMo Agent Toolkit", "BioNeMo Skills"],
        audit_note=added(
            "fm_result_7.json",
            "Dual Apache-2.0 OR CC-BY-4.0 licence quoted from the repository LICENSE; distinct from the existing NVIDIA BioNeMo framework record.",
        ),
    ),
    record(
        "bfm-boltz-lab", "platform", "Boltz Lab / Boltz API",
        "Hosted platform and API from Boltz PBC serving the company's biomolecular models with managed compute: BoltzMol-1 for small-molecule hit discovery and BoltzProt-1 for protein design, alongside the open Boltz model lineage.",
        "Target, ligands and job specification through the web interface or SDK -> designed molecules or binders with predicted structure, affinity and ADME properties",
        "Commercial hosted service with a self-serve free tier, then usage-based pricing; hosted models have no public weights, while Boltz-2 and BoltzGen remain open source",
        "Small-molecule hit discovery, de novo protein and nanobody design, structure and affinity prediction, agentic discovery pipelines",
        "2026",
        [],
        [
            ("Boltz platform", "https://boltz.bio/platform"),
            ("Boltz API", "https://boltz.bio/api"),
            ("Open Boltz models", "https://github.com/jwohlwend/boltz"),
        ],
        aliases=["Boltz Lab", "Boltz API", "Boltz PBC"],
        audit_state="verified_with_limits", audit_priority="P2",
        audit_note=added(
            "fm_result_7.json",
            "Hosted commercial access only for BoltzMol-1 and BoltzProt-1; pricing and free-tier wording taken from first-party pages.",
        ),
    ),

    # --- Proteins ---------------------------------------------------------
    record(
        "bfm-protgpt3", "protein", "ProtGPT3",
        "Open family of autoregressive protein language models from the Ferruz lab spanning 112M to 10B parameters in a sparse mixture-of-experts architecture, with DPO-aligned variants and an MSA-promptable model for homolog-conditioned generation.",
        "Amino-acid prefix with a direction token, or a prompt of homologous sequences -> generated protein sequences and per-sequence likelihoods",
        "Seven ungated checkpoints on Hugging Face described as open source in the paper, but no licence is declared on the model cards or code repository",
        "De novo protein generation, family-conditioned and homolog-prompted design, zero-shot variant scoring, enzyme design",
        "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.06.04.730041v1")],
        [
            ("Hugging Face collection", "https://huggingface.co/collections/AI4PD/protgpt3-family"),
            ("GitHub", "https://github.com/michele1993/protGPT3"),
        ],
        audit_state="verified_with_limits", audit_priority="P2",
        audit_note=added(
            "fm_result_8.json",
            "No SPDX licence exists on any of the seven model cards or in the code repository; the only availability statement is the paper's appendix.",
        ),
    ),
    record(
        "bfm-msa-pairformer", "protein", "MSA Pairformer",
        "111M-parameter MSA-based protein language model that adapts AlphaFold's Pairformer sequence-pair updates into a pretrained model of protein and protein-protein coevolution, published in Cell after a 2025 preprint and weight release.",
        "Query sequence plus its multiple sequence alignment -> sequence and pairwise embeddings, contact maps and zero-shot variant scores",
        "Open code + weights under a modified MIT licence that explicitly permits commercial use, ungated",
        "Protein embedding, unsupervised and interface contact prediction, interacting-pair screening, variant-effect prediction",
        "2025",
        [
            ("Cell", "https://doi.org/10.1016/j.cell.2026.06.029"),
            ("bioRxiv", "https://www.biorxiv.org/content/10.1101/2025.08.02.668173v1"),
        ],
        [
            ("GitHub", "https://github.com/yoakiyama/MSA_Pairformer"),
            ("Hugging Face", "https://huggingface.co/yoakiyama/MSA-Pairformer"),
        ],
        audit_note=added("fm_result_8.json", "Modified MIT licence covers code and weights and states commercial use is permitted."),
    ),
    record(
        "bfm-prollama", "protein", "ProLLaMA",
        "Llama-2-7B-based multitask protein language model trained by continued pretraining on protein sequences followed by instruction tuning, handling both superfamily-conditioned generation and protein understanding tasks.",
        "Instruction such as generate-by-superfamily or determine-superfamily, optionally with an amino-acid prefix -> generated sequence or predicted superfamily",
        "Public ungated weights and Apache-2.0 code; the checkpoints derive from Llama-2-7B and the cards direct users to the Llama 2 licence",
        "Controllable protein generation by superfamily, prefix-conditioned generation, superfamily prediction, instruction-style protein tasks",
        "2024",
        [("arXiv", "https://arxiv.org/abs/2402.16445")],
        [
            ("GitHub", "https://github.com/PKU-YuanGroup/ProLLaMA"),
            ("Hugging Face (instruction-tuned)", "https://huggingface.co/GreatCaptainNemo/ProLLaMA"),
            ("Hugging Face (Stage 1)", "https://huggingface.co/GreatCaptainNemo/ProLLaMA_Stage_1"),
        ],
        aliases=["ProLLaMA_Stage_1"],
        audit_state="verified_with_limits", audit_priority="P2",
        audit_note=added(
            "fm_result_8.json",
            "Cards declare apache-2.0 but also instruct users to follow the Llama 2 licence for the derived weights, so reuse is constrained by the base-model terms.",
        ),
    ),

    # --- RNA --------------------------------------------------------------
    record(
        "bfm-utrgen", "rna", "UTRGen",
        "Unified 5' UTR modelling framework built on a small autoregressive decoder pretrained on multi-species 5' UTR sequence and adapted through lightweight heads to translation efficiency, expression, ribosome load and IRES tasks, with reinforcement-learning-guided design.",
        "Nucleotide prompt or 5' UTR sequence -> generated UTRs, or predicted translation efficiency, expression, ribosome load and IRES class",
        "Open MIT code; pretrained checkpoints distributed as a publicly shared Google Drive archive with no separate terms",
        "5' UTR generation and design, translation efficiency and expression prediction, IRES identification",
        "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.06.26.734691v1")],
        [
            ("GitHub", "https://github.com/HIM-AIM/UTRGen"),
            ("Checkpoints and data", "https://drive.google.com/drive/folders/1E4TYXN48wdDru_-ETVxu2UWYSEKvO0wr"),
        ],
        audit_state="verified_with_limits", audit_priority="P3",
        audit_note=added(
            "fm_result_8.json",
            "The Drive folder is world-readable and lists the checkpoint archive, but its contents were not opened and Drive is not a permanent archive.",
        ),
    ),
    record(
        "bfm-shifu-lmr", "rna", "Shifu-LMR",
        "Family of compact masked-language-model RNA backbones released as the model component of the Shifu framework, spanning 65M to 290M parameters including a 4,096-token long-context variant, alongside a leakage-audited corpus and evaluation protocol.",
        "RNA nucleotide sequence -> contextual residue embeddings and masked-token predictions for fine-tuning",
        "Open code + four checkpoints (MIT), ungated; corpus databases retain their own terms",
        "RNA representation learning, secondary-structure prediction after fine-tuning, leakage-free benchmarking, continued pretraining",
        "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.07.15.738762v1")],
        [
            ("GitHub", "https://github.com/Vicens-Lab/LMR"),
            ("Hugging Face (LMR-mini, 65M)", "https://huggingface.co/GaboG7/LMR-mini"),
            ("Hugging Face (LMR-v0, 289M)", "https://huggingface.co/GaboG7/LMR-v0"),
            ("Hugging Face (LMR-G, 228M)", "https://huggingface.co/GaboG7/LMR-G"),
            ("Hugging Face (LMR-Long, 4k context)", "https://huggingface.co/GaboG7/LMR-Long"),
        ],
        aliases=["Shifu", "LMR", "Shifu-LMR-Nano"],
        audit_note=added("fm_result_8.json", "MIT on the repository and all four weight repositories, none gated."),
    ),
    record(
        "bfm-numonomer", "rna", "NUMonomer",
        "End-to-end model that predicts three-dimensional RNA and single-stranded DNA structures directly from sequence, without MSAs, secondary-structure annotations or language-model features.",
        "RNA or single-stranded DNA sequence -> predicted 3D structure with confidence scores",
        "Open MIT code; pretrained weights distributed through the authors' Google Drive folder",
        "RNA 3D structure prediction, ssDNA structure prediction, large-scale structure modelling",
        "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.07.20.739453v1")],
        [
            ("GitHub", "https://github.com/yunda-si/NUMonomer"),
            ("Pretrained weights", "https://drive.google.com/drive/folders/1K9fG3ndV2UH3atwyrxHDqPN-oHyvhRwG"),
        ],
        audit_state="verified_with_limits", audit_priority="P3",
        audit_note=added(
            "fm_result_9.json",
            "MIT is the only stated grant; the checkpoint file is listed in the public Drive folder but was not downloaded.",
        ),
    ),
    record(
        "bfm-rnapro", "rna", "RNAPro",
        "NVIDIA RNA 3D structure prediction model developed with the hosts and winners of a public RNA folding competition, coupling an all-atom co-folding trunk with MSAs, template modelling and the frozen RibonanzaNet2 RNA foundation model.",
        "RNA sequence with MSAs and templates -> all-atom 3D structure",
        "Open code (Apache-2.0) + public weights under the NVIDIA Open Model License, ungated",
        "RNA 3D structure prediction, template-based RNA modelling, structure-driven RNA drug discovery",
        "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2025.12.30.696949v1")],
        [
            ("GitHub", "https://github.com/NVIDIA-BioNeMo/RNAPro"),
            ("Hugging Face", "https://huggingface.co/nvidia/RNAPro-Public-Best-500M"),
        ],
        audit_note=added("fm_result_9.json", "Apache-2.0 code and NVIDIA Open Model License weights, both quoted from official artifacts."),
    ),
    record(
        "bfm-rnaelectra", "rna", "RNAElectra",
        "Single-nucleotide-resolution RNA language model pretrained on RNAcentral non-coding RNAs with a replaced-token-detection objective rather than masked language modelling, released as a reusable discriminator backbone.",
        "RNA sequence -> per-nucleotide contextual embeddings for fine-tuning",
        "Open weights (Apache-2.0), ungated; no separate code repository",
        "RNA structure and function prediction, RNA-protein and RNA-RNA interaction prediction, modification and stability prediction",
        "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.03.15.711950v1")],
        [("Hugging Face", "https://huggingface.co/FreakingPotato/RNAElectra")],
        audit_note=added("fm_result_9.json", "Apache-2.0 declared on the model card; the preprint's data-availability statement confirms author ownership of the upload."),
    ),
    record(
        "bfm-dgrna", "rna", "DGRNA",
        "Long-context RNA foundation model built on bidirectional Mamba2 with attention, pretrained on 100 million RNA sequences to avoid the quadratic cost of attention on long RNAs.",
        "RNA sequence -> per-nucleotide contextual embeddings for fine-tuning",
        "Open MIT code; pretrained weights distributed through the authors' Google Drive folder",
        "RNA embedding extraction, RNA structure and function prediction, long RNA modelling",
        "2024",
        [("bioRxiv", "https://www.biorxiv.org/content/10.1101/2024.10.31.621427v1")],
        [
            ("GitHub", "https://github.com/TimothyChen225/DGRNA"),
            ("Pretrained weights", "https://drive.google.com/drive/folders/1LQOIo-fvij3L2dPEA2zfyOGNn3mkz4KE"),
        ],
        audit_state="verified_with_limits", audit_priority="P3",
        audit_note=added(
            "fm_result_9.json",
            "MIT is the only stated grant; the checkpoint filename is listed in the public Drive folder but was not downloaded.",
        ),
    ),
    record(
        "bfm-ribonanzanet2", "rna", "RibonanzaNet2",
        "Das lab RNA foundation model pretrained to map RNA sequence to per-nucleotide chemical reactivity for DMS and SHAPE probes; the released alpha checkpoint supplies frozen sequence and pairwise features reused by downstream models such as RNAPro.",
        "RNA sequence -> per-nucleotide DMS and SHAPE reactivity profiles plus sequence and pairwise representations",
        "Public MIT-licensed alpha weights on Kaggle and MIT training code; no RibonanzaNet2-specific paper exists",
        "Chemical reactivity prediction, RNA secondary structure prediction, embedding backbone for RNA 3D structure prediction",
        "2025",
        [
            ("bioRxiv (describes RNet2 use)", "https://www.biorxiv.org/content/10.64898/2025.12.30.696949v1"),
            ("RibonanzaNet v1 preprint", "https://www.biorxiv.org/content/10.1101/2024.02.24.581671v1"),
        ],
        [
            ("Kaggle model weights", "https://www.kaggle.com/models/shujun717/ribonanzanet2"),
            ("GitHub training code", "https://github.com/Shujun-He/RibonanzaNet2"),
        ],
        aliases=["RNet2"],
        audit_state="verified_with_limits", audit_priority="P3",
        audit_note=added(
            "fm_result_9.json",
            "Weight metadata and the MIT instance licence were read through the Kaggle public API after a parallel lane could not render the HTML page; the release is self-described as an alpha and has no dedicated paper.",
        ),
    ),

    # --- Single cell ------------------------------------------------------
    record(
        "bfm-perturbgen", "singlecell", "PerturbGen",
        "Generative single-cell model from the Lotfollahi lab trained on over 100 million transcriptomes that predicts perturbation responses along cellular trajectories rather than at a single static state.",
        "Source-state expression + genetic perturbation + target state -> predicted target-state expression, gene embeddings and gene programs",
        "Open MIT code; the pretraining checkpoint is publicly downloadable and ungated but the model card states no licence",
        "Trajectory-aware perturbation prediction, gene-program discovery, in silico genetic screens",
        "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.03.04.709254v1")],
        [
            ("GitHub", "https://github.com/Lotfollahi-lab/Perturbgen"),
            ("Hugging Face", "https://huggingface.co/lotfollahi-lab/PerturbGen"),
        ],
        audit_state="verified_with_limits", audit_priority="P3",
        audit_note=added("fm_result_10.json", "Code is MIT; the weights ship without any stated licence."),
    ),

    # --- Spatial and pathology -------------------------------------------
    record(
        "bfm-prism2", "spatial", "PRISM2",
        "Paige multimodal slide-level pathology foundation model coupling a whole-slide Perceiver encoder to a language-model decoder, trained on 2.3 million whole-slide images with report-derived question-answer pairs; released with a survival-finetuned variant.",
        "Virchow2 tile embeddings of a whole-slide image + optional text prompt -> slide-level embedding and diagnostic text",
        "Gated weights (manual approval, institutional email) under CC BY-NC-ND-4.0, non-commercial research only",
        "Slide-level embeddings, cancer detection, diagnostic question answering, biomarker and survival prediction",
        "2026",
        [
            ("Nature Medicine", "https://doi.org/10.1038/s41591-026-04521-4"),
            ("arXiv", "https://arxiv.org/abs/2506.13063"),
        ],
        [
            ("Hugging Face", "https://huggingface.co/paige-ai/Prism2"),
            ("Hugging Face (survival)", "https://huggingface.co/paige-ai/Prism2-survival"),
            ("Zenodo evaluation", "https://zenodo.org/records/19056118"),
        ],
        noncommercial=True,
        audit_state="verified_with_limits", audit_priority="P2",
        audit_note=added(
            "fm_result_11.json",
            "Successor to the separate PRISM record, whose links were narrowed to PRISM v1 in the same migration; weights are manually gated and non-commercial.",
        ),
    ),
    record(
        "bfm-kronos2", "spatial", "KRONOS2",
        "Second-generation marker-aware vision foundation model for multiplex spatial proteomics from the Mahmood Lab, pretrained with a 268-marker vocabulary to produce one embedding per multiplexed image patch conditioned on the markers present.",
        "Multiplex spatial proteomics image patch -> 768-dimensional marker-aware patch embedding",
        "Gated weights (manual approval, institutional email) under CC BY-NC-ND-4.0; no dedicated KRONOS2 paper yet, the card cites the KRONOS v1 paper",
        "Cell phenotyping, tissue classification, biomarker discovery, patient stratification from multiplex imaging",
        "2026",
        [("arXiv (KRONOS v1)", "https://arxiv.org/abs/2506.03373")],
        [
            ("Hugging Face", "https://huggingface.co/MahmoodLab/KRONOS2"),
            ("GitHub (KRONOS)", "https://github.com/mahmoodlab/KRONOS"),
        ],
        noncommercial=True,
        aliases=["KRONOSv2"],
        audit_state="verified_with_limits", audit_priority="P2",
        audit_note=added(
            "fm_result_11.json",
            "Separate release from the existing KRONOS record; a KRONOS2 technical report is announced but not published.",
        ),
    ),
    record(
        "bfm-gigapath-flash", "spatial", "GigaPath-Flash",
        "Efficient distillations of the Prov-GigaPath pathology foundation model from Microsoft Research: a ViT-S/16 tile encoder with a LongNet slide encoder retaining most slide-level performance at far lower compute, plus the companion GigaTIME-Flash that predicts virtual multiplexed-immunofluorescence maps from H&E tiles.",
        "H&E tiles and whole-slide images -> tile and slide embeddings; H&E tiles -> 23-channel virtual multiplexed-immunofluorescence maps",
        "Apache-2.0 weights behind a click-through contact gate; the model cards restrict intended use to research and exclude deployment",
        "Whole-slide representation learning, slide-level classification and biomarker prediction, tumour microenvironment mapping",
        "2026",
        [("arXiv", "https://arxiv.org/abs/2607.18218")],
        [
            ("Hugging Face (GigaPath-Flash)", "https://huggingface.co/prov-gigapath/prov-gigapath-flash"),
            ("Hugging Face (GigaTIME-Flash)", "https://huggingface.co/prov-gigatime/gigatime-flash"),
            ("GitHub (GigaTIME)", "https://github.com/prov-gigatime/GigaTIME"),
        ],
        aliases=["GigaTIME-Flash", "Prov-GigaPath-Flash"],
        audit_state="verified_with_limits", audit_priority="P3",
        audit_note=added(
            "fm_result_12.json",
            "Apache-2.0 is the operative licence, but the cards' research-only intended-use text and the access gate are recorded in the status field.",
        ),
    ),
    record(
        "bfm-alice", "spatial", "ALICE",
        "General-purpose computational pathology foundation model built by multi-stage agglomerative distillation of eight vision, vision-language and slide-level teacher models into a single backbone, evaluated across 96 downstream tasks.",
        "Pathology tiles or whole-slide images, optionally with text -> tile-, vision-language- and slide-level embeddings",
        "Gated weights (manual approval) under CC BY-NC-ND-4.0, non-commercial research only",
        "Tissue and tile classification, pathology vision-language tasks, whole-slide diagnosis and prognosis",
        "2026",
        [("arXiv", "https://arxiv.org/abs/2607.09526")],
        [
            ("GitHub", "https://github.com/WonderLandxD/ALICE"),
            ("Hugging Face", "https://huggingface.co/JWonderLand/ALICE"),
        ],
        noncommercial=True,
        audit_state="verified_with_limits", audit_priority="P2",
        audit_note=added("fm_result_12.json", "CC BY-NC-ND-4.0 on both the repository and the manually gated weights."),
    ),
    record(
        "bfm-tissueformer", "spatial", "TissueFormer",
        "Multimodal foundation model from the Uhler lab for paired histopathology and spatial transcriptomics at single-cell resolution, using linear-complexity whole-slide attention over more than 17 million image-expression pairs.",
        "Histology images with or without paired spatial transcriptomics -> single-cell spatial expression predictions and cell-, region- and slide-level embeddings",
        "Open MIT code; pretrained checkpoints distributed through Google Drive links in the official repository with no separate terms",
        "Spatial gene-expression prediction from H&E, cell- region- and slide-level diagnosis, mechanism hypothesis generation",
        "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.07.31.741265v1")],
        [("GitHub", "https://github.com/uhlerlab/TissueFormer")],
        audit_state="verified_with_limits", audit_priority="P3",
        audit_note=added("fm_result_12.json", "MIT repository licence is the only grant covering the Drive-hosted checkpoints."),
    ),
    record(
        "bfm-cellworld", "spatial", "CellWorld",
        "Joint-embedding predictive foundation model for spatial transcriptomics in which cells are tokens and masked spatial regions are predicted in latent space rather than reconstructed as gene counts; four variants pretrained on 46 million human cells.",
        "Spatially resolved single-cell expression with coordinates -> latent cell embeddings, with probe and finetune heads for annotation and niche prediction",
        "Open code + weights (MIT), ungated, four scales",
        "Spatial transcriptomics representation learning, cell-type annotation, tissue region and niche prediction",
        "2026",
        [("arXiv", "https://arxiv.org/abs/2608.06659")],
        [
            ("GitHub", "https://github.com/UoM-HealthAI/CellWorld"),
            ("Hugging Face", "https://huggingface.co/Haiping-UoM/CellWorld"),
        ],
        audit_note=added("fm_result_12.json", "MIT on code and weights; the weight repository became public and ungated before verification."),
    ),
    record(
        "bfm-seal", "spatial", "SEAL",
        "Self-supervised framework from the Mahmood Lab that finetunes existing patch-level pathology foundation models against paired spatial transcriptomics, yielding molecularly aligned drop-in vision encoders with matched expression encoders; CONCH and UNIv2 variants are released.",
        "H&E histology patch -> molecularly aligned patch embedding, with a paired expression encoder for cross-modal retrieval",
        "Click-through gated weights under CC BY-NC-ND 4.0; the code repository states no licence",
        "Molecular status and expression prediction, treatment-response assessment, gene-image retrieval, patch- and slide-level tasks",
        "2026",
        [("arXiv", "https://arxiv.org/abs/2602.14177")],
        [
            ("GitHub", "https://github.com/mahmoodlab/SEAL"),
            ("Hugging Face", "https://huggingface.co/MahmoodLab/SEAL"),
        ],
        noncommercial=True,
        aliases=["Spatial Expression-Aligned Learning"],
        audit_state="verified_with_limits", audit_priority="P2",
        audit_note=added(
            "fm_result_13.json",
            "Weights are CC BY-NC-ND 4.0 and gated; the GitHub repository has no licence file, so code terms are unspecified.",
        ),
    ),
    record(
        "bfm-spatialfusion", "spatial", "SpatialFusion",
        "Lightweight multimodal model from the Uhler lab that fuses histology and spatial-transcriptomics embeddings from pretrained backbones into joint neighbourhood representations and pathway-informed spatial niches at single-cell resolution.",
        "Paired histology and spatial transcriptomics embeddings -> joint neighbourhood embedding and pathway-informed niche assignments",
        "Open source (MIT) with pretrained checkpoints for each backbone combination bundled in the package",
        "Spatial niche mapping, multimodal spatial embedding, tumour microenvironment characterization, cohort finetuning",
        "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.03.16.712056v1")],
        [
            ("GitHub", "https://github.com/uhlerlab/spatialfusion"),
            ("Zenodo benchmark data", "https://zenodo.org/records/20934900"),
        ],
        audit_note=added(
            "fm_result_13.json",
            "MIT covers code and the bundled checkpoints; the fusion heads are small modules over frozen third-party encoders.",
        ),
    ),
    record(
        "bfm-path-foundation", "spatial", "Path Foundation",
        "Google Health AI histopathology embedding model: a ViT-S trained with masked siamese networks on 60 million H&E patches from public tumour studies at three magnifications, producing 384-dimensional patch embeddings.",
        "H&E histopathology patch -> 384-dimensional embedding",
        "Weights gated by click-through acceptance of Google's Health AI Developer Foundations terms; commercial use permitted subject to those use restrictions",
        "Tumour identification and grading, biomarker detection, similar-image search, data-efficient pathology classifiers",
        "2023",
        [("arXiv", "https://arxiv.org/abs/2310.13259")],
        [
            ("Hugging Face", "https://huggingface.co/google/path-foundation"),
            ("Developer documentation", "https://developers.google.com/health-ai-developer-foundations/path-foundation"),
        ],
        aliases=["google/path-foundation"],
        audit_state="verified_with_limits", audit_priority="P2",
        audit_note=added(
            "fm_result_13.json",
            "Custom Health AI Developer Foundations terms with use restrictions and a click-through gate; Google documents it as an older single-modality model.",
        ),
    ),
]


# Existing displayed records that materially change in this refresh.
CATALOG_UPDATES: dict[str, dict] = {
    # The dead Hugging Face artifact prescribed for removal by the 2026-07-13
    # audit was re-checked on 2026-08-13 (401 on page and API, no public
    # relocation) and is now removed from links and sources.
    "bfm-scmulan": {
        "status": "Public code + official externally hosted checkpoint; the former model-hub copy is gone",
        "audit_note": (
            "Dead Hugging Face artifact removed on 2026-08-13 after re-verification (401 on both page and API, "
            "no public relocation found); the official repository and the Tsinghua Cloud checkpoint remain. "
            "Completes the action recorded in the 2026-07-13 source audit."
        ),
        "date_modified": DATE,
    },
    # PRISM2 is now a separate verified record, so the PRISM entry is narrowed
    # to PRISM v1 and its PRISM2 links move to bfm-prism2.
    "bfm-prism": {
        "description": (
            "Paige multimodal generative slide-level pathology foundation model built on Virchow tile features "
            "(587k WSIs, 195k clinical reports); the PRISM2 successor is catalogued as a separate record."
        ),
        "paper_links": links([("arXiv", "https://arxiv.org/abs/2405.10254")]),
        "code_links": links([("Hugging Face", "https://huggingface.co/paige-ai/Prism")]),
        "sources": [
            "https://arxiv.org/abs/2405.10254",
            "https://huggingface.co/paige-ai/Prism",
        ],
        "audit_note": (
            "set NC true; PRISM is a gated CC BY-NC-ND model. Narrowed to PRISM v1 on 2026-08-13 when the "
            "separately verified PRISM2 record was added (evidence/additions-2026-08-13/fm_result_11.json)."
        ),
        "date_modified": DATE,
    },
}

SCMULAN_DEAD_LINK = "https://huggingface.co/deeplife/scmulan_model"


# Promotions out of the under-review register. Each patch is applied to the
# register's stored record, which keeps its stable id and original date_added.
PROMOTIONS: dict[str, dict] = {
    "bfm-chemberta-3": {
        "description": (
            "Open training and benchmarking framework for chemical foundation models, published in Digital "
            "Discovery, with released c3 checkpoints (a 1.1B c3-MoLFormer and a 100M ChemBERTa MLM) on the "
            "DeepChem model hub."
        ),
        "status": "Open framework + released checkpoints (MIT); two smaller c3-MoLFormer repositories are still weight-free",
        "use_cases": "Re-training and benchmarking chemical encoders, molecular property prediction, chemical model fine-tuning",
        "year": "2026",
        "paper_links": links([("Digital Discovery", "https://doi.org/10.1039/D5DD00348B")]),
        "code_links": links([
            ("GitHub", "https://github.com/deepforestsci/chemberta3"),
            ("Hugging Face (MoLFormer-c3-1.1B)", "https://huggingface.co/DeepChem/MoLFormer-c3-1.1B"),
            ("Hugging Face (ChemBERTa-100M-MLM)", "https://huggingface.co/DeepChem/ChemBERTa-100M-MLM"),
        ]),
        "sources": [
            "https://doi.org/10.1039/D5DD00348B",
            "https://github.com/deepforestsci/chemberta3",
            "https://huggingface.co/DeepChem/MoLFormer-c3-1.1B",
            "https://huggingface.co/DeepChem/ChemBERTa-100M-MLM",
        ],
        "noncommercial": False,
        "audit_state": "verified",
        "audit_priority": "P4",
        "audit_note": (
            "Promoted from the under-review register on 2026-08-13: the published Digital Discovery article "
            "(10.1039/D5DD00348B) confirms the training-framework scope and MIT covers both the framework and the "
            "released checkpoints. Evidence: evidence/hold-review-2026-08-13/fm_hold_review_4.json."
        ),
    },
    "bfm-virchow-virchow2-and-virchow2g": {
        "description": (
            "Paige/MSK self-supervised ViT-H tile-level pathology foundation models: Virchow (632M parameters, "
            "1.5M WSIs), Virchow2 (3.1M+ WSIs) and the 1.85B-parameter Virchow2G, which has no public weights."
        ),
        "status": (
            "Member-specific terms: Virchow is Apache-2.0 behind an automatic gate, Virchow2 is CC BY-NC-ND-4.0 "
            "non-commercial behind an automatic gate, and Virchow2G is commercial-licence-only with no public weights"
        ),
        "paper_links": links([
            ("Nature Medicine (Virchow)", "https://www.nature.com/articles/s41591-024-03141-0"),
            ("arXiv (Virchow2)", "https://arxiv.org/abs/2408.00738"),
        ]),
        "code_links": links([
            ("Hugging Face (Virchow)", "https://huggingface.co/paige-ai/Virchow"),
            ("Hugging Face (Virchow2)", "https://huggingface.co/paige-ai/Virchow2"),
            ("Official family access", "https://www.paige.ai/foundation-models"),
        ]),
        "sources": [
            "https://www.nature.com/articles/s41591-024-03141-0",
            "https://arxiv.org/abs/2408.00738",
            "https://huggingface.co/paige-ai/Virchow",
            "https://huggingface.co/paige-ai/Virchow2",
            "https://www.paige.ai/foundation-models",
        ],
        "noncommercial": True,
        "audit_state": "verified_with_limits",
        "audit_priority": "P2",
        "audit_note": (
            "Promoted from the under-review register on 2026-08-13 with member-specific terms encoded: Virchow "
            "Apache-2.0 (auto-gated), Virchow2 CC BY-NC-ND-4.0 (auto-gated, non-commercial), Virchow2G and "
            "Virchow2G-Mini commercial licence only with no public artifact and no verified paper. Record-level "
            "noncommercial is therefore true. Evidence: evidence/hold-review-2026-08-13/fm_hold_review_3.json."
        ),
    },
    "bfm-h-optimus-0-h-optimus-1": {
        "description": (
            "Bioptimus 1.1B-parameter ViT pathology foundation models trained by self-supervised learning on "
            "hundreds of millions of tiles from 500k+ (H-optimus-0) to 1M+ (H-optimus-1) H&E slides; neither model "
            "has a peer-reviewed paper or preprint."
        ),
        "status": (
            "Member-specific terms: H-optimus-0 is Apache-2.0 behind an automatic gate, H-optimus-1 is "
            "CC BY-NC-ND-4.0 behind manual approval with an institutional email"
        ),
        "paper_links": links([
            ("Company announcement", "https://www.bioptimus.com/news/bioptimus-launches-h-optimus-1"),
        ]),
        "code_links": links([
            ("Hugging Face (H-optimus-0)", "https://huggingface.co/bioptimus/H-optimus-0"),
            ("Hugging Face (H-optimus-1)", "https://huggingface.co/bioptimus/H-optimus-1"),
            ("Official release page", "https://github.com/bioptimus/releases/tree/main/models/h-optimus/v0"),
        ]),
        "sources": [
            "https://www.bioptimus.com/news/bioptimus-launches-h-optimus-1",
            "https://huggingface.co/bioptimus/H-optimus-0",
            "https://huggingface.co/bioptimus/H-optimus-1",
            "https://github.com/bioptimus/releases/tree/main/models/h-optimus/v0",
        ],
        "noncommercial": True,
        "audit_state": "verified_with_limits",
        "audit_priority": "P2",
        "audit_note": (
            "Promoted from the under-review register on 2026-08-13 with both model cards verified and per-member "
            "terms encoded: H-optimus-0 Apache-2.0 (auto-gated), H-optimus-1 CC BY-NC-ND-4.0 (manually gated). The "
            "listed paper is a company announcement and is labelled as such; no DOI exists. Evidence: "
            "evidence/hold-review-2026-08-13/fm_hold_review_3.json."
        ),
    },
}


def hold_record(
    record_id: str,
    modality: str,
    name: str,
    description: str,
    io: str,
    status: str,
    use_cases: str,
    year: str,
    papers: list[tuple[str, str]],
    codes: list[tuple[str, str]],
    *,
    audit_note: str,
    noncommercial: bool = False,
    aliases: list[str] | None = None,
    extra_sources: list[str] | None = None,
) -> dict:
    item = record(
        record_id, modality, name, description, io, status, use_cases, year, papers, codes,
        audit_note=audit_note, noncommercial=noncommercial, aliases=aliases,
        audit_state="hold", audit_priority="P2", extra_sources=extra_sources,
    )
    return item


REGISTER_ADDITIONS: list[dict] = [
    {
        "record": hold_record(
            "bfm-jump-lite", "benchmark", "JUMP-lite (with Nahual)",
            "Compact benchmark subset of the JUMP Cell Painting resource for reproducible evaluation of cell-image representations.",
            "Cell Painting images and precomputed embeddings + benchmark tasks -> cell-representation benchmark results",
            "HOLD — MIT harness code and a Zenodo code archive exist, but the benchmark image, embedding and metadata bundle is not yet retrievable from the Cell Painting Gallery",
            "Benchmarking cell-image representation models",
            "2026",
            [("arXiv", "https://arxiv.org/abs/2608.07632")],
            [
                ("GitHub", "https://github.com/afermg/JUMP_lite"),
                ("Zenodo code archive", "https://zenodo.org/records/21779243"),
            ],
            audit_note=(
                "Held on 2026-08-13: paper and MIT code verified, but an unsigned listing of the Cell Painting "
                "Gallery prefixes returns no objects, so the benchmark data cannot be downloaded. Evidence: "
                "evidence/additions-2026-08-13/fm_result_1.json."
            ),
        ),
        "review": {
            "status": "under_review",
            "hold_since": DATE,
            "reason_code": "multiple",
            "reason": (
                "Paper (arXiv 2608.07632) and MIT code verified, but the benchmark artifact is not retrievable: the "
                "README states the release is deposited for publication in the Cell Painting Gallery and the public "
                "paths become available only after gallery promotion, and unsigned S3 listings of the cited prefixes "
                "return no objects. The data licence is deferred to Cell Painting Gallery / JUMP terms rather than "
                "stated. Scope note: JUMP-lite/Nahual is benchmark and deployment infrastructure, not a pretrained "
                "model. Evidence: evidence/additions-2026-08-13/fm_result_1.json."
            ),
            "source": AUDIT_SOURCE,
            "reconsider_when": (
                "An unsigned listing of the Cell Painting Gallery publication_data / images prefixes for the "
                "JUMP-lite release returns objects, i.e. the metadata bundle, embeddings and image stores are "
                "actually downloadable; re-verify the data licence at that point."
            ),
        },
    },
    {
        "record": hold_record(
            "bfm-aqaffinity", "complex", "AQAffinity",
            "SandboxAQ binding-affinity model that predicts protein-ligand affinity directly from sequence and ligand structure, implemented as an affinity module on an open co-folding backbone.",
            "Protein sequence + ligand SMILES, with no precomputed structure -> predicted binding affinity",
            "HOLD — Apache-2.0 weights, inference and training code are published behind an auto-approved contact form, but no primary paper exists and the model is a single-capability affinity head",
            "Binding-affinity prediction and hit triage",
            "2026",
            [],
            [("Hugging Face", "https://huggingface.co/SandboxAQ/AQAffinity")],
            audit_note=(
                "Held on 2026-08-13: artifact, ownership and Apache-2.0 terms verified, but no paper or preprint "
                "exists and scope is narrower than a reusable backbone. Evidence: "
                "evidence/additions-2026-08-13/fm_result_2.json."
            ),
        ),
        "review": {
            "status": "under_review",
            "hold_since": DATE,
            "reason_code": "multiple",
            "reason": (
                "Artifact fully verified on the official SandboxAQ model hub (weights, inference and training code, "
                "Apache-2.0, auto-approved contact gate), but two gates fail: no paper or preprint exists anywhere "
                "(the only primary source is a first-party vendor release post, and the card cites another team's "
                "preprint), and the model is a single-purpose affinity head on another backbone rather than a "
                "pretrained model reusable across tasks. Also outside the refresh window. Evidence: "
                "evidence/additions-2026-08-13/fm_result_2.json."
            ),
            "source": AUDIT_SOURCE,
            "reconsider_when": (
                "A primary paper or preprint for AQAffinity appears, or the index adopts a written rule that a "
                "first-party vendor release post counts as the primary source and that single-capability heads built "
                "on another backbone are in scope. No artifact re-verification is needed at that point."
            ),
        },
    },
    {
        "record": hold_record(
            "bfm-planthelixseek", "dna", "PlantHelixSeek",
            "Plant DNA language model released with a base checkpoint and downstream task heads for regulatory-element and annotation tasks.",
            "Plant DNA sequence -> embeddings and downstream task predictions",
            "HOLD — public MIT code and ungated CC BY-NC 4.0 weights, but no paper, preprint or technical report exists",
            "Plant regulatory-element prediction, genome annotation, representation transfer",
            "2026",
            [],
            [
                ("Hugging Face", "https://huggingface.co/zhangtaolab/PlantHelixSeek"),
                ("GitHub", "https://github.com/zhangtaolab/PlantHelixSeek"),
            ],
            noncommercial=True,
            audit_note=(
                "Held on 2026-08-13: artifacts and lab provenance verified, but there is no primary document; the "
                "repository's citation block is self-referential. Evidence: "
                "evidence/additions-2026-08-13/fm_result_3.json."
            ),
        ),
        "review": {
            "status": "under_review",
            "hold_since": DATE,
            "reason_code": "scope",
            "reason": (
                "Model and provenance are real - an established plant-DNA-model lab, a base checkpoint plus "
                "downstream heads on the hub, MIT code and CC BY-NC 4.0 weights - but no primary paper, preprint or "
                "technical report exists and literature searches return no hits, so catalog eligibility is "
                "unresolved. Weights are non-commercial, and uptake is unproven. Evidence: "
                "evidence/additions-2026-08-13/fm_result_3.json."
            ),
            "source": AUDIT_SOURCE,
            "reconsider_when": (
                "A primary document appears - a preprint, journal article, or dated technical report for "
                "PlantHelixSeek or its architecture. Accept then with modality dna, noncommercial true, and a status "
                "naming the CC BY-NC 4.0 weights and MIT code."
            ),
        },
    },
    {
        "record": hold_record(
            "bfm-seqlens-v2", "dna", "SeqLens v2 (with mgxLens v2)",
            "Announced second generation of the seqLens genomic language model family, with only the smallest variant public and a companion metagenomic profiler bundle.",
            "DNA or metagenomic sequence -> embeddings and downstream predictions",
            "HOLD — v2 provenance is unverified, only the smallest variant is released, and the companion profiler declares no licence",
            "Genomic representation learning, metagenomic profiling",
            "2026",
            [("seqLens v1 (Molecular Biology and Evolution)", "https://doi.org/10.1093/molbev/msag139")],
            [],
            audit_note=(
                "Held on 2026-08-13: no v2 primary document, unverified organisation provenance, partial release, "
                "and an unlicensed companion bundle. Evidence: evidence/additions-2026-08-13/fm_result_3.json."
            ),
        ),
        "review": {
            "status": "under_review",
            "hold_since": DATE,
            "reason_code": "multiple",
            "reason": (
                "Three conditions fail. No primary document for v2 exists - literature hits cover only the v1 work "
                "and the v2 card cites itself. Provenance is unverified: the publishing hub organisation is "
                "unaffiliated with the v1 authors, no public v2 code repository exists, and the card cites "
                "non-public internal files. The release is partial - only the smallest variant is public, with the "
                "larger family members marked in development or planned. The companion mgxLens v2 additionally "
                "fails scope and licence: it is a self-described proof-of-concept retrieval profiler with no licence "
                "declared. Evidence: evidence/additions-2026-08-13/fm_result_3.json."
            ),
            "source": AUDIT_SOURCE,
            "reconsider_when": (
                "Positive evidence of ownership appears - the v1 authors publicly claiming the publishing "
                "organisation, a public v2 code repository, or a v2 paper naming authors - and the larger family "
                "members actually ship. Reassess mgxLens separately only if it is relicensed and re-scoped as a "
                "reusable model."
            ),
        },
    },
    {
        "record": hold_record(
            "bfm-screenshot", "singlecell", "ScreenShot",
            "In-context model for few-shot combination drug screening, pretrained on 40 screening datasets covering about 3,700 drugs and 6,000 samples, that predicts responses from functional dose-response measurements without fine-tuning.",
            "Observed combination dose-response measurements -> predicted responses for unseen combinations",
            "HOLD — checkpoints are present in the public repository but no licence exists anywhere, so reuse rights are unresolved and scope placement needs a curator ruling",
            "Combination drug-screening prediction, few-shot perturbation-response modelling",
            "2026",
            [("arXiv", "https://arxiv.org/abs/2608.12219")],
            [("GitHub", "https://github.com/tansey-lab/screenshot")],
            noncommercial=True,
            audit_note=(
                "Held on 2026-08-13: paper and artifacts verified, but the repository has no licence file and the "
                "released checkpoints are per-held-out-cohort evaluation artifacts. Evidence: "
                "evidence/additions-2026-08-13/fm_result_5.json."
            ),
        ),
        "review": {
            "status": "under_review",
            "hold_since": DATE,
            "reason_code": "multiple",
            "reason": (
                "Paper (arXiv 2608.12219) and artifacts check out - the official lab repository ships model "
                "checkpoints and drug libraries - but no licence exists in any form, so the default is "
                "all-rights-reserved and no honest reuse phrase can be written. Scope also needs a curator call: the "
                "model is pretrained and reusable by in-context learning, but it consumes functional dose-response "
                "measurements rather than molecular representations, and the released checkpoints are "
                "leave-one-cohort-out evaluation artifacts rather than one canonical model. If admitted it belongs "
                "in the perturbation-response slot (singlecell), not molecule. Evidence: "
                "evidence/additions-2026-08-13/fm_result_5.json."
            ),
            "source": AUDIT_SOURCE,
            "reconsider_when": (
                "A LICENSE file appears in the official repository, or the paper states explicit terms for the "
                "released weights, and the curator rules on whether functional-screening perturbation-response "
                "models belong in the index."
            ),
        },
    },
    {
        "record": hold_record(
            "bfm-spgen", "spatial", "SPgen",
            "Framework that predicts proteome-wide spatial protein abundance by combining frozen third-party sequence, expression and text encoders with a graph network trained per dataset.",
            "Spatial transcriptomics with protein-sequence and text embeddings -> predicted spatial protein expression",
            "HOLD — the official repository has no licence and ships no pretrained weights; the pretrained content is entirely third-party frozen encoders",
            "Spatial proteomics prediction",
            "2026",
            [("bioRxiv", "https://doi.org/10.64898/2026.07.16.739037")],
            [("GitHub", "https://github.com/lijc0804/SPgen")],
            noncommercial=True,
            audit_note=(
                "Held on 2026-08-13: preprint and repository identity verified, but no licence, no released "
                "checkpoint, and narrow single-task scope. Evidence: "
                "evidence/additions-2026-08-13/fm_result_7.json."
            ),
        ),
        "review": {
            "status": "under_review",
            "hold_since": DATE,
            "reason_code": "multiple",
            "reason": (
                "Preprint and official repository verified and linked by the paper's code-availability statement, "
                "but three independent blockers remain: no licence file exists, so redistribution terms default to "
                "all-rights-reserved; the repository contains scripts and notebooks only, with no checkpoint files "
                "or weight-download instructions; and the pretrained content is third-party frozen encoders wrapped "
                "by a graph network trained per dataset, i.e. one task rather than reusable pretrained scope. "
                "Evidence: evidence/additions-2026-08-13/fm_result_7.json."
            ),
            "source": AUDIT_SOURCE,
            "reconsider_when": (
                "The repository adds an explicit licence and ships downloadable SPgen checkpoints, or an "
                "author-controlled model-hub or Zenodo artifact appears, or a peer-reviewed version documents "
                "released weights. Re-verify licence wording at that point."
            ),
        },
    },
    {
        "record": hold_record(
            "bfm-omicslm", "multimodal", "OmicsLM",
            "Multimodal large language model that embeds continuous expression profiles in the language-model context for multi-sample omics reasoning, trained on more than 5.5 million instruction examples across 70+ task types.",
            "Expression profiles + natural-language question -> omics reasoning, analysis and answers",
            "HOLD — paper only; no official code, weights or endpoint could be located",
            "Multi-sample omics reasoning, expression-aware question answering",
            "2026",
            [("arXiv", "https://arxiv.org/abs/2605.06728")],
            [],
            audit_note=(
                "Held on 2026-08-13: the primary source is verified, but hub and repository searches return no "
                "official artifact. Evidence: evidence/additions-2026-08-13/fm_result_7.json."
            ),
        ),
        "review": {
            "status": "under_review",
            "hold_since": DATE,
            "reason_code": "artifact",
            "reason": (
                "Primary source verified (arXiv 2605.06728, not withdrawn) and the abstract matches the described "
                "capability, but no official artifact could be found anywhere: the abstract page states no code or "
                "weights availability, a model-hub search returns nothing, and a repository search returns no "
                "matching project. Paper-only entries with no reusable artifact do not meet the artifact criterion. "
                "Evidence: evidence/additions-2026-08-13/fm_result_7.json."
            ),
            "source": AUDIT_SOURCE,
            "reconsider_when": (
                "An official repository or model card appears under the authors' organisation, or a revised version "
                "of the paper adds a code-availability link; then verify weights licence and gating before "
                "accepting, and record whether the release is weights or inference-only."
            ),
        },
    },
    {
        "record": hold_record(
            "bfm-x-cell", "singlecell", "X-Cell / X-Cell-Ultra",
            "Xaira Therapeutics diffusion language model for causal perturbation prediction across diverse cellular contexts, announced with a small public variant and a much larger internal one.",
            "Cell context + perturbation -> predicted post-perturbation expression",
            "HOLD — the official repositories are public and CC BY-NC-SA-4.0, but both carry a 'weights and inference code coming soon' banner and contain no model files",
            "Perturbation-response prediction, in silico genetic screens",
            "2026",
            [("bioRxiv", "https://doi.org/10.64898/2026.03.18.712807")],
            [
                ("Hugging Face", "https://huggingface.co/Xaira-Therapeutics/X-Cell"),
                ("GitHub", "https://github.com/Xaira-Therapeutics/x-cell"),
            ],
            noncommercial=True,
            aliases=["X-Cell", "X-Cell-Ultra"],
            audit_note=(
                "Held on 2026-08-13: paper, ownership, scope and terms verified, but no weights exist yet. "
                "Evidence: evidence/additions-2026-08-13/fm_result_10.json."
            ),
        ),
        "review": {
            "status": "under_review",
            "hold_since": DATE,
            "reason_code": "artifact",
            "reason": (
                "Paper verifies (bioRxiv 10.64898/2026.03.18.712807, posted 2026-03-20, not withdrawn) and ownership, "
                "modality and CC BY-NC-SA-4.0 terms are clear, but the reusable-artifact rule fails: the model "
                "repository lists no model file and both the model card and the code repository carry the identical "
                "banner stating that weights and inference code are coming soon. Evidence: "
                "evidence/additions-2026-08-13/fm_result_10.json."
            ),
            "source": AUDIT_SOURCE,
            "reconsider_when": (
                "The model repository lists an actual weight file, or the inference package ships and the "
                "coming-soon banner is removed; then re-check whether X-Cell-Ultra is released separately or stays "
                "internal and record it under its own terms."
            ),
        },
    },
    {
        "record": hold_record(
            "bfm-scmamba-snrna", "singlecell", "scMamba (snRNA-seq, neurodegeneration)",
            "Bidirectional Mamba model pretrained on single-nucleus RNA-seq from postmortem brain tissue for neurodegeneration analysis; a different model from the multi-omics-integration scMamba.",
            "Single-nucleus RNA-seq expression -> cell embeddings, annotations and imputed profiles",
            "HOLD — Apache-2.0 code is public, but the pretrained checkpoint is available only by email request",
            "Cell-type annotation, doublet detection, imputation, differential-expression analysis",
            "2025",
            [("arXiv", "https://arxiv.org/abs/2502.19429")],
            [("GitHub", "https://github.com/okt0711/scMamba")],
            audit_note=(
                "Held on 2026-08-13 on the reusable-artifact rule; recorded separately from the multi-omics "
                "scMamba so the two are never merged. Evidence: evidence/additions-2026-08-13/fm_result_10.json."
            ),
        ),
        "review": {
            "status": "under_review",
            "hold_since": DATE,
            "reason_code": "artifact",
            "reason": (
                "One half of a name collision, recorded so the two models are never merged. arXiv 2502.19429 is a "
                "genuinely different model from arXiv 2506.20697: different authors, data (postmortem-brain "
                "snRNA-seq), tasks and architecture lineage. The official repository names the same paper and "
                "authors, so ownership is clear, but there are no public weights - the checkpoint section is a "
                "request-by-email gate. Held on the reusable-artifact rule, not on scope or identity. Evidence: "
                "evidence/additions-2026-08-13/fm_result_10.json."
            ),
            "source": AUDIT_SOURCE,
            "reconsider_when": (
                "The pretrained checkpoint is published at a public locator with readable terms instead of the "
                "email-request gate. Any catalog entry must keep a disambiguated name, because arXiv 2506.20697 "
                "scMamba is a different model."
            ),
        },
    },
    {
        "record": hold_record(
            "bfm-scmamba-multiomics", "singlecell", "scMamba (multi-omics integration)",
            "State-space-duality model for single-cell multi-omics integration that tokenizes genomic regions instead of selecting highly variable features; a different model from the snRNA-seq scMamba.",
            "Paired single-cell multi-omics profiles -> aligned joint cell embeddings",
            "HOLD — the AGPL-3.0 repository is stale and states that code follows manuscript acceptance; checkpoints are offered only through a share whose contents could not be verified",
            "Single-cell multi-omics integration, clustering, cell-type annotation, trajectory inference",
            "2025",
            [("arXiv", "https://arxiv.org/abs/2506.20697")],
            [("GitHub", "https://github.com/23AIBox/scMamba")],
            audit_note=(
                "Held on 2026-08-13: two verification lanes disagreed on the artifact, neither could enumerate the "
                "checkpoint files, and the conservative reading prevails. Evidence: "
                "evidence/additions-2026-08-13/fm_result_10.json and fm_result_11.json."
            ),
        ),
        "review": {
            "status": "under_review",
            "hold_since": DATE,
            "reason_code": "artifact",
            "reason": (
                "Paper verified (arXiv 2506.20697, not withdrawn), but the artifact does not clear the bar. Two "
                "independent lanes reviewed it and disagreed: one read the repository as documenting inference from "
                "pretrained checkpoints, the other found the repository stale since before the paper was posted and "
                "its README stating that all code will be public following acceptance. Neither lane could enumerate "
                "the checkpoint files, which are offered only through a share page that does not render a file "
                "listing, so the conservative reading applies. A second, unrelated scMamba (arXiv 2502.19429) is "
                "held separately, so any future entry needs explicit disambiguation. Evidence: "
                "evidence/additions-2026-08-13/fm_result_10.json and fm_result_11.json."
            ),
            "source": AUDIT_SOURCE,
            "reconsider_when": (
                "The manuscript is accepted or published and the full code plus checkpoints are formally released at "
                "a verifiable locator (model hub, Zenodo, or a populated repository release) with the paper pointing "
                "at the repository; then add with disambiguation against the snRNA-seq scMamba."
            ),
        },
    },
]


# Re-review outcomes for register entries that stay held. Each appends one dated
# sentence, guarded by REREVIEW_MARK so a second run changes nothing.
REGISTER_REREVIEW: dict[str, str] = {
    "bfm-atlas-rudolfv-successor": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_3.json): the listed Hugging Face "
        "artifact is still absent; the official product page now presents a three-generation line ending in Atlas 2 "
        "(arXiv 2601.05148, January 2026) with commercial licensing only and no public weight download; and a gated "
        "RudolfV-2 family has appeared on the vendor's model-hub organisation whose licence text is unreadable "
        "without authentication. The RudolfV-2 family is a separate candidate, not evidence for Atlas."
    ),
    "bfm-tabula": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_3.json and "
        "evidence/additions-2026-08-13/fm_result_10.json): the repository is alive but still ships training code "
        "only, with no weights and no releases, and no model-hub artifact exists under the authors. A rediscovered "
        "candidate was matched to this entry rather than added: the work now also appears as arXiv 2607.19400 under "
        "a new title, with a federated-orchestration companion platform, which explains the title mismatch between "
        "the repository README and the cited preprint. The custom non-commercial repository licence corroborates the "
        "existing noncommercial flag but supplies no weights."
    ),
    "bfm-deepsea": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_1.json): the original standalone "
        "DeepSEA artifact has been located at deepsea.princeton.edu/help/, distinct from the Selene framework this "
        "record links, and the page states no licence for that download. The remaining blocker is the missing "
        "written historical-exception policy, which no external evidence can satisfy; if that policy is adopted, "
        "replace the Selene link with the located artifact and record the absent licence."
    ),
    "bfm-mrna-fm-plantrna-fm": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_1.json): the split is now evidenced "
        "but not executed. PlantRNA-FM is fully documented as an individual member - MIT licence, ungated "
        "downloadable weights, its own primary paper - and would be promotable standalone; mRNA-FM's weights are "
        "ungated under AGPL-3.0, but its card links only the family preprint, so its own primary evidence is "
        "missing. The two members carry conflicting licences, so the combined record cannot be promoted as-is."
    ),
    "bfm-hybridna": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_4.json): the official project page's "
        "code link now points to a repository that returns not-found, so the only official artifact locator is dead, "
        "while three Apache-2.0, ungated weight repositories have appeared on a personal model-hub account whose "
        "display name matches the first author but whose organisations do not match the paper's institution. The "
        "paper-to-weights link is uploader-asserted rather than officially published, so provenance is unconfirmed."
    ),
    "bfm-genemamba": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_4.json): a parallel discovery lane "
        "proposed this model as a new addition on the strength of an Apache-2.0 header in the weights repository; "
        "reading the licence file itself shows the body is not the verbatim Apache-2.0 text (an altered patent-grant "
        "clause and a modified derivative-works definition), while the official code repository carries no licence "
        "at all. The catalog must not display this as Apache-2.0 until the authors resolve the discrepancy, so the "
        "hold stands and no new record was created."
    ),
    "bfm-bioreason": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_3.json): the promised checkpoints "
        "are still unreleased - the README's checkpoint section reads that they will be released soon, while the "
        "abstract in the same file continues to claim public checkpoints - and no model-hub artifact exists. The "
        "successor BioReason-Pro has been released separately and is already a displayed record; it is a different "
        "model and does not lift this hold."
    ),
    "bfm-openprotein-ai-poet-poet-2": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_3.json): the PoET-2 repository is "
        "real and self-hosting, with Apache-2.0 code and a non-commercial model-weights licence, which confirms the "
        "recorded non-commercial flag for the model side. The condition remains a register-side editorial act: this "
        "record must be narrowed to the commercial platform or merged with the displayed PoET-2 record, with the "
        "stable-ID disposition documented. No separate held PoET-2 record exists, so the duplicate target lives in "
        "the displayed catalog."
    ),
    "bfm-sctranslator": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_3.json): the journal publication and "
        "the recorded year were confirmed from the registration record, and the checkpoints remain real but "
        "term-free - three model sizes behind personal cloud-drive links, with no licence file and no SPDX licence "
        "on the repository. Both halves of the condition, scope eligibility and explicit reuse terms, stay open."
    ),
    "bfm-drfold": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_2.json): the successor repository "
        "does ship reusable artifacts - its install script downloads about 1.3 GB of model weights under MIT-form "
        "terms - but the weight locator is indirect and both remaining paths are curatorial: no written "
        "structural-model exception exists, and the record still frames the entry as one-task RNA structure "
        "prediction rather than around the pretrained language-model component."
    ),
    "bfm-next-mol": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_4.json): the artifacts were located "
        "and are downloadable - a pretrained molecular language model on the model hub and conformer checkpoints on "
        "an open repository - but none of the three official locations declares a licence, the repository offers a "
        "citation request rather than terms, and it still warns that open sourcing is in progress."
    ),
    "bfm-lingshu-cell": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_4.json): the official collection "
        "still contains only the paper and no model, and the official project page links no code, weights or "
        "endpoint. An unaffiliated third-party repository carrying checkpoint files has appeared; its provenance is "
        "not established and it must not be treated as the official artifact."
    ),
    "bfm-plip-pathology-language-image-pretraining": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_4.json): neither official artifact "
        "grants reuse rights - the code repository has no licence file and the weights repository has empty card "
        "metadata. The only use-terms text is inherited from the upstream CLIP card and states that any deployed use "
        "case, commercial or not, is out of scope; if this entry is ever promoted, the terms field must reproduce "
        "that wording rather than imply an open licence, and the record's noncommercial flag must be revisited."
    ),
    "bfm-pearl": (
        "Re-reviewed 2026-08-13 (evidence/hold-review-2026-08-13/fm_hold_review_3.json): paper identity was "
        "confirmed, but no artifact or terms exist to verify - the vendor's research page describes the model "
        "without stating access, weights, API or licensing, dedicated product paths return not-found, and the public "
        "inference catalogue lists no matching entry. A vendor endpoint path returns HTTP 200 for arbitrary paths, "
        "so it is worthless as evidence; a public endpoint remains unverified rather than confirmed absent."
    ),
}


def apply_catalog(records: list[dict]) -> tuple[int, int]:
    by_id = {item["id"]: item for item in records}
    if len(by_id) != len(records):
        raise SystemExit("duplicate IDs exist before migration")

    add_count = 0
    replace_count = 0
    for item in NEW_RECORDS:
        record_id = item["id"]
        if record_id in by_id:
            by_id[record_id].clear()
            by_id[record_id].update(item)
            replace_count += 1
        else:
            records.append(item)
            by_id[record_id] = item
            add_count += 1

    missing = sorted(set(CATALOG_UPDATES) - set(by_id))
    if missing:
        raise SystemExit(f"catalog update targets missing: {missing}")
    for record_id, patch in CATALOG_UPDATES.items():
        by_id[record_id].update(patch)

    scmulan = by_id["bfm-scmulan"]
    scmulan["code_links"] = [
        link for link in scmulan["code_links"] if link["url"] != SCMULAN_DEAD_LINK
    ]
    scmulan["sources"] = [url for url in scmulan["sources"] if url != SCMULAN_DEAD_LINK]

    return add_count, replace_count


def apply_promotions(records: list[dict], register: dict) -> int:
    by_id = {item["id"]: item for item in records}
    entries_by_id = {entry["record"]["id"]: entry for entry in register["entries"]}
    promoted = 0

    for record_id, patch in PROMOTIONS.items():
        if record_id in entries_by_id:
            entry = entries_by_id.pop(record_id)
            promoted_record = entry["record"]
            register["entries"] = [
                item for item in register["entries"] if item["record"]["id"] != record_id
            ]
        elif record_id in by_id:
            promoted_record = by_id[record_id]
        else:
            raise SystemExit(f"promotion target missing from both stores: {record_id}")

        promoted_record.update(patch)
        promoted_record["date_modified"] = DATE
        promoted_record["verified"] = DATE
        if record_id not in by_id:
            records.append(promoted_record)
            by_id[record_id] = promoted_record
            promoted += 1

    return promoted


def apply_register(register: dict) -> tuple[int, int]:
    entries = register["entries"]
    by_id = {entry["record"]["id"]: entry for entry in entries}

    added_entries = 0
    for entry in REGISTER_ADDITIONS:
        record_id = entry["record"]["id"]
        if record_id in by_id:
            existing = by_id[record_id]
            existing["record"].clear()
            existing["record"].update(entry["record"])
            existing["review"].clear()
            existing["review"].update(entry["review"])
        else:
            entries.append(entry)
            by_id[record_id] = entry
            added_entries += 1

    updated = 0
    for record_id, sentence in REGISTER_REREVIEW.items():
        entry = by_id.get(record_id)
        if entry is None:
            raise SystemExit(f"re-review target missing from register: {record_id}")
        if REREVIEW_MARK not in entry["review"]["reason"]:
            entry["review"]["reason"] = f"{entry['review']['reason']} {sentence}"
            updated += 1
        if REREVIEW_MARK not in entry["record"]["audit_note"]:
            entry["record"]["audit_note"] = f"{entry['record']['audit_note']} {sentence}"
        entry["record"]["date_modified"] = DATE

    # The Atlas entry's own facts changed, so its record is edited too.
    atlas = by_id["bfm-atlas-rudolfv-successor"]["record"]
    atlas["description"] = (
        "Aignostics/Mayo Clinic/Charite pathology foundation model (ViT-H/14, 632M params) built on the RudolfV "
        "pathologists-in-the-loop approach, trained on 1.2M WSIs across 70+ tissue and 100+ stain types; the "
        "product line has since advanced to Atlas 2 (arXiv 2601.05148, January 2026)."
    )
    atlas["status"] = (
        "HOLD — no public Atlas or Atlas 2 weight artifact; commercial licensing only, and the previously listed "
        "model-hub entry is absent"
    )
    atlas["paper_links"] = links([
        ("arXiv (Atlas)", "https://arxiv.org/abs/2501.05409"),
        ("arXiv (Atlas 2)", "https://arxiv.org/abs/2601.05148"),
    ])
    atlas["code_links"] = links([
        ("Official model page", "https://www.aignostics.com/products/foundation-models"),
    ])
    atlas["sources"] = [
        "https://arxiv.org/abs/2501.05409",
        "https://arxiv.org/abs/2601.05148",
        "https://www.aignostics.com/products/foundation-models",
        "https://www.aignostics.com/blog/atlas-2-setting-a-new-standard-for-pathology-foundation-models",
    ]

    # Tabula's identity chain now also runs through a renamed preprint version.
    tabula = by_id["bfm-tabula"]["record"]
    tabula_paper = "https://arxiv.org/abs/2607.19400"
    if all(link["url"] != tabula_paper for link in tabula["paper_links"]):
        tabula["paper_links"].append({"label": "arXiv (2026 version)", "url": tabula_paper})
    if tabula_paper not in tabula["sources"]:
        tabula["sources"].append(tabula_paper)

    # Every remaining register candidate was re-checked against primary sources today.
    for entry in entries:
        entry["record"]["verified"] = DATE

    register["date_modified"] = DATE
    register["record_count"] = len(entries)
    return added_entries, updated


def apply_metadata(records: list[dict], register: dict) -> None:
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    displayed = len(records)
    held = len(register["entries"])
    verified = sum(1 for item in records if item["audit_state"] == "verified")
    with_limits = sum(1 for item in records if item["audit_state"] == "verified_with_limits")

    metadata["resource_version"] = RESOURCE_VERSION
    metadata["modified"] = DATE
    metadata["baseline_commit"] = BASELINE_COMMIT
    metadata["baseline_commit_url"] = BASELINE_COMMIT_URL
    metadata["release_ref"] = None
    metadata["baseline_data_date"] = DATE
    metadata["provenance"] = (
        "Curated from primary papers, official repositories, model hubs, project pages, and explicit licence or "
        "access terms. The 2026-07-13 review covered 377 source-audited candidates. The 2026-08-13 refresh ran "
        "delegated discovery across all ten modalities, verified every candidate against primary sources, and "
        "re-reviewed all 32 under-review records, promoting three of them. The "
        f"{displayed} records meeting the release policy form the canonical displayed catalog; {held} unresolved "
        "candidates are preserved losslessly in a separate under-review register. Generated distributions come "
        "from the canonical JSON through a deterministic build."
    )
    metadata["evidence_statement"] = (
        f"Every displayed record carries an evidence-verification date. The displayed catalog contains {displayed} "
        f"records: {verified} verified and {with_limits} verified with visible limitations. The 2026-08-13 refresh "
        "verified new records and promotions from primary papers, official repositories, model hubs, and exact "
        f"licence wording, and re-checked every held candidate. {held} unresolved candidates are excluded from the "
        "index and preserved with stable IDs, evidence, reasons, and reconsideration conditions in the repository's "
        "under-review register."
    )
    METADATA.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    records = json.loads(DATA.read_text(encoding="utf-8"))
    register = json.loads(REGISTER.read_text(encoding="utf-8"))

    add_count, replace_count = apply_catalog(records)
    promoted = apply_promotions(records, register)
    register_added, register_updated = apply_register(register)

    ids = [item["id"] for item in records]
    if len(set(ids)) != len(ids):
        raise SystemExit("duplicate IDs after migration")
    names = [item["name"].casefold().strip() for item in records]
    if len(set(names)) != len(names):
        raise SystemExit("exact duplicate display names after migration")
    held_ids = {entry["record"]["id"] for entry in register["entries"]}
    overlap = sorted(held_ids & set(ids))
    if overlap:
        raise SystemExit(f"records appear in both stores: {overlap}")

    DATA.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REGISTER.write_text(json.dumps(register, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    apply_metadata(records, register)

    print(
        f"added={add_count} replaced={replace_count} promoted={promoted} "
        f"register_added={register_added} register_rereviewed={register_updated} "
        f"displayed={len(records)} held={len(register['entries'])}"
    )


if __name__ == "__main__":
    main()
