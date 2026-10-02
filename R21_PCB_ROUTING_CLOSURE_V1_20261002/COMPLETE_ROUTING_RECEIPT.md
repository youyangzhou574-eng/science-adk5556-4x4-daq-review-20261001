# R2.1 PCB 布线审查阻断回执

Package: SCIENCE_ADK5556_4X4_R21_PCB_ROUTING_CLOSURE_V1

结论：完成本轮原生布线实施和保存，尚未取得最终有效原生 DRC / 完整冷重开审计；**PCB_REVIEW_READY=false，MANUFACTURING_NOT_RELEASED，BENCH_NOT_RELEASED**。不要把最后一次有效 DRC 的 8 个未连接条目说成已经清零。后续 15 段电源桥接及实际重新覆铜已实施，但最后一次核验调用失败。本回执不是制板、装配或上电许可。

## 授权与冻结范围

完整 12 号裁定见 PRO_ROUTING_CLOSURE_RULING_FULL.md。批准 360 min，session3/save12/captureaudit4/DRC4/reviewExport2。用户明确要求 Computer Use；本包使用已存在的嘉立创原生编辑器 GUI 完成实际铜区重建、保存和画布查看。通信仍只走内部 read_thread/send_message_to_thread。没有浏览器沟通、其他项目、原理图修改、Import Changes、全板 autoroute、仿真、Gerber、采购、制造、bench 或本地 Git 写入。

冻结 100×90 mm 四层，176 器件、550 焊盘、514 已赋网、107 网、36 NC；器件值/器件和封装身份、J2 行列、J3/J4 sense 接口不改变。新独立工作副本 SCIENCE_ADK5556_4X4_R21_ROUTING_CLOSURE_WORK.eprj2；最终审查 File 为 SCIENCE_ADK5556_4X4_R21_PCB_ROUTED_REVIEW.epro2。

## 实际实施

P0：32 个选定局部模拟路径，4 个 HF 电容旋转 180°并重建对应感测/反馈短路径，12 个明确模拟/分压/ADC 取样层间连接。P0 原生 DRC 为 381 Connection 条目，没有其他错误类别。

P1：63 个选定普通信号网的显式走线、局部 dogleg 和必要层切换。六个既有离散器件微移：C_U14(65,40.5 mm)，C_U13(68,40.5)，U11_CT_C(75,75.5)，U12_CT_C(82,72)，R_SEL_PD1(49.5,35)，U9_OV_B2(18,85.5)，均在原有功能区域；其网名/身份保持。没有调用整板 autorouter。局部候选仅对工程选择的引脚出口/连接对进行有限几何筛查，失败方案保留，筛查不是原生 DRC 的替代。

P2：供电主干 16/20 mil、局部 12 mil，受 IC 引脚出口限制的短颈 6 mil；过孔 hole12/diameter24 mil。L2(layer15)全板 GND；L3(layer16) V3V3 优先于 V5；L1 增加 GND guard/return 覆铜，保留 L2 连续地、不划分 AGND/DGND。三轮 GUI 铜区管理器实际 Rebuild All 并保存。首次电源铺铜被 V5 优先级覆盖，V3V3 未形成；调整实际优先级后四个 POUR 均有原生 POURED。

首次实际覆铜 DRC：83 = Connection72 + Clearance11。11 个 Hole-to-Hole0 是同网同坐标重复过孔，已删除重复图元、保留各自一个真实孔。局部 ROW_SEL0/HW_ENABLE/VCM 出口调整，补齐 MCU_ROW0、ROW_SEL3、U12_CT、V5_IN 及指定供电/GND 引脚，19 个新 via 和 62 段新线，供电可放宽处按实际外国网几何筛查放宽。第二轮覆铜后第三次原生 DRC：**8 Connection，Short0、Clearance0、NetlistError0**，详见 TARGETED_DRC.json；V5 两个、V3V3 六个对象仍未连接。

最后针对 C_ADCA2-1 / U11_TOP0-1 / C_MCU1-1 / U10_BLEED-1 / U10_PG_T-1 / U10-6 铜区接入，操作创建15段12/20 mil供电桥和1个过孔，最终原生source相对warm净增17个LINE图元；15桥均可对应created IDs，另外两条L1/6mil/0.1mil的VCM与TIA1短线来源未独立确认，不推断自动分段，再一次实际重建和保存。该阶段之后没有有效原生 DRC，不能声称电气闭合通过。

## 最终文件和可读证据

真实 sys_FileManager.getProjectFile 返回 File，经 arrayBuffer 得 810028 bytes epro2，SHA256 **5603E205FCB5170DE00A125DCD7A6271665D78BED153E4B6B489ABEAF8F8FB6E**；不是本地自行构造的原生文件。包含最终保存 PCB 的实际文档。最终铜：**909 LINE，296 VIA，4 POUR/4 POURED**；L1 689 段、L4(layer2)135、L3(layer16)85、L2(layer15)0 信号线。

WARM_CAPTURE.json 的第三次成功实际审计保持 176/550/514/107/36，ALL_550_PAD_NET_IDENTITY.csv 逐焊盘和开始版本赋网一致；ALL_176_COMPONENT_IDENTITY.csv 器件核心字典一致，允许的坐标/旋转变化单列。这次 warm capture 在最终 15 段供电桥之前，后续操作仅铜图元，不把 warm 检查说成最后的完整 cold 检查。最终原生 PCB 文档从真实 File 读取到 FINAL_PCB_DOCUMENT_FROM_NATIVE_FILE.txt；ACTUAL_ROUTED_SEGMENTS.csv / ACTUAL_VIAS.csv 来自该最终文档。

