from pathlib import Path
import json,csv,math,datetime,sys,itertools
import numpy as np
from shapely.geometry import box
from shapely.ops import unary_union
from placement_geometry import G,C,body,physical,newpad
P=Path(__file__).parent
def write(name,data): (P/name).write_text(json.dumps(data,indent=2),encoding='utf8')
def reserve(kind,reason):
 b=json.loads((P/'EXECUTION_BUDGET.json').read_text());now=datetime.datetime.now(datetime.timezone.utc)
 assert b['status']=='ACTIVE' and now<datetime.datetime.fromisoformat(b['deadlineUTC'])
 assert b['actual'][kind]+1<=b['limits'][kind]
 b['actual'][kind]+=1;b['reservations'].append({'UTC':now.isoformat(),'kind':kind,'reason':reason});write('EXECUTION_BUDGET.json',b);return b['actual'][kind]
def pd(r,num):return next(p for p in G[r]['pads'] if p['number']==str(num))
def point(r,num,pos):return np.array(newpad(r,pd(r,num),pos[r]))
def local(r,num):return np.array(newpad(r,pd(r,num),(0,0,0)))
baseA={'J2':(2,38,90),'U1':(20,26,90),'U2':(20,49,90),'U4':(35,26,90),'U3':(49,24,0),'U6':(49,13,180),'U5':(41,49,180),'U7':(65,49,180),'U13':(55,35,90),'U14':(55,26,90),'U15':(63,35,180),'J3':(78,53,90),'J4':(78,35,90),'J1':(4,4,0),'U9':(20,7,0),'U8':(39,7,180),'U10':(58,7,0),'U11':(24,16,0),'U12':(62,17,0)}
baseB={'J2':(2,36,90),'U1':(20,22,90),'U2':(20,46,90),'U4':(33,22,90),'U3':(45,22,0),'U6':(47,10,180),'U5':(41,46,180),'U7':(64,46,180),'U13':(55,33,90),'U14':(57,23,90),'U15':(65,33,180),'J3':(77,54,90),'J4':(77,35,90),'J1':(4,4,0),'U9':(18,7,0),'U8':(36,7,180),'U10':(53,7,0),'U11':(23,15,0),'U12':(67,15,0)}
def macro_summary(pos):
 # Known signal lanes, true corresponding IC pad connections; no old coordinates used.
 edges=[('U2','1','U5','16'),('U2','7','U5','18'),('U2','8','U5','21'),('U2','14','U5','23'),('U5','1','U7','14'),('U5','36','U7','13'),('U3','1','U4','4'),('U3','7','U4','2'),('U4','3','U1','3'),('U4','8','U1','5'),('U9','6','U8','1'),('U8','5','U10','5')]
 return {'positions':pos,'edgeDistancesMm':[{'from':a+'.'+ap,'to':b+'.'+bp,'length':float(np.linalg.norm(point(a,ap,pos)-point(b,bp,pos)))} for a,ap,b,bp in edges],'macroPhysicalCollisions':[(a,b) for a,b in itertools.combinations(pos,2) if physical(a,pos[a]).intersection(physical(b,pos[b])).area>1e-8],'note':'candidate compares actual pin lanes, footprint compatibility/local-cell closure pending; no former positions used as seed'}
def initmacro():
 for label,pos in [('A',baseA),('B',baseB)]:reserve('macroCandidates',label);write('MACRO_'+label+'.json',macro_summary(pos))
 write('MACRO_SELECTION.json',{'selected':'A','reason':'A gives more ROW/MUX and ADC/Bias separation than B. Equal analog/digital direction, interface orientation fixed by actual pins. Extra area accepted for pin-neighborhood; area not minimization goal.','selectedBeforePlacement':True})
keys=[]
for q in csv.DictReader((P/'KEY_PIN_DISTANCE_B21.csv').open(encoding='utf-8-sig')):
 keys.append({'ic':q['icRef'],'icPad':q['icPad'],'passive':q['passiveRef'],'passivePad':q['passivePad'],'limit':float(q['B21Mm']),'association':q['association']})
