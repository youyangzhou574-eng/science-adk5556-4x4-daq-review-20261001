exec((__import__('pathlib').Path(__file__).parent/'filled_geometry.py').read_text('utf8'))
out={'lineChanges':[],'viaChanges':[],'deleteLines':[],'newSegments':[],'screen':[]}
byId={t['id']:t for t in traces};viaId={q['id']:q for q in vias}
def changeLine(id,pts):
 t=byId[id];t['points']=pts;t['geometry']=LineString(pts).buffer(t['width']/2,cap_style=1);out['lineChanges'].append({'id':id,'net':t['net'],'points':pts})
def moveVia(id,q):
 old=viaId[id];oldp=[old['x'],old['y']];old.update(x=q[0],y=q[1],geometry=Point(*q).buffer(old['diameter']/2));out['viaChanges'].append({'id':id,'net':old['net'],'old':oldp,'new':q})
 for t in traces:
  if t['net']!=old['net']:continue
  pts=[[q[0],q[1]]if math.dist(p,oldp)<.11 else p for p in t['points']]
  if pts!=t['points']:changeLine(t['id'],pts)
# Free top U14 pin2: straighten the adjacent pin3 escape outward, preserving its destination copper.
rowvia=next(q for q in vias if q['net']=='ROW_SEL0'and abs(q['x']-2316)<.2 and abs(q['y']-1217.1)<.2)
moveVia(rowvia['id'],[2376,1190])
out['deleteLines']=['463292e559fb2d7d','d1a0ab977d0e5681']
traces[:]=[t for t in traces if t['id']not in out['deleteLines']]
out['newSegments'].append({'net':'ROW_SEL0','layer':1,'width':6,'x1':2376,'y1':1307.1,'x2':2376,'y2':1190})
traces.append({'net':'ROW_SEL0','layer':1,'width':6,'points':[[2376,1307.1],[2376,1190]],'geometry':LineString([[2376,1307.1],[2376,1190]]).buffer(3,cap_style=1)})
# Give bottom pin11 a landing pocket by taking the existing HW_ENABLE bridge farther outside the row.
for id in['4486d20a494639ec','6fe5f1528d40c139','31958de6a9a71fcc']:
 t=byId[id];changeLine(id,[[x,1645 if abs(y-1592.6)<.2 else y]for x,y in t['points']])
# Move the U12 PGOOD landing laterally, away from CT pin5. All copper terminating there follows it.
pg=next(q for q in vias if q['net']=='PGOOD'and abs(q['x']-3371.85)<.2 and abs(q['y']-3090.6)<.2)
moveVia(pg['id'],[3471.85,3090.6])
for x in out['lineChanges']:
 t=byId[x['id']];out['screen'].append({'line':x['id'],'net':t['net'],'clear':clear(t['points'],t['net'],t['layer'],t['width'])})
for x in out['viaChanges']:out['screen'].append({'via':x['id'],'net':x['net'],'clear':viaFree(*x['new'],x['net'])})
(P/'FANOUT_REPAIR_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
print(json.dumps(out))
