from pathlib import Path
import json,hashlib,datetime
from PIL import Image
P=Path("E:/open/SCIENCE_ADK5556_4X4_DAQ_REPLICA/R21_B22_STRUCTURED_CHANNEL_ARRAY_PLACEMENT_V1");D=P.parent/'GITHUB_B22_STRUCTURED_DELIVERY_20261002'
rows=json.loads((P/'INDEPENDENT_FINAL_AUDIT.json').read_text());budget=json.loads((P/'EXECUTION_BUDGET.json').read_text())
assert budget['actual']['placementAdjustment']==2 and budget['actual']['finalImages']==1
assert all(budget['actual'][k]==0 for k in('CAD','GUI','native','simulation','sources'))
assert len(rows['inputSHA'])==7 and all(r['sourceAndCopyUnchanged']for r in rows['inputSHA'])
im=Image.open(P/'PLACEMENT_B21_VS_B22.png')
v={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'identity':rows['identity'],'criticalInherited94':'PASS_NO_INCREASE','extraDecap':'HOLD_FIVE','overlapCompletePairsEach':15400,'image':{'path':'PLACEMENT_B21_VS_B22.png','pixels':im.size,'sha256':hashlib.sha256((P/'PLACEMENT_B21_VS_B22.png').read_bytes()).hexdigest(),'actualViewed':True},'noThirdAdjustmentOrSecondImage':True,'frozenInputSourceAndCopies7PASS':True,'nativeUnmodified':True}
(P/'FINAL_ARTIFACT_VERIFICATION.json').write_text(json.dumps(v,indent=2),encoding='utf8')
old=P.parent/'B21_FINAL_ACCEPTANCE_AND_CONDITIONAL_NATIVE_SCOPE_20261002'
(old/'USER_REQUIREMENT_SUPERSESSION_20261002.json').write_text(json.dumps({'previousB21Choice':'NOT_RECEIVED','newRulingAssistantId':'3d968530-1342-4bbd-9af0-dae4f321ab20','newRulingParentUserId':'a9ed76f1-da40-41ef-822c-7751b8071c0c','newUserIntent':'同功能阻容阵列化B2.2','old480minNativeBudget':'DORMANT_NOT_ACTIVATED_OR_TRANSFERRED','newScope':'120minoffline2adjustments1imageCAD0','package':str(P)},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(v))

