from pathlib import Path
import json
P=Path("E:/open/SCIENCE_ADK5556_4X4_DAQ_REPLICA/R21_B22_STRUCTURED_CHANNEL_ARRAY_PLACEMENT_V1");n=json.loads((P/'PLACEMENT_B22.json').read_text())
for t in n['templates']:
 if len(t['refs'])>1:print(json.dumps(t))
print('EXCEPTIONS',json.dumps(n['exceptions']))

