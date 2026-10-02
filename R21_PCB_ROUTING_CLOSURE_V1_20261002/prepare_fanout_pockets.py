exec((__import__('pathlib').Path(__file__).parent/'filled_geometry.py').read_text('utf8'))
out={'lineChanges':[],'deleteLines':['463292e559fb2d7d','d1a0ab977d0e5681'],'newSegments':[],'newVias':[],'screen':[]}
byId={t['id']:t for t in traces}
traces[:]=[t for t in traces if t['id']not in out['deleteLines']]
def changeLine(id,pts):
 t=byId[id];t['points']=pts;t['geometry']=LineString(pts).buffer(t['width']/2,cap_style=1);out['lineChanges'].append({'id':id,'net':t['net'],'points':pts})
for id in['291d32f22690511d','4f1c4460fb01d2bc','ca9e93b668d2977e']:
 t=byId[id];changeLine(id,[[x,1420 if abs(y-1462.6)<.2 else y]for x,y in t['points']])
def addPath(net,layer,pts,width=6):
 assert clear(pts,net,layer,width),'Manual path clearance '+net+' '+str(pts)
 commit(net,layer,pts,'selected pad','selected landing')
 out['newSegments'] += [{'net':net,'layer':layer,'width':width,'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for a,b in zip(pts,pts[1:])]
def addVia(net,q):
 assert viaFree(*q,net),'Manual landing clearance '+net+' '+str(q)
 addvia(q,net);out['newVias'].append({'net':net,'x':q[0],'y':q[1],'hole':12,'diameter':24})
addVia('ROW_SEL0',(2376,1190));addPath('ROW_SEL0',1,[(2376,1307.1),(2376,1190)]);addPath('ROW_SEL0',2,[(2376,1190),(2316,1217.1)])
addVia('ROW_SEL3',(2400,1453));addPath('ROW_SEL3',1,[(2401.6,1527.6),(2400,1453)])
addVia('U12_CT',(3370,3055));addPath('U12_CT',1,[(3332.1,3070.9),(3353,3070.9),(3370,3055)])
addVia('V5_IN',(815,3280));addPath('V5_IN',1,[(817.5,3189),(815,3280)])
for x in out['lineChanges']:
 t=byId[x['id']];out['screen'].append({'id':x['id'],'net':t['net'],'clear':clear(t['points'],t['net'],t['layer'],t['width'])})
(P/'FANOUT_POCKETS_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
assert all(x['clear']for x in out['screen']),'Do not apply blocked bridge change'
print(json.dumps(out))
