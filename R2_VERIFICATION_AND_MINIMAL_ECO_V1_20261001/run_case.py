import pathlib,subprocess,json,datetime,hashlib,time,sys
ROOT=pathlib.Path(__file__).resolve().parent
EXE=ROOT/'runtime/Spice64/bin/ngspice_con.exe'
def run(name,category,qualification=False,compat=False):
 ledger_path=ROOT/'EXECUTION_BUDGET.json';ledger=json.loads(ledger_path.read_text(encoding='utf-8'))
 counts=ledger['counts']
 for key in ([category]+(['qualification_runs'] if qualification else [])):
  if counts.get(key,0)>=ledger['limits'][key]:raise RuntimeError('budget exhausted '+key)
  counts[key]=counts.get(key,0)+1
 ledger_path.write_text(json.dumps(ledger,indent=2),encoding='utf-8')
 case=ROOT/'cases'/name;result=ROOT/'results'/case.stem;result.mkdir(exist_ok=True)
 command=[str(EXE),'-n']+(['-D','ngbehavior=psa'] if compat else [])+['-b',str(case)]
 record={'command':command,'cwd':str(result),'category':category,'qualification':qualification,'compatibility':compat,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_sha256':hashlib.sha256(case.read_bytes()).hexdigest()}
 start=time.monotonic()
 try:
  cp=subprocess.run(command,cwd=result,capture_output=True,timeout=48)
  record['exit_code']=cp.returncode
  (result/'stdout.log').write_bytes(cp.stdout);(result/'stderr.log').write_bytes(cp.stderr)
 except subprocess.TimeoutExpired as e:
  record['exit_code']='TIMEOUT_48s';(result/'stdout.log').write_bytes(e.stdout or b'');(result/'stderr.log').write_bytes(e.stderr or b'')
 record['elapsed_seconds']=time.monotonic()-start
 (result/'execution.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
 print(json.dumps(record));print((result/'stdout.log').read_text(encoding='utf-8',errors='replace')[-2200:]);print((result/'stderr.log').read_text(encoding='utf-8',errors='replace')[-2200:])
 return record
if __name__=='__main__':run(sys.argv[1],sys.argv[2],qualification='--qualification' in sys.argv,compat='--compat' in sys.argv)
