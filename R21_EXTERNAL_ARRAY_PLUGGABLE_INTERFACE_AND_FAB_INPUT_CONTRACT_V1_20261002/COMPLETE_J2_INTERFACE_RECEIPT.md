# R17 J2 可插拔接口ECO与制造输入合同 — 工程审查版

用户要求“单排8针线、插槽插拔、不是焊8根线”。本包已把J2从通用裸排针的实际封装改为 **Molex1718560008板端 +22012087/22-01-2087线端壳体** 的准确8位2.54mm竖直摩擦锁方案。真实原生8孔、body/lock/courtyard/pin1与温冷针网复核通过；原生ROW/COL文字丝印要求未闭合，J2_ECO_CONFORMANCE_HOLD。准确端子MPN/线束/制造工艺/完整3D仍未放行。不是采购、制造或上电结果。

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

实际File SCIENCE_ADK5556_4X4_R21_J2_PLUGGABLE_REVIEW.epro2，773916bytes，SHA256 **801149F292E86CF34AB2872F177125099D640421B48B62F3F9044EF2151DB241**。不把eprj2或脚本计划当actualFile。源码/8孔文件原文、实际全部550CSV、工程BOM176CSV、warm/colddrclog、图面PNG、所有失败与来源hash均直接提供。

## 预算和停止状态

批准180min，start 2026-10-02T03:23:28.606658+00:00，本阶段记录 2026-10-02T04:42:36.204633+00:00，当前elapsed 79.13min（公开交付最终时另更新）。copy1/1、session2/2、save2/2（实例apply1+一次finalSaveAll1）、captureaudit3/3（baseline/warm/cold+File）、DRC2/3、export1/1、officialSources4/4、candidate1/2、normalPour1、J2onlyImport1。部分J2workingobservations与source尺寸checks另列，不假称只有3次工具读取。P0/P1/P2/P3的45/30/45/60作为计划分配，未把长期拖延重置总180min；有限实施失败/途径在ledger保留，未另开API/工具研究。

两officialsessionsclosed、freshownGUI空、solver0。新仿真/MIMO/descriptor/全板重布/Gerber/采购/制造/bench/上电/localGit/system均0。原生阶段已终结，不因DRC1/candidate1剩余自启CAD，当前只读合同/终审/交付。

## 终审要求差距与下一阶段请求（用户明确要求更多有界工作预算）

一次fresh-context终审发现Important：17号要求原生丝印1/ROW0或三角+ROW/COL名称，actualFile只有J2/三角、无ROW/COL文字。GUIpadnet和配套图不能冒称制板文字。当前三硬额度save/audit/export满，不再CAD；回执一次文档修复明确J2_ECO_CONFORMANCE_HOLD、PCB_REVIEW_READY=false（15/16基线接受保留不回写），电气/真实封装温冷资格PASS。Mandatory8针图/CSV明确方向，可审查但独立接口conformance需Pro接受偏差或补字。

用户明确要求在正常报告同时申请适合项目的执行时间、次数和自主范围，以减少反复请示。请求唯一下一包 **R21_J2_SILK_CONFORMANCE_AND_ASSEMBLY_INPUT_CLOSURE_V1** 最多180min：有限knownGUI丝印/metadata30、温冷45、成套输入合同45、交付60。优先请Pro接受现有mandatory针序图/选料覆盖，让工程主线前行；仅若要求原生补字，条件copy1/session2/save2/captureaudit3/DRC3/export1，范围仅J2附近非铜层1/ROW0及ROW0–3/COL0–3短丝印，禁止改铜/孔/网/位置/值/规则、Import、库/新候选、API研究。Normalpour0，主电路仿真/采购/制造/bench/Gerber全部0。ordinary文件核对和可操作现有UI实现自主累计；失败保留companion，不把工具研究作为门。实际AWG/fab输入到后可读合同核对official新增资料<=4/terminal候选<=2，无输入就保存清单等待用户，不能循环重做。

只是请求，未批准不执行；不扩平台或账户额度，不自用旧剩量。继续保持J2_ECO_CONFORMANCE_HOLD、J2_EXACT_TERMINAL_PENDING、J2_GENERIC_DEVICE_METADATA_HOLD/J2_3D_NOT_QUALIFIED、FAB_INPUT_PENDING、MANUFACTURING_NOT_RELEASED、BENCH_NOT_RELEASED及历史科学/性能HOLD。readablecompanion强制随原生，独立自动制造文件未放行。

END-OF-COMPLETE-R21-J2-PLUGGABLE-INTERFACE-AND-FAB-INPUT-CONTRACT-REVIEW-RECEIPT
