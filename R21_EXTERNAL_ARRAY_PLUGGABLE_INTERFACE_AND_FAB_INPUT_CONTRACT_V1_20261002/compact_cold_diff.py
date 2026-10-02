from pathlib import Path
import json,collections
P=Path(__file__).parent;r=json.loads((P/'WARM_COLD_SOURCE_DIFF_RAW.json').read_text('utf8'));print('PCB',[(x['key'],list(x.get('diff',{})))for x in r['pcb']]);print('SCH',json.dumps(r['sch'],ensure_ascii=False)[:9000])
a=json.loads((P/'WARM_PCB.json').read_text('utf8'));b=json.loads((P/'COLD_PCB.json').read_text('utf8'));x,y=json.loads(a['netlist']),json.loads(b['netlist']);print('NET JSON EQ',x==y)
for k in x['components']:
 if x['components'][k]!=y['components'][k]:print('NET component diff',k,x['components'][k]['props'],y['components'][k]['props'])
for k in x:
 if k!='components'and x[k]!=y[k]:print('NET otherdiff',k)
