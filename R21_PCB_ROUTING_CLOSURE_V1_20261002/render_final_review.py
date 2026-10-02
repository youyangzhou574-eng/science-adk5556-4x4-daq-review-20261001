exec((__import__('pathlib').Path(__file__).parent/'final_offline_evidence.py').read_text('utf8').split("print(json.dumps(summary))",1)[0])
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PatchPolygon,PathPatch
from matplotlib.path import Path
from shapely.geometry import box
from shapely.affinity import rotate,translate
bf=P/'EXECUTION_BUDGET.json';budget=json.loads(bf.read_text('utf8'));assert budget['actual']['reviewExport']<budget['limits']['reviewExport']
budget['actual']['reviewExport']+=1;budget['reservations'].append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'reviewExport','count':1,'reason':'One delivery-only offline review render batch from actual exported native copper, no additional EDA operation'});bf.write_text(json.dumps(budget,indent=2),'utf8')
def patch_geom(ax,geom,color):
 for poly in(geom.geoms if geom.geom_type=='MultiPolygon'else[geom]):
  verts=[];codes=[]
  for ring in[poly.exterior]+list(poly.interiors):
   c=[(x*.0254,y*.0254)for x,y in ring.coords];verts.extend(c);codes.extend([Path.MOVETO]+[Path.LINETO]*(len(c)-2)+[Path.CLOSEPOLY])
  ax.add_patch(PathPatch(Path(verts,codes),facecolor=color,edgecolor='none',alpha=.28))
def render(name,bounds,layers,label):
 fig,axs=plt.subplots(1,len(layers),figsize=(7*len(layers),8),squeeze=False)
 for ax,layer in zip(axs[0],layers):
  for boundary,g in polys:
   if boundary['layerId']==layer:patch_geom(ax,g,'#609080'if boundary['netName']=='GND'else '#dda66b'if boundary['netName']=='V5'else'#89a0cc')
  for t in lines:
   if t['layerId']==layer:ax.plot([t['startX']*.0254,t['endX']*.0254],[t['startY']*.0254,t['endY']*.0254],color='#cf4646'if layer==1 else'#376cc1',lw=max(.25,t['width']*.08))
  for c in warm['parts']:
   if len(layers)==1:ax.text(c['x']*.0254,c['y']*.0254,c['ref'],fontsize=4,color='#222222')
   for p in c['pads']:
    if p['layer']not in(layer,12):continue
    s=p['pad'];x,y=p['x'],p['y']
    if s[0]=='POLYGON':co=[q for q in s[1]if isinstance(q,(int,float))];g=Polygon(list(zip(co[::2],co[1::2])))
    else:g=translate(rotate(box(-s[1]/2,-s[2]/2,s[1]/2,s[2]/2),p['rotation'],origin=(0,0)),x,y)
    ax.add_patch(PatchPolygon([(x*.0254,y*.0254)for x,y in g.exterior.coords],facecolor='#333333',edgecolor='none'))
  for q in vias:ax.add_patch(plt.Circle((q['centerX']*.0254,q['centerY']*.0254),q['viaDiameter']*.0254/2,fill=False,color='#4b4b4b',lw=.3))
  ax.set_xlim(bounds[:2]);ax.set_ylim(bounds[3],bounds[2]);ax.set_aspect('equal');ax.set_xlabel('mm');ax.set_title('Layer '+str(layer)+' actual native copper');ax.grid(alpha=.1)
 fig.suptitle(label+' | FINAL DRC / COLD AUDIT HOLD | REVIEW ONLY',fontsize=12);fig.tight_layout();fig.savefig(P/name,dpi=220);plt.close(fig)
for layer in(1,15,16,2):render('FINAL_LAYER_'+str(layer)+'.png',(0,100,0,90),[layer],'100 x 90 mm / 4 layers')
render('FINAL_ANALOG_DETAIL.png',(18,65,10,68),(1,2),'Analog routing details; fill arcs sampled <=8 degrees')
render('FINAL_LOGIC_DETAIL.png',(54,84,28,57),(1,2),'MCU / ADC / logic routing')
render('FINAL_POWER_DETAIL.png',(48,91,73,89),(1,2,16),'Power monitor / regulator routing')
print('Seven actual native review PNGs rendered in one batch')