for q in csv.DictReader((P/'EXTRA_LOCAL_PIN_DISTANCES.csv').open(encoding='utf-8-sig')):
 keys.append({'ic':q['ic'],'icPad':q['icPad'],'passive':q['passive'],'passivePad':q['passivePad'],'limit':float(q['beforeMm']),'association':'EXTRA_LOCAL_PIN_SAME_NET'})
def keyrows(r):return [q for q in keys if q['passive']==r]
def key_ok(r,pos,cand):
 for q in keyrows(r):
  d=np.linalg.norm(newpad(r,pd(r,q['passivePad']),cand)-point(q['ic'],q['icPad'],pos))
  if d>q['limit']+1e-6:return False
 return True
def outline_center(r,pos):
 g=G[r];bb=body(r,pos[r]).bounds;return np.array([(bb[0]+bb[2])/2,(bb[1]+bb[3])/2])
def nearest_association(r):
 if keyrows(r):return keyrows(r)[0]['ic']
 if r.startswith(('D_TIA','RF','CF','R_TIA','R_COL')):return'U2'
 if r.startswith(('D_ROW','R_ROW','R_ISO')):return'U1'
 if r.startswith(('RD_','D_V','R_V','C_DIV')):return'U3'
 if r=='C_PWR':return'U9'
 if r=='C_MCU_BULK':return'U7'
 if r in ['C_RST','R_RST']:return'U15'
 if r=='R_ENABLE_PD':return'U13'
 if r=='R_HW_PD':return'U14'
 if r=='R_ADC_RESET_PD':return'U13'
 if r=='R_CS_PU':return'U5'
 if r.startswith('R_SEL_PD'):return'U4'
 if r.startswith(('D_J3','R_J3')):return'J3'
 if r.startswith(('D_J4','R_J4')):return'J4'
 if r.startswith('U9_'):return'U9'
 if r.startswith('U10_'):return'U10'
 if r.startswith('U11_'):return'U11'
 if r.startswith('U12_'):return'U12'
 if r=='C_MUX':return'U4'
 if r.startswith('C_U'):return r[2:]
 raise RuntimeError('NO_EXPLICIT_ASSOCIATION '+r)
def anchor(r,ic,pos):
 qs=keyrows(r)
 if qs:return np.mean([point(ic,q['icPad'],pos) for q in qs],axis=0)
 nets=set(p['net'] for p in G[r]['pads'])-{'GND','V5','V3V3',''}
 candidates=[p for p in G[ic]['pads'] if p['net'] in nets]
 if not candidates:candidates=[p for p in G[ic]['pads'] if p['net'] in set(q['net'] for q in G[r]['pads']) and p['net']!='GND']
 if not candidates:return np.array(pos[ic][:2])
 return np.mean([newpad(ic,p,pos[ic]) for p in candidates],axis=0)
def preferred(r,ic,pos):
 # New explicit pin-cluster stations at U5, derived from pin5/7/9/30/34 and package dimensions.
 # These are not former block coordinates; preserve space for REFCAP before larger REFIO.
 adcstations={'C_ADC_REFCAP':(2,6.5),'C_ADC_REFIO':(6,5.0),'C_AVDD9_HF':(-1.8,5.7),'C_AVDD30_HF':(0,-5.7),'C_DVDD34A':(5.5,-5.7)}
 if r in adcstations:return np.array(pos['U5'][:2])+np.array(adcstations[r])
 a=anchor(r,ic,pos);d=a-np.array(pos[ic][:2]);d=d/max(np.linalg.norm(d),1e-8)
 # Channel cells grow from pin outward; supply dividers/remaining parts keep local pin-centered mesh.
 if r.startswith(('D_J','R_J')):d=np.array([-1.,0.])
 dist=2.2
 if r.startswith(('D_TIA','D_ROW')):dist=6.0
 if r.startswith(('RF','CF')):dist=5.0
 if r.startswith(('R_COL','R_ROW_FB','R_ISO','R_TIA_ISO')):dist=3.8
 if r.startswith('RD_'):dist=4.5
 return a+dist*d
