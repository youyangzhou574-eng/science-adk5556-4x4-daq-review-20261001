from pathlib import Path
import json,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,Polygon
P=Path(__file__).parent;b=json.loads((P/'COLD_PCB.json').read_text('utf8'));j=next(c for c in b['parts']if c['ref']=='J2');fig,ax=plt.subplots(figsize=(10,7),dpi=180)
x=j['x']*.0254;y=j['y']*.0254
ax.axvline(0,color='black',lw=2);ax.text(-.25,y,'PCB left edge',rotation=90,va='center',ha='right')
ax.add_patch(Rectangle((x-3.1,y-10.085),6.35,20.17,fill=False,ec='#007b87',lw=2,label='Manufacturer board-header body'))
ax.add_patch(Rectangle((x-3.6,y-10.94),7.37,21.88,fill=False,ec='#667085',ls='--',lw=1.5,label='Project courtyard (design choice)'))
ax.plot([x-2.7,x-2.7],[y-9.8,y+9.8],color='#bd7700',lw=2,label='Friction-lock side / native silk')
for p in j['pads']:
 px,py=p['x']*.0254,p['y']*.0254
 if p['number']=='1':ax.add_patch(Rectangle((px-.85,py-.85),1.7,1.7,ec='#823fbf',fc='#e8d7f4',lw=1.5))
 else:ax.add_patch(Circle((px,py),.85,ec='#823fbf',fc='#e8d7f4',lw=1.5))
 ax.add_patch(Circle((px,py),.57,ec='black',fc='white',lw=.8));ax.text(px+4.4,py,f"PCB {p['number']}  {p['net']}",va='center',fontsize=12);ax.plot([px+1,px+4],[py,py],color='#697586',lw=.8)
ax.add_patch(Polygon([[x+1.65,y-9.55],[x+1.65,y-8.23],[x+.95,y-8.89]],fill=False,ec='#bd7700',lw=1.5));ax.text(12,29,'Square pad + triangle: PCB pin 1\nHousing numbers may not align.\nTrace actual mated contacts.',fontsize=9,va='top')
ax.set_xlim(-1,27);ax.set_ylim(25,54);ax.set_aspect('equal');ax.set_xlabel('PCB x (mm)');ax.set_ylabel('PCB y (mm; native positive y upward)');ax.grid(alpha=.15);ax.legend(loc='upper right',fontsize=9)
ax.set_title('J2: Molex 1718560008 + 22012087 housing\nActual cold-native pad positions; 2D review companion, not 3D/fabrication release',fontsize=12);fig.tight_layout();fig.savefig(P/'J2_PINOUT_AND_BODY.png');plt.close(fig)
# Exact manufacturer/project envelope in current placement and orientation.
r={'coordinateSource':'actual cold native component and8pad coordinates','boardEdgeXmm':0,'headerBodyXrangeMm':[x-3.10,x+3.25],'headerBodyYrangeMm':[y-10.085,y+10.085],'headerMinBoardEdgeMm':x-3.10,'courtyardXrangeMm':[x-3.60,x+3.77],'courtyardYrangeMm':[y-10.94,y+10.94],'courtyardMinEdgeMm':x-3.60,'boardNominalBoundsMm':[0,100,0,90],'bodyAndCourtyardInside':x-3.6>0 and y-10.94>0 and x+3.77<100 and y+10.94<90,'noJ2Movement':True,'enclosureNotProvided':True,'fullMated3DNotQualified':True}
assert r['bodyAndCourtyardInside'];(P/'J2_MECHANICAL_2D_CHECK.json').write_text(json.dumps(r,indent=2),'utf8');print(json.dumps(r))

