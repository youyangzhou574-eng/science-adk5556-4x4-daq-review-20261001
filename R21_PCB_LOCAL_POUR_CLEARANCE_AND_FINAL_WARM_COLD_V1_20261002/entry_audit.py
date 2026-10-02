from pathlib import Path
import json,collections,csv
P=Path(__file__).parent;old=P.parent/'R21_PCB_V3V3_MINIMAL_CONNECTION_CORRECTION_V1'
a=json.loads((old/'POSTFIX_FAILURE_CAPTURE.json').read_text('utf8'))['parsed']['value'];b=json.loads((P/'ENTRY_CAPTURE.json').read_text('utf8'))['parsed']['value']
def records(src):
 out=[]
 for ln in src.splitlines():
  if '||'not in ln:continue
  h,q=ln.split('||',1)
  try:out.append((json.loads(h),json.loads(q.rstrip('|'))))
  except ValueError:pass
 return out
ra,rb=records(a['source']),records(b['source'])
def mult(rs,k):return collections.Counter(json.dumps([h.get('id'),q],sort_keys=True,separators=(',',':'))for h,q in rs if h['type']==k)
types=('COMPONENT','PAD_NET','ATTR','LINE','VIA','POUR','POURED','POLY','RULE');cmp={k:mult(ra,k)==mult(rb,k)for k in types}
ids={h.get('id')for h,q in rb};required=['a9e5041778cdb40e','9a5309ba44b7aefd','4e5c023ee9440731','5c0162206220ea3b','d9d6381bb71f0d80'];present={i:i in ids for i in required}
pa={(c['ref'],p['number']):p['net']for c in a['parts']for p in c['pads']};pb={(c['ref'],p['number']):p['net']for c in b['parts']for p in c['pads']};ca={c['ref']:c for c in a['parts']}
# Only the GUI-confirmed isolated-project owner UUID differs; never ignore library identity or arbitrary fields.
oldowner='6c25a449ce9ab470f4c1db4bd85120e6cad325b0f291f573b07c6aaa4d353ee1';newowner='7efd53fbc610430d096d3e416ed545dafaea621ce2f02ed4c02d0ed9d65ed701';ownerDifferences=[]
def equalfield(ref,k,x,y):
 if x==y:return True
 if k not in('footprint','device')or not isinstance(x,dict)or not isinstance(y,dict):return False
 if x.get('libraryUuid')!=oldowner or y.get('libraryUuid')!=newowner:return False
 xx=dict(x);yy=dict(y);xx['libraryUuid']=oldowner;yy['libraryUuid']=oldowner
 if xx!=yy:return False
 ownerDifferences.append({'ref':ref,'field':k,'before':x,'after':y});return True
core={c['ref']:all(equalfield(c['ref'],k,ca[c['ref']][k],c[k])for k in('name','footprint','device','uniqueId','manufacturerId','props','x','y','rotation','layer'))for c in b['parts']}
(P/'ENTRY_PROJECT_OWNER_UUID_DIFF.json').write_text(json.dumps({'onlyGUIObservedCopyOwnerChanged':True,'oldOwner':oldowner,'newOwner':newowner,'differences':ownerDifferences,'nativeComponentIDBodyStrictSame':cmp['COMPONENT']},indent=2),'utf8')
r={'parts':len(b['parts']),'pads':len(pb),'assigned':sum(bool(n)for n in pb.values()),'nets':len({n for n in pb.values()if n}),'NC':sum(not n for n in pb.values()),'LINE':sum(h['type']=='LINE'for h,q in rb),'VIA':sum(h['type']=='VIA'for h,q in rb),'core176':all(core.values()),'padNet550':pa==pb,'rules':a['rules']==b['rules'],'strictIDbodyEqual':cmp,'required14CopperPresent':present,'causeUnknownHistoricalShortSegmentsNotEdited':True}
ok=all(present.values())and all(cmp.values())and r['core176']and r['padNet550']and r['rules']and(r['parts'],r['pads'],r['assigned'],r['nets'],r['NC'])==(176,550,514,107,36)
r['entryPASS']=ok;(P/'ENTRY_GATE.json').write_text(json.dumps(r,indent=2),'utf8');(P/'ENTRY_PCB_SOURCE.txt').write_text(b['source'],'utf8');print(json.dumps(r))
if not ok:
 budget=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'));budget['status']='STOP_ENTRY_14_COPPER_OR_IDENTITY_NOT_QUALIFIED';(P/'EXECUTION_BUDGET.json').write_text(json.dumps(budget,indent=2),'utf8');raise SystemExit('STOP no pour rebuild')
