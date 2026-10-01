# 08号工程包完整阻断回执

**ACTUAL_PIN_NET_ERROR / BLOCKED_NOT_FOR_USE。本包未完成合格R2.1原理图。**

包：SCIENCE_ADK5556_4X4_R21_ENGINEERING_R21_NATIVE_AND_LIMITED_VALIDATION_V1。
消费裁定：CIRCUIT-PRO-R21-ENGINEERING-CONVERGENCE-AND-NATIVE-R21-20261002-08；assistant92351b17-2d28-4158-9959-c3d1ed8ea841，parent user b34fcafb-f81e-45bc-be18-f62b05e1ad9a。完整裁定原文随附。

本轮已回到工程目标，没有新增MIMO、descriptor、参考归一化、internal pole或证明工具研究。停止原因是我在最小ECO实施中引入的实际原生连接错误，符合08第十一节第7条；不是宏模型数值困难，也不是理论证书不足。旧科学失败保留历史，不改写旧07或冻结R2。

## 工程目标与已有有限结果

正常验收1–7kΩ、约10%变化可辨识；0.8–8kΩ是保护带。4×4、8线、VCM2.5V、VEXC2.25V、E0.25V、Rf4.99kΩ、Cf2.2nF、ADC0–5.12V、100fps保持。校准后平均误差≤1%、帧间重复性≤0.2%仍是待实体台架验证目标。

40组理想DC=10矩阵×4选行，输出160个单元结果。矩阵为全800/1k/3.3k/7k/8k、棋盘1k/7k、7k目标邻居1k、1k目标邻居7k、单点+10%、一行+10%。采用精确虚地、无线路电阻/输入偏置/钳位泄漏/ADC INL的静态计算，不能冒称宏模型或精度实测。

- ADC理想输入2.65567193–4.05896910V。
- TIA驱动最大4.37593397V，4.75V供电下理想余量0.37406603V；ROW驱动最低1.0V。
- 最大传感器电流312.5µA，800Ω单元理想功耗78.125µW；5.25V/99Ω泄放电阻功耗0.278409W。不是短路/热/反灌认证。
- +10%理想码差：1k约−1451.49码、3.3k约−439.85码、7k约−207.36码。7k→7.7k属于保护带，不能当正常精度端点。

六次真实ngspice47进程，原OPA4388/OPAx388模型字节复制、未编辑。4ROW+1TIA及1ROW+4TIA，各800/8000/高目标三模式。高目标为8000Ω目标/800Ω邻居，仍属保护带。VEXC正确2.25V，切换3µs，计划终点353µs，不做9.6ms整帧或长窗。每次包含一次blank OP与一次TRAN，无optran额外初始化。

六次blank OP有文件；六次TRAN均在名义180s终止门停止，实际含终止调度约180.144–180.168s。最后报告积分时刻166.493–277.467µs，完整trace0、300µs残余验收0。状态全部MACROMODEL_NUMERICAL_LIMIT，不能称动态PASS，也不能由此声称实体失稳。原始stdout/stderr及强制终止状态保留，未追加收敛研究或重跑。进度输出实际在stdout；本包监督器原stderr检查无效、lastIntegration字段null，且配置30s不符08要求15s，**15s积分停滞门未正确实现，属于执行控制偏差**。单独只读提取CSV纠正解释，原字段保留。180s壁钟门仍实际执行；没有额外科学运行来修此监督器。

协议代码和回归直接复制冻结coupled版本，21条基础+11条progress合计32条实际重放全部通过。没有重写状态机。8×1.2ms=9.6ms，288传输=32dummy+256有效，48时钟/传输；假设SPI2MHz，SPI6.912ms+八次300µs建立2.4ms=9.312ms，每状态36µs额外CS/开销余量，帧末0.4ms处理预算。仅算术可行，真实SPI/DMA/中断/WCET、100fps及硬件故障延迟未验证。

## 原生工程：先通过基线，后ECO失败

冻结R2文件、BOM、计划及引脚网表SHA未变。仅复制一份新的R2 .eprj2工作副本，经官方LCEDA CLI打开，得到新的独立工程UUID a8676ecc06b5399826a37ec617e3c862b83d70e446d12d7b9a2a7b02796fcd50。未打开修改旧工程、旧master或数据库，不重建168器件。

复制后的真实Protel2 File基线：168器件、6页、498/498连接、104网、36NC全部匹配。随后添加VCM/VEXC各4.99k/100p反馈、四个22p TIA电容，物理替换R_J3_5为真实1k器件，修四个C_ADC的Value、更新说明和端口文字。

22p实体库为muRata GRM1885C1H220JA01D，LCSC C77031，22pF±5%、50V、C0G、C0603；官方设备库原始File及两符号针/两封装焊盘核对随附。R_J3_5实际厂家型号0603WAF1001T5E、R0603、Value1k；四个ADC Value实际10nF X7R。字段/库身份局部正确不能代替电气连接通过；旧通用插针及全量供应链/HF容量证据限制保留。

ECO后的真实File全量审计：**176器件、514计划连接中334匹配，180不匹配；99实际网对106计划网；36NC仍一致。** 原生实体引脚/封装身份集合通过，但电气连接FAIL。原始失败网表、完整514针CSV、网络成员、页源码和失败前后捕获全部保留。没有把计划网表充当实际网表。

发现的具体实施问题：

