from floorplan_core import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PatchPoly,Rectangle
reserve('image',2,'Exactlyone P1 andone P2 partial-review drawing; missing actualparts visible, no extra render')
page=json.loads((P/'FINAL_COLD_CAPTURE_ACTUAL_PARTS_AND_NETS.json').read_text(encoding='utf-8'))
colors=['#409a6f','#4f97bd','#27a897','#9573b7','#c97074','#c29443']
col={t['ref']:colors[i]for i,p in enumerate(page['pages'])for t in p['parts']}
summary=json.loads((P/'PARTIAL_PLACEMENT_AUDIT.json').read_text())
def drawpoly(ax,geom,**kwargs):
 for g in list(geom.geoms)if hasattr(geom,'geoms')else[geom]:
  if hasattr(g,'exterior'):ax.add_patch(PatchPoly(list(g.exterior.coords),**kwargs))
for name in ['P1','P2']:
 audit=summary[name];pos=json.loads((P/(name+'_PASS3_PARTIAL.json')).read_text())['positions'];fig=plt.figure(figsize=(15,11),dpi=200);gs=fig.add_gridspec(1,2,width_ratios=[3,1.15],wspace=.14);ax=fig.add_subplot(gs[0]);side=fig.add_subplot(gs[1]);side.axis('off')
 ax.add_patch(Rectangle((0,0),50,50,fc='#f5f4ee',ec='#334a59',lw=2,zorder=0))
 j=pos['J2'][1];ax.add_patch(Rectangle((-8,j-8),16,16,fc='#82b4d8',ec='#427894',alpha=.13,hatch='///',lw=.8,zorder=1));ax.annotate('FFC exits outboard',xy=(-7,j),xytext=(2,j+10),arrowprops={'arrowstyle':'->','color':'#21617b'},fontsize=9,color='#21617b')
 for r,v in pos.items():
  drawpoly(ax,shape(r,v),fc='#d7d9d4',ec='#a8adae',lw=.35,zorder=2)
  drawpoly(ax,body(r,v),fc=col[r],ec='#33484e',lw=.55,zorder=3)
  x,y,a=v;ic=r.startswith('U')and r[1:].isdigit();isj=r.startswith('J')
  ax.text(x,y,r,fontsize=8 if ic or isj else 4.2,ha='center',va='center',color='white'if ic or isj else'#152b33',fontweight='bold'if ic or isj else'normal',zorder=5)
 # Four representative true same-net flight segments: these are NOT copper.
 for i,out in enumerate([1,7,8,14]):
  r='R_ADC'+str(i);n=next(v['number']for v in G[r]['pads']if v['net']=='TIA'+str(i));a=pad('U2',out,pos['U2']);b=pad(r,n,pos[r]);ax.plot([a[0],b[0]],[a[1],b[1]],'--',color='#b4893f',lw=.7,alpha=.6,zorder=4)
 for r,w,h in [('J1',10,6),('J3',6,17),('J4',6,13)]:
  x,y,_=pos[r];ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,fill=False,ec='#774b63',lw=.8,ls='--',zorder=1))
 ax.set_xlim(-9,53);ax.set_ylim(-2,53);ax.set_aspect('equal');ax.set_xlabel('Planning x (mm)');ax.set_ylabel('Planning y (mm)');ax.grid(color='#bfcbd0',lw=.4,alpha=.2);ax.set_xticks(range(0,51,10));ax.set_yticks(range(0,51,10))
 title='Horizontal signal flow'if name=='P1'else'L composition'
 ax.set_title(name+' | '+title+' | PARTIAL '+str(audit['actualPlacedCount'])+'/101\n50 x 50 mm planning rectangle; NOT native PCB / routing',fontsize=14,fontweight='bold',loc='left')
 txt=['C101 electrical baseline accepted','with mandatory addendum / pin map','','PARTIAL VISUAL REVIEW ONLY',str(audit['actualPlacedCount'])+' placed; '+str(len(audit['unplaced']))+' UNPLACED','Body / pad proxy overlap: 0',str(audit['actualPartialPairs']['pairs'])+' partial pairs checked','All5050-pair qualification: HOLD','','UNPLACED actual C101 parts:']+audit['unplaced']+['','None deleted / DNP / moved in CAD.','All101 identities / 363 pin nets frozen.','','J2: 8P / 1mm FFC ZIF placeholder','14x7 body reserve; exact datum HOLD.','Hatched zone: cable / operation reserve.','J1/J3/J4 final connector body unknown.','','Colored body = native shape or J2 reserve.','Gray pads = conservative physical proxy.','Gold dash = representative flight line.','Actual routed lengths / DRC: NOT DONE.','','Source0 / CAD0 / solver0 / bench0','No fourth coordinate pass.']
 side.text(0,1,'\n'.join(txt),va='top',fontsize=9.5,linespacing=1.45,color='#273c47')
 fig.suptitle('C101 OFFLINE FLOORPLAN — incomplete cap neighborhoods, not selectable final placements',fontsize=14,color='#9b533d',y=.98)
 fig.subplots_adjust(top=.92,bottom=.07,left=.06,right=.97);fig.savefig(P/(name+'_PARTIAL_REVIEW.png'));plt.close(fig)
 print(json.dumps({'image':name+'_PARTIAL_REVIEW.png','placed':audit['actualPlacedCount'],'missing':audit['unplaced']}))
