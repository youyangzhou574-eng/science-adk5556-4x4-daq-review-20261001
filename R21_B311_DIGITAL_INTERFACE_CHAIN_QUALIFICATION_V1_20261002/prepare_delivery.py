from pathlib import Path
import json,hashlib,zipfile,shutil,re,urllib.request
P=Path(__file__).parent;R=P.parent;D=R/'GITHUB_B311_DIGITAL_CHAIN_DELIVERY_20261002';D.mkdir(exist_ok=True);Q=D/'payload';Q.mkdir(exist_ok=True)
assert (P/'FINAL_REVIEW.md').exists() and (P/'REVIEW_DISPOSITION.md').exists()
assert json.loads((P/'EXECUTION_BUDGET.json').read_text(encoding='utf8'))['status']=='COMPLETE_READONLY_WAIT_USER_VISUAL_SELECTION'
files=sorted(x for x in P.rglob('*') if x.is_file() and '__pycache__' not in x.relative_to(P).parts)
pat=re.compile(r'gh[pousr]_[A-Za-z0-9_]{25,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer\s+[A-Za-z0-9_.-]{25,}')
scan=[]
for x in files:
 assert x.suffix.lower() not in ['.db','.sqlite','.sqlite3','.eprj2','.pdf','.html']
 if x.suffix.lower() in ['.txt','.md','.json','.csv','.py','.log']:assert not pat.search(x.read_text(encoding='utf-8-sig',errors='replace')),'Credential-shape detected, value withheld'
 scan.append({'name':x.relative_to(P).as_posix(),'bytes':x.stat().st_size,'SHA256':hashlib.sha256(x.read_bytes()).hexdigest().upper()})
for x in files:
 d=Q/x.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(x,d)
manifest={'package':P.name,'ownPublicFiles':scan,'onlyOwnFiles':True,'thirdPartyBulk':False,'accountSQLite':False,'reportSHA256':hashlib.sha256((P/'COMPLETE_B311_RECEIPT.md').read_bytes()).hexdigest().upper()}
(Q/'PUBLIC_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
with zipfile.ZipFile(Q/'B311_COMPLETE_OWN_REVIEW_EVIDENCE.zip','w',zipfile.ZIP_DEFLATED) as z:
 for x in files:z.write(x,x.relative_to(P).as_posix())
repo='youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001';folder=P.name+'_20261002'
raw=urllib.request.urlopen(urllib.request.Request('https://raw.githubusercontent.com/'+repo+'/main/README.md',headers={'User-Agent':'Codex-circuit-index'}),timeout=20).read().decode('utf8')
append='\n\n## B311 digital interface qualification, 2026-10-02\n\n[Complete review directory]('+folder+'/README.md). FrozenB31 completePASS1; fiveactualMCU-seriesR-interface functional paths qualified for readonlyplacementgeometry. No coordinate changes.176/552/514/107/36+2MP,15400proxy0,106key/full8cells maintained. ROW/Power variances acceptedbyProforplacementonly. Uservisualchoicepending, CAD/native/routing0. OneactualPNG/readablechainsCSV/fullreport/manifestZIP. OldMacro rankingnotrewritten.\n'
(Q/'ROOT_README.md').write_text(raw+append,encoding='utf8')
old=R/'GITHUB_B31_MACRO_B_DELIVERY_20261002';code=(old/'github_delivery.py').read_text(encoding='utf8').replace("folder = 'R21_B31_MACRO_B_CHANNEL_COMPOSITION_CLOSURE_V1_20261002'","folder = '"+folder+"'").replace('Deliver B31 Macro B complete-cell placement and chain-HOLD review; CAD0','Deliver B311 readonly digital interface chains; frozen placement, user choice pending')
(D/'github_delivery.py').write_text(code,encoding='utf8');shutil.copyfile(old/'run_network.py',D/'run_network.py')
prep={'directory':folder,'publicSourceCount':len(files),'newRemoteObjects':len(files)+3,'reportSHA256':manifest['reportSHA256'],'manifestSHA256':hashlib.sha256((Q/'PUBLIC_MANIFEST.json').read_bytes()).hexdigest().upper(),'ZIPBytes':(Q/'B311_COMPLETE_OWN_REVIEW_EVIDENCE.zip').stat().st_size,'ZIPSHA256':hashlib.sha256((Q/'B311_COMPLETE_OWN_REVIEW_EVIDENCE.zip').read_bytes()).hexdigest().upper()}
(D/'PAYLOAD_PREPARATION.json').write_text(json.dumps(prep,indent=2),encoding='utf8');(D/'PUBLIC_SOURCE_SCAN.json').write_text(json.dumps({'credentialMatches':0,'files':scan},indent=2),encoding='utf8');print(json.dumps(prep))
