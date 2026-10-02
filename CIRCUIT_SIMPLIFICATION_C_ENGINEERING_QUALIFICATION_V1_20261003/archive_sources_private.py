import pathlib,json,hashlib,urllib.request,datetime
P=pathlib.Path(__file__).resolve().parent
D=P.parent/'NEW_PRO_CIRCUIT_SIMPLIFICATION_HANDOFF_20261003'/'C_PRIVATE_OFFICIAL_SOURCES'
D.mkdir(exist_ok=True)
sources=[('S1','TMUX1109.pdf','https://www.ti.com/lit/ds/symlink/tmux1109.pdf'),('S2','LP5912.pdf','https://www.ti.com/lit/ds/symlink/lp5912.pdf'),('S3','BAT54XY.pdf','https://assets.nexperia.com/documents/data-sheet/BAT54XY.pdf'),('S4','TI_LP5912_10UF_QA.html','https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1345093/lp5912-inrush-current-when-cout-is-10uf')]
records=[]
for ident,name,url in sources:
 rec={'id':ident,'url':url,'privateArchive':str(D/name),'publicBulkIncluded':False,'sameLogicalSourcePreviouslyRead':True}
 try:
  with urllib.request.urlopen(url,timeout=12) as response:
   content=response.read();rec.update(HTTP=response.status,bytes=len(content),SHA256=hashlib.sha256(content).hexdigest(),contentType=response.headers.get('Content-Type'),isPDF=content.startswith(b'%PDF'))
  (D/name).write_bytes(content)
 except Exception as e:rec['error']=type(e).__name__+': '+str(e)
 records.append(rec)
(P/'OFFICIAL_SOURCE_ARCHIVE_IDENTITY.json').write_text(json.dumps(records,indent=2),'utf8')
print(json.dumps(records))
