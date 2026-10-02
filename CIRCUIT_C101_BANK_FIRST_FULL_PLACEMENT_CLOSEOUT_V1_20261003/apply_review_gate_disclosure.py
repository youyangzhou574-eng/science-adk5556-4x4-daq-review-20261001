from pathlib import Path
import json,hashlib
P=Path(__file__).parent
assert not (P/'PRE_REVIEW_GATES.json').exists(),'One disclosure pass only'
protected=['P1_FULL_PLACEMENT.csv','P1_FULL_PLACEMENT.json','P1_FULL_LAYOUT_REVIEW.png','ADC_BANK_AND_TIA_DETAIL.png','EXECUTION_BUDGET.json']
sha={n:hashlib.sha256((P/n).read_bytes()).hexdigest()for n in protected}
for n in ['GATES.json','FULL_OFFLINE_AUDIT.json']:(P/('PRE_REVIEW_'+n)).write_bytes((P/n).read_bytes())
g=json.loads((P/'GATES.json').read_text());g.update(J2_PIN_SIDE_ROW_ADJACENCY_HOLD=True,ALL_MACRO_LAYOUT_INTENTS_ACCEPTED=False,NATIVE_PLACEMENT_ELIGIBLE=False,FINAL_REVIEW_IMPORTANT_OPEN=1,USER_VISUAL_ACCEPTANCE='PENDING_ENGINEERING_DIRECTION_DISPOSITION_AND_HUMAN')
(P/'GATES.json').write_text(json.dumps(g,indent=2),encoding='utf-8')
a=json.loads((P/'FULL_OFFLINE_AUDIT.json').read_text());a.update(ROWPinSideContractAccepted=False,J2_ROWPlannedPinsWorld={'xMm':6,'yMm':[25.5,26.5,27.5,28.5]},J2_COLPlannedPinsWorld={'xMm':6,'yMm':[29.5,30.5,31.5,32.5]},ROWMacroAbovePlannedROWSide=True,allMacroIntentAccepted=False,reviewDirectionFinding='I1 still requires Pro explicit acceptance or new local correction scope')
(P/'FULL_OFFLINE_AUDIT.json').write_text(json.dumps(a,indent=2),encoding='utf-8')
assert all(hashlib.sha256((P/n).read_bytes()).hexdigest()==h for n,h in sha.items())
(P/'REVIEW_DISCLOSURE_PROTECTED_SHA.json').write_text(json.dumps({'protectedSHA':sha,'unchanged':True,'newCoordinatesImagesScience':0},indent=2),encoding='utf-8')
print(json.dumps({'ImportantEngineeringHOLD':True,'complete101GeometryRetained':True,'protectedUnchanged':True}))
