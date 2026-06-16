#!/usr/bin/env python3
"""Merge existing + new models, apply audit fixes, classify modality, derive fields."""
import json, re

existing = json.load(open('existing_models.json'))
res = json.load(open('workflow_result.json'))
newraw = res['confirmedNew']

# ---------- helpers ----------
def url_label(u, kind='paper'):
    d = u.lower()
    table = [
        ('biorxiv','bioRxiv'),('arxiv','arXiv'),('nature.com','Nature'),('science.org','Science'),
        ('pnas.org','PNAS'),('aclanthology','ACL'),('openreview','OpenReview'),('academic.oup.com','Oxford Acad.'),
        ('pubs.rsc','RSC'),('pmc.ncbi','PMC'),('proceedings.mlr','PMLR'),('proceedings.neurips','NeurIPS'),
        ('journals.plos','PLOS'),('link.springer','Springer'),('neurips.cc','NeurIPS'),('chemrxiv','ChemRxiv'),
        ('github.com','GitHub'),('huggingface.co','Hugging Face'),('zenodo','Zenodo'),
        ('virtualcellmodels','CZI VCP'),('docs.nvidia','NVIDIA'),('genbio.ai','GenBio'),
    ]
    for k,lab in table:
        if k in d:
            return lab
    if kind=='code':
        return 'Code'
    return 'Paper'

def to_links(url, kind='paper'):
    if not url: return []
    url = url.strip()
    if not url.lower().startswith('http'):
        return []
    return [{'label': url_label(url, kind), 'url': url}]

def parse_year(rec):
    if rec.get('year'):
        m = re.search(r'(19|20)\d\d', str(rec['year']))
        if m: return m.group(0)
    blob = ' '.join(l['url'] for l in rec.get('paper_links',[])) + ' ' + ' '.join(l['url'] for l in rec.get('code_links',[]))
    # biorxiv / medrxiv 10.1101/2024.xx
    m = re.search(r'10\.1101/(20\d\d)\.', blob)
    if m: return m.group(1)
    # arxiv abs/2306.xxxx  -> 23 -> 2023
    m = re.search(r'arxiv\.org/(?:abs|pdf)/(\d{2})(\d{2})\.', blob)
    if m: return '20'+m.group(1)
    # nature/springer s415xx-024-  -> 024 -> 2024 ; s415xx-22 styles
    m = re.search(r's\d{5}-0?(2\d)-', blob)
    if m: return '20'+m.group(1)
    # nmeth.3547 (2015 era) -> skip
    # PMLR v202 -> 2023, v235 -> 2024, v139->2021 ... approximate map
    m = re.search(r'mlr\.press/v(\d+)/', blob)
    if m:
        vol=int(m.group(1)); volmap={119:'2020',139:'2021',162:'2022',202:'2023',235:'2024',267:'2025'}
        if vol in volmap: return volmap[vol]
    return ''

def noncommercial(status):
    s=(status or '').lower()
    return any(k in s for k in ['non-commercial','noncommercial','cc-by-nc','cc by-nc','nc-sa','nc 4.0','research use','academic'])

