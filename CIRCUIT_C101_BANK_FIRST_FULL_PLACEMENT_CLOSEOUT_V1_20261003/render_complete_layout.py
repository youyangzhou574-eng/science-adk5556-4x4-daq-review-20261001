from floorplan_core import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PatchPoly,Rectangle
a=json.loads((P/'FULL_OFFLINE_AUDIT.json').read_text());g=json.loads((P/'GATES.json').read_text())
assert a['all101Placed']and a['all363ActualPinNetIdentityUnchanged']and a['all5050BodyAndPhysicalProxyNoOverlap']and g['OFFLINE_FULL101_REVIEW_READY']
d=json.loads((P/'P1_FULL_PLACEMENT.json').read_text());ps=d['positions'];assert len(ps)==101
reserve('image',2,'One full101 overview and one analogdetail from same complete P1; no partial candidates/P2')
bankrefs={r for b in d['banks'].values()for tier in b['tiers']for r in tier}
def color(r):
 if r in bankrefs or r=='U5':return '#527dab'
 if r in ['U2','C_TIA_OP']or r.startswith(('RF','CF','R_ADC','C_ADC')):return '#30a48d'
 if r in ['U1','U4','C_MUX','C_ROW_OP','R_SEL_PD0','R_SEL_PD1','R_ENABLE_PD']:return '#4d9b69'
 if r in ['U6','C_REF','C_DIV','C_VCM_OUT','RD_TOP','RD_B1']:return '#946ab0'
 if r in ['U7','C_MCU1','C_MCU_BULK','R_RST','R_CS_PU','R_ADC_RESET_PD']or r.startswith(('R_J','D_DBG')):return '#c99342'
 if r.startswith('J')or r.startswith('D_FFC'):return '#68818e'
 return '#c77775'
def poly(ax,geom,**kw):
 for p in list(geom.geoms)if hasattr(geom,'geoms')else[geom]:
  if hasattr(p,'exterior'):ax.add_patch(PatchPoly(list(p.exterior.coords),**kw))
def layout(ax,labels=4.8):
 ax.add_patch(Rectangle((0,0),50,50,fc='#f7f8f5',ec='#304655',lw=2,zorder=0))
 for owner,rect in d['edgeReserves'].items():
  x0,y0,x1,y1=rect;ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fc='#a5bfce',ec='#5e8499',hatch='///',alpha=.18,lw=.8,zorder=1))
 for r,v in ps.items():
  poly(ax,shape(r,v),fc='#d7dbd7',ec='#a5aeae',lw=.3,zorder=2)
  poly(ax,body(r,v),fc=color(r),ec='#3f555c',lw=.45,zorder=3)
  ic=r in ['U1','U2','U4','U5','U6','U7','U8','U9','U11','U12']or r.startswith('J')
  ax.text(*v[:2],r,fontsize=9 if ic else labels,ha='center',va='center',color='white'if ic else'#162d35',fontweight='bold'if ic else'normal',zorder=5)
 for i,out in enumerate([1,7,8,14]):
  r='R_ADC'+str(i)
  for owner,n in [('U2',out),('U5',[16,18,21,23][i])]:
   rp=next(q['number']for q in G[r]['pads']if q['net']==net(owner,n));p1=pad(r,rp,ps[r]);p2=pad(owner,n,ps[owner]);ax.plot([p1[0],p2[0]],[p1[1],p2[1]],'--',lw=.75,alpha=.8,color=['#874b47','#9a7440','#276997','#7756a0'][i],zorder=4)
 ax.set_aspect('equal');ax.set_xlabel('Planning x (mm)');ax.set_ylabel('Planning y (mm)');ax.grid(color='#bcc8ca',alpha=.15,lw=.4)
fig=plt.figure(figsize=(15,11),dpi=200);gs=fig.add_gridspec(1,2,width_ratios=[3.5,1.15],wspace=.10);ax=fig.add_subplot(gs[0]);side=fig.add_subplot(gs[1]);side.axis('off');layout(ax)
ax.set_xlim(-9,52);ax.set_ylim(-2,52);ax.annotate('FFC exits left / outboard',xy=(-6,29),xytext=(1,46),arrowprops={'arrowstyle':'->','color':'#356a87'},fontsize=10,color='#356a87')
ax.set_title('P1-FULL | 50 x 50 mm | 101 / 101\nBank-first horizontal flow; OFFLINE review candidate',loc='left',fontsize=14,fontweight='bold')
side.text(0,1,'C101 COMPLETE OFFLINE PLACEMENT\n\n101 parts / 363 signal pads\n323 connected / 54 nets / 40 NC\n5050 pairs: body / pad proxy overlap 0\nMinimum proxy gap: 0.204 mm\nAll16 ADC bank capacitors present\n\nFour repeated RF/CF role cells\nADC input caps paired top/bottom\nR_ADC fanout is not exact full mirror\n\nTIA-RADC-ADC two-stub proxy:\nmean 8.776 mm / max10.863 mm\nOld partial P1:11.405 /15.268 mm\nRF3.470 / CF5.664 mm two-stub\nEuclidean proxies, NOT copper\n\nColors:\nGreen: ROW / MUX\nTeal: four TIA / input RC\nBlue: ADC /16 cap banks\nPurple: REF / VCM / VEXC\nRose: power / supervisors\nGold: MCU / debug / UART\n\nHatch: exact checked edge reserve\nGray: conservative physical pad proxy\nDashed lines: true same-net stubs\n\nJ2: FFC14x7 inflated placeholder\nExact actuator / mating: HOLD\nJ1/J3/J4 final mechanics: HOLD\n\nNative PCB / routing / DRC:0\nNo manufacturing or bench release\nUSER VISUAL SELECTION: PENDING',va='top',fontsize=9.8,linespacing=1.4,color='#293f4a')
fig.subplots_adjust(top=.92,left=.06,right=.97,bottom=.07);fig.savefig(P/'P1_FULL_LAYOUT_REVIEW.png');plt.close(fig)
fig,ax=plt.subplots(figsize=(13,11),dpi=200);layout(ax,labels=7.5);ax.set_xlim(11,43);ax.set_ylim(13,36.8);ax.set_title('P1-FULL analog detail | same complete101 candidate\nU5 +16 supply/reference capacitors; U2 RF/CF + four input RC\nConservative physical proxy; no native routing / DRC qualification',fontsize=13,loc='left');fig.subplots_adjust(top=.88,left=.07,right=.97,bottom=.07);fig.savefig(P/'ADC_BANK_AND_TIA_DETAIL.png');plt.close(fig)
b=json.loads((P/'EXECUTION_BUDGET.json').read_text());b.update(coordinateSTOP=True,STOP=True,STOPUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),STOPReason='OFFLINE_COMPLETE_FULL101_TWO_IMAGES_CLOSED_PENDING_VISUAL_AND_NATIVE_SCOPE',phase='COMPLETE_OFFLINE_LAYOUT_READONLY_REVIEW_AND_DELIVERY_ONLY');(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),encoding='utf-8')
print(json.dumps({'images':2,'candidate':'P1','all101':True,'STOP':True}))
