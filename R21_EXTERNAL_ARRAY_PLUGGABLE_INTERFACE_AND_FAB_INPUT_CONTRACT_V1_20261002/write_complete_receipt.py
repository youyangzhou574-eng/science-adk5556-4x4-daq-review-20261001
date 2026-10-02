from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).parent
f=P/'CONNECTOR_SOURCE_QUALIFICATION.md';t=f.read_text('utf8').replace('public delivery will provide links, bounded notes and selected relevant cropped pages rather than bulk PDFs.','public delivery provides source links, bounded dimension notes and source hashes; full mirrored PDFs, full-page PNGs and bulk extracts remain local only.');f.write_text(t,'utf8')
with (P/'IMPLEMENTATION_DEVIATIONS.md').open('a',encoding='utf8')as f:f.write('''

Final implementation route: instance overlay was not selectable in schematic library. Verified original project footprint87b2... is used only byJ2; GUI restore-to-template then edit-project-template. Renamed and manufacturer-derived fivebody/courtyard/silk primitives replaced the sixgeneric outline primitives. Final exact native pad1setter completed1.70×1.70mm; previous GUI mixed/table values and failed dimension checks retained. No new library account/catalog save. Final one SaveAll after warmPASS persisted projectfootprint+sch+PCB; conservative actualsave2 consumed (instanceapply1 + finalSaveAll1), no more saves.

ImportChanges dialog listed onlyJ2 properties, no footprint/pin reorder or otherparts. Simultaneouswire-network update explicitly unchecked before apply. One normalRebuildAll withinJ2ECO rule scope, fourPOUR boundaries/rules unchanged, expandedJ2pad anti-pads derived. No fanout/reroute was needed.

Initial strict warm source comparison wasfalse only because all6DOCHEAD changedclient/updateTime/version; every substantive source primitive outsideJ2 unchanged. Originalfalse retained; bounded threeheader-field exclusion and explicitdiff inspection yielded true. Cold rawsource/netlist equality wasfalse: fourPOURED209 floating numbers max2.1032064978498966e-12 with identicalstructure (same accepted16 arithmetic noise), seven hiddenJ2metadata attributezIndex reordered, and one warmnetlist transporttext Manufacturer muRata(村���) vs correctcold村田. NativeATTR and full176core exact, allpinInfoMaps exact. Rawfalse retained, no source or manufacturerdata rewritten to makePASS. File contains same historically acceptedtwo0.1milLINE extras, not newly edited. No additionalnative capture/DRC/repair/solver.

CustomJ2attribute keys exist but values empty; genericcatalog device and generic3Dassociation retained. AccurateMPN/Manufacturer/Name and realprojectfootprint are proven. Companion assemblyoverride is mandatory; no manufacturer-librarydevice/full3D/automaticBOMqualification. SupplierPart oldC124381 was actually cleared viaGUIandimport. Do not letmetadata caveat imply allconnectorproductization/manufacturing is fully complete.

Allnative quotas terminated aftercold. Twoofficialsessionsclosed and bothownGUIexited; no solver. Currentpackage stopsnewCAD/save/capture/export regardless unusedDRC1/candidate1. Wholepackagefinalread-only review remains; no secondreview or minorpolish.
''')
m=json.loads((P/'FINAL_NATIVE_FILE_METADATA.json').read_text('utf8'));b=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'));now=datetime.datetime.now(datetime.timezone.utc)
receipt=f'''# R17 J2 可插拔接口ECO与制造输入合同 — 工程审查版

用户要求“单排8针线、插槽插拔、不是焊8根线”。本包已把J2从通用裸排针的实际封装改为 **Molex1718560008板端 +22012087/22-01-2087线端壳体** 的准确8位2.54mm竖直摩擦锁方案。真实原生8孔、body/lock/courtyard/pin1与温冷针网复核通过；准确端子MPN/线束/制造工艺/完整3D仍未放行。不是采购、制造或上电结果。

## 裁定和冻结输入

唯一17号CIRCUIT-PRO-R21-MANUFACTURING-PREFLIGHT-ACCEPT-PLUGGABLE-J2-ECO-20261002-17，assistant9aa9447b-4ee7-435f-827a-c2c24055dff5，parent320de471-6b63-4a0f-ba41-1681d6d74928。全文PRO_J2_INTERFACE_RULING_FULL.md。
基线15/16接受commit e9c1b72f4d1659bb9a7a1dbe4a82e7937c5fe86a，actualnativeSHA C2D53B0B6BB438D7C916BE24CB0B0D6AE5C7D884E7784EEFFED90E61505BEE6C；新唯一eprj2副本，旧基线未打开改动。正常1–7kΩ约10%变化、0.8–8kΩ保护带，4×4/8线/5V+3V3/VCM2.5/VEXC2.25/E.25/Rf4.99k/Cf2.2nF/100fps目标保持，所有实际性能HOLD继承。

## 接口与厂家证据边界

四个logicalsources：exactheader页、exacthousing页、headerSD171856图、housing26950000图。厂家主机请求超时保留，同一厂家文档从分销镜像取得，未新增第五独立工程来源。header图首B2续B1（2018），housingA3明确8位表；不冒称最新B3。exacthousing产品表明确171856/171857对接系列。当前Molex页面LimitedInformationAvailable，纠正旧裁定Active未核说法。完整第三方PDF/全文extract/全页PNG只本地保留，公开短说明/链接/SHA。

8针pinspan17.78mm、pitch2.54mm；headerbody20.17×6.35mm，housinglong20.88mm。finishedPTH1.14±0.05mm来自厂家；铜盘1.70mm与courtyard21.88×7.37mm是本板选择。不存在厂家指定铜盘/courtyard声明。当前body左边距1.90mm、courtyard边距1.40mm，均在100×90板框内，无移动J2/板框/其他件。竖直法向插拔的2D板面空间通过，机壳净高/全mated3D/实际线束操作未验证。

针序真实1ROW0、2ROW1、3ROW2、4ROW3、5COL0、6COL1、7COL2、8COL3；方形1脚+原生三角在图下端。Rij接ROWi↔COLj，不加GND/电源。housing模制数字可能不对应header1，必须实际对接连通映射。2695-8R摩擦ramp没有RP极化筋，不能承诺完全防反插。terminal exactMPN必须按实际22–30AWG范围内芯线/绝缘<=1.57mm以及端子具体规格确定；未替用户采购。未知原有线材兼容不冒称PASS。

## 原生实际实施

仅J2封装87b2e6ab0bf2243f使用者核查PASS后编辑项目template；Name MOLEX_1718560008_MFR_SD171856_R17。actualFile8pads全部孔1.14、铜1.70，pin1RECT、其余ELLIPSE，pin坐标/ROWCOL未变。新assembly/courtyard/silkbody/lock/pin1共5poly替旧6generic；无主铜改动。ImportChanges仅J2身份属性，对导线网络自动更新取消勾选。

Name/ManufacturerPart实际1718560008，Manufacturer MOLEX，旧SupplierPartC124381清空。generic8针symbol/deviceassociation仍保留，不冒称厂家catalogdevice入库。customMatingHousing/CrimpTerminal/Provenance等属性实际空，旧generic3D保留；**J2_CONNECTOR_AND_HARNESS_SPEC.md与实际8针CSV是配套装配合同，不能按旧genericdevice/3D选料或机械认证**。这份mandatorycompanion也是可读审批附件。

## Warm/cold真实证据

baseline/warm/cold **176parts/550pads/514assigned/107nets/36NC**；其它175核心字典与所有坐标exact；全部550padnet/NC、全部pinInfoMaps一致。主LINE909/VIA297/POUR4边界/规则/铜层同baseline；仅J2封装pad/body/silk和正常derivedfill局部变化。未重布走线。
真实WarmDRC=[]，独立coldDRC=[]：Connection/Short/Clearance/NetlistError全部0。warmofficialsession关闭+ownGUI退出后newcoldsession2，真实File冷导出。

不能称rawsource/netlistbyte相等：transportDOCHEAD3字段变化；cold7hiddenJ2ATTRzIndex顺序变化；4POURED209浮点数max2.1032064978498966e-12、结构0差，属于16已接受表示精度；warmnetlist单个muRata中文文本UTF8替换字符，cold正确，actualATTR/176core一致。严格初false和原diff全部保留；qualified工程证据不屏蔽pin、铜、MPN差。File额外历史两0.1milLINE VCM137f992f55430857/TIA121f945bfa3a6372f仍按16接受表示差保留，不自行重画。实际File核心/padnet/规则与cold相同。

实际File {m['name']}，{m['bytes']}bytes，SHA256 **{m['SHA256']}**。不把eprj2或脚本计划当actualFile。源码/8孔文件原文、实际全部550CSV、工程BOM176CSV、warm/colddrclog、图面PNG、所有失败与来源hash均直接提供。

## 预算和停止状态

批准180min，start {b['startUTC']}，本阶段记录 {now.isoformat()}，当前elapsed {(now-datetime.datetime.fromisoformat(b['startUTC'])).total_seconds()/60:.2f}min（公开交付最终时另更新）。copy1/1、session2/2、save2/2（实例apply1+一次finalSaveAll1）、captureaudit3/3（baseline/warm/cold+File）、DRC2/3、export1/1、officialSources4/4、candidate1/2、normalPour1、J2onlyImport1。部分J2workingobservations与source尺寸checks另列，不假称只有3次工具读取。P0/P1/P2/P3的45/30/45/60作为计划分配，未把长期拖延重置总180min；有限实施失败/途径在ledger保留，未另开API/工具研究。

两officialsessionsclosed、freshownGUI空、solver0。新仿真/MIMO/descriptor/全板重布/Gerber/采购/制造/bench/上电/localGit/system均0。原生阶段已终结，不因DRC1/candidate1剩余自启CAD，当前只读合同/终审/交付。

## 制造输入与下一阶段请求（用户明确要求更多有界工作预算）

用户明确要求在正常报告同时申请适合项目的执行时间、次数和自主范围，以减少反复请示。本包工程接受后建议唯一下阶段 **R21_CONNECTOR_ASSEMBLY_AND_FAB_INPUT_CLOSURE_V1**：有实际线径/绝缘与目标fab/装配输入才展开，最多180min（输入30/official资料+端子合同60/集中制造矩阵30/交付60）、official新增资料<=4/端子候选<=2；普通资料核对和合同编辑自主累计，重大兼容/工艺拒绝集中报告。CADcopy/session/save/capture/DRC/export/所有仿真/采购/制造/bench/Gerber全部0；不扩平台或账户额度。若输入未到，只接受现有J2工程与缺输入清单等待用户，不重复已结案包、不为metadata/3D再研究API。若必须做独立自动BOMmetadataECO另由统一裁定明确一次有界范围，不擅用旧预算。

继续保持FAB_INPUT_PENDING、J2_EXACT_TERMINAL_PENDING、J2_GENERIC_DEVICE_METADATA_HOLD/J2_3D_NOT_QUALIFIED、MANUFACTURING_NOT_RELEASED、BENCH_NOT_RELEASED及历史科学/性能HOLD。readablecompanion强制随原生，独立自动制造文件未放行。

END-OF-COMPLETE-R21-J2-PLUGGABLE-INTERFACE-AND-FAB-INPUT-CONTRACT-REVIEW-RECEIPT
'''
(P/'COMPLETE_J2_INTERFACE_RECEIPT.md').write_text(receipt,'utf8');(P/'README.md').write_text('''# R17 J2单排8位可插拔接口 — 工程审查版

[完整回执](COMPLETE_J2_INTERFACE_RECEIPT.md) · [接口和配套选料](J2_CONNECTOR_AND_HARNESS_SPEC.md) · [针序和方向](J2_PINOUT_AND_KEYING.md) · [实际8针CSV](J2_ACTUAL_8PIN_HARNESS.csv) · [制造合同](FABRICATION_INPUT_CONTRACT.md) · [41项矩阵](MANUFACTURING_PREFLIGHT_MATRIX.csv)

Molex1718560008板端+22012087线端壳体；actual8孔/ROWCOL/warm+coldDRC四类0；其它175与主铜不变。准确端子按实际线径待定，未知现有线束兼容、全3D和制造未放行。原生genericdevice/3D保留，必须随[J2配套装配覆盖合同](J2_CONNECTOR_AND_HARNESS_SPEC.md)，不按genericcatalog选料。

![实际针序与2D外形](J2_PINOUT_AND_BODY.png)

![实际冷重开GUI](J2_COLD_NATIVE_GUI.png)

实际File SCIENCE_ADK5556_4X4_R21_J2_PLUGGABLE_REVIEW.epro2；完整eprj2源工程、实际550padnetCSV/176BOMCSV、warm/cold全source、DRC/资格/失败回执直接交付。原生body/孔参数以actualFile源确认，不冒称metadata自动BOM或3D全资格。publicSHAmanifest与ZIP另生成。厂家整PDF/全页PNG/大段extract本地存证不公开复刻，仅官方/镜像链接、边界短说明与SHA。
''','utf8');print('Complete review receipt and index prepared')
