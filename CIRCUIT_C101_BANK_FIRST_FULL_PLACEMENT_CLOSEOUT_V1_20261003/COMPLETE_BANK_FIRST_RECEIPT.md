# C101 bank-first full101 offline placement closeout

本轮已完成一个完整101件、50×50 mm离线摆放候选P1。不是原生PCB、布线、DRC或制造放行。USER_VISUAL_ACCEPTANCE=PENDING，CAD_RELEASED=false。无需为凑两个候选再做旧L方案或放宽板框。

终审重要限定：101/363/5050和16bank通过不等于全部宏布局意图通过。实际FFC占位ROW四pin在下半、COL在上半，而ROW宏在上方，存在J2_PIN_SIDE_ROW_ADJACENCY_HOLD。现候选供审查，ALL_MACRO_LAYOUT_INTENTS_ACCEPTED/NATIVE_PLACEMENT_ELIGIBLE=false，须统一工程裁定方向/邻近取舍。下文“关键代理收口”仅指已核几何代理，不能带入native作无条件接受。

## 授权、输入与计数

完整批准assistant0efc68cd-fbc6-47c7-89cb-8e2678c8d92f，parent188c6864-4406-40c2-8df8-15a723470c1f；300min，candidate≤2/placement≤4/image≤2/source0。唯一包CIRCUIT-C101-BANK-FIRST-FULL-PLACEMENT-CLOSEOUT-V1。开始22:12:46UTC，墙钟截止03:12:46UTC。旧07包、坐标、失败和额度保持历史，不迁移。

当前C101电气基线来自b1b4413d9aba4abfd9979833ae40a627547e7379的schematic+mandatoryaddendum+actualBOM/pin集合，由2a9裁定正式接受。101=36R44C7保护10IC4J，363信号pin/323connected/54nets/40NC。冻结输入来源、复制字节和SHA在INPUT_SHA_REGISTER；本轮7份全部源及副本SHA不变。没有使用旧P1/P2/B311世界坐标作seed；既有100器件实际封装几何+J2明确FFC保守placeholder复用。actualpin-map363逐pin复核。

Pro列出的五ADC bank实际2+3+4+4+3=16颗，文字“15”按明确designator纠正为16，没有删电容或增元件。REFIO两个22µF，无凭空新增100nF；REFCAP2.2µF+双22µF；AVDDpin9/30各100nF、2.2µF、双22µF；DVDDpin34为100nF+双22µF。

## 实际执行

Candidate1，placement2，image2；candidate2及placement3/4未消费，不是继续自主排版的授权。所有sources/CAD/session/save/export/SPICE/PCB/routing/via/pour/Gerber/采购制造bench/install/localGit/system0。本轮没有新工具、优化产品、安装、求解器或原生会话。

Attempt1从空白按接口→U5全16bank→四TIA/filter→ROW→REF→完整power→MCU实现101，5050body/proxy0。工程复核发现输入滤波摆放重复性偏弱，个别RF/CF代理没有缩短，使用已批第二次全局调整，不把第一次完整等于最终美观合格。

Attempt2为P1同一候选调整：ADCbank保留完整供电pin邻近优先级并在芯片reference/supply侧占地，U2移近并旋转180，按真实RF/CF两脚网络选0/180角，四C_ADC采用成对上下fanout，其他macro可随实际几何合法位移动。所有低优先级件在ADCbank后放；没有8.2mm硬搜索半径，有限近pin0.5mm网格+整板1mm后备格；这只是本包摆放实现，不是优化器研究。ATTEMPT1/2_EXECUTED_SCRIPT和stage进度保留第一次与第二次全部坐标、实际执行日志；无失败、无partial拼接。P1_FULL_PLACEMENT为第二次实际结果。

## 实际全量核查与候选门

