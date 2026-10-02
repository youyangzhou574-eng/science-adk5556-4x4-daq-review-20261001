from pathlib import Path
import json,shutil,hashlib,re,datetime,zipfile
P=Path(__file__).parent;D=P.parent/'GITHUB_J2_FFC_DELIVERY_20261002';D.mkdir(exist_ok=True)
previous=P.parent/'GITHUB_FAB_INPUT_CLOSURE_DELIVERY_20261002'
folder='R21_J2_FFC_FPC_INTERFACE_CORRECTION_V1_20261002'
for n in ['github_delivery.py','run_network.py','public_batch.py']:
 text=(previous/n).read_text('utf8').replace('R21_FAB_AND_ASSEMBLY_RELEASE_INPUT_CLOSURE_V1_20261002',folder)
 text=text.replace('Deliver R18 read-only fabrication, structural176 BOM and8wire harness inputs; no manufacturing release','Deliver Pro20 FFC J2 warm implementation and honest cold closure blockers; no physical release')
 text=text.replace('COMPLETE_FAB_INPUT_CLOSURE_RECEIPT.md','COMPLETE_FFC_CORRECTION_RECEIPT.md').replace('BOM_STRUCTURAL_176.csv','J2_ACTUAL_SIGNAL_AND_MECHANICAL_PADS.csv').replace('DEFAULT_FAB_PARAMETERS.csv','ACTUAL_552_PAD_NET.csv').replace('J2_PINOUT_AND_BODY.png','J2_FFC_ACTUAL_WARM_DETAIL.png').replace('J2_HARNESS_BUILD_SPEC.md','J2_FFC_CABLE_SPEC.md')
 (D/n).write_text(text,'utf8')
out=D/'payload';assert not out.exists();out.mkdir()
patterns=[rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'github_pat_[A-Za-z0-9_]{50,}',rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',rb'(?i)(?:password|passwd|api_key|access_token)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}[\"\x27]']
files=[];excluded=[]
for p in sorted(P.rglob('*')):
 if not p.is_file()or'__pycache__'in p.parts:continue
 n=p.relative_to(P).as_posix();data=p.read_bytes();sha=hashlib.sha256(data).hexdigest().upper()
 if 'sources_local_only' in p.parts or p.suffix.lower()in['.eprj2','.eprj2-wal','.eprj2-shm'] or 'eprj2-'in p.name:
  excluded.append({'path':n,'bytes':len(data),'sha256':sha,'reason':'native account SQLite not credential-safe; preserve locally only'if'.eprj2'in p.name else'thirdparty full PDF/HTML/extract/page image local-only; own summary/official links public'})
  continue
 assert len(data)<100_000_000,n
 assert not any(re.search(x,data)for x in patterns),n
 dst=out/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst)
 files.append({'path':n,'bytes':len(data),'sha256':sha})
manifest={'package':'SCIENCE_ADK5556_4X4_R21_J2_FFC_FPC_INTERFACE_CORRECTION_V1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sourceScope':'Complete own warm source/captures/CSV/PNG/report/failures. Native SQLite and thirdpartybulk deliberately excluded. No successful real epro2 File, no cold PASS.','files':files,'excludedLocalOnly':excluded,'selfAndArchiveExcluded':True}
(out/'SHA256_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf8')
with zipfile.ZipFile(out/'COMPLETE_SOURCE_AND_EVIDENCE.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for row in files:z.write(out/row['path'],row['path'])
 z.write(out/'SHA256_MANIFEST.json','SHA256_MANIFEST.json')
rootprev=(previous/'payload/ROOT_README.md').read_text('utf8')
(out/'ROOT_README.md').write_text(f'''# Latest: Pro20 actual FFC/FPC J2 warm ECO; independent cold closure blocked

[Full receipt]({folder}/COMPLETE_FFC_CORRECTION_RECEIPT.md) · [Index]({folder}/README.md) · [Actual local picture]({folder}/J2_FFC_ACTUAL_WARM_DETAIL.png) · [Whole PCB picture]({folder}/PCB_FINAL_WARM_REVIEW.png) · [8 signal +2 mechanical pads]({folder}/J2_ACTUAL_SIGNAL_AND_MECHANICAL_PADS.csv) · [Gates]({folder}/GATES.json).

User clarified thin FFC/FPC ribbon ZIF slot. Default2005290081+154670229 is Pro20 authorized1mm set, not userconfirmed existingcable spec. Warm176/552/514/107/36+2 andDRC0; other175 frozen. Cold calls failed, realFile export0; CONTACT-side native text/legacy3D/name pending. CurrentFFC PCB_REVIEW_READY=false. No purchase/manufacture/bench/powerup. HistoricalKK interface no longer fulfills user requirement. Own readable/raw evidence direct; local account .eprj2 and thirdpartybulk excluded withSHA.

---

'''+rootprev,'utf8')
sha=lambda n:hashlib.sha256((out/n).read_bytes()).hexdigest().upper()
r={'sourceFilesDelivered':len(files),'payloadFiles':len(files)+3,'excludedLocalFiles':len(excluded),'reportSHA256':sha('COMPLETE_FFC_CORRECTION_RECEIPT.md'),'manifestSHA256':sha('SHA256_MANIFEST.json'),'zipSHA256':sha('COMPLETE_SOURCE_AND_EVIDENCE.zip'),'zipBytes':(out/'COMPLETE_SOURCE_AND_EVIDENCE.zip').stat().st_size,'sourceBytes':sum(x['bytes']for x in files),'credentialScan':'PASS public actual-token/private-key/value shapes absent; entire native account SQLite excluded','rawDBUploaded':False,'actualNativeFileSuccess':0,'scopeOnlyThisCircuit':True}
(D/'PREPARE_AND_SCAN.json').write_text(json.dumps(r,indent=2),'utf8');print(json.dumps(r))
