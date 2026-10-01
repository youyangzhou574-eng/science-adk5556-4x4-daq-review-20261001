# CIRCUIT-PRO-R21-COUPLED-BLOCKED-ACCEPT-MIMO-CLOSURE-20261001-05

**项目：`SCIENCE_ADK5556_4X4_DAQ_REPLICA`**

我已按固定 commit `a3e22772f368322dd9de671ab816c09e3b7f1b72` 阅读本次完整阻断回执以及返回比、静态耦合、暂态、RESET、协议回归、预算审计等核心证据。

## 一、统一裁定

**接受本包停止原生推进的决定；接受已经取得的方法验证、局部动态和软件契约结果。**

当前不是重新设计架构，而是最后一轮**耦合稳定性闭合**。

这次最重要的进展有四个：

- 之前完整耦合测试台确实存在 **90 kΩ / 10 kΩ 分压写反**的问题，导致旧模型实际 VEXC≈0.25 V。冻结原理图真实连接是10 kΩ上臂、90 kΩ下臂，即 **2.25 V**。因此旧三次耦合卡死**不能继续作为目标电路不稳定的证据**。
- 原来的 `-V(fb)/V(minus)` 单注入 PM 数值退出正式验收。Tian 双注入与独立 Y-port 方法已经高度一致：Row/VCM/VEXC约 **8.20 MHz / 99.23°**，TIA约 **6.68 MHz / 101.32°**。我接受 `RETURN_RATIO_METHOD_VALIDATED`。
- 单TIA和4宏模型局部暂态结果支持现有补偿候选，但两个关键 **7宏模型分区暂态仍没有真正跑过300 µs有效窗口**。
- progress watchdog及最终32项软件回归，可以接受为 `FAULT_LATENCY_LOGIC_CONTRACT_PASS`，但明确仍是**软件/时序契约**，不是MCU实测WCET或实体故障延迟。

`P0 39/32` 的7例超额我记录为**预算分类执行偏差**。已取得科学数据不因此作废，也不追认成旧预算合法扩张；你们后续增加“多属性原子预检”的修复是正确的。

---

# 二、当前几个门的正式状态

| 门 | 本次裁定 |
|---|---|
| `RETURN_RATIO_METHOD_VALIDATED` | **PASS** |
| `FAULT_LATENCY_LOGIC_CONTRACT_PASS` | **PASS，限离线合同范围** |
| 单TIA 22 pF筛查 | **PASS，局部模型范围** |
| 4宏模型关键暂态 | **PASS，局部范围** |
| `PARTITIONED_COUPLED_DYNAMIC_PASS` | **HOLD** |
| `FULL_STATIC_COUPLED_NO_INSTABILITY_EVIDENCE` | **HOLD** |
| `RESET_DIRECT_PATH_PASS` | **25°C scoped PASS / 温度与故障域HOLD** |
| R2.1原生进入门 | **尚未开启** |
| Bench/PCB/制造 | **全部未放行** |

另外，静态AC里已经得到的9个5 V标称组合，接受其**有限DC工作点存在、没有这些工作点削顶**的结论；不能用普通输入到输出AC曲线本身证明不存在RHP极点。

---

# 三、7宏模型的唯一闭合路线

这次不再继续盲目加仿真时间，也不再扫第三轮补偿值。

## 第一步：把暂态切换事件移到仿真起点附近

当前7宏模型网表中，ROW切换发生在：

\[
t=100\ \mu s
\]

而已经跑到：

- `4row+1TIA`：375.633 µs；
- `1row+4TIA`：287.162 µs。

这意味着第一种实际上只取得了约 **275.6 µs的切换后数据**，第二种约187.2 µs。

下一包统一改成：

**先由ngspice求真正pre-switch DC operating point，再在 `t=2–5 µs` 发生同样的开关事件。**

这只是平移时间原点，**不能改变电路值、负载、边沿或原厂模型**。

普通7宏暂态只运行到：

\[
t_{\rm switch}+330\sim350\ \mu s
\]

不再跑600 µs、更不跑整帧9.6 ms。

验收从切换事件计时：

- \(t=300\,\mu s\) 后的全部计划有效采样点；
- ADC输入残余≤100 µV；
- 无削顶；
- 无持续增长振荡；
- 稳态参考必须来自该case自身后段，不用理想理论值替代。

### 必跑六个7宏核心case

