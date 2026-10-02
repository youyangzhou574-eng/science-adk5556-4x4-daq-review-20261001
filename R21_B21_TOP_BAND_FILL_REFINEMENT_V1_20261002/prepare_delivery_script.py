from pathlib import Path
P=Path(__file__).parent
s=(P.parent/'R21_PLACEMENT_B2_INTERLOCKING_V1'/'prepare_github_delivery.py').read_text(encoding='utf8')
s=s.replace("D=P.parent/'GITHUB_B2_INTERLOCKING_DELIVERY_20261002'","D=P.parent/'GITHUB_B21_TOP_BAND_DELIVERY_20261002'")
s=s.replace("PREV=P.parent/'GITHUB_PLACEMENT_ONLY_DELIVERY_20261002'","PREV=P.parent/'GITHUB_B2_INTERLOCKING_DELIVERY_20261002'")
s=s.replace("folder='R21_PLACEMENT_B2_INTERLOCKING_V1_20261002'","folder='R21_B21_TOP_BAND_FILL_REFINEMENT_V1_20261002'")
s=s.replace(".replace('R21_PLACEMENT_ONLY_TWO_RECTANGULAR_CANDIDATES_V1_20261002',folder)",".replace('R21_PLACEMENT_B2_INTERLOCKING_V1_20261002',folder)")
s=s.replace('SCIENCE_ADK5556_4X4_R21_PLACEMENT_B2_INTERLOCKING_V1','SCIENCE_ADK5556_4X4_R21_B21_TOP_BAND_FILL_REFINEMENT_V1')
s=s.replace('COMPLETE_B2_RECEIPT.md','COMPLETE_B21_RECEIPT.md').replace('PLACEMENT_B2.csv','PLACEMENT_B21.csv').replace('KEY_PIN_DISTANCE_B2.csv','KEY_PIN_DISTANCE_B21.csv')
s=s.replace('PLACEMENT_B2_NO_COPPER.png','PLACEMENT_B2_VS_B21.png').replace('PLACEMENT_OLD_B_VS_B2.png','FROZEN_AND_MOVED_REGISTER.json')
s=s.replace('# Latest: B2 interlocking placement; user selection before native CAD','# Latest: B2.1 final top-band refinement; user selection before native CAD').replace('[B2 no-copper + occupancy map]','[B2 / B2.1 comparison]').replace('[Old B / B2 comparison]','[6 moved / 170 frozen register]')
s=s.replace('176 parts / 552 pads; natural body envelope71.0x63.5mm.','Only6 components translated X-28mm, 170 positions exactly frozen; 176 parts / 552 pads; natural body envelope71.0x63.5mm.')
(P/'prepare_github_delivery.py').write_text(s,encoding='utf8')
