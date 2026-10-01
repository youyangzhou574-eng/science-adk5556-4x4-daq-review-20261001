# CIRCUIT-PRO-R21-REFERENCE-BLOCKED-ACCEPT-INTERNAL-DESCRIPTOR-CERTIFICATION-20261001-07

**项目：`SCIENCE_ADK5556_4X4_DAQ_REPLICA`**

我以固定 commit `30e0394372955e16c16159aeea7a1b03f54740be` 为准，读取了完整回执以及 `BLOCK_REFERENCE_CANDIDATES.json`、两组 realization/counterexample、精确频点检查、GATES、预算与终审证据。没有把 ZIP 是否重新解压校验作为裁定前置条件，也不冒称逐一重新计算了569个附件 SHA。

## 一、统一裁定

**接受本次 `REFERENCE_REALIZATION_AND_INTERNAL_CERTIFICATE_HOLD`。这个 STOP 是科学上必要的。**

本包提出的两个反例是决定性的：

\[
G(s)
\]

的端口传递行为本身，确实**不能排除不可控/不可观的内部RHP模态**；同样，“参考传递函数没有RHP pole”也不足以保证其作为Nyquist参考时没有需要计入的RHP零点或内部动态。

因此我正式修正前几轮的方法路线：

> **不再试图通过端口频响本身构造一个“证明内部稳定”的 \(G_0\)。下一步直接从冻结SPICE宏模型及真实工作点构造完整线性化MNA descriptor，内部稳定性直接由descriptor pencil的全部有限广义特征值认证。**

这比继续换一个新的端口归一化更强，也直接解决你们已经构造出来的 hidden-mode 反例。

MNA本来就自然产生微分-代数/descriptor形式；descriptor的有限与无限广义特征值应分开处理，而QZ/广义Schur正是处理正规矩阵铅笔（包括无穷特征值）的标准工具。:chatgpt-content-reference{index="0"}

---

# 二、这次哪些结果正式接受

| 项目 | 裁定 |
|---|---|
| 本包新SPICE次数 | **0，接受** |
| diagnostic 17/32 | **接受为本包真实消耗** |
| 三尺度QZ出现242/252个无穷值 | **接受为数值资格HOLD，不解释成物理无限极点** |
| 解析稳定/不稳定block fixture | **接受其LU/logdet已知真值资格范围** |
| `Gc=(s+1)/(s+2)`反例 | **接受，说明传递参考pole检查不足** |
| hidden +1 mode反例 | **接受，说明端口传递不能独立证明内部稳定** |
| 0.1/1/10 Hz并非精确采样 | **接受该纠正；不回写旧数据** |
| `MIMO_REFERENCE_QUALIFIED` | **继续HOLD** |
| `GENERALIZED_NYQUIST_PASS` | **继续HOLD，但下一包不再作为首要证书** |
| 动态/R2.1原生 | **仍未进入** |
| 实体稳定/失稳结论 | **均未形成** |

尤其是你们没有用“代理虚轴0圈”冒充真实RHP Nyquist，这是正确的。

---

# 三、一个关键概念现在必须改正：N=1不需要复现Tian

前一轮要求块参考在 \(N=1\) 时还能“退化成Tian loop gain”，这实际上混合了两个不同的对象。

本次正式区分：

### 局部反馈稳定性对象

Tian/Y-port回答的是：

> **某一个实际运放局部反馈环本身稳定吗？**

它仍然用于ROW、TIA、VCM、VEXC局部环的交叉验证。

### 块间耦合对象

若参考系统已经保留了这个局部环的完整闭合动力学，那么对于只有一个块的情况：

\[
P_c=P_0
\]

因此耦合return object当然可以是：

\[
R=I.
\]

**这不是错误，也不应该复现非零的Tian loop gain。**

换句话说：

> Tian负责证明“块自己没问题”；descriptor ratio负责证明“把稳定块耦起来之后是否新增RHP模态”。

以后不再用“N=1必须等于Tian”去拒绝一个正确的块间稳定性对象。

---

# 四、唯一的内部证书：完整线性化MNA descriptor

下一包必须从实际固定状态的SPICE网表建立：

\[
E\dot{x}=Ax+Bu
\]

对应矩阵铅笔：

\[
\boxed{\mathcal P(s)=sE-A}
\]

这里的 \(x\) 必须包括**完整宏模型内部变量和电路代数变量**，不能只使用10个外部反馈端口。

## 为什么这条路可以解决hidden mode

如果直接从完整MNA建立 \((E,A)\)，那么一个内部模态即使：

