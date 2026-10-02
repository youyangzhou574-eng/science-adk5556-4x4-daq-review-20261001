from b31_core import *
from placement_geometry import padshape
from shapely.affinity import rotate,translate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch,Rectangle
N=json.loads((P/'PLACEMENT_B31.json').read_text())['positions']
COLORS={'TIA':'#227d99','ROW':'#459c78','ADC':'#986bb1','BIAS_MUX':'#c98726','POWER':'#a96243','DIGITAL':'#4976ae','INTERFACE_J2':'#444d5c'}
if __name__=='__main__':
 # Newpackage image quota, not previousB31 imagecounter.
 b=json.loads((P/'EXECUTION_BUDGET.json').read_text());assert b['status']=='ACTIVE' and b['actual']['finalImages']==0
 b['actual']['finalImages']=1;b['reservations'].append({'kind':'finalImages','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'one final frozen176 image with 5 actualseries paths and8cells'});save('EXECUTION_BUDGET.json',b)
 bounds=unary_union([body(r,v) for r,v in N.items()]).bounds;ox,oy=bounds[:2]
 fig,ax=plt.subplots(figsize=(15,12),dpi=190)
 for r in sorted(N):
  sh=body(r,N[r]);polys=list(sh.geoms) if sh.geom_type=='MultiPolygon' else[sh]
  for s in polys:ax.add_patch(Patch([(x-ox,y-oy) for x,y in s.exterior.coords],fc=COLORS[family(r)],ec='white',lw=.25))
  for p in G[r]['pads']:
   s=translate(rotate(translate(padshape(p),xoff=-G[r]['xMm'],yoff=-G[r]['yMm']),N[r][2]-G[r]['rotation'],origin=(0,0)),xoff=N[r][0]-ox,yoff=N[r][1]-oy)
   if s.geom_type=='Polygon':ax.add_patch(Patch(list(s.exterior.coords),fc='#a3acb1',ec='#657781',lw=.15))
  if r.startswith('U') and r[1:].isdigit() or r.startswith('J'):
   x,y=N[r][:2];ax.annotate(r,(x-ox,y-oy),xytext=(0,0 if r in ['U1','U2','U3','U4','U5','U7','J1','J2','J3','J4'] else -13),textcoords='offset points',ha='center',va='center',fontsize=8,fontweight='bold',color='white' if r in ['U1','U2','U3','U4','U5','U7','J1','J2','J3','J4'] else '#283d4b',bbox=None if r in ['U1','U2','U3','U4','U5','U7','J1','J2','J3','J4'] else {'fc':'white','ec':'none','alpha':.8,'pad':.3})
 register=json.loads((P/'CHANNEL_CELL_REGISTER.json').read_text())
 for f in ['TIA','ROW']:
  for i in range(4):
   refs=[x['ref'] for x in register if x['family']==f and x['channel']==i];bb=unary_union([physical(r,N[r]) for r in refs]).bounds
   ax.add_patch(Rectangle((bb[0]-ox-.3,bb[1]-oy-.3),bb[2]-bb[0]+.6,bb[3]-bb[1]+.6,fill=False,ec=COLORS[f],ls=':',lw=1))
   ax.text(bb[0]-ox,bb[3]-oy+.6,f+' CH'+str(i),fontsize=7,color=COLORS[f])
 for q in json.loads((P/'DIGITAL_INTERFACE_CHAIN_AUDIT.json').read_text())['signalPaths']:
  points=[]
  for node in q['orderedNodes']:
   r,p=node.split('.');x,y=pt(N,r,p);points.append((x-ox,y-oy))
  # Dashed functions, include R span. Not native copper and no router used.
  ax.plot([x for x,y in points],[y for x,y in points],ls='--',lw=.7,alpha=.65,color='#b55d32')
 ax.add_patch(Rectangle((0,0),bounds[2]-ox,bounds[3]-oy,fill=False,ls='--',ec='#6a737d',lw=.8))
 ax.set_xlim(-4,78);ax.set_ylim(-3,68);ax.set_aspect('equal');ax.grid(alpha=.10);ax.set_xlabel('Display X (mm, body-min recentered)');ax.set_ylabel('Display Y (mm)')
 ax.set_title('B31 FROZEN PLACEMENT - DIGITAL CHAINS QUALIFIED FOR GEOMETRY REVIEW\n176 parts / 552 pads - NO COORDINATE CHANGE - USER VISUAL CHOICE PENDING',fontsize=12,pad=16)
 ax.legend(handles=[Rectangle((0,0),1,1,fc=c,label=f) for f,c in COLORS.items()],loc='upper center',bbox_to_anchor=(.5,-.08),ncol=4,fontsize=8)
 fig.text(.5,.037,'Dashed orange = 5 actual MCU - series resistor - interface functional paths; associations, NOT routed copper. Dashed bbox = natural body envelope, NOT board outline.',ha='center',fontsize=8)
 fig.text(.5,.020,'73.90 x 61.92 mm body envelope. ROW/Power length tradeoffs accepted for placement only. No native PCB / routing / performance / manufacturing release.',ha='center',fontsize=8)
 fig.text(.5,.006,'TIA/ROW role topology retained. Exact FFC actuator mechanics remain pending. Full176/552 metadata and actual 2-segment lengths in readable CSV.',ha='center',fontsize=8)
 fig.tight_layout(rect=[0,.08,1,.97]);fig.savefig(P/'B311_FINAL_FROZEN_PLACEMENT.png');plt.close(fig)
 print('one final image1/1, coordinates unchanged')
