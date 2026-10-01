import pathlib,json,urllib.request,hashlib,concurrent.futures
from pypdf import PdfReader
p=pathlib.Path(__file__).resolve().parent;out=p/'sources';out.mkdir(exist_ok=True)
sources={'LM73100':'https://www.ti.com/lit/ds/symlink/lm7310.pdf','LM66100_REJECTED':'https://www.ti.com/lit/ds/symlink/lm66100.pdf','TPS3808_REJECTED':'https://www.ti.com/lit/ds/symlink/tps3808.pdf','TPS3890':'https://www.ti.com/lit/ds/symlink/tps3890.pdf','SN74LVC08A':'https://www.ti.com/lit/ds/symlink/sn74lvc08a.pdf','BAT54S':'https://assets.nexperia.com/documents/data-sheet/BAT54S.pdf','OPA4388':'https://www.ti.com/lit/ds/symlink/opa4388.pdf'}
def fetch(item):
 name,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=35)as r:b=r.read()
  assert b.startswith(b'%PDF');f=out/(name+'.pdf');f.write_bytes(b)
  reader=PdfReader(f);text='\n'.join('---PAGE %d---\n%s'%(i+1,page.extract_text())for i,page in enumerate(reader.pages))
  (out/(name+'.txt')).write_text(text,encoding='utf-8')
  return {'name':name,'url':url,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'pages':len(reader.pages),'status':'DOWNLOADED_PRIMARY'}
 except Exception as e:return {'name':name,'url':url,'status':'FAILED','error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=7)as pool:rows=list(pool.map(fetch,sources.items()))
(p/'PRIMARY_SOURCE_ACQUISITION.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows))
