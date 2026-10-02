import json,math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch,Rectangle
from matplotlib import gridspec
from shapely.affinity import rotate,translate
from placement_geometry import G,body,padshape,newpad
from build_b3 import reserve
from audit_b3 import family
P=Path(__file__).parent
N=json.loads((P/'PLACEMENT_B3.json').read_text())['positions'];O=json.loads((P/'PLACEMENT_B22.json').read_text())['positions']
colors={'TIA':'#227d99','ROW':'#459c78','ADC':'#986bb1','BIAS_MUX':'#c98726','POWER':'#a96243','DIGITAL':'#4976ae','INTERFACE_J2':'#444d5c'}
def norm_bounds(pos):
 bs=[body(r,v).bounds for r,v in pos.items()];return min(b[0] for b in bs),min(b[1] for b in bs),max(b[2] for b in bs),max(b[3] for b in bs)
def plot_geometry(ax,pos,label,labels=True):
 bb=norm_bounds(pos);ox,oy=bb[0],bb[1]
 for r in sorted(pos):
  b=body(r,pos[r]);polys=list(b.geoms) if b.geom_type=='MultiPolygon' else [b]
  for sh in polys:
   xy=[(x-ox,y-oy) for x,y in sh.exterior.coords];ax.add_patch(Patch(xy,facecolor=colors[family(r)],edgecolor='white',lw=.25,alpha=.9))
  for p in G[r]['pads']:
   sh=padshape(p);sh=translate(rotate(translate(sh,xoff=-G[r]['xMm'],yoff=-G[r]['yMm']),pos[r][2]-G[r]['rotation'],origin=(0,0)),xoff=pos[r][0]-ox,yoff=pos[r][1]-oy)
   if sh.geom_type=='Polygon':ax.add_patch(Patch(list(sh.exterior.coords),facecolor='#9ca5ac',edgecolor='#68747d',lw=.15))
  if labels:
   x,y=pos[r][:2];isanchor=(r.startswith('U') and r[1:].isdigit()) or r.startswith('J');ax.text(x-ox,y-oy,r,ha='center',va='center',fontsize=6.5 if isanchor else 3.6,color='white' if isanchor else '#14232f',zorder=5,fontweight='bold' if isanchor else 'normal')
 ax.set_aspect('equal');ax.set_xlim(-14,92);ax.set_ylim(-4,70);ax.grid(alpha=.14,lw=.4);ax.set_xlabel('Display X (mm, body-min recentered)');ax.set_ylabel('Display Y (mm)');ax.set_title(label,fontsize=12)
 ax.add_patch(Rectangle((0,0),bb[2]-ox,bb[3]-oy,fill=False,ls='--',ec='#8c949c',lw=.6))
 return ox,oy
def pin_inset(ax,r,pos,label,chosen=None):
 pp=pos[r];b=body(r,(0,0,pp[2]));polys=list(b.geoms) if b.geom_type=='MultiPolygon' else[b]
 for s in polys:ax.add_patch(Patch(list(s.exterior.coords),fc='#edf0f5',ec='#44556a',lw=.7))
 for p in G[r]['pads']:
  if chosen and p['number'] not in chosen:continue
  x,y=newpad(r,p,(0,0,pp[2]));net=p['net'] or'NC';ax.plot(x,y,'o',ms=2.5,color='#4d667d');sx=1 if x>0 else -1
  # Number/net outside the actual package; sparse key groups only.
  if abs(y)>abs(x):ax.text(x,y+(.6 if y>0 else -.6),p['number']+' '+net,fontsize=5,ha='center',va='bottom' if y>0 else'top',rotation=90)
  else:ax.text(x+sx*.5,y,p['number']+' '+net,fontsize=5,ha='left' if sx>0 else'right',va='center')
 ax.set_xlim(-9,9);ax.set_ylim(-9,9);ax.set_aspect('equal');ax.set_title(label,fontsize=9);ax.axis('off')
