import argparse,json,pathlib,subprocess,datetime
p=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('label');ap.add_argument('args',nargs=argparse.REMAINDER);a=ap.parse_args()
args=list(a.args)
for option,replacement in [('--code-file','--code'),('--args-file','--args')]:
 if option in args:
  i=args.index(option);f=pathlib.Path(args[i+1]).resolve()
  if not f.is_relative_to(p):raise SystemExit('local package inputs only')
  args[i:i+2]=[replacement,f.read_text(encoding='utf-8')]
cmd=[r'H:\Program Files\lceda-pro\lceda-pro.exe']+args
record={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd}
try:
 with (p/(a.label+'.stdout')).open('wb') as out,(p/(a.label+'.stderr')).open('wb') as err:
  r=subprocess.Popen(cmd,stdout=out,stderr=err)
  try:r.wait(timeout=58)
  except subprocess.TimeoutExpired:
   r.terminate();r.wait(timeout=1)
   record.update(outer_timeout=True,execution_state='UNKNOWN: inspect session/context before any mutation')
 record.update(returncode=r.returncode,stdout=(p/(a.label+'.stdout')).read_bytes().decode('utf-8','replace'),stderr=(p/(a.label+'.stderr')).read_bytes().decode('utf-8','replace'))
 try:record['parsed']=json.loads(record['stdout'])
 except ValueError:record['parsed']=None
except subprocess.TimeoutExpired as e:
 record.update(outer_timeout=True,execution_state='UNKNOWN: stop native operations, do not retry',stdout=(e.stdout or b'').decode('utf-8','replace'),stderr=(e.stderr or b'').decode('utf-8','replace'))
(p/(a.label+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
value=record.get('parsed')
print(json.dumps({'record':a.label,'returncode':record.get('returncode'),'outer_timeout':record.get('outer_timeout',False),'parsed':value if len(record.get('stdout',''))<2500 else {'ok':value.get('ok') if value else None,'value_keys':list(value.get('value',{})) if value and isinstance(value.get('value'),dict) else None,'error':value.get('error') if value else None},'stdout_bytes':len(record.get('stdout','').encode('utf-8'))},ensure_ascii=True))