- 101/101全部有坐标，全部physicalproxy位于50×50规划框。
- 全5050对body与physicalpadproxy交叠0，最小proxy间距0.2040031 mm。不是真实courtyard、routingclearance或nativeDRC。
- 363实际信号pin的number/net/NC与冻结actualCSV一致；323/54/40未改，BOM和SCH未改。
- J2/J1/J3/J4实际检查reserve无非所属件侵犯；图中阴影使用相同检查矩形。J2左出线占位，J1底边，J3/J4右边。
- 全16ADCcap齐，100nF先于2.2µF和bulk，U5+16一次完成后才允许U2及其余件。ADC16_BANK_PRIORITY_AND_PIN_DISTANCES列每颗实际signalpad→对应U5pin距离，所有bank按角色层次单调邻近。不是容量/高频回流/ESL资格。
- 四RF/CF2+2模板真实OUT/IN−pin/net关联，RF两leadstub各3.470096mm、CF各5.663505mm，四路同角色距离完全一致。C_ADC上下两对重复。R_ADC具体fanout因合法间距不同，不声称整条四channel精确mirror。
- ROW0..3的J2/MUX实际网络以及drive/sense相关pin完整静态关联；172登记同网引脚代理全列，五MCU→串阻→J3/J4功能链另列，未把串阻两侧不同网混为same-net。

唯一图P1_FULL_LAYOUT_REVIEW.png为全101，第二图ADC_BANK_AND_TIA_DETAIL.png为同一完整候选模拟细节。两图已实际查看；细节图有部分裁剪区外designator文字飘到边缘，不影响101原坐标/CSV/全图，图片额满不另出第三张；designator精读使用CSV。尚未取得用户视觉认可。左上/电源与模拟间有自然空白，不声称占满、均匀、全网最短或用户已满意。

## 同网几何代理比较

|实际版本|放齐|TIA→RADC→U5两stub均值/最大mm|RF/CF最大两stub mm|
|---|---:|---:|---:|
|旧07 P1 partial|89/101|11.4052/15.2677|6.1763|
|旧07 P2 partial|88/101|16.1584/19.4476|6.1763|
|当前P1-full|101/101|8.7760/10.8631|5.6635|

当前四TIA两stub实际7.3952/10.8631/8.8945/7.9512mm。均值/最大相对旧partialP1约−23.05%/−28.85%；只是相同定义的欧氏pin代理，包含R两端分别到芯片而不含铜蛇形/绕障，不能推误差、噪声、100fps或稳定性。RF/CF严格由实际脚网络核；不声称所有通道方向完全等价。BEFORE_AFTER_PARTIAL_VS_FULL_PROXY_COMPARISON保存准确值。

## 保留HOLD与下一步

J2为2005290081 8P1mmBottomContactFrontFlipZIF默认标准，14×7mm为明确inflated规划占位，旧KKbody没有用；2MP仍机械空网元数据，未实际做FFCfootprint。精确厂家datum/actuator/排线插拔/最终封装资格仍HOLD；J1/J3/J4具体配套连接器机械未知。ERC752count无正文、旧R2文字需addendum、Ceff、fullmatrix动态/精度/100fps/温区故障/容量/保护/bench制造都保留HOLD。原生旧176PCB没有改，不是现C101PCB。

按照获批规则，P1已101/5050/16bank/关键proxy收口，无明显反馈劣化，不启动条件P2或板框放宽；不是证明52mm备选无用。当前OFFLINE_FULL101_REVIEW_READY=true，仅供工程和用户视觉审查。所有坐标/图片活动已经STOP，等待接受/人选及完整新native范围；旧剩placement或墙钟不能用来擅自改CAD。

下一步先集中裁定实际J2方向/ROW邻近差异。可明确接收当前代理取舍待人选，或批准唯一120min局部方向收口（既有接口几何30、ROW宏调整30、全101复核30、一图交付30），sources0/candidate1/placement≤1/image≤1，CAD/原理图BOM/仿真/铜/采购制造bench0。只是正常报告内申请未批不执行，不借本轮剩额度。以后实际人选和方向门明确后，原生480min仅保留历史条件请求、不激活。不为字号/ERCcount或精确3D回工具研究，不无限回整体排版。

唯一whole-package fresh审查后结果和处置见FINAL_REVIEW/REVIEW_DISPOSITION。公开交付须逐文件可读、固定commit、manifest/完整ZIP、旧nonroot冻结及匿名SHA核。账户SQLite、私有native作者metadata、第三方整PDF/context不公开。

END-OF-COMPLETE-C101-BANK-FIRST-FULL101-OFFLINE-REVIEW-RECEIPT
