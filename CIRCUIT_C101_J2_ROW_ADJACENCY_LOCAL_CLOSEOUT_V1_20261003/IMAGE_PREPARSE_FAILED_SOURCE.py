from floorplan_core import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PatchPoly,Rectangle
d=json.loads((P/'LOCAL_FINAL_FULL101_PLACEMENT.json').read_text());ps=d['positions'];a=json.loads((P/'FULL_LOCAL_AUDIT.json').read_text());g=json.loads((P/'GATES.json').read_text())
assert len(ps)==101 and a['all8RowPathsNonIncreasing']and a['all4ImbalanceReduced']and g['ALL_MACRO_LAYOUT_INTENTS_ACCEPTED']
reserve('image',1,'Sole full101 image after one successful localROWmove/fullgeometry; no detail/partial redraw')
bankrefs={r for v in d['banks'].values()for tier in v['tiers']for r in tier}
def color(r):
 if r in bankrefs or r=='U5':return '#527dab'
 if r in ['U2','C_TIA_OP']or r.startswith(('RF','CF','R_ADC','C_ADC')):return '#30a48d'
 if r in ['U1','U4','C_MUX','C_ROW_OP','R_SEL_PD0','R_SEL_PD1','R_ENABLE_PD']:return '#4d9b69'
 if r in ['U6','C_REF','C_DIV','C_VCM_OUT','RD_TOP','RD_B1']:return '#946ab0'
 if r in ['U7','C_MCU1','C_MCU_BULK','R_RST','R_CS_PU','R_ADC_RESET_PD']or r.startswith(('R_J','D_DBG')):return '#c99342'
 if r.startswith('J')or r.startswith('D_FFC'):return '#68818e'
 return '#c77775'
def poly(ax,geom,**kw):
 for pp in list(geom.geoms)if hasattr(geom,'geoms')else[geom]:
  if hasattr(pp,'exterior'):ax.add_patch(PatchPoly(list(pp.exterior.coords),**kw))
fig=plt.figure(figsize=(15,11),dpi=200);gs=fig.add_gridspec(1,2,width_ratios=[3.5,1.15],wspace=.10);ax=fig.add_subplot(gs[0]);side=fig.add_subplot(gs[1]);side.axis('off')
ax.add_patch(Rectangle((0,0),50,50,fc='#f7f8f5',ec='#304655',lw=2,zorder=0))
for owner,rect in d['edgeReserves'].items():
 x0,y0,x1,y1=rect;ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fc='#a5bfce',ec='#5e8499',hatch='///',alpha=.18,lw=.8,zorder=1))
for r,v in ps.items():
 poly(ax,shape(r,v),fc='#d7dbd7',ec='#a5aeae',lw=.3,zorder=2);poly(ax,body(r,v),fc=color(r),ec='#3f555c',lw=.45,zorder=3)
 ic=r in ['U1','U2','U4','U5','U6','U7','U8','U9','U11','U12']or r.startswith('J')
 ax.text(*v[:2],r,fontsize=9 if ic else4.8,ha='center',va='center',color='white'if ic else'#162d35',fontweight='bold'if ic else'normal',zorder=6,clip_on=True)
for n in range(1,9):
 x,y=pad('J2',n,ps['J2']);ax.plot(x,y,'o',ms=2,color='#d8efca'if n<=4 else'#d4e6ff',zorder=7)
ax.text(1.25,31,'COL 5-8',rotation=90,fontsize=7,color='white',ha='center',va='center',zorder=6)
ax.text(1.25,27,'ROW 1-4',rotation=90,fontsize=7,color='white',ha='center',va='center',zorder=6)
for i,n in enumerate([4,5,6,7]):
 j=pad('J2',i+1,ps['J2']);v=pad('U4',n,ps['U4']);ax.plot([j[0],v[0]],[j[1],v[1]],'--',lw=.65,alpha=.65,color='#57874d',zorder=4)
for up,mp in [(1,8),(4,9)]:
 j=pad('U1',up,ps['U1']);v=pad('U4',mp,ps['U4']);ax.plot([j[0],v[0]],[j[1],v[1]],'--',lw=.8,color='#43733f',zorder=4)
ax.set_xlim(-9,52);ax.set_ylim(-2,52);ax.set_aspect('equal');ax.set_xlabel('Planning x (mm)');ax.set_ylabel('Planning y (mm)');ax.grid(color='#bcc8ca',alpha=.15,lw=.4)
ax.annotate('FFC exits left / outboard',xy=(-6,29),xytext=(1,46),arrowprops={'arrowstyle':'->','color':'#356a87'},fontsize=10,color='#356a87')
ax.set_title('P1-ROW-LOCAL | 50 x 50 mm | 101 / 101\nOne local ROW adjacency correction; OFFLINE review',loc='left',fontsize=14,fontweight='bold')
txt='C101 COMPLETE OFFLINE CANDIDATE\n\nOne purposeful local change\n7 ROW parts +3 allowed VEX parts\n91 other parts exactly frozen\n\n101 parts /363 signal pins\n323 connected /54 nets /40 NC\n5050 body/pad-proxy pairs: overlap0\nMinimum proxy gap:0.2024 mm\n\nJ2 direction/pin1-8 unchanged\nROW planned lower / COL upper\nU4 moved toROWside, rotated90deg\nU1 stays compact aboveU4\nAll8 ROW paths shorter\nDrive10.109..10.724 mm\nSense6.044..7.024 mm\nFour imbalance values reduced\nROW_DRV6.724 ->2.884 mm\nROW_FB4.649 ->4.597 mm\nAll distances: proxies, NOT copper\n\nADC/TIA/RF/CF/16-bank unchanged\nTIA-ADC inherited8.776/10.863 mm\n\nExact checked reserve: hatched\nSmallest reserve margin0.0073mm\nPlanning only, not finalmechanics\nJ2 exactactuator/mating: HOLD\nJ1/J3/J4 finalmechanics: HOLD\n\nNativeCAD/routing/DRC:0\nPerformance/bench/manufacture:HOLD\nVisual selection:PENDING'
side.text(0,1,txt,va='top',fontsize=9.8,linespacing=1.4,color='#293f4a')
fig.subplots_adjust(top=.92,left=.06,right=.97,bottom=.07);fig.savefig(P/'P1_ROW_LOCAL_FULL101_REVIEW.png');plt.close(fig)
b=json.loads((P/'EXECUTION_BUDGET.json').read_text());b.update(STOP=True,coordinateSTOP=True,STOPUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),STOPReason='ONE_LOCAL_PLACEMENT_AND_ONE_IMAGE_COMPLETE_PENDING_REVIEW_AND_UNIFIED_NATIVE_SCOPE',phase='READONLY_FINAL_REVIEW_AND_DELIVERY_ONLY');(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),encoding='utf-8')
print(json.dumps({'image':1,'STOP':True,'CAD':0}))