1. C_TIA_HF0..3放在page3 y1320的四个旧器件位置，没有做占位核对。分别重叠C_TIA_OP、R_TIA_ISO0、D_TIA0、R_TIA_ISO1；新增端口/导线与旧端子坐标接触，GND/V5/TIA等网络合并。冻结位置和实际失败网络给出直接证据。这是我引入的排布错误，不是电路架构或实体器件失稳。
2. U3.2/U3.6目标VCM_FB/VEXC_FB实际仍落在VCM/VEXC。现有端口的setter调用未实现所需电气改名，实际File否定了计划。下一步只需按真实端口身份删除这两个旧端口、用已正常创建的官方NetPort接口重建同锚点端口并核查实际网表；不研究API原理或修改SDK。
3. 六页端口标签显式fontSize8设置后，实际PDF全部出现超大重叠文字，无法清晰阅读。六页已真实render并逐页看过，图面FAIL。下一步恢复冻结/default字号，适量调整文字位置并实际查看一次，不开发图面验证工具。

严格依08实际pin-net错误门停止：发现后没有修正、追加原生编辑/保存、第三轮参数、新的仿真或第二会话。仅只读解释既有失败、导出已失败状态的真实File/PDF、关闭唯一自有session并完整交付。冷重开及新ERC/DRC未执行；不能称冷重开PASS、DRC clean或图面PASS。

导出文件均明确BLOCKED_NOT_FOR_USE，**仅失败证据，禁止按此装配/制造/上电**：

- SCIENCE_ADK5556_4X4_R21_BLOCKED_NOT_FOR_USE.epro2：751329bytes，SHA F1BE33B9999984D41C5DEB4786BDF44C597B3E97788B1C815AECF1897A3D0933。
- SCIENCE_ADK5556_4X4_R21_BLOCKED_NOT_FOR_USE.pdf：667899bytes，SHA 8DD7F935A82C67EA2875EF159F2CC1FB2D5CE3B5297B9D9AD46B305039B84217。
- 编辑后的.eprj2工作文件同样只是失败副本。没有新合格R2.1工程，旧R2继续是冻结历史输入。

## 执行控制、预算及回执

480min未耗尽；因明确工程STOP结束技术执行，剩余额度不自动解除STOP。预扣实耗：OP/AC6/32、normalTRAN6/12、offline41/48（DC40+六日志一次解释）、protocol32/48、reset0/32、sources0/8、candidate0/2、library1/4、copy1/1、session1/2、save7/8、captureAudit3/4、PDF1/2、ERC/DRC0/2。PZ/MIMO/descriptor/full-long以及PCB/制造/采购/实际bench/本地Git/系统写全0。

save7含首个flat wire形状读取错误的预扣1，该错误在首次修改前发生，实际save调用6。实际pin-net审计2（基线与ECO后），第三capture为STOP后既有失败状态真实File/PDF取证。全部失败计数保留，不退款、不伪装冷重开。

打开新工作副本的旧Python收集器因继承stdout管道等待超过58s；只读session list/currentProject确证会话已创建及新副本身份，没有重复open。核路径/启动时间后只停止自有Python收集器83312，未终止EDA应用或科学求解器。仅本包CLI收集器改为文件输出及bounded wait，后续命令正常返回；没有平台/账户/执行器/安装/DB/cache/profile/system修改。承认该首次收集等待未达到预期CLI收集时限，不包装为全流程控制PASS。

唯一自有session a329d737-9586-42ac-96b4-499531e8b1ca官方closed；六个自有solver全部终态，没有pending native调用或本包求解器存活。

## 请求唯一下一工程包（未批准，不执行）

**这是用户明确提出的要求：在正常报告里申请更大的有界执行时间、次数和自主推进范围，减少小步骤反复请示。** 请集中裁定下一包R21_NATIVE_PIN_NET_CORRECTION_AND_FINAL_DRAWING_V1，240min：明确连接/位置/字号修正60min、真实全量网表及冷重开/关键元数据/图面90min、受控台架输入整理30min、完整交付60min。

申请工作副本1、session2、save6、capture/audit4、ERC/DRC1、PDF2；普通位置/标签/元数据修正可自主推进，以实际全量网络和冷重开同成员作为工程完成门。库/资料/候选新增加0。OP/AC/TRAN/PZ/MIMO/descriptor/full-long/reset解析/新协议回归均0，复用本包有限结果；不扩大模型平台额度、环境修复、补偿扫描、PCB/制造/采购/bench权限。

唯一修正路线限定为：迁移四个新TIA电容及其自有短线/端口到核过占位的空白行；重建U3.2/.6这两个端口到正确反馈网；恢复default字体并实际看图；514连接/106网/36NC全量核查、冷重开同网络、关键MPN/Value/Footprint、原生/PDF一次性交付。不得将此退回理论证书或工具研究。

BENCH_VALIDATION_PLAN.md仅准备了正常范围、10%变化、精度/建立/100fps和后续故障分列验收，未上电。本报告冻结时GitHub发布、发送及接续监控尚待执行；具体固定commit、owner、nextCheckAtUTC及发送/历史确认以 GITHUB_ENGINEERING_R21_DELIVERY_20261002 的送达生命周期账及简短交付正文为准。会在本回合用独立公开电路GitHub新目录、固定版本一次性交付完整报告、可读CSV/TXT/PNG、原始case/model/log和失败原生File，并建立接续监控。网页实际已读未验证，不虚报读取，也不附加ACK等待门。

END-OF-COMPLETE-R21-ENGINEERING-NATIVE-PIN-NET-BLOCKED-RECEIPT
