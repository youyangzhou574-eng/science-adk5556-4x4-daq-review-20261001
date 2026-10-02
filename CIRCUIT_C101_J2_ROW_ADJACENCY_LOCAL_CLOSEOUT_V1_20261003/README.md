# C101 J2/ROW adjacency local closeout — complete offline candidate

120min唯一局部包已完成一次有目的调整与一张完整101件图。101/363/5050及全部八条ROW代理相对门通过。按77a4c655明确条件，OFFLINE_FULL101_REVIEW_READY/ALL_MACRO_LAYOUT_INTENTS_ACCEPTED/NATIVE_PLACEMENT_ELIGIBLE=true，J2_PIN_SIDE_ROW_ADJACENCY_HOLD=false。NATIVE_PLACEMENT_ELIGIBLE只表示可作为下一原生placement输入；CAD/原生PCB/routing/实际性能/制造bench均没有放行或执行。用户视觉仍PENDING。

## 唯一授权与输入

完整assistant77a4c655-5e03-4530-8ad4-3f503b76d18c，parentcca236e8-4ec5-4ff2-ba1d-9b24b20ab49c。包CIRCUIT-C101-J2-ROW-ADJACENCY-LOCAL-CLOSEOUT-V1，120min，source0/candidate1/placement≤1/image≤1。7源/副本SHA不变，当前完整101 P1来自固定055c73356a4d124ccd58867c7206d6b0353daf5e，不再空白整板重排，不使用旧partial。旧08预算/STOP/Important记录不回写；本包依据新的具体方向授权。

仅允许ROW七件U4/U1/C_MUX/C_ROW_OP/R_SEL_PD0/R_SEL_PD1/R_ENABLE_PD及必要RD_TOP/RD_B1/C_DIV三件伴随。实际10件改变，TEN_ALLOWED_COMPONENT_CHANGES逐一给before/after，其他91件坐标/角度完全相同；身份/MPN/值/footprint/pin/net均保持。J2方向/针序、U2/U5/全部16ADCcap/RF_CF/RADC_CADC/power/U6/U7/J1/J3/J4及50×50全部冻结。

## 一次实际局部调整

不是运行顺序贪心或新优化器。先依据既有包实物封装代理、J2 keepout x≤8与U2左侧x15.675的窄通道做目的性手工局部坐标计划，然后预扣candidate1/placement1，在apply_single_row_macro中执行一份固定literal，没有第二次调整/枚举生成候选/退款或整版replay。

U4从(14,37.5,0°)到(11.735,20.5,90°)，位于已冻结ROW/COL分界29mm的ROW侧；U1从(21.5,37,0°)到(11.735,26.1,0°)，靠U4common OUT/FB侧。不是转J2或交换ROW/COL。J2.1–4仍worldx6/y25.5..28.5、.5–8仍y29.5..32.5。七件与三分压伴随位置全部保存在CSV，没有改料值或输入GPIO协议。

## 实际六项门与代理比较

101/101全部在50×50规划框。全5050 body/padproxy碰撞0，最小physicalproxy间距0.2024041mm，所有非owner接口reserve侵犯0。7冻结input源及copySHA一致，363actualpin/323connected/54net/40NC不变。GND/NC未“凑数”。J2机械空MP只是原规划元数据，不假称原生新footprint。

|ROW|drive before→after mm|sense before→after mm|两支路绝对差before→after mm|
|---|---:|---:|---:|
|0|11.93805→10.10884|16.72993→6.04447|4.79188→4.06437|
|1|11.63689→10.30497|16.16610→6.36706|4.52921→3.93791|
|2|11.45104→10.51006|15.67176→6.69390|4.22072→3.81616|
|3|11.38616→10.72357|15.25368→7.02439|3.86752→3.69919|

全部8条对应距离更短，全部4差值缩小；这是布局指标，不是扫描建立或性能PASS。U1.1↔U4.8 ROW_DRV 6.72397→2.88358mm，U1.4↔U4.9 ROW_FB 4.64856→4.59734mm。除Pro明示8条nonincrease门外，桌面保守地也检查driver/feedback两proxy不增，两者均满足；这不是新增电气绝对mm阈值。

冻结34件模拟核心（U2/U5/8RF_CF/8RC_ADC/16bank）位置逐一相同，四TIA→RADC→U5两stub7.39515/10.86307/8.89448/7.95123mm、mean/max8.77598/10.86307完全继承；四RF3.470096/四CF5.663505mm不变。不是再优化或新AC/TRAN。