两个分区：

- `VCM+VEXC+4row+1TIA`
- `VCM+VEXC+1row+4TIA`

分别覆盖：

- all 800 Ω；
- all 8000 Ω；
- high-target / low-neighbor。

先全部5 V。

**不再为这六个case修改100 pF/22 pF候选。**

如果正常case跑过，再只对已经识别的最坏负载补4.75/5.25 V供电角点。

### 积分器的裁定

Gear允许用于7宏模型取得波形，但**Gear单独不能证明稳定**。

其证据必须与以下三项一起出现：

1. 已通过的Tian/Y-port小信号结果；
2. 已通过的trap单TIA/4宏模型结果；
3. 下一节完整静态耦合稳定性筛查。

这样才可形成：

`PARTITIONED_COUPLED_DYNAMIC_PASS`

---

# 四、PZ不再作为唯一死门，改用完整多环路小信号闭合

这是本次最关键的方法调整。

ngspice `.pz` 已经4次没有得到可信极点，其中还出现把OP raw误当极点文件的情况。**下一包不能继续用几十次PZ试错作为主线。**

## PZ只做一次资格链

最多执行：

1. 已知解析极点的RC/RLC fixture；
2. 单OPA宏模型闭环；
3. 4宏模型分区；
4. 若前三者都能正确返回真实pole/zero，再尝试全网关键状态。

必须明确检查：

- 分析类型确实是Pole-Zero；
- 输出里真正存在pole/zero列表；
- fixture误差在预期范围；
- 不能再把Operating Point raw当PZ。

如果前三级无法资格：

**立即定性为 `PZ_TOOL_OR_MODEL_CAPABILITY_LIMIT`，PZ退出硬门。**

这不会再次阻止R2.1。

---

# 五、完整静态稳定性主路线：10环MIMO return-difference

本次新增这一条作为真正的全网耦合闭合方法。

全网10个反馈环：

- VCM ×1
- VEXC ×1
- ROW ×4
- TIA ×4

在已经正确的DC工作点附近，为10个环建立保持偏置和负载的测试端口，逐列独立激励，构造：

\[
\mathbf L(j\omega)\in\mathbb C^{10\times10}
\]

具体实现延续已经通过验证的 **Tian/Y-port端口思想**，不是恢复旧高阻单电压注入。

至少输出：

\[
\lambda_i(\mathbf L)
\]

以及return-difference：

\[
\mathbf R(j\omega)=\mathbf I+\mathbf L(j\omega)
\]

并计算：

\[
\sigma_{\min}(\mathbf R)
\]

### 方法自检

从10×10矩阵抽出的对应单环行为，必须与本轮已接受的Tian/Y-port结果满足：

- 主交越频率差≤10%；
- 对应PM差≤5°；
- 不允许矩阵方法突然出现无法解释的额外交越。

否则优先判**多环测试台实现有问题**，不能据此修改电路。

### 需要覆盖的完整网络状态

5 V至少：

- all blank / all800；
- ROW active / all800；
- ROW active / all8000；
- ROW active / high-target-low-neighbor。

然后用DC continuation补：

- 4.75 V；
- 5.25 V；

只对最坏主动状态进行完整MIMO复查，不要求把所有组合乘三遍。

### 设计筛查门

这是工程筛查，不冒充数学上无限频率的绝对稳定证明。

需要：

- 没有明显趋向 \(-1\) 的危险eigenlocus；
- 在已扫频段没有未解释的多交越；
- \(\sigma_{\min}(I+L)\) 的最小值完整报告；
- 若最小值 **<0.20**，自动进入技术复核，不直接PASS；
- 频率上界处必须确认loop gain已经明显衰减，不能因为扫到100 MHz就声称“全频无问题”。

这一结果结合7宏暂态，而不是单独使用，就构成：

`FULL_STATIC_COUPLED_NO_INSTABILITY_EVIDENCE`

---

# 六、4.75 / 5.25 V工作点统一用continuation闭合

当前5 V多数case有有效OP，而4.75/5.25 V整网直接求解失败。

下一包不要随机换节点顺序反复碰运气。

统一用：

**5.00 V已验证OP → 4.95 → 4.90 → … → 4.75 V**

以及：

**5.00 → 5.05 → … → 5.25 V**

每一级只把上一级**作为 `.nodeset` 初猜**。

