#!/usr/bin/env python3
"""Build a single self-contained interactive HTML index from a models JSON file.
Usage: python3 build_html.py [models_final.json] [out.html]
"""
import json, sys, html, datetime
from collections import Counter

SRC = sys.argv[1] if len(sys.argv) > 1 else 'models_final.json'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'biological_foundation_models_wiki.html'
models = json.load(open(SRC))

MOD_LABELS = {
    'dna':'DNA / Genome','rna':'RNA','protein':'Protein','complex':'Structure / Complex',
    'molecule':'Small molecule','singlecell':'Single-cell / Omics','spatial':'Spatial / Pathology',
    'multimodal':'Multimodal / Bio-LLM','platform':'Platform / Hub','benchmark':'Benchmark / Dataset',
}
MOD_ORDER = ['dna','rna','protein','complex','molecule','singlecell','spatial','multimodal','platform','benchmark']
ACCESS_LABELS = {'open':'Open code + weights','partial':'Open code, gated/partial weights','hub':'Model hub',
    'api':'Web / API / commercial','paper':'Paper / preprint only','platform':'Platform / framework'}
ACCESS_SHORT = {'open':'Open','partial':'Partial','hub':'Hub','api':'API/Web','paper':'Paper-only','platform':'Platform'}
ACCESS_ORDER = ['open','partial','hub','api','platform','paper']

def access_cat(status, modality):
    s=(status or '').lower()
    if 'paper/preprint only' in s or s.strip()=='paper/preprint only': return 'paper'
    if modality=='platform' or 'framework' in s or 'toolkit' in s or s.strip().startswith('web/cli'): return 'platform'
    if 'open code + weights' in s and not any(k in s for k in ['gated','unclear','fragmented','selected','not released','weights not']): return 'open'
    if any(k in s for k in ['gated','unclear','fragmented','selected','smaller models','vary by release','not released','weights not','via google drive','login']): return 'partial'
    if 'model hub' in s or 'bionemo' in s or 'ngc' in s: return 'hub'
    if any(k in s for k in ['api','commercial','web','server']): return 'api'
    if 'open code' in s: return 'partial'
    return 'partial'

norm=[]
for m in models:
    cat = access_cat(m.get('status',''), m.get('modality',''))
    code_links=m.get('code_links',[]); paper_links=m.get('paper_links',[])
    s=(m.get('status','') or '').lower()
    has_weights = cat in ('open','hub') or ('weight' in s and cat!='paper' and 'not released' not in s and 'not yet' not in s)
    rec={
        'name':m.get('name',''),'modality':m.get('modality',''),'description':m.get('description',''),
        'io':m.get('io',''),'status':m.get('status',''),'access':cat,'year':str(m.get('year','') or ''),
        'use_cases':m.get('use_cases',''),'paper_links':paper_links,'code_links':code_links,
        'new':bool(m.get('new',False)),'canonical':bool(m.get('canonical',False)),
        'nc':bool(m.get('noncommercial',False)),'hasCode':len(code_links)>0,'hasWeights':bool(has_weights),
    }
    rec['_s']=' '.join([rec['name'],rec['description'],rec['use_cases'],rec['io'],rec['status'],MOD_LABELS.get(rec['modality'],'')]).lower()
    norm.append(rec)

def sort_key(m):
    return (MOD_ORDER.index(m['modality']) if m['modality'] in MOD_ORDER else 99,
            ACCESS_ORDER.index(m['access']) if m['access'] in ACCESS_ORDER else 99,
            0 if m['canonical'] else 1, m['name'].lower())
norm.sort(key=sort_key)

today=datetime.date.today().isoformat()
total=len(norm)
n_new=sum(1 for m in norm if m['new'])
n_cats=len(set(m['modality'] for m in norm))
ac=Counter(m['access'] for m in norm)
n_open=ac.get('open',0); n_gated=ac.get('partial',0)+ac.get('hub',0); n_api=ac.get('api',0)

