from pathlib import Path
import json,base64,hashlib,zipfile,collections,csv
P=Path(__file__).parent
def value(n):return json.loads((P/n).read_text('utf8'))['parsed']['value']
pre=value('PRE_CAPTURE.json');post=value('POSTFIX_FAILURE_CAPTURE.json');file=value('FAILURE_NATIVE_FILE_CAPTURE.json');data=base64.b64decode(file['base64']);assert len(data)==file['bytes'];nf=P/file['name'];nf.write_bytes(data)
def records(src):
 r=[]
 for ln in src.splitlines():
  if '||'not in ln:continue
  h,b=ln.split('||',1)
  try:r.append((json.loads(h),json.loads(b.rstrip('|'))))
  except ValueError:pass
 return r
a=records(pre['source']);b=records(post['source']);n=[];inpcb=False;source=[]
with zipfile.ZipFile(nf)as z:
 candidates=[name for name in z.namelist()if name.endswith('.epru')];assert len(candidates)==1
 raw=z.read(candidates[0]).decode('utf8')
 for ln in raw.splitlines():
  rr=records(ln)
  if not rr:continue
  h,q=rr[0]
  if h['type']=='DOCHEAD':inpcb=q.get('docType')=='PCB'and q.get('uuid')=='268e6597399ebcce'
  if inpcb:n.append((h,q));source.append(ln)
(P/'FAILURE_PCB_DOCUMENT_FROM_NATIVE_FILE.txt').write_text('\n'.join(source)+'\n','utf8');(P/'ACTUAL_POSTFIX_FAILURE_PCB_SOURCE.txt').write_text(post['source'],'utf8')
def mult(rs,k):return collections.Counter(json.dumps([h['id'],q],sort_keys=True,separators=(',',':'))for h,q in rs if h['type']==k)
kinds=('COMPONENT','PAD_NET','ATTR','LINE','VIA','POUR','POURED','POLY','RULE')
cmp={k:mult(b,k)==mult(n,k)for k in kinds};diff={}
for k in kinds:
 am={h['id']:q for h,q in a if h['type']==k};bm={h['id']:q for h,q in b if h['type']==k}
 diff[k]={'beforeCount':len(am),'afterCount':len(bm),'added':[{'id':i,'body':bm[i]}for i in bm.keys()-am.keys()],'removed':[{'id':i,'body':am[i]}for i in am.keys()-bm.keys()],'changed':[{'id':i,'before':am[i],'after':bm[i]}for i in am.keys()&bm.keys()if am[i]!=bm[i]]}
for k in ('COMPONENT','PAD_NET','ATTR','POUR','POURED','POLY','RULE'):assert not diff[k]['added']and not diff[k]['removed']and not diff[k]['changed'],k
assert all(q['body']['netName']=='V3V3'for q in diff['LINE']['added']+diff['LINE']['removed']+diff['VIA']['added'])and not diff['LINE']['changed']and not diff['VIA']['removed']and not diff['VIA']['changed']
fdiff={}
for k in kinds:
 am={h['id']:q for h,q in b if h['type']==k};bm={h['id']:q for h,q in n if h['type']==k}
 fdiff[k]={'captureCount':len(am),'fileCount':len(bm),'addedInFile':[{'id':i,'body':bm[i]}for i in bm.keys()-am.keys()],'missingInFile':[{'id':i,'body':am[i]}for i in am.keys()-bm.keys()],'changed':[{'id':i,'capture':am[i],'file':bm[i]}for i in am.keys()&bm.keys()if am[i]!=bm[i]]}
(P/'ACTUAL_CAPTURE_VS_NATIVE_FILE_DIFF.json').write_text(json.dumps(fdiff,indent=2),'utf8')
assert all(cmp[k]for k in('COMPONENT','PAD_NET','ATTR','VIA','POUR','POLY','RULE')),cmp
ap={(c['ref'],p['number']):p['net']for c in pre['parts']for p in c['pads']};ac={c['ref']:c for c in pre['parts']};rows=[{'ref':c['ref'],'pad':p['number'],'net':p['net'],'beforeNet':ap[(c['ref'],p['number'])],'PASS':p['net']==ap[(c['ref'],p['number'])]}for c in post['parts']for p in c['pads']];cores=[{'ref':c['ref'],'PASS':all(c[k]==ac[c['ref']][k]for k in('name','footprint','device','uniqueId','manufacturerId','props','x','y','rotation'))}for c in post['parts']];assert all(q['PASS']for q in rows+cores)
def csvout(name,rows):
 with(P/name).open('w',encoding='utf8',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
csvout('ALL_550_PAD_NET_COMPARE.csv',rows);csvout('ALL_176_CORE_COMPARE.csv',cores)
errs=[]
def walk(q):
 if isinstance(q,dict):
  if 'errorType'in q and 'globalIndex'in q:errs.append(q)
  else:
   for x in q.values():walk(x)
 elif isinstance(q,list):
  for x in q:walk(x)
walk(value('FIRST_POSTFIX_DRC.json'));csvout('ACTUAL_FOUR_CLEARANCE_ERRORS.csv',[{'category':q['errorType'],'layer':q['layer'],'obj1':q['obj1']['suffix'],'obj2':q['obj2']['suffix'],'obj2PrimitiveId':q['explanation']['errData']['obj2'],'minDistance':q['explanation']['param']['minDistance'],'required':q['explanation']['param']['shouldBe'],'xMil':q['pos']['x']*10,'yMil':q['pos']['y']*10}for q in errs])
sum={'parts':len(post['parts']),'pads':len(rows),'assigned':sum(bool(q['net'])for q in rows),'nets':len({q['net']for q in rows if q['net']}),'NC':sum(not q['net']for q in rows),'preLINE':len([1 for h,q in a if h['type']=='LINE']),'postLINE':len([1 for h,q in b if h['type']=='LINE']),'postVIA':len([1 for h,q in b if h['type']=='VIA']),'identity550and176':'PASS','rulesEqual':post['rules']==pre['rules'],'nativeFileMatchesActualFailedCapture':cmp,'nativeFileName':file['name'],'nativeFileBytes':len(data),'nativeFileSHA256':hashlib.sha256(data).hexdigest().upper(),'explicitDocumentSave':False,'cold':'NOT_STARTED_ON_NEW_CLEARANCE_STOP','DRC':dict(collections.Counter(q['errorType']for q in errs)),'ConnectionError':0,'Short':0,'NetlistError':0,'ClearanceError':4,'PCB_REVIEW_READY':False,'MANUFACTURING_NOT_RELEASED':True,'BENCH_NOT_RELEASED':True,'nativeLabel':'BLOCKED_NOT_FOR_USE_UNSAVED_FAILURE_STATE_ACTUAL_FILE'}
sum['nativeFileLINE']=len([1 for h,q in n if h['type']=='LINE']);sum['allThisPackageCreatedIdsPresentInNativeFile']=all(q['id']in {h.get('id')for h,z in n}for q in value('APPLY_LOCAL_BRIDGES.json')['created']);assert sum['allThisPackageCreatedIdsPresentInNativeFile']
(P/'NATIVE_PRE_POST_OBJECT_DIFF.json').write_text(json.dumps(diff,indent=2),'utf8');(P/'BLOCKED_EVIDENCE_SUMMARY.json').write_text(json.dumps(sum,indent=2),'utf8');print(json.dumps(sum))
