import pathlib,json,urllib.request,hashlib,concurrent.futures
from pypdf import PdfReader
p=pathlib.Path(__file__).resolve().parent;out=p/'sources'
sources={'SN74LVC1G17':'https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf','YAGEO_RC_L':'https://www.yageo.com/upload/media/product/productsearch/datasheet/rchip/PYu-RC_Group_51_RoHS_L_12.pdf','MURATA_22u':'https://psearch.en.murata.com/capacitor/product/GRM32ER71E226KE15%23.pdf','MURATA_2u2':'https://psearch.en.murata.com/capacitor/product/GRM31CR71H225KA88%23.pdf','STM32G031':'https://www.st.com/resource/en/datasheet/stm32g031c8.pdf'}
def fetch(item):
 name,url=item
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30)as r:b=r.read()
  assert b.startswith(b'%PDF');f=out/(name+'.pdf');f.write_bytes(b);reader=PdfReader(f)
  (out/(name+'.txt')).write_text('\n'.join('---PAGE %d---\n%s'%(i+1,q.extract_text())for i,q in enumerate(reader.pages)),encoding='utf-8')
  return {'name':name,'url':url,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'pages':len(reader.pages),'status':'DOWNLOADED_PRIMARY'}
 except Exception as e:return {'name':name,'url':url,'status':'FAILED','error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5)as pool:rows=list(pool.map(fetch,sources.items()))
(p/'REMAINING_PRIMARY_SOURCE_ACQUISITION.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows))
