from pathlib import Path
import json,re
p=Path(__file__).parent;plan=json.loads((p/'C_NATIVE_BUILD_PLAN.json').read_text(encoding='utf-8'))
def category(q):
 if re.fullmatch(r'U\d+',q['ref']):return 'IC'
 if q['ref'].startswith('J'):return 'connector'
 if q['ref'].startswith('D'):return 'protection'
 if any(x in q['value'] for x in ['uF','nF','pF']):return 'capacitor'
 return 'resistor'
plan['counts']={c:sum(category(q)==c and not q['dnp']for q in plan['parts'])for c in ['IC','connector','protection','capacitor','resistor']}
(p/'C_NATIVE_BUILD_PLAN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
template=r'''
const plan=PLAN; const result={page:plan.page,status:'STARTED',parts:[],deleted:{},saved:false};
try{
 const project=await eda.dmt_Project.getCurrentProjectInfo();if(project.uuid!==plan.project)throw Error('Wrong isolated C project');
 await eda.dmt_EditorControl.openDocument(plan.page.uuid);
 // Current working-copy page only; no PCB document and no old source session.
 const keep=new Set(plan.parts.filter(q=>q.ref==='J2').map(q=>q.ref));
 const all=await eda.sch_PrimitiveComponent.getAll();
 for(const c of all){if(c.getState_ComponentType()==='sheet'||keep.has(c.getState_Designator()))continue;if(!await eda.sch_PrimitiveComponent.delete(c))throw Error('Component delete failed');result.deleted.component=(result.deleted.component||0)+1;}
 for(const w of await eda.sch_PrimitiveWire.getAll()){if(!await eda.sch_PrimitiveWire.delete(w))throw Error('Wire delete failed');result.deleted.wire=(result.deleted.wire||0)+1;}
 for(const t of await eda.sch_PrimitiveText.getAll()){if(!await eda.sch_PrimitiveText.delete(t))throw Error('Text delete failed');result.deleted.text=(result.deleted.text||0)+1;}
 for(const c of await eda.sch_PrimitiveComponent.getAll())if(c.getState_ComponentType()==='sheet'){
  const border=(await eda.sch_PrimitiveAttribute.getAll(c.getState_PrimitiveId())).find(a=>a.getState_Key()==='Border');if(border)await eda.sch_PrimitiveAttribute.modify(border.getState_PrimitiveId(),{value:'0'});
 }
 await eda.sch_PrimitiveText.create(80,30,'C CANDIDATE - NOT FOR USE - '+plan.page.name+' / electrical and material HOLD');
 for(let i=0;i<plan.parts.length;i++){
  const q=plan.parts[i];let c;
  if(q.ref==='J2'){c=(await eda.sch_PrimitiveComponent.getAll()).find(v=>v.getState_Designator()==='J2');if(!c)throw Error('Inherited J2 missing');}
  else{c=await eda.sch_PrimitiveComponent.create(q.association,350+(i%4)*560,220+Math.floor(i/4)*420,q.sub,0,false,true,true);if(!c)throw Error('Create '+q.ref);}
  const m=await eda.sch_PrimitiveComponent.modify(c.getState_PrimitiveId(),{designator:q.ref,name:q.value,otherProperty:{...c.getState_OtherProperty(),Value:q.value,'Review Status':'C CANDIDATE / NOT FOR USE / POWER_AND_DYNAMIC_HOLD','Add into BOM':q.dnp?'no':'yes','DNP':q.dnp?'yes':'no','Circuit Role':q.role||'C candidate; no PCB/bench release'}});if(!m)throw Error('Metadata '+q.ref);
  const ps=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(m.getState_PrimitiveId());
  const actual=ps.map(v=>({number:String(v.getState_PinNumber()),name:v.getState_PinName(),x:v.getState_X(),y:v.getState_Y(),rotation:v.getState_Rotation()}));
  if(actual.length!==Object.keys(q.nets).length||new Set(actual.map(x=>x.number)).size!==actual.length||actual.some(x=>!(x.number in q.nets)))throw Error('Actual pin set mismatch '+q.ref+' '+JSON.stringify(actual));
  for(let z=0;z<ps.length;z++){
   const a=actual[z],net=q.nets[a.number];
   if(net===null){await ps[z].setState_NoConnected(true).done();continue;}
   await ps[z].setState_NoConnected(false).done();
   const length=q.ref.match(/^U\d+$/)?120:65;const delta={0:[length,0],180:[-length,0],90:[0,length],270:[0,-length]}[a.rotation];if(!delta)throw Error('Unknown pin rotation');
   const port=await eda.sch_PrimitiveComponent.createNetPort('BI',net,a.x+delta[0],a.y+delta[1],a.rotation,false);if(!port)throw Error('Port '+q.ref);
   const pp=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(port.getState_PrimitiveId());if(pp.length!==1)throw Error('Port anchor');
   const w=await eda.sch_PrimitiveWire.create([[a.x,a.y,pp[0].getState_X(),pp[0].getState_Y()]],net);if(!w)throw Error('Wire '+q.ref);
   for(const attr of await eda.sch_PrimitiveAttribute.getAll(w.getState_PrimitiveId()))if(['NET','Net'].includes(attr.getState_Key()))await eda.sch_PrimitiveAttribute.modify(attr.getState_PrimitiveId(),{valueVisible:false,keyVisible:false});
  }
  result.parts.push({ref:q.ref,id:m.getState_PrimitiveId(),actualPins:actual,planned:q.nets,association:m.getState_Component(),footprint:m.getState_Footprint(),dnp:q.dnp});
 }
 if(plan.save){result.saved=await eda.sch_Document.save();if(result.saved!==true)throw Error('Save failed');}
 result.status='PAGE_CANDIDATE_CREATED';return result;
}catch(e){result.status='STOP_NATIVE_IMPLEMENTATION_ERROR';result.error={name:e.name,message:e.message,stack:e.stack};return result;}
'''
for page in plan['pages']:
 q={'project':plan['project'],'page':page,'parts':[x for x in plan['parts']if x['page']==page['index']],'save':page['index']in[2,5]}
 (p/('build_c_page'+str(page['index'])+'.js')).write_text(template.replace('PLAN',json.dumps(q,ensure_ascii=False),1),encoding='utf-8')
ledger=p/'PLAN_AND_LEDGER.md';s=ledger.read_text(encoding='utf-8');s+='''
Ruling: Independent V5-supervisor output PWR5_OK controls LDO EN, pulled up100k toV5; U11 VDD/MR moved toV5. Reuse the unused isolated upper Schottky branch in the fourth BAT54XY to propagate power-bad into3.3V NRST without a5V MCU pullup. This is a concrete engineering amendment to the literal common wired-AND suggestion; same logical power qualification, no added IC. Not yet approved/qualified; fast input-loss sequence and diode/reset limits remain HOLD. Cost if wrong: revise only power/control page; do not energize.
Ruling: Qualified18k/162k devices preserveVEX ratio while raising dividerThevenin9k→16.2k; no performance claim. Cost if wrong: restore10k/90k when sourced, recheckstartup.
Ruling: Single17k0.1% exactdevice not found; preserve old16.99k chain and disclose until actualmatchingMPN. Cost if wrong: extra3 R and0.037%threshold difference, no silent5%replacement.
Ruling: Retain all double ADC/referencebulkcapacitors untilCeffclosed; projected103populated/115structural is honestcount, notforced90. DNP12isolatedreferenceparts are NOT aqualifiedswitchablecompensationnetwork; future routing restoration needs explicitECO. Cost if wrong: further design review, noPCBrelease.
Ruling: C125795 TPD template has missingmanufacturerfield; useonlyelectricalcandidatepinplan with materialconformanceHOLD, never verifiedTIstock. Cost ifwrong: replace/supplyqualifiedtemplate before release.
''';ledger.write_text(s,encoding='utf-8')
print(json.dumps({'counts':plan['counts'],'populatedCandidate':plan['populatedCount'],'structural':plan['structuralCount'],'sixPreparedPages':True}))
