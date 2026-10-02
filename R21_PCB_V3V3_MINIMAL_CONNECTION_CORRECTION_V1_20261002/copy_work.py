from pathlib import Path
import json,shutil,hashlib
P=Path(__file__).parent;old=P.parent/'R21_PCB_ROUTING_CLOSURE_V1'/'SCIENCE_ADK5556_4X4_R21_ROUTING_CLOSURE_WORK.eprj2';new=P/'SCIENCE_ADK5556_4X4_R21_V3V3_MINIMAL_WORK.eprj2'
b=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'));assert b['status']=='ACTIVE'and b['actual']['copy']==1 and not new.exists()
data=old.read_bytes();shutil.copyfile(old,new);assert new.read_bytes()==data
(P/'INPUT_COPY_HASH.json').write_text(json.dumps({'source':str(old),'copy':str(new),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest().upper(),'byteIdentical':True},indent=2),'utf8');print('One byte-identical work copy created')
