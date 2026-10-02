from pathlib import Path
import json,math,csv
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as PlotPath
from matplotlib.patches import PathPatch,Circle
from shapely.geometry import Polygon
P=Path(__file__).parent;v=json.loads((P/'COLD_CAPTURE_AND_NATIVE.json').read_text('utf8'))['parsed']['value']['capture'];rs=[]
for ln in v['source'].splitlines():
 if '||'not in ln:continue
 h,b=ln.split('||',1)
 try:rs.append((json.loads(h),json.loads(b.rstrip('|'))))
 except ValueError:pass
def points(path):
 x,y=path[:2];out=[(x*.254,y*.254)];i=2;mode='L'
 while i<len(path):
  if isinstance(path[i],str):mode=path[i];i+=1;continue
  if mode=='ARC':
   ang,nx,ny=path[i:i+3];i+=3;theta=math.radians(ang);dx,dy=nx-x,ny-y
   if abs(math.sin(theta/2))>1e-10:
    cx=(x+nx)/2-dy/(2*math.tan(theta/2));cy=(y+ny)/2+dx/(2*math.tan(theta/2));sx,sy=x-cx,y-cy;n=max(4,math.ceil(abs(ang)/2))
    for k in range(1,n+1):
     t=theta*k/n;out.append(((cx+sx*math.cos(t)-sy*math.sin(t))*.254,(cy+sx*math.sin(t)+sy*math.cos(t))*.254))
   else:out.append((nx*.254,ny*.254))
   x,y=nx,ny;mode='L'
  else:x,y=path[i:i+2];i+=2;out.append((x*.254,y*.254))
 return out
lines=[dict(id=h['id'],**b)for h,b in rs if h['type']=='LINE'];vias=[dict(id=h['id'],**b)for h,b in rs if h['type']=='VIA'];pours={h['id']:b for h,b in rs if h['type']=='POUR'};fills=[]
for h,b in rs:
 if h['type']!='POURED':continue
 parent=json.loads(h['id'])[1];p=pours[parent]
 for chunk in b['pourFill']:
  if not chunk.get('fill'):continue
  ps=chunk['path'];ps=ps if isinstance(ps[0],list)else[ps];rings=[points(q)for q in ps];fills.append({'id':parent,'layer':p['layerId'],'net':p['netName'],'rings':rings})
def draw(ax,layer,local):
 for f in fills:
  if f['layer']!=layer:continue
  vertices=[];codes=[]
  for ring in f['rings']:
   vertices.extend(ring+[ring[0]]);codes.extend([PlotPath.MOVETO]+[PlotPath.LINETO]*(len(ring)-1)+[PlotPath.CLOSEPOLY])
  ax.add_patch(PathPatch(PlotPath(vertices,codes),facecolor={'GND':'#a8c9a1','V3V3':'#d2b1df','V5':'#efc582'}.get(f['net'],'#c9c9c9'),edgecolor='#5e7158',lw=.3))
 for t in lines:
  if t['layerId']!=layer:continue
  ax.plot([t['startX']*.0254,t['endX']*.0254],[t['startY']*.0254,t['endY']*.0254],color='#a72c39'if t['netName']=='V3V3'else'#284b8c',lw=max(.3,t['width']*.04),alpha=.95)
 for t in vias:
  x,y=t['centerX']*.0254,t['centerY']*.0254
  ax.add_patch(Circle((x,y),t['viaDiameter']*.0254/2,facecolor='#b15d87'if t['netName']=='V3V3'else'#909e91',edgecolor='#343434',lw=.35))
  ax.add_patch(Circle((x,y),t['holeDiameter']*.0254/2,facecolor='white',edgecolor='#303030',lw=.25))
 if local:
  ax.set_xlim(79.5,87.5);ax.set_ylim(48.5,43.5);ax.annotate('e307 V3V3',(3380*.0254,1790.7*.0254),xytext=(83,44),arrowprops={'arrowstyle':'->','lw':.8},fontsize=9)
 else:ax.set_xlim(0,100);ax.set_ylim(90,0)
 ax.set_aspect('equal');ax.set_xlabel('x mm');ax.set_ylabel('y mm');ax.grid(alpha=.15)
for name,local in(('FINAL_FOUR_COPPER_LAYERS.png',False),('FINAL_LOCAL_VIA_AND_ANTIPADS.png',True)):
 fig,axes=plt.subplots(2,2,figsize=(13,11))
 for ax,layer,label in zip(axes.flat,(1,15,16,2),('Top / GND fill','Inner1 / GND plane','Inner2 / V3V3 and V5','Bottom routing')):draw(ax,layer,local);ax.set_title(label)
 fig.suptitle('Actual cold PCB source — engineering review only\nNative warm/cold DRC zero; no manufacturing/bench release; ARC render max step2deg',fontsize=12);fig.tight_layout(rect=(0,0,1,.94));fig.savefig(P/name,dpi=180);plt.close(fig)
for name,rows in(('FINAL_ACTUAL_909_LINES.csv',lines),('FINAL_ACTUAL_297_VIAS.csv',vias)):
 with(P/name).open('w',encoding='utf8',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(P/'REVIEW_BATCH_METADATA.json').write_text(json.dumps({'scope':'One offline review batch from existing actualcold capture; no CAD mutation/export/save or scientificsolve','PNGfiles':['FINAL_FOUR_COPPER_LAYERS.png','FINAL_LOCAL_VIA_AND_ANTIPADS.png'],'LINE':len(lines),'VIA':len(vias),'arcMaxStepDegrees':2,'rendersApproximateNativeArcs':True,'manufactureBenchReleased':False},indent=2),'utf8');print('One reviewbatch:2PNG +2actualcopperCSV, no newCAD.')
