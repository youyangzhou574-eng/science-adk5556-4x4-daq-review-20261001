from b31_core import *
import sys,time,traceback
def roles(f,i):
 return {'HF':'C_'+f+'_HF'+str(i),'SENSE':('R_COL_SENSE' if f=='TIA' else 'R_ROW_FB')+str(i),'ISO':('R_TIA_ISO' if f=='TIA' else 'R_ISO')+str(i),'CLAMP':'D_'+f+str(i)} | ({'RF':'RF'+str(i),'CF':'CF'+str(i)} if f=='TIA' else {})
def channel_frame(ic,i,pos):
 op=[1,7,8,14][i];ip=[2,6,9,13][i];origin=(pt(pos,ic,op)+pt(pos,ic,ip))/2
 return origin,np.array([1 if i in [0,1] else -1,-1 if i in [0,3] else 1])
def cell_positions(f,pos,params):
 ic='U2' if f=='TIA' else 'U1';out={};reg=[]
 for i in range(4):
  a,s=channel_frame(ic,i,pos);rs=roles(f,i)
  xy={'HF':(params['hf'],0),'SENSE':(params['iso'],2.1 if f=='ROW' else -1.25),'ISO':(params['iso'],-2.1 if f=='ROW' else 1.25),'CLAMP':(params['clampX'],params['clampY']),'RF':(params['rf'],0),'CF':(params['cf'],0)}
  for role,r in rs.items():
   x,y=a+s*np.array(xy[role]);angle=(90 if s[1]<0 else 270) if role in ['HF','RF','CF'] else (0 if s[0]>0 else 180) if role in ['ISO','CLAMP'] else (180 if s[0]>0 else 0)
   out[r]=(float(x),float(y),angle);reg.append({'family':f,'channel':i,'role':role,'ref':r,'origin':a.tolist(),'signs':s.tolist(),'canonicalCentreMm':list(xy[role]),'rotation':angle})
 return out,reg
def conflict(cands,placed,keep):
 sh={r:physical(r,v) for r,v in cands.items()}
 for r,x in sh.items():
  if x.intersection(keep).area>1e-8:return r+' FFC_ZONE'
  if any(x.distance(y)<.18-1e-8 for y in placed.values()):return r+' EXISTING_PROXY'
 for a,b in itertools.combinations(sh,2):
  if sh[a].distance(sh[b])<.18-1e-8:return a+' '+b
 return None
