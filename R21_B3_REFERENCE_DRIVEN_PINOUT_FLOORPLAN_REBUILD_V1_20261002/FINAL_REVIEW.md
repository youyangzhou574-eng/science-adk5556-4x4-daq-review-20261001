# B3 唯一一次 fresh final engineering review

审查日期：2026-10-02。审查对象为本目录完整交付草案；依据完整 `PRO_B3_RULING_FULL.md`、绑定 assistant `7c32a7c3-e1bf-43f0-81b2-b0e749476769` / parent `087b5fa4-1953-44c0-8b2f-b19b7f542088` 及 `PLAN_AND_LEDGER.md`。本次是最终独立审查，不执行修复，不进行第二轮复审。

## 判定

**HOLD / PARTIAL：真实的新 pin-driven 离线构造已成立，合格 PCB placement 和用户要求的完整方正构图尚未成立。**

这份结果不能归类为旧六块整体搬运或仅重新排列无源件：新宏观位置与旋转直接写在 `build_b3.py`，19 个 IC/接口锚点改变，局部位置从实际 pin anchor 与登记距离生成，构造函数没有读取 `PLACEMENT_B22`。冻结几何文件内旧绝对坐标用于消除 footprint 捕获原点和转换局部焊盘，属于几何恢复；旧块坐标另外用于比较和复用审计。六区任意刚体匹配的必要条件上界均远低于 70%，支持“没有沿用旧大块刚体形状”的判断。

但“未复用旧块”不等于“已经完成真正可接受的 floorplan”。U3/U14 的保守物理代理相交、候选评分存在未披露的遗漏、完整 channel cell 与宏观构图验收不齐全，因此不批准进入 CAD、布线、制造或实验阶段。`GATES.json` 与回执目前正确保持 `GEOMETRY_PASS=false`、`PCB_REVIEW_READY=false`、`CAD_RELEASED=false`、`USER_VISUAL_ACCEPTANCE=false`。

## 审查方法与确认事实

仅阅读包内 Markdown、JSON、CSV、日志和脚本；查看既有三张 PCB PNG；对包内冻结输入及本地来源文件做字节数/SHA256核对；只用现有 `pdftotext` 读取本地来源正文到标准输出。未执行构造、macro 初始化、render、acquire、audit 模块 import、MILP、几何碰撞重算或关键距离重算。`render_b3.py` 会 import `audit_b3.py` 并产生文件写入，因此本次没有执行或导入它。唯一新增文件为本终审。

确认的交付一致性：

| 项目 | 本次只读核对结果 |
|---|---|
| 器件/位置/body register | 均为 176；位置 CSV 无重复 designator |
| 焊盘/赋网/不同非空网 | 552 / 514 / 107；逐个 ref.pad 的 CSV net 与冻结几何一致 |
| 空网 | 36 ordinary NC + 2 J2 mechanical；MP1/MP2 仍为空网 |
| J2 | 1–4 = ROW0–3；5–8 = COL0–3；未将机械焊盘改为 GND |
| 关键距离 | 106 行 = 94 继承 + 12 追加；CSV 无失败，最大 delta = -0.061076247522160454 mm |
| 原始输入 | `INPUT_MANIFEST.json` 八项包内文件 SHA256 全部相符 |
| 官方来源 | 六个登记文件 bytes/SHA 全部相符；五个 TI PDF + 一个 ADI HTML 实际存在 |
| 拓扑 | RF0–3/CF0–3 八件的冻结 pad nets 与 `CHANNEL_TOPOLOGY_AUDIT.json` 一致：TIA_i tap ↔ COL_i |
| 几何记录 | 保存的全量审计明确记录 body collision 0、physical proxy collision 1，碰撞对 U14/U3；日志与 gates 一致 |
| 次数 | ledger 为 macro 2/2、placement 3/3、images 3/3；CAD/native/routing/outline/simulation 均为 0；状态已关闭 |
| 补充信号边 | 审查过程中 owner 提供的 31 条明确选择同网边 CSV/JSON 已纳入本次阅读；未改变坐标或图 |

106 项只证明已登记 pad 到 pad 的直线距离满足旧上限。90 项标为 same-net 的关联与 16 项 RF/CF 功能支路关联在表中区分；后者不是运放 pin 与 RF/CF pad 的直接同网连接。全部通过不能推导未登记连接、真实反馈回路、回流路径、噪声或可布线性均已通过。

保存的六区复用结果如下。读过 `audit_core.py` / `audit_b3.py`：有限 SO(2) 拟合仅为下界；上界来自任意 0.5 mm inlier 所必须满足的成对距离变化不超过 1 mm 条件，故不限于离散旋转候选。六个求解状态均为 0、`globalUpperBoundValid=true`。本次没有重跑求解器。

