import pathlib,json,hashlib,datetime,shutil
p=pathlib.Path(__file__).resolve().parent
v=p.parent/'FIRST_BUILD_DETAILED_DESIGN_AND_NATIVE_SCHEMATIC_V1'
manifest=json.loads((v/'PACKAGE_HASHES.json').read_text(encoding='utf-8'))
rows=[]
for x in manifest['files']:
 f=v/x['relative_path'];b=f.read_bytes();h=hashlib.sha256(b).hexdigest().upper()
 rows.append({**x,'actual_bytes':len(b),'actual_sha256':h,'pass':len(b)==x['bytes'] and h==x['sha256'].upper()})
assert all(x['pass'] for x in rows)
(p/'V1_INPUT_HASHES.json').write_text(json.dumps({'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen_files':len(rows),'all_pass':True,'files':rows},indent=2)+'\n',encoding='utf-8')
budget={'started_utc':'2026-10-01T05:01:00+00:00','phase':'P1','phase_started_utc':'2026-10-01T05:11:00+00:00','phase_minutes_limits':{'P0':15,'P1':60,'P2':90,'P3':60,'P4':15},'total_active_minutes_limit':240,'counts':{'new_project':0,'sessions':1,'saves':0,'native_capture_and_audits':0,'erc':0,'pdf_export':0,'new_primary_sources':5,'new_model_packages':0,'new_function_classes':0,'new_library_identities':0,'library_search_and_readbacks':0,'DC':0,'AC_macro':0,'normal_transient_macro':0,'fault_macro':0,'analytic_selftests':3,'design_revisions':0},'owned_sessions':['e12c7ead-a970-4582-ba16-b7af144322b1'],'closed_sessions':[],'P0':'No confirmed existing SPICE executor: stop adaptation; analytical/model-ready work only','limits':{'new_project':1,'sessions':3,'saves':8,'native_capture_and_audits':4,'erc':3,'pdf_export':3,'new_primary_sources':16,'new_model_packages':4,'new_function_classes':6,'new_library_identities':12,'library_search_and_readbacks':60,'DC':256,'AC_macro':96,'normal_transient_macro':96,'fault_macro':96,'design_revisions':3}}
(p/'EXECUTION_BUDGET.json').write_text(json.dumps(budget,indent=2)+'\n',encoding='utf-8')
shutil.copyfile(v/'ALL_LIBRARY_PARSED.json',p/'V1_LIBRARY_PARSED.json')
print(json.dumps({'frozen_files_verified':len(rows),'all_pass':True}))
