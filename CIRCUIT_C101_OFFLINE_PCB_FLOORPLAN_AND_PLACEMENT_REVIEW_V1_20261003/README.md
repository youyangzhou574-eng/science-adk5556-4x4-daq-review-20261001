# C101 离线两候选布局：完整阻断回执，非合格布局

已完整接收 2a9ac0f3-75b9-4f8c-9ab3-316418e46572 / parent b77ea843-d432-48f0-a33c-e005ff54f11a。Pro正式接受C101电气基线，接受对象是原理图+强制DRAWING_ANNOTATION_ADDENDUM+actual BOM/pin map配套集合；历史C101公开回执与SHA不回写。本轮只离线重新规划101件，CAD/native/PCB/仿真/制造bench均0。

## 本轮结果

| 项目 | P1 横向信号流 | P2 L形咬合 |
|---|---:|---:|
| 规划板框（未改原生） | 50×50mm | 50×50mm |
| 长宽比 | 1.000 | 1.000 |
| 实际已放入器件 | 89/101 | 88/101 |
| 尚未放入 | 12 | 13 |
| 部分器件两两检查分母 | 3916 | 3828 |
| 部分body/pad-proxy交叠 | 0/0 | 0/0 |
| 全101/5050对资格 | HOLD | HOLD |
| 合格候选/用户可选终稿 | 否 | 否 |

不是最终50mm板尺寸建议；完整电容位置尚未闭合，不能以部分计数冒称101全量几何PASS、较旧版已更优或用户满意。两个3000×2200 PNG均实际查看；不出第三图。主图明确PARTIAL、缺件清单和NOT native/routing。

P1缺件：C_AVDD9_HF、C_DIV、C_DVDD34A、C_DVDD34B、C_LDO_FF、C_LDO_IN、C_LDO_OUT、C_MCU_BULK、C_PWR、C_REFCAP_BULKA、C_REFCAP_BULKB、C_REFIO_B。P2同上另缺C_AVDD9B。没有删除、改DNP或用目标件数掩盖这些缺件。

## 实际输入/物理模型

冻结C101实际101身份/值/footprint/363pin/323connected/54net/40NC；已取得100件current export FOOTPRINT文档的component_shape及实际pad，逐number与SCH363pin映射，不能把SCH坐标当PCB尺寸。所有六个冻结输入原文件及本包复制SHA重新核一致。没有借旧B311坐标作seed，也没有打开任何EDA session。

J2的旧KK body明确排除。仅采用2005290081的8P/1mm/bottomcontact/frontflip/rightangle机械拓扑和显式14×7mm保守平面占位、规划焊尾/2个机械空网占位；厂家图纸之前已得，复用既有本地页图，不新增来源。A=13.2±0.2/C=11.6±0.2及约5.3深度作为既有参考，不宣称14×7是厂家max courtyard或准确actuator/pad-row datum。native仍旧KK metadata，未修native或替换精确footprint。FFC_MECHANICAL_HOLD保留。

J2左侧出线、操作保留区在所有已放件中无侵犯；当前保留区为工程规划，实际线材/翻盖/弯曲半径未测。J1/J3/J4用明确edge reserve；内部仍画既有电气封装代理，不能据此声称最终侧插座body/公母/装配/mating匹配。所有已放件proxy在规划板框内；完整最终机械和制造HOLD。

## 信号/反馈/去耦证据边界

RF/CF采用四角2+2角色模板，按U2 OUT/IN-实际pin映射登记；四通道反馈件全部在两个部分草稿中。矩形pad proxy与实体body跨全部已放件检查，没有按功能类过滤。channel模板是功能角色几何重复，不是每个pad精确镜像或可制造最优路径证明。

FUNCTIONAL_PIN_DISTANCE_PARTIAL.csv逐实际同网pin给Euclidean stub指标，包含R_ADC两端TIA/ADC和C_ADC信号端。PARTIAL_PLACEMENT_AUDIT.json列四feedback lead-stub sums及四ADC input/filter指标；这些是直线引脚代理，不是绕芯片/不同层/回流的实际走线长度，不声称全网最短或100fps/性能通过。缺件行明确UNPLACED。ground仅用于同owner IC最近ground引脚辅助评分，未做铜回流/高速电源完整资格。

没有合格101布局，故目前不给用户二选一，也不推荐某个部分草稿作为可执行native模板。横向P1仍是Pro优先的宏观方向，但需先完成全部必需电容及全101审查，不能凭漂亮轮廓放行。

## 全部失败及硬预算

初次脚本导入bundled Python因无shapely失败，未到candidate/placement预扣；随后使用机器已安装Python313的既有shapely/matplotlib，未安装新包/执行器。只读探针先遇语法/UTF8/emptyEND/FILL/POLYGON pad等记录类型差异，按实际导出显式处理、失败保留，不是工具/API理论研究。实际参数和所有旧工程未改。

