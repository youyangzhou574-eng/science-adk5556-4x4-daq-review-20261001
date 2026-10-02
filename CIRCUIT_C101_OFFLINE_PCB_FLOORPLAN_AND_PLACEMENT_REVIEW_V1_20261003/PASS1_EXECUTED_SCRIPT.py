from floorplan_core import *
import csv,traceback
reserve('candidate',2,'P1 horizontal / P2 L, sole two macro candidates, blank101 inputs')
reserve('placement',1,'First complete attempt to place all101 in both candidates; all failure counts retained')
config={
 'P1':{'outline':[50,50],'anchors':{'J1':[8,2.8,0],'J2':[3.5,29,0],'J3':[47.2,40.5,90],'J4':[47.2,20.5,90],'U9':[12,8,0],'U8':[28,8,180],'U11':[20,9,0],'U12':[36,9,0],'U1':[21.5,36,0],'U4':[14.5,37,0],'U2':[16,23,0],'U5':[30.5,24,180],'U6':[24,32.5,0],'U7':[37,39,270]}},
 'P2':{'outline':[50,50],'anchors':{'J1':[8,2.8,0],'J2':[3.5,38,0],'J3':[47.2,40.5,90],'J4':[47.2,20.5,90],'U9':[12,8,0],'U8':[33,8,180],'U11':[21,9,0],'U12':[41,9,0],'U1':[22,41.5,0],'U4':[14.5,40,0],'U2':[20,29.5,0],'U5':[21,17,270],'U6':[29,30.5,0],'U7':[38,35,270]}}
}
# Exact role→actual pin targets; connected ground picks nearest ground pin on SAME owner IC.
targets={}
def add(ref,ic,pin):
 n=net(ic,pin);pairs=[]
 assert n is not None,ref+' primarytargetNC'
 for q in G[ref]['pads']:
  if q['net']==n:pairs.append([q['number'],ic,str(pin),'primary'])
  elif q['net']=='GND':
   gg=[v for v in G[ic]['pads']if v['net']=='GND'];assert gg
   v=min(gg,key=lambda v:dist((v['x'],v['y']),(actualpin(ic,pin)['x'],actualpin(ic,pin)['y'])));pairs.append([q['number'],ic,v['number'],'ground_sameIC'])
 assert any(z[3]=='primary'for z in pairs),ref+' wrongICpinnet'
 targets.setdefault(ref,[]).extend(pairs)
for r,n in [('C_ROW_OP',5)]:add(r,'U1',n)
for r,n in [('C_MUX',14),('R_SEL_PD0',1),('R_SEL_PD1',16),('R_ENABLE_PD',2)]:add(r,'U4',n)
for r,n in [('C_REF',1),('C_VCM_OUT',2),('RD_TOP',2),('RD_B1',2),('C_DIV',2)]:
 if r in ['RD_B1','C_DIV']:
  # VEXC node has no REF3025 same-net endpoint; explicit series functional endpoint U1+IN.
  add(r,'U1',3)
 else:add(r,'U6',n)
add('C_TIA_OP','U2',4)
channels={0:[1,2],1:[7,6],2:[8,9],3:[14,13]}
for i,(out,minus)in channels.items():
 add('RF'+str(i),'U2',out);add('RF'+str(i),'U2',minus)
 add('CF'+str(i),'U2',out);add('CF'+str(i),'U2',minus)
 add('R_ADC'+str(i),'U2',out);add('R_ADC'+str(i),'U5',[16,18,21,23][i]);add('C_ADC'+str(i),'U5',[16,18,21,23][i])
for r in ['C_ADC_REFIO','C_REFIO_B']:add(r,'U5',5)
for r in ['C_REFCAP_BULKA','C_REFCAP_BULKB','C_ADC_REFCAP']:add(r,'U5',7)
for r in ['C_AVDD9A','C_AVDD9B','C_AVDD9_HF','C_ADCA1']:add(r,'U5',9)
for r in ['C_AVDD30A','C_AVDD30B','C_AVDD30_HF','C_ADCA2']:add(r,'U5',30)
for r in ['C_DVDD34A','C_DVDD34B','C_ADCD']:add(r,'U5',34)
for r,pin in [('R_CS_PU',38),('R_ADC_RESET_PD',2)]:add(r,'U5',pin)
for r,pin in [('C_MCU1',4),('C_MCU_BULK',4),('R_RST',6)]:add(r,'U7',pin)
for r,pin in [('C_LDO_IN',6),('C_LDO_OUT',1),('C_LDO_FF',2),('R_LDO_TOP',1),('R_LDO_TOP',2),('R_LDO_BOT',2),('R_LDO_EN_PU',4),('D_LDO_REV',1),('D_LDO_REV',6),('U10_BLEED',1)]:add(r,'U8',pin)
for r,pin in [('C_PWR',6),('U9_IN_CAP',5),('U9_OUT_CAP',6),('U9_EN_R',1),('U9_EN_G',1),('U9_OV_T',2),('U9_OV_B1',2),('U9_BLEED',6)]:add(r,'U9',pin)
for k in ['U11','U12']:
 for suffix,pin in [('CT_C',5),('VDD_C',4),('SENSE_C',1),('TOP0',1),('BOT',1)]:add(k+'_'+suffix,k,pin)
