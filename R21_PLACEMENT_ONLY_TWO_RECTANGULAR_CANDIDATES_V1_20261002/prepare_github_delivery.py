from pathlib import Path
import json,shutil,hashlib,re,datetime,zipfile
P=Path(__file__).parent;D=P.parent/'GITHUB_PLACEMENT_ONLY_DELIVERY_20261002';D.mkdir(exist_ok=True)
PREV=P.parent/'GITHUB_J2_FFC_DELIVERY_20261002'
folder='R21_PLACEMENT_ONLY_TWO_RECTANGULAR_CANDIDATES_V1_20261002'
for name in ('github_delivery.py','run_network.py','public_batch.py'):
    text=(PREV/name).read_text(encoding='utf8').replace('R21_J2_FFC_FPC_INTERFACE_CORRECTION_V1_20261002',folder)
    text=text.replace('Deliver Pro20 FFC J2 warm implementation and honest cold closure blockers; no physical release','Deliver Pro23 two complete176 placement candidates and mechanical limits; no native modification')
    if name=='public_batch.py':
        first=text.index('names=');end=text.index('\n',first)
        names=['COMPLETE_PLACEMENT_RECEIPT.md','SHA256_MANIFEST.json','PLACEMENT_A.csv','PLACEMENT_B.csv','PLACEMENT_AB_COMPARISON.png','KEY_PIN_DISTANCE_COMPARISON.csv','GATES.json','COMPLETE_SOURCE_AND_EVIDENCE.zip']
        text=text[:first]+'names='+repr(names)+text[end:]
    (D/name).write_text(text,encoding='utf8')
out=D/'payload';assert not out.exists(),'Do not replace frozen prepared payload';out.mkdir()
patterns=[rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'github_pat_[A-Za-z0-9_]{50,}',rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',rb'(?i)(?:password|passwd|api_key|access_token)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}[\"\x27]']
files=[];excluded=[]
for p in sorted(P.rglob('*')):
    if not p.is_file()or'__pycache__'in p.parts:continue
    name=p.relative_to(P).as_posix();data=p.read_bytes()
    assert p.suffix.lower()not in('.eprj2','.pdf','.html'),name
    assert len(data)<100_000_000 and not any(re.search(x,data)for x in patterns),name
    dst=out/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst)
    files.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest().upper()})
manifest={'package':'SCIENCE_ADK5556_4X4_R21_PLACEMENT_ONLY_TWO_RECTANGULAR_CANDIDATES_V1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':files,'scope':'All own placement/report/source/geometry/failures/review files; no native SQLite or third-party PDF/HTML included','excludedExternalInputs':[{'path':r['path'],'sha256':r['sha256'],'reason':'Read-only existing source. Not new delivery file; official PDF and raw native archive remain historical/local.'}for r in json.loads((P/'INPUT_SHA_MANIFEST.json').read_text(encoding='utf8'))]}
(out/'SHA256_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
with zipfile.ZipFile(out/'COMPLETE_SOURCE_AND_EVIDENCE.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
    for r in files:z.write(out/r['path'],r['path'])
    z.write(out/'SHA256_MANIFEST.json','SHA256_MANIFEST.json')
oldroot=(PREV/'payload/ROOT_README.md').read_text(encoding='utf8')
(out/'ROOT_README.md').write_text(f'''# Latest: Pro23 A/B visual drafts; placement acceptance BLOCKED

[A/B comparison]({folder}/PLACEMENT_AB_COMPARISON.png) · [Full receipt]({folder}/COMPLETE_PLACEMENT_RECEIPT.md) · [A coordinates]({folder}/PLACEMENT_A.csv) · [B coordinates]({folder}/PLACEMENT_B.csv) · [Body sources]({folder}/BODY_SOURCE_REGISTER.csv) · [74 actual pin-distance comparisons]({folder}/KEY_PIN_DISTANCE_COMPARISON.csv) · [Gates]({folder}/GATES.json).

Both176 real-scale components/552pads; no trace/via/pour, CAD0. Nativebody graphics for175 components, conservative official-dimension FFC outline with exact datum mechanical HOLD. FFC body/actuator datum STOP, key-distance full coverage and pad-proxy full coverage HOLD; drawings are unaccepted visual drafts. Choosing A/B does not release these gates. New unified bounded ruling required before further geometry or board changes. No manufacture/bench release. Complete own CSV/PNG/source/failed attempts/review direct; ZIP supplemental.

---

'''+oldroot,encoding='utf8')
sha=lambda n:hashlib.sha256((out/n).read_bytes()).hexdigest().upper()
summary={'sourceFilesDelivered':len(files),'payloadFiles':len(files)+3,'reportSHA256':sha('COMPLETE_PLACEMENT_RECEIPT.md'),'manifestSHA256':sha('SHA256_MANIFEST.json'),'zipSHA256':sha('COMPLETE_SOURCE_AND_EVIDENCE.zip'),'zipBytes':(out/'COMPLETE_SOURCE_AND_EVIDENCE.zip').stat().st_size,'credentialScan':'PASS actual credential/key value shapes absent','scopeOnlyThisCircuit':True,'rawSQLiteUploaded':False,'newCAD':0}
(D/'PREPARE_AND_SCAN.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
print(json.dumps(summary))