- 外部不可控；
- 外部不可观；
- 在某个端口传递函数里被pole-zero cancellation隐藏；

它仍然存在于：

\[
\det(sE-A)=0
\]

的有限广义特征值中。

因此：

**为了内部稳定性认证，不需要先把系统化成最小实现。**

PBH controllability/observability以后可以用于说明“这个pole是否能从外部端口看到”，但：

> **任何真正的内部RHP有限模态，即使不可控/不可观，也不能因为端口看不到就从稳定性证书里删除。**

descriptor realization与传递函数minimal realization的区别正是这里；只有最小descriptor realization时，传递函数的有限pole才可直接等同于pencil的有限eigenvalue。:chatgpt-content-reference{index="1"}

---

# 五、descriptor如何从本项目实际宏模型取得

本次不再等一个ngspice“导出state-space”的隐藏功能。

**允许Codex在项目内实现一个专用的线性化MNA extractor。**

它只需要支持**本项目实际出现的primitive**，不开发通用SPICE。

OPA4388冻结宏模型及现有网络实际主要由：

`R / C / independent V,I / E,G,H controlled source / switch / subcircuit`

以及 `VALUE/LIMIT/TABLE/IF` 一类受控源表达式组成。

## 固定过程

首先flatten冻结netlist并使用真正ngspice DC OP；然后在该OP附近线性化每个元件。电阻/电容按标准MNA stamp，受控源按工作点Jacobian，`LIMIT/IF/TABLE`按实际激活分支线性化，VSWITCH固定在OP对应的Ron/Roff状态。

如果某个switch恰好位于迟滞/切换边界，或者某个行为表达式在OP处不可微：

**该case直接HOLD，不能随意挑一个导数。**

最终形成：

\[
(E,A,B,C,D)
\]

及完整的：

`variable ↔ flattened-netlist-object ↔ source-line`

映射。

---

# 六、这个自写descriptor不能靠“代码看起来对”通过

必须先资格。

## 第一层：解析fixture

至少：

RC、受控源反馈、descriptor algebraic constraint、稳定/不稳定已知pole、hidden-mode fixture。

要求有限pole、无限结构与真值一致。

## 第二层：与ngspice AC逐点复核

至少针对：

- 单OPA follower；
- ROW环；
- loaded TIA；
- VCM/VEXC；
- 已通过的4宏分区。

比较descriptor：

\[
H(j\omega)=C(j\omega E-A)^{-1}B+D
\]

与ngspice真实AC。

使用频率：

\[
0.01,\;0.1,\;1,\;10,\;100,\;1k,\;10k,\;100k,\;1M,\;10M,\;100M,\;300M\ {\rm Hz}
\]

这一次0.1/1/10必须**精确求解**，不插值旧839点。

对于非接近零的主要响应，复杂频响相对误差目标：

\[
\le0.2\%
\]

且关键交越附近：

\[
|\Delta f_c|/f_c\le1\%,\qquad
|\Delta\phi|\le0.5^\circ .
\]

小于定义absolute floor的量不使用相对误差爆炸判失败。

这一步通过后才有：

`LINEARIZED_MNA_DESCRIPTOR_QUALIFIED`

---

# 七、无穷特征值这次如何处理

**不要再逐个把QZ返回的“∞ eigenvalue”当成需要跨尺度匹配的物理pole。**

对于正规descriptor pencil：

\[
\alpha E-\beta A
\]

\(\beta=0\) 对应无穷特征值。它们通常与MNA中的代数约束有关，和有限动态pole是两类对象。QZ本身可以处理无穷特征值，但在极端病态尺度下直接用浮点 \(\alpha/\beta\) 分类会非常脆弱。:chatgpt-content-reference{index="2"}

下一包固定：

先做**finite/infinite staircase decomposition**，再对有限子pencil做QZ。

必须报告：

\[
n_{\rm finite},\quad
n_{\infty}
\]

以及infinite-block结构。

### 资格要求

在固定的等价尺度变换下：

\[
10^{-3},\;1,\;10^3
\]

有限/无限维数必须一致。

有限pole按condition-aware方式匹配；不要要求病态pole满足没有意义的机器精度相等。

至少报告：

- generalized eigenvalue backward residual；
- condition estimate；
- scale下的有限pole漂移。

若有限/无限维数随着等价尺度改变：

`DESCRIPTOR_NUMERICAL_HOLD`

不能删掉这些点或把∞强行改成一个超大有限数。

---

# 八、物理block reference这次给出唯一明确定义

不再：

