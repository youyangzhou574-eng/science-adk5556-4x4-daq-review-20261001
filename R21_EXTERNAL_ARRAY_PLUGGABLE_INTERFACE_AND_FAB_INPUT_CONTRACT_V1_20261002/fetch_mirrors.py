from pathlib import Path
import urllib.request,concurrent.futures,hashlib,json,datetime
P=Path(__file__).parent; D=P/'sources';D.mkdir(exist_ok=True)
items=[('171856_DRAWING_B2_MIRROR.pdf','https://www.farnell.com/cad/2790017.pdf','SD-171856-0001'),('2695_DRAWING_A3_BUNDLE_MIRROR.pdf','https://www.100y.com.tw/pdf_file/10-molex-2201-2057.pdf','26950000-SD')]
def run(item):
 name,url,doc=item;r={'filename':name,'url':url,'documentIdentity':doc,'sameReservedDrawing':True,'sourceCountIncrement':0}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=18) as q:b=q.read(10_000_000)
  assert b.startswith(b'%PDF'),'Not PDF';(D/name).write_bytes(b);r.update(downloaded=True,bytes=len(b),sha256=hashlib.sha256(b).hexdigest().upper())
 except Exception as e:r.update(downloaded=False,error=type(e).__name__+': '+str(e))
 return r
with concurrent.futures.ThreadPoolExecutor(2) as pool:rs=list(pool.map(run,items))
(P/'DRAWING_MIRROR_FETCH.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'items':rs},indent=2),'utf8');print(json.dumps(rs))
