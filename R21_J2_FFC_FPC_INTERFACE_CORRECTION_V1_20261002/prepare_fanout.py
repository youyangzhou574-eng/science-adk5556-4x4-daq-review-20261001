from pathlib import Path
import json
P=Path(__file__).parent;pcb=json.loads((P/'BASELINE_PCB.json').read_text('utf8'));rows=[]
for l in pcb['source'].splitlines():
 if '||'in l:
  h,b=l.split('||',1);rows.append((json.loads(h),json.loads(b.rstrip('|'))))
by={h['id']:b for h,b in rows if h['type']=='LINE'}
spec=[('ROW0',2,'d1c3a7d7e2116933','end'),('ROW1',2,'7726ab5223a23e6f','end'),('ROW2',2,'ead83aba11bc71e5','end'),('ROW3',16,'c17fbc7097dc3d91','end'),('COL0',16,'dd68a6ffebd3428c','start'),('COL1',16,'4c8f2eaf08a2a5db','start'),('COL2',16,'380176028e5c4e3a','start')]
changes=[]
for net,layer,id,end in spec:
 b=by[id];x=450.;y=b['startY']+(x-b['startX'])*(b['endY']-b['startY'])/(b['endX']-b['startX']);changes.append({'net':net,'layer':layer,'id':id,'end':end,'x':x,'y':y,'old':b})
plan={'changed':changes,'deleted':['25da72589bb6fbc5','efa67fdd90fc547f','0dc8623cd3c3fe37'],'component':{'xMm':6.5,'yMm':39,'angle':90},'newViaXMil':320,'launchXMil':355,'widthMil':6,'viaHoleMil':12,'viaDiameterMil':24,'localBoundary':{'maxXMil':450,'minYMil':1000,'maxYMil':2100},'newVia':8,'sameNets':['ROW0','ROW1','ROW2','ROW3','COL0','COL1','COL2','COL3']}
(P/'J2_LOCAL_FANOUT_PLAN.json').write_text(json.dumps(plan,indent=2),'utf8')
code="""const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='33bea4d378d43e15e958ffe0eb3058ea5cedff592b3de7cb3eb882844cd142d6')throw Error('Wrong isolatedFFC copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');const plan=PLAN;
const c=(await eda.pcb_PrimitiveComponent.getAll()).find(c=>c.getState_Designator()==='J2');const pins=await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());if(pins.length!==10||Math.abs(c.getState_X()-6.5/.0254)>.001)throw Error('Qualified new J2 placement expected');
for(const ch of plan.changed){const p=await eda.pcb_PrimitiveLine.get(ch.id);if(!p||p.getState_Net()!==ch.net)throw Error('Only declared existing J2 fanout');}
const modified=[];for(const ch of plan.changed){const p=await eda.pcb_PrimitiveLine.modify(ch.id,{[ch.end+'X']:ch.x,[ch.end+'Y']:ch.y});if(!p)throw Error('Scoped trace truncation');modified.push(ch.id);}
if(!await eda.pcb_PrimitiveLine.delete(plan.deleted))throw Error('Only3 obsolete local J2 lead-ins');const vias=[],lines=[];
async function line(net,layer,x1,y1,x2,y2){const p=await eda.pcb_PrimitiveLine.create(net,layer,x1,y1,x2,y2,6,true);if(!p)throw Error('J2 local line');lines.push(p.getState_PrimitiveId());}
for(let i=0;i<8;i++){const n=String(i+1),p=pins.find(p=>String(p.getState_PadNumber())===n),net=plan.sameNets[i],y=39/.0254+(-3.5+i)/.0254,x=6.5/.0254;if(!p||p.getState_Net()!==net)throw Error('Never reorder J2 signals');const v=await eda.pcb_PrimitiveVia.create(net,320,y,12,24,undefined,undefined,null,true);if(!v)throw Error('J2 transitionvia');vias.push({id:v.getState_PrimitiveId(),net,x:320,y});await line(net,1,x,y,320,y);
 if(i<7){const ch=plan.changed[i];await line(net,ch.layer,320,y,355,y);await line(net,ch.layer,355,y,ch.x,ch.y);}else{await line(net,2,320,y,196.9,1885.4);}}
return{modified,deleted:plan.deleted,newVias:vias,newLines:lines,scope:'J2 fanout only; preserved existing lead segment outsidex450mil and all other cores; no mainanalog reroute',explicitSaveCalled:false};
""".replace('PLAN',json.dumps(plan))
(P/'j2_local_fanout.js').write_text(code,'utf8');print(json.dumps({'changes':len(changes),'delete':3,'newvia':8,'newLines':23,'x450':[(c['net'],round(c['y'],3)) for c in changes]}))
