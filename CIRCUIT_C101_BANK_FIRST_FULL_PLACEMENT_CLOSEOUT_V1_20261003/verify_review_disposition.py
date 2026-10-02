from pathlib import Path
import json,hashlib
P=Path(__file__).parent;g=json.loads((P/'GATES.json').read_text());a=json.loads((P/'FULL_OFFLINE_AUDIT.json').read_text());b=json.loads((P/'EXECUTION_BUDGET.json').read_text())
assert g.get('J2_PIN_SIDE_ROW_ADJACENCY_HOLD')is True,'Missing actual J2/ROW side-conflict engineering HOLD'
assert g.get('ALL_MACRO_LAYOUT_INTENTS_ACCEPTED')is False,'Geometry review must not promote macrointent acceptance'
assert g.get('NATIVE_PLACEMENT_ELIGIBLE')is False and not g['CAD_RELEASED']and not g['PCB_ROUTING_RELEASED']
assert a['all101Placed']and a['all363ActualPinNetIdentityUnchanged']and a['all5050BodyAndPhysicalProxyNoOverlap']
assert a.get('ROWPinSideContractAccepted')is False
assert b['STOP']and b['coordinateSTOP']and b['spent']['placement']==2 and b['spent']['image']==2
assert 'ROW_PIN_SIDE_ADJACENCY' in (P/'REVIEW_DISPOSITION.md').read_text(encoding='utf-8')
for q in json.loads((P/'INPUT_SHA_REGISTER.json').read_text()):
 assert hashlib.sha256((P/q['copy']).read_bytes()).hexdigest()==q['sha256']
print(json.dumps({'reviewGateFixChecks':7,'GREEN':True,'newCoordinatesImagesScience':0}))
