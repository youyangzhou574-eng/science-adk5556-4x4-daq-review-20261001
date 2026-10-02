# B2 whole-package fresh-context final review

审查时间：2026-10-02 11:57 UTC。对象仅为 `SCIENCE_ADK5556_4X4_DAQ_REPLICA/R21_PLACEMENT_B2_INTERLOCKING_V1`。按 executing-plans 的一次整包终审执行；本审查只读输入、源代码、冻结结果并实际查看两张PNG，仅新增本文件。未运行任何 placement、几何求交/距离重算、图片生成、CAD、API研究、GUI、仿真、Git或新代理。

结论：可按 `B2_OFFLINE_PLACEMENT_READY_FOR_USER_VISUAL_SELECTION_WITH_LIMITS` 交用户视觉选择。Critical 0，Important 0，Minor 2。此结论不代表用户已经认可规整度，也不放行原生PCB、布线、DRC、制造或上电。GATES 中 CAD_RELEASED=false、USER_SELECTION_REQUIRED=true 等限制应保持。

## Findings

### Critical：无

未发现冻结器件缺失、关键小块拆散、网络被改写、碰撞检查按组豁免、失败证据被丢弃，或把离线结果当作制造放行的阻断问题。

### Important：无

本次不以旧23阶段的STOP重新阻断离线排布。完整 `PRO_B2_RULING_FULL.md` 明确允许在完整FFC翻盖扫掠HOLD下做离线方案；报告与GATES保留了这一边界。无需补CAD、3D扫掠、理论或新一轮布局来获得本阶段视觉选择资格。

### Minor 1：自由件数量初始文案为54，实录为53

初始审查读取的 `COMPLETE_B2_RECEIPT.md` 及 `finalize_receipt.py` 报告模板写“普通件54个”。`GREEDY_CANDIDATE_TRACE.csv` 和 `PLACEMENT_B2.json.greedyTrace` 均为53；14个多器件刚体合计119件，加4个接口锚点，共123件骨架，余53件。全部176身份与坐标完整，因此只是统计文案错误，不是漏件。执行者已收到此项并在同一文档修订中处理；应同步模板避免后续再次生成旧数字。无需重跑布局或追加审查。

### Minor 2：占用热图对末端截断单元使用了等距显示

`build_b2.py:109–114` 用ceil尺寸建立网格，末端单元被bbox截断；`render_b2.py:40` 用imshow把所有单元等距铺满真实bbox。当前宽71.0000204 mm会生成72列，故占用图的显示格宽并非逐格严格1 mm，红框和黑白格的定位存在轻微偏差。主器件图保持真实比例，266 mm²来自完整1 mm空单元的表内算法，未被imshow重算；此项不改变碰撞或距离记录。占用图应视为示意，不据它量取制造间距。2/2图额度已用完，本阶段记录为延期的显示细节，不要求重绘。

## 已核对的证据

1. **输入与完整性。** 直接读取本包冻结ACTUAL_GEOMETRY、CONSTRAINT_BLOCKS及CSV/JSON，得到176个源器件、176个membership、176行B2 CSV、176个B2 positions；身份集合差异0，CSV与JSON的X/Y/角度差异0。源pads共552，其中514有网、107个非空网络、38空网；J2有1–8及MP1/MP2，电气脚1–4对应ROW0–3、5–8对应COL0–3，两个MP为空。七个输入的当前SHA256全部与INPUT_SHA_MANIFEST一致。值/封装/网络沿用冻结源，输出只是位姿表；没有新原生工程。

2. **94 pair及真实网关联。** 旧表74项，加U9/U10各输入/输出电容4项，加RF0–3/CF0–3各两端16项，共94。对每行重新读取源器件的指定pad核对net，并核对关键两器件属于同一刚体，错误0。78个direct项确为同网；16个functional项经对应R_TIA_ISO或R_COL_SENSE的实际两端网络联接，不能称直接同网。FUNCTIONAL_SERIES_PAIR_NET_AUDIT的16条与此结构一致。距离值采用既有运行记录，最大变化6.21725e-15 mm；本审查未重算几何距离。

