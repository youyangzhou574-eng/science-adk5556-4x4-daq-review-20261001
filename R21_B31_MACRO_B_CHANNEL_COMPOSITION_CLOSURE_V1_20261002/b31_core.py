from pathlib import Path
import json,csv,math,itertools,datetime
import numpy as np
from shapely.geometry import box
from shapely.ops import unary_union
from placement_geometry import G,C,body,physical,newpad
from pin_cost import matching_cost
P=Path(__file__).parent
def save(n,d):(P/n).write_text(json.dumps(d,indent=2),encoding='utf8')
def reserve(kind,why):
 f=P/'EXECUTION_BUDGET.json';b=json.loads(f.read_text());now=datetime.datetime.now(datetime.timezone.utc)
 assert b['status']=='ACTIVE' and now<datetime.datetime.fromisoformat(b['deadlineUTC'])
 assert b['actual'][kind]<b['limits'][kind]
 b['actual'][kind]+=1;b['reservations'].append({'UTC':now.isoformat(),'kind':kind,'reason':why});save(f.name,b);return b['actual'][kind]
def pd(r,n):return next(p for p in G[r]['pads'] if p['number']==str(n))
def pt(pos,r,n):return np.array(newpad(r,pd(r,n),pos[r]))
keys=[]
for q in csv.DictReader((P/'KEY_PIN_DISTANCE_B21.csv').open(encoding='utf-8-sig')):keys.append({'ic':q['icRef'],'icPad':q['icPad'],'passive':q['passiveRef'],'passivePad':q['passivePad'],'limit':float(q['B21Mm']),'association':q['association']})
for q in csv.DictReader((P/'EXTRA_LOCAL_PIN_DISTANCES.csv').open(encoding='utf-8-sig')):keys.append({'ic':q['ic'],'icPad':q['icPad'],'passive':q['passive'],'passivePad':q['passivePad'],'limit':float(q['beforeMm']),'association':'EXTRA_LOCAL_PIN_SAME_NET'})
def krows(r):return [q for q in keys if q['passive']==r]
def keyok(r,cand,pos):return all(math.dist(newpad(r,pd(r,q['passivePad']),cand),pt(pos,q['ic'],q['icPad']))<=q['limit']+1e-6 for q in krows(r))
def family(r):
 m=C['membership'][r]
 if m in ['TIA','ROW','ADC']:return m
 if m in ['REFERENCE','MUX'] or r.startswith('R_SEL'):return 'BIAS_MUX'
 if r.startswith(('U8','U9','U10','U11','U12','C_LDO')) or r in ['J1','C_PWR']:return 'POWER'
 return 'INTERFACE_J2' if r=='J2' else 'DIGITAL'
def association(r):
 if krows(r):return krows(r)[0]['ic']
 for starts,ic in [(('D_TIA','RF','CF','R_TIA','R_COL'),'U2'),(('D_ROW','R_ROW','R_ISO'),'U1'),(('RD_','D_V','R_V','C_DIV'),'U3'),(('D_J3','R_J3'),'J3'),(('D_J4','R_J4'),'J4'),(('U9_',),'U9'),(('U10_',),'U10'),(('U11_',),'U11'),(('U12_',),'U12'),(('R_SEL_PD',),'U4')]:
  if r.startswith(starts):return ic
 d={'C_PWR':'U9','C_MCU_BULK':'U7','C_RST':'U15','R_RST':'U15','R_ENABLE_PD':'U13','R_HW_PD':'U14','R_ADC_RESET_PD':'U13','R_CS_PU':'U5','C_MUX':'U4'}
 if r in d:return d[r]
 if r.startswith('C_U'):return r[2:]
 raise ValueError('NO_ASSOC '+r)
def anchor(r,ic,pos):
 q=krows(r)
 if q:return np.mean([pt(pos,ic,v['icPad']) for v in q],axis=0)
 nets={p['net'] for p in G[r]['pads']}-{'','GND','V5','V3V3'}
 a=[newpad(ic,p,pos[ic]) for p in G[ic]['pads'] if p['net'] in nets]
 return np.mean(a,axis=0) if a else np.array(pos[ic][:2])
def pincost(r,ic,cand,pos):
 targets={}
 for p in G[ic]['pads']:targets.setdefault(p['net'],[]).append(newpad(ic,p,pos[ic]))
 return matching_cost([(p['net'],newpad(r,p,cand)) for p in G[r]['pads']],targets)
