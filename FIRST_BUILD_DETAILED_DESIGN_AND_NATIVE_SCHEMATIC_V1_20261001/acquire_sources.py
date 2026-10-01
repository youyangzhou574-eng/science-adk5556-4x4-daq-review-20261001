import pathlib,urllib.request,concurrent.futures,json,hashlib,datetime,zipfile
p=pathlib.Path(__file__).resolve().parent;s=p/'sources';s.mkdir(exist_ok=True)
urls={
 'OPAx388.pdf':'https://www.ti.com/lit/ds/symlink/opa4388.pdf',
 'TMUX1134.pdf':'https://www.ti.com/lit/ds/symlink/tmux1134.pdf',
 'ADS8684.pdf':'https://www.ti.com/lit/ds/symlink/ads8684.pdf',
 'REF3025.pdf':'https://www.ti.com/lit/ds/symlink/ref3025.pdf',
 'TPS7A20.pdf':'https://www.ti.com/lit/ds/symlink/tps7a20.pdf',
 'STM32G031.pdf':'https://www.st.com/resource/en/datasheet/stm32g031k8.pdf',
 'OPA4388_PSPICE.zip':'https://www.ti.com/lit/zip/SBOMAZ6',
 'OPA4388_TINA.zip':'https://www.ti.com/lit/zip/SBOMAZ7'}
def fetch(item):
 name,url=item;rec={'file':name,'url':url,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=25) as r: data=r.read();rec.update(final_url=r.url,content_type=r.headers.get('Content-Type'))
  if name.endswith('.pdf') and not data.startswith(b'%PDF'):raise ValueError('response is not PDF')
  if name.endswith('.zip') and not data.startswith(b'PK'):raise ValueError('response is not ZIP')
  (s/name).write_bytes(data);rec.update(ok=True,bytes=len(data),sha256=hashlib.sha256(data).hexdigest().upper())
  if name.endswith('.pdf'):
   from pypdf import PdfReader
   reader=PdfReader(s/name);text='\n'.join('=== PAGE '+str(i+1)+' ===\n'+(pg.extract_text() or '') for i,pg in enumerate(reader.pages))
   (s/(name+'.txt')).write_bytes(text.encode('utf-8'));rec['pages']=len(reader.pages)
  else:
   with zipfile.ZipFile(s/name) as z:
    rec['members']=z.namelist()
    for n in z.namelist():
     target=(s/(name+'.unpacked')/n).resolve()
     if not target.is_relative_to((s/(name+'.unpacked')).resolve()):raise ValueError('unsafe ZIP path')
    z.extractall(s/(name+'.unpacked'))
 except Exception as e:rec.update(ok=False,error=str(e))
 return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(fetch,urls.items()))
(p/'SOURCE_ACQUISITION.json').write_bytes((json.dumps(records,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps(records,ensure_ascii=True))
