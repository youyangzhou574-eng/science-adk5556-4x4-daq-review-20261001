import pathlib,json,collections
P=pathlib.Path(__file__).resolve().parent;O=P.parent/'R21_FINAL_INTERFACE_ANNOTATION_AND_BENCH_READINESS_V1'
props=collections.defaultdict(dict)
for i in range(1,7):
 for ln in (O/f'FINAL_PAGE_{i}_SOURCE.txt').read_text('utf8').splitlines():
  bits=ln.split('||')
  if len(bits)!=2:continue
  h=json.loads(bits[0]);b=json.loads(bits[1].rstrip('|'))
  if h['type']=='ATTR':props[b['parentId']][b['key']]=b.get('value')
links=[]
for p in props.values():
 if 'Designator'in p and 'Unique ID'in p:links.append({'ref':p['Designator'],'uniqueId':p['Unique ID']})
plan=json.loads((P/'PCB_COMPONENT_PLAN.json').read_text('utf8'));refs={x['ref']for x in plan};links=[p for p in links if p['ref']in refs]
assert len(links)==176 and len({p['ref']for p in links})==176
assert all(p['uniqueId']for p in links) and len({p['uniqueId']for p in links})==176
(P/'SCHEMATIC_PCB_LINKAGE_PLAN.json').write_text(json.dumps(links,indent=2),'utf8')
code='const links='+json.dumps(links,separators=(',',':'))+';\n'
code+='''const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=="e58f223d256cd14d13a6fb04a0e150585301864f01c50827f9241f5945cf2801")throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');const all=await eda.pcb_PrimitiveComponent.getAll(),refs=new Map(all.map(c=>[c.getState_Designator(),c]));for(const p of links){const c=refs.get(p.ref);if(!c)throw Error(p.ref);await eda.pcb_PrimitiveComponent.modify(c,{uniqueId:p.uniqueId});}const check=(await eda.pcb_PrimitiveComponent.getAll()).map(c=>({ref:c.getState_Designator(),uniqueId:c.getState_UniqueId()}));return {check,saved:await eda.pcb_Document.save()};'''
(P/'link_schematic.js').write_text(code,'utf8');print(json.dumps({'uniqueRefs':len(links),'uniqueIds':len({p['uniqueId']for p in links})}))
