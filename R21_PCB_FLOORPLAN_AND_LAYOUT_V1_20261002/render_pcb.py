import pathlib,json,math,sys
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Ellipse,Polygon
from matplotlib.transforms import Affine2D
P=pathlib.Path(__file__).resolve().parent;label=sys.argv[1]
v=json.loads((P/(label+'.json')).read_text('utf8'))['parsed']['value'];floor=json.loads((P/'FLOORPLAN.json').read_text('utf8'))
v['traces']=[]
for ln in v['source'].splitlines():
 bits=ln.split('||')
 if len(bits)!=2:continue
 h=json.loads(bits[0]);b=json.loads(bits[1].rstrip('|'))
 if h['type']=='LINE':v['traces'].append({'layer':b['layerId'],'width':b['width'],'x1':b['startX'],'y1':b['startY'],'x2':b['endX'],'y2':b['endY']})
def draw(xlim,ylim,file,title):
 fig,ax=plt.subplots(figsize=(15,13));ax.set_facecolor('#123d30');fig.patch.set_facecolor('white')
 for c in v['parts']:
  if not(xlim[0]-5<c['x']*.0254<xlim[1]+5 and ylim[0]-5<c['y']*.0254<ylim[1]+5):continue
  note=floor['notes'][c['ref']];b=note['envelope_mm'];ax.add_patch(Rectangle((b[0],b[1]),b[2]-b[0],b[3]-b[1],fill=False,edgecolor='#98bca5',lw=.5))
  for p in c['pads']:
   x,y=p['x']*.0254,p['y']*.0254;s=p['pad'];color='#eda867' if p['net'] else '#666666'
   if s[0]=='POLYGON':
    co=[a for a in s[1]if isinstance(a,(int,float))];patch=Polygon([(a*.0254,b*.0254)for a,b in zip(co[::2],co[1::2])],facecolor=color,edgecolor='none');ax.add_patch(patch)
   else:
    w,h=s[1]*.0254,s[2]*.0254
    if s[0]=='ELLIPSE':patch=Ellipse((x,y),w,h,angle=p['rotation'],facecolor=color)
    else:patch=Rectangle((-w/2,-h/2),w,h,facecolor=color,edgecolor='none');patch.set_transform(Affine2D().rotate_deg(p['rotation']).translate(x,y)+ax.transData)
    ax.add_patch(patch)
   if p.get('hole'):
    ho=p['hole'];diam=ho[1]*.0254 if isinstance(ho,list) and len(ho)>1 and isinstance(ho[1],(int,float))else .8;ax.add_patch(Ellipse((x,y),diam,diam,facecolor='#123d30'))
  ax.text(c['x']*.0254,b[1]-.2,c['ref'],color='white',ha='center',va='bottom',fontsize=5 if file=='PCB_FULL_LAYOUT.png'else 8)
 for tr in v.get('traces',[]):
  if tr['layer']!=1:continue
  ax.plot([tr['x1']*.0254,tr['x2']*.0254],[tr['y1']*.0254,tr['y2']*.0254],color='#fdcb72',lw=max(.4,tr['width']*.15))
 ax.plot([0,100,100,0,0],[0,0,90,90,0],color='#eeeeee',lw=2)
 ax.set_xlim(xlim);ax.set_ylim(ylim[::-1]);ax.set_aspect('equal');ax.set_xlabel('X / mm');ax.set_ylabel('Y / mm');ax.set_title(title+'\nActual native pad capture; review only, no manufacturing release')
 fig.tight_layout();fig.savefig(P/file,dpi=230);plt.close(fig)
draw((-2,102),(-2,92),'PCB_FULL_LAYOUT.png','R2.1 PCB — provisional 100 x 90 mm, four copper layers')
draw((12,67),(4,69),'PCB_ANALOG_DETAIL.png','Analog island — ROW, references, TIA and ADC')
print('Rendered full actual PCB layout and analog detail')
