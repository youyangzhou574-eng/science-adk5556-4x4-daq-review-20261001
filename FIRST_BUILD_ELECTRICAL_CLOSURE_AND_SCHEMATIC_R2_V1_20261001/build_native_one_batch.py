import pathlib,json,subprocess,sys,datetime,hashlib
p=pathlib.Path(__file__).resolve().parent;index=int(sys.argv[1]);names=json.loads((p/'NATIVE_BUILD_SCRIPT_ORDER.json').read_text())
assert 1<=index<len(names)
name=names[index];label='BUILD_'+name.replace('.js','').upper();f=p/(label+'.json')
if f.exists():
 old=json.loads(f.read_text(encoding='utf-8'));v=old.get('parsed',{}).get('value',{})
 if v.get('status')=='BATCH_CREATED':print(json.dumps({'already_verified':label}));raise SystemExit(0)
 raise SystemExit('Existing unsuccessful/unknown batch cannot be blindly repeated')
r=subprocess.run([sys.executable,str(p/'cli_call.py'),label,'invoke','--session','e12c7ead-a970-4582-ba16-b7af144322b1','--ext-uuid','eda','--code-file',str(p/name),'--timeout','50000'],cwd=p,capture_output=True,timeout=59)
print(r.stdout.decode('utf-8','replace'))
record=json.loads(f.read_text(encoding='utf-8'));v=record.get('parsed',{}).get('value',{})
if not record.get('parsed',{}).get('ok') or v.get('status')!='BATCH_CREATED':raise SystemExit('STOP NATIVE: inspect exact recorded error, no automatic retry')
b=json.loads((p/'EXECUTION_BUDGET.json').read_text());b['counts']['new_project']=1;b['phase']='P3';b['P3_started_utc']='2026-10-01T05:47:57+00:00'
if v.get('saved') is True:b['counts']['saves']+=1
(p/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2)+'\n')
(p/'NATIVE_BATCH_JOURNAL.jsonl').open('a',encoding='utf-8').write(json.dumps({'index':index,'script':name,'sha256':hashlib.sha256((p/name).read_bytes()).hexdigest(),'status':v['status'],'parts':len(v['parts']),'save_true':v.get('saved',False),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