| family | 总数 | 任意刚体匹配上界 | 比例 |
|---|---:|---:|---:|
| TIA | 26 | 3 | 11.54% |
| ROW | 18 | 4 | 22.22% |
| ADC | 25 | 4 | 16.00% |
| BIAS_MUX | 29 | 5 | 17.24% |
| POWER | 46 | 4 | 8.70% |
| DIGITAL | 31 | 3 | 9.68% |

六区合计 175，另有独立 J2 interface 1 件；没有把 176 件错误重复分组。继承的细粒度 membership 经明确 family 映射归并，不是把 membership 数量直接当六大区数量。

## Findings：按交付实际影响分级

### Critical：0

本包明确是阻断草案，没有原生 PCB、铜或制造放行。现有证据不支持认定已经造成不可逆制造、电气或数据破坏。以下问题仍须阻断下一阶段，不能因 Critical 为 0 而称通过。

### Important I-01：初始 macro 碰撞被记录却未阻止选择与构造

证据：`MACRO_A.json` 已记录 U3/U14，`MACRO_B.json` 的 macro collision 为 0；`build_b3.py:23–25` 仍无条件选择 A，`construct()` 将全部 macro anchors 直接加入 `placedshape`，只在后续无源件加入时检查间距。最终 `FULL_GEOMETRY_AND_IDENTITY_AUDIT.json` 仍记录同一对 physical proxy 相交。其根因不是后来无源件挤进去，而是宏观准入漏检；B 的宏观零碰撞也不等于其完整 176 件可行或其他指标合格。

实际影响：全局物理代理无碰撞硬门失败；body=0 不能覆盖 pad proxy=1。回执已如实披露，红色图注与 gate 一致，披露并未消除问题。

处置：**HOLD，现额度内不改坐标。** 将来另获有界授权时，应先验证全部 19 个 anchors 的保守代理，再接受 macro；修后仍须保留 176 身份/全部 pin-net/J2 映射和 106 距离约束。本审查不预先批准该修正。

### Important I-02：同网候选评分只计最后一个 pad，未完整执行注释中的 pin matching cost

证据：`build_b3.py:101–105` 的 `if pps: match += ...` 与 `for p in G[r]['pads']` 同级，因此循环结束后只使用最后一次 `p` / `pps`。多 pad 元件其余 pad 的同网距离不进入该项评分。实际例子 `U9_EN_R` 的 pad 顺序为 2=U9_EN、1=V5_IN；评分只留下最后的 V5_IN，遗漏 U9_EN 到 U9 对应 pin 的该项成本。其 `anchor()` 仍能看到匹配网络，故不是完全无 pin 依据；但 anchor 的平均位置不能替代逐 pad 候选朝向成本。

实际影响：生成器对多连接无源件的候选排序不完整，尤其未登记关键距离的供电/控制支路不能由“全-key bound”获得补偿。现有 106 距离记录和冻结 identity 不因此失效，也不能据此推定所有受影响连接实际变差。**这是本次新增的未披露代码缺陷，而非已验证的性能失效。**

处置：**HOLD / 记录待授权修正。** 本次不改脚本后重新运行，不以无输出的代码修补宣称已修复生成结果。后续范围至少应区分已有坐标可继续保留的证据与需要重新生成/验收的受影响器件。

### Important I-03：完整重复通道和方正宏观构图尚无可接受的闭环证据

证据：`MACRO_SELECTION.json` 主要以 A 比 B 留出局部空间选择 A；没有按裁定优先级提供完整局部反馈/去耦、四路链、channel repeatability 与跨区交叉的可核验比较。`preferred()` 是逐元件的 pin anchor + 径向偏好，完整 channel cell 的成员相对关系不是统一模板约束。回执已承认四个完整 channel cell 一致性/跨区飞线交叉未量化。

图面效果：U1/U2 的实际 2+2 朝向、U5 analog 向 TIA / digital 向 MCU、U3→U4→U1 以及底部电源流的方向可辨认；这说明重建有实质变化。与此同时，电源仍呈三个局部簇加独立 J1，中央空白较大，supervisor/support 与相邻电源形成不均匀占位。现有图不能证明用户期望的整板有序矩形 composition 已满足。自然 body 包络 83.9003192 × 58.3210984 mm 只是所有 body 的 bbox；更宽或低面积都不是该审美/工程目标的替代验收。

