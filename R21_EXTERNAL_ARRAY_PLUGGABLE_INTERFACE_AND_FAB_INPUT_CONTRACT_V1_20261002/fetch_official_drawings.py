from pathlib import Path
from urllib.request import urlopen,Request
from concurrent.futures import ThreadPoolExecutor,as_completed
import datetime,hashlib,json
P=Path(__file__).parent;(P/'sources').mkdir(exist_ok=True)
b=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'))
assert b['actual']['officialSources']==1
b['actual']['officialSources']=4
b['reservations'].append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'officialSources','count':3,'reason':'Housing product page already read (late read-only accounting, no backdated reservation); header family customer drawing and exacthousing drawing reserved before direct fetch; 4 independent documents total. Search discovery excerpts not separate engineering authority.'})
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2)+'\n','utf8')
urls={'171856_CUSTOMER_DRAWING.pdf':'https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/171/171856/1718560002_sd.pdf','22012087_CUSTOMER_DRAWING.pdf':'https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/269/2695/022012087_sd.pdf'}
def fetch(e):
 name,url=e
 try:
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=24) as r:data=r.read()
  assert data.startswith(b'%PDF'),name
  (P/'sources'/name).write_bytes(data)
  return {'name':name,'url':url,'bytes':len(data),'SHA256':hashlib.sha256(data).hexdigest().upper(),'downloaded':True}
 except Exception as ex:return {'name':name,'url':url,'downloaded':False,'error':type(ex).__name__+':'+str(ex)}
with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(fetch,urls.items()))
sources={'officialSourcesCount':4,'scope':'two exact product pages plus two customer drawings; no backup-source accessed','productPages':['https://www.molex.com/en-us/products/part-detail/1718560008','https://www.molex.com/en-us/products/part-detail/22012087'],'downloads':results,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(P/'SOURCES.json').write_text(json.dumps(sources,indent=2)+'\n','utf8');print(json.dumps(sources))
