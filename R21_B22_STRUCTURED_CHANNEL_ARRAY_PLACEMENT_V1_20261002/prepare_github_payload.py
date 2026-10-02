from pathlib import Path
import json,shutil,re,hashlib,zipfile,datetime
P=Path("E:/open/SCIENCE_ADK5556_4X4_DAQ_REPLICA/R21_B22_STRUCTURED_CHANNEL_ARRAY_PLACEMENT_V1");D=P.parent/'GITHUB_B22_STRUCTURED_DELIVERY_20261002';prev=P.parent/'GITHUB_B21_TOP_BAND_DELIVERY_20261002';folder=P.name+'_20261002'
out=D/'payload';assert not out.exists(),'Do not replace frozen payload';out.mkdir()
patterns=[rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'github_pat_[A-Za-z0-9_]{50,}',rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',rb'(?i)(?:password|passwd|api_key|access_token)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}[\"\x27]']
files=[]
for p in sorted(P.rglob('*')):
 if not p.is_file()or'__pycache__'in p.parts:continue
 assert p.suffix.lower()not in('.eprj2','.pdf','.html','.db','.sqlite')
 data=p.read_bytes();assert len(data)<100_000_000
 assert not any(re.search(x,data)for x in patterns),p.name
 n=p.relative_to(P).as_posix();dst=out/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst)
 files.append({'path':n,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest().upper()})
manifest={'package':'SCIENCE_ADK5556_4X4_R21_B22_STRUCTURED_CHANNEL_ARRAY_PLACEMENT_V1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':files,'inputProvenance':json.loads((P/'INPUT_MANIFEST.json').read_text()),'scope':'All own readable report/PNG/CSV/JSON/codes/first failure/review. No account SQLite or third-party bulk. PARTIAL_HOLD; CAD0.'}
(out/'SHA256_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
with zipfile.ZipFile(out/'COMPLETE_SOURCE_AND_EVIDENCE.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for r in files:z.write(out/r['path'],r['path'])
 z.write(out/'SHA256_MANIFEST.json','SHA256_MANIFEST.json')
(out/'ROOT_README.md').write_text(f'''# Latest: B2.2 structured channel visual draft — partial / HOLD
[Comparison]({folder}/PLACEMENT_B21_VS_B22.png) · [Complete receipt]({folder}/COMPLETE_B22_RECEIPT.md) · [Coordinates]({folder}/PLACEMENT_B22.csv) · [Role groups]({folder}/STRUCTURED_GROUPS.csv) · [Extra distances]({folder}/EXTRA_LOCAL_PIN_DISTANCES.csv) · [Gates]({folder}/GATES.json) · [Final review]({folder}/FINAL_REVIEW.md).
125passives moved/rotated; all15IC+4connector anchors frozen,176/552/514/107/36+2emptyMP. Complete body/pad proxy0collision and inherited94actualpaddistances no increase. Added real-net checks include5increases; incomplete ADC banks/commontemplates disclosed. Not CADready, not nativeDRC/manufacturing. No actual PCB modified. One figure + readable evidence direct, ZIP supplementary.
---
'''+(prev/'payload/ROOT_README.md').read_text(encoding='utf8'),encoding='utf8')
sha=lambda n:hashlib.sha256((out/n).read_bytes()).hexdigest().upper()
r={'sourceFilesDelivered':len(files),'payloadFiles':len(files)+3,'reportSHA256':sha('COMPLETE_B22_RECEIPT.md'),'manifestSHA256':sha('SHA256_MANIFEST.json'),'zipSHA256':sha('COMPLETE_SOURCE_AND_EVIDENCE.zip'),'zipBytes':(out/'COMPLETE_SOURCE_AND_EVIDENCE.zip').stat().st_size,'credentialScan':'PASS','scopeOnlyThisCircuit':True,'rawSQLiteUploaded':False,'CAD':0}
(D/'PREPARE_AND_SCAN.json').write_text(json.dumps(r,indent=2),encoding='utf8');print(json.dumps(r))
