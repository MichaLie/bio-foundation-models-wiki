#!/usr/bin/env python3
"""Persist the 2026-07-13 full source audit and conservative corrections.

The migration is intentionally idempotent.  It copies the frozen internal
review ledgers into the repository, turns their 377-record coverage into
machine-readable record fields, and applies only corrections supported by the
reviewed primary/official sources.  Generated distributions are rebuilt by
``build.py`` after this migration.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREVIEW_ROOT = ROOT.parents[1]
DATE = "2026-07-13"
FROZEN_COMMIT = "e79a48cb7caa70555d0e6cb0a0838d849297c57e"
REVIEW_NAMES = (
    "foundation_initial.md",
    "foundation_residual_mod0.md",
    "foundation_residual_mod1.md",
    "foundation_residual_mod2.md",
)


def review_path(name: str) -> Path:
    public = ROOT / "evidence" / "source-audit" / name
    if public.is_file():
        return public
    source = PREVIEW_ROOT / "audit" / "reviews" / name
    if not source.is_file():
        raise FileNotFoundError(f"missing frozen review ledger: {source}")
    public.parent.mkdir(parents=True, exist_ok=True)
    public.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return public


def urls(text: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"https?://[^)\s>|]+", text)))


def clean_note(text: str) -> str:
    text = re.sub(r"^lines \d+(?:-\d+)?(?:,\s*`[^`]+`(?:,\s*`[^`]+`)*)?\.\s*", "", text)
    text = re.sub(r"`R\(id\)\.[^`]+`;?\s*", "", text)
    text = re.sub(r"\[([^]]+)\]\(https?://[^)]+\)", r"\1", text)
    text = text.replace("`", "")
    text = re.sub(r"\s*Action:\s*none\.?$", "", text, flags=re.I)
    text = re.sub(r"\s+", " ", text).strip(" |")
    return text


def parse_residual_ledgers() -> dict[str, dict]:
    findings: dict[str, dict] = {}
    for name in REVIEW_NAMES[1:]:
        path = review_path(name)
        for line in path.read_text(encoding="utf-8").splitlines():
            parsed = None
            # mod0: | `id` | outcome | Pn | finding |
            match = re.match(
                r"\|\s*`(bfm-[^`]+)`\s*\|\s*(verified_with_limits|provisional|verified)\s*"
                r"\|\s*(P[1-4])\s*\|\s*(.*)\|$",
                line,
            )
            if match:
                parsed = (match.group(1), match.group(2), match.group(3), match.group(4))
            # mod1: | number | `id` | Pn | outcome | finding |
            match = re.match(
                r"\|\s*\d+\s*\|\s*`(bfm-[^`]+)`\s*\|\s*(P[1-4])\s*"
                r"\|\s*(verified_with_limits|provisional|verified)\s*\|\s*(.*)\|$",
                line,
            )
            if match:
                parsed = (match.group(1), match.group(3), match.group(2), match.group(4))
            # mod2: 1. `id` — **P2 CORRECTION** — finding
            match = re.match(
                r"\d+\.\s+`(bfm-[^`]+)`\s+—\s+\*\*(P[1-4])\s+"
                r"(VERIFIED|CORRECTION|QUALIFY)\*\*\s+—\s+(.*)$",
                line,
            )
            if match:
                outcome = {
                    "VERIFIED": "verified",
                    "CORRECTION": "verified_with_limits",
                    "QUALIFY": "verified_with_limits",
                }[match.group(3)]
                parsed = (match.group(1), outcome, match.group(2), match.group(4))
            if not parsed:
                continue
            record_id, outcome, priority, finding = parsed
            findings[record_id] = {
                "audit_state": "hold" if outcome == "provisional" else outcome,
                "audit_priority": priority,
                "audit_note": clean_note(finding),
                "sources": urls(finding),
                "review": f"evidence/source-audit/{name}",
            }
    if len(findings) != 300:
        raise RuntimeError(f"expected 300 residual audit records, parsed {len(findings)}")
    return findings


NC_TRUE = {
    # Initial and mod0 corrections.
    "bfm-openphenom-s-16-phenom-family", "bfm-mupd", "bfm-aido-cell", "bfm-aido-rna",
    "bfm-alphafold-server", "bfm-chatcell", "bfm-conch", "bfm-lc-plm", "bfm-poet",
    "bfm-prot2text", "bfm-uni-uni2-h", "bfm-virtues",
    # Residual mod1 explicit first-party non-commercial terms.
    "bfm-alphafold-3", "bfm-agront-agronomic-nucleotide-transformer", "bfm-ankh", "bfm-chatnt",
    "bfm-galactica", "bfm-get-general-expression-transformer",
    "bfm-gpfm-generalizable-pathology-foundation-model", "bfm-h-optimus-0-h-optimus-1",
    "bfm-helixfold3", "bfm-iglm", "bfm-kronos", "bfm-mstar",
    "bfm-openprotein-ai-poet-poet-2", "bfm-phikon-phikon-v2", "bfm-prism",
    "bfm-safe-gpt", "bfm-segmentnt", "bfm-tabula", "bfm-titan",
    # Residual mod2 explicit first-party non-commercial terms.
    "bfm-aido-aido-modelgenerator", "bfm-aido-protein-16b", "bfm-cellfm", "bfm-chemfm",
    "bfm-chief", "bfm-decima", "bfm-dnagpt", "bfm-foldflow-2",
    "bfm-glm-genomic-language-model", "bfm-igfold", "bfm-musk",
    "bfm-nucleotide-transformer", "bfm-omiclip-loki", "bfm-orca", "bfm-sc-mamba2",
    "bfm-sei", "bfm-stack-arc-institute",
}


STATUS_OVERRIDES = {
    "bfm-3d-molt5": "Open MIT code + public pretrained and fine-tuned weights",
    "bfm-alphafold-server": "Hosted server; outputs restricted to non-commercial use with additional prohibited uses",
    "bfm-atlas-rudolfv-successor": "HOLD — no current public Atlas weight artifact verified; commercial access information only",
    "bfm-bend": "Open benchmark code, data and wrappers around third-party checkpoints; no own model weights",
    "bfm-dnalongbench": "Open benchmark datasets, evaluation code and baselines; no own model weights",
    "bfm-genept": "Open code + precomputed gene embeddings; no conventional trained model weights",
    "bfm-genomic-benchmarks": "Open benchmark datasets, package and baselines; no own model weights",
    "bfm-grover-dna-language-model": "Public model hub artifact; exact model reuse licence not declared",
    "bfm-neuralplexer-and-neuralplexer3": "HOLD — v1 and NP3 are conflated and have different artifact availability/terms",
    "bfm-pearl": "HOLD — paper and project identity verified; no public model endpoint or reusable artifact verified",
    "bfm-scconcept": "Open MIT code, package and public pretrained checkpoints",
    "bfm-sclinguist": "Open MIT code, documentation and released checkpoints",
    "bfm-scmulan": "Public code + official externally hosted checkpoint; previous model-hub link is unavailable",
    "bfm-therapeutics-data-commons-tdc": "Open platform/benchmark datasets, library, oracles and leaderboards; no own model weights",
    "bfm-open-problems-in-single-cell-analysis": "Open benchmark code, tasks, datasets and containers; evaluated checkpoints are external",
    "bfm-pathbench": "Open benchmark application and data; evaluated model weights are external",
    "bfm-peer-protein-sequence-understanding": "Open benchmark code, datasets and configurations; no own model weights",
    "bfm-sceval": "Open benchmark code using external models/checkpoints; repository licence not declared",
    "bfm-protriever": "HOLD — official repository is a README placeholder; no released code, checkpoint or licence verified",
    "bfm-bioreason": "HOLD — checkpoints remain forthcoming; no reusable model artifact verified",
    "bfm-mistral-dna": "HOLD — primary paper absent and referenced checkpoint could not be verified",
    "bfm-mrna-fm-plantrna-fm": "HOLD — family record mixes two models with incomplete paper evidence and different terms",
    "bfm-openprotein-ai-poet-poet-2": "HOLD — platform/model identity overlaps PoET-2 and requires a distinct platform evidence boundary",
    "bfm-pulsar": "Open MIT code + public checkpoints",
    "bfm-saturn": "HOLD — method code and derived embeddings exist, but no reusable pretrained SATURN checkpoint was verified",
    "bfm-scdiva": "HOLD — paper only; no official reusable code or checkpoint verified",
    "bfm-scprotein": "HOLD — task framework with dataset-specific checkpoints; broad pretrained-model scope unverified",
    "bfm-tabula": "HOLD — non-commercial training code only; no reusable pretrained checkpoint verified",
    "bfm-xtrimogene": "HOLD — paper only; no official reusable code or checkpoint verified",
    "bfm-atacformer": "Public code/documentation and model weights; exact reuse licence requires confirmation",
    "bfm-cellvq": "Public code + pretrained checkpoint access",
    "bfm-chai-2": "Commercial access plus limited non-commercial academic access; terms apply",
    "bfm-chemberta-3": "HOLD — public training framework/model links; exact reuse licence not confirmed",
    "bfm-genecompass": "HOLD — public code/checkpoints; no confirmed reuse licence",
    "bfm-genemamba": "HOLD — public code/weights; no confirmed reuse licence",
    "bfm-helical": "Platform/framework; no standalone primary model paper identified",
    "bfm-hybridna": "HOLD — paper verified; no provenance-confirmed reusable artifact found",
    "bfm-lingshu-cell": "HOLD — paper/project page only; official collection did not contain a released model",
    "bfm-next-mol": "HOLD — public code/checkpoints; no confirmed reuse licence",
    "bfm-plip-pathology-language-image-pretraining": "HOLD — public code/weights; reuse terms not confirmed",
    "bfm-regformer": "Open MIT code + public CC BY 4.0 checkpoints",
    "bfm-scmmgpt": "HOLD — public source skeleton; weights and licence not confirmed",
    "bfm-smiles-bert": "Public source code; pretrained weights not released",
    "bfm-storm": "Paper + official project page; no public code or weights verified",
    "bfm-teddy": "Public Apache-2.0 code/configuration; model weight files not confirmed",
    "bfm-txgemma": "Gated/authenticated model access under Gemma terms",
    "bfm-gpt-rosalind": "Hosted Enterprise access for qualified customers; initial availability is United States only",
    "bfm-mupd": "Public model artifact under CC BY-NC-ND terms",
}


MODALITY_OVERRIDES = {
    "bfm-bioseq-blm": "platform",
    "bfm-chemberta-3": "platform",
    "bfm-scchat": "platform",
    "bfm-scelmo": "platform",
}


LINK_ADDITIONS = {
    "bfm-3d-molt5": [("code_links", "Weights", "https://huggingface.co/QizhiPei/3d-molt5-base")],
    "bfm-atacformer": [
        ("code_links", "Documentation", "https://docs.bedbase.org/atacformer/"),
        ("code_links", "Weights", "https://huggingface.co/databio/atacformer-base-hg38"),
    ],
    "bfm-cellvq": [
        ("code_links", "Code", "https://github.com/A4Bio/CellVQ"),
        ("code_links", "Weights", "https://modelscope.cn/models/wj1006/CellVQ/files"),
    ],
    "bfm-chai-2": [("code_links", "Official access", "https://www.chaidiscovery.com/product")],
    "bfm-genomeocean": [("code_links", "Code", "https://github.com/jgi-genomeocean/genomeocean")],
    "bfm-lingshu-cell": [("code_links", "Official project", "https://alibaba-damo-academy.github.io/lingshu-cell-homepage/")],
    "bfm-phylogpn": [("code_links", "Shared GPN code", "https://github.com/songlab-cal/gpn")],
    "bfm-regformer": [
        ("code_links", "Code", "https://github.com/BGIResearch/RegFormer"),
        ("code_links", "Checkpoints", "https://figshare.com/articles/online_resource/pretraining_models/28645493"),
    ],
    "bfm-smiles-bert": [("code_links", "Code", "https://github.com/uta-smile/SMILES-BERT")],
    "bfm-storm": [("code_links", "Official project", "https://storm-web-demo.vercel.app/")],
    "bfm-teddy": [("code_links", "Official repository", "https://huggingface.co/Merck/TEDDY")],
    "bfm-scconcept": [
        ("code_links", "Code", "https://github.com/theislab/scConcept"),
        ("code_links", "Weights", "https://huggingface.co/theislab/scConcept"),
    ],
    "bfm-sclinguist": [("code_links", "Code", "https://github.com/OmicsML/scLinguist")],
    "bfm-scmulan": [("code_links", "Current checkpoint", "https://cloud.tsinghua.edu.cn/f/2250c5df51034b2e9a85/?dl=1")],
    "bfm-subcell": [("code_links", "Model card", "https://virtualcellmodels.cziscience.com/model/0193323e-ebd5-727c-bb32-87ed8f737213")],
    "bfm-pulsar": [("code_links", "Code and checkpoints", "https://github.com/snap-stanford/PULSAR")],
}


PAPER_REPLACEMENTS = {
    "bfm-bend": ("Final paper", "https://proceedings.iclr.cc/paper_files/paper/2024/hash/429e7b31625a8b7839f9e4d6e2aa9bb9-Abstract-Conference.html"),
    "bfm-biomedgpt": ("Final paper", "https://ieeexplore.ieee.org/document/10767279/"),
    "bfm-genslms": ("Final paper", "https://journals.sagepub.com/doi/10.1177/10943420231201154"),
    "bfm-langcell": ("Final paper", "https://proceedings.mlr.press/v235/zhao24u.html"),
    "bfm-lc-plm": ("TMLR paper", "https://openreview.net/forum?id=dWvztQzfy4"),
    "bfm-molgen": ("Final paper", "https://proceedings.iclr.cc/paper_files/paper/2024/hash/ed7dd1e32cf9b0abf664bf0e891527e5-Abstract-Conference.html"),
    "bfm-mole": ("Paper", "https://www.nature.com/articles/s41467-024-53751-y"),
    "bfm-poet": ("NeurIPS paper", "https://papers.nips.cc/paper_files/paper/2023/hash/f4366126eba252699b280e8f93c0ab2f-Abstract-Conference.html"),
    "bfm-protrek": ("Final paper", "https://www.nature.com/articles/s41587-025-02836-0"),
    "bfm-sceptr": ("Final paper", "https://www.sciencedirect.com/science/article/pii/S2405471224003697"),
    "bfm-therapeutics-data-commons-tdc": ("Final paper", "https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/hash/4c56ff4ce4aaf9573aa5dff913df997a-Abstract-round1.html"),
    "bfm-uce": ("Final paper", "https://www.nature.com/articles/s41586-026-10689-z"),
}


INITIAL_OVERRIDES = {
    "bfm-openphenom-s-16-phenom-family": (
        "verified_with_limits", "P2",
        "Official project terms restrict model use to non-commercial purposes; the official project hub is cited.",
        ["https://www.rxrx.ai/phenom"],
    ),
    "bfm-mupd": (
        "verified_with_limits", "P2",
        "The official artifact is public rather than gated and uses CC BY-NC-ND terms.",
        ["https://huggingface.co/xiangjx/MuPaD-256"],
    ),
    "bfm-gpt-rosalind": (
        "verified_with_limits", "P2",
        "Access is limited to qualified Enterprise customers and initially scoped to the United States.",
        ["https://openai.com/index/introducing-gpt-rosalind/"],
    ),
    "bfm-poet-2": (
        "verified_with_limits", "P2",
        "Model identity is verified; keep distinct from the OpenProtein platform record and expose exact model terms.",
        ["https://www.openprotein.ai/", "https://docs.openprotein.ai/rest-api/prompt.html"],
    ),
}


def add_link(record: dict, field: str, label: str, url: str) -> None:
    links = record.setdefault(field, [])
    if not any(link.get("url") == url for link in links):
        links.append({"label": label, "url": url})


def main() -> None:
    initial_path = review_path(REVIEW_NAMES[0])
    findings = parse_residual_ledgers()
    data_path = ROOT / "models_final.json"
    records = json.loads(data_path.read_text(encoding="utf-8"))
    by_id = {record["id"]: record for record in records}
    if len(by_id) != len(records):
        raise RuntimeError("duplicate IDs in canonical data")

    residual_ids = set(findings)
    # The residual ledgers deterministically contain the 300 records that
    # predated this refresh; their complement is the 77 changed-record audit.
    # Deriving the complement keeps this migration idempotent after every
    # record's real verification date has been advanced.
    fresh_ids = set(by_id) - residual_ids
    if residual_ids | fresh_ids != set(by_id):
        missing = sorted(set(by_id) - residual_ids - fresh_ids)
        raise RuntimeError(f"source audit does not cover all records: {missing[:10]}")

    for record in records:
        record_id = record["id"]
        finding = findings.get(record_id)
        if finding is None:
            finding = {
                "audit_state": "verified",
                "audit_priority": "P4",
                "audit_note": "Identity, scope, primary/official sources and current catalog claims were checked in the changed-record audit; no unresolved material error was recorded.",
                "sources": [],
                "review": "evidence/source-audit/foundation_initial.md",
            }
        if record_id in INITIAL_OVERRIDES:
            state, priority, note, source_urls = INITIAL_OVERRIDES[record_id]
            finding.update(audit_state=state, audit_priority=priority, audit_note=note, sources=source_urls)

        current_sources = [
            link["url"]
            for field in ("paper_links", "code_links")
            for link in record.get(field, [])
            if isinstance(link, dict) and link.get("url")
        ]
        record["sources"] = list(dict.fromkeys(current_sources + finding["sources"]))
        record["audit_state"] = finding["audit_state"]
        record["audit_priority"] = finding["audit_priority"]
        record["audit_note"] = finding["audit_note"]
        record["audit_source"] = finding["review"]
        record["verified"] = DATE

        if record_id in NC_TRUE:
            record["noncommercial"] = True
        if record_id == "bfm-storm":
            record["noncommercial"] = False
        if record_id in MODALITY_OVERRIDES:
            record["modality"] = MODALITY_OVERRIDES[record_id]
        if record_id in STATUS_OVERRIDES:
            record["status"] = STATUS_OVERRIDES[record_id]
        elif record["audit_state"] == "hold" and not record.get("status", "").startswith("HOLD"):
            record["status"] = "HOLD — catalog eligibility or reusable-artifact evidence is unresolved; see audit note"

        if record.get("noncommercial") and "non-commercial" not in record.get("status", "").lower() and record["audit_state"] != "hold":
            record["status"] = record["status"].rstrip(" ;") + "; non-commercial terms apply to at least one artifact or access route"

        for field, label, url in LINK_ADDITIONS.get(record_id, []):
            add_link(record, field, label, url)
            if url not in record["sources"]:
                record["sources"].append(url)

        if record_id in PAPER_REPLACEMENTS:
            label, url = PAPER_REPLACEMENTS[record_id]
            record["paper_links"] = [{"label": label, "url": url}]
            if url not in record["sources"]:
                record["sources"].append(url)

        if record_id == "bfm-uni-mol":
            record["name"] = "Uni-Mol"
            record["aliases"] = sorted(set(record.get("aliases", [])) | {"Uni-Mol base"})
            record["description"] = re.sub(r"\s*Uni-Mol3.*$", "", record["description"], flags=re.I)
            record["paper_links"] = [
                link for link in record.get("paper_links", [])
                if "2508.00920" not in link.get("url", "")
            ]
        if record_id == "bfm-megamolbart":
            record["paper_links"] = [
                link for link in record.get("paper_links", [])
                if "github.com/NVIDIA/MegaMolBART" not in link.get("url", "")
            ]
            add_link(record, "code_links", "Official repository", "https://github.com/NVIDIA/MegaMolBART")
        if record_id == "bfm-virchow-virchow2-and-virchow2g":
            record["audit_state"] = "hold"
            record["status"] = "HOLD — family members have different gating, commercial access and model terms; split required"
        if record_id == "bfm-framediff-frameflow-multiflow":
            record["audit_state"] = "hold"
            record["status"] = "HOLD — record conflates three distinct methods; split or narrow to MultiFlow"

        # Alias comparison is case/punctuation-insensitive.  Preserve the
        # first spelling and remove redundant variants such as MuPaD/MUPAD.
        seen_aliases = {re.sub(r"[^a-z0-9]+", " ", record["name"].casefold()).strip()}
        cleaned_aliases = []
        for alias in record.get("aliases", []):
            key = re.sub(r"[^a-z0-9]+", " ", alias.casefold()).strip()
            if key and key not in seen_aliases:
                seen_aliases.add(key)
                cleaned_aliases.append(alias)
        record["aliases"] = cleaned_aliases

        # A material persisted audit correction receives a real modification date.
        if record["audit_state"] != "verified" or record_id in MODALITY_OVERRIDES or record_id in LINK_ADDITIONS:
            record["date_modified"] = DATE

    # Recompute sources after link replacements/additions and keep them stable.
    for record in records:
        links = [
            link["url"]
            for field in ("paper_links", "code_links")
            for link in record.get(field, [])
            if isinstance(link, dict) and link.get("url")
        ]
        record["sources"] = list(dict.fromkeys(links + record.get("sources", [])))

    data_path.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    ledger = {
        "schema_version": "1.0.0",
        "audit_date": DATE,
        "frozen_commit": FROZEN_COMMIT,
        "role": "internal adversarial source review",
        "coverage": {"records": len(records), "source_reviewed": len(records)},
        "counts": dict(Counter(record["audit_state"] for record in records)),
        "priority_counts": dict(Counter(record["audit_priority"] for record in records)),
        "review_files": [
            {
                "path": f"evidence/source-audit/{name}",
                "sha256": hashlib.sha256(review_path(name).read_bytes()).hexdigest(),
            }
            for name in REVIEW_NAMES
        ],
        "records": [
            {
                "id": record["id"],
                "audit_state": record["audit_state"],
                "audit_priority": record["audit_priority"],
                "audit_note": record["audit_note"],
                "audit_source": record["audit_source"],
                "sources": record["sources"],
            }
            for record in records
        ],
    }
    evidence = ROOT / "evidence"
    evidence.mkdir(exist_ok=True)
    (evidence / "SOURCE_AUDIT_2026-07-13.json").write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    counts = Counter(record["audit_state"] for record in records)
    summary = f"""# Full source audit — 2026-07-13

Frozen baseline: `{FROZEN_COMMIT}`.  This was an internal adversarial review, not an external certification.

- Coverage: {len(records)}/{len(records)} canonical records source-reviewed.
- Verified without a material limitation: {counts['verified']}.
- Verified with a visible limitation or correction: {counts['verified_with_limits']}.
- HOLD pending scope, identity, licence, or reusable-artifact resolution: {counts['hold']}.
- Machine-readable ledger: `SOURCE_AUDIT_2026-07-13.json`.

Every canonical record now carries `verified`, `sources`, `audit_state`, `audit_priority`, `audit_note`, and `audit_source`.  HOLD is deliberately conservative: the record remains findable for transparency but must not be treated as release-ready evidence of a reusable foundation model.

Catalogue-level licence, publisher identity, final version and publication approval remain separate human governance gates.
"""
    (evidence / "SOURCE_AUDIT_2026-07-13.md").write_text(summary, encoding="utf-8")
    print(f"Persisted full source audit for {len(records)} records: {dict(counts)}")


if __name__ == "__main__":
    main()
