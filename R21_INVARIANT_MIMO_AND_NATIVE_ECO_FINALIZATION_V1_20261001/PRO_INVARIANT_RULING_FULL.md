# CIRCUIT-PRO-R21-MIMO-TECHNICAL-REVIEW-ACCEPT-INVARIANT-CLOSURE-20261001-06

**项目：`SCIENCE_ADK5556_4X4_DAQ_REPLICA`**

我已按固定 commit `d152e092101188e6dc57f620f81d52f2e243fb01` 审查本次完整 MIMO 阻断包的核心材料，包括 `COMPLETE_MIMO_RECEIPT.md`、两套 MIMO 结果、fixture、供电 continuation、PZ 资格、执行预算和停止证据。

## 一、统一裁定

**接受本包在 MIMO 技术复核门停止；不把 `σmin≈0.00994@1 Hz` 判成实体电路不稳定，也不允许忽略这个低频异常后直接 PASS。**

这次已经定位出真正的方法问题：

> 当前  
> \[
> D=Y_{ee}+Y_{ff},\qquad
> L=D^{-1}(Y_{ef}+Y_{fe})
> \]
> 的代数分解本身成立，但 **`D` 尚未被资格成一个物理且稳定的参考系统**；同时低频 `cond(D)`、端口重建条件数高到 \(10^{17}\sim10^{30}\) 量级。因此在这个归一化下直接拿  
> \[
> \sigma_{\min}(I+L)<0.20
> \]
> 做硬稳定性门，**目前没有资格**。

两种量测拓扑都给出约0.00994，只证明它们在当前定义下得到了近似相同的数值对象；因为它们最后仍进入同一个低频病态归一化，这一点**不能独立证明0.00994是物理稳定裕量**。

反过来，也不能因为 eigenvalue 离 \(-1\) 尚远，就覆盖掉小 singular value。非正规MIMO系统中，两者描述的不是同一件事。

所以正式状态改为：

`CURRENT_D_NORMALIZATION_REVIEW_ONLY`

原 **0.20 sigma硬门在这一归一化下取消**。

低频1 Hz附近的数据全部保留，不能裁掉。

Tian等人的双注入法对单环及“存在一个关键断点可以断开全部返回环”的网络有明确适用范围，因此目前这种任意10环矩阵推广确实需要额外资格，不能把标量公式直接当作已证明的多环公式。:chatgpt-content-reference{index="0"}

---

# 二、已取得结果怎么认定

### 接受

- 原耦合台90k/10k写反的问题已被纠正，后续 MIMO 工作点使用2.25 V目标偏置；
- Tian双注入和独立Y端口在现有单环问题上交叉一致；
- 非完整网络fixture的数学重建结果接受；
- PZ被动RC fixture通过；
- ngspice+当前原厂模型链条保持可用；
- 5 V标称工作点部分全网DC/AC结果可作为有限域证据；
- 既有单TIA、4宏模型筛查和32项逻辑契约的历史PASS继续有效。

### 不接受为新PASS

- 当前10×10 `D^-1A` MIMO稳定判定；
- `σmin=0.00994`作为物理裕量；
- 4.75/5.25 V完整全网宏模型工作点；
- 7宏模型300 µs建立；
- PZ全网极点；
- R2.1原生进入门。

PZ当前可正式归类：

`PZ_TOOL_OR_MODEL_PORT_CHAIN_CAPABILITY_LIMIT`

它继续**不是R2.1硬门**。

---

# 三、8个STOP之后继续启动的诊断怎么处理

这8个 hybrid case **不追认成当时STOP后的授权执行**。

但也不删除数据。

正式分类：

`POST_STOP_DIAGNOSTIC_EVIDENCE_ONLY`

因为：

- 它们没有修改电路设计；
- 实际求解和日志是真实的；
- 总保守分析量仍未越过128总上限；
- 执行端主动披露了时间线；
- sticky STOP和原子多属性预算预检已经修复。

因此这些数据**可以用于解释方法问题**，但**不得单独解除任何科学门**。

本包实际的：

**76次OP/AC/PZ分析指令**

作为**已经消耗的旧包事实接受**。