def empty_rectangle(shapes,step=1):
 # Largest full empty rectangle on a 1mm lattice; sampled/quantized, not continuous exact.
 b=unary_union(list(shapes)).bounds;x0,y0=math.floor(b[0]),math.floor(b[1]);nx,ny=math.ceil(b[2])-x0,math.ceil(b[3])-y0
 union=unary_union(list(shapes));heights=[0]*nx;best=(0,None)
 for j in range(ny):
  for i in range(nx):heights[i]=heights[i]+1 if i not in (0,nx-1) and j not in (0,ny-1) and union.intersection(box(x0+i,y0+j,x0+i+1,y0+j+1)).area<1e-9 else 0
  stack=[]
  for i,h in enumerate(heights+[0]):
   left=i
   while stack and stack[-1][1]>h:
    start,hh=stack.pop();area=(i-start)*hh
    if area>best[0]:best=(area,[x0+start,y0+j+1-hh,x0+i,y0+j+1])
    left=start
   stack.append((left,h))
 return {'areaMm2':best[0],'boundsMm':best[1],'gridMm':1,'domain':'floor/ceil physical bbox, full-cell intersection occupancy; not exact continuous void'}
def bbox(pos):
 b=unary_union([physical(r,v) for r,v in pos.items()]).bounds;w,h=b[2]-b[0],b[3]-b[1]
 return {'bounds':list(b),'widthMm':w,'heightMm':h,'aspectRatio':max(w,h)/min(w,h),'longShortDifferenceMm':abs(w-h)}
def chain_edges():
 e=[]
 for i,op in enumerate([1,7,8,14]):
  e += [('COL'+str(i),'J2',str(i+5),'U2',str([2,6,9,13][i]),'FUNCTIONAL_VIA_SENSE'),('TIA'+str(i),'U2',str(op),'U5',str([16,18,21,23][i]),'FUNCTIONAL_VIA_ISO_ADC_RC'),('ROW'+str(i),'U1',str(op),'J2',str(i+1),'FUNCTIONAL_VIA_R_ISO')]
 e += [('VCM','U3','1','U4','4','FUNCTIONAL_VIA_ISO'),('VEXC','U3','7','U4','2','FUNCTIONAL_VIA_ISO')]
 for i,n in enumerate([3,8,13,18]):e.append(('CMD'+str(i),'U4',str(n),'U1',str([3,5,10,12][i]),'SAME_NET'))
 for a,b in [(1,14),(36,13),(37,12),(38,11)]:e.append(('SPI','U5',str(a),'U7',str(b),'SAME_NET'))
 # Actual shared non-rail pin connections, controls/interface lanes. All retained, no guessed direction.
 for ar,br in [('U7','J3'),('U7','J4'),('U7','U13'),('U7','U14'),('U7','U15'),('U13','U14'),('U13','U15')]:
  for ap in G[ar]['pads']:
   for bp in G[br]['pads']:
    if ap['net'] and ap['net']==bp['net'] and ap['net'] not in ['GND','V5','V3V3']:e.append(('DIGITAL',ar,ap['number'],br,bp['number'],'SAME_NET'))
 e += [('V5_IN','J1','1','U9','5','SAME_NET'),('V5','U9','6','U8','1','SAME_NET'),('V3_LDO','U8','5','U10','5','SAME_NET'),('MON5','U11','1','U9','6','FUNCTIONAL_VIA_DIVIDER'),('MON3','U12','4','U10','6','SAME_NET')]
 return e
def macro_audit(pos):
 assert all(pd(a,ap)['net']==pd(b,bp)['net'] and pd(a,ap)['net'] for lane,a,ap,b,bp,assoc in chain_edges() if assoc=='SAME_NET')
 collisions=[(a,b) for a,b in itertools.combinations(pos,2) if physical(a,pos[a]).intersection(physical(b,pos[b])).area>1e-8]
 es=[{'lane':lane,'from':a+'.'+ap,'to':b+'.'+bp,'association':assoc,'lengthMm':math.dist(pt(pos,a,ap),pt(pos,b,bp))} for lane,a,ap,b,bp,assoc in chain_edges()]
 bb=bbox(pos);emp=empty_rectangle([physical(r,v) for r,v in pos.items()]);total=sum(x['lengthMm'] for x in es)
 return {'positions':pos,'physicalCollisions':collisions,'edges':es,'bbox':bb,'largestSampledEmptyRectangle':emp,'signalLengthSumMm':total,'score':total+bb['longShortDifferenceMm']*2+emp['areaMm2']*.025,'scoreMeaning':'sum explicit actual inter-pad functional/same-net macro edges + 2*long-short mm + .025*1mm empty rectangle area; proxy, no routing/physical claim'}
