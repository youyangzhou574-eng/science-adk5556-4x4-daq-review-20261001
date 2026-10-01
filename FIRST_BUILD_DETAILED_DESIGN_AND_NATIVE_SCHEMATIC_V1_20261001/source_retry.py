import urllib.request,pathlib,json,hashlib
from pypdf import PdfReader
p=pathlib.Path(__file__).resolve().parent;s=p/'sources'
results=[]
for name,url in [('REF30.pdf','https://www.ti.com/lit/ds/symlink/ref30.pdf'),('STM32G031.pdf','https://www.st.com/resource/en/datasheet/stm32g031j6.pdf')]:
 rec={'name':name,'url':url}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as r:data=r.read();rec['final_url']=r.url
  assert data.startswith(b'%PDF')
  (s/name).write_bytes(data);pages=PdfReader(s/name).pages
  (s/(name+'.txt')).write_bytes('\n'.join('=== PAGE '+str(i+1)+' ===\n'+(pg.extract_text()or'') for i,pg in enumerate(pages)).encode('utf-8'))
  rec.update(ok=True,bytes=len(data),pages=len(pages),sha256=hashlib.sha256(data).hexdigest().upper())
 except Exception as e:rec.update(ok=False,error=str(e))
 results.append(rec)
(p/'SOURCE_RETRY.json').write_bytes(json.dumps(results,indent=2).encode('utf-8'));print(json.dumps(results))