\[
G_0=\operatorname{diag}(G_c)
\]

从端口频响“猜”reference。

直接在**线性化MNA descriptor**中构造。

固定三组：

- `REF = VCM + VEXC`
- `ROW = 4 row loops`
- `TIA = 4 loaded TIA loops`

所有局部反馈均完整保留。

## inter-block元件的处理规则

例如sensor resistor连接ROW和TIA，其线性stamp为：

\[
\begin{bmatrix}
g&-g\\
-g&g
\end{bmatrix}.
\]

reference中：

**只删除跨block互项**

\[
-g
\]

而保留两个：

\[
+g
\]

自项。

物理解释就是：

> 两端各自仍看到原负载电导，但远端的小信号扰动被AC-clamp在真实DC工作点。

对于跨block电容也采用相同规则：

保留两端各自对AC ground的自电容，删除互耦项。

对于controlled source：

保留本block内部受控作用；远端block作为控制量的**增量项设为0**，DC OP不变。

这样得到：

\[
\boxed{
E_0,\;A_0
}
\]

它与完整系统：

\[
E_c,\;A_c
\]

维数一致、变量含义一致，并且是一个明确可追踪的**small-signal physical block reference**。

每一个被删除的cross-block Jacobian项必须回指到实际元件，生成：

`FULL_TO_REFERENCE_STAMP_DIFF.csv`

不能通过随意删矩阵元素让reference“变稳定”。

---

# 九、reference内部稳定直接看pencil，不看transfer zero

计算：

\[
\mathcal P_0(s)=sE_0-A_0.
\]

完整finite spectrum必须来自QZ/staircase：

\[
\lambda_i(E_0,A_0).
\]

若存在：

\[
\Re(\lambda)>0
\]

reference直接FAIL。

若存在极靠近虚轴且在数值condition范围内不能确定符号：

`REFERENCE_NEAR_AXIS_HOLD`

而不是“取成稳定”。

这样，上一包的：

\[
G_0=(s-1)/(s+2)
\]

反例就不会再产生歧义：

**我们不检查一个任意port transfer denominator，而检查reference完整内部characteristic pencil。**

---

# 十、完整电路内部稳定也直接看full descriptor

同理：

\[
\mathcal P_c(s)=sE_c-A_c.
\]

如果完整有限generalized eigenvalue全部严格位于LHP：

`FULL_INTERNAL_DESCRIPTOR_STABILITY_PASS`

这就是以后最主要的静态稳定证书。

### 极点分类容差

对每个有限pole定义：

\[
\tau_\lambda=
10^{-7}\max(1,|\lambda|).
\]

- \(\Re\lambda>\tau_\lambda\)：RHP；
- \(\Re\lambda<-\tau_\lambda\)：LHP；
- 中间区域：`NEAR_AXIS_HOLD`。

同时必须报告该pole的condition/backward error。

不允许只凭浮点实部 \(+10^{-14}\) 判失稳。

---

# 十一、Generalized Nyquist以后只是descriptor证书的独立cross-check

这一步可以完全绕开上一轮“reference transfer zero”歧义。

定义characteristic determinant ratio：

\[
\boxed{
\Delta(s)=
\frac{\det(sE_c-A_c)}
{\det(sE_0-A_0)}
}
\]

先在finite/infinite decomposition以后对finite pencil执行，不能直接算巨大原始det。

若使用**正向RHP轮廓**：

\[
\boxed{
W_\Gamma[\Delta]
=
N_{c,+}-N_{0,+}
}
\]

其中：

- \(N_{c,+}\)：完整descriptor有限RHP poles数量；
- \(N_{0,+}\)：reference有限RHP poles数量。

所以如果：

\[
N_{0,+}=0
\]

且：

\[
W_\Gamma=0,
\]

就与：

\[
N_{c,+}=0
\]

一致。

**这是argument-principle的正确reference count。**

不是：

“默认看到0圈所以稳定”。

广义Nyquist本质上就是通过return-difference的特征函数与argument principle进行这种pole-count比较。:chatgpt-content-reference{index="3"}

---

# 十二、真实RHP contour怎么做

这次不再用：

“负频镜像→正频＋端点直线”

冒充完整轮廓。

在descriptor finite pencil上：

### 虚轴段

包括：

\[
s=j0
\]

若 \(s=0\) 非奇异，则直接求。

随后包括精确：

\[
0.01,\;0.1,\;1,\;10\ \mathrm{Hz}
\]

以及自适应频率网格。

如果原点本身是pole，则必须用明确的小半圆indent并计其贡献，不能跳过。