for r,pin in [('R_J3_1',1),('R_J3_3',3),('R_J3_4',4),('R_J3_5',5)]:add(r,'J3',pin)
for r,pin in [('R_J4_1',1),('R_J4_3',3),('R_J4_4',4)]:add(r,'J4',pin)
for r,ic,pin in [('R_J3_3','U7',24),('R_J3_4','U7',25),('R_J3_5','U7',6),('R_J4_3','U7',19),('R_J4_4','U7',21)]:add(r,ic,pin)
for r,ic,pin in [('D_DBG0','J3',3),('D_DBG1','J3',4),('D_DBG2','J4',3),('D_DBG3','J4',4)]:add(r,ic,pin)
# ESD devices lie between FFC and core; ROW/COL group targets not ground-driven.
for r,group in [('D_FFC_ROW','ROW'),('D_FFC_COL','COL')]:
 for pp in G[r]['pads']:
  if pp['net']and pp['net'].startswith(group):
   jp=next(j for j in G['J2']['pads']if j['net']==pp['net']);targets.setdefault(r,[]).append([pp['number'],'J2',jp['number'],'primary'])
for name,c in config.items():
 try:
  W,H=c['outline'];outline=box(0,0,W,H);placed={};j=c['anchors']['J2'][1]
  reserves={'J2':[-10,j-8,8,j+8],'J1':[3,-10,13,6],'J3':[44,32,60,49],'J4':[44,14,60,27]}
  exclusions=[(r,box(*b))for r,b in reserves.items()]
  for r,pos in c['anchors'].items():
   assert legal(r,pos,placed,outline,exclusions),('anchorcollision',name,r,allpairs({**placed,r:pos}));placed[r]=pos
  remaining=set(G)-set(placed);assert remaining==set(targets),(sorted(remaining-set(targets)),sorted(set(targets)-remaining))
  # Rigid symmetric2+2 feedback role template, derived from actual quad pin locations.
  for i,(out,minus)in channels.items():
   corner=pad('U2',out,placed['U2']);cx,cy=placed['U2'][:2];sign=1 if corner[1]>cy else -1;side=1 if corner[0]>cx else -1
   for typ,dx in [('RF',-0.9),('CF',0.9)]:
    r=typ+str(i);pos=[cx+side*3.3+dx,cy+sign*4.7,90]
    assert legal(r,pos,placed,outline,exclusions),(name,'feedbacktemplate',r);placed[r]=pos;remaining.remove(r)
  priority=sorted(remaining,key=lambda r:(0 if r in ['C_TIA_OP','C_MUX','C_ROW_OP','C_ADCA1','C_ADCA2','C_ADCD','C_REF','C_VCM_OUT','C_MCU1','U11_VDD_C','U12_VDD_C']else 1 if r.startswith('C_ADC') or r.startswith('R_ADC') else 2 if r.startswith('D_FFC') else 3 if not r.startswith('C_') else 4,r))
  for r in priority:
   edges=targets[r];primary=[e for e in edges if e[3]=='primary'];anchor=tuple(sum(pad(e[1],e[2],placed[e[1]])[k]for e in primary)/len(primary)for k in[0,1]);best=None;candidates=[]
   # Bounded local 0.5mm lattice. This is a finite artifact layout pass, not a new optimizer product.
   for ix in range(-16,17):
    for iy in range(-16,17):
     x=round(anchor[0]*2)/2+ix*.5;y=round(anchor[1]*2)/2+iy*.5
     if math.hypot(x-anchor[0],y-anchor[1])>8.2:continue
     for angle in [0,90,180,270]:
      pos=[x,y,angle]
      cost=sum((1 if e[3]=='primary'else.35)*dist(pad(r,e[0],pos),pad(e[1],e[2],placed[e[1]]))for e in edges)
      cost+=.04*dist((x,y),anchor)
      candidates.append((cost,pos))
   existing=[shape(q,v)for q,v in placed.items()];tree=STRtree(existing)
   for cost,pos in sorted(candidates,key=lambda z:z[0]):
    if legal(r,pos,placed,outline,exclusions,tree=tree,existing=existing):best=(cost,pos);break
   if best is None:raise ValueError('No bounded legal location '+r+' '+name)
   placed[r]=best[1]
  assert set(placed)==set(G);audit=allpairs(placed);assert not audit['physicalProxyCollisions']and not audit['bodyCollisions']
  result={'candidate':name,'boardPlanningMm':[W,H],'actualNativeOutlineChanged':False,'positions':placed,'edgeReserves':reserves,'geometryAudit':audit,'unplaced':[],'all101ActualIdentityFrozen':True,'feedbackTemplate':'four2+2corner role cells; actual pad names not exact manufacturable mirror proof','J2ExactMechanicalHOLD':True}
  (P/(name+'_PLACEMENT.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
  with(P/(name+'_PLACEMENT.csv')).open('w',encoding='utf-8',newline='')as f:
   w=csv.writer(f);w.writerow(['ref','xMm','yMm','rotation']);w.writerows([r,*pos]for r,pos in sorted(placed.items()))
  print(json.dumps({'candidate':name,'placed':len(placed),'audit':audit}))
 except Exception as e:
  (P/(name+'_PASS1_PARTIAL.json')).write_text(json.dumps({'positions':placed,'error':str(e)},indent=2),encoding='utf-8');(P/(name+'_PASS1_FAILURE.log')).write_text(traceback.format_exc(),encoding='utf-8');raise
(P/'FUNCTIONAL_TARGET_REGISTER.json').write_text(json.dumps(targets,indent=2),encoding='utf-8')
(P/'MACRO_ANCHORS_AND_MECHANICAL_RESERVES.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
