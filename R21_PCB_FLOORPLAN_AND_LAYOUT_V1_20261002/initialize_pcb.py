import pathlib,json,hashlib,datetime,shutil
P=pathlib.Path(__file__).resolve().parent
O=P.parent/'R21_FINAL_INTERFACE_ANNOTATION_AND_BENCH_READINESS_V1'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
auth={'userAuthorization':'允许：按常规矩形4层实验室验证板，尺寸随布局确定，机械要求未定；不采购、不制造、不上电','authorizedUTC':now,'pcbDesign':True,'actualBench':False,'procurement':False,'manufacture':False,'localGitWrites':False,'mechanicalStatus':'LAB_REVIEW_RECTANGLE_NO_CONFIRMED_ENCLOSURE_OR_MOUNTING_HOLES'}
(P/'USER_PCB_AUTHORIZATION.json').write_text(json.dumps(auth,ensure_ascii=False,indent=2),'utf8')
q={'startedUTC':now,'totalMaxMinutes':360,'phasesMinutes':{'mappingRules':60,'floorplan':90,'routing':120,'auditDRC':60,'delivery':30},'counts':{},'prohibited':['schematicElectricalChange','simulation','actualBench','procurement','manufacture','localGitWrites','systemChanges'],'operations':[],'status':'P0_MAPPING','implementationCapsNote':'Pro specified phase time only; actual PCB operation counts will be logged, no invented approved operation quota.'}
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(q,indent=2),'utf8')
files=['SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_WORK.eprj2','SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_REVIEW.epro2','SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_REVIEW.pdf','ENGINEERING_PLAN.json','ENGINEERING_LIBRARY_PARSED.json','FINAL_514_PIN_NET_CHECKS.csv','FINAL_176_BOM.csv','FINAL_107_NETWORK_MEMBERS.csv','FINAL_36_NC.csv']
frozen={f:{'bytes':(O/f).stat().st_size,'sha256':hashlib.sha256((O/f).read_bytes()).hexdigest().upper()}for f in files}
assert frozen[files[1]]['sha256']=='2821A51AFCF9BB474D895B53AE6C514A9B4B637CC3016054356FA7E43F3A97E9'
(P/'FROZEN_INPUT_SHA.json').write_text(json.dumps(frozen,indent=2),'utf8')
work=P/'SCIENCE_ADK5556_4X4_R21_PCB_WORK.eprj2'
assert not work.exists();shutil.copy2(O/files[0],work)
assert work.read_bytes()==(O/files[0]).read_bytes()
q['counts']['workcopy']=1;q['operations'].append({'UTC':now,'kind':'workcopy','path':str(work),'bytes':work.stat().st_size});(P/'EXECUTION_BUDGET.json').write_text(json.dumps(q,indent=2),'utf8')
(P/'IMPLEMENTATION_PLAN.md').write_text('''# R2.1 PCB first review design\n\nUser authorized four-layer lab rectangle; no confirmed enclosure/holes. Accepted schematic fbb7c0ed5f322f078583fadbdb353efe835e4c01 is immutable.\n\n1. Audit 176 component symbols/physical pads and all 514 connected pins / 36 NC from official native PCB import.\n2. Create 4-layer review PCB, J2→ROW/TIA→ADC analog area, references/decoupling local, MCU/SPI opposite side, input/protection separate. Plan practical clearance/width/stackup, no AGND/DGND slit.\n3. Place devices and locally route feedback/decoupling before remaining board connections; retain L2 continuous GND, L3 power/slow digital. No automatic placement.\n4. Actual net/pad/DRC connectivity verification, cold reopen, native review exports and readable layer renders. Report unresolved DRC/unrouted precisely; no manufacture release.\n5. One fresh-context whole-package review, bounded fix pass; full GitHub new directory/fixed commit once plus successor reply monitor.\n\nRuling: use dedicated new PCB workfile, not Git worktree/checkpoint; user forbids local Git writes and schematic baseline changes. Retain all evidence, no cleanup.\nRuling: static helper scripts receive only meaningful structural checks; do not initiate new scientific tests or tool research. Official CLI document use is limited to the needed PCB operations.\n''','utf8')
print(json.dumps({'root':str(P),'workcopyBytes':work.stat().st_size,'sources':len(frozen),'started':now}))
