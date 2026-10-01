import json,shutil,hashlib,datetime,pathlib
P=pathlib.Path(__file__).resolve().parent
BASE=P.parent
OLD=BASE/'R21_ENGINEERING_R21_NATIVE_AND_LIMITED_VALIDATION_V1'
R2=BASE/'FIRST_BUILD_ELECTRICAL_CLOSURE_AND_SCHEMATIC_R2_V1'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
limits={'workcopy':1,'session':2,'save':6,'captureAudit':4,'ERC':1,'PDF':2,'library':0,'sources':0,'candidate':0,'OP_AC':0,'transient':0,'PZ':0,'descriptor':0,'MIMO':0,'reset':0,'protocol':0}
q=dict(startedUTC=now,totalMaxMinutes=240,phase='P0',phaseStartedUTC=now,limits={k:{'minutes':v}for k,v in [('P0',60),('P1',90),('P2',30),('P3',60)]},globalLimits=limits,used={k:0 for k in limits},operations=[],phaseHistory=[],scienceStopped=False)
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(q,indent=2)+'\n','utf8')
for f in ['cli_call.py','audit_actual.py','budget.py','ENGINEERING_LIBRARY_PARSED.json']:
 shutil.copy2(OLD/f,P/f)
shutil.copy2(R2/'R2_PLAN.json',P/'ENGINEERING_PLAN.json')
shutil.copy2(OLD/'ENGINEERING_PLAN.json',P/'FINAL_EXPECTED_PLAN_FROZEN.json')
shutil.copy2(OLD/'BENCH_VALIDATION_PLAN.md',P/'BENCH_VALIDATION_PLAN.md')
shutil.copy2(OLD/'context.js',P/'context.js')
from budget import charge
charge('workcopy','unique clean frozen R2 copy')
src=R2/'SCIENCE_ADK5556_4X4_R2_NATIVE.eprj2'
dst=P/'SCIENCE_ADK5556_4X4_R21_NATIVE_CORRECTION_WORK.eprj2'
assert not dst.exists()
shutil.copy2(src,dst)
rec={str(f.relative_to(BASE)):dict(bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest().upper())for f in [src,R2/'R2_PLAN.json',OLD/'SCIENCE_ADK5556_4X4_R21_ENGINEERING_WORK.eprj2',OLD/'SCIENCE_ADK5556_4X4_R21_BLOCKED_NOT_FOR_USE.epro2']}
rec['newCopyBytesEqual']=src.read_bytes()==dst.read_bytes()
(P/'FROZEN_SOURCE_IDENTITY.json').write_text(json.dumps(rec,indent=2)+'\n','utf8')
print(json.dumps({'copy':str(dst),'bytes':dst.stat().st_size,'sourceSHA':rec[str(src.relative_to(BASE))]['sha256'],'startedUTC':now}))
