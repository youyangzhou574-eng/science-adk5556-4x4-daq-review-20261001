exec((__import__('pathlib').Path(__file__).parent/'prepare_cap_rotation.py').read_text('utf8').split("out={'rotations'")[0])
from shapely.geometry import Point
viaDiameter=24;hole=12;vias=[];added=[];failures=[]
def clear(pts,net,layer,w=6):
 g=LineString(pts).buffer(w/2+6.2,cap_style=1,join_style=2)
 return not any(g.intersects(p['geometry'])for p in pads if p['layer']in(layer,12)and p['net']!=net) and not any(g.intersects(t['geometry'])for t in traces if t['layer']==layer and t['net']!=net) and not any(g.intersects(q['geometry'])for q in vias if q['net']!=net)
def viaFree(x,y,net):
 g=Point(x,y).buffer(viaDiameter/2+6.2)
 return 20<x<100/.0254-20 and 20<y<90/.0254-20 and not any(g.intersects(p['geometry'])for p in pads if p['net']!=net)and not any(g.intersects(t['geometry'])for t in traces if t['net']!=net)and not any(g.intersects(q['geometry'])for q in vias if q['net']!=net)
def escapes(p):
 if p['layer']==12:return [((p['x'],p['y']),False)]
 x,y=p['x'],p['y'];bounds=p['geometry'].bounds
 points=[(bounds[2]+25,y),(bounds[0]-25,y),(x,bounds[3]+25),(x,bounds[1]-25)]
 for d in(60,90,130):points += [(x+d,y),(x-d,y),(x,y+d),(x,y-d)]
 return [(q,True)for q in points if clear([(x,y),q],p['net'],1)and viaFree(*q,p['net'])]
def recordPath(net,layer,pts,ak,bk):
 pts=[q for k,q in enumerate(pts)if k==0 or q!=pts[k-1]]
 if len(pts)<2:return
 t={'net':net,'layer':layer,'width':6,'points':pts,'from':ak,'to':bk,'geometry':LineString(pts).buffer(3,cap_style=1)};traces.append(t);added.append(t)
keys={p['key']:p for p in pads}
# Engineer-selected connections: output compensation branches, RF/COL short links,
# direct TIA-to-ADC takeoffs, and the existing ordered divider chain. No digital nets here.
pairs=[]
for i in(1,2):pairs += [('COL'+str(i),'RF'+str(i)+'-2','CF'+str(i)+'-2')]
for i in range(4):pairs += [('TIA'+str(i),'R_ADC'+str(i)+'-1','RF'+str(i)+'-1')]
for i in(1,2,3,5,6,7,8):pairs += [('DIV_SEG'+str(i),'RD_B'+str(i)+'-2','RD_B'+str(i+1)+'-1')]
for net,ak,bk in pairs:
 a,b=keys[ak],keys[bk];assert a['net']==b['net']==net
 made=False
 for aq,av in escapes(a):
  for bq,bv in escapes(b):
   for pts in candidates(aq,bq):
    if not clear(pts,net,2):continue
    # Both escapes are checked against existing L1 and all foreign via/pad copper.
    if av:recordPath(net,1,[(a['x'],a['y']),aq],ak,'via');vias.append({'net':net,'x':aq[0],'y':aq[1],'hole':hole,'diameter':viaDiameter,'geometry':Point(*aq).buffer(12)})
    if bv:recordPath(net,1,[(b['x'],b['y']),bq],bk,'via');vias.append({'net':net,'x':bq[0],'y':bq[1],'hole':hole,'diameter':viaDiameter,'geometry':Point(*bq).buffer(12)})
    recordPath(net,2,pts,ak,bk);made=True;break
   if made:break
  if made:break
 if not made:failures.append({'net':net,'from':ak,'to':bk})
out={'scope':'Explicit analog short layer transitions and ADC takeoff pairs','viaDiameterMil':24,'holeMil':12,'paths':[{k:v for k,v in t.items()if k!='geometry'}for t in added],'vias':[{k:v for k,v in q.items()if k!='geometry'}for q in vias],'failures':failures,'segments':[{'net':t['net'],'layer':t['layer'],'width':t['width'],'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in added for a,b in zip(t['points'],t['points'][1:])]}
(P/'P0_TRANSITION_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
code="const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='315433ef1f45b1184319722b4f2939c77ef021639b42a2c9559dabe747dba45a')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');if((await eda.pcb_PrimitiveLine.getAll()).length!==169)throw Error('Unexpected initial routes');const ids=[];\n"
code+='const vs='+json.dumps(out['vias'])+';for(const q of vs){const x=await eda.pcb_PrimitiveVia.create(q.net,q.x,q.y,q.hole,q.diameter);if(!x)throw Error("via create failed");ids.push(x.getState_PrimitiveId());}\n'
code+='const segs='+json.dumps(out['segments'])+';for(const s of segs){const t=await eda.pcb_PrimitiveLine.create(s.net,s.layer,s.x1,s.y1,s.x2,s.y2,s.width,true);if(!t)throw Error("Route failed");ids.push(t.getState_PrimitiveId());}return {created:ids,saved:await eda.pcb_Document.save()};'
(P/'apply_p0_transitions.js').write_text(code,'utf8')
print(json.dumps({'pairs':len(pairs),'completed':len(pairs)-len(failures),'vias':len(vias),'segments':len(out['segments']),'failures':failures}))
