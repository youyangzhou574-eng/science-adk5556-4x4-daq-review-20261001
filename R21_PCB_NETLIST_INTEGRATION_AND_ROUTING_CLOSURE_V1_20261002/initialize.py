from pathlib import Path
import json, datetime, shutil, hashlib
P=Path(__file__).resolve().parent
O=P.parent/'R21_PCB_FLOORPLAN_AND_LAYOUT_V1'
D=P.parent/'GITHUB_PCB_FLOORPLAN_DELIVERY_20261002'
def put(n,v): (P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf8')
assert not (P/'EXECUTION_BUDGET.json').exists()
shutil.copyfile(D/'PRO_PCB_ROUTING_CLOSURE_RULING_FULL.md',P/'PRO_ROUTING_CLOSURE_RULING_FULL.md')
names=['SCIENCE_ADK5556_4X4_R21_PCB_WORK.eprj2','SCIENCE_ADK5556_4X4_R21_PCB_BLOCKED_REVIEW.epro2','PCB_FINAL_COLD_CAPTURE.json','ACTUAL_550_PADS.csv','PCB_BOM_AND_PLACEMENT.csv','ACCEPTED_SCHEMATIC_JLC_NETLIST.json','FINAL_DRC_DETAILS.csv','FLOORPLAN.json','PCB_COMPONENT_PLAN.json','SCHEMATIC_PCB_LINKAGE_PLAN.json']
frozen=[]
for name in names:
    b=(O/name).read_bytes(); frozen.append({'path':str(O/name),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest().upper()})
put('FROZEN_INPUT_SHA.json',frozen)
shutil.copyfile(O/names[0],P/'SCIENCE_ADK5556_4X4_R21_PCB_CLOSURE_WORK.eprj2')
shutil.copyfile(O/'cli_call.py',P/'cli_call.py')
shutil.copyfile(O/'capture_pcb.js',P/'capture_pcb.js')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
put('EXECUTION_BUDGET.json',{'startedUTC':now,'approvedMinutes':360,'phasesMinutes':{'nativeIntegration':60,'criticalAnalogRouting':120,'ordinaryRouting':90,'drcColdDelivery':90},'caps':{'createdSessions':3,'saveAttempts':12,'captureAudit':4,'DRC':4},'used':{'copy':1,'createdSessions':0,'saveAttempts':0,'captureAudit':0,'DRC':0},'rulingAssistant':'e13aa5ff-3062-4aa7-859d-fd57ecbf7cd4','rulingParent':'230dd058-72ff-48be-ae8c-aa1fcdef32f9','status':'PHASE1_NATIVE_INTEGRATION','prohibited':['schematicElectricalChange','wholeBoardAutoroute','APIorSDKResearch','simulation','Gerber','procurement','manufacture','actualBench','localGit','systemChanges'],'operations':[]})
put('GATES.json',{'nativeNetlistErrorZero':False,'actual550PadMappingUnchanged':False,'remainingConnectionErrorsProvenOnlyRatsnest':False,'fullRoutingComplete':False,'DRCClean':False,'manufactureReleased':False,'benchReleased':False})
(P/'IMPLEMENTATION_PLAN.md').write_text('''# 唯一 PCB 网络整合及布线包

依据已全文保存的新裁定 e13aa5ff，360min；session3/save12/capture4/DRC4。用户已有PCB设计范围授权，不采购、不制造、不上电。

1. 复制冻结工作PCB一次，先用既有官方操作读取明确JLCEDA格式PCB网表，对照原接受107网/514成员；检查误绑、孤立pad与普通ratsnest。只在有明确证据时同步或重新绑定，不凭空删网或改原理图。遇同一不支持路径、超时或需要工具内部调查即给出可操作交接；不重试autoroute。
2. P1通过后手工完成TIA/ADC/参考短路径与连续GND参考，再普通数字/电源连接。禁止全板自动布线。
3. 最多4次详细DRC、4份完整capture，包含最后冷打开；真实错网/短路/间距须修，丝印提醒记录，不将未连接当模板提醒。
4. 一次新上下文终审后正常完整GitHub固定版本交付、单次内部摘要及接续monitor。若P1阻断则不进入布线，不循环工具修复，明确需用户官方同步动作。
''','utf8')
print(json.dumps({'package':P.name,'workcopyBytes':(P/'SCIENCE_ADK5556_4X4_R21_PCB_CLOSURE_WORK.eprj2').stat().st_size,'startedUTC':now}))
