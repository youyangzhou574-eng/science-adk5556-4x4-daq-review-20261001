from pathlib import Path
import json
P=Path(__file__).parent
v=json.loads((P/'BASELINE_J2_BATCH.json').read_text('utf8'))['parsed']['value']
(P/'BASELINE_SCHEMATIC.json').write_text(json.dumps(v['schematic'],ensure_ascii=False,indent=2),'utf8')
(P/'BASELINE_PCB.json').write_text(json.dumps(v['pcb'],ensure_ascii=False,indent=2),'utf8')
for p in v['schematic']['pages']:
 for x in p['parts']:
  if x['ref']=='J2': print(json.dumps({'page':p['page'],'J2sch':x},ensure_ascii=False))
for x in v['pcb']['parts']:
 if x['ref']=='J2':print(json.dumps({'J2pcb':x},ensure_ascii=False))
print('Baseline counts',len(v['pcb']['parts']),sum(len(x['pads']) for x in v['pcb']['parts']))
