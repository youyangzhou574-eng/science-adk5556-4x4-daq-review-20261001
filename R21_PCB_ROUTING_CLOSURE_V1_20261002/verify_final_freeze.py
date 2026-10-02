import json,pathlib,hashlib,collections
P=pathlib.Path(__file__).parent
old=P.parent/'R21_PCB_IMPORT_DIFF_RESOLUTION_V1';manifest=json.loads((P.parent/'GITHUB_PCB_IMPORT_DIFF_DELIVERY_20261002/payload/SHA256_MANIFEST.json').read_text('utf8'))
r=[]
for row in manifest['files']:
 f=old/row['path'];r.append({'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest().upper(),'expected':row['sha256']})
assert all(x['sha256']==x['expected']for x in r)
def rec(s):
 r=[]
 for ln in s.splitlines():
  if '||'not in ln:continue
  a,b=ln.split('||',1)
  try:h=json.loads(a);j=json.loads(b.rstrip('|'))
  except ValueError:continue
  r.append((h,j))
 return r
wv=json.loads((P/'WARM_CAPTURE.json').read_text('utf8'))['parsed']['value'];sv=json.loads((P/'START_CAPTURE.json').read_text('utf8'))['parsed']['value'];final=rec((P/'FINAL_PCB_DOCUMENT_FROM_NATIVE_FILE.txt').read_text('utf8'))
warm=rec(wv['source']);types=collections.Counter(h['type']for h,b in final)
def bodyset(data,kind):return collections.Counter(json.dumps([h.get('id'),b],sort_keys=True,separators=(',',':'))for h,b in data if h['type']==kind)
out={'frozenPreviousFiles':len(r),'frozenPreviousSHA':'PASS','rulesWarmVsStartEqual':wv['rules']==sv['rules'],'finalNativeTypes':dict(types),'warmToFinalCoreTypes':{k:bodyset(warm,k)==bodyset(final,k)for k in('COMPONENT','PAD_NET','ATTR','RULE')}}
assert out['rulesWarmVsStartEqual']
# PAD may live in embedded footprint data; actual all550 getter audit is separately retained.
assert all(out['warmToFinalCoreTypes'].values())and types['PAD_NET']==550
out['files']=r;(P/'FROZEN_INPUT_AND_FINAL_SOURCE_CHECK.json').write_text(json.dumps(out,indent=2),'utf8')
print(json.dumps({k:v for k,v in out.items()if k!='files'}))
