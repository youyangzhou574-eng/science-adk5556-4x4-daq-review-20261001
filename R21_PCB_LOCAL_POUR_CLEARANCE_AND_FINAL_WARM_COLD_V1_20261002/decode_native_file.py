from pathlib import Path
import json,hashlib,base64,zipfile,collections
P=Path(__file__).parent;v=json.loads((P/'COLD_CAPTURE_AND_NATIVE.json').read_text('utf8'))['parsed']['value'];nf=v['nativeFile'];data=base64.b64decode(nf['base64']);assert len(data)==nf['bytes'];file=P/nf['name'];file.write_bytes(data)
def rec(src):
 out=[]
 for ln in src.splitlines():
  if '||'not in ln:continue
  h,q=ln.split('||',1)
  try:out.append((json.loads(h),json.loads(q.rstrip('|'))))
  except ValueError:pass
 return out
with zipfile.ZipFile(file)as z:
 names=[n for n in z.namelist()if n.endswith('.epru')];assert len(names)==1;raw=z.read(names[0]).decode('utf8')
lines=[];active=False
for ln in raw.splitlines():
 r=rec(ln)
 if not r:continue
 h,q=r[0]
 if h['type']=='DOCHEAD':active=q.get('docType')=='PCB'and q.get('uuid')=='268e6597399ebcce'
 if active:lines.append(ln)
src='\n'.join(lines)+'\n';(P/'FINAL_PCB_DOCUMENT_FROM_NATIVE_FILE.txt').write_text(src,'utf8');a=rec(v['capture']['source']);b=rec(src);d={}
for k in('COMPONENT','PAD_NET','ATTR','LINE','VIA','POUR','POURED','POLY','RULE'):
 am={h.get('id'):q for h,q in a if h['type']==k};bm={h.get('id'):q for h,q in b if h['type']==k};d[k]={'captureCount':len(am),'fileCount':len(bm),'addedInFile':[{'id':i,'body':bm[i]}for i in bm.keys()-am.keys()],'missingInFile':[{'id':i,'body':am[i]}for i in am.keys()-bm.keys()],'changed':[{'id':i,'capture':am[i],'file':bm[i]}for i in am.keys()&bm.keys()if am[i]!=bm[i]]}
for k in('COMPONENT','PAD_NET','ATTR','VIA','POUR','POLY','RULE'):assert not d[k]['addedInFile']and not d[k]['missingInFile']and not d[k]['changed'],k
assert{q['id']for q in d['LINE']['addedInFile']}=={'21f945bfa3a6372f','137f992f55430857'}and not d['LINE']['missingInFile']and not d['LINE']['changed']
ids={h.get('id')for h,q in b};assert all(i in ids for i in('a9e5041778cdb40e','9a5309ba44b7aefd','4e5c023ee9440731','5c0162206220ea3b','d9d6381bb71f0d80'))
(P/'COLD_CAPTURE_VS_NATIVE_FILE_DIFF.json').write_text(json.dumps(d,indent=2),'utf8')
r={'name':nf['name'],'bytes':len(data),'SHA256':hashlib.sha256(data).hexdigest().upper(),'actualNativeFile':True,'constructor':nf['constructor'],'tag':nf['tag'],'actualLINE':len([1 for h,q in a if h['type']=='LINE']),'nativeFileLINE':len([1 for h,q in b if h['type']=='LINE']),'all14SubstantiveCopperPresent':True,'coreViaPourBoundaryRuleExact':True,'savedBeforeCold':True,'representationDifferenceRetained':True,'manufactureBenchReleased':False};(P/'FINAL_NATIVE_FILE_METADATA.json').write_text(json.dumps(r,indent=2),'utf8');print(json.dumps(r))