QUICK=[
 ("Protein embeddings","ESM-C, ESM-2, ProtTrans, Ankh, SaProt, AMPLIFY"),
 ("Protein variant effect / fitness","ESM-1v, Tranception, EVE, PoET, ProteinNPT, Protriever"),
 ("Protein structure from sequence","ESMFold, AlphaFold2, OpenFold, OmegaFold"),
 ("Protein / binder design","ProteinMPNN, LigandMPNN, RFdiffusion, RFdiffusion2, Chai-2"),
 ("De novo protein generation","ESM3, ProGen2, Chroma, DPLM, EvoDiff, Genie 2"),
 ("Antibody modeling","IgLM, AntiBERTy, AbLang, BALM, p-IgGen, IgFold, AntiFold"),
 ("Long genomic DNA modeling","HyenaDNA, Caduceus, Nucleotide Transformer, Evo 2"),
 ("Regulatory genomics / variant effect","Enformer, Borzoi, AlphaGenome, Sei, Evo 2, GPN-MSA"),
 ("RNA sequence / function","RNA-FM, RiNALMo, ERNIE-RNA, Orthrus, UTR-LM"),
 ("RNA structure (3D)","RhoFold+, trRosettaRNA, DRfold, RoseTTAFoldNA"),
 ("Single-cell embeddings","Geneformer, scGPT, scFoundation, UCE, scPRINT, SCimilarity"),
 ("Perturbation / virtual cell","scGPT, STATE, Tahoe-x1, scFoundation"),
 ("Pathology / histology (WSI)","UNI, Virchow, CONCH, H-optimus, Prov-GigaPath, TITAN"),
 ("Spatial transcriptomics","Nicheformer, scGPT-spatial"),
 ("Cell imaging / morphology","OpenPhenom, SubCell, Cell-DINO"),
 ("Molecular property / embeddings","MoLFormer, Uni-Mol, ChemBERTa, MolCLR, Uni-Mol2"),
 ("Molecular generation","GenMol, SAFE-GPT, MolGPT, MegaMolBART, Megalodon"),
 ("Biomolecular complexes","AlphaFold 3, Chai-1, Boltz, Protenix, RoseTTAFold-AA, HelixFold3"),
 ("Protein-ligand docking","DiffDock, DiffDock-L, Uni-Mol Docking V2, Umol, FlowDock"),
 ("Unified access layer","Helical, CZI Virtual Cells, NVIDIA BioNeMo, AIDO"),
 ("Benchmarks to evaluate on","ProteinGym, BEND, scEval, TDC, Open Problems"),
]
quick_rows="\n".join(f'<tr><td>{html.escape(n)}</td><td><button class="qcbtn" data-q="{html.escape(v.split(",")[0].strip())}">filter</button> {html.escape(v)}</td></tr>' for n,v in QUICK)

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Biological Foundation Models — Researcher Index</title>
<style>
:root{
 --bg:#f6f7f9;--panel:#fff;--ink:#1a1d24;--muted:#5b6472;--line:#e3e7ee;--accent:#2563eb;
 --chip:#eef1f6;--chipline:#dce1ea;--rowhover:#f0f4fb;--detail:#f8fafc;
 --open:#0f7a3d;--openbg:#e3f6ec;--partial:#9a5b00;--partialbg:#fbeed5;--hub:#1763a6;--hubbg:#e1eefb;
 --api:#6d28d9;--apibg:#efe7fc;--platform:#0e7490;--platformbg:#dcf2f6;--paper:#a13a3a;--paperbg:#fbe6e6;
 --new:#d6336c;--star:#e8a800;
}
html[data-theme="dark"]{
 --bg:#0f1218;--panel:#161b22;--ink:#e6e9ef;--muted:#9aa3b2;--line:#262c36;--accent:#5b8cff;
 --chip:#1d232d;--chipline:#2b3340;--rowhover:#1b2330;--detail:#12161d;
 --open:#5fd99a;--openbg:#10331f;--partial:#f0b95c;--partialbg:#33260f;--hub:#6cb6f0;--hubbg:#0e273b;
 --api:#b794f4;--apibg:#241039;--platform:#5fd0de;--platformbg:#06303a;--paper:#f08a8a;--paperbg:#3a1414;
 --new:#f06595;--star:#f2c200;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:13.5px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1340px;margin:0 auto;padding:16px 18px 90px}
header.top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
h1{font-size:21px;margin:0 0 4px}
.sub{color:var(--muted);font-size:12.5px;max-width:820px}
.toolbtn{background:var(--panel);border:1px solid var(--line);color:var(--ink);border-radius:8px;padding:7px 12px;cursor:pointer;font-size:13px}
.stats{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 2px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:7px 12px}
.stat b{font-size:17px}.stat span{color:var(--muted);font-size:11.5px;display:block}
.controls{position:sticky;top:0;z-index:30;background:var(--bg);padding:10px 0 8px;border-bottom:1px solid var(--line);margin-bottom:4px}
.searchrow{display:flex;gap:9px;flex-wrap:wrap;align-items:center}
#q{flex:1;min-width:240px;padding:9px 12px;border:1px solid var(--line);border-radius:10px;background:var(--panel);color:var(--ink);font-size:14px}
.toolbtn.sm{padding:8px 11px}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px;align-items:center}
.chips .lbl{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-right:2px}
.chip{background:var(--chip);border:1px solid var(--chipline);color:var(--ink);border-radius:999px;padding:4px 10px;font-size:12px;cursor:pointer;user-select:none}
.chip.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.chip .c{opacity:.6;margin-left:5px;font-size:10.5px}
.chip.tog.on{background:var(--open);border-color:var(--open)}
.countpill{font-size:12px;color:var(--muted);margin:9px 0 0}
details.qc{margin:12px 0;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:4px 14px}
details.qc summary{cursor:pointer;font-weight:600;padding:7px 0}
table.qct{width:100%;border-collapse:collapse;font-size:12.5px}
table.qct td{padding:5px 8px;border-top:1px solid var(--line);vertical-align:top}
table.qct td:first-child{font-weight:600;white-space:nowrap;width:30%}
.qcbtn,.qcclear{background:var(--chip);border:1px solid var(--chipline);border-radius:6px;color:var(--accent);font-size:11px;padding:1px 7px;cursor:pointer;margin-right:6px}
table.main{width:100%;border-collapse:collapse;font-size:13px}
table.main thead th{position:sticky;top:96px;background:var(--bg);text-align:left;padding:8px 8px;border-bottom:2px solid var(--line);font-size:11.5px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);cursor:pointer;white-space:nowrap;z-index:10}
table.main thead th.nosort{cursor:default}
table.main tbody td{padding:8px 8px;border-bottom:1px solid var(--line);vertical-align:top}
tr.row{cursor:pointer}
tr.row:hover{background:var(--rowhover)}
.exp{color:var(--muted);width:16px;display:inline-block;transition:transform .12s}
tr.open .exp{transform:rotate(90deg)}
.nm{font-weight:700}
.star{color:var(--star);margin-left:3px}
.tag{font-size:10px;padding:1px 6px;border-radius:999px;font-weight:700;vertical-align:middle;margin-left:5px}
.tag-new{color:#fff;background:var(--new)}
.tag-nc{color:var(--paper);background:var(--paperbg);margin-left:4px}
.badge{font-size:11px;padding:2px 9px;border-radius:999px;font-weight:600;white-space:nowrap;display:inline-block}
.b-open{color:var(--open);background:var(--openbg)}.b-partial{color:var(--partial);background:var(--partialbg)}
.b-hub{color:var(--hub);background:var(--hubbg)}.b-api{color:var(--api);background:var(--apibg)}
.b-paper{color:var(--paper);background:var(--paperbg)}.b-platform{color:var(--platform);background:var(--platformbg)}
.b-mod{color:var(--muted);background:var(--chip);font-weight:600}
td.io,td.uses{max-width:300px;color:var(--ink)}
td.io .t,td.uses .t{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
td.yr{color:var(--muted);white-space:nowrap}
td.lnk a{font-size:14px;margin-right:5px;text-decoration:none}
tr.detailrow td{background:var(--detail);padding:0 8px 14px 30px}
.detail h4{margin:10px 0 4px;font-size:12.5px}
.detail .kv{font-size:12.5px;margin:3px 0}
.detail .kv b{color:var(--muted);font-weight:600}
.detail .links a{display:inline-block;font-size:12px;border:1px solid var(--line);padding:3px 9px;border-radius:7px;margin:3px 6px 0 0;background:var(--panel)}
.grouprow td{background:var(--bg);font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);font-weight:700;padding:14px 8px 5px;border-bottom:1px solid var(--line)}
.empty{text-align:center;color:var(--muted);padding:50px 0}
footer{margin-top:30px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:14px}
.legend{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px;font-size:11.5px;color:var(--muted)}
</style></head>
<body><div class="wrap">
<header class="top"><div>
<h1>Biological Foundation Models — Researcher Index</h1>
<div class="sub">Filterable index of foundation models for biological sequences, molecules, structures, omics, cells, and tissue images.
Answer fast: <b>what object?</b> · <b>in → out?</b> · <b>accessible today?</b> · <b>what for?</b>
Updated __TODAY__. Access tags are best-effort — <b>always verify the license</b> before commercial use. Click any row for detail.</div>
</div><button class="toolbtn" id="theme">🌓 Theme</button></header>

<div class="stats">
<div class="stat"><b>__TOTAL__</b><span>models &amp; resources</span></div>
<div class="stat"><b>__NOPEN__</b><span>open code + weights</span></div>
<div class="stat"><b>__NGATED__</b><span>gated / hub weights</span></div>
<div class="stat"><b>__NAPI__</b><span>web / API only</span></div>
<div class="stat"><b>__NCATS__</b><span>categories</span></div>
</div>

<div class="controls">
 <div class="searchrow">
  <input id="q" type="search" placeholder="Search name, description, use case, in/out…  space = AND  (e.g. variant antibody, single-cell perturbation)">
  <button class="toolbtn sm" id="reset">Reset</button>
 </div>
 <div class="chips" id="modchips"><span class="lbl">Modality</span></div>
 <div class="chips" id="accchips"><span class="lbl">Access</span></div>
 <div class="chips" id="togchips"><span class="lbl">Only</span></div>
 <div class="countpill" id="count"></div>
</div>

<details class="qc"><summary>⚡ Quick chooser — pick by task</summary>
<table class="qct"><tbody>__QUICK__</tbody></table></details>

<table class="main"><thead><tr>
<th class="nosort"></th>
<th data-k="name">Name</th><th data-k="modality">Modality</th><th data-k="access">Access</th>
<th data-k="year">Year</th><th class="nosort">Input → Output</th><th class="nosort">Use cases</th><th class="nosort">Links</th>
</tr></thead><tbody id="tb"></tbody></table>
<div id="empty"></div>

<footer>
<b>__TOTAL__</b> models &amp; resources · ⭐ = canonical / most-used in its area · <span class="tag tag-nc">NC</span> = non-commercial license noted.
A discovery index — always confirm each repository's license and weight availability before use.
<div class="legend">
<span><span class="badge b-open">Open</span> code + weights public</span>
<span><span class="badge b-partial">Partial</span> gated / partial weights</span>
<span><span class="badge b-hub">Hub</span> weights via HF/NGC/CZI</span>
<span><span class="badge b-api">API/Web</span> hosted / commercial</span>
<span><span class="badge b-platform">Platform</span> framework / serving</span>
<span><span class="badge b-paper">Paper-only</span> no confirmed code</span>
</div></footer>
</div>
<script>
const DATA=__DATA__;
const MOD_LABELS=__MODLABELS__,MOD_ORDER=__MODORDER__,ACCESS_LABELS=__ACCLABELS__,ACCESS_SHORT=__ACCSHORT__,ACCESS_ORDER=__ACCORDER__;
const BC={open:'b-open',partial:'b-partial',hub:'b-hub',api:'b-api',paper:'b-paper',platform:'b-platform'};
const st={q:'',mods:new Set(),accs:new Set(),tog:new Set(),sort:'default',dir:1,openset:new Set()};
const esc=s=>(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function counts(f,order){const c={};order.forEach(k=>c[k]=0);DATA.forEach(m=>{if(c[m[f]]!==undefined)c[m[f]]++});return c}
const modC=counts('modality',MOD_ORDER),accC=counts('access',ACCESS_ORDER);
function chips(el,order,labels,cnts,set,cls){order.forEach(k=>{if(cnts&&!cnts[k])return;const d=document.createElement('div');d.className='chip'+(cls||'');d.dataset.k=k;d.innerHTML=labels[k]+(cnts?'<span class="c">'+cnts[k]+'</span>':'');d.onclick=()=>{set.has(k)?set.delete(k):set.add(k);d.classList.toggle('on');render()};el.appendChild(d)})}
chips(document.getElementById('modchips'),MOD_ORDER,MOD_LABELS,modC,st.mods,'');
chips(document.getElementById('accchips'),ACCESS_ORDER,ACCESS_LABELS,accC,st.accs,'');
chips(document.getElementById('togchips'),['hasWeights','hasCode','canonical'],{hasWeights:'Downloadable weights',hasCode:'Has code repo',canonical:'⭐ Canonical only'},null,st.tog,' tog');
const qEl=document.getElementById('q');
qEl.addEventListener('input',e=>{st.q=e.target.value.toLowerCase();render()});
document.getElementById('reset').onclick=()=>{st.q='';qEl.value='';st.mods.clear();st.accs.clear();st.tog.clear();st.sort='default';document.querySelectorAll('.chip.on').forEach(c=>c.classList.remove('on'));render()};
document.getElementById('theme').onclick=()=>{const h=document.documentElement;h.dataset.theme=h.dataset.theme==='dark'?'':'dark';try{localStorage.setItem('bfm-theme',h.dataset.theme)}catch(e){}};
(function(){try{const t=localStorage.getItem('bfm-theme');if(t)document.documentElement.dataset.theme=t;else if(matchMedia('(prefers-color-scheme:dark)').matches)document.documentElement.dataset.theme='dark'}catch(e){}})();
document.querySelectorAll('th[data-k]').forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(st.sort===k){st.dir*=-1}else{st.sort=k;st.dir=1}render()});
document.querySelectorAll('.qcbtn').forEach(b=>b.onclick=()=>{st.q=b.dataset.q.toLowerCase();qEl.value=b.dataset.q;render();document.querySelector('table.main').scrollIntoView({behavior:'smooth'})});
function tokens(q){return q.split(/\s+/).filter(Boolean)}
function match(m){
 if(st.mods.size&&!st.mods.has(m.modality))return false;
 if(st.accs.size&&!st.accs.has(m.access))return false;
 for(const t of st.tog){if(!m[t])return false}
 for(const tk of tokens(st.q)){if(!m._s.includes(tk))return false}
 return true}
