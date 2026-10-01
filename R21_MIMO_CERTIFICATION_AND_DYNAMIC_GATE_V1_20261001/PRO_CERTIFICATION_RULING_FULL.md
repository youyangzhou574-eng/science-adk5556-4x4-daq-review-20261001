我看完这次 R21_INVARIANT 包的结论了。先给结论：

**这一步是正确的 STOP，不是失败。现在真正的问题已经从“电路稳不稳定”转变成“如何定义一个数学上有物理意义的多环稳定参考”。**

目前不要进原生 ECO，也不要继续堆 transient。下一步必须先把 MIMO 稳定性证明路线闭合。

---

# 一、当前状态统一裁定

包：

`SCIENCE_ADK5556_4X4_R21_INVARIANT_MIMO_AND_NATIVE_ECO_FINALIZATION_V1`

状态：

```
INVARIANT_MIMO_METHOD_HOLD
DYNAMIC_VALIDATION_NOT_ENTERED
NATIVE_ECO_NOT_ENTERED
BENCH_NOT_RELEASED
```

---

## 已接受

### 1. 旧 sigma 门正式废除

接受 06 号裁定：

\[
\sigma_{\min}(I+D^{-1}A)=0.00994
\]

不再作为稳定 FAIL。

原因：

当前：

\[
D=Y_{ee}+Y_{ff}
\]

没有证明它是：

- 稳定参考系统；
- 物理闭合系统；
- 与实际反馈不确定性对应的基准。

所以这个 sigma 只能叫：

> 数值诊断指标

不能叫：

> 稳定裕量。

这一点本包完成。

---

### 2. 对称重建路线失败，接受真实20列测量

这是重要结果。

之前依赖：

- ROW/TIA结构对称；
- 少量激励恢复完整矩阵。

现在实际重复列误差：

约：

\[
8.83\%
\]

说明：

这个系统虽然拓扑对称，但小信号行为并不严格对称。

因此后续冻结：

```
NO_SYMMETRY_RECONSTRUCTION
```

以后：

- 10个反馈端口；
- 20列Y矩阵；

全部必须来自真实测量。

这是一个很好的闭环。

---

### 3. QZ路线方向正确，但参考系统没有资格

本次：

三个解析fixture：

- 稳定；
- 不稳定；
- 非交换；

已经证明：

QZ/LU工具链可以工作。

但是：

真实电路：

\[
G_c
\]

对应的：

\[
G_0
\]

没有定义完成。

所以不能继续。

---

# 二、下一步唯一数学路线

我裁定：

不要再使用：

\[
G_0=\operatorname{diag}(G_c)
\]

作为最终方案。

原因：

这个方案虽然直观，但仍存在问题：

如果某一个局部环本身不稳定：

diag出来的G0就是假的参考。

你已经自己发现：

> N=1时Gc/G0=1，R-I=0

这个结果说明：

如果参考定义不对，会得到一个没有信息量的 return difference。

---

# 三、唯一接受的 G0 定义

下一包采用：

## 层级参考系统

不是直接拆diag。

定义：

完整闭合小信号系统：

\[
G_c(s)
\]


构造三个层级：

---

## Level 0：单环物理参考

10个反馈环分别：

- VCM
- VEXC
- ROW0~3
- TIA0~3


每个环：

保持：

- 原运放；
- 原反馈；
- 原负载；

只打开该环。


得到：

\[
G_i(s)
\]


必须证明：

每一个：

\[
G_i
\]

稳定。

方法：

Tian/Y端口。

这是单环资格。

---

## Level 1：块对角参考

不是10×10 diag。

而是：

\[
G_0=
\begin{bmatrix}
G_{ROW}&0&0\\
0&G_{TIA}&0\\
0&0&G_{REF}
\end{bmatrix}
\]

其中：

ROW block：

4×4

TIA block：

4×4

VCM/VEXC：

2×2


为什么？

因为：

ROW之间天然共享：

- VCM；
- VEXC；

TIA之间共享：

- ADC；
- VCM。


完全拆成10个单环会破坏物理耦合。

---

## Level 2：完整系统

\[
G_c=G_0+\Delta G
\]


然后：

\[
R(s)=G_0^{-1}G_c
\]

但是：

禁止直接矩阵求逆。


使用：

generalized eigenvalue：

\[
G_cx=\mu G_0x
\]


观察：

\[
\mu_i(j\omega)
\]


---

# 四、稳定证书要求

下一包不再看：

