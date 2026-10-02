from pathlib import Path
import datetime, hashlib, json, shutil
p=Path(__file__).parent;old=p.parent/'CIRCUIT_SIMPLIFICATION_C_ENGINEERING_QUALIFICATION_V1';delivery=p.parent/'GITHUB_C_SIMPLIFICATION_DELIVERY_20261003'
now=datetime.datetime.now(datetime.timezone.utc)
limits={'sources':4,'LDOcandidate':2,'copy':1,'session':2,'save':6,'capture':6,'audit':4,'ERC':2,'PDF':1,'OP_AC_PZ':16,'TRAN':4,'placement':0,'PCB':0,'routing':0,'pour':0,'Gerber':0,'bench':0,'procurement':0,'manufacturing':0,'localGit':0,'system':0}
b={'scope':'CIRCUIT-SIMPLIFICATION-C-POWER-AND-SCHEMATIC-CLOSEOUT-V1','startUTC':now.isoformat(),'deadlineUTC':(now+datetime.timedelta(minutes=300)).isoformat(),'limits':limits,'spent':{k:0 for k in limits},'events':[],'STOP':False}
def save(): (p/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),encoding='utf-8')
save()
shutil.copyfile(delivery/'PRO_C_POWER_NEW_RULING_FULL.md',p/'PRO_C_POWER_RULING_FULL.md')
for name in ['cli_call.py','BASELINE_PARTS_AND_NETS.json','BASELINE_ALL_SCHEMATIC_PINS.csv','BASELINE_ACTUAL_RAW.net','C_LIBRARY_CANDIDATES.json','MODEL_SOURCE_SHA.json']:
    shutil.copyfile(old/name,p/name)
(p/'PLAN_AND_LEDGER.md').write_text('''# C power and native schematic closeout
Spec: PRO_C_POWER_RULING_FULL.md; assistant7492ccc0-973b-4538-95f2-4ba4f190d8e3 parent2d7fdffa-4627-4fb6-ac73-6b26d297417a.
300min total; source/material60, schematic120, finite electrical60, delivery60. All counts atomic before actions, no reuse of old budget. C only, no LP/A/full-matrix/PZ rerun, no PCB/placement/manufacturing/bench/Git/system.
S0 verify TPS7A3701 real pin/capacitance/reverse/EN conditions and bounded BOM changes. Whole-rail Ceff/EN removal sequence remains explicit until evidence.
S1 isolated working copy; source pages rebuilt only with actual library/pin mapping and complete designator diff; all core unchanged functions audited from actual File.
S2 bounded power/reset/off analysis or limited models; no macro repair. Keep numerical unresolved history, not global performance PASS.
S3 save/cold actual audit/ERC/PDF, complete receipt and single fresh-context review; normal fixed-commit GitHub delivery and reply successor monitor.
Ruling: same established isolation workflow, no Git/write cleanup; user continuous authorization overrides redundant plan approval. Do not overwrite old source/data. Do not use target90 as mandatory deletion count.
''',encoding='utf-8')
b['spent']['copy']=1;b['events'].append({'utc':now.isoformat(),'cost':{'copy':1},'purpose':'Atomic precharge one private native container copy'})
save()
source=old/'C_ENGINEERING_WORK_PRIVATE_NOT_FOR_PUBLIC.eprj2';target=p/'C_POWER_WORK_PRIVATE_NOT_FOR_PUBLIC.eprj2';target.write_bytes(source.read_bytes())
(p/'PRIVATE_COPY_SOURCE_SHA.json').write_text(json.dumps({'source':str(source),'copy':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'byteIdentical':target.read_bytes()==source.read_bytes(),'publicAllowed':False},indent=2),encoding='utf-8')
print(json.dumps({'initialized':True,'scope':b['scope'],'deadline':b['deadlineUTC'],'copy':1}))
