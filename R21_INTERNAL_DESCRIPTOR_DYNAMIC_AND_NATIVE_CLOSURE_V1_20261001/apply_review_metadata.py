"""Evidence-only corrections: no descriptor builds, numerical recomputation or solver."""
from pathlib import Path
import json,hashlib,re,shutil,ast,datetime
r=Path(__file__).resolve().parent;ev=r/'evidence';corrections=[]
p=r/'LOCAL_QUALIFICATION_CASES.json';shutil.copyfile(p,ev/'LOCAL_QUALIFICATION_CASES_BEFORE_SHA_CORRECTION.json');cases=json.loads(p.read_text())
for c in cases:
 old=c['netlistSHA256'];actual=hashlib.sha256((r/'cases'/(c['name']+'.cir')).read_bytes()).hexdigest();c['originalInMemoryLFSHA256']=old;c['netlistSHA256']=actual;c['shaMeaning']='actual on-disk bytes';corrections.append({'case':c['name'],'previousInMemorySHA256':old,'actualFileSHA256':actual,'reason':'LF text was hashed before Windows newline translation; raw netlists unchanged'})
p.write_text(json.dumps(cases,indent=2));(ev/'NETLIST_SHA_CORRECTION.json').write_text(json.dumps(corrections,indent=2))
paths=[r/'results/PROCESSED_FOLLOWER_STAMP_MAP.json']+list((r/'results').glob('qual_*/STAMP_MAP.json'))
for p in paths:
 shutil.copyfile(p,ev/(p.parent.name+'_'+p.name+'_BEFORE_LINE_ANNOTATION.json'));data=json.loads(p.read_text());stamps=data['stamps'];source=Path(stamps[0]['source']);lines=source.read_text(errors='replace').splitlines()
 for stamp in stamps:
  card=stamp['line'];pattern=r'\s*'+str(card)+r'\s*:\s*'+re.escape(stamp['original'])+r'\s*';matches=[i for i,line in enumerate(lines,1)if re.fullmatch(pattern,line.lower())]
  stamp['listingCardNumber']=card;stamp['lineFieldMeaning']='ngspice expanded deck card number, not source file physical line';stamp['physicalLogLine']=matches[0]if matches else None
 data['processedToFrozenOriginalLIBSourceBridgeQualified']=False;data['mappingScope']='Actual expanded listing source is auditable; complete transformed primitive to original frozen library bridge not closed.';p.write_text(json.dumps(data,indent=2))
syntax=[]
for p in r.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'));syntax.append(p.name)
(ev/'POST_REVIEW_STATIC_SYNTAX_CHECK.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':syntax,'PASS':True,'scientificReruns':0,'regressionsRerun':0,'runtimeControlQualification':False},indent=2))
p=r/'progress.md';p.write_text(p.read_text().replace('Task1 inprogress; upstream scientific package ledgers frozen.','Task1 P0 BLOCKED: REF2 exact comparison fails; science sticky STOP. Upstream scientific package ledgers frozen. Final review source-line/SHA corrections and launch-control guards added without science or regression rerun. Successor monitor required before final handoff ends.'))
print(json.dumps({'metadataCorrections':len(corrections),'sourceMapsAnnotated':len(paths),'pythonStaticSyntaxPASS':len(syntax),'newScience':0}))
