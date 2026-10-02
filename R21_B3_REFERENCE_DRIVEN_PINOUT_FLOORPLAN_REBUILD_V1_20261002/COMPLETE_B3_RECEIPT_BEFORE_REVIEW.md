# B3 reference-driven pinout floorplan — 完整审查草案与阻断回执

包：SCIENCE_ADK5556_4X4_R21_B3_REFERENCE_DRIVEN_PINOUT_FLOORPLAN_REBUILD_V1。
绑定完整裁定assistant7c32a7c3-e1bf-43f0-81b2-b0e749476769、parentuser087b5fa4-1953-44c0-8b2f-b19b7f542088。该裁定回应用户真实类似板案例要求，替代较早300min B3及已取消B23。完整原文PRO_B3_RULING_FULL.md。用户连续普通技术执行授权内实施，未另向网页追问小步骤。

## 结果和真实门

完整176件离线位置已生成，19个主IC/接口的位置或旋转均与B22不同，旧坐标没有作为构造种子。三张图实际查看，所有源、输入、失败日志、完整坐标、552pin、106关键距离及六区刚体复用证据随包交付。

本包是PARTIAL/BLOCKED审查草案，不是用户已满意或合格placement：U3与U14保守焊盘代理有一处相交；全器件body无交叠，但不能用body0替代physicalproxy1。因此B3_GEOMETRY_PASS=false、CAD_RELEASED=false、USER_VISUAL_ACCEPTANCE=false。最大原生尺寸、板框、铜、布线、原生DRC、温冷、实物性能均未实施/未通过。本包三轮位置和三张最终图额度满，禁止第四轮/第四图/新CAD。

科学停止：B3_MACRO_PAD_PROXY_COLLISION_AND_PLACEMENT_IMAGE_QUOTAS_USED。剩余360min墙钟不解除次数门。本板原理图、MPN、值、footprint、padnet及J2实际映射均未编辑；本包只写新的离线坐标，并非新原生文件。旧native项目未打开覆盖，旧SQLite不公开。

## 真实参考案例

独立核实5个TI原始文档及ADI CN0175网页，登记六官方URL、下载字节与SHA。ADS8684第58页图101、TIPD167第32页实板top/bottom布局已在本地render并查看；有Symbol字体告警，实际图完整可见。完整第三方PDF/HTML及其private页面只留sources_local_only，公开原创短说明REFERENCE_CASE_RULES.md/登记/URL。

直接适用：ADS8684自己的analog/ref/digital针群、OPAx388短反馈与去耦、TMUX1134真实交错通道。TIPD167/CN0175仅借鉴短参考/输入和重复通道；六层或不同ADC/参考的电路值、性能、层数不迁移。TIDA01214仅核实相近ADS8688A隔离模块/设计文件入口，没有下载其全Altium/坐标，不能称已资格其全部placement。网页引用占位没有当成已获取source；广告或同类图片没有当成厂家图纸。

裁定中的简化示意图经实际pin核实纠正：U4 S/D/SEL交错，不存在整边S整边D。U5实际数字端1/2/36–38与模拟端16/18/21/23，180°时analog向左，digital向右，REF5–7位于上长边。U7 SPI11–14在原右边，180°后朝ADC；UART/SWD与J3/J4相应靠右可接近边。图上的箭头是原理图关联，不是已走铜。

## 构造而非旧块搬运

两个新macro由实际芯片pin/接口朝向直接定义，不加载旧B22坐标。A给ROW/MUX、ADC/Bias更多局部空间，B更紧。MACRO_A/B.json保存19位置/真实连接长度/碰撞，MACRO_SELECTION.json选择A。身份/几何输入来自同一冻结ACTUAL_GEOMETRY，使用其中旧绝对坐标仅为消除footprint捕获原点得到局部pad/body，未用来生成新宏观/旧块相对布局。旧B22只在独立比较/复用audit/render中读取。

