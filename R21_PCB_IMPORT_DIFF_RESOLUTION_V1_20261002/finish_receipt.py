from pathlib import Path
import json,hashlib,datetime,csv,shutil
p=Path(__file__).resolve().parent; prior=p.parent/'R21_PCB_NETLIST_INTEGRATION_AND_ROUTING_CLOSURE_V1'
oldfreeze=json.loads((prior/'FROZEN_INPUT_SHA.json').read_text('utf8'))
freeze=[]
for x in oldfreeze:
 f=Path(x['path']);h=hashlib.sha256(f.read_bytes()).hexdigest().upper();assert h==x['sha256'];freeze.append(dict(x,actualSHA256=h,PASS=True))
f=prior/'SCIENCE_ADK5556_4X4_R21_PCB_CLOSURE_WORK.eprj2';receipt=json.loads((p/'UI_WORKCOPY_RECEIPT.json').read_text('utf8'))
assert hashlib.sha256(f.read_bytes()).hexdigest().upper()==receipt['sha256'] and f.stat().st_size==receipt['bytes']
freeze.append({'path':str(f),'bytes':f.stat().st_size,'actualSHA256':hashlib.sha256(f.read_bytes()).hexdigest().upper(),'note':'prior package frozen input; compared to UI_WORKCOPY_RECEIPT source hash separately below'})
(p/'FROZEN_INPUT_FINAL_PASS.json').write_text(json.dumps(freeze,indent=2)+'\n','utf8')
shutil.copyfile(prior/'ACTUAL_PCB_JLC_NETLIST.json',p/'BEFORE_ACTUAL_PCB.enet')
shutil.copyfile(p.parent/'R21_PCB_FLOORPLAN_AND_LAYOUT_V1/ACCEPTED_SCHEMATIC_JLC_NETLIST.json',p/'ACCEPTED_SCHEMATIC.enet')
audit=json.loads((p/'FINAL_ACTUAL_AUDIT.json').read_text('utf8'));classification=json.loads((p/'IMPORT_DIFF_CLASSIFICATION_SUMMARY.json').read_text('utf-8-sig'))
assert audit['pads']==550 and audit['nets']==107 and classification['SourceMismatch']==0
budget={'approvedMinutes':60,'rulingAssistant':'f81ed2e0-961f-4de1-b2aa-1b89e74ab2a2','status':'IMPORT_DIFF_RESOLVED_REVIEW_COMPLETE_NO_ROUTING_IN_THIS_PACKAGE','GUIIndependentWorkcopy':1,'GUIFullCSVExport':1,'GUIImportApply':1,'GUICtrlSSave':1,'GUIProjectNativeExport':1,'GUINativeExportConfigSaveToast':1,'GUIJLCNetlistExport':1,'GUI_DRC':2,'GUIOpenLifecycle':2,'headlessReadonlyColdAuditSession':1,'headlessReadonlyCapture':1,'headlessReadonlyColdAuditClosed':True,'routing':0,'simulation':0,'schematicEdit':0,'procurement':0,'manufacture':0,'actualBench':0,'localGit':0,'notNewHardCountQuotas':'Pro specified 60min and one synchronization; these are actual operation records, not invented approved quotas.'}
(p/'EXECUTION_BUDGET.json').write_text(json.dumps(budget,indent=2)+'\n','utf8')
gates={'IMPORT_DIFF_CLASSIFIED':'PASS 697 property changes; 0 net/pin/footprint/component actions','SCHEMATIC_PCB_ALL_PIN_MAPPING':'PASS 550/550 before/warm/cold','NETLIST_ERROR':'PASS 0 after sync and GUI cold reopen','ROUTING_CLOSURE':'HOLD 452 ConnectionError entries remain','DRC_CLEAN':False,'BENCH_NOT_RELEASED':True,'MANUFACTURING_RELEASED':False,'NEXT_PACKAGE_NOT_STARTED':True}
(p/'GATES.json').write_text(json.dumps(gates,indent=2)+'\n','utf8')
report=f'''# R21 PCB Import Changes：实际差异核对与一次同步回执

本包已解决 schematic↔PCB NetlistError。按用户本轮“开 computer use”指示，实际操作嘉立创EDA V4.1.60 的独立本地工程副本；未改原理图、未新增布线。温检查和关闭应用后冷重开检查均只剩452条连接性错误，NetlistError=0。452条表示尚未完成的铜连接，整板仍非DRC clean、不可制造/上电。

## 冻结输入与真实差异

输入为已交付闭合尝试的工作工程，先复制至本包；原始包不修改。Import Changes窗口先导出报告再分类，导出CSV实际为TAB分隔、BOM FF FE的UTF-16LE，保留原字节；IMPORT_CHANGE_DIFF_WEB.csv另作UTF-8标准逗号CSV供网页读取，全部873行字段逐格一致。873行=176器件组+697变更；367新增属性、330修改属性，全部导入后值逐项与accepted schematic JLC官方网表核对一致。没有新增/删除器件、改变封装、引脚归网或网络名称的动作。

665项可接受属性同步，32项为C_ADC0–3的历史库描述残留按master同步为空，包含Tolerance/Voltage Rating/LCSC Part Name/Description等，不是删除Device/Footprint/MPN。完整原值与型号保存在原CSV、分类CSV、BEFORE_ACTUAL_PCB.enet和冻结输入。J1的Name补全，176 Channel ID补全；Value125项恢复master描述（例如2.2nF→2.2nF C0G），无重新设计电气值。分类脚本初将中文“立创元件名”映射为DeviceName导致4项校验不匹配，实际键为LCSC Part Name，核官方两份props后更正；最终697/697 source match。未借此改master或查工具内部。

## 唯一同步和保存

在上述分类完成后只点击一次“应用修改”，界面显示导入完成；Ctrl+S显示保存成功。设计规则导入未勾选。导线网络同步默认勾选但本次列表无net变更。未增加线路、重新布局、清网、重建PCB或删除器件。导出真实PCB JLC .enet及工程epro2，同时保留可直接打开的已保存eprj2。

## 同步后与冷重开证据

GUI温DRC完成：全部452，连接性错误452；原来的1条NetlistError消失。完全关闭本轮GUI应用（窗口清单中已无本应用），重新启动并从准确本包路径打开eprj2；冷DRC同样全部452/连接性452，NetlistError0。未对菜单瞬时提示宣称完整空diff证书。

温GUI导出的AFTER_SYNC_ACTUAL_PCB.enet、随后只读headless冷捕获COLD_ACTUAL_PCB.enet、同步前官方PCB .enet与master均逐针相同：176器件/550pads/514assigned/107nets/36NC，额外与缺失引脚0。BEFORE_AFTER_NETLIST_COMPARE.csv含全部550行，含NC。

冷捕获全部176器件的坐标/旋转/层/550pad位置形状与归网、Device的uuid/name/source与Footprint的uuid身份，与上包冷捕获严格一致。副本全部176器件外层libraryUuid由父包5f0f...重定位到本包5827...，属于工程库命名空间，比较明确排除此字段而核库内uuid/name/source，不冒称完整库对象字节相等。四插针无MPN的返回表示由None变为空串，不称原字节相等，INITIAL_STRICT_MPN_ABSENCE_DIFFERENCES.json保留初严格失败。93线路、板框POLY、POUR、PAD_NET及规则记录的完整KV/多重集合一致；不是单纯核数量。冻结10输入哈希复核PASS。原eprj2父包源哈希对照UI_WORKCOPY_RECEIPT记录。

epro2真实导出{audit['nativeBytes']}bytes，SHA256 {audit['nativeSHA256']}，ZIP CRC全PASS。导出的epru保留，含历史/删除记录，不能按全行现态直接比较；该尝试遇到RULE_SELECTOR空payload后停止，没有继续研究parser/API。本次两种冷重开针对交付eprj2，不冒称独立epro2重开已验证；epro2由GUI实际工程另存导出，不是伪造格式。

只读headless审计session8c9b3d88-c194-4e07-ba0a-35980e0cfa36官方closed；本轮两个GUI生命周期均正常关闭。没有solver或pending操作。

## 实际门和范围

本包Import diff分类、514连接+36NC逐针同源、冷重开NetlistError0通过；后续routing尚未执行。452连接性DRC未消除、铺铜填充和缝合/完整GND平面未验证。保持动态/供电/温区/故障/容量/WCET/SWD/bench/ERC/原理图旧注释质量等原HOLD；本包不解决这些、不将原理图基线接受等同于硬件性能。

实际operation见EXECUTION_BUDGET.json：copy1、Apply1、CtrlS1、nativeExport1、GUI_DRC2、GUI .enet1、GUI生命周期2、只读headless session/capture1。新routing/schematicedit/SPICE/PCB制造/采购/actualbench/localGit均0。既有HEADLESS审计仅已知官方capture方法，无API/SDK内部研究。

## 集中请求唯一下一工程包

用户明确要求在下一次正常报告同时申请更多执行时间/次数/自主推进范围，以减少细步请示。本报告据此请求R21_PCB_ROUTING_CLOSURE_V1，360min（敏感采集120/其余网络120/GND与电源45/DRC冷审45/交付30）；最多session3/save12/captureaudit4/DRC4。在冻结100×90mm四层候选、176器件和电气拓扑下自主完成余下铜连接、必要过孔/地缝合和铺铜，不动schematic/主值/封装身份、不展开理论或新仿真，不重试已失败自动布线。实际短路、错网、器件身份漂移或NetlistError复现即停止并保留证据；不靠消音DRC通过。目标全部pin归网保留、NetlistError0/连接性0及DRC完整分类，仍仅审查板，不输出生产Gerber、不采购制造上电。只是请求，未批准不执行。

END-OF-COMPLETE-R21-PCB-IMPORT-DIFF-RESOLUTION-RECEIPT
'''
(p/'COMPLETE_IMPORT_DIFF_RECEIPT.md').write_text(report,'utf8')
(p/'README.md').write_text('# R21 PCB import diff — synchronization resolved\n\n[Complete receipt](COMPLETE_IMPORT_DIFF_RECEIPT.md) · [Readable UTF8 actual diff](IMPORT_CHANGE_DIFF_WEB.csv) · [Original UTF16LE/TAB export](IMPORT_CHANGE_DIFF.csv) · [Classified diff](IMPORT_CHANGE_CLASSIFICATION.csv) · [All550 before/warm/cold pins](BEFORE_AFTER_NETLIST_COMPARE.csv) · [Actual audit](FINAL_ACTUAL_AUDIT.json) · [Cold GUI DRC](COLD_REOPEN_DRC_UI.txt) · [Native epro2](SCIENCE_ADK5556_4X4_R21_PCB_SYNC_REVIEW.epro2) · [Cold reopened workfile](SCIENCE_ADK5556_4X4_R21_IMPORT_DIFF_WORK.eprj2).\n\n697 property-only changes reviewed then one Apply. NetlistError0;452 incomplete copper connection entries remain. REVIEW ONLY, no manufacturing/powerup; routing is the requested next package.\n','utf8')
print(json.dumps({'reportBytes':len(report.encode()),'freezeChecked':len(oldfreeze),'state':'synchronization gate passed; routing not started'}))
