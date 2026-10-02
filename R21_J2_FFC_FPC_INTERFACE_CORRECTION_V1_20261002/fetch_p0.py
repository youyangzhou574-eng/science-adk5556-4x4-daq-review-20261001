from pathlib import Path
import urllib.request,json,hashlib,concurrent.futures
P=Path(__file__).parent
(P/'sources_local_only').mkdir(exist_ok=True)
urls={
'S1_connector.html':'https://www.molex.com/en-us/products/part-detail/2005290081',
'S2_connector_drawing.pdf':'https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/200/200529/2005290061_sd.pdf?inline=',
'S3_cable.html':'https://www.molex.com/en-us/products/part-detail/154670229',
'S4_cable_drawing.pdf':'https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/154/15467/154670229_sd.pdf'}
def fetch(k,u):
 try:
  r=urllib.request.build_opener(urllib.request.ProxyHandler({})).open(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=18);d=r.read();(P/'sources_local_only'/k).write_bytes(d)
  return {'file':k,'url':u,'bytes':len(d),'SHA256':hashlib.sha256(d).hexdigest().upper(),'type':r.headers.get('Content-Type'),'ok':True}
 except Exception as e:return {'file':k,'url':u,'ok':False,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: out=list(ex.map(lambda kv:fetch(*kv),urls.items()))
(P/'OFFICIAL_SOURCE_DIRECT_FETCH.json').write_text(json.dumps(out,indent=2),'utf8');print(json.dumps(out))
