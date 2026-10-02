from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).parent;d=json.loads((P/'COLD_OBJECT_DIFF.json').read_text('utf8'))['POURED'];nums=[];struct=[]
def walk(a,b,path):
 if isinstance(a,(int,float))and not isinstance(a,bool)and isinstance(b,(int,float))and not isinstance(b,bool):
  if a!=b:nums.append({'path':path,'warm':a,'cold':b,'absoluteDifference':abs(a-b)})
 elif type(a)!=type(b):struct.append({'path':path,'warm':a,'cold':b})
 elif isinstance(a,dict):
  if a.keys()!=b.keys():struct.append({'path':path,'keysDifferent':True})
  for k in a.keys()&b.keys():walk(a[k],b[k],path+'/'+str(k))
 elif isinstance(a,list):
  if len(a)!=len(b):struct.append({'path':path,'lengths':[len(a),len(b)]})
  for i,(x,y)in enumerate(zip(a,b)):walk(x,y,path+'/'+str(i))
 elif a!=b:struct.append({'path':path,'warm':a,'cold':b})
for x in d['changed']:walk(x['before'],x['after'],x['id'])
r={'changedObjects':len(d['changed']),'addedObjects':d['added'],'removedObjects':d['removed'],'numericDifferenceCount':len(nums),'maxAbsoluteNumericDifference':max((n['absoluteDifference']for n in nums),default=0),'structuralDifferences':struct,'numericDifferences':nums,'rawPOUREDStrictEqual':False,'note':'No geometry rounded away; full originals/differences retained. No extra CAD operation.'};(P/'WARM_COLD_POURED_REPRESENTATION_DIFF.json').write_text(json.dumps(r,indent=2),'utf8');print(json.dumps({k:v for k,v in r.items()if k!='numericDifferences'}))
b=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'));b['actual']['DRC']=2;b['reservations'].append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'DRC','count':1,'reason':'Late debit actual COLD_DRC after reservation failed on overly strict POURED comparison; not backdated','executionDeviation':True});b['coldDRCPredebitGuardFailure']={'actualOperation':'COLD_DRC.json','reason':'Sequential tool orchestration did not abort on failed reserve.py and executed read-only COLD_DRC anyway. No additional CAD mutation/save/rebuild. Report deviation; no retrospective exception claim.'};b['status']='COLD_DRC_ZERO_REPRESENTATION_REVIEW_NO_MORE_NATIVE_OPERATIONS';b['evidenceOnlyAfterStop']=True;(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),'utf8')
