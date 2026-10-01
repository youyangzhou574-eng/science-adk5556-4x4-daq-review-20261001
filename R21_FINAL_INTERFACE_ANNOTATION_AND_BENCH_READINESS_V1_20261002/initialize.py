import pathlib,json,shutil,hashlib,datetime
P=pathlib.Path(__file__).resolve().parent;O=P.parent/'R21_NATIVE_PIN_NET_CORRECTION_AND_FINAL_DRAWING_V1'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
lim={'workcopy':1,'session':2,'save':2,'captureAudit':2,'PDF':1,'ERC':0,'library':0,'sources':0,'candidate':0,'OP_AC':0,'transient':0,'PZ':0,'MIMO':0,'descriptor':0,'reset':0,'protocol':0}
q=dict(startedUTC=now,totalMaxMinutes=180,phase='P0',phaseStartedUTC=now,limits={k:{'minutes':v}for k,v in [('P0',45),('P1',30),('P2',45),('P3',60)]},globalLimits=lim,used={k:0 for k in lim},operations=[],phaseHistory=[],scienceStopped=False)
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(q,indent=2)+'\n','utf8')
for f in ['cli_call.py','run_native.py','budget.py','audit_actual.py','ENGINEERING_LIBRARY_PARSED.json','context.js']:
 shutil.copy2(O/f,P/f)
plan=json.loads((O/'PLAN_FINAL.json').read_text('utf8'))
old=[(x['ref'],pin,net)for x in plan['parts']for pin,net in x['nets'].items()if net=='V3V3_EXT']
assert set(old)=={('J3','1','V3V3_EXT'),('J4','1','V3V3_EXT'),('R_J3_1','1','V3V3_EXT'),('R_J4_1','1','V3V3_EXT')}
for x in plan['parts']:
 if x['ref']in ['J3','R_J3_1']:x['nets']['1']='V3V3_EXT_SWD'
 if x['ref']in ['J4','R_J4_1']:x['nets']['1']='V3V3_EXT_UART'
(P/'ENGINEERING_PLAN.json').write_text(json.dumps(plan,indent=2)+'\n','utf8')
src=O/'SCIENCE_ADK5556_4X4_R21_NATIVE_CORRECTION_WORK.eprj2'
assert hashlib.sha256(src.read_bytes()).hexdigest().upper()=='BF1241A169A3CE981C2DD315D11A73840043F57F13604DA972AF67EE470F9997'
from budget import charge
charge('workcopy','unique09 cold-PASS source byte copy')
dst=P/'SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_WORK.eprj2';assert not dst.exists();shutil.copy2(src,dst)
rec={str(f.relative_to(P.parent)):dict(bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest().upper())for f in [src,O/'SCIENCE_ADK5556_4X4_R21_REVIEW.epro2',O/'SCIENCE_ADK5556_4X4_R21_REVIEW.pdf',O/'PLAN_FINAL.json']}
rec['copyBytesEqual']=src.read_bytes()==dst.read_bytes()
(P/'FROZEN_INPUT_SHA.json').write_text(json.dumps(rec,indent=2)+'\n','utf8')
print(json.dumps({'oldNetwork':old,'newNetworkExpected':107,'copyBytes':dst.stat().st_size,'startedUTC':now}))
source=(O/'FINAL_PAGE_5_SOURCE.txt').read_text('utf8')
for line in source.splitlines():
 if '"type":"TEXT"'in line:print(line[:850])