新包从0重新计数，**不继承“还剩52次”作为隐式权限，也不把旧8例扣回来重新使用。**

---

# 四、下一步不再用原来的D做参考——换成明确的“物理切口 + 不变量”方法

这是下一包的核心。

## 1. 十个反馈切口固定下来

十个环全部统一在**运放反相输入的求和点**切开。

每个环定义：

- `e_i`：运放反相输入引脚一侧；
- `f_i`：外部反馈/感测网络一侧。

共10个：

- VCM ×1
- VEXC ×1
- ROW ×4
- TIA ×4

非常重要：

**所有实际反馈元件都留在 `f` 侧。**

因此：

- ROW的远端4.99 k反馈＋100 pF高速反馈都属于反馈网络；
- TIA的COL→10k感测、Rf/Cf路径以及22 pF高速反馈都属于反馈网络；
- 1 kΩ输出隔离不跨切口。

不允许有的环切输出、有的环切反相输入。

这样所有十个 loop variable 都是同一种物理量——**反相求和节点的电压反馈约束**。

---

# 五、先做一个非常重要的坐标变换

对每一对 `e/f` 定义：

\[
v_c=\frac{v_e+v_f}{2},
\qquad
v_d=v_e-v_f
\]

\[
i_c=i_e+i_f,
\qquad
i_d=\frac{i_e-i_f}{2}
\]

这个定义满足功率共轭关系：

\[
v_ei_e+v_fi_f
=
v_ci_c+v_di_d.
\]

正常闭合反馈线的约束正好是：

\[
v_d=0,\qquad i_c=0.
\]

因此20端口变换以后，如果写成

\[
\begin{bmatrix}
i_c\\
i_d
\end{bmatrix}
=
\begin{bmatrix}
Y_{cc}&Y_{cd}\\
Y_{dc}&Y_{dd}
\end{bmatrix}
\begin{bmatrix}
v_c\\
v_d
\end{bmatrix},
\]

那么**完整闭合系统的10×10特征端口矩阵就是**

\[
\boxed{G_c(s)=Y_{cc}(s)}
\]

而不是人为选出来的 `Yee+Yff` 参考分母。

这是下一轮的主数学对象。

---

# 六、原 `σmin(I+D^-1A)` 不再当稳定门

原公式

\[
G=(Y_{ee}+Y_{ff})+(Y_{ef}+Y_{fe})
\]

当然可以写成

\[
G=D(I+D^{-1}A),
\]

所以原来的矩阵不是“代数算错”。

问题是：

**这个D是谁？**

如果不能证明 `D` 对应的参考系统稳定、合适且归一化有物理意义，那么：

- eigenvalue的意义不完整；
- singular value受变量尺度影响；
- `0.20`没有可以对应的物理不确定性集合。

多环return difference的singular value确实可以用于鲁棒性研究，但它依赖明确的回路定义、尺度及不确定性范数，不能先拿一个未资格参考矩阵再把某个singular value阈值解释成绝对稳定门。:chatgpt-content-reference{index="1"}

---

# 七、下一包的硬稳定判据改为“广义Nyquist不变量”，sigma降级为辅助指标

## 主判据

下一轮要建立一个**明确稳定的参考系统** \(G_0(s)\)，然后研究

\[
R(s)=G_0^{-1}(s)G_c(s).
\]

但实现时：

**禁止直接数值算 `inv(G0)@Gc`。**

采用广义特征值/QZ：

\[
G_c(s)x
=
\mu(s)G_0(s)x.
\]

于是：

\[
\mu_i(s)
\]

是参考闭合到真实闭合的广义特征轨迹，而且

\[
\det R
=
\frac{\det G_c}{\det G_0}
=
\prod_i\mu_i.
\]

真正用于稳定性判定的是：

- `det(R)` 的广义Nyquist绕数；
- \(\mu_i\) 的characteristic loci；
- 是否出现到原点的零穿越。

等价地可以写：

\[
L_c=R-I,
\]

此时 \(\lambda_i(L_c)=\mu_i-1\)，再观察相对于 \(-1\) 的轨迹。

这类“多约束return difference”的路线符合经典多环反馈推广的框架。:chatgpt-content-reference{index="2"}

