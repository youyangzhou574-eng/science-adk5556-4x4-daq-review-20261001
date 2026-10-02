"""Final structural delivery check; no coordinate refinement or native calls."""
from pathlib import Path
import json,csv,hashlib,math
P=Path(__file__).parent
G=json.loads((P/'ACTUAL_GEOMETRY.json').read_text(encoding='utf8'))
checks=[]
for a in'AB':
    rows=list(csv.DictReader((P/('PLACEMENT_'+a+'.csv')).open(encoding='utf-8-sig')))
    assert len(rows)==176 and len({r['Designator']for r in rows})==176
    assert set(r['Designator']for r in rows)==set(G)
    d=json.loads((P/('PLACEMENT_'+a+'.json')).read_text(encoding='utf8'))
    assert not d['metrics']['bodyOverlapPairs'] and not d['metrics']['conservativePadEnvelopeOverlapPairs']
    assert not d['metrics']['FFC2DKeepoutBodyCollisions']
    pairs=list(csv.DictReader((P/('KEY_PIN_DISTANCES_'+a+'.csv')).open(encoding='utf-8-sig')))
    assert len(pairs)==74 and max(float(r['deltaMm'])for r in pairs)<1e-8
    for r in pairs:
        ic=next(p for p in G[r['icRef']]['pads']if p['number']==r['icPad'])
        passive=next(p for p in G[r['passiveRef']]['pads']if p['number']==r['passivePad'])
        assert ic['net']==passive['net']==r['net']
        assert abs(math.hypot(ic['xMm']-passive['xMm'],ic['yMm']-passive['yMm'])-float(r['beforeMm']))<1e-8
    checks.append({'candidate':a,'rows':176,'uniqueRefs':176,'sameNetActualPadPairs':74,'bodyOverlapClaimMatchesFrozenAudit':True})
manifest=json.loads((P/'INPUT_SHA_MANIFEST.json').read_text(encoding='utf8'))
for r in manifest:assert hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256']
pngs=[P/('PLACEMENT_'+a+'_NO_COPPER.png')for a in'AB']+[P/'PLACEMENT_AB_COMPARISON.png']
from PIL import Image
images=[]
for p in pngs:
    with Image.open(p)as im:
        im.verify()
    with Image.open(p)as im:images.append({'file':p.name,'width':im.width,'height':im.height,'format':im.format,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
result={'checks':checks,'images':images,'inputHashesUnchanged':4,'nativeOperations':0,'classification':'STRUCTURAL_DELIVERY_CHECK_NOT_NEW_GEOMETRY_REFINEMENT_OR_SCIENTIFIC_VALIDATION'}
(P/'FINAL_ARTIFACT_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps({'candidates':2,'coordsRowsEach':176,'sameNetPairsEach':74,'verifiedPNGs':3,'frozenInputs':4,'nativeOperations':0}))