构造顺序：U1/U2四路22p HF回路、U3两HF优先；ADC参考核心后排pin9/30/34供电电容；按真实IC pin约束生成剩余局部lane，最后同信号分支保护/分压/数字接口件。每元件从已指定对应IC实际pin附近0.5mm有限网格及四rotation枚举，保守代理与所有已经放置对象>=0.18mm，106登记距离不得增长。它是本包有限pin-neighbor生成脚本，不是工具安装/全局自动布局产品/制造可布线保证。

完整通道拓扑另外核查RF/CF八件确实各接TIA_i tap与COL_i，是通过ISO/SENSE支路的功能回路，不虚标为运放output/input直接同网；22p HF才直接跨运放输出/感测两pin。U1/U2重复通道按实际2+2 pin facing展开，并不承诺四个channel cell的所有相对几何严格相同。本版有方向/局部重复关系，但完整channel一致性/跨区飞线交叉尚未量化验收，仍人工工程审查，不能说比旧版所有视觉指标更好。

## 本地实施错误及停止

第一轮在pin距离评分发生tuple减tuple TypeError，完整日志和失败code保留。真实计入placement1，即使没有完整结果；没有回填取消。
第二轮先排较大REFIO，有限局部候选让REFCAP无合法位置。保存部分实际坐标与完整trace，计入placement2；不声称数学不可行。第三轮以REFCAP优先及明确pin-cluster站位完成176件，计入placement3。不追加第四轮。

最终全量audit才发现U3/U14代理相交。更早MACRO_A.json实际上已经记录这对collision，选择脚本仍选择A，完整构造只对后加入passive做collision过滤，没有拒绝初始macro冲突。此为本地宏观准入遗漏，不是厂家pinout错误、软件bug、物理失稳或无法排板。该偏差明示，未事后删除macro记录、放宽包络或改坐标。后续如批准最小修正，必须先检查全部宏观anchor代理再接收；本包不能靠文档宣称修好了。

## 全量证据

176refs、552pads、514assignedpins、107非空nets、36ordinaryNC、2J2机械空网保持。输出ALL_552_PIN_MAP_B3.csv逐针；实际pad-number/net来自冻结源，位置是离线变换，不native捕获。J2.1–4ROW0..3、5–8COL0..3、MP1/MP2空网，不改为GND。其他身份原始源SHA冻结，通过INPUT_MANIFEST逐项核验。shape/padnet身份digest在audit登记；MPN/value实物未重新验证，本包从未写它们。

全15400distinctrefpairs：body交叠0，physicalproxy相交1（U3/U14）；最小physicalgap0。代理由真实body加真实pad形状保守矩形包络，不是nativeDRC、mask、courtyard或厂家最大机械。176自然bodybbox83.9003192×58.3210984mm，宽高比约1.4386。旧B22约71×63.5mm，面积和方正程度未改善，不能以“19锚点变了”代替用户美观认可。板框未定义，不假称83.9×58.3新板尺寸。

106关键距离=94继承+12追加（10IC/passive组合），全项不增长，最大delta=-0.0610762475mm。每项actualnet与association保存，不只报告一个总PASS。这个只证明已登记直线pad距离的局部约束，不保证回流、可布线、传输噪声、所有未登记节点或实体精度。

六大区旧刚体复用：按对应designator有限SO(2)拟合下界，再用任意rigid inliers必要条件 |old pair distance-new pair distance|<=1mm的0–1上界计算，六次均最优终态。其上界覆盖任意旋转/平移，不把离散角拟合当全局最优。各区上界match比例：TIA3/26=11.54%、ROW4/18=22.22%、ADC4/25=16%、BIAS_MUX5/29=17.24%、POWER4/46=8.70%、DIGITAL3/31=9.68%，全部<=70%。完整refs/下界/上界/求解状态保存。这里只做批准的审计，不用于生成布局/新优化器研究。

