from pathlib import Path
import json,hashlib,shutil,re,zipfile,datetime
source=Path(__file__).parent;root=source.parent/'GITHUB_PCB_ROUTING_DELIVERY_20261002';root.mkdir(exist_ok=True)
previous=source.parent/'GITHUB_PCB_IMPORT_DIFF_DELIVERY_20261002'
folder='R21_PCB_ROUTING_CLOSURE_V1_20261002'
for name in('github_delivery.py','run_network.py','public_batch.py'):
 s=(previous/name).read_text('utf8').replace('R21_PCB_IMPORT_DIFF_RESOLUTION_V1_20261002',folder)
 s=s.replace('Deliver actual PCB import diff classification and cold verified synchronization','Deliver saved native PCB routing with final verification HOLD and complete evidence')
 if name=='public_batch.py':
  a=s.index('names=');b=s.index('\n\ndef fetch',a)
  s=s[:a]+"names=['COMPLETE_ROUTING_RECEIPT.md','README.md','SHA256_MANIFEST.json','ALL_550_PAD_NET_IDENTITY.csv','FINAL_LAYER_15.png','SCIENCE_ADK5556_4X4_R21_PCB_ROUTED_REVIEW.epro2','SCIENCE_ADK5556_4X4_R21_ROUTING_CLOSURE_WORK.eprj2','COMPLETE_SOURCE_AND_EVIDENCE.zip']"+s[b:]
 (root/name).write_text(s,'utf8')
print(str(root))