七张 FINAL_* PNG 来自最终原生 copper/source 与 warm 实际焊盘几何，属一次只读离线审查导出；不是进度计划图或生产 Gerber。原生filled path的ARC按目标约8°采样用于显示/几何检查，实际最大9.997384°，源数据完整保留。L2 GND filled 几何为单一连通多边形、无信号轨穿越、约8386.25 mm²；这是静态地平面几何审查，不能替代最终电气 DRC、回流电感或实物可靠性。V3V3 有3个 filled几何块，L1GND有15个；其层间接入仍须最终原生检查，不以局部岛数独自判短路或通过。

模拟局部图已实际查看：ROW/TIA核心反馈/感测保持局部L1，明确取样/分压连接含层间过渡，完整实际走线和过孔 CSV供审查。保留 CRITICAL_ANALOG_FINAL_ACCEPTANCE_HOLD；未测寄生、噪声、串扰、真实精度、300µs/WCET/100fps。旧容量/动态/故障/台架各 HOLD不变。丝印和机械最终质量未放行。

最终 File 中176 COMPONENT /550 PAD_NET /529 ATTR /16 RULE的完整body与图元ID多重集合和第三次成功warm来源完全一致；这支持最后供电桥阶段没有改器件/焊盘赋网/规则。上一同步包46个冻结源文件SHA逐项保持，见FROZEN_INPUT_AND_FINAL_SOURCE_CHECK.json。该文件核对不冒充失败的cold实际getter审计。

图面文字纠正：FINAL_ANALOG_DETAIL.png标题中的“arcs sampled <=8 degrees”不准确，实际采样按max(4,int(abs(angle)/8))计算，2838个ARC中2571个步长>8°，最大9.997384°。以上PNG须与REVIEW_DRAWING_ADDENDUM.md一起阅读；此处只修正文档/可读CSV，保留已用2/2导出批次，不做第三次图面导出。最终native原始ARC完整未改；不把显示采样当原生电气边界精度。

## 失败、预算偏差及冷重开

1. P1 原始大脚本在 Windows命令行长度上限前启动失败（WinError206），native0；失败 save预扣保留，按既有计划分为较小批次，没有调查SDK/数据库。
2. 局部线路修改曾报告 isAsync 等错误，但已产生部分真实变更。先用已知图元ID及选定网 source 对账，不盲重放已成功动作。11重复孔/两段旧ROW_SEL0铜已删除；HW_ENABLE返回新分段ID，遗留同网stub明确删掉；VCM三段桥只对尚未变化者重建。APPLY_TARGETED_* / RECONCILE_TARGETED* / READ_TARGETED_ROUTES保留失败与实际状态。没有把错误返回说成native0或完整失败。
3. **save10 预扣参数写法错误**，PowerShell顺序仍执行实际 save成功；随后按真实时间追加 conservative debit。这是一次执行控制偏差，不回填预扣时间、不减少实耗；没有超过12保存额度。所有后续预扣与操作分开调用。
4. session3官方冷打开成功，但首次 cold capture返回 `Cannot read properties of null (reading 'map')`；第四次 DRC返回“指定的主题消息在对应的画布内没有相关订阅”。二者均无有效核验数据，失败次数保留。随后只读GUI观察见项目树而没有PCB页签，双击PCB1后实际画布可见。这支持调用发生于画布尚未准备好的解释，**没有用该解释追认核验PASS，也没有继续修工具或增加第五次核查**。
5. 三个自有session均官方closed，结果见CLOSE_ROUTING_1/2/3；closed ID不复用，无本包求解器。关闭后的窗口视图变化只属只读观察，不继续编辑/保存。

最终 conservative实耗：session3/3；save12/12（11成功显式保存+1前启动失败预扣）；captureaudit4/4（3成功+1失败）；DRC4/4（3成功+1失败）；reviewExport2/2（1原生File+1最终离线PNG批次）。未用满360min不解除硬次数门。STOP=NATIVE_HARD_QUOTAS_USED_FINAL_COLD_AUDIT_AND_DRC_NOT_COMPLETED。禁止新的本包CAD写入、核查或开session；仅交付和回复监控。

## 下一步集中申请（用户明确要求更大有界预算）

用户明确提出“下次正常报告同时申请更多执行时间/次数/自主范围，减少反复请示”。本次只申请唯一 **R21_PCB_FINAL_READONLY_VERIFICATION_V1**，120min（画布准备及审查30/温冷原生核验45/证据交付45）；copy0，session≤2，save0，captureaudit≤4，DRC≤4，reviewExport≤1。原理图/Import/布线修改/器件值/库/仿真/理论研究/制造采购bench均0。

每个session先在GUI实际打开PCB1并确认原生画布及正确工作副本，再消耗有界实际核查次数，不靠时间睡眠当准备证据。仅一次 warm和一次独立cold核对176/550/514/107/36、同网络/器件/最终铜及原生DRC；失败记录而不展开工具研究。需要改铜或发现真实电气错误则STOP并集中报告，不用只读预算改板。若有效最终DRC为0且cold一致，再给PCB_REVIEW_READY；否则给具体未过门。只是申请，尚未获批，不执行。

END-OF-COMPLETE-R21-PCB-ROUTING-FINAL-VERIFICATION-BLOCKED-RECEIPT
