import json,pathlib,sys
P=pathlib.Path(__file__).resolve().parent;label=sys.argv[1];v=json.loads((P/(label+'_PLAN.json')).read_text('utf8'))
base="const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='315433ef1f45b1184319722b4f2939c77ef021639b42a2c9559dabe747dba45a')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');const ids=[];"
batches=[]
for i in range(0,len(v['vias']),50):batches.append(('VIA_'+str(i//50),v['vias'][i:i+50],[]))
for i in range(0,len(v['segments']),90):batches.append(('LINE_'+str(i//90),[],v['segments'][i:i+90]))
for name,vs,ss in batches:
 code=base+'const vs='+json.dumps(vs,separators=(',',':'))+';for(const q of vs){const x=await eda.pcb_PrimitiveVia.create(q.net,q.x,q.y,q.hole,q.diameter);if(!x)throw Error("via");ids.push(x.getState_PrimitiveId());}'
 code+='const ss='+json.dumps(ss,separators=(',',':'))+';for(const s of ss){const t=await eda.pcb_PrimitiveLine.create(s.net,s.layer,s.x1,s.y1,s.x2,s.y2,s.width,true);if(!t)throw Error("route");ids.push(t.getState_PrimitiveId());}return {created:ids};'
 (P/(label+'_'+name+'.js')).write_text(code,'utf8');print(label+'_'+name,len(vs),len(ss))
