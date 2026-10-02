from pathlib import Path
import json
P=Path(__file__).parent
# One documentation fix pass for final-review Important: native net labels missing.
g=json.loads((P/'GATES.json').read_text('utf8'));g.update(PCB_REVIEW_READY=False,BASELINE_PCB_REVIEW_READY_INHERITED=True,J2_NATIVE_SILK_ROWCOL_MISSING=True,J2_ECO_CONFORMANCE_HOLD=True,J2_ELECTRICAL_AND_2D_FOOTPRINT_REVIEW_PASS=True,MANDATORY_PINOUT_COMPANION=True);(P/'GATES.json').write_text(json.dumps(g,indent=2),'utf8')
add='''\n\n## 17号丝印要求的未闭合项\n\n实际原生丝印可见J2与1脚三角，但**没有ROW0–ROW3/COL0–COL3或1/ROW0文字**；GUI padnet显示不属于制板丝印。17号要求未完全满足。准确针序图/CSV为mandatory companion，不能声称该文字已印在板上。J2电气/尺寸/温冷DRC通过，独立J2制造接口conformance保持HOLD，请Pro接受配套图作为当前审查合同或统一批准一次最小原生丝印补字。当前硬save/audit/export已满，不自行追加CAD，也不调查工具。\n'''
for n in('J2_PINOUT_AND_KEYING.md','J2_CONNECTOR_AND_HARNESS_SPEC.md','MANUFACTURING_OPEN_ITEMS.md','FABRICATION_INPUT_CONTRACT.md'):
 with(P/n).open('a',encoding='utf8')as f:f.write(add)
f=P/'COMPLETE_J2_INTERFACE_RECEIPT.md';t=f.read_text('utf8');t=t.replace('真实原生8孔、body/lock/courtyard/pin1与温冷针网复核通过；准确端子MPN/线束/制造工艺/完整3D仍未放行。','真实原生8孔、body/lock/courtyard/pin1与温冷针网复核通过；原生ROW/COL文字丝印要求未闭合，J2_ECO_CONFORMANCE_HOLD。准确端子MPN/线束/制造工艺/完整3D仍未放行。')
pos=t.index('## 制造输入与下一阶段请求');end=t.index('END-OF-COMPLETE-R21-',pos)
t=t[:pos]+'''## 终审要求差距与下一阶段请求（用户明确要求更多有界工作预算）

一次fresh-context终审发现Important：17号要求原生丝印1/ROW0或三角+ROW/COL名称，actualFile只有J2/三角、无ROW/COL文字。GUIpadnet和配套图不能冒称制板文字。当前三硬额度save/audit/export满，不再CAD；回执一次文档修复明确J2_ECO_CONFORMANCE_HOLD、PCB_REVIEW_READY=false（15/16基线接受保留不回写），电气/真实封装温冷资格PASS。Mandatory8针图/CSV明确方向，可审查但独立接口conformance需Pro接受偏差或补字。

用户明确要求在正常报告同时申请适合项目的执行时间、次数和自主范围，以减少反复请示。请求唯一下一包 **R21_J2_SILK_CONFORMANCE_AND_ASSEMBLY_INPUT_CLOSURE_V1** 最多180min：有限knownGUI丝印/metadata30、温冷45、成套输入合同45、交付60。优先请Pro接受现有mandatory针序图/选料覆盖，让工程主线前行；仅若要求原生补字，条件copy1/session2/save2/captureaudit3/DRC3/export1，范围仅J2附近非铜层1/ROW0及ROW0–3/COL0–3短丝印，禁止改铜/孔/网/位置/值/规则、Import、库/新候选、API研究。Normalpour0，主电路仿真/采购/制造/bench/Gerber全部0。ordinary文件核对和可操作现有UI实现自主累计；失败保留companion，不把工具研究作为门。实际AWG/fab输入到后可读合同核对official新增资料<=4/terminal候选<=2，无输入就保存清单等待用户，不能循环重做。

只是请求，未批准不执行；不扩平台或账户额度，不自用旧剩量。继续保持J2_ECO_CONFORMANCE_HOLD、J2_EXACT_TERMINAL_PENDING、J2_GENERIC_DEVICE_METADATA_HOLD/J2_3D_NOT_QUALIFIED、FAB_INPUT_PENDING、MANUFACTURING_NOT_RELEASED、BENCH_NOT_RELEASED及历史科学/性能HOLD。readablecompanion强制随原生，独立自动制造文件未放行。

'''+t[end:];f.write_text(t,'utf8')
f=P/'README.md';t=f.read_text('utf8');t=t.replace('其它175与主铜不变。准确端子','其它175与主铜不变。原生ROW/COL文字未印，17号丝印conformance HOLD（配套图/CSV强制随附，不能当实际丝印）。准确端子');f.write_text(t,'utf8')
f=P/'IMPLEMENTATION_DEVIATIONS.md';f.write_text(f.read_text('utf8')+add+'\nOne final review Important fixed in disclosure only; no native operations, no second review.\n','utf8')
(P/'IMPORTANT_DISCLOSURE_FIX.json').write_text(json.dumps({'nativeBeforeAndAfterIdentical':True,'noNativeFixWithinExhaustedQuota':True,'originalReportClaimIncomplete':True,'newGateFalseAndMandatoryCompanion':True,'requiresNewUnifiedDecision':True,'oneDocumentationFixPass':True},indent=2),'utf8')
print('Important requirement deviation disclosed; updated conformanceHOLD and unique bounded next request')
