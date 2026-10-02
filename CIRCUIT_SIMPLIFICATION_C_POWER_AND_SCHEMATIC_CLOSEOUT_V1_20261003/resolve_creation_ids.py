from pathlib import Path
import json,re
from association_guard import validate_creation_id
p=Path(__file__).parent
old=json.loads((p.parent/'FIRST_BUILD_ELECTRICAL_CLOSURE_AND_SCHEMATIC_R2_V1'/'R2_PLAN.json').read_text(encoding='utf-8'))
lookup={q['device']:q for q in old['parts']}
lookup['GRM1885C1H220JA01D']={'device_uuid':'3d240fa64e4f48b1bdeb9f0c19efceb7','library_uuid':'0819f05c4eef4c71ace90d822a990e87'}
plan=json.loads((p/'C_NATIVE_BUILD_PLAN.json').read_text(encoding='utf-8'));changes=[]
for q in plan['parts']:
 if q['ref']!='J2' and len(q['association']['uuid'])==16:
  source=lookup[q['association']['name']]
  changes.append({'ref':q['ref'],'imported':q['association']['uuid'],'catalog':source['device_uuid'],'creationMPN':q['association']['name']})
  q['association']={'libraryUuid':source['library_uuid'],'uuid':source['device_uuid']}
 validate_creation_id(q)
(p/'C_NATIVE_BUILD_PLAN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
(p/'CREATION_ID_CORRECTION.json').write_text(json.dumps({'hypothesis':'Imported16char device association differs from recorded32char catalog creation UUID; first pending create wasJ1','changes':changes,'nativeSuccessStillUnverified':True,'firstSessionClosed':True,'sourceAndCopyUnchangedAfterClose':True},indent=2),encoding='utf-8')
print(json.dumps({'correctedReferences':len(changes),'validatedCreationInputs':len(plan['parts']),'notAFinalNativeClaim':True}))
