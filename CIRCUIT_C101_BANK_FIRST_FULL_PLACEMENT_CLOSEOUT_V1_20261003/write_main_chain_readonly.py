from floorplan_core import *
import csv
ps=json.loads((P/'P1_FULL_PLACEMENT.json').read_text())['positions'];edges=[]
def edge(label,a,ap,b,bp):
 assert net(a,ap)is not None and net(a,ap)==net(b,bp)
 edges.append({'role':label,'fromRef':a,'fromPin':ap,'toRef':b,'toPin':bp,'actualSameNet':net(a,ap),'distanceMm':dist(pad(a,ap,ps[a]),pad(b,bp,ps[b])),'evidence':'EUCLIDEAN_ONLY_NOT_ROUTING'})
edge('ROW_DRIVER_TO_MUX','U1',1,'U4',8);edge('MUX_FEEDBACK_TO_ROW_AMP','U4',9,'U1',4)
for i in range(4):
 edge('FFC_ROW'+str(i),'J2',i+1,'U4',[4,5,6,7][i]);edge('FFC_COL'+str(i),'J2',i+5,'U2',[2,6,9,13][i])
for label,a,ap,b,bp in [('MOSI','U5',1,'U7',14),('MISO','U5',36,'U7',13),('SCLK','U5',37,'U7',12),('CS','U5',38,'U7',11),('POWERINPUT','J1',1,'U9',5),('POWERLDO','U9',6,'U8',6),('ENABLE','U11',6,'U8',4),('RESET','U12',6,'U7',6)]:edge(label,a,ap,b,bp)
for r,pin in [('R_J3_3',24),('R_J3_4',25),('R_J3_5',6),('R_J4_3',19),('R_J4_4',21)]:
 edge(r+'_MCU','U7',pin,r,2);edge(r+'_EXTERNAL',r,1,'J3'if r.startswith('R_J3')else'J4',int(r[-1]))
assert len(edges)==28
with(P/'FULL28_MAIN_CHAIN_ACTUAL_PIN_PROXY.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(edges[0]));w.writeheader();w.writerows(edges)
print(json.dumps({'readonlyMainChainEdges':len(edges),'ROWdriveSense':edges[:2],'newPlacementImages':0}))