本次审查期间补充的 `REPRESENTATIVE_SIGNAL_EDGE_COMPARISON.csv` / `REPRESENTATIVE_SIGNAL_METRICS.json` 记录 31 条明确选定的实际 same-net 边。保存值总和从 463.17628098424944 mm 降到 295.8315798409529 mm，包含 TIA/ADC/SPI 连接缩短，也明确保留三条变长：ROW0 的 R_ISO0→J2 +9.448901505514772 mm、ROW3 的 R_ISO3→J2 +16.468013670144803 mm、V5_IN 的 J1→U9 +6.4664089768567 mm。这提供了真实且混合的系统链权衡证据，补充了早先只有方向示意的不足；仍不是全 ratsnest、crossings、route length 或可布线性验收，也不是“全部信号链更好”。本次仅阅读保存数据，不重算它们。

实际影响：不得把“19 anchors changed”或六区复用 PASS 宣称为用户已认可的新 floorplan；不得称方正程度优于旧图。此项是交付需求仍未完成的证据缺口，不以个人审美作最终拒绝标准。

处置：**HOLD / USER_VISUAL_ACCEPTANCE=false。** 当前额度已满，保留现有三图供用户裁定方向与具体不足。后续授权如只修碰撞，也不能自动关闭此项。

### Minor M-01：TMUX1134 来源文档编号写错

`REFERENCE_CASE_RULES.md:11` 写 `SCPS213B`，本地已登记的 S5 PDF 实际首页为 **SCDS412B，June 2019 / revised January 2024**，9.4.2 图 9-5 为 TMUX1134 layout example。官方 URL、SHA 和实际器件家族正确，交错 S/D/SEL 的解释未因此被推翻；应在文档处置中更正文档编号，不需新来源或新坐标。

### Minor M-02：标题与 U5 inset 可读性限制

现有 `B3_NO_COPPER.png` 顶部标题贴边且部分字形被裁；`B3_PINOUT_AND_SIGNAL_FLOW.png` 的 U5 高密度 pin/net 标签重叠，不能只靠 inset 独立审清每个数字/模拟 pin。主图小阻容标签也需放大才能辨识。U2/U4 inset 的方向与分组仍可辨，完整 CSV 可逐针核查；问题影响审阅效率，并非本包主要碰撞门或身份错误。

处置：文档说明与 CSV 兜底，现有 3/3 image quota 下**不重画第四张**。后续获图面额度时再改善。

## 来源与适用边界

已读取本地 ADS8684 p57–58、TIPD167 p31–32、OPAx388 p26、TMUX1134 正文 layout 部分、TIDA-01214 正文相关家族标记，以及 ADI CN0175 HTML 的对应段落。正文支持 short feedback/decoupling、analog/digital 分区、重复通道和参考邻近这些规则；TIDA 正文确实包含 ADS8688A，不因首页资源表也列 ADS8688 就判为错误来源。没有把裁定内 chatgpt citation/image placeholders 当已获取证据。

S1/U5、S4/OPA 家族与 S5/U4 的规则较直接；TIPD167、TIDA 和 CN0175 为不同板/不同器件系统的有限借鉴。包内已经声明不迁移六层叠层、参考电路值、性能、完整 Altium 坐标。TIDA 的全部元件 placement 未被资格；本审查也未打开或下载其外部设计文件。第三方 PDF/HTML 和 private source-page PNG 仍只存在 `sources_local_only`，本审查没有公开复制它们。

## Declined to judge

- **原生 DRC、真实 pad/mask/courtyard clearance、可布线性、回流与噪声：**没有原生 PCB/铜/板框，代理碰撞与直线距离不足以验证这些性质。
- **厂家最大机械、FFC actuator/mating/cable 操作以及 J3/J4 三维可接近性：**native component-shape 和规划 cable rectangle 不等于厂家机械资格；保留 HOLD。
- **四路完整 channel 几何一致性与全 ratsnest crossing 优劣：**没有相应验收数据，本次不新增坐标/科学检查；仅判断既有图和算法不足以证明通过。
- **最终美观、Science 感以及方正优于 B22：**这是用户尚未接受的结果，bbox 比例、复用审计和个人观察不能替用户作批准。
- **制造、温漂、动态响应、bench/性能：**没有本阶段相应实验或仿真证据。
- **公开仓库、匿名下载 SHA、最终交付消息与 successor monitor 是否完成：**本次范围仅本地目录，未对外查询或写入；需由交付 owner 的独立回执证明。

## 最终处置要求

本次 fresh review 已结束：Critical 0、Important 3、Minor 2。**继续交付只能称“完整证据的 PARTIAL/BLOCKED 审查草案”，不能称合格 PCB placement。** 当前不得新增 macro/coordinate pass、图片、科学 rerun、来源、CAD、安装或 Git 写操作。owner 可在既有允许的文档处置中承认 I-02、纠正 M-01、记录其余 HOLD；不应将文字处置计为解决 I-01/I-02/I-03，也不得以剩余墙钟时间解除已满次数门。
