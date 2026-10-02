from pathlib import Path
P=Path("E:/open/SCIENCE_ADK5556_4X4_DAQ_REPLICA/R21_B22_STRUCTURED_CHANNEL_ARRAY_PLACEMENT_V1");D=P.parent/'GITHUB_B22_STRUCTURED_DELIVERY_20261002';D.mkdir(exist_ok=True)
prev=P.parent/'GITHUB_B21_TOP_BAND_DELIVERY_20261002';folder=P.name+'_20261002'
for name in ['github_delivery.py','run_network.py','public_batch.py']:
 s=(prev/name).read_text(encoding='utf8').replace('R21_B21_TOP_BAND_FILL_REFINEMENT_V1_20261002',folder)
 s=s.replace('Deliver B2.1 top-band-only refinement: six moved, 170 frozen; CAD0','Deliver B2.2 structured-channel placement and actual-pin audit; CAD0')
 if name=='public_batch.py':
  i=s.index('names=');e=s.index('\n',i)
  s=s[:i]+'names='+repr(['COMPLETE_B22_RECEIPT.md','SHA256_MANIFEST.json','PLACEMENT_B22.csv','PLACEMENT_B21_VS_B22.png','INDEPENDENT_FINAL_AUDIT.json','KEY_PIN_DISTANCE_B22.csv','GATES.json','COMPLETE_SOURCE_AND_EVIDENCE.zip'])+s[e:]
 (D/name).write_text(s,encoding='utf8')
print('Existing authorized report publisher reused; no network writes yet')

