from placement_geometry import *
import csv
Q=json.loads((P/'PLACEMENT_B21.json').read_text())['positions']
for r in ['U1','U2','U3','U5','RF0','CF0','C_TIA_HF0','C_AVDD9A','U9','U10','U13','U14','U15']:
 print(r,'pos',Q[r],'bodybounds',body(r,Q[r]).bounds,'pads',[(p['number'],tuple(round(v,3)for v in newpad(r,p,Q[r])),p.get('net'))for p in G[r]['pads']])

