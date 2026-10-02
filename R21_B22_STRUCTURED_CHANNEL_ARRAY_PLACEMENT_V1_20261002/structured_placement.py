from placement_geometry import *
import csv,itertools,time,sys
from shapely.prepared import prep
old=json.loads((P/'PLACEMENT_B21.json').read_text())['positions']
checks=list(csv.DictReader((P/'KEY_PIN_DISTANCE_B21.csv').open(encoding='utf-8-sig')))
byref={}
for row in checks:byref.setdefault(row['passiveRef'],[]).append(row)
fixed={r for r in G if (r.startswith('J') and '_'not in r)or(r.startswith('U')and'_'not in r)}|{'C_ROW_OP','C_TIA_OP','C_BUF','C_REF','C_MCU1','C_MUX'}
positions={r:tuple(old[r])for r in fixed}
occupied={r:physical(r,positions[r])for r in fixed}
pending={r:physical(r,old[r])for r in byref if r not in fixed}
j=old['J2'];keepout=unary_union([box(j[0]-15.5,j[1]-8.7,j[0]-5.5,j[1]+8.7),box(j[0]-7.5,j[1]-8.7,j[0]+.3,j[1]+8.7)])
bb=json.loads((P/'PLACEMENT_B21.json').read_text())['metrics']['naturalBBoxMm']
templates=[];exceptions=[];trials={}
def keypass(ref,pos):
 for row in byref.get(ref,[]):
  ic=row['icRef'];rp=next(v for v in G[ic]['pads']if str(v['number'])==row['icPad']);sp=next(v for v in G[ref]['pads']if str(v['number'])==row['passivePad'])
  if math.dist(newpad(ic,rp,old[ic]),newpad(ref,sp,pos))>float(row['B21Mm'])+1e-6:return False
 return True
def valid(ps):
 shapes={}
 for r,pos in ps.items():
  if not keypass(r,pos):return None
  b=body(r,pos).bounds
  if b[0]<bb[0]-1e-6 or b[1]<bb[1]-1e-6 or b[2]>bb[2]+1e-6 or b[3]>bb[3]+1e-6:return None
  q=physical(r,pos)
  if q.intersection(keepout).area>1e-8:return None
  if any(q.intersection(s).area>1e-8 for s in occupied.values()):return None
  if any(q.intersection(s).area>1e-8 for rr,s in pending.items()if rr not in ps):return None
  if any(q.intersection(s).area>1e-8 for s in shapes.values()):return None
  shapes[r]=q
 return shapes
def adopt(name,ps,info):
 sh=valid(ps)
 if sh is None:return False
 positions.update(ps);occupied.update(sh)
 for r in ps:pending.pop(r,None)
 templates.append(dict(name=name,refs=list(ps),**info));return True
def rowfit(name,refs,axis=None,span=6,spacing=None,center=None,angles=None,mirror=False):
 # Finite local template, no optimizer, no new placement family.
 origin=center or (sum(old[r][0]for r in refs)/len(refs),sum(old[r][1]for r in refs)/len(refs))
 best=None;count=0
 for angle in angles or (0,90,180,270):
  w=max(body(r,(0,0,angle)).bounds[2]-body(r,(0,0,angle)).bounds[0]for r in refs)
  h=max(body(r,(0,0,angle)).bounds[3]-body(r,(0,0,angle)).bounds[1]for r in refs)
  for ax in ([axis]if axis else ['x','y']):
   pitch=spacing or((w if ax=='x'else h)+.8)
   if len(refs)==1:pitch=0
   for dx in range(-span,span+1):
    for dy in range(-span,span+1):
     ox,oy=origin[0]+dx*.5,origin[1]+dy*.5
     ps={r:(ox+(i-(len(refs)-1)/2)*pitch*(ax=='x'),oy+(i-(len(refs)-1)/2)*pitch*(ax=='y'),angle)for i,r in enumerate(refs)}
     count+=1
     sh=valid(ps)
     if sh is None:continue
     score=sum(math.dist(ps[r][:2],old[r][:2])**2 for r in refs)
     if best is None or score<best[0]:best=(score,ps,sh,pitch,ax,angle)
 trials[name]=count
 if best:
  _,ps,sh,pitch,ax,angle=best;positions.update(ps);occupied.update(sh)
  for r in ps:pending.pop(r,None)
  templates.append({'name':name,'refs':refs,'kind':'EQUAL_PITCH_ROW','axis':ax,'pitchMm':pitch,'rotation':angle,'candidateCount':count});return True
 return False
