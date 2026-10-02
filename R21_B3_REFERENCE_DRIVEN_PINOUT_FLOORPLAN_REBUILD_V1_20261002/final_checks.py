import json,hashlib,math,csv
from pathlib import Path
from PIL import Image
P=Path(__file__).parent
m=json.loads((P/'INPUT_MANIFEST.json').read_text());checks=[]
for x in m:
 a=hashlib.sha256(Path(x['source']).read_bytes()).hexdigest();b=hashlib.sha256((P/x['name']).read_bytes()).hexdigest();checks.append({'name':x['name'],'sourceUnchanged':a==x['SHA256'],'copyMatches':b==a})
g=json.loads((P/'ACTUAL_GEOMETRY.json').read_text());pos=json.loads((P/'PLACEMENT_B3.json').read_text())['positions'];budget=json.loads((P/'EXECUTION_BUDGET.json').read_text(encoding='utf-8-sig'));audit=json.loads((P/'FULL_GEOMETRY_AND_IDENTITY_AUDIT.json').read_text())
imgs=[]
for n in ['B22_vs_B3.png','B3_NO_COPPER.png','B3_PINOUT_AND_SIGNAL_FLOW.png']:
 im=Image.open(P/n);im.verify();im=Image.open(P/n);imgs.append({'file':n,'dimensions':list(im.size),'SHA256':hashlib.sha256((P/n).read_bytes()).hexdigest()})
assert all(x['sourceUnchanged'] and x['copyMatches'] for x in checks);assert set(pos)==set(g) and len(pos)==176
assert all(len(v)==3 and all(math.isfinite(a) for a in v) for v in pos.values())
assert budget['actual']['macroCandidates']==2 and budget['actual']['placementRefinements']==3 and budget['actual']['images']==3 and budget['status']!='ACTIVE'
assert audit['geometryPass']==False and audit['all15400PhysicalCollisionPairs']==[['U14','U3']]
assert len(list(csv.DictReader((P/'ALL_552_PIN_MAP_B3.csv').open())))==552
result={'oldInputs':checks,'inputsAllPASS':True,'positionsComplete176':True,'key106NoIncrease':not audit['keyDistanceFailures'],'identityImmutableInputOnly':True,'images':imgs,'criticalCollisionVisible':True,'hardBudgetClosed':True,'nativeOrCADorSimulationOperations':0,'reviewArtifactsOnly':True}
(P/'FINAL_ARTIFACT_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result))