J2有限规划空域无其他代理相交。精确actuator/bodydatum/真实线材厚度接触面匹配仍HOLD，本包没有借独立规划矩形虚报机械制造资格。J3/J4在图右侧，但线缆/手操作三维尚未资格。

追加同坐标只读代表信号边比较：31条明确选出的真实同网pin→pin边（四TIA经ISO/ADC RC、四SPI、四ROW经ISO到J2、3电源边），总直线距离463.176281→295.831580mm。但ROW0到J2+9.448902mm、ROW3到J2+16.468014mm、J1输入到U9+6.466409mm增长，逐边保留。此是指定子集，未包括全部Bias/control/debug/地/供电分布，未算全ratsnest交叉或布线，不能称全网或性能全面改善。局部106key距离PASS没有覆盖这些外部链增长。

## 图面说明

B22_vs_B3.png同mm尺度显示每版自然body-min重定原点，不是共同板框；B3_NO_COPPER.png含实际所有body/padproxy和一处红色HOLD；B3_PINOUT_AND_SIGNAL_FLOW.png含实际信号链和三个真实pin inset。三图已查看。图上没有制造铜或silkscreen，英文designator是分析标注。U5 inset少数高密pin-label相叠，小阻容标注及主图顶部标题有可读性限制，以ALL_552_PIN_MAP_B3.csv/PIN_FUNCTION_GRAPH.csv作可读附件，不虚报图上全部针名可单独看清。3/3图硬满，不再重画。

## 执行预算/终审/交付

批准360min，自14:16:40UTC起，截止20:16:40UTC。实际macro2/2、placement3/3、finalimage3/3。CAD/GUI/EDA_API/native/routing/outline/仿真/Gerber/制造采购bench上电/本地Git/system均0。只读audit/render内部import又执行了一次同坐标audit，日志明示，没有新增placement/image；最初fitz三张官方源页渲染尝试因模块不存在失败，改既有pdftoppm实际渲染并查看两张private源页，不安装执行器，不扩系统权限。第三方selectedsource页为研究查看非本板finalimage。

唯一fresh终审和处置将在FINAL_REVIEW.md/REVIEW_DISPOSITION.md登记；所有Critical/Important若需第四次位置或图修正，本包保留HOLD而不超额修复。不要为收口再开验证工具/API研究。

完整own源/可读附件直接上传专用电路仓库新目录，ZIP仅辅助。公开sourcebulk/accountDB排除并登记SHA，凭据/其他项目数据不混入。固定commit/公开匿名SHA核验/发送精确正文/回执/历史确认与owner+nextCheck在交付目录保存。只发一次摘要，不重复旧报告、不以额外网页逐附件ACK作门。

## 集中请求下一阶段

这是按用户明确要求在正常报告中申请更多适合项目的有界执行时间/次数/自主范围，非扩大模型平台额度：建议仅180min B3_MACRO_COLLISION_AND_VISUAL_ACCEPTANCE_CLOSURE（确认当前方向及限制30、U3/U14小局部修正40、完整audit及图40、交付70），最多2局部coordinatepasses、1对比图，CAD/原生/布线/板框/仿真/新资料/安装/制造采购bench0。优先修真实collision，不将小label问题当主线硬门，不重做整板/理论体系。176身份/全部pin-net/J2映射冻结，106距离须继续不增长、宏观全部19proxy先检。

当前只是请求，未批准不执行。请同时按这三图裁定：新的pin方向/通道形态是否响应用户要求；方正整体和空白仍不足是否需要具体有限macro修改。用户尚未选B3，不代选，不以复用PASS替代美观，也不预先启动旧条件原生480min。

END-OF-COMPLETE-R21-B3-REFERENCE-DRIVEN-PINOUT-FLOORPLAN-COLLISION-BLOCKED-RECEIPT
FINAL-GITHUB-COMPLETE-DELIVERY
