from b31_core import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch,Rectangle
from placement_geometry import padshape
from shapely.affinity import rotate,translate
from construct_b31 import roles
N=json.loads((P/'PLACEMENT_B31.json').read_text())['positions'];O=json.loads((P/'PLACEMENT_B3.json').read_text())['positions']
colors={'TIA':'#227d99','ROW':'#459c78','ADC':'#986bb1','BIAS_MUX':'#c98726','POWER':'#a96243','DIGITAL':'#4976ae','INTERFACE_J2':'#444d5c'}
def draw(ax,pos,title):
 b=unary_union([body(r,v) for r,v in pos.items()]).bounds;ox,oy=b[:2]
 for r in sorted(pos):
  sh=body(r,pos[r]);polys=list(sh.geoms) if sh.geom_type=='MultiPolygon' else [sh]
  for s in polys:ax.add_patch(Patch([(x-ox,y-oy) for x,y in s.exterior.coords],fc=colors[family(r)],ec='white',lw=.25))
  for p in G[r]['pads']:
   s=translate(rotate(translate(padshape(p),xoff=-G[r]['xMm'],yoff=-G[r]['yMm']),pos[r][2]-G[r]['rotation'],origin=(0,0)),xoff=pos[r][0]-ox,yoff=pos[r][1]-oy)
   if s.geom_type=='Polygon':ax.add_patch(Patch(list(s.exterior.coords),fc='#a3acb1',ec='#657781',lw=.15))
  anchor=r in json.loads((P/'MACRO_SELECTION.json').read_text())['positions']
  if anchor:ax.text(pos[r][0]-ox,pos[r][1]-oy,r,color='white',ha='center',va='center',fontsize=8,fontweight='bold',zorder=10)
 ax.add_patch(Rectangle((0,0),b[2]-ox,b[3]-oy,fill=False,ls='--',ec='#6a737d',lw=.8))
 ax.set_xlim(-13,90);ax.set_ylim(-4,69);ax.set_aspect('equal');ax.set_xlabel('Display X (mm, body-min recentered)');ax.set_ylabel('Display Y (mm)');ax.grid(alpha=.12);ax.set_title(title,fontsize=12)
 return ox,oy
if __name__=='__main__':
 reserve('finalImages','actual failedB3A versus available B31 completepass1 same mm scale')
 fig,axs=plt.subplots(1,2,figsize=(18,8),dpi=190);draw(axs[0],O,'B3-A BEFORE: macro collision / 83.90 x 58.32 mm');draw(axs[1],N,'B31 complete PASS1: no proxy overlap / 73.90 x 61.92 mm')
 fig.suptitle('REAL OFFLINE PLACEMENT COMPARISON - B31 STILL HOLD',fontsize=17);fig.text(.5,.025,'Same mm scale. No copper or board outline. Pass2/3 failed; final candidate not accepted. ROW interface growth +7.31/+7.39 mm; power input +2.55 mm vsB22.',ha='center',fontsize=9);fig.tight_layout(rect=[0,.055,1,.94]);fig.savefig(P/'B3A_vs_B31_FINAL.png');plt.close(fig)
 reserve('finalImages','actual176 and552 proxies with complete8cell outlines, direction and powerstrip')
 fig,ax=plt.subplots(figsize=(16,11),dpi=190);ox,oy=draw(ax,N,'B31 COMPLETE PASS1 - 176 actual footprint bodies / 552 pad proxies - HOLD')
 for f,ic in [('TIA','U2'),('ROW','U1')]:
  for i in range(4):
   bb=unary_union([physical(r,N[r]) for r in roles(f,i).values()]).bounds
   ax.add_patch(Rectangle((bb[0]-ox-.3,bb[1]-oy-.3),bb[2]-bb[0]+.6,bb[3]-bb[1]+.6,fill=False,ec=colors[f],ls=':',lw=1.1));ax.text(bb[0]-ox,bb[3]-oy+.6,f+' CH'+str(i),fontsize=7,color=colors[f])
 for a,b,label in [('U2','U5','Analog -> ADC'),('U5','U7','ADC -> SPI / MCU'),('J1','U9','5V IN'),('U9','U8','5V'),('U8','U10','3V LDO')]:
  x1,y1=N[a][:2];x2,y2=N[b][:2];ax.annotate('',(x2-ox,y2-oy),(x1-ox,y1-oy),arrowprops={'arrowstyle':'->','color':'#313e49','alpha':.65});ax.text((x1+x2)/2-ox,(y1+y2)/2-oy+1.5,label,fontsize=8,ha='center',bbox={'fc':'white','ec':'none','alpha':.8})
 ax.legend(handles=[Rectangle((0,0),1,1,fc=c,label=f) for f,c in colors.items()],loc='upper center',bbox_to_anchor=(.5,-.095),ncol=4,fontsize=8)
 fig.text(.5,.028,'Dashed bbox = natural body envelope only. Cells show complete functional role topology; clamp rail pads are not exact mirrored copies. No routed copper/native DRC.',ha='center',fontsize=9);fig.text(.5,.01,'FFC actuator exact mechanics pending. 106 key distances no increase. Readable full designators/pin nets: PLACEMENT_B31.csv and ALL_552_PIN_MAP_B31.csv.',ha='center',fontsize=8);fig.tight_layout(rect=[0,.09,1,1]);fig.savefig(P/'B31_FINAL_NO_COPPER_AND_CELLS.png');plt.close(fig)
 print('2 documented HOLD images; quota now2/2; no additional rendering')
