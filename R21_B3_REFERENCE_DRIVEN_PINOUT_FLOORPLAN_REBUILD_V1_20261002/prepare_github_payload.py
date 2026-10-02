from pathlib import Path
import json,csv,hashlib,zipfile,shutil,re,urllib.request,datetime
P=Path(__file__).parent;R=P.parent;D=R/'GITHUB_B3_REFERENCE_DELIVERY_20261002';D.mkdir(exist_ok=True);Q=D/'payload';Q.mkdir(exist_ok=True)
assert (P/'FINAL_REVIEW.md').exists() and (P/'REVIEW_DISPOSITION.md').exists()
assert json.loads((P/'EXECUTION_BUDGET.json').read_text(encoding='utf-8-sig'))['status']!='ACTIVE'
files=sorted(x for x in P.rglob('*') if x.is_file() and not any(p in ['sources_local_only','__pycache__'] for p in x.relative_to(P).parts))
private=[]
for x in (P/'sources_local_only').glob('*'):
 if x.is_file():private.append({'name':x.name,'bytes':x.stat().st_size,'SHA256':hashlib.sha256(x.read_bytes()).hexdigest(),'reason':'third-party bulk PDF/HTML or selected source page; local-only, original URL and own short note public'})
scan=[]
pat=re.compile(r'gh[pousr]_[A-Za-z0-9_]{25,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer\s+[A-Za-z0-9_.-]{25,}')
for x in files:
 assert x.suffix.lower() not in ['.db','.sqlite','.sqlite3','.eprj2']
 if x.suffix.lower() in ['.txt','.md','.json','.csv','.py','.log']:
  text=x.read_text(encoding='utf-8-sig',errors='replace');hits=list(pat.finditer(text))
  assert not hits,'Credential-shape match, stop; value not printed'
 scan.append({'name':x.relative_to(P).as_posix(),'bytes':x.stat().st_size,'SHA256':hashlib.sha256(x.read_bytes()).hexdigest().upper()})
(D/'PUBLIC_SOURCE_SCAN.json').write_text(json.dumps({'actualCredentialShapeMatches':0,'privateExcluded':private,'ownPublicCount':len(files),'checks':scan},indent=2),encoding='utf8')
for x in files:
 dest=Q/x.relative_to(P);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(x,dest)
manifest={'package':P.name,'publicOwnFiles':scan,'privateExcluded':private,'notOnlyZIP':True,'noLFS':True,'referenceBulkPublished':False,'zeroCredentialsPublished':True,'reportSHA256':hashlib.sha256((P/'COMPLETE_B3_RECEIPT.md').read_bytes()).hexdigest().upper()}
(Q/'PUBLIC_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
with zipfile.ZipFile(Q/'B3_COMPLETE_OWN_REVIEW_EVIDENCE.zip','w',zipfile.ZIP_DEFLATED) as z:
 for x in files:z.write(x,x.relative_to(P).as_posix())
repo='youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001';folder='R21_B3_REFERENCE_DRIVEN_PINOUT_FLOORPLAN_REBUILD_V1_20261002'
rooturl='https://raw.githubusercontent.com/'+repo+'/main/README.md'
raw=urllib.request.urlopen(urllib.request.Request(rooturl,headers={'User-Agent':'Codex-circuit-index'}),timeout=20).read().decode('utf8')
append='\n\n## B3 reference-driven placement, 2026-10-02\n\n[Complete review directory]('+folder+'/README.md). All176parts/19IC-connectors rebuilt from actual pin neighborhoods. U3/U14 physical-pad-proxy overlap BLOCKS acceptance. 106key distances non-increasing, old-six-block rigid reuse audit passes; aesthetics/user selection and full repeated-cell uniformity not accepted. 3readablePNG + all552pinCSV + full evidence. No CAD/routing/native/boardoutline/bench or manufacture.\n'
(Q/'ROOT_README.md').write_text(raw+append,encoding='utf8')
oldD=R/'GITHUB_B22_STRUCTURED_DELIVERY_20261002'
code=(oldD/'github_delivery.py').read_text();code=code.replace("folder = 'R21_B22_STRUCTURED_CHANNEL_ARRAY_PLACEMENT_V1_20261002'","folder = '"+folder+"'");code=code.replace('Deliver B2.2 structured-channel placement and actual-pin audit; CAD0','Deliver B3 reference-driven pinout placement collision-blocked review; CAD0')
(D/'github_delivery.py').write_text(code,encoding='utf8');shutil.copyfile(oldD/'run_network.py',D/'run_network.py')
summary={'directory':folder,'publicSourceCount':len(files),'newRemoteObjects':len(files)+3,'reportSHA256':manifest['reportSHA256'],'manifestSHA256':hashlib.sha256((Q/'PUBLIC_MANIFEST.json').read_bytes()).hexdigest().upper(),'ZIPBytes':(Q/'B3_COMPLETE_OWN_REVIEW_EVIDENCE.zip').stat().st_size,'ZIPSHA256':hashlib.sha256((Q/'B3_COMPLETE_OWN_REVIEW_EVIDENCE.zip').read_bytes()).hexdigest().upper()}
(D/'PAYLOAD_PREPARATION.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))
