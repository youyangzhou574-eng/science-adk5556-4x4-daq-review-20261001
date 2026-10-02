# Fresh-context whole-package final review

审查对象：CIRCUIT_C101_BANK_FIRST_FULL_PLACEMENT_CLOSEOUT_V1。审查日期：2026-10-03。按 executing-plans 的唯一整包终审执行；本审查独立于摆放实现。只读本包及 INPUT_SHA_REGISTER 明确列出的源文件，只写本文件。没有调用原摆放、审计或出图脚本，没有新增 candidate/placement/image，没有 CAD、solver、网络、Git 写入或子审查。

## 审查结论

**支持“50×50 mm 完整101件离线候选已生成，离线身份/几何门通过，可供工程及用户视觉审查”；不支持“全部 Pro 宏布局意图已无条件收口”或任何原生/布线/制造放行。**

Critical：0。Important：1（I1，J2 ROW 侧规划合同与实际冻结占位坐标不一致，尚需明确书面裁定）。Minor：1（M1，已披露的 detail 文字裁剪）。重要问题的处置可以是明确限定结论并保留待决工程门；本审查不授权也不要求消耗余量立即重排或重画。两图已满额且 STOP，应继续保持。

## 独立证据

没有仅凭 FULL_OFFLINE_AUDIT.json 的布尔值作结论。以 Python -B 的内存只读计算重新读取 JSON/CSV，使用独立的仿射变换重建 body 和 physical-pad-proxy，再做所有成对几何计算；未导入本包脚本。结果如下。

- BOM、identity、geometry、最终 JSON 与最终坐标 CSV：同一101个唯一 designator，CSV 坐标/角度逐项与 JSON 一致。
- 原始 actual-pin CSV、geometry pads、identity pin 集合、363审查CSV：363个唯一 ref/pin 完全对应；实际 net、expected net、geometry net 与 NC 一致。323 connected、40 NC、54 非空网络。
- 两次 attempt 的 stage 坐标分别独立检查全部5050对：body 交叠0、physical proxy交叠0、规划50×50框外0、所有 J1/J2/J3/J4 reserve 的非所属器件侵犯0。Attempt1 最小间距0.2000036 mm；最终 Attempt2 为0.2040031 mm，最小对 C_AVDD9_HF / R_ADC_RESET_PD。这里计算的是现有代理，非 courtyard/铜间距/native DRC。
- 两次 stage 数量都为4→21→39→48→54→84→101，顺序前缀一致。前4为接口，第5为U5，接下来16个明确bank电容全部在U2之前完成；最终 stage 坐标与交付坐标完全一致。16来自2+3+4+4+3；以明确designator纠正文字15是合理裁定，没有删件。
- bank CSV全16行独立核对角色、值、U5 pin、放置顺序及实际信号pad距离。REFIO两22µF分别4.003/4.599 mm；REFCAP 2.528→6.990/7.304 mm；AVDD9 1.746→3.006→7.854/9.002 mm；AVDD30 1.747→3.008→5.472/8.339 mm；DVDD34 1.400→6.850/7.060 mm。各角色层次距离单调；不将同一bulk层内部先后强加为距离顺序。
- ALL_FUNCTIONAL_172_SAME_NET_PROXY_EDGES.csv全部172行：端点实际同网、target登记集合、欧氏距离均独立相符，没有重复条目替代漏项。
- 四路 RF、CF 均按实际 OUT/IN−网络重新寻找各端pad，真实连接 COLi/TIAi；四RF两stub均3.470096 mm，四CF均5.663505 mm。四R_ADC两端分别连接TIA/U5，合计7.395152、10.863075、8.894476、7.951235 mm，均值8.775985、最大10.863075 mm，与报告一致。四C_ADC均是相应AIN/GND；到AIN距离1.398915、1.485204、2.844028、1.400695 mm。支持RF/CF基本重复和C_ADC成对摆放，不支持完整四路精确镜像。
- FIVE_DIGITAL_SERIES_INTERFACE_CHAINS.csv全部5链：MCU侧与接口侧分别在串阻不同pad、不同网，三段距离及含电阻跨度总值全部相符。没有把电阻两端混成同一网络。
- 审查进行中新增 FULL28_MAIN_CHAIN_ACTUAL_PIN_PROXY.csv 和 write_main_chain_readonly.py 已纳入同一次审查。28行的实际同网及距离全部重新核对通过。它是代表边表，不是全网布线；ROW部分只列J2至一个MUX支路，另一sense支路另由本审查计算。
- ROW0..3各有J2对应pin及U4两个同网pin；U1.1↔U4.8为ROW_DRV，U1.4↔U4.9为ROW_FB，U1.3为VEXC。driver和feedback直接stub为6.723968/4.648561 mm。电气静态关联完整，不能因此证明“贴着正确J2侧”和实际成对短铜线。
- INPUT_SHA_REGISTER七项副本与其明确源路径均实时重算SHA256，14个文件均与冻结SHA一致。
- EXECUTION_BUDGET事件求和等于spent：candidate1/placement2/image2/source0，其余登记活动0；现有包对应1份最终候选、2份attempt日志和2张PNG，STOP和coordinateSTOP均true。记录内部一致；不把本地日志当成对未记录外部活动的全局证明。
- 两PNG均已通过 view_image 实际查看。全图是完整101候选，detail是同一候选模拟区域，不是第二候选。实际绘图脚本读取同一个最终坐标文件，图中可见宏位置与CSV一致。

