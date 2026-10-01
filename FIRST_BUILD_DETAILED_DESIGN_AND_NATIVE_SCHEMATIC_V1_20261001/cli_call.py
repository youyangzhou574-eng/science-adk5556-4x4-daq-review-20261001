import argparse,json,pathlib,subprocess,datetime,sys
p=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('label');ap.add_argument('args',nargs=argparse.REMAINDER);a=ap.parse_args()
if not a.args: raise SystemExit('CLI arguments required')
cli_args=list(a.args)
if '--code-file' in cli_args:
 i=cli_args.index('--code-file');js_path=pathlib.Path(cli_args[i+1]).resolve()
 if not js_path.is_relative_to(p):raise SystemExit('code file must be in this package')
 cli_args[i:i+2]=['--code',js_path.read_text(encoding='utf-8')]
if '--args-file' in cli_args:
 i=cli_args.index('--args-file');arg_path=pathlib.Path(cli_args[i+1]).resolve()
 if not arg_path.is_relative_to(p):raise SystemExit('args file must be in this package')
 payload=arg_path.read_text(encoding='utf-8');json.loads(payload)
 cli_args[i:i+2]=['--args',payload]
cmd=[r'H:\Program Files\lceda-pro\lceda-pro.exe']+cli_args
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
try:
 r=subprocess.run(cmd,capture_output=True,timeout=90)
 out=r.stdout.decode('utf-8','replace');err=r.stderr.decode('utf-8','replace')
 record={'started_utc':start,'command':cmd,'returncode':r.returncode,'stdout':out,'stderr':err}
 try: record['parsed']=json.loads(out)
 except (ValueError,TypeError): record['parsed']=None
except subprocess.TimeoutExpired as e:
 record={'started_utc':start,'command':cmd,'outer_timeout':True,'stdout':(e.stdout or b'').decode('utf-8','replace'),'stderr':(e.stderr or b'').decode('utf-8','replace'),'execution_state':'UNKNOWN; do not retry native invoke or close/create sessions'}
(p/(a.label+'.json')).write_bytes((json.dumps(record,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
parsed=record.get('parsed')
print(json.dumps({'record':str(p/(a.label+'.json')),'returncode':record.get('returncode'),'outer_timeout':record.get('outer_timeout',False),'parsed':parsed if len(out if 'out' in locals() else '')<1800 else {'ok':parsed.get('ok') if parsed else None,'value_keys':list(parsed.get('value',{})) if parsed and isinstance(parsed.get('value'),dict) else None,'error':parsed.get('error') if parsed else None},'stdout_bytes':len(record.get('stdout','').encode('utf-8'))},ensure_ascii=True))