def mirrored4(name,refs,center,pRange,qRange,angleRange=(0,180,90,270)):
 # Two IC pin-facing pairs; channel sequence around IC is 0,1,2,3.
 best=None;count=0
 for px in pRange:
  for py in qRange:
   for angle in angleRange:
    for dx in (-.5,0,.5):
     for dy in (-.5,0,.5):
      ox,oy=center[0]+dx,center[1]+dy
      ps={r:(ox+sx*px/2,oy+sy*py/2,angle)for r,(sx,sy)in zip(refs,[(-1,-1),(1,-1),(1,1),(-1,1)])}
      count+=1;sh=valid(ps)
      if sh is None:continue
      score=sum(math.dist(ps[r][:2],old[r][:2])**2 for r in refs)
      if best is None or score<best[0]:best=(score,ps,sh,px,py,angle)
 trials[name]=count
 if best:
  _,ps,sh,px,py,angle=best;positions.update(ps);occupied.update(sh)
  for r in ps:pending.pop(r,None)
  templates.append({'name':name,'refs':refs,'kind':'PIN_FACING_MIRROR_2_PLUS_2','pitchXmm':px,'pitchYmm':py,'rotation':angle,'candidateCount':count});return True
 return False
def retain(name,refs,reason):
 ps={r:tuple(old[r])for r in refs}
 if not adopt(name,ps,{'kind':'PIN_FORCED_BASELINE','reason':reason}):raise RuntimeError('Cannot retain '+name+' without collision')
 exceptions.append({'name':name,'refs':refs,'reason':reason})
def group4(name,prefix,ic,pRange,qRange):
 refs=[prefix+str(i)for i in range(4)]
 # four-in-line only if actual critical pads and IC collision allow it
 if rowfit(name,refs,span=4):return
 if mirrored4(name,refs,old[ic][:2],pRange,qRange):return
 retain(name,refs,'No bounded equal-pitch row or common-rotation mirrored2+2 passed original critical-distance and physical-proxy gates')
