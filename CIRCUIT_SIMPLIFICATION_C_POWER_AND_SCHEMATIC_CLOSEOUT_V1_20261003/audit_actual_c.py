from pathlib import Path
import csv,hashlib,json,re
p=Path(__file__).parent
j=json.loads((p/'C_FINAL_WARM_CAPTURE.json').read_text(encoding='utf-8'))['parsed']['value']
plan=json.loads((p/'C_NATIVE_BUILD_PLAN.json').read_text(encoding='utf-8'))
raw=bytes(j['actualFile']['bytes']);(p/'C_ACTUAL_WARM_RAW.net').write_bytes(raw)
t=raw.decode('utf-8').replace('\r','');mapping={};netmembers={};duplicates=[]
for m in re.finditer(r'^\(\s*\n([^\n]+)\n([\s\S]*?)^\)\s*$',t,re.M):
 net=m.group(1).strip();members=[x.split()[0]for x in m.group(2).splitlines()if x.strip()];netmembers[net]=members
 for member in members:
  if member in mapping and mapping[member]!=net:duplicates.append(member)
  mapping[member]=net
actual={q['ref']:q for pg in j['pages']for q in pg['parts']}
expected={q['ref']:q for q in plan['parts']};errors=[];rows=[]
for ref,q in expected.items():
 if ref not in actual:errors.append({'ref':ref,'missingPart':True});continue
 a=actual[ref]
 if {x['number']for x in a['pins']}!=set(q['nets']):errors.append({'ref':ref,'pinSetMismatch':True})
 for pin in a['pins']:
  key=ref+'-'+pin['number'];want=q['nets'].get(pin['number']);got=mapping.get(key);nc=pin['nc'];ok=(got==want and not nc)if want else(nc and got is None)
  rows.append({'ref':ref,'pin':pin['number'],'pinName':pin['name'],'expected':want,'actual':got,'NC':nc,'matches':ok})
  if not ok:errors.append(rows[-1])
 if a['name']!=q['value']:errors.append({'ref':ref,'valueNameExpected':q['value'],'actualName':a['name']})
 if q['dnp'] and a['props'].get('DNP')!='yes':errors.append({'ref':ref,'DNPmissing':True})
if set(actual)!=set(expected):errors.append({'actualRefSetDiff':sorted(set(actual)^set(expected))})
audit={'structuralParts':len(actual),'plannedPopulated':sum(not q['dnp']for q in plan['parts']),'DNPObserved':sum(q['props'].get('DNP')=='yes'for q in actual.values()),'pins':len(rows),'connected':sum(x['actual']is not None for x in rows),'nets':len(netmembers),'NC':sum(bool(x['NC'])for x in rows),'matchingPins':sum(x['matches']for x in rows),'errors':errors,'duplicateMembership':duplicates,'allActualPinNetsMatchPlan':not errors and not duplicates,'actualFileSHA256':hashlib.sha256(raw).hexdigest().upper(),'actualFileBytes':len(raw),'auditDomain':'Warm candidate only; no independent cold or performance certification','materialAndPowerHOLDs':plan['hold'],'DNPPhysicalRestorationQualified':False}
(p/'C_ACTUAL_WARM_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
(p/'C_ACTUAL_PARTS_AND_NETS.json').write_text(json.dumps({'pages':[{'page':pg['page'],'parts':pg['parts']}for pg in j['pages']],'pinNetMap':mapping},ensure_ascii=False,indent=2),encoding='utf-8')
with(p/'C_ACTUAL_ALL_PINS.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with(p/'C_ACTUAL_BOM.csv').open('w',encoding='utf-8',newline='')as f:
 fields=['ref','name','associationName','footprint','DNP','plannedPopulate','materialHold'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for ref,a in actual.items():w.writerow({'ref':ref,'name':a['name'],'associationName':a['association'].get('name'),'footprint':a['footprint'].get('name')if a['footprint']else None,'DNP':a['props'].get('DNP','no'),'plannedPopulate':not expected[ref]['dnp'],'materialHold':'TI maker missing'if ref.startswith('D_FFC')else 'J1/J3/J4 mating unknown'if ref in ['J1','J3','J4']else ''})
print(json.dumps({k:audit[k]for k in ['structuralParts','plannedPopulated','DNPObserved','pins','connected','nets','NC','matchingPins','allActualPinNetsMatchPlan']}));print('firstErrors',json.dumps(errors[:8]))
