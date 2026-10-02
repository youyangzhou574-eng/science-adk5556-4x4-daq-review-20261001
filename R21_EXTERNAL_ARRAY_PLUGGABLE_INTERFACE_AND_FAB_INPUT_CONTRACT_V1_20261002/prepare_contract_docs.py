from pathlib import Path
import json,csv,hashlib,datetime,math,collections
P=Path(__file__).parent;old=P.parent/'R21_PCB_MANUFACTURING_PREFLIGHT_READONLY_V1'
b=json.loads((P/'COLD_PCB.json').read_text('utf8'));s=json.loads((P/'COLD_SCHEMATIC.json').read_text('utf8'));j=next(c for c in b['parts']if c['ref']=='J2');gate=json.loads((P/'COLD_QUALIFIED_GATE.json').read_text('utf8'));assert gate['PASS']
with(P/'ACTUAL_550_PAD_NET.csv').open('w',encoding='utf8',newline='')as f:
 w=csv.writer(f);w.writerow(['reference','pad_number','net','x_mil','y_mil','NC']);w.writerows([c['ref'],p['number'],p['net'],p['x'],p['y'],not bool(p['net'])]for c in b['parts']for p in c['pads'])
with(P/'J2_ACTUAL_8PIN_HARNESS.csv').open('w',encoding='utf8',newline='')as f:
 w=csv.writer(f);w.writerow(['PCB_pin','PCB_net','array_conductor','PCB_x_mm','PCB_y_mm','housing_contact']);w.writerows([p['number'],p['net'],p['net'],p['x']*.0254,p['y']*.0254,'Trace actual mating contact; do not assume molded housing numbering']for p in j['pads'])
with(P/'ACTUAL_176_CORE_BOM.csv').open('w',encoding='utf8',newline='')as f:
 w=csv.writer(f);w.writerow(['reference','name','manufacturerPart','footprint_name','x_mil','y_mil','rotation_deg']);w.writerows([c['ref'],c['name'],c['manufacturerId'],c['footprint']['name'],c['x'],c['y'],c['rotation']]for c in b['parts'])
rows=list(csv.DictReader((old/'MANUFACTURING_PREFLIGHT_MATRIX.csv').open(encoding='utf-8-sig')))
for r in rows:
 if 'J2' in r['item'] or 'connector' in r['item'].lower():r['requiredInputOrAction']+='; R17 Molex1718560008/22012087 implemented; terminalAWG and actual supplied cable compatibility remain pending'