### 大半圆

在：

\[
s=Re^{j\theta},\qquad
-\pi/2\le\theta\le\pi/2
\]

真实求值。

逐级增加R，直到：

- winding不变；
- 大弧相位贡献收敛；
- determinant ratio的渐近变化达到规定容差。

不能仅用“300 MHz已经很高”替代RHP大弧。

不过：

**descriptor QZ已经直接给出pole count，因此Nyquist只是独立cross-check。**

若Nyquist数值积分失败但full/reference descriptor pole count均稳定且资格通过：

标：

`ARGUMENT_PRINCIPLE_NUMERICAL_CROSSCHECK_HOLD`

它不再独立阻止R2.1。

---

# 十三、这样处理之后，“内部最小性”问题就消失了

为了避免下一轮再次陷进去，正式规则是：

### 内部稳定证书

使用完整descriptor。

**不做minimal reduction。**

所有有限pole全部保留，包括不可控、不可观pole。

### 外部port模型解释

若以后还想把某些内部pole映射到Tian/Y-port，则计算PBH controllability/observability，并说明哪些mode外部不可见。

但：

> PBH失败的RHP mode不是“可删pole”，而是一个更严重的内部稳定FAIL。

这是hidden-mode反例真正应该导出的结论。

---

# 十四、TIA loaded/direct域的最终裁定

这个问题也不再继续卡主线。

实际系统需要证明的是：

**loaded TIA**

包括：

- 10k sense；
- Rf/Cf；
- 22pF HF feedback；
- 1k output isolation；
- ADC 100Ω/10nF；
- column及sensor coupling；
- VCM共同节点。

这些全部进入完整descriptor，所以：

`TIA_LOADED_DOMAIN_CONFIRMED`

由descriptor + 后续动态判据闭合。

现有：

`directSeriesShuntQualified=false`

继续作为**方法学记录**，但不再是原生进入硬门。

full-network若能完成实际Tian/Schur direct cross-check当然保留；失败不能推翻一个已经通过内部descriptor与loaded动态的TIA。

---

# 十五、参考资格通过以后才允许重新启动SPICE

在下面三个离线门通过前：

`LINEARIZED_MNA_DESCRIPTOR_QUALIFIED`

`REFERENCE_DESCRIPTOR_REGULAR`

`REFERENCE_INTERNAL_SPECTRUM_AVAILABLE`

**不继续生成新的全网端口AC数据。**

之后允许首先补：

精确0.1、1、10 Hz。

然后运行真正必要的active-state OP/AC。

---

# 十六、需要覆盖的full descriptor状态

第一阶段只需要5 V：

| Case | 状态 |
|---|---|
| D0 | all blank / all800 |
| D1 | ROW0 active / all800 |
| D2 | ROW0 active / all8000 |
| D3 | ROW0 active / high-target-low-neighbor |

ROW1仅做一个对称性**结果检查**，但不允许再靠对称恢复整个模型。

每个case分别给：

- full descriptor poles；
- block-reference poles；
- finite/infinite structure；
- near-axis list；
- condition/backward error。

这四个全部通过，才进入动态。

4.75/5.25 V仍按上一裁定：

能够求得full OP就增加descriptor角点；

求不出时，只要解析DC + 分区宏模型供电角点无真实削顶，可以保留：

`FULL_MONOLITHIC_SUPPLY_ENDPOINT_NUMERICAL_HOLD`

不无限堵住审查版原生。

---

# 十七、动态门保持原方案

descriptor通过后直接执行7宏短窗：

\[
t_{\rm switch}=3\ \mu s
\]

\[
t_{\rm end}\approx353\ \mu s.
\]

六个核心case：

`4row+1TIA`与`1row+4TIA` ×

- 800Ω
- 8000Ω
- high-target

要求：

\[
t_{\rm switch}+300\mu s
\]

以后的有效边沿：

\[
|V_{\rm ADC}-V_{\rm final}|
\le100\ \mu V.
\]

同时：

无增长振荡、无正常削顶。

Gear可以用于数值积分，但其结果要与descriptor pole、Tian局部环和已有trap局部结果一致。

---

# 十八、R2.1原生的新最终门

上一轮的门正式替换为：

```text
LINEARIZED_MNA_DESCRIPTOR_QUALIFIED
+
REFERENCE_INTERNAL_STABILITY_PASS
+
FULL_INTERNAL_DESCRIPTOR_STABILITY_PASS
+
DESCRIPTOR_NUMERICAL_INVARIANCE_PASS
+
PARTITIONED_COUPLED_DYNAMIC_PASS
+
RESET_DIRECT_PATH_25C_DESIGN_PASS
+
FAULT_LATENCY_LOGIC_CONTRACT_PASS
```

