import urllib.request,pathlib,json,hashlib,concurrent.futures
from pypdf import PdfReader
p=pathlib.Path(__file__).resolve().parent;s=p/'sources'
urls=[('ADS86xx_EVM.pdf','https://www.ti.com/lit/ug/sbau245a/sbau245a.pdf'),('RF4990_MANUFACTURER.pdf','https://yageogroup.com/component-documentation/download/specsheet/RT0603BRD074K99L'),('STM32G031_CN.pdf','https://www.st.com.cn/resource/en/datasheet/stm32g031k8.pdf')]
def run(item):
 name,url=item;rec={'name':name,'url':url}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as r:b=r.read();rec['final_url']=r.url
  assert b.startswith(b'%PDF');(s/name).write_bytes(b);pages=PdfReader(s/name).pages
  (s/(name+'.txt')).write_bytes('\n'.join('=== PAGE '+str(i+1)+' ===\n'+(pg.extract_text()or'') for i,pg in enumerate(pages)).encode('utf-8'))
  rec.update(ok=True,bytes=len(b),pages=len(pages),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:rec.update(ok=False,error=str(e))
 return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:recs=list(pool.map(run,urls))
(p/'SUPPORT_SOURCE_ACQUISITION.json').write_bytes(json.dumps(recs,indent=2).encode('utf-8'));print(json.dumps(recs))
