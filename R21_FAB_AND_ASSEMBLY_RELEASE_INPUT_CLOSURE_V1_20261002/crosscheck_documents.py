from pathlib import Path
import json,hashlib,datetime,csv
P=Path(__file__).parent;OLD=P.parent/'R21_EXTERNAL_ARRAY_PLUGGABLE_INTERFACE_AND_FAB_INPUT_CONTRACT_V1'
now=datetime.datetime.now(datetime.timezone.utc)
b=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'))
assert b['status']=='ACTIVE_READONLY_DOCUMENTS_ONLY' and b['actual']['existingFrozenEvidencePass']==0
before=json.loads((P/'FROZEN_J2_SOURCE_HASHES_BEFORE.json').read_text('utf8'));after={}
for n,v in before.items():
 f=OLD/n;after[n]={'bytes':f.stat().st_size,'SHA256':hashlib.sha256(f.read_bytes()).hexdigest().upper()}
assert after==before
(P/'FROZEN_J2_SOURCE_HASHES_AFTER.json').write_text(json.dumps(after,indent=2),'utf8')
required=['PRO_FAB_INPUT_CLOSURE_RULING_FULL.md','FABRICATION_INPUT_CONTRACT.md','ASSEMBLY_RELEASE_INPUTS.md','J2_HARNESS_BUILD_SPEC.md','MANUFACTURING_RELEASE_CHECKLIST.md','COMPLETE_FAB_INPUT_CLOSURE_RECEIPT.md','BOM_STRUCTURAL_176.csv','BOM_GROUPED.csv','BOM_MISSING_MANUFACTURER_MPN.csv','J2_PINOUT_AND_BODY.png']
assert all((P/n).is_file()for n in required)
comp={}
for n in ['J2_PINOUT_AND_BODY.png','J2_ACTUAL_8PIN_HARNESS.csv','J2_CONNECTOR_AND_HARNESS_SPEC.md']:
 comp[n]={'sha256':hashlib.sha256((P/n).read_bytes()).hexdigest().upper(),'identicalToAccepted17':(P/n).read_bytes()==(OLD/n).read_bytes()}
assert all(v['identicalToAccepted17']for v in comp.values())
bom=list(csv.DictReader((P/'BOM_STRUCTURAL_176.csv').open(encoding='utf8')))
grp=list(csv.DictReader((P/'BOM_GROUPED.csv').open(encoding='utf8')))
assert len(bom)==176==len({r['Designator']for r in bom})
assert sum(int(r['Quantity'])for r in grp)==176
assert {r['Designator']for r in bom if not r['MPN']or not r['Manufacturer']}=={'J1','J3','J4'}
pins=list(csv.DictReader((P/'J2_ACTUAL_8PIN_HARNESS.csv').open(encoding='utf8')))
assert [r['PCB_net']for r in pins]==['ROW0','ROW1','ROW2','ROW3','COL0','COL1','COL2','COL3']
g=json.loads((P/'GATES.json').read_text('utf8'))
assert g['PCB_REVIEW_READY'] and g['J2_SILK_TEXT_VARIANCE_ACCEPTED'] and g['J2_NATIVE_SILK_ROWCOL_MISSING']
assert all(g[x]is False for x in ['MANUFACTURING_RELEASE','PROCUREMENT_RELEASE','BENCH_RELEASE','GERBER_RELEASE','CAD_ALLOWED_THIS_PACKAGE'])
assert all(v==0 for v in b['forbiddenActual'].values()) and b['actual']['officialNewSources']==1
b['actual']['existingFrozenEvidencePass']=1;b['actual']['manufacturingContractBatch']=1;b['status']='DOCUMENTS_COMPLETE_FINAL_READONLY_REVIEW_PENDING'
b['crosscheckUTC']=now.isoformat()
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),'utf8')
result={'UTC':now.isoformat(),'PASS':True,'frozenOldFiles':len(before),'allFrozenOldSHAUnchanged':True,'BOMrows':176,'groups':len(grp),'groupQty':176,'missingManufacturerMPN':['J1','J3','J4'],'mandatoryCompanions':comp,'defaultParameters':20,'noNewCADorPhysicalExecution':True,'engineeringAcceptedNotManufactureReleased':True,'actualSourceCount':1,'terminalCandidates':0,'scope':'One document crosscheck and frozen SHA pass; no scientific or CAD rerun'}
(P/'DOCUMENT_CROSSCHECK.json').write_text(json.dumps(result,indent=2),'utf8')
print(json.dumps(result))