function yr(m){const y=parseInt(m.year);return isNaN(y)?-1:y}
function links(m,all){let o=[];const ps=m.paper_links||[],cs=m.code_links||[];
 if(all){ps.forEach(l=>o.push('<a href="'+l.url+'" target="_blank" rel="noopener">📄 '+esc(l.label)+'</a>'));cs.forEach(l=>o.push('<a href="'+l.url+'" target="_blank" rel="noopener">⚙️ '+esc(l.label)+'</a>'));return o.join('')}
 if(ps[0])o.push('<a href="'+ps[0].url+'" target="_blank" rel="noopener" title="paper">📄</a>');
 if(cs[0])o.push('<a href="'+cs[0].url+'" target="_blank" rel="noopener" title="code">⚙️</a>');
 return o.join('')}
function rowHtml(m,i){
 const bc=BC[m.access]||'b-paper';
 const nm='<span class="nm">'+esc(m.name)+'</span>'+(m.canonical?'<span class="star" title="canonical / most-used">⭐</span>':'')+(m.nc?'<span class="tag tag-nc" title="non-commercial license noted">NC</span>':'');
 const open=st.openset.has(m.name);
 let h='<tr class="row'+(open?' open':'')+'" data-n="'+esc(m.name)+'">'
  +'<td><span class="exp">▸</span></td>'
  +'<td>'+nm+'</td>'
  +'<td><span class="badge b-mod">'+esc(MOD_LABELS[m.modality]||m.modality)+'</span></td>'
  +'<td><span class="badge '+bc+'" title="'+esc(m.status)+'">'+esc(ACCESS_SHORT[m.access]||m.access)+'</span></td>'
  +'<td class="yr">'+esc(m.year||'—')+'</td>'
  +'<td class="io"><span class="t">'+esc(m.io||'')+'</span></td>'
  +'<td class="uses"><span class="t">'+esc(m.use_cases||'')+'</span></td>'
  +'<td class="lnk">'+links(m,false)+'</td></tr>';
 if(open){
  h+='<tr class="detailrow"><td colspan="8"><div class="detail">'
   +'<div class="kv"><b>Description:</b> '+esc(m.description)+'</div>'
   +'<div class="kv"><b>Input → Output:</b> '+esc(m.io)+'</div>'
   +'<div class="kv"><b>Use cases:</b> '+esc(m.use_cases)+'</div>'
   +'<div class="kv"><b>Access detail:</b> '+esc(m.status)+(m.nc?' · <b>non-commercial</b>':'')+'</div>'
   +'<div class="links">'+links(m,true)+'</div>'
   +'</div></td></tr>';
 }
 return h}
