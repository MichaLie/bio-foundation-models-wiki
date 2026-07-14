#!/usr/bin/env python3
"""Build synchronized Markdown distributions from the canonical catalog."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from fair_metadata import load_resource_metadata


MODELS = json.loads(Path("models_final.json").read_text(encoding="utf-8"))
META = load_resource_metadata()
MOD_TITLE = {
    "dna": "DNA and Genome Models",
    "rna": "RNA Models",
    "protein": "Protein Sequence, Fitness, and Design Models",
    "complex": "Structure and Biomolecular Complex Models",
    "molecule": "Small-Molecule and Chemical Models",
    "singlecell": "Single-Cell, Omics, and Cellular Models",
    "spatial": "Spatial Omics and Pathology / Cell-Imaging Models",
    "multimodal": "Multimodal Bio-Language Models and Bioinformatics LLMs",
    "platform": "Platforms, Wrappers, and Model Hubs",
    "benchmark": "Benchmarks and Datasets",
}
MOD_ORDER = list(MOD_TITLE)
AUDIT_LABEL = {
    "verified": "Verified",
    "verified_with_limits": "Verified with limits",
    "hold": "HOLD",
}


def cell(value: object) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ").strip()


def links_md(record: dict) -> str:
    links = record.get("paper_links", []) + record.get("code_links", [])
    return " · ".join(f"[{cell(link['label'])}]({link['url']})" for link in links) or "—"


def access_rank(record: dict) -> tuple[int, int, str]:
    audit = {"hold": 2, "verified_with_limits": 1, "verified": 0}[record["audit_state"]]
    status = record.get("status", "").lower()
    access = 0 if "open code + weights" in status and "gated" not in status else 4
    if "paper" in status and "only" in status:
        access = 9
    return audit, access, record["name"].casefold()


counts = Counter(record["modality"] for record in MODELS)
audit_counts = Counter(record["audit_state"] for record in MODELS)
out = [
    "# Biological Foundation Models Wiki",
    "",
    f"Last evidence review: {META['modified']} · {len(MODELS)} entries across {len(MOD_ORDER)} categories.",
    "",
    "A researcher-facing index of foundation models and explicitly labelled platforms or benchmarks for biological sequences, molecules, structures, omics, cells, and tissue images. Presence is not a recommendation, proof of reuse rights, or evidence of clinical fitness.",
    "",
    f"Audit state: **{audit_counts['verified']} verified** and **{audit_counts['verified_with_limits']} verified with limits**. Every displayed row links to a dated source-review note in the canonical JSON. Unresolved candidates are excluded from this index and preserved in the repository's separate under-review register.",
    "",
    "Legend: ⭐ = canonical / widely used in its area; NC = non-commercial terms apply to at least one artifact or access route. Always inspect the exact code, weight, data, and service terms.",
    "",
    "## Contents",
    "",
]
for modality in MOD_ORDER:
    anchor = MOD_TITLE[modality].lower().replace(",", "").replace("/", "").replace(" ", "-")
    out.append(f"- [{MOD_TITLE[modality]}](#{anchor}) — {counts[modality]}")
out.append("")

for modality in MOD_ORDER:
    items = sorted((record for record in MODELS if record["modality"] == modality), key=access_rank)
    if not items:
        continue
    out.extend([
        f"## {MOD_TITLE[modality]}",
        "",
        "| Model | Year | Audit | Description | Input → Output | Access | Links | Main use cases |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for record in items:
        name = cell(record["name"])
        if record.get("canonical"):
            name += " ⭐"
        if record.get("noncommercial"):
            name += " · NC"
        audit = AUDIT_LABEL[record["audit_state"]]
        if record["audit_state"] != "verified":
            audit += f": {cell(record['audit_note'])}"
        out.append(
            "| {name} | {year} | {audit} | {description} | {io} | {status} | {links} | {uses} |".format(
                name=name,
                year=cell(record.get("year") or "—"),
                audit=cell(audit),
                description=cell(record["description"]),
                io=cell(record["io"]),
                status=cell(record["status"]),
                links=links_md(record),
                uses=cell(record["use_cases"]),
            )
        )
    out.append("")

out.extend([
    "## Evidence and reuse boundary",
    "",
    META["evidence_statement"],
    "",
    "The catalog records discovery and evidence. It does not grant rights to external artifacts. Code, weights, data and hosted services can have different terms; institutional, data-protection, ethics and domain review still apply.",
    "",
    "Catalog data, metadata, and original documentation are licensed under CC BY 4.0. Maintenance/build code is MIT licensed. External resources, logos, and trademarks retain their own terms.",
    "",
    "Machine-readable distributions: `models_final.json`, `schema.json`, and `metadata.jsonld`.",
    "",
])

payload = "\n".join(out)
Path("biological_foundation_models_wiki.md").write_text(payload, encoding="utf-8")
docs = Path("docs")
docs.mkdir(exist_ok=True)
(docs / "biological_foundation_models_wiki.md").write_text(payload, encoding="utf-8")
print(f"Wrote synchronized Markdown ({len(MODELS)} records)")
