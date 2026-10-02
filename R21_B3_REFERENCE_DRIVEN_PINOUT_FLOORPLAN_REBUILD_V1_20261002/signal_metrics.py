from pathlib import Path
import csv,json,math
from placement_geometry import G,newpad
P=Path(__file__).parent
new=json.loads((P/'PLACEMENT_B3.json').read_text())['positions'];old=json.loads((P/'PLACEMENT_B22.json').read_text())['positions']
def pt(pos,r,p):return newpad(r,next(v for v in G[r]['pads'] if v['number']==str(p)),pos[r])
edges=[]
def add(label,a,ap,b,bp):
 na=next(v['net'] for v in G[a]['pads'] if v['number']==str(ap));nb=next(v['net'] for v in G[b]['pads'] if v['number']==str(bp));assert na==nb and na
 before=math.dist(pt(old,a,ap),pt(old,b,bp));after=math.dist(pt(new,a,ap),pt(new,b,bp));edges.append({'lane':label,'fromRef':a,'fromPad':ap,'toRef':b,'toPad':bp,'net':na,'beforeStraightMm':before,'afterStraightMm':after,'deltaMm':after-before})
for i,op in enumerate([1,7,8,14]):
 add('TIA_CH'+str(i),'U2',op,'R_TIA_ISO'+str(i),1);add('TIA_CH'+str(i),'R_TIA_ISO'+str(i),2,'R_ADC'+str(i),1);add('TIA_CH'+str(i),'R_ADC'+str(i),2,'C_ADC'+str(i),1);add('TIA_CH'+str(i),'C_ADC'+str(i),1,'U5',[16,18,21,23][i])
for up,mp in [(1,14),(36,13),(37,12),(38,11)]:add('SPI','U5',up,'U7',mp)
for i,op in enumerate([1,7,8,14]):add('ROW_CH'+str(i),'U1',op,'R_ISO'+str(i),1);add('ROW_CH'+str(i),'R_ISO'+str(i),2,'J2',i+1)
add('POWER','J1',1,'U9',5);add('POWER','U9',6,'U8',1);add('POWER','U8',5,'U10',5)
with (P/'REPRESENTATIVE_SIGNAL_EDGE_COMPARISON.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=list(edges[0]));w.writeheader();w.writerows(edges)
out={'edgeCount':len(edges),'sumBeforeStraightMm':sum(x['beforeStraightMm'] for x in edges),'sumAfterStraightMm':sum(x['afterStraightMm'] for x in edges),'increasedEdges':[x for x in edges if x['deltaMm']>1e-6],'note':'31 explicitly selected same-net inter-pad representative edges only; not full ratsnest, crossings, routing lengths or routability. Excludes GND/supply distribution and many Bias/control/debug edges.'}
(P/'REPRESENTATIVE_SIGNAL_METRICS.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out))