## Findings

### Critical

未发现本次离线交付范围内的 Critical 问题。

### Important — I1：J2 ROW侧合同与实际规划pin方向不一致，完成结论需要限定

位置：PRO_BANK_FIRST_RULING_FULL.md:129、138、144；C101_PHYSICAL_GEOMETRY.json:915起的J2块；P1_FULL_PLACEMENT.csv:90；COMPLETE_BANK_FIRST_RECEIPT.md:47。

批准文本认为J2上半部是ROW，并要求ROW宏贴着ROW侧。冻结几何却使最终J2 ROW0..3规划pad位于世界坐标x=6、y=25.5/26.5/27.5/28.5，下半部；COL0..3位于y=29.5/30.5/31.5/32.5，上半部。实际U4在(14,37.5)，U1在(21.5,37)，而TIA U2在(20,25.5)。因此ROW宏实际在COL侧上方，不能从静态网络完整推导“按正确ROW侧收口”。

独立计算J2 ROW0..3至U4 drive支路为11.938/11.637/11.451/11.386 mm，至另一sense支路为16.730/16.166/15.672/15.254 mm；同一ROW的两条直线代理相差约3.868–4.792 mm。没有授权的绝对长度阈值，也没有实际铜线，所以这些数值本身不是电气FAIL；但它们证明不能跳过J2方向/ROW贴侧这一工程合同差异。现有FFC机械HOLD是必要的，却没有明确交代这个已经存在于规划数据中的方向冲突及其宏布局影响。

影响：若“关键proxy收口/无需再重排”被带入native任务，可能把尚未解决的连接器方向假设和ROW摆放一起冻结。此项按工程交接影响列Important，而不是因缺少制造资格泛化阻断离线候选。

建议处置：执行者应在 receipt/disposition 明确写出这个矛盾及裁定，保留 J2 pin-side/ROW adjacency 的待决门；可以保留 OFFLINE_FULL101_REVIEW_READY 供评审，但不得等价于“全部宏布局意图通过”。若之后实际厂家datum证明规划方向不同，或要求恢复ROW贴侧，必须在新的明确授权范围中处理。不得在本轮余量内自行旋转J2、换针序、重排、重画，亦不得靠口头将上下方向解释为已机械验证。

### Minor — M1：detail范围外的designator文字未裁剪

位置：render_complete_layout.py:30；ADC_BANK_AND_TIA_DETAIL.png。

实际图上存在范围外R_SEL_PD1、R_RST等文字溢到边缘/标题附近。receipt已准确披露；全图、坐标及全量CSV仍可供审查。本轮只登记deferred minor，不建议生成第三张图，也不把它升级为工程几何失败。独立使用detail作为出版图不合适。

## Declined to judge

- 原生101 PCB、native DRC/ERC正文、真实铜线/过孔/回流/可布通性：本轮没有这些产物或授权，明确不以代理通过代替。
- J2厂家精确datum、BottomContact/FrontFlip实际安装方向、actuator与排线操作以及J1/J3/J4配套机械：仅保守占位与reserve可证，真实机械HOLD。I1的现有规划数据冲突已单独作为finding，没有因机械未定而忽略。
- Ceff、ESL/高频去耦、模拟稳定性、噪声、温区、故障与100fps/full-matrix性能：离线距离与静态身份不足以裁定，现有HOLD必须延续。
- 用户视觉满意、最终选型：用户尚未接受；两图已看不等于用户已认可。
- 52×50或50×52候选是否更优、全局最短/最佳布局：没有第二候选或最优性证明，不能裁定；预算上限不要求消费。
- 旧partial原始坐标的全部历史距离和外部批准来源：本次未扩展到历史包全量重审；比较CSV中的当前行已独立重算，旧行仅作包内记录。旧partial不成为新坐标seed的代码/数据证据支持现有声明。
- 公开GitHub固定commit、ZIP、manifest、匿名下载及隐私过滤的最终完成状态：不在本次电路包审查范围；receipt的发布要求不能替代这些交付的实际验证。

## 最终评定与推荐处置

离线完整候选、冻结身份、保守几何、bank-first层次、RF/CF与输入RC基本重复均有独立证据支持。无须因轻微图面缺陷重画，也没有必须为了预算再做P2的证据。继续 STOP。

**Ready for bounded offline review：Yes。无条件整体工程收口：No，先对I1作明确书面裁定与结论限缩。Native/routing/制造放行：No。**

本文件记录的是唯一fresh-context审查意见；执行者负责分级复核与最终disposition。没有要求再次派审，也没有授权本轮额外坐标或图像动作。