单个 sigma。

必须同时满足：

---

## 条件1：参考稳定

证明：

\[
G_0
\]

没有RHP pole。


来源：

- 单环Tian；
- block PZ；
- state-space pole。

---

## 条件2：广义Nyquist

计算：

\[
\det(G_c/G_0)
\]


要求：

绕数：

\[
N=0
\]


并且：

没有：

- 穿过0；
- 穿过负实轴危险区域。


---

## 条件3：尺度不变

必须做：

端口缩放：

\[
S_v,S_i
\]

例如：

10^-3

1

10^3


结果：

稳定判断必须不变。


否则：

方法 FAIL。

---

# 五、TIA loaded/direct问题裁定

这里需要分开。

现在：

loaded 2port：

PASS。

direct series/shunt：

FAIL。

不要混。

原因：

TIA存在：

- 输入10k；
- Rf；
- Cf；
- ADC RC；
- 输出隔离。


所以：

真正物理环不是简单2port。

下一包要求：

建立两个模型：

---

## Model A

真实loaded：

包含：

- ADC100Ω
- ADC10nF
- COL网络


用于：

系统稳定。

---

## Model B

direct：

只用于：

方法交叉。

不能作为系统稳定证书。


所以：

```
directSeriesShuntQualified=false
```

继续保持。

---

# 六、低频问题怎么处理

这个必须明确：

不能删低频。

现在：

\[
cond(G_c)\approx6.6\times10^{18}
\]

不是小问题。

下一包：

频率：

至少：

\[
10^{-2}\sim300MHz
\]

低频：

必须包含：

0.01Hz

0.1Hz

1Hz

10Hz


---

处理方式：

不是：

“忽略低频”。

而是：

先检查：

### 1.

是不是：

参考矩阵导致。


### 2.

是不是：

端口尺度。


### 3.

是不是：

真正存在慢模态。


如果最终：

QZ特征在低频接近奇异：

那才进入：

真实耦合风险。

---

# 七、下一包唯一任务

包名：

```
SCIENCE_ADK5556_4X4_R21_MIMO_CERTIFICATION_AND_DYNAMIC_GATE_V1
```

目标：

不是原生。

目标只有三个：

---

## Task 1

完成：

\[
G_0
\]

资格。

输出：

- 10单环证书；
- ROW/TIA block证书；
- reference pole。

---

## Task 2

完成：

generalized Nyquist。


输出：

- μ轨迹；
- det绕数；
- QZ condition；
- scale invariance。


---

## Task 3

如果通过：

进入：

7宏短窗。

否则停止。

---

# 八、预算批准

你的480 min申请可以接受。

但重新定义：

不是“做完全部”。

而是：

## P0 方法资格

90 min

- G0构造
- fixture
- QZ验证


## P1 MIMO

150 min

- 全20列矩阵
- block reference
- Nyquist


## P2 动态

100 min

只有P1通过才进入：

- 7宏
- 300us


## P3 原生准备

仅条件开启：

80 min


## P4交付

30 min


---

额度：

|项目|额度|
|-|-:|
|OP/AC/PZ|192|
|MIMO diagnostic|32|
|Transient|64|
|Long transient|1|
|Reset|96|
|Protocol|48|
|Sources|8|
|Candidate|2|

保持：

- 不安装新执行器；
- 不换模型；
- 不改OPA/Rf/Cf；
- 不PCB；
- 不bench。

---

# 九、进入动态和原生的最终门

必须：

```
MIMO_REFERENCE_QUALIFIED

+
GENERALIZED_NYQUIST_PASS

+
FULL_NETWORK_PORT_CUT_PASS

+
TIA_LOADED_DOMAIN_CONFIRMED
```

之后：

才进入：

```
PARTITIONED_COUPLED_DYNAMIC
```

动态通过：

再进入：

```
R2.1_NATIVE_ECO
```

---

# 十、当前最重要判断

这一轮其实已经把最难的问题定位了。

之前：

> “是不是电路不稳定？”

现在：

> “我们有没有建立一个正确的多环稳定参考？”

这是两个完全不同的问题。

目前证据支持：

- 电路可能存在复杂耦合；
- 数值方法需要修正；
- 没有证据证明失稳。

所以停止是合理的。

下一步不要继续跑更多 SPICE。

先把：

**物理反馈切口 → 合格参考系统 → 广义Nyquist证书**

闭合。

这一步通过以后，后面的7宏和R2.1原生才有意义。
