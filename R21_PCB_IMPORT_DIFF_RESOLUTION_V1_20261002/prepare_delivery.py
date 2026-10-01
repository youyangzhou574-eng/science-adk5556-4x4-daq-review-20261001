from pathlib import Path
import json
p=Path(__file__).resolve().parent
d=p.parent/'GITHUB_PCB_IMPORT_DIFF_DELIVERY_20261002';d.mkdir(exist_ok=True)
prev=p.parent/'GITHUB_PCB_CLOSURE_DELIVERY_20261002'
oldfolder='R21_PCB_NETLIST_INTEGRATION_AND_ROUTING_CLOSURE_V1_20261002'
folder='R21_PCB_IMPORT_DIFF_RESOLUTION_V1_20261002'
for name in ['github_delivery.py','run_network.py','public_batch.py','prepare.py']:
 s=(prev/name).read_text('utf8').replace(oldfolder,folder)
 if name=='github_delivery.py':s=s.replace('Deliver PCB integration gate evidence and concrete editor sync handoff','Deliver actual PCB import diff classification and cold verified synchronization')
 if name=='public_batch.py':
  start=s.index('names=');end=s.index('\n',start)
  names=['COMPLETE_IMPORT_DIFF_RECEIPT.md','README.md','SHA256_MANIFEST.json','IMPORT_CHANGE_DIFF_WEB.csv','BEFORE_AFTER_NETLIST_COMPARE.csv','SCIENCE_ADK5556_4X4_R21_PCB_SYNC_REVIEW.epro2','SCIENCE_ADK5556_4X4_R21_IMPORT_DIFF_WORK.eprj2','COMPLETE_SOURCE_AND_EVIDENCE.zip']
  s=s[:start]+'names='+repr(names)+s[end:]
 if name=='prepare.py':
  s=s.replace("source=root.parent/'R21_PCB_NETLIST_INTEGRATION_AND_ROUTING_CLOSURE_V1'","source=root.parent/'R21_PCB_IMPORT_DIFF_RESOLUTION_V1'")
  s=s.replace("previous=root.parent/'GITHUB_PCB_FLOORPLAN_DELIVERY_20261002'","previous=root.parent/'GITHUB_PCB_CLOSURE_DELIVERY_20261002'")
  s=s.replace('SCIENCE_ADK5556_4X4_R21_PCB_NETLIST_INTEGRATION_AND_ROUTING_CLOSURE_V1','SCIENCE_ADK5556_4X4_R21_PCB_IMPORT_DIFF_RESOLUTION_V1')
  s=s.replace('COMPLETE_ROUTING_CLOSURE_RECEIPT.md','COMPLETE_IMPORT_DIFF_RECEIPT.md')
  s=s.replace('approved PCB integration attempt; unresolved native netlist error; no further routing; editor handoff; no procurement/manufacture/bench','actual GUI property diff classified; one sync; cold verified NetlistError0; no new routing/procurement/manufacture/bench')
  start=s.index("prefix=");end=s.index("\n(payload/'ROOT_README.md')",start)
  prefix='# Latest: actual GUI synchronization resolved; routing remains incomplete\n\n[Complete receipt]('+folder+'/COMPLETE_IMPORT_DIFF_RECEIPT.md) · [Actual697 diff]('+folder+'/IMPORT_CHANGE_DIFF_WEB.csv) · [All550 pin comparison]('+folder+'/BEFORE_AFTER_NETLIST_COMPARE.csv) · [Index]('+folder+'/README.md). One reviewed property sync, warm/cold NetlistError0;452 connection entries still need routing. Review only; no manufacture/powerup.\n\n---\n\n'
  s=s[:start]+'prefix='+repr(prefix)+s[end:]
 (d/name).write_text(s,'utf8')
print(json.dumps({'delivery':str(d),'preparedHelpers':4,'payloadNotFrozenYet':True}))

