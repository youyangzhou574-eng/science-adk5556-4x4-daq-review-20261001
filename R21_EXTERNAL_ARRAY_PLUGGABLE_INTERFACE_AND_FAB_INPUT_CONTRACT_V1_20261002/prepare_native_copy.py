from pathlib import Path
import datetime,json,hashlib,shutil
P=Path(__file__).parent;old=P.parent/'R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1'
src=old/'SCIENCE_ADK5556_4X4_R21_POUR_CLOSURE_WORK.eprj2';dst=P/'SCIENCE_ADK5556_4X4_R21_J2_PLUGGABLE_WORK.eprj2'
b=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'));assert b['actual']['copy']==0 and not dst.exists()
b['actual']['copy']=1;b['reservations'].append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'copy','count':1,'reason':'Only isolated actual accepted15 project copy; no old native opens/writes'});b['status']='ACTIVE'
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2)+'\n','utf8')
shutil.copyfile(src,dst)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
assert sha(src)==sha(dst)
(P/'INPUT_COPY_HASH.json').write_text(json.dumps({'source':str(src),'copy':str(dst),'bytes':dst.stat().st_size,'SHA256':sha(src),'byteIdentical':True,'acceptedNativeSHA256':'C2D53B0B6BB438D7C916BE24CB0B0D6AE5C7D884E7784EEFFED90E61505BEE6C','baselineCommit':'e9c1b72f4d1659bb9a7a1dbe4a82e7937c5fe86a'},indent=2)+'\n','utf8')
for n in ['cli_call.py','reserve.py','drc_routing.js','save_only.js']:shutil.copyfile(old/n,P/n)
(P/'context.js').write_text('return {project:await eda.dmt_Project.getCurrentProjectInfo(),schematics:await eda.dmt_Schematic.getAllSchematicsInfo()};\n','utf8')
(P/'search_connector.js').write_text("const libraryUuid=await eda.lib_LibrariesList.getSystemLibraryUuid(); return {libraryUuid,items:await eda.lib_Device.search('1718560008',libraryUuid,undefined,undefined,12,1)};\n",'utf8')
print(json.dumps({'copy':str(dst),'bytes':dst.stat().st_size,'SHA256':sha(dst)}))
