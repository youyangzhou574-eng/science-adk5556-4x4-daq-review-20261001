import pathlib,json,hashlib,datetime
P=pathlib.Path(__file__).resolve().parent
r=json.loads((P/'FROZEN_SOURCE_IDENTITY.json').read_text('utf8'));checks=[]
for name,e in r.items():
 if not isinstance(e,dict):continue
 f=P.parent/name
 sha=hashlib.sha256(f.read_bytes()).hexdigest().upper()
 checks.append(dict(path=name,bytes=f.stat().st_size,sha256=sha,pass_=sha==e['sha256']and f.stat().st_size==e['bytes']))
assert all(x['pass_']for x in checks)
(P/'FROZEN_INPUTS_FINAL_SHA_PASS.json').write_text(json.dumps(checks,indent=2)+'\n','utf8')
print(json.dumps({'frozen_source_files_PASS':len(checks)}))