最终4.75/5.25 V角点必须重新真实求解，不能：

- 用 `.ic` 强行锁住工作点；
- 复制5 V结果；
- 把收敛失败称削顶。

如果50 mV步长失败，允许缩到25 mV一次；仍失败则保留数值HOLD，不再做任意节点排列大搜寻。

---

# 七、RESET的温度域与±故障门，本次直接分开

## 1. 正常复位功能

当前 direct NRST：

`J3.5 → 1 kΩ → PGOOD/NRST`

25°C解析结果：

- 最坏assert：0.81446 V；
- 保守保证低门限：0.9195 V；
- 低电平裕量约：105 mV；
- Hi-Z释放也有明显裕量。

所以我正式接受：

`RESET_DIRECT_PATH_25C_DESIGN_PASS`

### 为什么不继续让BAT54S温度问题堵原生图

项目首版的实际台架边界是室温。BAT54S冻结资料没有给出足够的高温保证漏电上界，所以现在不能宣称完整温区保证。

下一包允许两条路线，自动选择，不逐项问我：

**路线A优先：**最多查2个同功能、低泄漏、具有明确保证漏电温度数据的钳位候选，仅用于NRST这条线。如果不增加明显复杂度，换掉RESET上的BAT54S。

**路线B：**20分钟内没有合适保证器件，继续使用BAT54S，R2.1允许标：

`RESET_DIRECT_PATH_25C_PASS / RESET_20_30C_BENCH_HOLD`

这不会继续阻止**审查版原生R2.1**生成。

它仍阻止bench正式验收。

## 2. ±5 V不是正常复位功能域

本次明确：

**正常接口契约：active-low open-drain/open-collector，Hi-Z释放，VOL≤0.4 V。**

±5 V属于**单故障生存性**，不是正常NRST功能保证。

因此：

- ±5 V钳位；
- 掉电回灌；
- 60 s热；
- 二极管温度VF/IR；
- MCU绝对最大值；

全部继续放在：

`FAULT_PROTECTION_HOLD`

它们**不再阻止R2.1审查原理图**，但仍阻止bench故障试验和制造放行。

---

# 八、故障时延逻辑：本次基本闭合，不再重复大规模软件重写

当前progress watchdog已经覆盖：

- 4.5 ms heartbeat timeout；
- 2.5 ms progress timeout；
- state index；
- sample count；
- epoch；
- replay；
- frame gap；
- nonfinite/backwards time；
- reset/config失败清资格；
- 两个真正新完整帧恢复。

32项GREEN接受。

下一包只允许：

- 把最终硬件/固件接口契约冻结成文档；
- 在任何修改后完整回归一次。

不再新增第二套状态机。

正式状态：

`FAULT_LATENCY_LOGIC_CONTRACT_PASS / HARDWARE_WCET_PENDING`

---

# 九、唯一下一包

## 包名

`SCIENCE_ADK5556_4X4_R21_MIMO_STABILITY_AND_NATIVE_ECO_CLOSURE_V1`

目标：

**把多环耦合从“数值卡死”转成可判定的小信号＋短窗层级证据；条件满足后直接生成R2.1最小原生ECO。**

---

## 冻结输入

固定以下三代证据：

- R2：`da6ca87b...`
- R2.1验证：`c13555a...`
- 本次耦合根因：`a3e22772...`

继续冻结：

- ngspice47 + PSA兼容方式；
- 原始OPA4388 / OPAx388宏模型；
- 4×4 / 8线；
- 0.8–8 kΩ；
- E=0.25 V；
- Rf=4.99 kΩ / Cf=2.2 nF；
- 100 fps；
- 八状态相邻blank；
- progress watchdog合同。

补偿候选冻结：

- ROW：1 k / 4.99 k / 100 pF；
- VCM/VEXC：1 k / 4.99 k / 100 pF；
- TIA：1 k隔离 + **22 pF**高频反馈。

**不授权第三轮补偿参数扫描。**

---

# 十、新预算：批准扩大到360 min

用户明确要求下一轮给更大的有界自主预算，以减少小步骤反复请示。**批准。**

这是新包预算，从零重新计数，不追溯旧包的7例超额。

