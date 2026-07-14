#!/usr/bin/env python3
"""Move audited HOLD records out of the displayed catalog, losslessly and idempotently."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "models_final.json"
REGISTER = ROOT / "records_under_review.json"
EXPECTED_IDS = {
    "bfm-abodybuilder3",
    "bfm-atlas-rudolfv-successor",
    "bfm-bioreason",
    "bfm-chrombpnet",
    "bfm-deepsea",
    "bfm-drfold",
    "bfm-florabert",
    "bfm-framediff-frameflow-multiflow",
    "bfm-h-optimus-0-h-optimus-1",
    "bfm-mistral-dna",
    "bfm-mrna-fm-plantrna-fm",
    "bfm-neuralplexer-and-neuralplexer3",
    "bfm-openprotein-ai-poet-poet-2",
    "bfm-pearl",
    "bfm-protgps",
    "bfm-protriever",
    "bfm-saturn",
    "bfm-scdiva",
    "bfm-scprotein",
    "bfm-sctranslator",
    "bfm-tabula",
    "bfm-uni-mol-docking-v2",
    "bfm-virchow-virchow2-and-virchow2g",
    "bfm-xtrimogene",
    "bfm-chemberta-3",
    "bfm-genecompass",
    "bfm-hybridna",
    "bfm-genemamba",
    "bfm-scmmgpt",
    "bfm-plip-pathology-language-image-pretraining",
    "bfm-next-mol",
    "bfm-lingshu-cell",
}

ADDITIONAL_HOLD_IDS = {
    "bfm-chemberta-3",
    "bfm-genecompass",
    "bfm-hybridna",
    "bfm-genemamba",
    "bfm-scmmgpt",
    "bfm-plip-pathology-language-image-pretraining",
    "bfm-next-mol",
    "bfm-lingshu-cell",
}

REVIEW = {
    "bfm-mrna-fm-plantrna-fm": ("family_identity", "Split the family or verify each member with its own primary evidence, artifact locator, and licence."),
    "bfm-saturn": ("artifact", "Reconsider when an official reusable pretrained SATURN checkpoint is released and its terms are verified, or reclassify outside model scope."),
    "bfm-xtrimogene": ("artifact", "Reconsider when official reusable code or a checkpoint is released and verified."),
    "bfm-scprotein": ("scope", "Reconsider if broader reusable pretraining is evidenced or a written scope-policy revision explicitly includes this class."),
    "bfm-deepsea": ("scope", "Reconsider only under a written historical-exception policy with the original artifact correctly identified."),
    "bfm-chrombpnet": ("scope", "Reconsider if a written scope policy includes assay-specific predictors or broader reusable pretraining is evidenced."),
    "bfm-mistral-dna": ("multiple", "Reconsider when a primary source, authorized checkpoint, direct model card, and exact terms are all verified."),
    "bfm-florabert": ("scope", "Reconsider if broader reusable foundation-model scope is established by primary evidence."),
    "bfm-drfold": ("scope", "Reconsider only under a written structural-model exception or after reframing around an evidenced reusable pretrained component."),
    "bfm-framediff-frameflow-multiflow": ("family_identity", "Split FrameDiff, FrameFlow, and MultiFlow into independently evidenced records, or narrow this record to one system."),
    "bfm-protriever": ("artifact", "Reconsider when official executable code or reusable weights are released and verified."),
    "bfm-protgps": ("scope", "Reconsider if broader reusable foundation-model scope is established or a written task-specific exception is adopted."),
    "bfm-neuralplexer-and-neuralplexer3": ("family_identity", "Split NeuralPLexer v1 and NP3 and verify each version's implementation, weights, and terms."),
    "bfm-uni-mol-docking-v2": ("scope", "Reconsider only under a written structural/docking exception or with evidence of broader reusable scope."),
    "bfm-abodybuilder3": ("scope", "Reconsider only under a written structural-model exception or with evidence of broader reusable scope."),
    "bfm-scdiva": ("artifact", "Reconsider when official reusable code or a checkpoint is released and verified."),
    "bfm-tabula": ("artifact", "Reconsider when an official reusable pretrained checkpoint is released and its terms are verified."),
    "bfm-virchow-virchow2-and-virchow2g": ("family_identity", "Split the family or encode member-specific artifacts, access routes, and terms with primary evidence."),
    "bfm-h-optimus-0-h-optimus-1": ("family_identity", "Verify and link each model card and encode the family members' distinct access and reuse terms."),
    "bfm-atlas-rudolfv-successor": ("artifact", "Reconsider when a current official public artifact or endpoint and its exact access terms are verified."),
    "bfm-bioreason": ("artifact", "Reconsider when the promised official checkpoints are released and their terms are verified."),
    "bfm-openprotein-ai-poet-poet-2": ("duplication", "Narrow to the platform or merge with the PoET-2 record while documenting the stable-ID disposition."),
    "bfm-pearl": ("artifact", "Reconsider when an official reusable model artifact or public endpoint and its terms are verified."),
    "bfm-sctranslator": ("multiple", "Reconsider when scope eligibility and explicit code/checkpoint reuse terms are both resolved."),
    "bfm-chemberta-3": ("multiple", "Reconsider after platform scope and explicit reuse terms for the released framework/model artifacts are verified."),
    "bfm-genecompass": ("terms", "Reconsider when explicit code and checkpoint reuse terms are confirmed from an official source."),
    "bfm-hybridna": ("artifact", "Reconsider when a provenance-confirmed official reusable model artifact is released and verified."),
    "bfm-genemamba": ("terms", "Reconsider when explicit reuse terms for the official code and weights are confirmed."),
    "bfm-scmmgpt": ("multiple", "Reconsider when official reusable weights and explicit reuse terms are both confirmed."),
    "bfm-plip-pathology-language-image-pretraining": ("terms", "Reconsider when explicit reuse terms for the official code and weights are confirmed."),
    "bfm-next-mol": ("terms", "Reconsider when explicit reuse terms for the official code and checkpoints are confirmed."),
    "bfm-lingshu-cell": ("artifact", "Reconsider when the official collection contains a released reusable model artifact with verified terms."),
}


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    records = json.loads(CATALOG.read_text(encoding="utf-8"))
    held = [
        record for record in records
        if record.get("audit_state") == "hold" or record.get("id") in ADDITIONAL_HOLD_IDS
    ]
    existing_entries = []
    if REGISTER.is_file():
        existing = json.loads(REGISTER.read_text(encoding="utf-8"))
        existing_entries = existing.get("entries", [])
    existing_ids = {entry["record"]["id"] for entry in existing_entries}

    if not held:
        if not REGISTER.is_file():
            raise SystemExit("No HOLD records found and the under-review register is missing")
        if existing_ids != EXPECTED_IDS or existing.get("record_count") != 32:
            raise SystemExit("Existing under-review register does not match the audited 32-record set")
        print("Release-policy migration already applied: 345 public + 32 under review")
        return 0

    held_ids = {record["id"] for record in held}
    if held_ids & existing_ids:
        raise SystemExit("A HOLD record appears in both the displayed catalog and existing register")
    if held_ids | existing_ids != EXPECTED_IDS:
        raise SystemExit(
            f"Refusing unexpected HOLD set: expected 32 audited IDs, "
            f"found {len(held_ids | existing_ids)}"
        )

    entries = list(existing_entries)
    for record in held:
        record["audit_state"] = "hold"
        if record["id"] == "bfm-hybridna":
            record["audit_priority"] = "P2"
        reason_code, reconsider_when = REVIEW[record["id"]]
        entries.append({
            "record": record,
            "review": {
                "status": "under_review",
                "hold_since": "2026-07-13",
                "reason_code": reason_code,
                "reason": record["audit_note"],
                "source": record["audit_source"],
                "reconsider_when": reconsider_when,
            },
        })

    public_records = [record for record in records if record.get("id") not in held_ids]
    register = {
        "$schema": "records_under_review.schema.json",
        "schema_version": "1.0.0",
        "title": "Biological Foundation Models — records under review",
        "description": "Audited candidates excluded from the displayed canonical index until their scope, artifact, identity, duplication, or reuse-term issue is resolved.",
        "status": "editorial-hold",
        "date_modified": "2026-07-14",
        "record_count": len(entries),
        "policy": {
            "displayed_in_index": False,
            "stable_ids_reserved": True,
            "promotion_rule": "A record may move into models_final.json only after the stated reconsideration condition is met, primary evidence is refreshed, and the full maintenance gate passes.",
        },
        "entries": entries,
    }

    write_json(CATALOG, public_records)
    write_json(REGISTER, register)
    print(f"Release-policy migration applied: {len(public_records)} public + {len(entries)} under review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