def construct(passid):
 pos={r:tuple(v) for r,v in json.loads((P/'MACRO_SELECTION.json').read_text())['positions'].items()}
 assert not macro_audit(pos)['physicalCollisions']
 placed={r:physical(r,v) for r,v in pos.items()};j2=placed['J2'].bounds;keep=box(j2[0]-10,j2[1]-2,j2[0],j2[3]+2);trace=[];cells=[]
 def partial(why):save('PLACEMENT_PASS_'+str(passid)+'_PARTIAL.json',{'positions':pos,'failed':why,'trace':trace,'cells':cells})
 # Simultaneous four-channel templates, common role offsets and reflected local pin frames.
 for f in ['TIA','ROW']:
  proposals=[];rejected=[]
  for hf,iso,rf,cf,cx,cy in itertools.product([1.6,1.9],[1.9,2.2,2.5] if f=='ROW' else [3.4,3.7],[5.3,5.6],[7.0,7.25],[4.3,5.4],[3.5,4.4]):
   params={'hf':hf,'iso':iso,'rf':rf,'cf':cf,'clampX':cx,'clampY':cy};cs,rg=cell_positions(f,pos,params)
   if not all(keyok(r,v,pos) for r,v in cs.items()):continue
   why=conflict(cs,placed,keep)
   if why:rejected.append(why);continue
   score=sum(pincost(r,'U2' if f=='TIA' else 'U1',v,pos) for r,v in cs.items())+.3*(cx+cy+cf+rf)
   proposals.append((score,params,cs,rg))
  if not proposals:
   partial('NO_COMPLETE_'+f+'_CELL_TEMPLATE');save('CELL_FAILED_'+str(passid)+'_'+f+'.json',{'rejections':rejected});raise RuntimeError('NO_COMPLETE_'+f+'_CELL_TEMPLATE')
  score,params,cs,rg=min(proposals,key=lambda x:x[0]);pos.update(cs);placed.update({r:physical(r,v) for r,v in cs.items()});cells.extend(rg);trace.append({'completeFamily':f,'params':params,'feasibleTemplates':len(proposals),'score':score})
 def preferred(r,ic):
  adc={'C_ADC_REFCAP':(2,6.5),'C_ADC_REFIO':(6,5),'C_AVDD9_HF':(-1.8,5.7),'C_AVDD30_HF':(0,-5.7),'C_DVDD34A':(5.5,-5.7)}
  if r in adc:return np.array(pos['U5'][:2])+adc[r]
  if r in ['C_ADC0','C_ADC1','C_ADC2','C_ADC3','R_ADC0','R_ADC1','R_ADC2','R_ADC3']:
   i=int(r[-1]);aa=pt(pos,'U5',[16,18,21,23][i]);return aa+[-2.5 if r.startswith('C_') else -4.5,0]
  aa=anchor(r,ic,pos);d=aa-np.array(pos[ic][:2]);d=d/max(np.linalg.norm(d),1e-8)
  if r.startswith(('D_J','R_J')):d=np.array([-1.,0.])
  return aa+d*(4.5 if r.startswith('RD_') else 2.2)
 def place(r):
  ic=association(r);aa=anchor(r,ic,pos);pref=preferred(r,ic);ks=krows(r)
  radius=12 if not ks else min(13,max(q['limit'] for q in ks)+3)
  candidates=[]
  for dx in np.arange(-radius,radius+.001,.5):
   for dy in np.arange(-radius,radius+.001,.5):
    x,y=aa+[dx,dy]
    if x<-2 or x>73 or y<-1 or y>66:continue
    for ang in [0,90,180,270]:
     cand=(round(float(x),5),round(float(y),5),ang)
     if not keyok(r,cand,pos):continue
     kd=sum(math.dist(newpad(r,pd(r,q['passivePad']),cand),pt(pos,q['ic'],q['icPad'])) for q in ks)
     # Every meaningful matching pad, including power EN/input, counts before collision choice.
     score=kd+pincost(r,ic,cand,pos)*.7+math.dist(cand[:2],pref)*1.2
     candidates.append((score,cand))
  candidates.sort(key=lambda v:v[0]);chosen=None
  for score,cand in candidates:
   sh=physical(r,cand)
   if sh.intersection(keep).area>1e-8:continue
   if any(sh.distance(other)<.18-1e-8 for other in placed.values()):continue
   chosen=cand;break
  if chosen is None:partial('NO_LOCAL_POSITION '+r);raise RuntimeError('NO_LOCAL_POSITION '+r)
  pos[r]=chosen;placed[r]=physical(r,chosen);trace.append({'ref':r,'ic':ic,'anchor':aa.tolist(),'preferred':pref.tolist(),'chosen':chosen,'finiteCandidates':len(candidates)})
 def order(r):
  ks=krows(r);m=min([q['limit'] for q in ks]+[99]);a=0 if r.startswith(('C_VCM_HF','C_VEX_HF','C_TIA_OP','C_ROW_OP')) else 1 if r=='C_ADC_REFCAP' else 2 if r=='C_ADC_REFIO' else 3 if ks else 4
  return a,m,association(r),r
 for r in sorted(set(G)-set(pos),key=order):place(r)
 save('PLACEMENT_PASS_'+str(passid)+'.json',{'positions':pos,'trace':trace,'cellRegister':cells,'J2PlanningKeepoutBounds':list(keep.bounds),'seed':'selected verified MACRO_B1/B2 only; all176 generated, no B3-A position seed'})
 save('PLACEMENT_B31.json',{'positions':pos,'pass':passid});save('CHANNEL_CELL_REGISTER.json',cells);return pos
if __name__=='__main__':
 n=reserve('placementRefinements','complete176 MacroB pin construction pass');print('RESERVED',n,flush=True)
 try:
  out=construct(n);print('COMPLETE',n,len(out),flush=True)
 except Exception:traceback.print_exc();sys.exit(1)
