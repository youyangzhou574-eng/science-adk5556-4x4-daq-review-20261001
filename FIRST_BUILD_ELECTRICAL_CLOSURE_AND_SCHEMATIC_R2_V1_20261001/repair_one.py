import pathlib,json,subprocess,sys
p=pathlib.Path(__file__).resolve().parent;i=int(sys.argv[1]);name=json.loads((p/'REPAIR_ORDER.json').read_text())[i];label='REPAIR_'+str(i)
r=subprocess.run([sys.executable,str(p/'cli_call.py'),label,'invoke','--session','e12c7ead-a970-4582-ba16-b7af144322b1','--ext-uuid','eda','--code-file',str(p/name),'--timeout','50000'],capture_output=True,timeout=59,cwd=p);print(r.stdout.decode('utf-8','replace'));v=json.loads((p/(label+'.json')).read_text(encoding='utf-8')).get('parsed',{});assert v.get('ok')and v.get('value',{}).get('status')=='REPAIRED',v