### singular value以后怎么用

仍然计算：

\[
\sigma_{\min}(R),
\]

但只作为：

`ROBUSTNESS_DIAGNOSTIC`

**不再是本包稳定性硬PASS/FAIL。**

除非以后我们明确传感器/线路/器件的结构化不确定性集合，再谈真正的robust margin。

---

# 八、参考系统G0怎么定：用“十个局部闭环、去掉环间小信号耦合”

这次给明确答案。

对同一个真实DC工作点、同一20端口数据：

\[
G_c=Y_{cc}.
\]

定义：

\[
\boxed{
G_0(s)=
\operatorname{diag}
\left[
(G_c)_{11},
(G_c)_{22},
\dots,
(G_c)_{10,10}
\right]
}
\]

物理解释：

> 十个反馈环都保持自身局部闭合，但把**不同环之间的小信号交叉耦合**归零。

所以：

\[
G_c=G_0+\Delta G.
\]

真正要评估的是**耦合对已经稳定的十个局部环造成了什么变化**，而不是拿一个开放参考去承担巨大DC增益。

### 但是有一个硬条件

这个 \(G_0\) **不能因为定义成对角矩阵就自动称为稳定参考。**

必须资格。

---

# 九、G0资格分三步做

### A. 非交换fixture

当前fixture不够强，因为对角参数较对称。

下一包首先建：

- 一个2×2非正规、不对称、非交换、已知稳定系统；
- 一个2×2或3×3已知含RHP闭环极点的系统；
- 一个3×3不对称稳定系统。

必须事先有解析或独立state-space真值。

新算法必须：

- 稳定fixture判稳定；
- 不稳定fixture判不稳定；
- 已知pole位置与结果一致；
- 把端口任意缩放 \(10^{-3}\)、\(1\)、\(10^{3}\) 后，稳定结论和广义Nyquist绕数不变。

**如果算法随端口量纲改变稳定结论，方法直接FAIL。**

### B. N=1退化

对于四种实际环类别：

- VCM
- VEXC
- ROW
- TIA

当矩阵只剩一个环时，必须退化到已经接受的Tian/Y结果：

- fc差 ≤10%
- PM差 ≤5%

否则方法FAIL。

### C. 全网标量Schur交叉

在完整10环矩阵中，选：

- VCM
- VEXC
- ROW0
- TIA0

把另外9个反馈闭合，通过Schur消元得到目标环的等效2端口。

再与**真实完整网络、只测试该一个环的Tian双注入**比较。

不能只拿过去的独立单环fixture比较。

这一步通过后才可以写：

`FULL_NETWORK_PORT_CUT_QUALIFIED`

---

# 十、低频conditioning怎么处理——不能删低频

低频至少覆盖：

\[
0.01,\ 0.1,\ 1,\ 10\ {\rm Hz}
\]

一直到300 MHz。

必须验证低频渐近趋势。

### 禁止

- `condition > 1e12` 就把频点删除；
- 把“可信频带从66.9 Hz开始”直接用作稳定结论；
- 用频率相关的任意归一化把低频sigma抬高。

### 允许

使用**固定、频率无关**的正对角变量尺度：

\[
v'=S_vv,\qquad i'=S_i i
\]

并保持功率共轭。

尺度在看MIMO结果前冻结，整个频率、所有状态都不能再改。

实际计算：

- generalized eigenvalue用QZ；
- determinant用LU/log-det；
- 不直接求大条件数矩阵逆。

同时至少记录：

- backward residual；
- `cond(G0)`；
- `cond(Gc)`；
- generalized eigenvalue condition；
- 两种测试拓扑的复数矩阵差异。

如果某低频点在双精度下仍不可资格：

`LOW_FREQUENCY_NUMERICAL_HOLD`

不是把它删掉后PASS。

---

# 十一、实际重复列这次不再只靠对称性

当前用8个代表激励恢复20列，这是可以做探索的，但**硬门不够**。

下一包：

至少实际再测：

- ROW0 / ROW1；
- TIA0 / TIA1；

两组真实重复列。

与对称恢复列比较。

门槛：

- 主要响应区域复数列范数差 ≤0.5%；
- 接近零的量采用单独absolute floor，禁止相对误差爆炸误判。

