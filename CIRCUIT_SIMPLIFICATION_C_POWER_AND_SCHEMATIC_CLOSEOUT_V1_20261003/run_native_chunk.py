from pathlib import Path
import json,sys,subprocess
p=Path(__file__).parent;chunks=json.loads((p/'REMAINING_NATIVE_CHUNKS.json').read_text(encoding='utf-8'));q=chunks[int(sys.argv[1])]
assert not(p/'NATIVE_CHUNK_STOP.json').exists(),'Already stopped; no retry'
args=[sys.executable,str(p/'native_step.py'),q['label'],json.dumps(q['cost']),'invoke','--session','130f762e-4e93-4eeb-adac-67d3e49c4457','--ext-uuid','eda','--code-file',str(p/q['codeFile'])]
r=subprocess.run(args,cwd=p,timeout=60)
j=json.loads((p/(q['label']+'.json')).read_text(encoding='utf-8'));v=(j.get('parsed')or{}).get('value',{})
ok=r.returncode==0 and v.get('status')=='PAGE_CANDIDATE_CREATED' and [x['ref']for x in v.get('parts',[])]==q['expectedRefs']
if not ok:(p/'NATIVE_CHUNK_STOP.json').write_text(json.dumps({'chunk':q,'resultStatus':v.get('status'),'error':v.get('error'),'timeout':j.get('outer_timeout',False),'reason':'Unknown or failed native implementation; no adaptive retry'},indent=2),encoding='utf-8')
print(json.dumps({'chunk':int(sys.argv[1]),'verifiedCompleted':ok,'partCount':len(v.get('parts',[]))}));sys.exit(0 if ok else 1)
