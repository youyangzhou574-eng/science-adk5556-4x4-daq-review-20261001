import json,csv,math
from pathlib import Path
from placement_geometry import G,physical,newpad
P=Path(__file__).parent
rows=list(csv.DictReader((P/'KEY_PIN_DISTANCE_B21.csv').open(encoding='utf-8-sig')))
print(json.dumps({r:{'keyLimits':[(q['icRef'],q['icPad'],q['passivePad'],round(float(q['B21Mm']),3)) for q in rows if q['passiveRef']==r],'physicalSize':[round(v,3) for v in (physical(r,(0,0,0)).bounds[2]-physical(r,(0,0,0)).bounds[0],physical(r,(0,0,0)).bounds[3]-physical(r,(0,0,0)).bounds[1])]} for r in G if not(r.startswith('U') and r[1:].isdigit())},ensure_ascii=True))
