from pathlib import Path
import json,hashlib,datetime,shutil
P=Path(__file__).parent;O=P.parent/'CIRCUIT_C101_BANK_FIRST_FULL_PLACEMENT_CLOSEOUT_V1';D=P.parent/'GITHUB_C101_BANK_FIRST_DELIVERY_20261003'
assert not (P/'EXECUTION_BUDGET.json').exists(),'Never reset initialized package'
files=['C101_PHYSICAL_GEOMETRY.json','C101_IDENTITY_AND_NETS.json','FINAL_COLD_CAPTURE_ACTUAL_BOM.csv','FINAL_COLD_CAPTURE_ALL_PINS.csv','DRAWING_ANNOTATION_ADDENDUM.md','FUNCTIONAL_TARGET_REGISTER.json']
register=[]
for n in files+['P1_FULL_PLACEMENT.json']:
 data=(O/n).read_bytes();dest='BASELINE_'+n if n=='P1_FULL_PLACEMENT.json'else n;(P/dest).write_bytes(data);register.append({'source':str(O/n),'copy':dest,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()})
shutil.copy2(O/'floorplan_core.py',P/'floorplan_core.py');shutil.copy2(D/'PRO_ROW_LOCAL_RULING_FULL.md',P/'PRO_ROW_LOCAL_RULING_FULL.md')
(P/'INPUT_SHA_REGISTER.json').write_text(json.dumps(register,indent=2),encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc);limits=dict(source=0,candidate=1,placement=1,image=1,CAD=0,session=0,save=0,export=0,schematic=0,BOM=0,SPICE=0,PCB=0,routing=0,copper=0,via=0,pour=0,Gerber=0,procurement=0,manufacture=0,bench=0,install=0,system=0,localGit=0)
b={'scope':'CIRCUIT-C101-J2-ROW-ADJACENCY-LOCAL-CLOSEOUT-V1','rulingAssistant':'77a4c655-5e03-4530-8ad4-3f503b76d18c','parentUser':'cca236e8-4ec5-4ff2-ba1d-9b24b20ab49c','startUTC':now.isoformat(),'deadlineUTC':(now+datetime.timedelta(minutes=120)).isoformat(),'limits':limits,'spent':{k:0 for k in limits},'events':[],'STOP':False,'coordinateSTOP':False}
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),encoding='utf-8')
s=json.loads((D/'COMMUNICATION_STATE.json').read_text());s.update(replyStatus='COMPLETE_ROW_LOCAL_RULING_CONSUMED',consumedAssistant=b['rulingAssistant'],consumedParent=b['parentUser'],nextCheckAtUTC=None,monitorStatus='DELETED_AUTHORIZED_ROW_LOCAL_PACKAGE_RUNNING',successorPackage=str(P));
for n in ['COMMUNICATION_STATE.json','PRO_BANK_FIRST_GITHUB_LINK_DELIVERY.json']:(D/n).write_text(json.dumps(s,indent=2),encoding='utf-8')
print(json.dumps({'package':str(P),'deadline':b['deadlineUTC'],'immutableInputs':len(register)}))