rows.extend([dict(id='J2-01',item='Molex 1718560008/22012087 compatible mating series',status='PASS',evidence='Manufacturer-authored exacthousing product sheet names171856/171857; 8position drawing table',requiredInputOrAction='No availability or currentActive claim',scope='default new matched connector standard'),dict(id='J2-02',item='Actual project-local8pad footprint and warm/cold fourclassDRC',status='PASS',evidence='Actual File footprint8holes1.14mm;1.70mm copper;2.54mm pitch;actual8pin ROW/COL;warm/coldDRCempty',requiredInputOrAction='Generic device association retained; use assembly MPN override and qualified project footprint',scope='J2-only ECO'),dict(id='J2-03',item='Exact crimp terminal and supplied cable',status='PENDING_INPUT',evidence='Housing2695-8R series22-30AWG/max insulation1.57mm; exact terminal not selected',requiredInputOrAction='Actual conductorAWG and insulation diameter; terminalplating/crimp tooling; continuity pin1 mapping',scope='No purchase or physical matching claim'),dict(id='J2-04',item='Full mated3D/enclosure envelope',status='PENDING_INPUT',evidence='2D bodyinside100x90board; verticalaccess expected with no enclosure model',requiredInputOrAction='Enclosure height and strainrelief/cable bend; old generic3D association is NOT qualified',scope='No full3D mechanical release')])
with(P/'MANUFACTURING_PREFLIGHT_MATRIX.csv').open('w',encoding='utf8',newline='')as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
(P/'J2_CONNECTOR_AND_HARNESS_SPEC.md').write_text('''# J2 可插拔8线接口规格（审查版）

板端 **Molex1718560008**，单排8位、2.54mm、竖直PTH、摩擦锁；线端 **22012087 /22-01-2087 /2695-8R** 压接壳体。线端接头插到板端，不把8根线直接焊到PCB。每个待测电阻Rij只接ROWi与COLj，16个电阻形成4行4列；J2没有GND或供电针。

从PCB真实方形1脚起：1ROW0、2ROW1、3ROW2、4ROW3、5COL0、6COL1、7COL2、8COL3。必须逐芯连通确认实际对接关系，不能假定线壳模制数字与板座1脚相同。它是摩擦锁接口，不承诺完全防反插。

准确压接端子MPN尚未锁定：实际AWG、绝缘外径、镀层和压接工具未知。厂家公共图给出22–30AWG/max insulation1.57mm及2759/6459/41572/4809/8088系列，不能把系列范围当作每个端子MPN资格。没有承诺兼容用户原有未知型号线缆；当前采用已批准的新成套标准。

## 原生工程实际身份与装配覆盖

J2原理图/PCBName与ManufacturerPart为1718560008，Manufacturer为MOLEX，旧通用供应编号C124381已清空。仅J2使用项目封装87b2e6ab0bf2243f，名MOLEX_1718560008_MFR_SD171856_R17，真实File里尺寸通过；保留通用8针电气symbol与generic device UUID，不冒称厂家库器件已入库。装配选料须使用准确MPN与本项目封装，不按generic device/catalog名采购。

原生自定义MatingHousing/CrimpTerminal等属性键创建但实际值为空，API返回true不是字段已写证明。配套壳体/端子/针序以本文和实际8针CSV为合同。旧generic排针3D关联仍存在，**不能用于新Molex机械验证**；没有制造/全3D或用户现有线缆兼容放行。项目正文不让这些元数据缺项卡住电气主线。

来源与尺寸见CONNECTOR_SOURCE_QUALIFICATION.md。当前Molex页Limited Information Available；不把旧裁定的Active说法作为实证。资料镜像旧版图明确列出8位，不称当前最新版或供货保证。
''','utf8')
(P/'J2_PINOUT_AND_KEYING.md').write_text('''# 实际针序与方向

见J2_ACTUAL_8PIN_HARNESS.csv及J2_PINOUT_AND_BODY.png。图按PCB顶面、EDA正y向上绘制：方形1脚在本图下端（x约5mm/y约30.11mm），三角丝印在1脚右侧。上端为8/COL3，不能按照片“从上到下”自动当作1..8。

板座body20.17×6.35mm，pinspan17.78mm。projectcourtyard选21.88×7.37mm（包括20.88mm线壳长向+两端0.5mm，以及板端外侧0.5mm余量）；这是本项目设计选择，非厂家推荐courtyard。manufacturerassembly外形离板左边最小约1.90mm，projectcourtyard约1.40mm，未移J2或改板框。孔径1.14±0.05mm来自厂家推荐；1.70mm铜盘为本板选择，名义环0.28mm，最大孔1.19mm时环0.255mm。

摩擦锁侧面沿PCB左侧（local+y经90°旋转后-x）。应沿板法向竖直插拔；机壳/扎带/弯曲半径未知，完整mated3D与真实操作空间仍PENDING。图中示意不作为完全机械认证。厂家特别注明header circuit1可能不与housing circuit1相同；装配线束须以实际接触连续性匹配，不只看壳体数字。
''','utf8')
(P/'FABRICATION_INPUT_CONTRACT.md').write_text('''# 制造输入合同（未放行生产）

接受的电路与板框：4×4/8线，正常1–7kΩ、0.8–8kΩ保护带；100×90mm矩形四层，176器件/550pad/514assigned/107nets/36NC。新J2准确板端1718560008+壳体22012087，针序与J2规格配套。其它175器件/主模拟走线/规则保持，warm/coldDRC四类0只证本原生工程。

仍需目标板厂、板厚/叠层/内外铜厚、表面处理、阻焊颜色及最小桥、finishedPTH容差与孔铜、钢网/回流/装配方式、拼板/定位/fiducials及机壳/插拔空间。U5/U9/U10约0.09–0.097mm阻焊桥等待板厂CAM接受，当前不改原封装。J2 PCBtail2.34mm及厂商孔1.14±0.05mm须对最终板厚/装配工艺核实，不能预先宣称可制造。

待用户明确真实线径/绝缘外径后才锁端子MPN/线束工艺；可先审图与选择工艺，不要求补线材照片才继续现有ECO。禁止下单、采购、制造、Gerber生产放行、bench及上电。PCB当前为工程审查版，3D/实体精度/100fps/故障保护/参考容量/WCET仍未放行。
''','utf8')
(P/'MANUFACTURING_OPEN_ITEMS.md').write_text('''# 仍待输入事项

1. 线芯AWG、绝缘外径、镀层、压接工具与准确端子MPN；不直接假定用户现有线束可配。
2. 目标板厂、板厚叠层铜厚、阻焊能力（约0.09–0.097mm桥）、表面处理、钢网回流与装配方式。
3. 机壳净高、线束应力释放与竖直插拔操作空间；旧generic3D不能作为Molex验证。
4. 原生device仍generic、J2配套自定义属性为空；准确选料使用J2_CONNECTOR_AND_HARNESS_SPEC.md、MPN和实际项目封装。之后若要求独立装配自动BOM，须集中批准一次有限metadata整理，不能自行追加当前save额度或API研究。
5. 继承动态/故障/容量/ERC明细/独立PDF文字/实际bench等HOLD。禁止生产与上电。

这些不否定J2真实8孔封装、针序与温冷电气连接验收，不循环重开已接受电路/制造前只读包。
''','utf8')
oldhash={}
for folder,names in [('R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1',['SCIENCE_ADK5556_4X4_R21_POUR_CLOSURE_WORK.eprj2','SCIENCE_ADK5556_4X4_R21_PCB_CLOSED_REVIEW.epro2']),('R21_PCB_MANUFACTURING_PREFLIGHT_READONLY_V1',['COMPLETE_MANUFACTURING_PREFLIGHT_RECEIPT.md','MANUFACTURING_PREFLIGHT_MATRIX.csv'])]:
 for n in names:
  f=P.parent/folder/n;oldhash[str(f.relative_to(P.parent))]={'bytes':f.stat().st_size,'SHA256':hashlib.sha256(f.read_bytes()).hexdigest().upper()}
