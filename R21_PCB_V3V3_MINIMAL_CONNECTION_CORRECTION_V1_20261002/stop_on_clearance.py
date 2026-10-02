from pathlib import Path
import json,datetime
P=Path(__file__).parent;f=P/'EXECUTION_BUDGET.json';b=json.loads(f.read_text('utf8'));r=json.loads((P/'FIRST_POSTFIX_DRC.json').read_text('utf8'))['parsed'];assert r['ok']and r['value'][0]['name']=='Clearance Error'and r['value'][0]['count']==4
b['status']='STOP_NEW_V3V3_VIA_TO_GND_FILLED_CLEARANCE';b['stopUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();b['evidenceOnlyAfterStop']=True;b['stopEvidence']='FIRST_POSTFIX_DRC.json';f.write_text(json.dumps(b,indent=2),'utf8');print('Sticky STOP; only existing-state capture/review evidence and normal close remain')
