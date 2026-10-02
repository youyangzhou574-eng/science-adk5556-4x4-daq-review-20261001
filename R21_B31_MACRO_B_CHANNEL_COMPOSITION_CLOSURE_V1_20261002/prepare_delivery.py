from pathlib import Path
import json,hashlib,zipfile,shutil,re,urllib.request
P=Path(__file__).parent;R=P.parent;D=R/'GITHUB_B31_MACRO_B_DELIVERY_20261002';D.mkdir(exist_ok=True);Q=D/'payload';Q.mkdir(exist_ok=True)
assert (P/'FINAL_REVIEW.md').exists() and (P/'REVIEW_DISPOSITION.md').exists()
assert json.loads((P/'EXECUTION_BUDGET.json').read_text())['status']=='COMPLETE_BLOCKED'
files=sorted(x for x in P.rglob('*') if x.is_file() and '__pycache__' not in x.relative_to(P).parts)
pat=re.compile(r'gh[pousr]_[A-Za-z0-9_]{25,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer\s+[A-Za-z0-9_.-]{25,}')
scan=[]
for x in files:
 assert x.suffix.lower() not in ['.db','.sqlite','.sqlite3','.eprj2','.pdf','.html']
 if x.suffix.lower() in ['.txt','.md','.json','.csv','.py','.log']:
  assert not pat.search(x.read_text(encoding='utf-8-sig',errors='replace')),'Credential-shaped value; not printed; stop'
 scan.append({'name':x.relative_to(P).as_posix(),'bytes':x.stat().st_size,'SHA256':hashlib.sha256(x.read_bytes()).hexdigest().upper()})
for x in files:
 d=Q/x.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(x,d)
manifest={'package':P.name,'ownPublicFiles':scan,'onlyOwnFiles':True,'thirdPartyBulk':False,'accountSQLite':False,'reportSHA256':hashlib.sha256((P/'COMPLETE_B31_RECEIPT.md').read_bytes()).hexdigest().upper()}
(Q/'PUBLIC_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
with zipfile.ZipFile(Q/'B31_COMPLETE_OWN_REVIEW_EVIDENCE.zip','w',zipfile.ZIP_DEFLATED) as z:
 for x in files:z.write(x,x.relative_to(P).as_posix())
repo='youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001';folder=P.name+'_20261002'
raw=urllib.request.urlopen(urllib.request.Request('https://raw.githubusercontent.com/'+repo+'/main/README.md',headers={'User-Agent':'Codex-circuit-index'}),timeout=20).read().decode('utf8')
append='\n\n## B31 Macro B channel composition, 2026-10-02\n\n[Complete review directory]('+folder+'/README.md). OnlyPASS1 complete; 176/552 frozen geometry,15400body/proxy0,106key no increase, fullTIA/ROW role templates. ROW+7.31/+7.39mm and power+2.545mm vsB22 remainHOLD, pass2/3 failures and hard STOP retained. Two actual HOLD PNGs, readableCSV/JSON/fullreport/failures. CAD/native/routing0; user visual acceptance pending.\n'
(Q/'ROOT_README.md').write_text(raw+append,encoding='utf8')
old=R/'GITHUB_B3_REFERENCE_DELIVERY_20261002';code=(old/'github_delivery.py').read_text().replace("folder = 'R21_B3_REFERENCE_DRIVEN_PINOUT_FLOORPLAN_REBUILD_V1_20261002'","folder = '"+folder+"'").replace('Deliver B3 reference-driven pinout placement collision-blocked review; CAD0','Deliver B31 Macro B complete-cell placement and chain-HOLD review; CAD0')
(D/'github_delivery.py').write_text(code,encoding='utf8');shutil.copyfile(old/'run_network.py',D/'run_network.py')
prep={'directory':folder,'publicSourceCount':len(files),'newRemoteObjects':len(files)+3,'reportSHA256':manifest['reportSHA256'],'manifestSHA256':hashlib.sha256((Q/'PUBLIC_MANIFEST.json').read_bytes()).hexdigest().upper(),'ZIPBytes':(Q/'B31_COMPLETE_OWN_REVIEW_EVIDENCE.zip').stat().st_size,'ZIPSHA256':hashlib.sha256((Q/'B31_COMPLETE_OWN_REVIEW_EVIDENCE.zip').read_bytes()).hexdigest().upper()}
(D/'PAYLOAD_PREPARATION.json').write_text(json.dumps(prep,indent=2),encoding='utf8');(D/'PUBLIC_SOURCE_SCAN.json').write_text(json.dumps({'credentialMatches':0,'files':scan},indent=2),encoding='utf8');print(json.dumps(prep))