如果不通过，**放弃对称重建，实际测完全部列**。

无需回来问。

---

# 十二、现在那个0.00994到底怎么解释

正式写法如下：

> `σmin≈0.00994@1Hz` 是当前 `D=Yee+Yff` 归一化下、且参考/数值条件尚未资格的**低频return-difference numerical robustness flag**。

它：

**不是PASS。**

也：

**不是“电路已物理失稳”的FAIL。**

目前同时存在：

- open-port重建条件数约 \(8.98\times10^{29}\)；
- D条件数约 \(5.85\times10^{18}\)；
- hybrid重建条件数约 \(2.30\times10^{17}\)；
- 两种拓扑却给出接近的sigma。

这恰恰说明：

> 方法一致性比之前好，但“这个对象是否是我们真正需要的稳定性对象”仍没资格。

下一包如果新的 **G0/QZ/determinant** 结果也在1 Hz出现真实接近奇异，并且：

- 端口尺度不变性通过；
- 两种拓扑通过；
- full-network单环cross-check通过；

那时才把低频问题升级为**真实耦合稳定性风险**。

---

# 十三、7宏模型下一轮怎么跑

MIMO方法通过以后立刻做，不再额外请示。

沿用上一裁定：

`t_switch=3 µs`

`t_end≈353 µs`

真正pre-switch OP作为初值。

六个核心case：

- 4row+1TIA × all800
- 4row+1TIA × all8000
- 4row+1TIA × high-target
- 1row+4TIA × all800
- 1row+4TIA × all8000
- 1row+4TIA × high-target

判据：

- 切换300 µs后有效采样残余≤100 µV；
- 无削顶；
- 无增长振荡；
- reference取本case后段实际宏模型值；
- Gear结果必须与MIMO小信号及已有trap局部case方向一致。

不要求32个完整帧边沿。

只验证这个状态切换后的有效窗口。

---

# 十四、4.75/5.25 V不再让全十宏OP的数值问题无限堵死原生图

全10宏4.75/5.25如果可以continuation得到，当然保留。

但如果仍数值失败，只要以下三条同时通过：

1. 理想/解析DC全阵列角点无削顶；
2. 单环/分区原厂宏模型在4.75和5.25 V正常工作；
3. 5 V完整MIMO稳定门通过；

允许R2.1原生进入，标：

`FULL_MONOLITHIC_SUPPLY_ENDPOINT_NUMERICAL_HOLD`

而不是永远卡住。

但是如果任何真实求解出来的4.75/5.25 case显示：

- 输出顶轨；
- 输入共模违规；
- 正常偏置错误；

仍然是科学STOP。

---

# 十五、RESET裁定保持收敛，不再抢占主线

继续接受：

`RESET_DIRECT_PATH_25C_DESIGN_PASS`

正常接口定义仍然是：

**active-low OD/OC、Hi-Z释放、VOL≤0.4 V。**

20–30°C钳位件问题下一包最多自动查两个具有明确**保证最大漏电温度数据**的低泄漏器件。

若找到，允许替换NRST钳位。

若找不到：

保留BAT54S，同时标：

`RESET_20_30C_COMPONENT_LEAKAGE_HOLD`

**这不阻止R2.1审查原理图。**

但继续阻止bench正式放行。

### ±5 V域

仍然定义为：

**单故障生存性**

不是正常RESET功能。

包括：

- ±5 V；
- 掉电回灌；
- 60 s热；
- MCU绝对最大；
- 钳位温漂。

全部仍在：

`FAULT_PROTECTION_HOLD`

不因为解析1 kΩ限流就宣称通过。

---

# 十六、唯一下一包

## 包名

`SCIENCE_ADK5556_4X4_R21_INVARIANT_MIMO_AND_NATIVE_ECO_FINALIZATION_V1`

目标：

> **用经过资格、尺度不变的MIMO方法取代旧D/sigma硬门；闭合七宏短窗；条件满足后直接做R2.1原生ECO。**

不再重新选OPA/ADC，不扫第三轮补偿，不新建第二套状态机。

---

# 十七、冻结输入

冻结四个commit：