# ---------- audit fixes to existing ----------
FIXES = {
 'GENA-LM': {'paper_links':[{'label':'bioRxiv','url':'https://www.biorxiv.org/content/10.1101/2023.06.12.544594'},
                            {'label':'NAR','url':'https://academic.oup.com/nar/article/53/2/gkae1310/7954523'}]},
 'RNA-MSM / RNA-MFM': {'name':'RNA-MSM',
    'paper_links':[{'label':'NAR','url':'https://academic.oup.com/nar/article/52/1/e3/7369930'}],
    'code_links':[{'label':'GitHub','url':'https://github.com/yikunpku/RNA-MSM'}],
    'status':'Open code + weights'},
 'GenerRNA': {'paper_links':[{'label':'bioRxiv','url':'https://www.biorxiv.org/content/10.1101/2024.02.01.578496v1'},
                             {'label':'PLOS One','url':'https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0310814'}],
    'code_links':[{'label':'GitHub','url':'https://github.com/pfnet-research/GenerRNA'}],
    'status':'Open code + weights'},
 'AIDO.RNA': {'paper_links':[{'label':'bioRxiv','url':'https://www.biorxiv.org/content/10.1101/2024.11.28.625345'}],
    'code_links':[{'label':'ModelGenerator','url':'https://github.com/genbio-ai/modelgenerator'},
                  {'label':'Hugging Face','url':'https://huggingface.co/genbio-ai/AIDO.RNA-1.6B'}],
    'status':'Open code + weights'},
 'UNI-RNA': {'code_links':[{'label':'GitHub','url':'https://github.com/ComDec/unirna_tf'}],
    'status':'Inference code public; weights via Google Drive, CC BY-NC (non-commercial)'},
 'ESM3': {'code_links':[{'label':'EvolutionaryScale ESM','url':'https://github.com/evolutionaryscale/esm'},
                        {'label':'EvolutionaryScale','url':'https://www.evolutionaryscale.ai/'}]},
 'ESM-C / ESM Cambrian': {'code_links':[{'label':'EvolutionaryScale ESM','url':'https://github.com/evolutionaryscale/esm'},
                        {'label':'Hugging Face','url':'https://huggingface.co/EvolutionaryScale'}]},
 'DPLM': {'code_links':[{'label':'GitHub','url':'https://github.com/bytedance/dplm'}],
    'status':'Open code + weights'},
 'ProGen / ProGen2': {'paper_links':[{'label':'ProGen (Nat Biotech)','url':'https://www.nature.com/articles/s41587-022-01618-2'},
                                     {'label':'ProGen2 (OpenReview)','url':'https://openreview.net/forum?id=ZOn4HXehSJ6'}]},
 'ESM-1b / ESM-1v': {'paper_links':[{'label':'ESM-1b (PNAS)','url':'https://www.pnas.org/doi/10.1073/pnas.2016239118'},
                                    {'label':'ESM-1v (bioRxiv)','url':'https://www.biorxiv.org/content/10.1101/2021.07.09.450648'}]},
 'Boltz-1 / Boltz-2': {'paper_links':[{'label':'Boltz-1 (PMC)','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC11601547/'},
                                      {'label':'Boltz-2 (bioRxiv)','url':'https://www.biorxiv.org/content/10.1101/2025.06.14.659707v1'}]},
 'MolE': {'status':'Open code, weights not released (CC-BY-NC)'},
 'MegaMolBART': {'code_links':[{'label':'GitHub','url':'https://github.com/NVIDIA/MegaMolBART'},
                               {'label':'BioNeMo Framework','url':'https://github.com/NVIDIA/bionemo-framework'}]},
 'MolMIM': {'code_links':[{'label':'BioNeMo Framework','url':'https://github.com/NVIDIA/bionemo-framework'}]},
 'scPROTEIN': {'code_links':[{'label':'GitHub','url':'https://github.com/TencentAILabHealthcare/scPROTEIN'}],
    'status':'Open code + weights'},
 'scMulan': {'code_links':[{'label':'GitHub','url':'https://github.com/SuperBianC/scMulan'},
                           {'label':'Hugging Face','url':'https://huggingface.co/deeplife/scmulan_model'}],
    'status':'Open code + weights'},
 'scCello': {'code_links':[{'label':'GitHub','url':'https://github.com/DeepGraphLearning/scCello'},
                           {'label':'Hugging Face','url':'https://huggingface.co/katarinayuan/scCello-zeroshot'}],
    'status':'Open code + weights'},
 'ChatCell': {'code_links':[{'label':'GitHub','url':'https://github.com/zjunlp/ChatCell'},
                            {'label':'Hugging Face','url':'https://huggingface.co/zjunlp/chatcell-large'}],
    'status':'Open code + weights'},
 'BioT5': {'paper_links':[{'label':'EMNLP 2023','url':'https://aclanthology.org/2023.emnlp-main.70/'}]},
 'ProtST': {'paper_links':[{'label':'ICML 2023 (PMLR)','url':'https://proceedings.mlr.press/v202/xu23t.html'}]},
 'ProteinDT': {'paper_links':[{'label':'Nat Mach Intell','url':'https://www.nature.com/articles/s42256-025-01011-z'},
                              {'label':'arXiv','url':'https://arxiv.org/abs/2302.04611'}]},
 'ProTrek': {'code_links':[{'label':'GitHub','url':'https://github.com/westlake-repl/ProTrek'},
                           {'label':'Hugging Face','url':'https://huggingface.co/westlake-repl/ProTrek_650M'}],
    'status':'Open code + weights'},
}

CANONICAL = {
 'ESM-2','ESMFold','ESM-1b / ESM-1v','ESM3','ESM-C / ESM Cambrian','AlphaFold 3','AlphaFold2','ProteinMPNN','RFdiffusion',
 'Enformer','Nucleotide Transformer','Evo 2','AlphaGenome','Borzoi','HyenaDNA','Caduceus','RNA-FM','RiNALMo',
 'Geneformer','scGPT','scFoundation','UCE','scPRINT','SCimilarity','Boltz-1 / Boltz-2','Chai-1','RoseTTAFold All-Atom',
 'ProGen / ProGen2','MoLFormer','Uni-Mol','ChemBERTa / ChemBERTa-2','UNI / UNI2-h','Virchow / Virchow2 (and Virchow2G)',
 'STATE (Arc Institute)','OpenFold','AlphaFold 2/3','Protenix','LigandMPNN','SaProt',
}

fixed_count=0
for e in existing:
    e['new']=False
    if e['name'] in FIXES:
        for k,v in FIXES[e['name']].items():
            e[k]=v
        fixed_count+=1
    e['year']=parse_year(e)
    e['canonical']= e['name'] in CANONICAL
    e['noncommercial']= noncommercial(e.get('status',''))