def stage():
 reserve('placementAdjustment','B2.2 one complete finite structured-channel adjustment; IC/interface macro anchors fixed')
 for name,prefix,ic in [('TIA_HF','C_TIA_HF','U2'),('ROW_HF','C_ROW_HF','U1')]:
  group4(name,prefix,ic,[5.4,5.8,6.2,6.4,6.6],[7,7.5,8,8.5,9,9.5,10])
 for name,prefix,ic in [('TIA_ISO','R_TIA_ISO','U2'),('TIA_SENSE','R_COL_SENSE','U2'),('ROW_ISO','R_ISO','U1'),('ROW_FB','R_ROW_FB','U1'),('TIA_RF','RF','U2'),('TIA_CF','CF','U2')]:
  group4(name,prefix,ic,[2.4,3.4,4.4,5.4,6.4,7.4,8.4,9.4],[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21])
 # ADC four input channels: explicit common4-column/two-row matrix under input pads.
 refsR=['R_ADC'+str(i)for i in range(4)];refsC=['C_ADC'+str(i)for i in range(4)]
 adc=False
 for pitch in (2.4,2.6,2.8,3.0):
  if adc:break
  for x in (44,44.5,45):
   if adc:break
   for cy in (14.2,14.7,15.2,15.7,16.2):
    if adc:break
    for angle in (0,180,90,270):
     ps={r:(x+(i-1.5)*pitch,cy,angle)for i,r in enumerate(refsC)}
     ps.update({r:(x+(i-1.5)*pitch,cy-2.4,angle)for i,r in enumerate(refsR)})
     if adopt('ADC_INPUT_4X2',ps,{'kind':'FOUR_CHANNEL_TWO_ROW','pitchXmm':pitch,'pitchYmm':2.4,'rotation':angle}):adc=True;break
 if not adc:
  for pref in('C_ADC','R_ADC'):group4('ADC_'+pref,pref,'U5',[8,10,12,14,16],[2.4,3,3.5,4])
  exceptions.append({'name':'ADC_INPUT_4X2','reason':'Single 4x2 layout rejected by real pads/physical bounds; pin-facing rows retained','refs':refsR+refsC})
 # VCM/VEX HF re-seat into 180-degree positional pairing about actualU3.
 refs=['C_VCM_HF','C_VEX_HF'];center=old['U3']
 done=False
 for dx in(-1.9,-1.4,-.9,-.5,0,.5,.9):
  if done:break
  for dy in(4.0,4.5,5):
   if done:break
   for angle in(0,180,90,270):
    ps={refs[0]:(center[0]+dx,center[1]-dy,angle),refs[1]:(center[0]-dx,center[1]+dy,angle)}
    if adopt('BIAS_HF_MIRROR',ps,{'kind':'CENTRAL_POSITIONAL_MIRROR','axisCenter':center[:2],'rotation':angle}):done=True;break
 if not done:retain('BIAS_HF',refs,'Exact U3 pin-local critical caps retained')
 # paired VCM/VEX feedback/isolators: finite mirror rows, otherwise critical local bank
 for suff in('FB','ISO'):
  refs=['R_VCM_'+suff,'R_VEX_'+suff];done=False
  for dx in(-3,-2,-1,0,1,2,3):
   if done:break
   for dy in(4,5,6,7,8):
    if done:break
    for a in(0,180,90,270):
     ps={refs[0]:(center[0]+dx,center[1]-dy,a),refs[1]:(center[0]-dx,center[1]+dy,a)}
     if adopt('BIAS_'+suff+'_MIRROR',ps,{'kind':'CENTRAL_POSITIONAL_MIRROR','axisCenter':center[:2],'rotation':a}):done=True;break
  if not done:retain('BIAS_'+suff,refs,'Pin-locality prevents bounded mirror')
 for name,refs in [
 ('ADC_AVDD9',['C_AVDD9_HF','C_AVDD9A','C_AVDD9B','C_ADCA2']),
 ('ADC_AVDD30',['C_AVDD30_HF','C_AVDD30A','C_AVDD30B','C_ADCA1']),
 ('ADC_REFCAP',['C_ADC_REFCAP','C_REFCAP_BULKA','C_REFCAP_BULKB']),
 ('ADC_REFIO',['C_ADC_REFIO','C_REFIO_B']),
 ('ADC_DVDD',['C_ADCD','C_DVDD34A','C_DVDD34B']),
 ('LDO_CAPS',['C_LDO_IN','C_LDO_OUT'])]:
  if not rowfit(name,refs,span=10):retain(name,refs,'Exact closest cap pin limits prevent full bank at finite templates')
 # Power caps use common role template, preserving actual input/output pad distances.
 for prefix in('U9','U10'):
  refs=[prefix+'_IN_CAP',prefix+'_OUT_CAP']
  if not rowfit(prefix+'_CAPS',refs,axis='x',spacing=8,span=4,angles=[0]):retain(prefix+'_CAPS',refs,'Critical power cap distance retained')
 # Digital ICs are frozen macro anchors. Rule only localcaps and resistor rows; no global migration.
 for refs,name in [(['RD_B'+str(i)for i in range(1,10)]+['RD_TOP'],'DIVIDER_BANK'),
 (['R_SEL_PD'+str(i)for i in range(4)],'MUX_PULLS'),
 (['U9_'+s for s in ('OV_T','OV_B1','OV_B2','PG_T','PG_B','EN_R','EN_G','BLEED')],'POWER5_CONTROL'),
 (['U10_'+s for s in ('OV_T','OV_B1','OV_B2','PG_T','PG_B','EN_R','EN_G','BLEED')],'POWER3_CONTROL'),
 (['U11_TOP'+str(i)for i in range(5)]+['U11_BOT'],'SUPERVISOR5_DIVIDER'),
 (['U12_TOP'+str(i)for i in range(4)]+['U12_BOT'],'SUPERVISOR3_DIVIDER'),
 (['R_J3_'+s for s in('1','3','4','5')],'J3_RESISTORS'),(['D_J3_'+s for s in('1','3','4','5')],'J3_DIODES'),
 (['R_J4_'+s for s in('1','3','4')],'J4_RESISTORS'),(['D_J4_'+s for s in('1','3','4')],'J4_DIODES'),
 (['R_CS_PU','R_ENABLE_PD','R_HW_PD','R_RST'],'DIGITAL_PULLS')]:
  if rowfit(name,refs,span=10):continue
  # Longrolebanks may need2 columns to stay local; split into adjacent equal rows.
  half=(len(refs)+1)//2
  for i,rs in enumerate([refs[:half],refs[half:]]):
   if not rs:continue
   if not rowfit(name+'_'+str(i),rs,span=12):retain(name+'_'+str(i),rs,'No finite collision-free bank inside original bbox')
 for r in sorted(set(G)-set(positions)):
  if not rowfit('LOCAL_'+r,[r],span=12):retain('LOCAL_'+r,[r],'Original local placement retained')
 bodies={r:body(r,positions[r])for r in G};shapes={r:physical(r,positions[r])for r in G}
 collisions={}
 for name,ss in [('body',bodies),('physicalProxy',shapes)]:
  collisions[name]=[{'a':r,'b':s,'areaMm2':ss[r].intersection(ss[s]).area}for r,s in itertools.combinations(sorted(G),2)if ss[r].intersection(ss[s]).area>1e-8]
 distances=[]
 for row in checks:
  r,s=row['icRef'],row['passiveRef'];rp=next(v for v in G[r]['pads']if str(v['number'])==row['icPad']);sp=next(v for v in G[s]['pads']if str(v['number'])==row['passivePad'])
  n=math.dist(newpad(r,rp,positions[r]),newpad(s,sp,positions[s]));distances.append(dict(row,B22Mm=n,B22MinusB21Mm=n-float(row['B21Mm'])))
 nat=unary_union(list(bodies.values()));bounds=nat.bounds
 metrics={'components':len(G),'pads':sum(len(g['pads'])for g in G.values()),'naturalBBoxMm':bounds,'naturalWidthMm':bounds[2]-bounds[0],'naturalHeightMm':bounds[3]-bounds[1],'macroAnchorsFixed':sorted(fixed),'movedCount':sum(tuple(old[r])!=tuple(positions[r])for r in G),'bodyOverlapPairs':collisions['body'],'physicalProxyOverlapPairs':collisions['physicalProxy'],'pairsExaminedEach':15400,'criticalPairs':len(distances),'maxCriticalIncreaseMm':max(r['B22MinusB21Mm']for r in distances),'minCriticalDeltaMm':min(r['B22MinusB21Mm']for r in distances),'FFCPlanningKeepoutCollisions':[r for r in G if r!='J2'and shapes[r].intersection(keepout).area>1e-8],'FFCExactSweepHOLD':True,'CAD':0}
 (P/'PLACEMENT_B22.json').write_text(json.dumps({'positions':positions,'metrics':metrics,'templates':templates,'exceptions':exceptions,'finiteCandidateCounts':trials},indent=2),encoding='utf8')
 with(P/'KEY_PIN_DISTANCE_B22.csv').open('w',newline='',encoding='utf-8-sig')as f:w=csv.DictWriter(f,fieldnames=list(distances[0]));w.writeheader();w.writerows(distances)
 with(P/'PLACEMENT_B22.csv').open('w',newline='',encoding='utf-8-sig')as f:
  w=csv.DictWriter(f,fieldnames=['Designator','X_mm','Y_mm','Rotation','Layer','Function','ChangedFromB21']);w.writeheader();w.writerows([dict(Designator=r,X_mm=positions[r][0],Y_mm=positions[r][1],Rotation=positions[r][2],Layer=G[r]['layer'],Function=regions[r],ChangedFromB21=tuple(old[r])!=tuple(positions[r]))for r in sorted(G)])
 assert not collisions['body']and not collisions['physicalProxy']and metrics['maxCriticalIncreaseMm']<=1e-6 and not metrics['FFCPlanningKeepoutCollisions']
 print(json.dumps({'metrics':metrics,'templateCount':len(templates),'exceptionCount':len(exceptions)},ensure_ascii=True))
if __name__=='__main__':
 try:stage()
 except Exception:
  (P/'LAST_FAILED_PARTIAL.json').write_text(json.dumps({'positions':positions,'templates':templates,'exceptions':exceptions,'pendingRefs':list(pending)},indent=2),encoding='utf8')
  raise