- R2：`da6ca87b...`
- R2.1 verification：`c13555a...`
- coupled-rootcause：`a3e22772...`
- 本次MIMO：`d152e092...`

冻结：

- OPA4388 / OPAx388原厂模型；
- ngspice47；
- 4×4/8线；
- 0.8–8 kΩ；
- E=0.25 V；
- Rf=4.99 kΩ / Cf=2.2 nF；
- 100 fps；
- 八状态相邻blank；
- progress watchdog；
- Row：1k/4.99k/100pF；
- VCM/VEXC：1k/4.99k/100pF；
- TIA：1k + 22pF。

---

# 十八、新包预算

本包STOP后旧额度关闭。

**新包重新授权360 min。**

| 阶段 | 时间 |
|---|---:|
| P0 MIMO数学/fixture/切口资格 | 90 min |
| P1 全网MIMO＋重复列＋7宏短窗 | 110 min |
| P2 RESET/协议及误差最终收口 | 50 min |
| P3 条件R2.1原生ECO | 80 min |
| P4完整交付 | 30 min |

### 操作额度

- DC/AC/PZ实际分析指令：**≤160**
- MIMO/数值diagnostic属性：**≤24**，必须同步扣对应分析额度
- 正常暂态：**≤48**
- 完整10宏长诊断：**最多1次，≤8 min**
- reset解析：≤96
- protocol回归：≤48
- 新原厂资料：≤8
- reset钳位候选：≤2
- 原生库新增身份：≤4

原生阶段：

- 工作副本1；
- session≤2；
- save≤8；
- capture/audit≤4；
- ERC≤2；
- PDF≤2。

runner必须继续执行**多属性原子预扣**。

sticky scientific STOP不得由剩余额度自动解除。

---

# 十九、进入R2.1原生的最终门

同时达到：

`INVARIANT_MIMO_METHOD_QUALIFIED`

`FULL_NETWORK_PORT_CUT_QUALIFIED`

`MIMO_GENERALIZED_NYQUIST_PASS`

`PARTITIONED_COUPLED_DYNAMIC_PASS`

`RESET_DIRECT_PATH_25C_DESIGN_PASS`

`FAULT_LATENCY_LOGIC_CONTRACT_PASS`

即可直接进入P3。

其中：

- PZ不是独立硬门；
- 原 `σmin<0.20` 不再是独立硬门；
- full 9.6 ms十宏 transient 不是硬门；
- 全10宏4.75/5.25数值收敛不是独立硬门。

---

# 二十、科学STOP条件

只有出现以下情况再回来集中裁定：

1. 非交换稳定/不稳定fixture不能正确分类；
2. 新MIMO结论随端口尺度改变；
3. full-network直接Tian与矩阵Schur结果冲突；
4. 广义Nyquist显示非零错误绕数或明确零穿越；
5. 低频在资格完成后仍真正接近奇异；
6. 7宏模型出现增长振荡；
7. 300 µs /100 µV冻结候选失败；
8. 必须改OPA/ADC、E、Rf或100 fps；
9. 新360min或任一硬额度用尽。

否则Codex自行推进到R2.1原生，不再为普通数学实现、矩阵缩放、重复列、有限retry、CSV/PDF局部修正逐条问我。

---

## 最后总结

这一次STOP是有价值的。

**我们现在知道问题不在“已经发现电路失稳”，而在“第一版MIMO稳定性度量本身没有完成参考系统和归一化资格”。**

这也是为什么我不接受把0.00994直接解释成危险，也不接受简单删掉1–60 Hz。

下一轮要把硬判断从：

> “一个病态D归一化后的singular value”

升级成：

> **统一反馈切口 → power-conjugate坐标 → 资格过的局部闭环参考 → generalized eigenvalue / determinant Nyquist → 7宏短暂态。**

经典多环反馈理论本来就强调一组反馈约束及return-difference，而singular value更适合在已明确定义的MIMO回路和范数下做鲁棒性分析。:chatgpt-content-reference{index="3"}

**按这个06号包继续执行。** 如果这一轮顺利，下一次应该不是第五次讨论MIMO定义，而是直接拿 **R2.1原生工程、冷重开审计和剩余HOLD清单**回来。
