from pathlib import Path
import json,shutil,hashlib,datetime
P=Path(__file__).parent
O=P.parent/'CIRCUIT_C101_OFFLINE_PCB_FLOORPLAN_AND_PLACEMENT_REVIEW_V1'
D=P.parent/'GITHUB_C101_FLOORPLAN_DELIVERY_20261003'
assert not (P/'EXECUTION_BUDGET.json').exists(), 'No reset of initialized package'
inputs=['C101_PHYSICAL_GEOMETRY.json','C101_IDENTITY_AND_NETS.json','FUNCTIONAL_TARGET_REGISTER.json','GEOMETRY_EXTRACTION_AUDIT.json']
register=[]
for name in inputs:
 data=(O/name).read_bytes();(P/name).write_bytes(data)
 register.append({'source':str(O/name),'copy':name,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()})
for name in ['floorplan_core.py']:
 shutil.copy2(O/name,P/name)
shutil.copy2(D/'PRO_BANK_FIRST_RULING_FULL.md',P/'PRO_BANK_FIRST_RULING_FULL.md')
(P/'INPUT_SHA_REGISTER.json').write_text(json.dumps(register,indent=2),encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc)
limits=dict(candidate=2,placement=4,image=2,source=0,CAD=0,session=0,save=0,export=0,SPICE=0,PCB=0,routing=0,via=0,pour=0,Gerber=0,bench=0,procurement=0,manufacture=0,install=0,localGit=0,system=0)
b={'scope':'CIRCUIT-C101-BANK-FIRST-FULL-PLACEMENT-CLOSEOUT-V1','rulingAssistant':'0efc68cd-fbc6-47c7-89cb-8e2678c8d92f','parentUser':'188c6864-4406-40c2-8df8-15a723470c1f','startUTC':now.isoformat(),'deadlineUTC':(now+datetime.timedelta(minutes=300)).isoformat(),'limits':limits,'spent':{k:0 for k in limits},'events':[],'STOP':False,'coordinateSTOP':False,'phase':'BANK_CONTRACT_AND_OFFLINE_FULL_PLACEMENT'}
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),encoding='utf-8')
old=json.loads((D/'COMMUNICATION_STATE.json').read_text(encoding='utf-8'))
old.update(replyStatus='COMPLETE_BANK_FIRST_RULING_CONSUMED',consumedAssistant=b['rulingAssistant'],consumedParent=b['parentUser'],monitorStatus='DELETED_NEW_AUTHORIZED_PACKAGE_RUNNING',nextCheckAtUTC=None,successorPackage=str(P),CADReleased=False)
(D/'COMMUNICATION_STATE.json').write_text(json.dumps(old,indent=2),encoding='utf-8')
(D/'PRO_FLOORPLAN_GITHUB_LINK_DELIVERY.json').write_text(json.dumps(old,indent=2),encoding='utf-8')
print(json.dumps({'package':str(P),'budget':b,'inputFiles':len(register)}))