print(f"Applied {fixed_count} audit fixes to existing (of {len(FIXES)} defined)")

# ---------- dedupe new self-duplicates ----------
def nkey(n): return re.sub(r'[^a-z0-9]','', re.sub(r'\(.*?\)','',n.lower()))
seen=set(); newdedup=[]
for m in newraw:
    k=nkey(m['name'])
    if k in seen:
        continue
    seen.add(k); newdedup.append(m)
print(f"New: {len(newraw)} -> {len(newdedup)} after self-dedupe")

# ---------- modality classification for new ----------
BENCH = ['bend','genomic benchmarks','open problems','proteinbench','proteingym',
         'therapeutics data commons','sceval','mol-instructions']
PLATFORM = ['ginkgo','neurosnap','tamarind','latch bio','openprotein.ai']
SPATIAL = ['uni / uni2','uni2-h','virchow','conch','h-optimus','prov-gigapath','phikon','hibou',
           'midnight','musk','mstar','titan','prism','chief','gpfm','atlas (rudolf','plip',
           'openphenom','subcell','cell-dino','cell painting cnn','nicheformer','scgpt-spatial']
SINGLECELL = ['c2s-scale','captain','cellvq','cellwhisperer','genemamba','genept','langcell',
              'pulsar','regformer','sc-mamba2','scchat','scconcept','scdiva','scelmo','sclinguist',
              'sclong','scmmgpt','scprint-2','sctab','stack (arc','state (arc','tabula','tahoe-x1','teddy']
DNA = ['alphagenome','borzoi','sei','deepsea','chrombpnet','gpn (','generator','grover (dna',
       'agront','florabert','dnagpt','megadna','glm (','mistral-dna','plantcaduceus','specieslm',
       'genomeocean','omnina','hybridna','janusdna','segmentnt','orca','decima','scooby','get (general']
RNA = ['birna-bert','mrnabert','codonbert','helix-mrna','orthrus','rnaernie','rnagenesis','omnigenome',
       'lamar','utr-lm','rhofold','drfold','trrosettarna']
COMPLEX = ['alphafold2','alphafold-multimer','rosettafold2','rosettafoldna','openfold3','protenix',
           'helixfold3','neuralplexer','umol','omegafold','diffdock-l','uni-mol docking','flowdock']
MOLECULE = ['chemfm','chemformer','genmol','megalodon','kpgt','molbert','molclr','mole-bert','molgen',
            'molgpt','safe-gpt','mist','smi-ssed','smi-ted','smiles-bert','cddd','uni-mol2']
MULTIMODAL = ['biomedgpt','bioreason','chatnt','instructprotein','prot2text','prott3','txgemma']
# everything else (antibody, design, plm) -> protein

def classify(m):
    n=m['name'].lower()
    def hit(lst): return any(k in n for k in lst)
    if hit(BENCH): return 'benchmark'
    if hit(PLATFORM): return 'platform'
    if hit(SPATIAL): return 'spatial'
    if hit(SINGLECELL): return 'singlecell'
    if hit(DNA): return 'dna'
    if hit(RNA): return 'rna'
    if hit(COMPLEX): return 'complex'
    if hit(MOLECULE): return 'molecule'
    if hit(MULTIMODAL): return 'multimodal'
    return 'protein'

NEW_CANON={'alphagenome','borzoi','uni / uni2-h','virchow','state (arc','protenix','ligandmpnn','saprot','nicheformer'}
out_new=[]
unknown=[]
for m in newdedup:
    mod=classify(m)
    rec={
        'modality':mod,
        'name':m['name'],
        'description':m.get('description',''),
        'io':m.get('io',''),
        'status':m.get('access',''),
        'use_cases':m.get('use_cases',''),
        'year':'',
        'paper_links':to_links(m.get('paper',''),'paper'),
        'code_links':to_links(m.get('code',''),'code'),
        'new':True,
        'canonical': any(k in m['name'].lower() for k in NEW_CANON),
        'noncommercial': noncommercial(m.get('access','')),
    }
    rec['year']=parse_year({'year':m.get('year',''), 'paper_links':rec['paper_links'], 'code_links':rec['code_links']})
    out_new.append(rec)

# merge
allm = existing + out_new
json.dump(allm, open('models_final.json','w'), indent=1, ensure_ascii=False)

from collections import Counter
print("\nTotal merged:", len(allm))
print("Existing:", len(existing), " New:", len(out_new))
print("\nModality distribution (new only):", dict(Counter(r['modality'] for r in out_new)))
print("Modality distribution (all):", dict(Counter(r['modality'] for r in allm)))
print("Year known:", sum(1 for r in allm if r['year']), "/", len(allm))
print("Canonical:", sum(1 for r in allm if r['canonical']))
print("Non-commercial flagged:", sum(1 for r in allm if r['noncommercial']))
# show new models with no links (quality check)
nolink=[r['name'] for r in out_new if not r['paper_links'] and not r['code_links']]
print("\nNew models with NO links (check):", nolink)