function render(){
 let rows=DATA.filter(match);
 document.getElementById('count').textContent=rows.length+' of '+DATA.length+' shown';
 const tb=document.getElementById('tb'),emp=document.getElementById('empty');
 if(!rows.length){tb.innerHTML='';emp.innerHTML='<div class="empty">No models match. Clear a filter or the search box.</div>';return}
 emp.innerHTML='';
 if(st.sort==='default'){
  rows.sort((a,b)=>(MOD_ORDER.indexOf(a.modality)-MOD_ORDER.indexOf(b.modality))||(ACCESS_ORDER.indexOf(a.access)-ACCESS_ORDER.indexOf(b.access))||((a.canonical?0:1)-(b.canonical?0:1))||(a.name.toLowerCase()<b.name.toLowerCase()?-1:1));
  let h='',cur=null;
  rows.forEach((m,i)=>{if(m.modality!==cur){cur=m.modality;const n=rows.filter(x=>x.modality===cur).length;h+='<tr class="grouprow"><td colspan="8">'+esc(MOD_LABELS[cur])+' · '+n+'</td></tr>'}h+=rowHtml(m,i)});
  tb.innerHTML=h;
 }else{
  const k=st.sort;
  rows.sort((a,b)=>{let r;if(k==='year')r=yr(a)-yr(b);else if(k==='modality')r=MOD_ORDER.indexOf(a.modality)-MOD_ORDER.indexOf(b.modality);else if(k==='access')r=ACCESS_ORDER.indexOf(a.access)-ACCESS_ORDER.indexOf(b.access);else r=a.name.toLowerCase()<b.name.toLowerCase()?-1:1;return r*st.dir||(a.name.toLowerCase()<b.name.toLowerCase()?-1:1)});
  tb.innerHTML=rows.map((m,i)=>rowHtml(m,i)).join('');
 }
 tb.querySelectorAll('tr.row').forEach(tr=>tr.onclick=e=>{if(e.target.tagName==='A')return;const n=tr.dataset.n;st.openset.has(n)?st.openset.delete(n):st.openset.add(n);render()});
}
render();
</script></body></html>
"""

repl = {
 '__TODAY__':today,'__TOTAL__':str(total),'__NOPEN__':str(n_open),'__NGATED__':str(n_gated),
 '__NAPI__':str(n_api),'__NNEW__':str(n_new),'__NCATS__':str(n_cats),'__QUICK__':quick_rows,
 '__DATA__':json.dumps(norm,ensure_ascii=False),'__MODLABELS__':json.dumps(MOD_LABELS),
 '__MODORDER__':json.dumps(MOD_ORDER),'__ACCLABELS__':json.dumps(ACCESS_LABELS),
 '__ACCSHORT__':json.dumps(ACCESS_SHORT),'__ACCORDER__':json.dumps(ACCESS_ORDER),
}
out=TEMPLATE
for k,v in repl.items():
    out=out.replace(k,v)
open(OUT,'w').write(out)
print(f"Wrote {OUT}  ({total} models, {n_new} new, {n_open} open)")
print("access:",dict(ac))
print("modality:",dict(Counter(m['modality'] for m in norm)))