第1次placement在D_DBG0目标设为J3外口时actual same-net guard失败；实际钳位在串阻内侧，已按MCU对应pin改正，初失败code/log保留且placement1计入。第2次在RF0合法性guard停止：4.7mm偏移的RF pad proxy与U2焊盘交叠；第三次统一角色模板偏移5.4mm。第3次P1依序摆至89件后C_AVDD9_HF在限定8.2mm局部邻域无合法位置，立即保留89件partial；没有移动这89件后重试。

第3次最初异常中断循环，P2原计划尚未开始；仅继续同一已预扣第3次中的未执行P2半段，P2 anchors/targets/template/lattice完全相同、无第四次调整、无P1重放或退款。P2摆到88件后C_AVDD9B局部搜索失败，也保留partial。两候选不拼接。这个有限失败不是数学不可行证明，不说明50mm全板无空间、必须删电容或C架构错误。

本地规划缺陷是顺序贪心和人为8.2mm局部邻域：部分低优先级器件/较大bulk先占据ADC附近空间，高频与剩余bulk不能闭合；不是EDA工具bug。应先为每组ADC reference/AVDD/DVDD全部HF+双bulk分配完整合法位置，再放较低优先级件/调整宏观位置，不能再盲目加一轮或修新的优化工具。本轮没有执行这个下一阶段建议。

实耗candidate2/2、placement3/3、image2/2，source0/0；全部CAD/session/save/export/SPICE/PCB/routing/via/pour/Gerber/制造采购bench/localGit/system=0。剩墙钟不改变三次坐标/两图硬额度。STOP=BOTH_PARTIAL_ADC_CAP_LOCAL_SPACE_FAILURE_THREE_PLACEMENT_TWO_IMAGE_QUOTAS_USED；禁止新坐标、第四轮、第三图或原生操作，仅最终审查、完整报告与一次正常交付。

## 状态与交付

C101_ELECTRICAL_BASELINE_ACCEPTED/C_SCHEMATIC_ACCEPTED_WITH_ADDENDUM/PCB_PLACEMENT_ELIGIBLE来自本次Pro新接收，均true；ALL101_PLACED/ALL5050_GEOMETRY_PASS/LAYOUT_REVIEW_READY/CAD_RELEASED仍false。USER_VISUAL_ACCEPTANCE=NOT_REQUESTED_INVALID_PARTIAL_CANDIDATES。ERC_DETAIL/LEGACY_ANNOTATION/FFC机械/Ceff/全矩阵动态/实际精度/100fps/bench/制造旧HOLD保留，不把这次布局失败回写电气基线或旧证据。

单次fresh最终审查及一次处置后，全自有source、完整actual101身份/net、几何、全部partial/失败、两图、指标CSV、预算、manifest和ZIP进入专用电路GitHub独立新目录固定commit。账户SQLite/私有上下文/第三方整PDF/作者字段不公开；引用的公开metadata-stripped输入epro2仍旧176PCB，不是本轮native输出，manifest明确排除并链接固定基线。一个短摘要集中Pro裁定下一最小有界收口；按用户明确更多有界预算要求同一正常报告申请，不另微问；每次送达有owner/nextCheck/接续monitor，不发完停住。

## 单次终审处置
# 单次最终审查处置
FINAL_REVIEW.md：未发现未披露Critical/Important，Minor1图例保留区精度。一次文档补充：图中接口虚线/阴影为示意；合法性检查矩形以保存源码reserves为准（J2外侧到−10mm，图显示到−8mm；J3/J4检查x44..60mm，而虚线以body中心示意），仍非厂家机械资格。不新增图、坐标或二审。
新增28条既有坐标只读same-net代表链比较（REPRESENTATIVE_ACTUAL_PIN_CHAIN_COMPARISON.csv），包括MCU→串R内/外→J双段，未把串阻外口当与MCU同网。CANDIDATE_COMPARISON.csv中P1 TIA→RADC→ADCpin lead-stub mean11.4052/max15.2677mm，P2 mean16.1584/max19.4476mm；RF/CF twoleadstub各5.8377..6.1763mm。仅直线代理、部分草稿，不据此宣布美观/整板胜者、最短铜或性能通过。这两CSV属自有只读交付核查，不声称finalreview再次评价它们。
继续BLOCKED_LAYOUT，全部坐标/图片硬额不继承，既有C101电气配套集接受不回写旧GATES；不得要求用户选择未放齐的P1/P2。

END-OF-COMPLETE-C101-OFFLINE-FLOORPLAN-PARTIAL-BLOCKED-RECEIPT
