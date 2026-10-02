exec((__import__('pathlib').Path(__file__).parent/'current_geometry.py').read_text('utf8'))
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PlotPolygon
for region,bounds in [('LOGIC',(55,76,29,42)),('POWER_MONITOR',(68,89,75,87)),('ANALOG',(18,65,10,68))]:
 fig,axs=plt.subplots(1,3,figsize=(18,8))
 for ax,layer in zip(axs,(1,2,16)):
  for p in pads:
   if p['layer']not in(layer,12):continue
   poly=p['geometry'];coords=[(x*.0254,y*.0254)for x,y in poly.exterior.coords]
   ax.add_patch(PlotPolygon(coords,facecolor='#bbbbbb',edgecolor='#777777',linewidth=.4))
   if bounds[0]<=p['x']*.0254<=bounds[1]and bounds[2]<=p['y']*.0254<=bounds[3]:ax.text(p['x']*.0254,p['y']*.0254,p['key'],fontsize=4)
  for t in traces:
   if t['layer']!=layer:continue
   xy=t['points'];ax.plot([x*.0254 for x,y in xy],[y*.0254 for x,y in xy],lw=max(.5,t['width']*.13))
  for q in vias:ax.add_patch(plt.Circle((q['x']*.0254,q['y']*.0254),.305,fill=False,color='#a00000',lw=.5))
  ax.set_xlim(bounds[0],bounds[1]);ax.set_ylim(bounds[3],bounds[2]);ax.set_aspect('equal');ax.set_title('Layer '+str(layer));ax.grid(True,alpha=.15)
 fig.suptitle('Baseline capture + successfully created routing parameters — review progress, not final native capture')
 fig.tight_layout();fig.savefig(P/('PROGRESS_'+region+'.png'),dpi=190);plt.close(fig)
print('Three region progress views saved')
