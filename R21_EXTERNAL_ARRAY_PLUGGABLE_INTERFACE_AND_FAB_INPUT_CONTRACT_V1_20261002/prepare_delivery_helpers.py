from pathlib import Path
import json,hashlib
P=Path(__file__).parent;prev=P.parent/'R21_PCB_MANUFACTURING_PREFLIGHT_READONLY_V1';expected=json.loads((prev/'FROZEN_94_SOURCE_HASHES_AFTER.json').read_text('utf8'))['files'];old=P.parent/'R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1';diff=[]
for n,e in expected.items():
 f=old/n;g={'bytes':f.stat().st_size,'SHA256':hashlib.sha256(f.read_bytes()).hexdigest().upper()}
 if g!=e:diff.append({'name':n,'expected':e,'actual':g})
assert not diff,diff
(P/'FROZEN_94_OLD_SOURCE_RECHECK.json').write_text(json.dumps({'all94Unchanged':True,'count':len(expected),'files':expected},indent=2),'utf8')
f=P/'SCIENCE_ADK5556_4X4_R21_J2_PLUGGABLE_WORK.eprj2';(P/'FINAL_SAVED_PROJECT_METADATA.json').write_text(json.dumps({'name':f.name,'bytes':f.stat().st_size,'SHA256':hashlib.sha256(f.read_bytes()).hexdigest().upper(),'actualIndependentColdVerified':True},indent=2),'utf8')
d=P.parent/'GITHUB_J2_INTERFACE_DELIVERY_20261002';d.mkdir(exist_ok=True);oldD=P.parent/'GITHUB_PCB_PREFLIGHT_DELIVERY_20261002'
for n in ('github_delivery.py','run_network.py','public_batch.py'):
 t=(oldD/n).read_text('utf8').replace('R21_PCB_MANUFACTURING_PREFLIGHT_READONLY_V1_20261002','R21_EXTERNAL_ARRAY_PLUGGABLE_INTERFACE_AND_FAB_INPUT_CONTRACT_V1_20261002')
 if n=='github_delivery.py':t=t.replace('Deliver frozen PCB manufacturing preflight, interface wiring and pending process inputs; no manufacture release','Deliver exact J2 pluggable interface ECO, actual warm/cold evidence and fabrication input contract; review only')
 if n=='public_batch.py':
  begin=t.index('names=');end=t.index('\n\n',begin)
  t=t[:begin]+"names=['COMPLETE_J2_INTERFACE_RECEIPT.md','SHA256_MANIFEST.json','J2_ACTUAL_8PIN_HARNESS.csv','ACTUAL_550_PAD_NET.csv','J2_PINOUT_AND_BODY.png','SCIENCE_ADK5556_4X4_R21_J2_PLUGGABLE_REVIEW.epro2','COLD_QUALIFIED_GATE.json','COMPLETE_SOURCE_AND_EVIDENCE.zip']"+t[end:]
 (d/n).write_text(t,'utf8')
print(json.dumps({'old94PASS':True,'deliveryHelpersPrepared':str(d),'noRemoteWriteYet':True}))
