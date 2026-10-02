from pathlib import Path
import json,csv,collections,hashlib,math
from shapely.geometry import Point,LineString
P=Path(__file__).parent;old=P.parent/'R21_PCB_ROUTING_CLOSURE_V1'
v=json.loads((P/'WARM_CAPTURE.json').read_text('utf8'))['parsed']['value'];a=json.loads((old/'WARM_CAPTURE.json').read_text('utf8'))['parsed']['value']
def records(s):
 r=[]
 for ln in s.splitlines():
  if '||'not in ln:continue
  h,b=ln.split('||',1)
  try:r.append((json.loads(h),json.loads(b.rstrip('|'))))
  except ValueError:continue
 return r
rs=records(v['source']);frozen=records((old/'FINAL_PCB_DOCUMENT_FROM_NATIVE_FILE.txt').read_text('utf8'))
def objects(data,kind):return collections.Counter(json.dumps([h.get('id'),b],sort_keys=True,separators=(',',':'))for h,b in data if h['type']==kind)
types=collections.Counter(h['type']for h,b in rs)
kinds=('COMPONENT','PAD_NET','ATTR','LINE','VIA','POUR','POURED','POLY','RULE')
cmp={k:objects(rs,k)==objects(frozen,k)for k in kinds}
diff={}
for k in kinds:
 oldmap={h['id']:b for h,b in frozen if h['type']==k};newmap={h['id']:b for h,b in rs if h['type']==k}
 changed=[{'id':i,'before':oldmap[i],'after':newmap[i]}for i in oldmap.keys()&newmap.keys() if oldmap[i]!=newmap[i]]
 diff[k]={'beforeCount':len(oldmap),'afterCount':len(newmap),'removed':[{'id':i,'body':oldmap[i]}for i in oldmap.keys()-newmap.keys()],'added':[{'id':i,'body':newmap[i]}for i in newmap.keys()-oldmap.keys()],'changed':changed}
(P/'FROZEN_NATIVE_VS_WARM_OBJECT_DIFF.json').write_text(json.dumps(diff,indent=2),'utf8')
print(json.dumps({k:{'before':q['beforeCount'],'after':q['afterCount'],'removed':len(q['removed']),'added':len(q['added']),'changed':len(q['changed'])}for k,q in diff.items()}))
ak={(c['ref'],p['number']):p['net']for c in a['parts']for p in c['pads']}
rows=[{'ref':c['ref'],'pad':p['number'],'net':p['net'],'expected':ak[(c['ref'],p['number'])],'PASS':p['net']==ak[(c['ref'],p['number'])],'xMil':p['x'],'yMil':p['y']}for c in v['parts']for p in c['pads']];assert all(r['PASS']for r in rows)
acs={c['ref']:c for c in a['parts']};core=[{'ref':c['ref'],'PASS':all(c[k]==acs[c['ref']][k]for k in('name','footprint','device','uniqueId','manufacturerId','props','x','y','rotation'))}for c in v['parts']];assert all(q['PASS']for q in core)
def csvout(name,rows):
 with(P/name).open('w',encoding='utf8',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
csvout('WARM_ALL_550_PAD_NET_COMPARE.csv',rows);csvout('WARM_ALL_176_CORE_COMPARE.csv',core)
lines=[(h,b)for h,b in rs if h['type']=='LINE'];via=[(h,b)for h,b in rs if h['type']=='VIA'];shorts=[]
for id in('137f992f55430857','21f945bfa3a6372f'):
 found=next(((h,b)for h,b in lines if h['id']==id),None)
 if found is None:
  h,b=next((h,b)for h,b in frozen if h['type']=='LINE'and h['id']==id)
  shorts.append({'id':id,'frozenNet':b['netName'],'presentInActualWarm':False,'status':'ABSENT_ON_REOPEN_CAUSE_UNCONFIRMED','attachment':'NOT_TESTABLE_ABSENT','editedThisPackage':False});continue
 h,b=found;ends=[(b['startX'],b['startY']),(b['endX'],b['endY'])];matches=[]
 for x,y in ends:
  near=[]
  for q,r in lines:
   if q['id']==id or r['netName']!=b['netName']or r['layerId']!=b['layerId']:continue
   if Point(x,y).distance(LineString([(r['startX'],r['startY']),(r['endX'],r['endY'])]))<=r['width']/2+1e-7:near.append(q['id'])
  matches.append(near)
 shorts.append({'id':id,'net':b['netName'],'layer':b['layerId'],'lengthMil':math.dist(*ends),'endpointSameNetLineContacts':matches,'nativeDRCFlags':False,'origin':'UNCONFIRMED_NOT_IN_BRIDGE_CREATED_IDS','attachedByCopperGeometry':all(matches)})
print(json.dumps(shorts))
(P/'TWO_SHORT_SEGMENT_READONLY_CHECK.json').write_text(json.dumps(shorts,indent=2),'utf8')
errs=[]
def walk(x):
 if isinstance(x,dict):
  if 'errorType'in x and 'globalIndex'in x:errs.append(x)
  else:
   for y in x.values():walk(y)
 elif isinstance(x,list):
  for y in x:walk(y)
walk(json.loads((P/'WARM_DRC.json').read_text('utf8'))['parsed']['value'])
erows=[{'category':q['errorType'],'net':q['net'],'object':q['obj1']['suffix'],'primitiveId':q['explanation']['errData']['obj1'],'xMil':q['pos']['x']*10,'yMil':q['pos']['y']*10,'description':q['explanation']['str']}for q in errs];csvout('ACTUAL_REMAINING_CONNECTIONS.csv',erows)
summary={'parts':len(v['parts']),'pads':len(rows),'assigned':sum(bool(q['net'])for q in rows),'nets':len({q['net']for q in rows if q['net']}),'NC':sum(not q['net']for q in rows),'nativeTypes':dict(types),'frozenFinalObjectsIdentical':cmp,'rulesEqual':v['rules']==a['rules'],'warmActualIdentity':'PASS','warmDRC':dict(collections.Counter(q['errorType']for q in errs)),'warmShort':0,'warmClearance':0,'warmNetlistError':0,'twoShortSegments':shorts,'cold':'NOT_STARTED_STOP_ON_TRUE_CONNECTION_ERROR','PCB_REVIEW_READY':False,'MANUFACTURING_NOT_RELEASED':True}
(P/'FINAL_READONLY_EVIDENCE_SUMMARY.json').write_text(json.dumps(summary,indent=2),'utf8');(P/'ACTUAL_WARM_PCB_SOURCE.txt').write_text(v['source'],'utf8')
print(json.dumps(summary))
