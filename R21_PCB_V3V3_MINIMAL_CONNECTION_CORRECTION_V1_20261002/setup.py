from pathlib import Path
import json,datetime,shutil,hashlib
P=Path(__file__).parent;old=P.parent/'R21_PCB_ROUTING_CLOSURE_V1';prev=P.parent/'R21_PCB_FINAL_READONLY_VERIFICATION_V1'
for n in('cli_call.py','capture_routing.js','drc_routing.js','summarize_drc.py'):shutil.copyfile(prev/n,P/n)
budget={'package':'SCIENCE_ADK5556_4X4_R21_PCB_V3V3_MINIMAL_CONNECTION_CORRECTION_V1','ruling':'f80cab79-8653-407b-9416-a808f358290c','parentUser':'504704c5-3b28-483b-a977-6d9a0a433581','startUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'approvedMinutes':180,'limits':{'copy':1,'session':2,'save':2,'captureaudit':4,'DRC':4,'reviewExport':1,'localBridge':2,'newVia':1,'sameAreaSecondPass':1},'actual':{'copy':0,'session':0,'save':0,'captureaudit':0,'DRC':0,'reviewExport':0,'localBridge':0,'newVia':0,'sameAreaSecondPass':0},'status':'ACTIVE','componentMove':0,'deviceValueFootprintEdit':0,'schematic':0,'ImportChanges':0,'autorouter':0,'largeReroute':0,'simulation':0,'Gerber':0,'procurement':0,'manufacture':0,'actualBench':0,'localGit':0,'reservations':[]}
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(budget,indent=2),'utf8')
print('Budget initialized only; copy not yet executed')
