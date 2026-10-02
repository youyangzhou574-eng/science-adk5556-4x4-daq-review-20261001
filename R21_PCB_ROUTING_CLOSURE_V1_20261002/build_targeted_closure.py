exec((__import__('pathlib').Path(__file__).parent/'filled_geometry.py').read_text('utf8'))
fan=json.loads((P/'FANOUT_POCKETS_PLAN.json').read_text('utf8'));last=json.loads((P/'FINAL_LANDINGS_PLAN.json').read_text('utf8'));pw=json.loads((P/'TARGETED_POWER_CLOSURE_PLAN.json').read_text('utf8'));dedup=json.loads((P/'NATIVE_CLOSURE_PLAN.json').read_text('utf8'))['deleteExactDuplicateVias']
allv=[q for q in vias if q['id']not in dedup]+fan['newVias']+last['vias']+pw['vias']
closePairs=[]
for i,q in enumerate(allv):
 for r in allv[:i]:
  d=math.hypot(q['x']-r['x'],q['y']-r['y'])
  if d<23.8-1e-5:closePairs.append([q.get('id','new'),r.get('id','new'),q['net'],r['net'],d])
assert not closePairs,closePairs
base="const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='315433ef1f45b1184319722b4f2939c77ef021639b42a2c9559dabe747dba45a')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');const ids=[];"
changes=fan['lineChanges']+pw['bridgeChanges']
code=base+'const ds='+json.dumps(dedup)+';for(const id of ds){if(!await eda.pcb_PrimitiveVia.delete(id))throw Error("dedup:"+id);}const dl='+json.dumps(fan['deleteLines'])+';for(const id of dl){if(!await eda.pcb_PrimitiveLine.delete(id))throw Error("line delete:"+id);}'
code+='const mods='+json.dumps(changes,separators=(',',':'))+';for(const m of mods){const t=await eda.pcb_PrimitiveLine.modify(m.id,{startX:m.points[0][0],startY:m.points[0][1],endX:m.points[1][0],endY:m.points[1][1]});if(!t)throw Error("local change");}'
code+="if(!await eda.pcb_PrimitivePour.modify('63f24421d5efdd71',{pourPriority:1}))throw Error('V5 order');if(!await eda.pcb_PrimitivePour.modify('5ec0f147a74d7106',{pourPriority:0}))throw Error('V3 order');return {deletedDuplicateVias:ds.length,deletedLines:dl.length,localChanges:mods.length,fillPending:true};"
(P/'apply_targeted_modifications.js').write_text(code,'utf8')
vs=fan['newVias']+last['vias']+pw['vias'];ss=fan['newSegments']+last['segments']+pw['segments']
traces[:]=[t for t in traces if t.get('id')not in set(fan['deleteLines'])|{m['id']for m in changes}]
for m in changes:traces.append(dict(m,layer=1,width=6,geometry=LineString(m['points']).buffer(3)))
for q in vs:vias.append(dict(q,geometry=Point(q['x'],q['y']).buffer(q['diameter']/2)))
for s in ss:traces.append(dict(s,points=[(s['x1'],s['y1']),(s['x2'],s['y2'])],geometry=LineString([(s['x1'],s['y1']),(s['x2'],s['y2'])]).buffer(s['width']/2)))
# Widen new local supply copper where the actual foreign geometry permits it.
widths=[]
for s in ss:
 if s['net']in('V5_IN','V5','V3V3','GND'):
  for w in(20,12):
   if clear([(s['x1'],s['y1']),(s['x2'],s['y2'])],s['net'],s['layer'],w):
    s['width']=w
    for t in traces:
     if t.get('x1')==s['x1']and t.get('y1')==s['y1']and t.get('x2')==s['x2']and t.get('y2')==s['y2']and t['net']==s['net']and t['layer']==s['layer']:t['geometry']=LineString(t['points']).buffer(w/2);t['width']=w
    break
 widths.append([s['net'],s['width']])
chunks=[('VIAS',vs,[])]+[('LINES_'+str(i//40),[],ss[i:i+40])for i in range(0,len(ss),40)]
for label,vq,sq in chunks:
 c=base+'const vs='+json.dumps(vq,separators=(',',':'))+';for(const q of vs){const t=await eda.pcb_PrimitiveVia.create(q.net,q.x,q.y,q.hole,q.diameter);if(!t)throw Error("via");ids.push(t.getState_PrimitiveId());}'
 c+='const ss='+json.dumps(sq,separators=(',',':'))+';for(const s of ss){const t=await eda.pcb_PrimitiveLine.create(s.net,s.layer,s.x1,s.y1,s.x2,s.y2,s.width,true);if(!t)throw Error("line");ids.push(t.getState_PrimitiveId());}return {created:ids};'
 (P/('targeted_'+label+'.js')).write_text(c,'utf8')
c=base+"const full=eda.pcb_MathPolygon.createPolygon([20,20,'L',100/.0254-20,20,100/.0254-20,90/.0254-20,20,90/.0254-20,20,20]);const q=await eda.pcb_PrimitivePour.create('GND',1,full,undefined,false,'L1_GND_GUARD_RETURN_REVIEW',0,8,true);if(!q)throw Error('Top ground');return {pour:q.getState_PrimitiveId(),fillPending:true,saved:await eda.pcb_Document.save()};"
(P/'save_targeted_closure.js').write_text(c,'utf8')
(P/'TARGETED_CLOSURE_COMBINED_PLAN.json').write_text(json.dumps({'deletedDuplicateVias':dedup,'lineChanges':changes,'vias':vs,'segments':ss,'topGroundGuard':True,'sameHoleDistanceCheck':'PASS'},indent=2),'utf8')
print(json.dumps({'vias':len(vs),'segments':len(ss),'widthCounts':dict(collections.Counter(w for n,w in widths)),'scripts':[x[0]for x in chunks]}))
