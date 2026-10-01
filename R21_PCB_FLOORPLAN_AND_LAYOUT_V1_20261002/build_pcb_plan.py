import pathlib,json,csv,collections
P=pathlib.Path(__file__).resolve().parent;O=P.parent/'R21_FINAL_INTERFACE_ANNOTATION_AND_BENCH_READINESS_V1'
lib=json.loads((O/'ENGINEERING_LIBRARY_PARSED.json').read_text('utf8'))
rows=list(csv.DictReader((O/'FINAL_176_BOM.csv').open(encoding='utf-8-sig')))
nets=collections.defaultdict(dict)
for r in csv.DictReader((O/'FINAL_514_PIN_NET_CHECKS.csv').open(encoding='utf-8-sig')):
 ref,pin=r['pin'].rsplit('-',1);assert r['pass_']=='True';nets[ref][pin]=r['actual']
nc=collections.defaultdict(set)
for r in csv.DictReader((O/'FINAL_36_NC.csv').open(encoding='utf-8-sig')):nc[r['ref']].add(r['pin'])
parts=[];audit=[]
for i,r in enumerate(rows):
 d=lib[r['actual_device']]['device'];pads=lib[r['actual_device']]['pads'];nums={p['body']['num']for p in pads}
 expected=set(nets[r['ref']])|nc[r['ref']]
 missing=sorted(expected-nums);extras=sorted(nums-expected)
 audit.append({'ref':r['ref'],'device':r['actual_device'],'schematicPins':len(expected),'libraryPadNumbers':len(nums),'missing':missing,'extras':extras,'padCount':len(pads)})
 parts.append({'ref':r['ref'],'device':r['actual_device'],'deviceItem':d,'footprint':r['footprint'],'value':r['Value'],'nets':nets[r['ref']],'nc':sorted(nc[r['ref']]),'initialX':400+(i%16)*250,'initialY':400+(i//16)*220})
result={'parts':176,'connected':sum(len(x['nets'])for x in parts),'nc':sum(len(x['nc'])for x in parts),'pass':all(not x['missing'] and not x['extras']for x in audit),'audit':audit,'note':'Library pad-number coverage prerequisite; actual native pads and manufacturer mapping still require audit. No footprint substitution.'}
(P/'LIBRARY_PAD_COVERAGE.json').write_text(json.dumps(result,indent=2),'utf8');(P/'PCB_COMPONENT_PLAN.json').write_text(json.dumps(parts,ensure_ascii=False,indent=2),'utf8')
print(json.dumps({k:v for k,v in result.items()if k!='audit'}));print(json.dumps([a for a in audit if a['missing']or a['extras']]))
if not result['pass']:raise SystemExit('STOP library pad mismatch')
for k in range(0,len(parts),20):
 batch=[dict(x,deviceItem={'libraryUuid':x['deviceItem']['libraryUuid'],'uuid':x['deviceItem']['uuid']}) for x in parts[k:k+20]if x['ref']!='J1']
 code='const plan='+json.dumps(batch,separators=(',',':'))+';\n'
 code+='''const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=="e58f223d256cd14d13a6fb04a0e150585301864f01c50827f9241f5945cf2801")throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');
const refs=new Set((await eda.pcb_PrimitiveComponent.getAll()).map(c=>c.getState_Designator()));for(const p of plan)if(refs.has(p.ref))throw Error('Duplicate '+p.ref);
const out=[];for(const p of plan){const c=await eda.pcb_PrimitiveComponent.create(p.deviceItem,1,p.initialX,p.initialY,0,false);if(!c)throw Error('Create '+p.ref);
await eda.pcb_PrimitiveComponent.modify(c,{designator:p.ref,name:p.value||p.device});
const pads=await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());const actual=new Set(pads.map(v=>String(v.getState_PadNumber())));const expected=new Set([...Object.keys(p.nets),...p.nc]);if(actual.size!==expected.size||[...expected].some(n=>!actual.has(n)))throw Error('Actual pads '+p.ref);
for(const pad of pads){const n=String(pad.getState_PadNumber());await pad.setState_Net(p.nets[n]||'').done();}
out.push({ref:p.ref,id:c.getState_PrimitiveId(),pads:(await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId())).map(v=>({n:String(v.getState_PadNumber()),net:v.getState_Net()}))});}
return {out,saved:await eda.pcb_Document.save(),actualPartCount:(await eda.pcb_PrimitiveComponent.getAll()).length};'''
 (P/f'create_batch_{k//20:02}.js').write_text(code,'utf8')
