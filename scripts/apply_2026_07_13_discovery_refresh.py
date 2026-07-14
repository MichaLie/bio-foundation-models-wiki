#!/usr/bin/env python3
"""Apply the separately discovered and adversarially cross-checked 2026-07-13 refresh.

This is a dated, idempotent migration for the protected FAIR preview. It never
publishes. Rejected and held candidates are documented in the companion audit
note rather than silently entering the catalog.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "models_final.json"
DATE = "2026-07-13"


def links(items: list[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"label": label, "url": url} for label, url in items]


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
    noncommercial: bool = False,
    aliases: list[str] | None = None,
) -> dict:
    item = {
        "id": record_id,
        "date_added": DATE,
        "verified": DATE,
        "modality": modality,
        "name": name,
        "description": description,
        "io": io,
        "status": status,
        "use_cases": use_cases,
        "year": year,
        "paper_links": links(papers),
        "code_links": links(codes),
        "canonical": False,
        "noncommercial": noncommercial,
    }
    if aliases:
        item["aliases"] = aliases
    return item


UPDATES: dict[str, dict] = {
    "bfm-esm-c-esm-cambrian": {
        "description": "Biohub-maintained protein sequence encoder family for efficient representation learning; current releases include openly available ESMC checkpoints and provide the language-model backbone used by ESMFold2.",
        "status": "Open code + weights (MIT); local and Biohub Platform inference",
        "paper_links": links([
            ("bioRxiv (ESMC / ESMFold2)", "https://www.biorxiv.org/content/10.64898/2026.06.03.729735v1"),
        ]),
        "code_links": links([
            ("GitHub", "https://github.com/Biohub/esm"),
            ("Hugging Face", "https://huggingface.co/biohub"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "bfm-rfdiffusion": {
        "name": "RFdiffusion / RFdiffusion3 (RFD3)",
        "aliases": ["RFdiffusion", "RFdiffusion3", "RFD3"],
        "description": "Protein-backbone and all-atom diffusion family for functional design; RFD3 extends the family to proteins in the context of ligands, nucleic acids, and other non-protein atoms.",
        "paper_links": links([
            ("Nature", "https://www.nature.com/articles/s41586-023-06415-8"),
            ("bioRxiv (RFD3 v2)", "https://www.biorxiv.org/content/10.1101/2025.09.18.676967v2"),
        ]),
        "code_links": links([
            ("RFdiffusion GitHub", "https://github.com/RosettaCommons/RFdiffusion"),
            ("RFD3 Foundry", "https://github.com/RosettaCommons/foundry/tree/production/models/rfd3"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "bfm-rosettafold-all-atom": {
        "name": "RoseTTAFold All-Atom / RoseTTAFold3 (RF3)",
        "aliases": ["RoseTTAFold All-Atom", "RoseTTAFold3", "RF3"],
        "description": "RoseTTAFold all-atom family for predicting arbitrary biomolecular assemblies; RF3 extends the family across proteins, RNA, DNA, ligands, ions, and covalent modifications.",
        "status": "Open code + checkpoints (BSD-3-Clause); RF3 inference API still stabilizing",
        "paper_links": links([
            ("Science", "https://www.science.org/doi/10.1126/science.adl2528"),
            ("bioRxiv (RF3 v2)", "https://www.biorxiv.org/content/10.1101/2025.08.14.670328v2"),
        ]),
        "code_links": links([
            ("Foundry", "https://github.com/RosettaCommons/foundry"),
            ("RF3 model", "https://github.com/RosettaCommons/foundry/tree/production/models/rf3"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "bfm-alphagenome": {
        "status": "Open research code + gated public weights under non-commercial terms; free non-commercial API",
        "noncommercial": True,
        "code_links": links([
            ("Research code", "https://github.com/google-deepmind/alphagenome_research"),
            ("Kaggle weights", "https://www.kaggle.com/models/google/alphagenome"),
            ("Model terms", "https://deepmind.google.com/science/alphagenome/model-terms"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "bfm-plantcaduceus-plantcad-plantcad2": {
        "description": "Plant genomic foundation-model family; PlantCAD2 expands the successor model to 65 angiosperm species and 8,192-base context for transferable plant-regulatory representations.",
        "status": "Open code + public weights; checkpoint reuse terms unresolved",
        "paper_links": links([
            ("bioRxiv (PlantCAD2 v3)", "https://www.biorxiv.org/content/10.1101/2025.08.27.672609v3.full"),
        ]),
        "code_links": links([
            ("GitHub", "https://github.com/plantcad/plantcad"),
            ("Hugging Face", "https://huggingface.co/collections/kuleshov-group/plantcad2-67e437e241a382671371a572"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "bfm-progen3": {
        "status": "Open code + weights through 3B (non-commercial); 46B remains API-only",
        "noncommercial": True,
        "paper_links": links([
            ("bioRxiv v2", "https://www.biorxiv.org/content/10.1101/2025.04.15.649055v2"),
        ]),
        "code_links": links([
            ("GitHub", "https://github.com/Profluent-AI/progen3"),
            ("Hugging Face", "https://huggingface.co/Profluent-Bio/progen3-3b"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "bfm-poet-2": {
        "status": "Open code + downloadable weights under a non-commercial model licence",
        "noncommercial": True,
        "code_links": links([
            ("GitHub", "https://github.com/OpenProteinAI/PoET-2"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "bfm-xtrimopglm": {
        "status": "Open code + public weights (non-commercial)",
        "noncommercial": True,
        "paper_links": links([
            ("arXiv", "https://arxiv.org/abs/2401.06199"),
        ]),
        "code_links": links([
            ("GitHub", "https://github.com/biomap-research/xTrimoPGLM"),
            ("Hugging Face", "https://huggingface.co/biomap-research/xtrimopglm-1b-mlm"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "bfm-chroma": {
        "status": "Open code; gated academic/non-profit weights under a restrictive parameters licence",
        "noncommercial": True,
        "code_links": links([
            ("GitHub", "https://github.com/generatebio/chroma"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "bfm-ablingua": {
        "status": "Open public Apache-2.0 checkpoint; larger family models not released",
        "code_links": links([
            ("Hugging Face", "https://huggingface.co/IDEA-AI4S/AbLingua"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "bfm-captain": {
        "status": "Public MIT code + public pretrained checkpoints/data; checkpoint terms not separately stated",
        "date_modified": DATE,
        "verified": DATE,
    },
    "bfm-czi-virtual-cells-platform": {
        "name": "Biohub AI-Supported Virtual Cells Platform",
        "aliases": ["CZI Virtual Cells Platform", "CZI Virtual Cell Models"],
        "description": "Biohub-operated platform for cell foundation models, datasets, benchmarking, model cards, and AI Workspace workflows.",
        "code_links": links([
            ("Model catalog", "https://virtualcellmodels.cziscience.com/models"),
            ("AI Workspace", "https://virtualcellmodels.cziscience.com/ai-workspace"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
}


NEW_RECORDS: list[dict] = [
    # Sequence, genomics, RNA and protein lane.
    record(
        "bfm-space", "dna", "SPACE",
        "Multi-species genomic-profile foundation model for transferable DNA representations and cross-species regulatory prediction.",
        "DNA sequence -> genomic profiles and transferable embeddings",
        "Public code + checkpoint; checkpoint reuse terms not separately stated",
        "Regulatory prediction, genomic representation learning, cross-species transfer", "2025",
        [("arXiv", "https://arxiv.org/abs/2506.01833")],
        [("GitHub", "https://github.com/ZhuJiwei111/SPACE"), ("Hugging Face", "https://huggingface.co/yangyz1230/space")],
    ),
    record(
        "bfm-bmfm-dna", "dna", "BMFM-DNA",
        "SNP-aware and reference 113M ModernBERT genomic model family for learning DNA representations with or without explicit variants.",
        "DNA sequence +/- variants -> genomic representations",
        "Public code + reference and SNP-aware checkpoints",
        "Variant-effect modeling, regulatory prediction, transferable genomic embeddings", "2025",
        [("arXiv", "https://arxiv.org/abs/2507.05265")],
        [("GitHub", "https://github.com/BiomedSciAI/biomed-multi-omic"), ("Reference model", "https://huggingface.co/ibm-research/biomed.dna.ref.modernbert.113m.v1"), ("SNP model", "https://huggingface.co/ibm-research/biomed.dna.snp.modernbert.113m.v1")],
    ),
    record(
        "bfm-omni-dna", "dna", "Omni-DNA",
        "Autoregressive 20M-to-1B genomic model family trained at multi-species scale for long-context DNA understanding, annotation, and generation.",
        "DNA sequence and optional textual context -> sequence likelihoods, annotations, or generated DNA",
        "Public code + weights",
        "Genomic sequence generation, annotation, long-context representation learning", "2025",
        [("arXiv", "https://arxiv.org/abs/2502.03499")],
        [("GitHub", "https://github.com/Zehui127/Omni-DNA"), ("Hugging Face", "https://huggingface.co/zehui127/Omni-DNA-1B")],
    ),
    record(
        "bfm-nucel", "dna", "NucEL",
        "Single-nucleotide ELECTRA-style genomic representation model designed to learn nucleotide- and sequence-level features.",
        "DNA sequence -> nucleotide and sequence representations",
        "Public source repository + checkpoint",
        "Genomic representation learning, sequence classification, regulatory transfer", "2026",
        [("AAAI", "https://ojs.aaai.org/index.php/AAAI/article/view/36982")],
        [("GitHub", "https://github.com/FreakingPotato/NucEL"), ("Hugging Face", "https://huggingface.co/FreakingPotato/NucEL")],
    ),
    record(
        "bfm-d3lm", "dna", "D3LM",
        "Discrete masked-diffusion DNA language model for genomic representations and mammalian-sequence generation.",
        "DNA sequence or masked sequence -> representations or generated/completed DNA",
        "Public checkpoints with custom model code; standalone training repository not confirmed",
        "DNA generation, sequence completion, genomic representation learning", "2026",
        [("arXiv", "https://arxiv.org/abs/2603.01780")],
        [("NT-initialized model", "https://huggingface.co/Hengchang-Liu/D3LM-from-nt"), ("Scratch model", "https://huggingface.co/Hengchang-Liu/D3LM-scratch")],
    ),
    record(
        "bfm-onegenome-rice", "dna", "OneGenome-Rice",
        "Rice genomic mixture-of-experts generative model trained across cultivated and wild genomes with context up to one megabase.",
        "Rice genomic sequence -> long-context representations or generated sequence",
        "Public code + weights",
        "Rice regulatory genomics, introgression analysis, breeding and sequence generation", "2026",
        [("bioRxiv", "https://doi.org/10.64898/2026.04.21.719822")],
        [("GitHub", "https://github.com/zhejianglab/OneGenome-Rice"), ("Hugging Face", "https://huggingface.co/ZhejiangLab/OneGenome-Rice")],
        aliases=["OGR"],
    ),
    record(
        "bfm-hydrarna", "rna", "HydraRNA",
        "Hybrid state-space and attention RNA language model trained on full-length coding and non-coding RNAs with long sequence support.",
        "RNA sequence -> embeddings, likelihoods, or downstream predictions",
        "Public code + downloadable checkpoints",
        "RNA representation learning, long-RNA analysis, coding and non-coding RNA transfer", "2025",
        [("Genome Biology", "https://doi.org/10.1186/s13059-025-03853-7")],
        [("GitHub", "https://github.com/GuipengLi/HydraRNA"), ("Weights", "https://drive.google.com/drive/folders/14ZXi_aANEEdPa_Sc2cQZtUa4dENPDTkz")],
    ),
    record(
        "bfm-structrfm", "rna", "structRFM",
        "Structure-guided RNA foundation model learning joint sequence, secondary-structure, and functional representations.",
        "RNA sequence and structure context -> transferable embeddings and predictions",
        "Public code + dataset + checkpoints",
        "RNA structure/function prediction, embeddings, downstream transfer", "2025",
        [("bioRxiv", "https://www.biorxiv.org/content/10.1101/2025.08.06.668731v1")],
        [("GitHub", "https://github.com/heqin-zhu/structRFM"), ("Hugging Face", "https://huggingface.co/heqin-zhu/structRFM"), ("Zenodo", "https://doi.org/10.5281/zenodo.16754363")],
    ),
    record(
        "bfm-codonfm-encodon", "rna", "CodonFM / EnCodon",
        "Codon-level foundation-model family trained across species for representations, sequence-property prediction, and codon-aware generation.",
        "Coding sequence at codon resolution -> embeddings, predictions, or optimized sequence",
        "Public code + checkpoints under NVIDIA model terms",
        "Expression and stability prediction, codon optimization, coding-sequence design", "2025",
        [("NVIDIA preprint", "https://research.nvidia.com/labs/dbr/assets/data/manuscripts/nv-codonfm-preprint.pdf")],
        [("GitHub", "https://github.com/NVIDIA-BioNeMo/CodonFM"), ("EnCodon weights", "https://huggingface.co/nvidia/NV-CodonFM-Encodon-80M-v1")],
        aliases=["CodonFM", "EnCodon"],
    ),
    record(
        "bfm-ankh3", "protein", "Ankh3",
        "Multi-task denoising and sequence-completion protein language model for transferable protein representations.",
        "Protein sequence -> embeddings, recovered sequence, or downstream predictions",
        "Public code + non-commercial weights",
        "Protein embeddings, sequence completion, function and property transfer", "2025",
        [("arXiv", "https://arxiv.org/abs/2505.20052")],
        [("GitHub", "https://github.com/agemagician/Ankh"), ("Hugging Face", "https://huggingface.co/ElnaggarLab/ankh3-large")],
        noncommercial=True,
    ),
    record(
        "bfm-esm-s", "protein", "ESM-S",
        "Structure-supervised protein language model producing sequence representations informed by three-dimensional structure.",
        "Protein sequence during inference, structure supervision during training -> structure-aware embeddings",
        "Public code + weights; exact repository licence unresolved",
        "Structure-aware protein embeddings, function prediction, downstream transfer", "2024",
        [("arXiv", "https://arxiv.org/abs/2402.05856")],
        [("GitHub", "https://github.com/DeepGraphLearning/esm-s"), ("Hugging Face", "https://huggingface.co/Oxer11/ESM-S")],
    ),
    record(
        "bfm-proust", "protein", "Proust",
        "Causal protein language model combining sequence generation, embeddings, and zero-shot fitness estimation.",
        "Protein sequence or prompt -> generated sequence, embeddings, or fitness score",
        "Public code + non-commercial checkpoint",
        "Protein generation, representation learning, zero-shot fitness estimation", "2026",
        [("arXiv", "https://arxiv.org/abs/2602.01845")],
        [("GitHub", "https://github.com/Furkan9015/proust-inference"), ("Hugging Face", "https://huggingface.co/nappenstance/proust_v0")],
        noncommercial=True,
    ),
    record(
        "bfm-ab-roberta", "protein", "Ab-RoBERTa",
        "Antibody-specific masked language model trained on antibody sequence repertoires for reusable antibody embeddings and fine-tuning.",
        "Antibody sequence -> embeddings or masked-token predictions",
        "Public checkpoint; separate source repository not confirmed",
        "Antibody representation learning, sequence classification, downstream fine-tuning", "2025",
        [("arXiv", "https://arxiv.org/abs/2506.13006")],
        [("Hugging Face", "https://huggingface.co/mogam-ai/Ab-RoBERTa")],
    ),
    record(
        "bfm-oneprot", "multimodal", "OneProt",
        "Cross-modal protein representation model aligning sequence, structure, binding-site, and textual information in a shared space.",
        "Protein sequence/structure/binding site/text -> aligned embeddings",
        "Public code + weights",
        "Cross-modal protein retrieval, representation learning, annotation and transfer", "2025",
        [("PLOS Computational Biology", "https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1013679")],
        [("GitHub", "https://github.com/klemens-floege/oneprot/"), ("Hugging Face", "https://huggingface.co/HelmholtzAI-FZJ/oneprot-4")],
    ),
    record(
        "bfm-protdat", "multimodal", "ProtDAT",
        "Text-conditioned protein generation model aligning natural-language descriptions with protein sequences.",
        "Functional text prompt -> generated protein sequence",
        "Public code + non-commercial weights",
        "Text-guided protein design, controllable generation, protein-language alignment", "2025",
        [("Nature Communications", "https://doi.org/10.1038/s41467-025-65562-w")],
        [("GitHub", "https://github.com/GXY0116/ProtDAT/tree/v1.0.0"), ("Zenodo weights", "https://zenodo.org/records/14264096")],
        noncommercial=True,
    ),

    # Structure, interaction, chemistry, platform and benchmark lane.
    record(
        "bfm-esmfold2", "complex", "ESMFold2",
        "ESMC-6B-conditioned diffusion model for all-atom prediction of proteins, nucleic acids, ligands, complexes, and binder candidates.",
        "Biomolecular sequence/specification with optional MSA -> all-atom structure",
        "Open code + weights (MIT); local and Biohub Platform inference",
        "Fast structure prediction, complex modeling, interaction and binder assessment", "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.06.03.729735v1")],
        [("GitHub", "https://github.com/Biohub/esm"), ("Hugging Face", "https://huggingface.co/biohub/ESMFold2")],
    ),
    record(
        "bfm-opendde-preview", "complex", "OpenDDE Preview",
        "Preview all-atom co-folding and design model for proteins, nucleic acids, ligands, ions, covalent bonds, and mixed biomolecular assemblies.",
        "Biomolecular JSON specification -> predicted or designed all-atom structure",
        "Open preview code + checkpoints + Docker (Apache-2.0); unstable and not production-ready",
        "All-atom structure prediction, co-folding, interaction modeling and early design research", "2026",
        [("arXiv", "https://arxiv.org/abs/2607.03787")],
        [("GitHub", "https://github.com/aurekaresearch/OpenDDE"), ("Hugging Face", "https://huggingface.co/aurekaresearch/OpenDDE"), ("Project", "https://aurekaresearch.github.io/OpenDDE-Website/")],
    ),
    record(
        "bfm-pocketxmol", "molecule", "PocketXMol",
        "Pocket-interacting molecular generative model supporting docking, conformer generation, structure-based design, linking, growing, PROTACs, and peptides.",
        "Pocket or partial-complex constraints -> molecules, peptide structures, or poses",
        "Open code + weights + train/test data",
        "Structure-based drug design, docking, conformer generation, molecular and peptide design", "2026",
        [("Cell", "https://doi.org/10.1016/j.cell.2026.01.003")],
        [("GitHub", "https://github.com/pengxingang/PocketXMol"), ("Zenodo", "https://doi.org/10.5281/zenodo.17801271")],
    ),
    record(
        "bfm-suiren-1", "molecule", "Suiren-1.0",
        "Molecular foundation-model family for quantum properties, energies, forces, embeddings, conformer aggregation, and intermolecular interactions.",
        "Molecular geometry or representation -> energies, forces, properties, or embeddings",
        "Public code + Base/Dimer/ConfAvg checkpoints; modified MIT-style terms",
        "Molecular property prediction, force modeling, conformer and interaction analysis", "2026",
        [("arXiv", "https://arxiv.org/abs/2603.21942")],
        [("GitHub", "https://github.com/golab-ai/Suiren-Foundation-Model"), ("Hugging Face", "https://huggingface.co/ajy112/Suiren-Base")],
        aliases=["Suiren-Base", "Suiren-Dimer", "Suiren-ConfAvg"],
    ),
    record(
        "bfm-ubio-molfm", "molecule", "UBio-MolFM",
        "Universal biomolecular machine-learning potential based on an equivariant all-atom representation model.",
        "All-atom biomolecular geometry -> energies, forces, embeddings, or molecular-dynamics potential",
        "Open code + public checkpoint (MIT); training-data release is partial/gated",
        "Biomolecular energy and force prediction, simulation, transferable atomistic embeddings", "2026",
        [("arXiv", "https://arxiv.org/abs/2602.17709")],
        [("GitHub", "https://github.com/IQuestLab/UBio-MolFM"), ("Hugging Face", "https://huggingface.co/IQuestLab/IQuest-UBio-MolFM-V1"), ("Data subset", "https://huggingface.co/datasets/IQuestLab/UBio-Protein26")],
    ),
    record(
        "bfm-uma", "molecule", "UMA",
        "Universal atomistic potential spanning molecules, materials, and catalysts; its OMol task covers drug-like molecules and biomolecular use cases.",
        "Atomic structure with task, charge, and spin context -> energies and forces",
        "Open code; gated weights under custom FAIR Chemistry Licence/AUP with geographic restrictions",
        "Molecular and biomolecular simulation, energy/force prediction, materials and catalyst modeling", "2025",
        [("arXiv", "https://arxiv.org/abs/2506.23971")],
        [("GitHub", "https://github.com/facebookresearch/fairchem"), ("Documentation", "https://fair-chem.github.io/uma/"), ("Hugging Face", "https://huggingface.co/facebook/UMA")],
    ),
    record(
        "bfm-seedfold", "complex", "SeedFold / SeedFold-Linear",
        "All-atom folding family for protein-protein, antibody-antigen, protein-ligand, RNA, and DNA complexes.",
        "Biomolecular sequence/complex specification -> predicted all-atom structure",
        "Registration-gated web server; no public code, weights, or explicit model licence located",
        "Complex structure prediction, antibody-antigen and protein-ligand modeling", "2025",
        [("arXiv", "https://arxiv.org/abs/2512.24354")],
        [("Project", "https://seedfold.github.io/"), ("Web server", "https://seedfold.io/")],
        aliases=["SeedFold", "SeedFold-Linear"],
    ),
    record(
        "bfm-boltzgen", "protein", "BoltzGen",
        "All-atom generative binder-design model and workflow for proteins, peptides, nanobodies, small molecules, and other biomolecular targets.",
        "Target structure and design constraints -> ranked binder sequences and structures",
        "Open code + weights + training data (MIT)",
        "Protein and peptide binder design, nanobody design, target-conditioned generation", "2025",
        [("bioRxiv", "https://doi.org/10.1101/2025.11.20.689494")],
        [("GitHub", "https://github.com/HannesStark/boltzgen"), ("Hugging Face", "https://huggingface.co/boltzgen/boltzgen-1"), ("Project", "https://boltz.bio/boltzgen")],
    ),
    record(
        "bfm-pxdesign", "protein", "PXDesign",
        "Diffusion-based protein-binder design suite with structure-prediction and filtering stages.",
        "Target structure/MSA, hotspots, and binder length -> binder sequence/structure candidates and scores",
        "Open code + checkpoint + free web server (Apache-2.0); dependencies have separate terms",
        "De novo protein binder design, target-conditioned generation, candidate filtering", "2025",
        [("bioRxiv", "https://doi.org/10.1101/2025.08.15.670450")],
        [("GitHub", "https://github.com/bytedance/PXDesign"), ("Project", "https://protenix.github.io/pxdesign/"), ("Server", "https://protenix-server.com/")],
    ),
    record(
        "bfm-boltzmol-1", "molecule", "BoltzMol-1",
        "Commercial prospective hit-discovery service combining Boltz-2-style screening, make-on-demand generation, and ADME filtering.",
        "Target and screening/design request -> ranked or generated molecular candidates",
        "Commercial web/API access only; no public code or weights",
        "Virtual screening, hit discovery, molecular generation and prioritization", "2026",
        [("Technical report", "https://boltz.bio/boltzmol1-technical-report.pdf")],
        [("Announcement", "https://boltz.bio/boltzmol-boltzprot-api"), ("API", "https://api.boltz.bio/")],
    ),
    record(
        "bfm-boltzprot-1", "protein", "BoltzProt-1",
        "Commercial protein-binder and nanobody-design service combining generative design with interaction ranking.",
        "Target structure and binder-design request -> ranked protein or nanobody candidates",
        "Commercial web/API access only; no public code or weights",
        "Protein binder design, nanobody generation, candidate ranking", "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.06.23.733997v1"), ("Technical report", "https://boltz.bio/boltzprot1-technical-report.pdf")],
        [("Announcement", "https://boltz.bio/boltzmol-boltzprot-api"), ("API", "https://api.boltz.bio/")],
    ),
    record(
        "bfm-seedproteo", "protein", "SeedProteo",
        "All-atom binder and unconditional protein-design system accessed through the Seed web service.",
        "Target/design constraints -> protein binder or unconditional design candidates",
        "Registration-gated web server; no public code, weights, or explicit model licence located",
        "Protein binder design, unconditional protein generation, structure-conditioned design", "2025",
        [("arXiv", "https://arxiv.org/abs/2512.24192")],
        [("Project", "https://seedfold.github.io/"), ("Web server", "https://seedfold.io/proteinDesign")],
    ),
    record(
        "bfm-alphaproteo", "protein", "AlphaProteo",
        "DeepMind protein-binder design system for generating candidate binders against specified target proteins.",
        "Target protein structure -> designed binder sequences and structures",
        "Paper/project only; no public code, weights, server/API, or model licence",
        "De novo protein binder design and experimental candidate generation", "2024",
        [("arXiv", "https://arxiv.org/abs/2409.08022")],
        [("Official project", "https://deepmind.google/blog/alphaproteo-generates-novel-proteins-for-biology-and-health-research/")],
    ),
    record(
        "bfm-rosetta-foundry", "platform", "Rosetta Foundry",
        "Shared training, inference, packaging, and model-registry platform for RF3, RFD3/RFD3NA, ProteinMPNN, LigandMPNN, and related RosettaCommons models.",
        "Model specification and biomolecular inputs -> installed models, training or inference workflows",
        "Open platform code + model checkpoints (BSD-3-Clause); some model APIs still stabilizing",
        "Reproducible model installation, training, inference, and Rosetta model discovery", "2025",
        [],
        [("GitHub", "https://github.com/RosettaCommons/foundry"), ("Documentation", "https://rosettacommons.github.io/foundry/")],
    ),
    record(
        "bfm-foldbench", "benchmark", "FoldBench",
        "Low-homology benchmark of biological assemblies across all-atom structure-prediction tasks involving proteins, nucleic acids, ligands, and interactions.",
        "Predicted assemblies + references -> quality and generalization metrics",
        "Open benchmark targets + evaluation code + samples (MIT); public results",
        "All-atom structure-prediction evaluation and generalization testing", "2025",
        [("Nature Communications", "https://doi.org/10.1038/s41467-025-67127-3")],
        [("GitHub", "https://github.com/BEAM-Labs/FoldBench")],
    ),
    record(
        "bfm-pxmeter", "benchmark", "PXMeter",
        "Structural-quality evaluation toolkit and curated benchmark pipeline for all-atom structure prediction.",
        "Predicted structures + benchmark references -> structural quality metrics",
        "Open evaluation toolkit + benchmark datasets/pipelines (Apache-2.0)",
        "All-atom model evaluation, structural-quality diagnostics, reproducible benchmarking", "2025",
        [("bioRxiv", "https://doi.org/10.1101/2025.07.17.664878")],
        [("GitHub", "https://github.com/bytedance/PXMeter")],
    ),
    record(
        "bfm-pfmbench", "benchmark", "PFMBench",
        "Protein-foundation-model evaluation suite spanning dozens of tasks, multiple protein-science areas, and fine-tuning and zero-shot settings.",
        "Protein foundation model + task datasets -> standardized evaluation results",
        "Open benchmark code + task-data links (Apache-2.0); no public leaderboard confirmed",
        "Comparative evaluation and model selection across protein-science tasks", "2025",
        [("arXiv", "https://arxiv.org/abs/2506.14796")],
        [("GitHub", "https://github.com/biomap-research/PFMBench")],
    ),
    record(
        "bfm-protein-se3", "benchmark", "Protein-SE(3)",
        "Unified retraining and evaluation framework for SE(3)-equivariant protein structure-generation models.",
        "Structure-generation model + standardized data -> retrained models and comparable metrics",
        "Open benchmark/training framework + preprocessed data (MIT)",
        "Evaluation of RFdiffusion, Genie, FrameDiff, FoldFlow/FrameFlow and related generators", "2025",
        [("arXiv", "https://arxiv.org/abs/2507.20243")],
        [("GitHub", "https://github.com/BruthYU/protein-se3")],
    ),
    record(
        "bfm-esm-atlas", "platform", "ESM Atlas",
        "Public protein-sequence and structure atlas with large-scale ESM-derived embeddings, predicted structures, search, and an alpha API.",
        "Protein sequence/query -> atlas search results, embeddings, structures, and metadata",
        "Public web atlas + alpha API; explicit current dataset licence not located",
        "Protein-space exploration, similarity search, predicted-structure access and programmatic retrieval", "2026",
        [],
        [("Biohub resources", "https://biohub.ai/resources"), ("ESM repository", "https://github.com/Biohub/esm"), ("Atlas API", "https://biohub.ai/esm/protein/atlas/api-docs/")],
    ),

    # Omics, spatial, multimodal, platform and benchmark lane.
    record(
        "bfm-biomatrix", "multimodal", "BioMatrix",
        "Native multimodal biomolecular generalist spanning molecule and protein sequences, three-dimensional structures, and natural language.",
        "Biomolecular sequence/structure/text -> cross-modal embeddings, understanding, or generation",
        "Open code + weights (Apache-2.0)",
        "Folding, inverse folding, design, captioning, affinity and interaction prediction", "2026",
        [("arXiv", "https://arxiv.org/abs/2606.22138")],
        [("GitHub", "https://github.com/QizhiPei/BioMatrix"), ("Hugging Face", "https://huggingface.co/QizhiPei/BioMatrix-4B-SFT")],
    ),
    record(
        "bfm-genejepa", "singlecell", "GeneJEPA",
        "Joint-embedding predictive transcriptomic model trained on large-scale single-cell data for transferable cell and gene representations.",
        "Sparse single-cell counts -> cell/gene embeddings and latent predictions",
        "Public source + checkpoint; checkpoint MIT, source-code licence not stated",
        "Cell clustering, representation transfer, perturbation and drug-response prediction", "2025",
        [("bioRxiv", "https://www.biorxiv.org/content/10.1101/2025.10.14.682378v1")],
        [("GitHub", "https://github.com/BiostateAI/GeneJEPA"), ("Hugging Face", "https://huggingface.co/elonlit/GeneJEPA")],
    ),
    record(
        "bfm-eva-scienta", "multimodal", "EVA (Scienta)",
        "Cross-species immunology and inflammation model combining transcriptomic and histology information for patient-level and translational representations; only EVA-RNA is publicly released.",
        "Bulk, microarray, or pseudobulk RNA with optional histology -> sample/gene embeddings and translational predictions",
        "Gated EVA-RNA weights under custom Scienta licence; full multimodal system closed",
        "Target efficacy, perturbation transfer, stratification and response prediction", "2026",
        [("arXiv", "https://arxiv.org/abs/2602.10168")],
        [("EVA-RNA", "https://huggingface.co/ScientaLab/eva-rna")],
        noncommercial=True,
    ),
    record(
        "bfm-genbio-pathfm", "spatial", "GenBio-PathFM",
        "Large histopathology representation model trained from public pathology data for transferable H&E patch embeddings.",
        "H&E image tiles -> transferable patch embeddings",
        "Public code + gated weights under a restrictive non-commercial licence",
        "Pathology representation learning, biomarker inference, classification and robustness analysis", "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.03.17.712534v1")],
        [("GitHub", "https://github.com/genbio-ai/genbio-pathfm"), ("Hugging Face", "https://huggingface.co/genbio-ai/genbio-pathfm")],
        noncommercial=True,
    ),
    record(
        "bfm-squall", "spatial", "SQUALL",
        "Joint histology and spatial-transcriptomics model pretrained on paired image and spatial molecular observations.",
        "H&E + spatial expression -> joint embeddings, reconstructed expression, and biomarker profiles",
        "Public code + weights + pretraining data under CC BY-NC-ND-4.0",
        "Virtual biomarkers, cross-platform spatial profiling, clustering and representation learning", "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.06.01.729028v1")],
        [("GitHub", "https://github.com/OswaldZhang/SQUALL-release"), ("Hugging Face", "https://huggingface.co/zongxu/SQUALL"), ("Zenodo data", "https://zenodo.org/records/17318279")],
        noncommercial=True,
    ),
    record(
        "bfm-spatialwhisperer", "spatial", "SpatialWhisperer",
        "Trimodal histology, expression, and language model placing image, molecular, and text signals in a shared embedding space.",
        "Image, expression, or text -> shared embeddings and natural-language cell queries",
        "Public code + non-commercial checkpoint; depends on gated UNI2",
        "Zero-shot cell typing, spatial annotation, cross-modal retrieval and natural-language querying", "2026",
        [("OpenReview", "https://openreview.net/forum?id=Ze7U293Zw4")],
        [("GitHub", "https://github.com/zinagoodlab/spatialwhisperer"), ("Hugging Face", "https://huggingface.co/Good-Lab/spatialwhisperer")],
        noncommercial=True,
    ),
    record(
        "bfm-deepspot-m", "spatial", "DeepSpot-M",
        "Gene-query model for transcriptome-wide virtual spatial transcriptomics from routine histology.",
        "H&E tile -> spatial expression predictions across a transcriptome-scale gene set",
        "Public non-commercial code + weights",
        "Virtual spatial transcriptomics, biomarker mapping, adaptation and large-cohort profiling", "2026",
        [("medRxiv", "https://www.medrxiv.org/content/10.64898/2026.06.19.26356060v1")],
        [("GitHub", "https://github.com/ratschlab/DeepSpotM"), ("Hugging Face", "https://huggingface.co/ratschlab/DeepSpotM")],
        noncommercial=True,
    ),
    record(
        "bfm-h2o-spatial", "spatial", "H2O",
        "Histopathology-to-spatial-transcriptomics and proteomics framework for predicting molecular landscapes from routine H&E images.",
        "H&E patches + spatial context -> spatial transcriptomic or proteomic expression",
        "Public source; referenced checkpoint is absent; all rights reserved and no reuse licence",
        "Virtual spatial multi-omics, clustering, communication and trajectory analysis", "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.04.21.717342v1")],
        [("GitHub", "https://github.com/TencentAILabHealthcare/H2O")],
        noncommercial=True,
    ),
    record(
        "bfm-lemon", "spatial", "LEMON",
        "Self-supervised single-nucleus morphology foundation model trained on millions of cell images.",
        "H&E nucleus crop -> compact cell-morphology embedding",
        "Public inference code + weights (MIT)",
        "Cell typing, gene-expression prediction and quantitative morphology studies", "2026",
        [("arXiv", "https://arxiv.org/abs/2603.25802")],
        [("Hugging Face", "https://huggingface.co/aliceblondel/LEMON")],
    ),
    record(
        "bfm-mupd", "spatial", "MuPD (Multimodal Pathology Diffusion)",
        "Generative multimodal pathology diffusion model sharing histology, transcriptomic, and clinical-text context.",
        "Text, RNA, and image combinations -> generated H&E, IHC, or multiplex-immunofluorescence images",
        "Public code + gated weights under CC BY-NC-ND-4.0",
        "Virtual staining, missing-modality generation and pathology-image augmentation", "2026",
        [("arXiv", "https://arxiv.org/abs/2604.03635")],
        [("Hugging Face code + weights", "https://huggingface.co/xiangjx/MuPaD-256")],
        noncommercial=True, aliases=["MuPaD", "MUPAD"],
    ),
    record(
        "bfm-bioairepo", "platform", "BioAIrepo",
        "EMBL-EBI BioStudies pilot repository for depositing and discovering life-science AI models, metadata, weights, and associated data.",
        "Model submission with metadata/assets -> searchable reusable model record",
        "Open institutional model repository / pilot; individual deposits retain their own terms",
        "FAIR-oriented model deposit, discovery, metadata and reuse", "2026",
        [("EMBL-EBI announcement", "https://www.ebi.ac.uk/about/news/technology-and-innovation/bioairepo-embl-ebis-hub-for-life-science-ai-models/")],
        [("Repository", "https://www.ebi.ac.uk/biostudies/BioAIrepo")],
    ),
    record(
        "bfm-vcbench", "benchmark", "VCBench",
        "Operational benchmark for single-cell foundation models with capability evaluation and a contamination-reporting schema.",
        "Single-cell model checkpoints + datasets -> capability, baseline, and contamination results",
        "Open code + evaluation artifacts",
        "Perturbation, cross-species, GRN, RNA-protein and temporal single-cell evaluation", "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.06.18.733146v1")],
        [("GitHub", "https://github.com/AppliedScientific/VCBench"), ("Hugging Face", "https://huggingface.co/collections/appliedscientific/vcbench-v100-single-cell-foundation-model-benchmark")],
    ),
    record(
        "bfm-scmbench", "benchmark", "SCMBench",
        "Benchmark of domain-specific and foundation models for paired and unpaired single-cell multi-omics integration.",
        "Multi-omics datasets + integration methods -> integration, biological-conservation, and batch metrics",
        "Open code + public data (MIT)",
        "RNA/ATAC/protein integration benchmarking and method selection", "2026",
        [("Nature Communications", "https://www.nature.com/articles/s41467-026-72570-x")],
        [("GitHub", "https://github.com/ml4bio/SCMBench")],
    ),
    record(
        "bfm-spapath-bench", "benchmark", "SpaPath-Bench",
        "Representation-level evaluation of pathology foundation models using paired whole-slide images and spatial transcriptomics.",
        "Pathology-model embeddings + paired WSI/ST slides -> spatial-domain scores",
        "Public paper and results dashboard; benchmark execution pipeline not released",
        "Pathology-encoder selection and spatial representation diagnostics", "2026",
        [("arXiv", "https://arxiv.org/abs/2605.25764")],
        [("Dashboard", "https://bokai-zhao.github.io/SpaPath-benchboard/")],
    ),
    record(
        "bfm-gpt-rosalind", "multimodal", "GPT-Rosalind",
        "Purpose-built life-science reasoning model for chemistry, proteins, genomics, evidence synthesis, tools, and experiment planning.",
        "Scientific questions + literature/data/tools -> synthesis, analysis, or experimental plans",
        "Restricted research preview in ChatGPT, Codex, and API for qualified institutions; no public weights/code",
        "Life-science reasoning, evidence synthesis, data analysis and experiment planning", "2026",
        [("Official release", "https://openai.com/index/introducing-gpt-rosalind/")],
        [("Access request", "https://openai.com/form/life-sciences-access/")],
    ),
    record(
        "bfm-mimic-polymathic", "multimodal", "MIMIC",
        "Any-to-any biomolecular model spanning DNA, RNA, proteins, structures, and cellular and semantic context.",
        "Biological sequence/structure/context modalities -> aligned or generated multimodal outputs",
        "Paper and informational repository; model code, weights, and LORE assets announced but not released",
        "Cross-modal biomolecular representation, retrieval, understanding and generation", "2026",
        [("arXiv", "https://arxiv.org/abs/2604.24506")],
        [("GitHub", "https://github.com/PolymathicAI/MIMIC")],
    ),
    record(
        "bfm-holocell", "singlecell", "HoloCell",
        "Generative single-cell model integrating epigenomic, transcriptomic, and proteomic modalities.",
        "Partial multi-omic cell profile -> cell embeddings and missing-modality generation",
        "Paper only; project repository says artifacts are in preparation and licence remains unresolved",
        "Multi-omic cell representation, missing-modality prediction and generative integration", "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.06.07.730684v2")],
        [("Placeholder repository", "https://github.com/bjzgcai/HoloCell")],
    ),
    record(
        "bfm-cellos", "singlecell", "CellOS",
        "Large multi-view single-cell joint-embedding predictive model for cell-state representation and perturbation prediction.",
        "Single-cell transcriptome -> cell-state embeddings and perturbation predictions",
        "Paper only; no public code or weights found",
        "Cell-state representation, transfer and perturbation prediction", "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.06.18.733163v2")],
        [],
    ),
    record(
        "bfm-omnicell-bgi", "spatial", "OmniCell",
        "Tissue-contextual model pretrained across dissociated and spatial expression profiles for unified cellular and molecular representations.",
        "Single-cell or spatial expression + tissue context -> unified cell and molecular representations",
        "Public source + checkpoint; source MIT and checkpoint labelled Apache-2.0",
        "Single-cell and spatial representation, tissue-context transfer and downstream prediction", "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2025.12.29.696804v3")],
        [("GitHub", "https://github.com/BGIResearch/omnicell"), ("ModelScope", "https://modelscope.cn/models/PJSucas/OmniCell-v1")],
    ),
    record(
        "bfm-bioreason-pro", "multimodal", "BioReason-Pro",
        "Protein-function reasoning model combining protein sequence understanding with language-model reasoning and tool/evidence workflows; distinct from the DNA-focused BioReason model.",
        "Protein sequence + scientific question/evidence -> multi-step protein-function reasoning",
        "Public source + web interface + Apache-2.0 weights; source-code licence not separately stated",
        "Protein-function reasoning, annotation, evidence synthesis and mechanistic explanation", "2026",
        [("bioRxiv", "https://www.biorxiv.org/content/early/2026/03/20/2026.03.19.712954")],
        [("GitHub", "https://github.com/bowang-lab/BioReason-Pro"), ("Hugging Face collection", "https://huggingface.co/collections/wanglab/bioreason-pro"), ("SFT weights", "https://huggingface.co/wanglab/bioreason-pro-sft"), ("RL weights", "https://huggingface.co/wanglab/bioreason-pro-rl")],
    ),
]


def main() -> None:
    records = json.loads(DATA.read_text())
    by_id = {item["id"]: item for item in records}
    if len(by_id) != len(records):
        raise SystemExit("duplicate IDs exist before migration")

    missing_updates = sorted(set(UPDATES) - set(by_id))
    if missing_updates:
        raise SystemExit(f"update targets missing: {missing_updates}")

    for record_id, patch in UPDATES.items():
        by_id[record_id].update(patch)

    added = 0
    replaced = 0
    for item in NEW_RECORDS:
        record_id = item["id"]
        if record_id in by_id:
            by_id[record_id].clear()
            by_id[record_id].update(item)
            replaced += 1
        else:
            records.append(item)
            by_id[record_id] = item
            added += 1

    if len({item["id"] for item in records}) != len(records):
        raise SystemExit("duplicate IDs after migration")
    display_names = [item["name"].casefold().strip() for item in records]
    if len(set(display_names)) != len(display_names):
        raise SystemExit("exact duplicate display names after migration")

    DATA.write_text(json.dumps(records, indent=1, ensure_ascii=False) + "\n")
    print(f"updated={len(UPDATES)} added={added} replaced={replaced} total={len(records)}")


if __name__ == "__main__":
    main()