### 必须披露的伴随路径和机械余量

RD_TOP/RD_B1/C_DIV依据明确伴随许可随U1靠ROW侧。高阻分压点到U1：RD_TOP的VEXC端1.38745→1.44403mm，RD_B1端1.64364→1.33685mm，C_DIV端1.16295→2.45558mm；U6 VCM→RD_TOP源端1.49054→14.18149mm增长12.69095mm。完整ALL172/VEX_DIVIDER_COMPANION_EDGES_BEFORE_AFTER公开，不假称所有路径都缩短。U6固定且U1移到ROW侧时，分压点靠U1把较长连接留在VCM源侧；这只是允许的局部布局取舍，实际回流/压降/耦合/稳定性/铜线均未资格，需要native routing时关注，不推性能PASS。

U4到保守J2操作区边界的最小非owner reserve gap仅0.0073087mm，physicalproxy对器件的最小gap仍≥.2024mm。只证明本轮规定的无侵犯，不证明厂家真实courtyard、翻盖/线厚/mating裕量。这一很小规划余量在图/报告显式保留；精确J2/最终J1J3J4机械HOLD继续，native应按实际封装再核，不能直接称制造机械PASS。

## 图与预算、失败来源

唯一P1_ROW_LOCAL_FULL101_REVIEW.png 3000×2200已经实际查看，101全图、明确画出J2 ROW下/COL上，阴影使用同一检查矩形，无第二图/detail重画。上左因旧ROW宏搬下而更空，仍未声称全板均匀/已人选/最佳美观。

实耗candidate1/1 placement1/1 image1/1 source0，其余CAD/session/save/export/SCH/BOM/SPICE/PCB/routing/copper/via/pour/Gerber/采购制造bench/install/system/localGit全0。坐标后STOP，只留已批一图；出唯一图后完整stickySTOP，不能重跑已有源码。

首次绘图脚本else4.8语法错误发生在Python解析阶段，尚未进入image预扣或生成图；IMAGE_PREPARSE_FAILED_SOURCE.py及ONE_IMAGE_EXECUTION.log保留，修正空白后唯一绘图实际image1，无坐标/科学重跑、没有退款/第二图。普通本地文法修正，不是EDA/API/优化器研究。

最终JSON原复制了baseline的attempt2/stages/order/oldCoordinatesUsed字段，现明确改名inheritedBaseline_*，localAttempt=1，acceptedFullP1CoordinatesUsedAsExplicitLocalInput=true，oldPartialCoordinatesUsed=false；原JSON留LOCAL_FINAL_PRE_METADATA_CLARIFICATION。METADATA_ONLY_CLARIFICATION_SHA证实坐标canonical与唯一PNG字节不变；来源元数据澄清，不是第二次布局。

唯一whole-package fresh review结果与一次处置见FINAL_REVIEW/REVIEW_DISPOSITION，不追加二审。最终交付通过新目录固定commit、逐文件自有可读源+manifest/ZIP、旧nonroot冻结、8匿名SHA核，生命周期账owner+nextCheck+monitor同回合接续。

## 保留门与接续

当前局部6门支持解除规划J2/ROW方向HOLD并接受宏意图；旧08GATES/历史I1仍冻结。NATIVE_PLACEMENT_ELIGIBLE只表示离线坐标输入资格，CAD_RELEASED/PCB_ROUTING_RELEASED=false，实际FFC datum/footprint/actuator、J1J3J4配套、ERCdetail/旧备注addendum、Ceff、精度/100fps/fullmatrix、温区故障/bench制造HOLD继续。原生旧176PCB没有改，用户还未真实选本图，不代答。

按用户更多有界预算要求，在同一正常报告保留仅人选后条件下一480min原生接续请求：实际机械/101新PCB合同60、搬件60、布线220、温冷核80、交付60；source≤2/candidate1/copy2/session4/save10/import2/audit6/DRC8/pour2/export1/image3。必须真实FFCfootprint/全101与363signal+2MP实际PCB匹配，旧176铜不得默认为C101合格；小reserve余量/较长VCM路径必须检查而不工具研究。未人选未完整统一native/routing范围就不执行，不另微预算；Gerber/采购制造bench/install/system/localGit仍0。若Pro仅接收待视觉选择则保存状态关monitor等，不再重做此包。

账户SQLite、私有作者native、context/第三方整PDF未复制或公开，本轮native导出0。

END-OF-COMPLETE-C101-J2-ROW-LOCAL-FULL101-OFFLINE-CLOSEOUT-RECEIPT