(P/'FROZEN_BASELINE_SHA_AFTER.json').write_text(json.dumps(oldhash,indent=2),'utf8')
now=datetime.datetime.now(datetime.timezone.utc);budget=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'));budget['nativeFinishedUTC']=now.isoformat();budget['status']='NATIVE_OPERATIONS_COMPLETE_NO_MORE_CAD_PENDING_DELIVERY';budget['usedNativeSummary']={'copy':1,'session':2,'save':2,'captureaudit':3,'DRC':2,'export':1,'officialSources':4,'candidate':1,'normalPourRebuild':1,'J2OnlyImportChanges':1,'solver':0};budget['partialWorkingObservationsSeparate']=True;budget['phaseAllocationNote']='45/30/45/60 are planning allocations; elapsed total remains180min hard cap. Actual implementation included finite failed setter/instance-overlay attempts retained, not a new tool research package.';(P/'EXECUTION_BUDGET.json').write_text(json.dumps(budget,indent=2),'utf8')
(P/'SESSION_GUI_LIFECYCLE.json').write_text(json.dumps({'warmSession':'91b63e42-6f8c-4581-b775-1bc0e7f07d3e','coldSession':'2f2b9d5b-7cd7-4547-8db5-1c64541a0e07','officialBothClosed':True,'warmGUIExitedBeforeCold':True,'freshFinalOwnWindows':[],'newSolverProcesses':0,'UTC':now.isoformat()},indent=2),'utf8')
(P/'GATES.json').write_text(json.dumps({'J2_MANUFACTURER_PAIRING_PASS':True,'J2_ACTUAL_8PAD_FOOTPRINT_PASS':True,'J2_PIN_NET_WARM_COLD_PASS':True,'OTHER175_AND_PRIMARY_COPPER_PASS':True,'J2_BODY_INSIDE_BOARD_PASS':True,'WARM_COLD_DRC_4CLASS_ZERO':True,'PCB_REVIEW_READY':True,'J2_EXACT_TERMINAL_PENDING':True,'J2_GENERIC_DEVICE_METADATA_HOLD':True,'J2_3D_NOT_QUALIFIED':True,'FAB_INPUT_PENDING':True,'MANUFACTURING_NOT_RELEASED':True,'BENCH_NOT_RELEASED':True,'NO_MORE_NATIVE_EDITS_THIS_PACKAGE':True},indent=2),'utf8')
print(json.dumps({'nativeReviewPASS':gate['PASS'],'matrixRows':len(rows),'contractFilesCreated':True,'noMoreCAD':True}))
