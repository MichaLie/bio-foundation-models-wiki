#!/usr/bin/env python3
"""Regenerate the markdown wiki from models_final.json (all entries, fixes applied)."""
import json
from collections import Counter
M = json.load(open('models_final.json'))

MOD_TITLE = {
 'dna':'DNA and Genome Models','rna':'RNA Models',
 'protein':'Protein Sequence, Fitness, and Design Models',
 'complex':'Structure and Biomolecular Complex Models',
 'molecule':'Small-Molecule and Chemical Models',
 'singlecell':'Single-Cell, Omics, and Cellular Models',
 'spatial':'Spatial Omics and Pathology / Cell-Imaging Models',
 'multimodal':'Multimodal Bio-Language Models and Bioinformatics LLMs',
 'platform':'Platforms, Wrappers, and Model Hubs',
 'benchmark':'Benchmarks and Datasets',
}
MOD_ORDER = ['dna','rna','protein','complex','molecule','singlecell','spatial','multimodal','platform','benchmark']
ACCESS_ORDER = {'Open code + weights':0}

def links_md(rec):
    out=[]
    for l in rec.get('paper_links',[]): out.append(f"[{l['label']}]({l['url']})")
    for l in rec.get('code_links',[]): out.append(f"[{l['label']}]({l['url']})")
    return ' · '.join(out) if out else '—'

def cell(s): return (s or '').replace('|','\\|').replace('\n',' ').strip()

def acc_rank(rec):
    s=(rec.get('status','') or '').lower()
    if 'open code + weights' in s and 'gated' not in s and 'unclear' not in s and 'not released' not in s: return 0
    if 'paper/preprint only' in s: return 9
    return 4

def rows_for(mod):
    items=[r for r in M if r['modality']==mod]
    items.sort(key=lambda r:(acc_rank(r), 0 if r.get('canonical') else 1, r['name'].lower()))
    return items

today='2026-06-16'
out=[]
out.append('# Biological Foundation Models Wiki')
out.append('')
out.append(f'Last updated: {today}  ·  {len(M)} entries across {len(MOD_ORDER)} categories.')
out.append('')
out.append('A researcher-facing index of foundation models for biological sequences, molecules, structures, '
 'omics, cells, and tissue images. For each model: what it operates on, what goes in and comes out, how '
 'accessible it is today, and what it is good for. An interactive, filterable/sortable version is in '
 '`biological_foundation_models_wiki.html` (open in any browser, works offline).')
out.append('')
out.append('Legend in the **Model** column: ⭐ = canonical / most-used in its area. '
 'Access is a best-effort classification — **always verify the license before commercial use.**')
out.append('')
out.append('## Status / Access Key')
out.append('')
out.append('| Status | Meaning |')
out.append('| --- | --- |')
for s,m in [
 ('Open code + weights','Public implementation AND public pretrained weights. Verify license.'),
 ('Open code, gated/partial weights','Code public; weights need approval/login/terms, or only some sizes are open.'),
 ('Model hub','Weights primarily via Hugging Face, NVIDIA NGC/BioNeMo, CZI Virtual Cells, or similar.'),
 ('Web / API / commercial','Access mainly through a hosted server, API, or commercial platform.'),
 ('Platform / framework','A toolkit/serving layer that makes many models usable rather than a single model.'),
 ('Paper / preprint only','Paper found; no stable public implementation confirmed in the sweep.'),
]:
    out.append(f'| {s} | {m} |')
out.append('')
# counts
c=Counter(r['modality'] for r in M)
out.append('## Contents')
out.append('')
for mod in MOD_ORDER:
    out.append(f"- [{MOD_TITLE[mod]}](#{MOD_TITLE[mod].lower().replace(',','').replace('/','').replace('  ',' ').replace(' ','-')}) — {c.get(mod,0)}")
out.append('')

