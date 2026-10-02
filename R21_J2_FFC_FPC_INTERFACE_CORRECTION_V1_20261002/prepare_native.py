from pathlib import Path
import json,datetime,shutil,hashlib
P=Path(__file__).parent;old=P.parent/'R21_EXTERNAL_ARRAY_PLUGGABLE_INTERFACE_AND_FAB_INPUT_CONTRACT_V1'
src=old/'SCIENCE_ADK5556_4X4_R21_J2_PLUGGABLE_WORK.eprj2';dst=P/'SCIENCE_ADK5556_4X4_R21_J2_FFC_WORK.eprj2'
b=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'));assert b['actual']['copy']==0 and not dst.exists()
assert datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat(b['startUTC'])+datetime.timedelta(minutes=240)
b['actual']['copy']=1;b['reservations'].append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'copy','count':1,'reason':'One isolated accepted17 native project copy for Pro20 J2-only ECO'})
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),'utf8');shutil.copyfile(src,dst)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
assert sha(src)==sha(dst)
(P/'INPUT_COPY_HASH.json').write_text(json.dumps({'source':str(src),'copy':str(dst),'bytes':dst.stat().st_size,'SHA256':sha(src),'byteIdentical':True,'oldEpro2SHA256':b['oldNativeSHA']},indent=2),'utf8')
(P/'context.js').write_text('return {project:await eda.dmt_Project.getCurrentProjectInfo(),schematics:await eda.dmt_Schematic.getAllSchematicsInfo()};','utf8')
print(json.dumps({'copied':str(dst),'SHA256':sha(dst)}))
