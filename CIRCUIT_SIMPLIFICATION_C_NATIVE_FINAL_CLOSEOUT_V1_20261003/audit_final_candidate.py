from pathlib import Path
import json,re,csv,hashlib,sys
p=Path(__file__).parent;label=sys.argv[1];a=json.loads((p/(label+'.json')).read_text(encoding='utf-8'))['parsed']['value'];plan=json.loads((p/'FINAL_BUILD_PLAN.json').read_text(encoding='utf-8'));parts={q['ref']:q for pg in a['pages']for q in pg['parts']};want={q['ref']:q for q in plan['parts']};raw=bytes(a['actualFile']['bytes']);t=raw.decode('utf-8').replace('\r','');nets={};mapping={};dupes=[]
for m in re.finditer(r'^\(\s*\n([^\n]+)\n([\s\S]*?)^\)\s*$',t,re.M):
 net=m.group(1).strip();ms=[x.split()[0]for x in m.group(2).splitlines()if x.strip()];nets[net]=ms
 for key in ms:
  if key in mapping:dupes.append(key)
  mapping[key]=net
rows=[];errors=[]
if set(parts)!=set(want):errors.append({'referenceSetMismatch':sorted(set(parts)^set(want))})
for ref,q in want.items():
 if ref not in parts:continue
 z=parts[ref]
 if {k['number']for k in z['pins']}!=set(q['nets']):errors.append({'ref':ref,'pinSetMismatch':True})
 if z['name']!=q['value']:errors.append({'ref':ref,'nameMismatch':True})
 for pin in z['pins']:
  net=q['nets'][pin['number']];got=mapping.get(ref+'-'+pin['number']);ok=(net==got and not pin['nc'])if net else(pin['nc']and got is None);rows.append({'ref':ref,'pin':pin['number'],'name':pin['name'],'expectedNet':net,'actualNet':got,'NC':pin['nc'],'match':ok})
  if not ok:errors.append(rows[-1])
for ref in ['D_FFC_ROW','D_FFC_COL']:
 props={v['key']:v['value']for v in parts[ref]['materialAttrs']}
 if props.get('Manufacturer')!='Texas Instruments' or props.get('Manufacturer Part')!='TPD4E05U06DQAR' or props.get('MPN')!='TPD4E05U06DQAR':errors.append({'ref':ref,'makerMPNMissing':props})
flags=[]
for block in re.findall(r'^\[\s*\n([\s\S]*?)^\]\s*$',t,re.M):
 ls=block.splitlines()
 if not ls:continue
 match=re.search(r'\{\s*Add into BOM\s*\}=\{(yes|no)\}',block,re.I)
 if match:flags.append({'ref':ls[0].strip(),'AddIntoBOM':match.group(1).lower()})
# Known Protel2 native flags have a different serialization; retain independent lines for evidence.
flaglines=[x for x in t.splitlines()if 'Add into BOM' in x]
yes=len(re.findall(r'^Add into BOM\nyes$',t,re.M));no=len(re.findall(r'^Add into BOM\nno$',t,re.M))
if yes!=101 or no!=0:errors.append({'actualBOMFlagsUnexpected':{'yes':yes,'no':no}})
if len(parts)!=101 or len(rows)!=363 or len(mapping)!=323 or len(nets)!=54 or sum(bool(x['NC'])for x in rows)!=40:errors.append({'actualCountsUnexpected':True})
summary={'parts':len(parts),'pins':len(rows),'connected':len(mapping),'nets':len(nets),'NC':sum(bool(x['NC'])for x in rows),'matchingPins':sum(x['match']for x in rows),'allPinNetsMatchPlan':not errors and not dupes,'errors':errors,'duplicateMembership':dupes,'rawFileSHA256':hashlib.sha256(raw).hexdigest().upper(),'rawFileBytes':len(raw),'actualNativeBOMYes':yes,'actualNativeBOMNo':no,'DNPPartCount':sum(z['props'].get('DNP')=='yes'for z in parts.values()),'TPDManufacturerMPNConfirmed':not any(x.get('makerMPNMissing')for x in errors),'domain':'actualcandidate, no systemperformance/PCB qualification'}
own={'pages':a['pages'],'pinNetMap':mapping}
# Project metadata stays in local raw; source copied separately below for direct editable evidence.
for pg in own['pages']:
 source=pg.pop('source');src=p/'ACTUAL_SCH_SOURCE';src.mkdir(exist_ok=True);(src/(label+'_'+pg['page']['uuid']+'.esch')).write_text(source,encoding='utf-8')
(p/(label+'_ACTUAL_PARTS_AND_NETS.json')).write_text(json.dumps(own,ensure_ascii=False,indent=2),encoding='utf-8');(p/(label+'_AUDIT.json')).write_text(json.dumps(summary,indent=2),encoding='utf-8');(p/(label+'_RAW.net')).write_bytes(raw)
with(p/(label+'_ALL_PINS.csv')).open('w',encoding='utf-8',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with(p/(label+'_ACTUAL_BOM.csv')).open('w',encoding='utf-8',newline='')as f:
 fields=['ref','name','association','footprint','Manufacturer','ManufacturerPart','MPN','DNP'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for ref,z in parts.items():
  attrs={v['key']:v['value']for v in z['materialAttrs']};w.writerow({'ref':ref,'name':z['name'],'association':z['association'].get('name'),'footprint':z['footprint'].get('name')if z['footprint']else None,'Manufacturer':attrs.get('Manufacturer'),'ManufacturerPart':attrs.get('Manufacturer Part'),'MPN':attrs.get('MPN'),'DNP':z['props'].get('DNP','no')})
print(json.dumps(summary));print('Flaglines',flaglines[:2]);assert not errors and not dupes
