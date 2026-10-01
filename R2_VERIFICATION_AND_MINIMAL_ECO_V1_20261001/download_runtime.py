import urllib.request, pathlib, hashlib, json, time, sys
ROOT=pathlib.Path(__file__).resolve().parent
url='https://downloads.sourceforge.net/project/ngspice/ng-spice-rework/47/ngspice-47_64.7z'
target=ROOT/'runtime'/'ngspice-47_64.7z'
started=time.monotonic()
record={'source_url':url,'started_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()}
try:
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as response:
  record['resolved_url']=response.url
  record['headers']=dict(response.headers)
  with target.open('wb') as f:
   while True:
    chunk=response.read(1024*1024)
    if not chunk:break
    f.write(chunk)
    if time.monotonic()-started>53:raise TimeoutError('download wall limit 53 s')
 record['bytes']=target.stat().st_size
 record['sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
 record['signature_7z']=target.read_bytes()[:6].hex()
 if target.read_bytes()[:6]!=b'7z\xbc\xaf\x27\x1c':raise ValueError('not a 7z archive')
 record['status']='DOWNLOAD_OK'
except Exception as e:
 record['status']='FAILED';record['error']=str(e)
finally:
 record['elapsed_seconds']=time.monotonic()-started
 (ROOT/'sources'/'NGSPICE_RUNTIME_SOURCE.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
 print(json.dumps(record,indent=2))
sys.exit(0 if record['status']=='DOWNLOAD_OK' else 1)