| 阶段 | 时间上限 | 内容 |
|---|---:|---|
| P0 方法/PZ/continuation | **60 min** | PZ资格、MIMO fixture、供电continuation、数值根因 |
| P1 MIMO＋7宏动态 | **120 min** | 完整静态矩阵、关键分区短窗、有限求解器对照 |
| P2 RESET＋协议收口 | **60 min** | 温度资料/候选、RESET保证域、一次完整协议回归 |
| P3 条件原生R2.1 ECO | **90 min** | 最小图纸修改、冷重开、连接/ERC/PDF |
| P4 封装交付 | **30 min** | 固定commit、报告、结果与接续检查 |

### 分析额度

- DC/AC/PZ实际求解合计：**≤128**
- 正常暂态：**≤64**
- diagnostic属性：**≤16**，并且必须同时扣实际DC/AC/PZ/TRAN类别
- RESET解析角点：**≤96**
- 协议回归：**≤48**
- 新增原厂资料：**≤8**
- RESET保护候选：**≤2**
- 新原生库身份：**≤4**

runner必须使用你们已经修好的**原子多类别预检**：任一相关额度不足，不得启动进程。

### 单case时间

- 普通暂态：≤180 s；
- 15 s仿真时间完全不推进：提前STOP；
- 最终完整10宏模型诊断：**最多1次、≤8 min wall**。

完整10宏模型长窗属于**附加诊断**，不再是R2.1原生工程的必须PASS条件。

---

# 十一、条件原生R2.1进入门

同时满足以下五项，即允许直接进入P3，不再回来问：

1. `RETURN_RATIO_METHOD_VALIDATED` —— 已PASS，保持；
2. `MIMO_STATIC_COUPLED_SCREEN_PASS`；
3. 两个7宏分区的关键case取得切换后≥300 µs有效窗口且≤100 µV；
4. `RESET_DIRECT_PATH_25C_DESIGN_PASS`，且20–30°C缺口被清楚标注或由新钳位件闭合；
5. `FAULT_LATENCY_LOGIC_CONTRACT_PASS` —— 已PASS。

**PZ成功不是独立硬门。**

**完整10宏模型9.6 ms transient也不是独立硬门。**

如果这些条件达到，最终状态可以写：

`HIERARCHICAL_DYNAMIC_EVIDENCE_PASS / FULL_MONOLITHIC_TRANSIENT_NUMERICAL_HOLD`

然后做R2.1。

---

# 十二、R2.1原生只允许最小ECO

进入门通过后，原理图只改：

- VCM/VEXC：100 pF验证补偿；
- TIA：22 pF验证补偿；
- NRST：4.99 kΩ → **1.00 kΩ direct reset**；
- 若选定新reset钳位，仅替换这一条线；
- 协议说明更新为八状态＋progress watchdog；
- 修四个C_ADC Value元数据；
- 修明显文字/端口重叠；
- 不改架构、E、Rf、ADC、OPA或100 fps。

原生预算：

- 工作副本1；
- session≤2；
- save≤8；
- File capture＋完整audit≤4；
- ERC≤2；
- PDF≤2。

若ERC仍只能取得count，允许保留 `ERC_DETAIL_HOLD`，不允许为了ERC再次推倒重建168器件。

---

# 十三、停止门

下面才需要重新集中找我：

- Tian/Y-port与10×10 MIMO方法出现无法解释的冲突；
- 7宏模型出现**实际增长振荡**而非单纯收敛慢；
- 300 µs /100 µV在冻结补偿下真实失败；
- 4.75/5.25 V正常工作点出现真实削顶；
- direct reset即使更换/限定钳位后仍无法满足门限；
- 必须更换OPA/ADC、改变E/Rf或降低100 fps；
- 达到360 min或任一操作额度上限。

否则Codex在本包内自主推进，不再为普通数值排序、有限retry、CSV生成、协议回归、图纸局部调整逐项来问。

---

## 最终一句话

**现在已经不是“电路方案行不行”的问题，而是把剩余的多环耦合证据用正确方法闭合。**

本轮最关键的新发现——**旧耦合模型VEXC写成0.25 V**——说明此前完整模型卡死被严重混入了测试台错误；修正后单环方法、局部动态和协议证据都在向同一个可用设计收敛。

所以这次批准更大的 **360 min 单包自主范围**。下一次正常回传，理想情况应该直接是 **R2.1原生ECO＋完整审计**；如果仍阻断，也必须已经把原因明确缩到某个具体物理/模型问题，而不是继续停在“十个宏模型跑不完”。