3. **刚体保持。** 完整membership包含TIA 26、ROW 18、REFERENCE 23、ADC 25、MCU 2、POWER5/POWER3/LDO各3、MUX/U13/U14/U15各2、U11/U12各4，以及单件组。`putgroup`对组内全部中心及角度施加同一刚体变换，pad变换使用同一原点/旋转差，没有缩放或单独挪动受约束成员。RIGID_BLOCK_AUDIT逐块覆盖全部中心组合，记录最大误差7.10543e-15 mm。它证明冻结局部关系保持，不证明这些原始距离本身具有电气性能资格。

4. **全不同器件对。** 静态检查 `build_b2.py:26–31,81–83`：位置完整性断言后，body字典和physical字典都以完整器件集合构建；双层循环遍历排序列表的所有i<j，无groups或同块豁免，分别对176×175/2=15,400对做交叠面积检查。PLACEMENT_B2_PASS_2/PLACEMENT_B2及结构验证记录两类结果均为空。这里依据实际结果记录与完整循环源代码交叉确认，没有在终审重放求交。阈值为面积>1e-8 mm²，结论限于该数值模型。

5. **body与physical不同。** body取冻结native轮廓/J2规划外形；physical为body与pad的并集，圆角/椭圆pad使用保守矩形代理。检查不等于原生DRC、最小爬电/装配间距、厂家最大courtyard。0.20 mm只用于自由件候选的buffer政策，骨架只要求不交叠；报告对此没有扩大承诺。71.0×63.5 mm是自然body bbox，不是完整机械包络或制造板尺寸。

6. **FFC裁定。** 冻结J2 bodyLocalPolygons给出13.4×5.8 mm已有保守规划外形，bodyStatus明确不是精确body trace。采用该值而非将13.2 nominal当最大宽度的Ruling合理；13.4×5.8及自定义插入/开启2D区域均未获得manufacturer full-sweep资格。当前physical与规划keepout的零交叠记录仅支持离线放置；exact actuator HOLD仍有效，但按新完整回复不阻止本次交图。

7. **有界实现与失败保留。** 源码先放14刚体/4接口，随后有限1 mm候选、四旋转、单遍贪心；candidate上限152，实际trace最大135，53个自由件。cost包括新增bbox、aspect、host距离、局部间隙proxy及同功能对齐，无大功能区矩形约束、全局优化器或AutoLayout。它是Pro有限填缝方法的有界实现；没有实现额外局部交换，报告已明示，最多3轮并非必须用满。PASS_1保留C_DVDD34B与C_MUX的1.918386872896 mm² physical碰撞；修正表仅把MUX改为[45,57,90]，第二轮最终结果通过。预算记录2/3布局、2/2图；未见本阶段需要继续消耗额度的理由。

8. **实际图像及目标诚实性。** 已用view_image查看2880×1800的B2图与3600×1800的旧B对比图。两幅比较面板使用相同x/y范围和equal aspect，主要器件/焊盘按实际轮廓画出，无六大区框代替器件。FFC左侧锚点、右侧接口、上沿MUX与数据一致。B2确实更紧凑，但左上仍有长带空白，重复小块纹理仍明显；不能宣称已达到用户“完整规整矩形云团”的满意标准。body占用由12.9741%到18.1578%，宽高比由1.0398到1.1181、CV由0.38788到0.41665，后两项并未更好。报告清楚披露CV较差及506/266空白算法不同，未给伪精确改善百分比；这一表述诚实。缩小bbox本身不构成最终视觉验收。

## 审查边界与交付处置

本审查接受源代码、冻结表与已保存运行证据的一致性；没有重新取得厂家机械资格，没有验证实际布线稳定性、串扰、精度、接口配合或可制造性。未重新打开旧native工程或未冻结membership，也未访问网络。当前合理下一步是把同一B2交给用户选择，并保持后续原生阶段的授权门；不用为了通过终审追加优化或工具研究。

本文件即唯一whole-package fresh-context终审。无Critical/Important修复要求；Minor按上列处置，不再要求第二位reviewer或新审查轮次。
