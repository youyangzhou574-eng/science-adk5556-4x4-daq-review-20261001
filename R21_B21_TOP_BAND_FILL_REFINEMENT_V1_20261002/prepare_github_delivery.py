from pathlib import Path
import json,shutil,hashlib,re,datetime,zipfile
P=Path(__file__).parent;D=P.parent/'GITHUB_B21_TOP_BAND_DELIVERY_20261002';D.mkdir(exist_ok=True)
PREV=P.parent/'GITHUB_B2_INTERLOCKING_DELIVERY_20261002';folder='R21_B21_TOP_BAND_FILL_REFINEMENT_V1_20261002'
for n in ('github_delivery.py','run_network.py','public_batch.py'):
    s=(PREV/n).read_text(encoding='utf8').replace('R21_PLACEMENT_B2_INTERLOCKING_V1_20261002',folder)
    s=s.replace('Deliver B2 interlocking placement, 94 pin constraints and complete proxy audit; CAD0','Deliver B2.1 top-band-only refinement: six moved, 170 frozen; CAD0')
    if n=='public_batch.py':
        i=s.index('names=');j=s.index('\n',i);s=s[:i]+'names='+repr(['COMPLETE_B21_RECEIPT.md','SHA256_MANIFEST.json','PLACEMENT_B21.csv','PLACEMENT_B2_VS_B21.png','FROZEN_AND_MOVED_REGISTER.json','KEY_PIN_DISTANCE_B21.csv','GATES.json','COMPLETE_SOURCE_AND_EVIDENCE.zip'])+s[j:]
    (D/n).write_text(s,encoding='utf8')
out=D/'payload';assert not out.exists(),'Do not replace frozen payload';out.mkdir()
patterns=[rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'github_pat_[A-Za-z0-9_]{50,}',rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',rb'(?i)(?:password|passwd|api_key|access_token)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}[\"\x27]']
files=[]
for p in sorted(P.rglob('*')):
    if not p.is_file()or'__pycache__'in p.parts:continue
    n=p.relative_to(P).as_posix();data=p.read_bytes();assert p.suffix.lower()not in('.eprj2','.pdf','.html')and len(data)<100_000_000
    assert not any(re.search(x,data)for x in patterns),n
    dst=out/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst);files.append(dict(path=n,bytes=len(data),sha256=hashlib.sha256(data).hexdigest().upper()))
manifest={'package':'SCIENCE_ADK5556_4X4_R21_B21_TOP_BAND_FILL_REFINEMENT_V1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':files,'inputProvenance':json.loads((P/'INPUT_SHA_MANIFEST.json').read_text()),'scope':'All own report/coordinates/readable PNG/geometry/CSV/code/failed first pass/review; no raw SQLite or third-party full PDF/HTML. Official links in OFFICIAL_SOURCE_LINKS.'}
(out/'SHA256_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
with zipfile.ZipFile(out/'COMPLETE_SOURCE_AND_EVIDENCE.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
    for r in files:z.write(out/r['path'],r['path'])
    z.write(out/'SHA256_MANIFEST.json','SHA256_MANIFEST.json')
(out/'ROOT_README.md').write_text(f'''# Latest: B2.1 final top-band refinement; user selection before native CAD

[B2 / B2.1 comparison]({folder}/PLACEMENT_B2_VS_B21.png) · [6 moved / 170 frozen register]({folder}/FROZEN_AND_MOVED_REGISTER.json) · [Complete receipt]({folder}/COMPLETE_B21_RECEIPT.md) · [176 coordinates]({folder}/PLACEMENT_B21.csv) · [94 actual pin distances]({folder}/KEY_PIN_DISTANCE_B21.csv) · [Gates]({folder}/GATES.json) · [Final review]({folder}/FINAL_REVIEW.md).

Only6 components translated X-28mm, 170 positions exactly frozen; 176 parts / 552 pads; natural body envelope71.0x63.5mm. Offline body + conservative pad-proxy complete pair checks, not native DRC. Exact FFC actuator sweep HOLD but current ruling explicitly permits offline layout. No native PCB or board-outline changes, no manufacture/bench release. Full own readable evidence direct; ZIP supplementary. User visual selection and new bounded native scope required.

---

'''+(PREV/'payload/ROOT_README.md').read_text(encoding='utf8'),encoding='utf8')
sha=lambda n:hashlib.sha256((out/n).read_bytes()).hexdigest().upper()
summary={'sourceFilesDelivered':len(files),'payloadFiles':len(files)+3,'reportSHA256':sha('COMPLETE_B21_RECEIPT.md'),'manifestSHA256':sha('SHA256_MANIFEST.json'),'zipSHA256':sha('COMPLETE_SOURCE_AND_EVIDENCE.zip'),'zipBytes':(out/'COMPLETE_SOURCE_AND_EVIDENCE.zip').stat().st_size,'credentialScan':'PASS','scopeOnlyThisCircuit':True,'rawSQLiteUploaded':False,'newCAD':0}
(D/'PREPARE_AND_SCAN.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))
