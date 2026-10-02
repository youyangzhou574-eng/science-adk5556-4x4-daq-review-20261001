from pathlib import Path
import json,collections,sys,csv
P=Path(__file__).parent;mode=sys.argv[1]
def value(n):return json.loads((P/n).read_text('utf8'))['parsed']['value']
def rec(src):
 out=[]
 for ln in src.splitlines():
  if '||'not in ln:continue
  h,q=ln.split('||',1)
  try:out.append((json.loads(h),json.loads(q.rstrip('|'))))
  except ValueError:pass
 return out
def mult(r,k):return collections.Counter(json.dumps([h.get('id'),q],sort_keys=True,separators=(',',':'))for h,q in r if h['type']==k)
a=value('ENTRY_CAPTURE.json'if mode=='warm'else'SAVED_WARM_CAPTURE.json');b=value('SAVED_WARM_CAPTURE.json'if mode=='warm'else'COLD_CAPTURE_AND_NATIVE.json');a=a.get('capture',a);b=b.get('capture',b);ar,br=rec(a['source']),rec(b['source']);types=('COMPONENT','PAD_NET','ATTR','LINE','VIA','POUR','POLY','RULE');cmp={k:mult(ar,k)==mult(br,k)for k in types};cmp['POURED']=mult(ar,'POURED')==mult(br,'POURED')
ap={(c['ref'],p['number']):p['net']for c in a['parts']for p in c['pads']};bp={(c['ref'],p['number']):p['net']for c in b['parts']for p in c['pads']};ac={c['ref']:c for c in a['parts']};core={c['ref']:all(c[k]==ac[c['ref']][k]for k in('name','footprint','device','uniqueId','manufacturerId','props','x','y','rotation','layer'))for c in b['parts']}
ids={h.get('id')for h,q in br};required=('a9e5041778cdb40e','9a5309ba44b7aefd','4e5c023ee9440731','5c0162206220ea3b','d9d6381bb71f0d80')
diff={}
for k in types+('POURED',):
 am={h.get('id'):q for h,q in ar if h['type']==k};bm={h.get('id'):q for h,q in br if h['type']==k};diff[k]={'beforeCount':len(am),'afterCount':len(bm),'added':[{'id':i,'body':bm[i]}for i in bm.keys()-am.keys()],'removed':[{'id':i,'body':am[i]}for i in am.keys()-bm.keys()],'changed':[{'id':i,'before':am[i],'after':bm[i]}for i in am.keys()&bm.keys()if am[i]!=bm[i]]}
result={'stage':mode,'parts':len(b['parts']),'pads':len(bp),'assigned':sum(bool(n)for n in bp.values()),'nets':len({n for n in bp.values()if n}),'NC':sum(not n for n in bp.values()),'counts':dict(collections.Counter(h['type']for h,q in br)),'strictIDbodyEqual':cmp,'core176':all(core.values()),'padNet550':ap==bp,'rulesEqual':a['rules']==b['rules'],'layerInfoEqual':a['layerInfo']==b['layerInfo'],'approved14CopperAllPresent':all(i in ids for i in required),'allowedDerivedPOUREDChangeOnly':all(cmp[k]for k in types)}
ok=(result['parts'],result['pads'],result['assigned'],result['nets'],result['NC'])==(176,550,514,107,36)and result['core176']and result['padNet550']and result['rulesEqual']and result['layerInfoEqual']and result['approved14CopperAllPresent']and all(cmp[k]for k in types)
if mode=='cold':ok=ok and cmp['POURED']
result['PASS']=ok
for n,q in((mode.upper()+'_AUDIT.json',result),(mode.upper()+'_OBJECT_DIFF.json',diff)):(P/n).write_text(json.dumps(q,indent=2),'utf8')
(P/(mode.upper()+'_PCB_SOURCE.txt')).write_text(b['source'],'utf8')
rows=[{'ref':c['ref'],'pad':p['number'],'net':p['net'],'previousNet':ap[(c['ref'],p['number'])],'PASS':p['net']==ap[(c['ref'],p['number'])]}for c in b['parts']for p in c['pads']]
with(P/(mode.upper()+'_550_PAD_NET.csv')).open('w',encoding='utf8',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with(P/(mode.upper()+'_176_CORE.csv')).open('w',encoding='utf8',newline='')as f:w=csv.DictWriter(f,fieldnames=['ref','PASS']);w.writeheader();w.writerows({'ref':r,'PASS':p}for r,p in core.items())
print(json.dumps(result))
if not ok:
 f=P/'EXECUTION_BUDGET.json';q=json.loads(f.read_text('utf8'));q['status']='STOP_'+mode.upper()+'_REAL_IDENTITY_OR_NONDERIVED_COPPER_DIFFERENCE';f.write_text(json.dumps(q,indent=2),'utf8');raise SystemExit('Real auditSTOP')
