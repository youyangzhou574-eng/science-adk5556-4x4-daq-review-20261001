import json,pathlib,re,math
P=pathlib.Path(__file__).resolve().parent
O=P.parent/'R21_ENGINEERING_R21_NATIVE_AND_LIMITED_VALIDATION_V1'
ctx=json.loads((P/'PROJECT_CONTEXT.json').read_text('utf8'))
base=json.loads((P/'ENGINEERING_PLAN.json').read_text('utf8'))
final=json.loads((P/'FINAL_EXPECTED_PLAN_FROZEN.json').read_text('utf8'))
extras=[q for q in final['parts']if q['ref']not in {x['ref']for x in base['parts']}]
assert len(extras)==8
for q in extras:q['y']=1460 if q['page']==0 else 1780
obs=json.loads((P/'OCCUPANCY_BEFORE.json').read_text('utf8'))['parsed']['value']['pages']
checks=[]
for q in extras:
 pg=obs[0 if q['page']==0 else 1];xmin,xmax=q['x']-180,q['x']+180;ymin,ymax=q['y']-60,q['y']+60
 hits=[]
 for c in pg['parts']:
  for pt in [dict(x=c['x'],y=c['y'])]+c['pins']:
   if xmin<=pt['x']<=xmax and ymin<=pt['y']<=ymax:hits.append(c['id'])
 for w in pg['wires']:
  raw=w['line'];lines=raw if isinstance(raw[0],list)else[raw]
  for line in lines:
   for i in range(0,len(line)-2,2):
    a,b=line[i:i+2];c,d=line[i+2:i+4]
    if max(a,c)>=xmin and min(a,c)<=xmax and max(b,d)>=ymin and min(b,d)<=ymax:hits.append(w['id'])
 # Catch original explicit junctions in source as well.
 for line in pg['source'].splitlines():
  ss=line.split('||')
  if len(ss)<2:continue
  try:hd=json.loads(ss[0]);data=json.loads(ss[1].rstrip('|'))
  except ValueError:continue
  if hd.get('type')in ['JUNCTION','JUNCT','JUNC'] and xmin<=data.get('x',-1e9)<=xmax and ymin<=data.get('y',-1e9)<=ymax:hits.append(hd.get('id'))
 checks.append(dict(ref=q['ref'],box=[xmin,ymin,xmax,ymax],hits=hits,pass_=not hits))
assert all(x['pass_']for x in checks),checks
(P/'PLACEMENT_OCCUPANCY_PASS.json').write_text(json.dumps(checks,indent=2)+'\n','utf8')
template=(O/'native_eco_template.js').read_text('utf8')
template=template[:template.index('// Move net names')]
old="await ports[0].setState_Net(net).done();await stub.wire.setState_Net(net).done();"
new="const rot=ports[0].getState_Rotation();if(!await eda.sch_PrimitiveComponent.delete(ports[0]))throw Error('Delete old feedback port');const rebuilt=await eda.sch_PrimitiveComponent.createNetPort('BI',net,stub.far[0],stub.far[1],rot,false);if(!rebuilt)throw Error('Rebuild feedback port');const a=(await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(rebuilt.getState_PrimitiveId()))[0];if(!close(a.getState_X(),stub.far[0])||!close(a.getState_Y(),stub.far[1]))throw Error('Feedback anchor changed');await stub.wire.setState_Net(net).done();"
assert old in template;template=template.replace(old,new)
tail="\nresult.saved=await eda.sch_Document.save();if(result.saved!==true)throw Error('Save failed');return result;\n"
reset=next(q for q in final['parts']if q['ref']=='R_J3_5')
for idx,label in [(0,'feedback'),(4,'reset'),(2,'tia')]:
 d=dict(project=ctx['project_uuid'],page=ctx['pages'][idx],added=[q for q in extras if q['page']==idx],reset=reset)
 (P/('eco_'+label+'.js')).write_text(template.replace('PLAN',json.dumps(d),1)+tail,'utf8')
b=json.loads(json.dumps(base))
b['parts'].extend([q for q in extras if q['page']==0])
for q in b['parts']:
 if q['ref']=='U3':q['nets'].update({'2':'VCM_FB','6':'VEXC_FB'})
(P/'PLAN_AFTER_B.json').write_text(json.dumps(b,indent=2)+'\n','utf8')
f=json.loads(json.dumps(final))
for q in f['parts']:
 if q['ref']in {x['ref']for x in extras}:q['y']=next(x['y']for x in extras if x['ref']==q['ref'])
(P/'PLAN_FINAL.json').write_text(json.dumps(f,indent=2)+'\n','utf8')
print(json.dumps({'placementBoxesPASS':len(checks),'addedRefs':[x['ref']for x in extras],'Bparts':len(b['parts']),'finalParts':len(f['parts'])}))