if __name__=='__main__':
 reserve('images','B22 vs B3 same-scale geometry comparison')
 fig,aa=plt.subplots(1,2,figsize=(20,10),dpi=170);plot_geometry(aa[0],O,'B22 BEFORE: fixed macro anchors / local passive edits');plot_geometry(aa[1],N,'B3 DRAFT: all 19 anchors moved / real pin-driven neighborhoods')
 fig.suptitle('Offline placement comparison - same mm scale - B3 HOLD: U3/U14 pad-proxy intersection',fontsize=16);fig.text(.5,.025,'Dashed rectangle = body envelope only, not board outline. No copper/routing/native DRC. FFC actual actuator qualification pending.',ha='center',fontsize=9);fig.tight_layout(rect=[0,.045,1,.94]);fig.savefig(P/'B22_vs_B3.png');plt.close(fig)
 reserve('images','B3 pure176-part visual draft')
 fig,ax=plt.subplots(figsize=(15,11),dpi=190);ox,oy=plot_geometry(ax,N,'B3 - actual 176 footprint bodies and 552 pad proxies - review draft')
 x,y=N['J2'][:2];ax.add_patch(Rectangle((x-ox-15.5,y-oy-9.3),10,18.6,fill=False,ls=':',ec='#cc5b59',lw=1));ax.text(x-ox-11,y-oy,'FFC\ncable\nzone',fontsize=8,ha='center',color='#a24d4b')
 for r in ['U3','U14']:
  x,y=N[r][:2];ax.scatter([x-ox],[y-oy],s=450,facecolors='none',edgecolors='#d12727',linewidths=1.5)
 ax.annotate('HOLD: U3/U14 pad proxy overlap',(N['U14'][0]-ox,N['U14'][1]-oy),xytext=(57,23),color='#bb2020',arrowprops={'arrowstyle':'->','color':'#bb2020'},fontsize=9)
 handles=[Rectangle((0,0),1,1,fc=c,label=f) for f,c in colors.items()];ax.legend(handles=handles,ncol=4,loc='upper center',bbox_to_anchor=(.5,-.085),fontsize=8)
 fig.text(.5,.02,'All19 IC/connectors repositioned. Identities/pin-nets frozen. 106 registered key distances non-increasing; one macro pad-proxy collision prevents CAD release.',ha='center',fontsize=8);fig.tight_layout(rect=[0,.07,1,1]);fig.savefig(P/'B3_NO_COPPER.png');plt.close(fig)
 reserve('images','B3 actual pin group and signal-flow review')
 fig=plt.figure(figsize=(20,15),dpi=170);gs=gridspec.GridSpec(2,3,height_ratios=[2.4,1],hspace=.2);ax=fig.add_subplot(gs[0,:]);ox,oy=plot_geometry(ax,N,'B3 actual pin map and schematic signal flow (arrows are associations, not routed copper)')
 edges=[('J2','5','U2','2','COL0 / sense branch'),('U2','1','U5','16','TIA0 via ISO/tap + ADC RC'),('U5','36','U7','13','SPI MISO'),('U3','1','U4','4','VCM'),('U4','3','U1','3','ROW CMD0'),('U1','1','J2','1','ROW0 via1k'),('J1','1','U9','5','5V IN'),('U9','6','U8','1','5V'),('U8','5','U10','5','3V LDO')]
 for a,ap,b,bp,label in edges:
  x1,y1=newpad(a,next(p for p in G[a]['pads'] if p['number']==ap),N[a]);x2,y2=newpad(b,next(p for p in G[b]['pads'] if p['number']==bp),N[b]);ax.annotate('',(x2-ox,y2-oy),(x1-ox,y1-oy),arrowprops={'arrowstyle':'->','color':'#203848','lw':1.1,'alpha':.65});ax.text((x1+x2)/2-ox,(y1+y2)/2-oy,label,fontsize=6,ha='center',bbox={'fc':'white','ec':'none','alpha':.8,'pad':.5})
 for idx,r in enumerate(['U2','U4','U5']):pin_inset(fig.add_subplot(gs[1,idx]),r,N,{'U2':'U2: four output/sense channels + supply','U4':'U4: S/D/SEL interleaved in actual pinout','U5':'U5: analog16-23 / reference5-7 / digital end'}[r],chosen=None if r!='U5' else ['1','2','5','6','7','9','16','18','21','23','30','34','36','37','38'])
 fig.suptitle('B3 REFERENCE-DRIVEN PINOUT FLOORPLAN - OFFLINE / COLLISION HOLD',fontsize=16,y=.97);fig.text(.5,.035,'No physical performance claim. Feedback RF/CF connects TIA tap to COL through external sense/ISO network; only 22p HF loop directly joins opamp pins.',ha='center',fontsize=9);fig.savefig(P/'B3_PINOUT_AND_SIGNAL_FLOW.png',bbox_inches='tight');plt.close(fig)
 print('3/3 final images generated, no more rendering allowed')
