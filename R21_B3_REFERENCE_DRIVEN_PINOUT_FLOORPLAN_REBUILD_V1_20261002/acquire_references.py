from pathlib import Path
import urllib.request,json,hashlib,csv
P=Path(__file__).parent;D=P/'sources_local_only';D.mkdir(exist_ok=True)
refs=[('S1','ADS8684','https://www.ti.com/lit/ds/symlink/ads8684.pdf'),('S2','TIPD167','https://www.ti.com/lit/pdf/tidu427'),('S3','TIDA-01214','https://www.ti.com/lit/pdf/tidud64'),('S4','OPAx388','https://www.ti.com/lit/ds/symlink/opa4388.pdf'),('S5','TMUX1134','https://www.ti.com/lit/ds/symlink/tmux1134.pdf'),('S6','ADI_CN0175','https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0175.html')]
out=[]
for sid,name,url in refs:
 try:
  b=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=15).read();f=D/(sid+'_'+name+('.pdf' if b[:4]==b'%PDF' else '.html'));f.write_bytes(b);out.append({'id':sid,'name':name,'URL':url,'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest(),'file':str(f),'publicBulk':False,'status':'DOWNLOADED'})
 except Exception as e:out.append({'id':sid,'name':name,'URL':url,'status':'DOWNLOAD_FAILED_WEB_PRIMARY_READ_EXISTS','error':str(e)})
(P/'OFFICIAL_SOURCE_REGISTER.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out))
