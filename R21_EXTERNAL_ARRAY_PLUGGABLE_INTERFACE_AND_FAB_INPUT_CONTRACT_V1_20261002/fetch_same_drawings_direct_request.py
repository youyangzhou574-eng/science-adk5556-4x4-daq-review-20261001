from pathlib import Path
from urllib.request import build_opener,ProxyHandler,Request
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,datetime
P=Path(__file__).parent
urls={'171856_CUSTOMER_DRAWING.pdf':'https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/171/171856/1718560002_sd.pdf','22012087_CUSTOMER_DRAWING.pdf':'https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/269/2695/022012087_sd.pdf'}
def fetch(entry):
 name,url=entry
 try:
  opener=build_opener(ProxyHandler({}))
  with opener.open(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=16) as r:data=r.read()
  assert data.startswith(b'%PDF')
  path=P/'sources'/name;assert not path.exists();path.write_bytes(data)
  return {'name':name,'url':url,'downloaded':True,'bytes':len(data),'SHA256':hashlib.sha256(data).hexdigest().upper()}
 except Exception as e:return {'name':name,'url':url,'downloaded':False,'error':type(e).__name__+':'+str(e)}
with ThreadPoolExecutor(max_workers=2) as pool:result=list(pool.map(fetch,urls.items()))
(P/'SAME_DRAWING_DIRECT_REQUEST_RECEIPT.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Same two already-accounted drawings; per-request no proxy only, no environment/profile/network/system settings changed, no security barrier bypass','results':result},indent=2)+'\n','utf8')
print(json.dumps(result))
