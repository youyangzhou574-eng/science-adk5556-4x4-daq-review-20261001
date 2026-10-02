from pathlib import Path
import json,math
p=Path(__file__).parent
oldsource=p.parent/'CIRCUIT_SIMPLIFICATION_C_POWER_AND_SCHEMATIC_CLOSEOUT_V1'/'ACTUAL_SCH_SOURCE'/'cae95ff24beaad15.esch'
dec=json.JSONDecoder();records=[]
for line in oldsource.read_text(encoding='utf-8').splitlines():
 if '||'not in line:continue
 h,rest=line.split('||',1);a=json.loads(h)
 if not rest.startswith('{'):continue
 v,_=dec.raw_decode(rest);records.append((a,v))
chain=json.loads((p/'U12_CHAIN_BASELINE.json').read_text(encoding='utf-8'));points=[(float(z['x']),-float(z['y']))for q in chain for z in q['pins']]
near=lambda a,b:abs(a[0]-b[0])<1e-7 and abs(a[1]-b[1])<1e-7
wires=[];endpoints=[]
for h,v in records:
 if h['type']!='LINE' or not v.get('lineGroup'):continue
 a=(v['startX'],v['startY']);b=(v['endX'],v['endY'])
 if any(near(a,z)for z in points):wires.append(v['lineGroup']);endpoints.append(b)
 elif any(near(b,z)for z in points):wires.append(v['lineGroup']);endpoints.append(a)
assert len(wires)==len(set(wires))==8
ports=[h['id']for h,v in records if h['type']=='COMPONENT'and any(near((v.get('x',1e10),v.get('y',1e10)),z)for z in endpoints)]
assert len(ports)==len(set(ports))==8
ownership={'chainPartIds':[q['id']for q in chain],'wireIds':wires,'netPortIds':ports,'method':'exact two-pin endpoints from frozen previous ownSCH_PAGE; no broad net deletion'}
(p/'U12_OWNED_ENTITY_CLEANUP_PLAN.json').write_text(json.dumps(ownership,indent=2),encoding='utf-8')
common=(p/'final_edit_power.js').read_text(encoding='utf-8').split("await eda.dmt_EditorControl.openDocument('595d5f2f11dee03d');")[0]
plan=json.loads((p/'FINAL_BUILD_PLAN.json').read_text(encoding='utf-8'));q=next(q for q in plan['parts']if q['ref']=='U12_TOP0');q['manufacturer']='YAGEO';q['MPN']='RT0603BRD0716K9L'
script=common+"await eda.dmt_EditorControl.openDocument('cae95ff24beaad15');const ownership=OWN;const all=await eda.sch_PrimitiveComponent.getAll();const ids=new Set(all.map(c=>c.getState_PrimitiveId()));if(ownership.chainPartIds.concat(ownership.netPortIds).some(id=>!ids.has(id)))throw Error('Ownedcomponentidentity');const ws=await eda.sch_PrimitiveWire.getAll();if(ownership.wireIds.some(id=>!ws.some(w=>w.getState_PrimitiveId()===id)))throw Error('Ownedwireidentity');for(const ref of ['U12_TOP0','U12_TOP1','U12_TOP2','U12_TOP3']){const c=await find(ref);if(!ownership.chainPartIds.includes(c.getState_PrimitiveId()))throw Error('Chainrefidentity');}for(const id of ownership.netPortIds){const c=all.find(c=>c.getState_PrimitiveId()===id);const ps=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(id);if(c.getState_ComponentType()==='part'||ps.length!==1)throw Error('Notownedport');}for(const id of ownership.wireIds)if(!await eda.sch_PrimitiveWire.delete(ws.find(w=>w.getState_PrimitiveId()===id)))throw Error('Wiredelete');for(const id of ownership.chainPartIds.concat(ownership.netPortIds))if(!await eda.sch_PrimitiveComponent.delete(all.find(c=>c.getState_PrimitiveId()===id)))throw Error('Componentdelete');const added=await create(NEW,2030,1900);const saved=await eda.sch_Document.save();if(saved!==true)throw Error('save');return{removed:ownership,added,saved};"
script=script.replace('OWN;',json.dumps(ownership)+';').replace('create(NEW,', 'create('+json.dumps(q,ensure_ascii=False)+',')
(p/'final_edit_u12.js').write_text(script,encoding='utf-8');print(json.dumps({'ownedWires8':len(wires),'ownedPorts8':len(ports),'parts4to1':True,'node':q['nets']}))