for mod in MOD_ORDER:
    items=rows_for(mod)
    if not items: continue
    out.append(f'## {MOD_TITLE[mod]}')
    out.append('')
    out.append('Sorted: open + canonical first, then by name.')
    out.append('')
    out.append('| Model | Year | Description | Input → Output | Access | Links | Main use cases |')
    out.append('| --- | --- | --- | --- | --- | --- | --- |')
    for r in items:
        name=cell(r['name'])
        if r.get('canonical'): name+=' ⭐'
        nc=' · *non-commercial*' if r.get('nc') else ''
        out.append('| {nm} | {yr} | {desc} | {io} | {acc}{nc} | {lnk} | {use} |'.format(
            nm=name, yr=cell(r.get('year','') or '—'), desc=cell(r['description']),
            io=cell(r['io']), acc=cell(r['status']), nc=nc, lnk=links_md(r), use=cell(r['use_cases'])))
    out.append('')

# operation notes (preserved/condensed) + gaps
out.append('## Practical Operation Notes')
out.append('')
out.append('**Sequence encoders (DNA/RNA/protein LMs)** are used in three modes: (1) embedding extraction — '
 'pass sequences, take token-level or pooled vectors; (2) zero-shot scoring — compare wild-type vs mutant '
 'log-likelihoods; (3) fine-tuning/adapters — attach task heads. Inputs are FASTA strings or tokenized '
 'k-mers/BPE; outputs are embeddings, logits, variant scores, or generated sequences.')
out.append('')
out.append('**Generative design models** (Evo, ESM3, ProGen, RFdiffusion, ProteinMPNN/LigandMPNN, GenMol, '
 'diffusion molecule/genome generators) need post-filtering: validity (frame, stop codons, chemical '
 'validity, structural plausibility), biological filters (novelty, off-target, immunogenicity, '
 'developability), and orthogonal/wet-lab validation before outputs are treated as candidates.')
out.append('')
out.append('**Single-cell / spatial models** are preprocessing-sensitive: confirm gene vocabulary and species '
 'assumptions, watch batch effects and training-atlas leakage, and compare against classical baselines '
 '(scVI/Harmony/CellTypist) for annotation, integration, perturbation, and GRN tasks.')
out.append('')
out.append('**Structure / complex models** are not interchangeable: protein-only → ESMFold/OpenFold/AlphaFold2; '
 'complexes with ligands/nucleic acids → AlphaFold3, Chai-1, Boltz, Protenix, HelixFold3, RoseTTAFold-AA; '
 'docking poses should be rescored (a good affinity is not a plausible pose).')
out.append('')
out.append('**Pathology / cell-imaging models** are tile or whole-slide encoders (ViT/DINOv2): input is an '
 'H&E or fluorescence image (tile or WSI), output is an embedding for downstream classification, retrieval, '
 'or weakly-supervised slide-level tasks. Most clinical-grade ones are gated (request access).')
out.append('')
out.append('## Remaining Gaps and Caveats')
out.append('')
out.append('- **License audit not done.** Access tags reflect code/weight availability, not license terms. '
 'Several "open" models are non-commercial (CC-BY-NC); these are flagged where known but not exhaustively.')
out.append('- **Structured specs are partial.** Parameter count, max context, and training-data scale live in '
 'the Description prose, not yet as filterable fields. Year is filled for ~86% of entries.')
out.append('- **Genuinely code-pending models** (mostly 2026 preprints): CellVQ, RegFormer, ScDiVa, '
 'scLinguist, scConcept, HybriDNA, TEDDY — listed as paper/preprint until code/weights appear.')
out.append('- **Fast-moving frontier.** New single-cell, pathology, and genome models appear weekly; treat this '
 'as a living document and re-sweep periodically.')
out.append('')

open('biological_foundation_models_wiki.md','w').write('\n'.join(out))
print('Wrote biological_foundation_models_wiki.md —', len(M), 'entries,', sum(1 for r in M if r.get("new")), 'new')
print('per section:', {MOD_TITLE[k][:18]:v for k,v in sorted(c.items(), key=lambda x:MOD_ORDER.index(x[0]))})
