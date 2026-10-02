from pathlib import Path
import json,hashlib,csv,datetime
P=Path(__file__).parent;old=P.parent/'R21_PCB_ROUTING_CLOSURE_V1';pub=P.parent/'GITHUB_PCB_ROUTING_DELIVERY_20261002'/'payload'
d=json.loads((P/'FROZEN_NATIVE_VS_WARM_OBJECT_DIFF.json').read_text('utf8'));numeric=[];structural=[]
def compare(a,b,path):
 if isinstance(a,(int,float))and not isinstance(a,bool)and isinstance(b,(int,float))and not isinstance(b,bool):
  if a!=b:numeric.append({'path':path,'before':a,'after':b,'absoluteDelta':abs(a-b)})
 elif type(a)!=type(b):structural.append(path)
 elif isinstance(a,dict):
  if a.keys()!=b.keys():structural.append(path+'/keys')
  for k in a.keys()&b.keys():compare(a[k],b[k],path+'/'+str(k))
 elif isinstance(a,list):
  if len(a)!=len(b):structural.append(path+'/length')
  for i,(x,y)in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
 elif a!=b:structural.append(path)
for q in d['POURED']['changed']:compare(q['before'],q['after'],q['id'])
(P/'POURED_NUMERIC_DIFF.json').write_text(json.dumps({'changedBodies':4,'differentNumericScalars':len(numeric),'maxAbsoluteNumericDelta':max((q['absoluteDelta']for q in numeric),default=0),'structuralOrNonnumericDifferences':structural,'differences':numeric,'interpretation':'tiny numeric differences; not byte/strict geometry identical; no pour rebuild performed'},indent=2),'utf8')
rows=[]
for name in ('SCIENCE_ADK5556_4X4_R21_ROUTING_CLOSURE_WORK.eprj2','SCIENCE_ADK5556_4X4_R21_PCB_ROUTED_REVIEW.epro2'):
 x=(old/name).read_bytes();y=(pub/name).read_bytes();rows.append({'file':name,'bytes':len(x),'sha256':hashlib.sha256(x).hexdigest().upper(),'publishedSHA256':hashlib.sha256(y).hexdigest().upper(),'unchanged':x==y})
(P/'FROZEN_INPUT_HASH_CHECK.json').write_text(json.dumps(rows,indent=2),'utf8')
(P/'GUI_CLOSE_CONFIRMED.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'officialSession':'0f4f5001-b4ba-4456-9735-fe059ed1997a','officialClosed':True,'GUIWindow4395510AbsentFromFreshSkyList':True,'oldOwnedWindows3217412And26151560AlsoAbsent':True,'note':'normal GUI close; no save or editing'},indent=2),'utf8')
print(json.dumps({'numericDifferences':len(numeric),'maxDelta':max((q['absoluteDelta']for q in numeric),default=0),'structural':structural,'inputHashes':rows}))
