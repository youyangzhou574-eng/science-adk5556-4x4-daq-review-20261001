from pathlib import Path
import json,collections,base64,hashlib,zipfile
P=Path(__file__).parent
v=json.loads((P/'COLD_J2_BATCH_AND_NATIVE.json').read_text('utf8'))['parsed']['value'];W=json.loads((P/'WARM_J2_BATCH.json').read_text('utf8'))['parsed']['value'];C=v['capture'];(P/'COLD_PCB.json').write_text(json.dumps(C['pcb'],ensure_ascii=False),'utf8');(P/'COLD_SCHEMATIC.json').write_text(json.dumps(C['schematic'],ensure_ascii=False),'utf8');(P/'COLD_PCB_SOURCE.txt').write_text(C['pcb']['source'],'utf8')
def rec(s):
 r=[]
 for l in s.splitlines():
  if '||' in l:
   h,q=l.split('||',1)
   try:r.append((json.loads(h),json.loads(q.rstrip('|'))))
   except ValueError:pass
 return r
def mult(s):
 a=[]
 for h,q in rec(s):
  q=dict(q)
  if h['type']=='DOCHEAD':
   for k in('client','updateTime','version'):q.pop(k,None)
  a.append(json.dumps([h['type'],h.get('id'),q],sort_keys=True))
 return collections.Counter(a)
pa={x['ref']:x for x in W['pcb']['parts']};pb={x['ref']:x for x in C['pcb']['parts']};diff={k:{f:[pa[k].get(f),pb[k].get(f)]for f in pa[k].keys()|pb[k].keys()if pa[k].get(f)!=pb[k].get(f)}for k in pa if pa[k]!=pb[k]};drc=json.loads((P/'COLD_J2_DRC.json').read_text('utf8'))['parsed'];r={'warmColdCoreExact':pa==pb,'differences':diff,'warmColdRulesExact':W['pcb']['rules']==C['pcb']['rules'],'warmColdNetlistExact':W['pcb']['netlist']==C['pcb']['netlist'],'warmColdPcbSourceKVMultiset':mult(W['pcb']['source'])==mult(C['pcb']['source']),'warmColdSchematicSourceKVMultiset':{x['page']['name']:mult(x['source'])==mult(y['source'])for x,y in zip(W['schematic']['pages'],C['schematic']['pages'])},'headerExcludedOnly':['client','updateTime','version'],'coldDRCempty':drc.get('ok')and drc.get('value')==[]}
r['PASS']=all([r['warmColdCoreExact'],r['warmColdRulesExact'],r['warmColdNetlistExact'],r['warmColdPcbSourceKVMultiset'],all(r['warmColdSchematicSourceKVMultiset'].values()),r['coldDRCempty']]);(P/'COLD_GATE.json').write_text(json.dumps(r,indent=2),'utf8');print(json.dumps(r))
f=v['nativeFile'];d=base64.b64decode(f['base64']);assert len(d)==f['bytes'];(P/f['name']).write_bytes(d);meta={'name':f['name'],'bytes':len(d),'SHA256':hashlib.sha256(d).hexdigest().upper(),'constructor':f['constructor'],'tag':f['tag'],'coldExportActual':True};(P/'FINAL_NATIVE_FILE_METADATA.json').write_text(json.dumps(meta,indent=2),'utf8');print(json.dumps(meta))
with zipfile.ZipFile(P/f['name'])as z:
 names=z.namelist();print('zip entries',names);t=[x for x in names if x.endswith('.epru')];assert len(t)==1;raw=z.read(t[0]).decode('utf8');(P/'FINAL_NATIVE_EPRU_LOCAL.txt').write_text(raw,'utf8')
 docs={};cur=None
 for l in raw.splitlines():
  t=rec(l)
  if not t:continue
  h,q=t[0]
  if h['type']=='DOCHEAD':cur=(q.get('docType'),q.get('uuid'));docs[cur]=[]
  if cur:docs[cur].append(l)
 print('docs',list(docs));(P/'FINAL_NATIVE_DOCUMENT_INDEX.json').write_text(json.dumps([{'type':k[0],'uuid':k[1],'lines':len(x)}for k,x in docs.items()],indent=2),'utf8')
 for k,x in docs.items():
  if k[1] in('87b2e6ab0bf2243f','268e6597399ebcce'):(P/('FINAL_NATIVE_'+k[0]+'_SOURCE.txt')).write_text('\n'.join(x)+'\n','utf8')
if not r['PASS']:raise SystemExit('COLD differences require actual evidence review; no remaining edits')
