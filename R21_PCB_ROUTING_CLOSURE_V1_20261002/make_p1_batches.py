import pathlib,json
P=pathlib.Path(__file__).resolve().parent;v=json.loads((P/'P1_SIGNAL_ROUTE_PLAN.json').read_text('utf8'))
base="const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='315433ef1f45b1184319722b4f2939c77ef021639b42a2c9559dabe747dba45a')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');const ids=[];"
batches=[('VIA_0',v['vias'][:50],[],False),('VIA_1',v['vias'][50:],[],False)]
for i in range(0,len(v['segments']),90):batches.append(('LINE_'+str(i//90),[],v['segments'][i:i+90],i+90>=len(v['segments'])))
for label,vs,ss,save in batches:
 code=base
 code+='const vs='+json.dumps(vs,separators=(',',':'))+';for(const q of vs){const x=await eda.pcb_PrimitiveVia.create(q.net,q.x,q.y,q.hole,q.diameter);if(!x)throw Error("via");ids.push(x.getState_PrimitiveId());}'
 code+='const ss='+json.dumps(ss,separators=(',',':'))+';for(const s of ss){const t=await eda.pcb_PrimitiveLine.create(s.net,s.layer,s.x1,s.y1,s.x2,s.y2,s.width,true);if(!t)throw Error("route");ids.push(t.getState_PrimitiveId());}'
 code+='return {created:ids'+(',saved:await eda.pcb_Document.save()'if save else '')+'};'
 (P/('p1_'+label+'.js')).write_text(code,'utf8')
 print(label,len(code),len(vs),len(ss),save)
(P/'P1_PRELAUNCH_FAILURE.json').write_text(json.dumps({'failedBeforeNativeLaunch':True,'error':'Windows CreateProcess WinError 206: inline command too long','nativeMutations':0,'savePredebitRetained':True,'resolution':'Same approved geometry split into small native calls; no API changes/research.'},indent=2),'utf8')