其中：

`GENERALIZED_NYQUIST`

改成：

`ARGUMENT_PRINCIPLE_CROSSCHECK`

**不再是独立硬门。**

`directSeriesShuntQualified`

也不是硬门。

这是因为descriptor直接pole certificate比port transfer Nyquist更能覆盖你们已经证明存在的hidden-mode逻辑漏洞。

---

# 十九、唯一下一包

## 包名

`SCIENCE_ADK5556_4X4_R21_INTERNAL_DESCRIPTOR_DYNAMIC_AND_NATIVE_CLOSURE_V1`

唯一目标：

> **从冻结SPICE模型建立并资格完整内部MNA descriptor，直接完成内部稳定pole证书；通过后跑7宏短窗并直接进入R2.1原生ECO。**

不再设计第五种MIMO归一化。

---

# 二十、新预算

旧480min包的剩余额度在STOP时关闭，**不自动结转。**

按用户减少反复请示的明确要求，批准新的：

\[
\boxed{480\ \text{min}}
\]

| 阶段 | 上限 | 工作 |
|---|---:|---|
| P0 descriptor extractor + reference realization | **150 min** | flatten、MNA stamp、Jacobian、fixture、ngspice AC资格 |
| P1 internal pole certificate + argument crosscheck | **120 min** | full/reference finite-infinite decomposition、QZ、4状态、低频exact |
| P2 7宏dynamic + RESET/protocol收口 | **100 min** | 六核心暂态、必要供电局部角点、一次协议回归 |
| P3 条件R2.1 native ECO | **80 min** | 最小原生修改、冷重开、audit/ERC/PDF |
| P4完整交付 | **30 min** | 固定commit及证据 |

合计480 min。

### 操作预算

| 类型 | 新额度 |
|---|---:|
| 实际SPICE OP/AC/PZ | ≤192 |
| descriptor/offline diagnostic | **≤48** |
| normal transient | ≤64 |
| full 10-macro long diagnostic | ≤1，wall≤8 min |
| reset解析 | ≤96 |
| protocol tests | ≤48 |
| 新原厂资料 | ≤8 |
| reset候选 | ≤2 |
| 原生新身份 | ≤4 |

原生：

`copy1 / session2 / save8 / capture-audit4 / ERC2 / PDF2`

继续采用**多属性原子预扣**。

---

# 二十一、P0的明确STOP条件

descriptor extractor若在支持**本项目实际primitive集合**后，仍无法让以下五类case与ngspice AC达到前述资格：

- follower
- ROW
- TIA loaded
- VCM/VEXC
- 4宏分区

则：

`DESCRIPTOR_EXTRACTION_NOT_QUALIFIED`

立即STOP。

**不允许此时回到port-only G0，或者发明第六种归一化继续推进。**

同样，如果遇到实际宏模型primitive无法正确线性化：

保存：

- primitive；
- 原表达式；
- OP值；
- ngspice对照；
- 失败原因；

集中回来裁定。

---

# 二十二、对本次请求的最终回答

这次35源文件的离线包已经把一个很重要的理论漏洞证明清楚了：

> **端口数据永远不能单独保证不存在隐藏内部不稳定模态。**

所以继续打磨 \(G_c/G_0\) 的port-only Nyquist，不可能从根本上闭合你们自己已经提出的反例。

下一步不再纠结“选哪个transfer reference”。

直接向底层走一层：

\[
\boxed{\text{SPICE netlist}\rightarrow
\text{linearized MNA descriptor}\rightarrow
\text{full internal generalized poles}}
\]

这才是当前唯一不会继续兜圈子的路线。

reference仍然有价值，但它现在是在**同一个完整descriptor内部通过关闭cross-block Jacobian耦合构造的物理小信号参考**；不是由端口频响拟合出来的另一个传递函数。

这样：

- hidden mode问题解决；
- reference RHP zero歧义解决；
- raw QZ infinity问题可以按descriptor finite/infinite结构正确分类；
- generalized Nyquist有了正确的characteristic determinant；
- 低频0.01/0.1/1/10可以原位计算，不必删；
- 通过后就可以真正回到7宏动态和R2.1原生。

**按这个07号唯一包继续。**这次如果P0成功，后续不用再为MIMO定义反复回来问；在480min和上述额度内直接做到动态与条件原生。