def construct(passid):
 pos={r:tuple(v) for r,v in baseA.items()};placedshape={r:physical(r,v) for r,v in pos.items()};trace=[]
 # Reserve interfaces independently. J2 planning cable rectangle extends left (rotation90) beyond footprint.
 j2=physical('J2',pos['J2']).bounds;keep=box(j2[0]-10,j2[1]-2,j2[0],j2[3]+2)
 def place(r):
  ic=nearest_association(r);aa=anchor(r,ic,pos);pref=preferred(r,ic,pos)
  # Finite pin-side neighborhood, no global optimizer. Enumerate 0.5mm local mesh and four rotations.
  candidates=[];angles=[0,90,180,270]
  maxrad=12 if not keyrows(r) else min(13,max(q['limit'] for q in keyrows(r))+3)
  for dx in np.arange(-maxrad,maxrad+.001,.5):
   for dy in np.arange(-maxrad,maxrad+.001,.5):
    x,y=aa+np.array([dx,dy])
    if x<-2 or x>82 or y<-1 or y>65:continue
    for ang in angles:
     cand=(round(float(x),5),round(float(y),5),ang)
     if not key_ok(r,pos,cand):continue
     # Pin matching cost; local cell preferred position, global rectangle only a weak tie breaker.
     kd=sum(float(np.linalg.norm(newpad(r,pd(r,q['passivePad']),cand)-point(q['ic'],q['icPad'],pos))) for q in keyrows(r))
     match=0
     for p in G[r]['pads']:
      n=p['net'];pps=[pp for pp in G[ic]['pads'] if pp['net']==n and n not in ('GND','V5','V3V3','')]
     if pps:match+=min(np.linalg.norm(np.array(newpad(r,p,cand))-np.array(newpad(ic,pp,pos[ic]))) for pp in pps)
     score=kd+match*.7+np.linalg.norm(np.array(cand[:2])-pref)*1.2
     candidates.append((float(score),cand))
  candidates.sort(key=lambda t:t[0]);chosen=None
  for score,cand in candidates:
   sh=physical(r,cand)
   if sh.intersects(keep):continue
   if any(sh.distance(other)<.18-1e-8 for other in placedshape.values()):continue
   chosen=cand;break
  if chosen is None:
   write('PLACEMENT_PASS_'+str(passid)+'_PARTIAL.json',{'positions':pos,'failedRef':r,'candidates':len(candidates),'trace':trace});raise RuntimeError('NO_PIN_SIDE_LEGAL_POSITION '+r)
  pos[r]=chosen;placedshape[r]=physical(r,chosen);trace.append({'ref':r,'ic':ic,'anchor':aa.tolist(),'preferred':pref.tolist(),'chosen':chosen,'finiteCandidates':len(candidates),'method':'actual-pin mesh with all-key bound, local cell score and global collision test'})
 # Tightest parts first. HF feedback/proper decap never relocated by later large components.
 remaining=set(G)-set(pos)
 def order(r):
  qs=keyrows(r);m=min([q['limit'] for q in qs]+[99])
  return (0 if r.startswith(('C_TIA_HF','C_ROW_HF','C_VCM_HF','C_VEX_HF')) else 1 if r=='C_ADC_REFCAP' else 2 if r=='C_ADC_REFIO' else 3 if qs else 4 if r.startswith(('RF','CF','R_TIA_ISO','R_COL','R_ROW_FB','R_ISO','C_ADC','R_ADC','D_TIA','D_ROW')) else 5, m,nearest_association(r),r)
 for r in sorted(remaining,key=order):place(r)
 write('PLACEMENT_PASS_'+str(passid)+'.json',{'positions':pos,'trace':trace,'constructionInputs':'ACTUAL_GEOMETRY local shapes/pads and newMACRO_A, key-distance bounds only; B22 coordinates not loaded','J2PlanningKeepoutBounds':list(keep.bounds)})
 return pos
if __name__=='__main__':
 if sys.argv[1]=='macro':initmacro();print('2 MACRO SAVED A SELECTED')
 else:
  n=reserve('placementRefinements','finite pin-side176 construction '+sys.argv[1]);pos=construct(n);write('PLACEMENT_B3.json',{'positions':pos,'pass':n});print('COMPLETE',n,len(pos))
