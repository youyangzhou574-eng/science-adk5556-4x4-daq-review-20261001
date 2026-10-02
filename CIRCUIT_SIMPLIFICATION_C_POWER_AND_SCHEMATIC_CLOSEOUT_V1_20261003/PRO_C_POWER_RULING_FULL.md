我把 `a7b505...` 的完整阻断回执重新核了一遍。这个 STOP 是合理的：**不能因为 LP5912 “1 µF 就能工作”就把它扩大成“带 ADS8684 大容量 DVDD 网络也已取得资格”**；同样，当前局部 AC/TRAN 也不足以删除 12 个 TIA 补偿器件。

但这个阻断不需要退回 A，也不需要修求解器。**C 继续作为唯一方向，电源链换一个更合适的实现即可。**

## 1. C版3.3 V电源：改用 TPS7A3701，不再用 LP5912

我指定下一版使用：

**`TPS7A3701DRVT`**（小卷装；大卷对应 `TPS7A3701DRVR`）

它是 1 A 可调 LDO，输入 2.2–5.5 V，具有反向电流保护；最关键的是 TI 明确规定其**稳定条件是 1 µF 或更大的输出电容**，而不是 LP5912 当前资料里造成歧义的有限电容范围。TI还明确说明其 NMOS 拓扑对输出电容值和 ESR 相对不敏感。:chatgpt-content-reference{index="0"}

3.3 V采用 TI 官方给出的推荐分压：

\[
R_1=52.3\,k\Omega,\qquad R_2=30.1\,k\Omega
\]

由官方公式

\[
V_{OUT}=1.204\left(1+\frac{R_1}{R_2}\right)
\]

得到约 **3.296 V**；这组阻值就是 TI 数据表给出的3.3 V推荐组合。:chatgpt-content-reference{index="1"}

这比继续纠结 LP5912 更合适，因为我们真正的问题不是需要超低噪声LDO，而是：

**5 V→3.3 V、能挂较大的DVDD储能电容、能阻止板OFF时3.3 V接口反灌回5 V，同时不让电源设计变得更复杂。**

TPS7A37正好覆盖这几个核心条件。

---

## 2. 3.3 V电容：这轮先不删两个22 µF

这里我改变上一版的精简策略。

下一版 C 原理图中，先继续保留：

- `C_DVDD34A = 22 µF`
- `C_DVDD34B = 22 µF`
- ADS8684 DVDD近端的小容量去耦；
- MCU及数字IC各自100 nF近端去耦。

原因是 ADS8684 的 DVDD 要求至少有足够的有效电容，而我们目前缺的是**指定MLCC在3.3 V DC bias和温度下的真实 Ceff**，不是名义容量。ADS8684本身规定数字电源工作范围1.65–5.25 V，模拟电源4.75–5.25 V；供电超出推荐区间不能再宣称精度有效。:chatgpt-content-reference{index="2"}

而 TPS7A37 明确允许 **1 µF或更大**的输出电容，所以保留44 µF名义容量不再与LDO稳定性合同直接冲突。:chatgpt-content-reference{index="3"}

因此新的策略是：

> **先让电源架构成立，不让“少一颗22 µF”继续卡整个C方案。**

后面如果准确曲线证明单颗22 µF在最坏偏压/温度/老化后仍满足ADS8684的有效容量要求，再删 `C_DVDD34B`。

如果单颗22 µF不够，备选是一颗 **Murata GRM32ER71A476KE15L，47 µF / 10 V / X7R / 1210**；Murata和JLC都存在该准确料号，JLC编号为C84494，但其DC-bias有效容量仍要取真实characteristic data后才能替代两颗22 µF。:chatgpt-content-reference{index="4"}

所以：

**此次ECO不以删除DVDD第二颗22 µF为门槛。**

---

# 3. 最终C版电源框图

我建议冻结成：

```text
J1
5.0 V ±5%
 │
 ▼
LM73100  U9
反接 / 反灌 / OVLO / power-path
 │
 ├────────────── V5 ─────→ OPA / ADC AVDD / REF 等
 │
 ├→ TPS3890 U11
 │   监控 V5
 │
 ▼
TPS7A3701
5 V → 3.3 V
reverse-current protected
 │
 ├────────────── V3V3 → MCU / ADC DVDD / logic
 │
 └→ TPS3890 U12
     监控 V3V3
```

也就是说，之前 C 中试图把 **U12也删掉** 的方案撤回。

最终保留：

- U9：5 V入口硬件保护；
- U11：5 V精密监督；
- TPS7A3701：3.3 V LDO + reverse current protection；
- U12：3.3 V精密监督。

这仍然比旧板：

`U8 + U9 + U10 + U11 + U12 + U13 + U14 + U15`

简单很多，而且不靠模糊的 PG 行为冒险。

TPS3890本身就是1%阈值精度、带可设延迟的开漏RESET supervisor。:chatgpt-content-reference{index="5"}

---

# 4. U9 OVLO现在正式给出数值

旧：

\[
10k/(10k+1k+1k)
\]

实际OVLO约 **7.2 V**，对当前5 V系统显然太高。

C版改成：

\[
R_{\rm TOP}=34.8k\Omega,\qquad
R_{\rm BOT}=10.0k\Omega
\]

两颗都要求：

**0.1%，≤25 ppm/°C。**

LM73100的OVLO rising threshold数据表范围为：

\[
1.183\sim1.223V
\]

典型1.2 V。:chatgpt-content-reference{index="6"}

因此标称：

\[
V_{\rm OVLO}
=
1.2\left(1+\frac{34.8}{10}\right)
=
5.376V
\]

把0.1%电阻容差和器件阈值范围计入后，OVLO rising大约在：

\[
\boxed{5.29\sim5.49V}
\]

LM73100 OVLO输入漏电最大约±0.1 µA，再带来的输入门限移动只有数mV量级，不改变这个裁定。:chatgpt-content-reference{index="7"}

所以新的**输入合同**正式定义为：

> **J1正常供电必须为稳定5 V ±5%，即4.75–5.25 V。**

5.25 V以上：

- **不属于有效测量工作区；**
- 数据立即视为无效；
- U9负责在约5.29–5.49 V进入硬件OVLO。

这一点很重要。

ADS8684推荐AVDD最大就是 **5.25 V**，但绝对最大值是7 V，所以 U9 的5.3～5.5 V量级OVLO是**故障损伤保护**，不是拿来扩展ADC的正常工作电压。:chatgpt-content-reference{index="8"}

这个区分以后必须写进图纸。

---

# 5. U11/U12门限保留，但把长电阻链压成两颗

### V5监督 U11

使用：

\[
R_{TOP}=24.0k,\qquad R_{BOT}=7.50k
\]

等效原来的32k/10k比例。

TPS389001可调阈值基准约1.15 V，因此：

\[
V_{TH}\approx1.15
\left(1+\frac{24}{7.5}\right)
\approx4.83V
\]

即 V5下降至约4.83 V开始撤销系统许可。

### V3V3监督 U12

使用：

\[
R_{TOP}=17.0k,\qquad R_{BOT}=10.0k
\]

得到约：

\[
V_{TH}\approx3.105V
\]

两者仍采用TPS3890的open-drain RESET wired-AND方式。

这保留原来“**5V和3.3V都必须合格**”的安全语义，但把很多串联拼阻删掉。TPS3890提供1%级阈值精度。:chatgpt-content-reference{index="9"}

---

# 6. OFF / EN / RESET合同现在也明确下来

这部分我不再使用“LP5912 PG应该能搞定”这种不闭合逻辑。

### Board OFF + debugger/UART ON

**继续视为必须支持的状态。**

所以这轮保持：

- J3/J4六条4.99 kΩ限流路径；
- NRST外部路径1 kΩ；
- Schottky rail-clamp语义；
- V3V3上的100 Ω bleed；
- 不默认改成33 Ω；
- 不默认DNP bleed。

TPS7A37自身又提供低反向泄漏/反向电流保护，进一步阻止V3V3回灌V5。:chatgpt-content-reference{index="10"}

以六条3.3 V外部信号同时通过约4.99 kΩ + Schottky向板内注入的极端静态估算，100 Ω bleed会把V3V3残余电位压在大约**几百mV量级**，而不是被外部接口抬到3.3 V附近。因此这个旧保护逻辑暂时有保留价值。

这不等于已做bench fault PASS，但结构上有明确作用。

---

### MCU reset

U11、U12的open-drain RESET输出共同形成：

**`PWR_OK` / reset qualification node**

只要任一电源不合格：

\[
NRST=LOW
\]

MCU硬复位。

TPS3890在自身VDD低于POR后输出最终会进入未定义，这是数据表明确限制，因此不能依赖它在0 V附近“永远拉低”。:chatgpt-content-reference{index="11"}

但是我们的board-OFF外部注入另由 **4.99 kΩ + Schottky + 100 Ω bleed** 限制，这两个机制不能混为一谈。

---

### ROW mux默认状态

不再使用原来的U13/U14/U15三颗逻辑。

TMUX的：

- A0下拉；
- A1下拉；
- **EN强制100 kΩ下拉。**

MCU GPIO只有在：

1. 两路supervisor释放NRST；
2. MCU启动完成；
3. ADC/reference初始化完成；
4. firmware显式进入MEASURE状态；

之后才能把 `ROW_MUX_EN` 拉高。

当 PWR_OK掉下去，MCU被硬复位，其GPIO重新成为高阻，外部EN下拉立即把ROW mux关闭。

因此不需要额外再加一颗AND gate。

这个状态链比原来两颗74LVC08加一颗1G17清楚很多：

```text
power bad
   ↓
NRST low
   ↓
MCU GPIO Hi-Z
   ↓
100k EN pulldown
   ↓
ROW mux OFF
```

---

# 7. 当前局部SPICE究竟允许我们删什么

这里我把界限正式定下来。

现有结果**可以支持**两个架构决策：

**① 可以继续采用“一个ROW运放 + dual 4:1 remote-feedback mux”作为C原理图候选。**

四个800 Ω并联时ROW静态值约2.25000019 V，且blank→enable局部恢复在约26 µs量级。这足以说明该结构值得继续工程化，不需要退回四行OPA4388。

**② 可以把“标准直接TIA”画成C版候选拓扑继续验证。**

局部AC结果约2.24 MHz交越、约79.6° PM，局部TRAN末段误差13–18 µV，说明直接TIA并没有在这个局部模型中暴露明显稳定性问题。

但：

> **这两个结果都不允许现在把 `R_COL_SENSE0..3 + R_TIA_ISO0..3 + C_TIA_HF0..3` 这12颗宣布正式删除。**

因为现有模型缺：

- 完整16R共享矩阵有效解；
- 三个未选ROW真实浮动/切换状态；
- FFC寄生；
- REF3025真实输出阻抗；
- ADS8684动态采样负载；
- 全矩阵切换串扰；
- 有效PZ结果。

因此这12颗的状态定为：

**`CANDIDATE_DELETE / QUALIFICATION_HOLD`**

而不是 `KEEP_FOREVER`，也不是 `DELETE_APPROVED`。

在下一版原理图里可以把直接TIA作为主绘制拓扑，但应保留**可恢复补偿的DNP工程位置**，直到全矩阵/bench证明不需要。

这样板上实际装配可以很简洁，同时仍有实验回退能力。

---

# 8. full-matrix和PZ失败怎么处理

不修求解器，也不再开一个“证明工具资格”分支。

### full-matrix OP

状态固定为：

**`NUMERICAL_UNRESOLVED`**

不是：

- physical unstable；
- physical stable；
- PASS；
- FAIL。

所以它只阻止三件事：

> **不能宣布≤1%精度；不能宣布≤0.2%重复性；不能宣布100 fps系统级成立。**

它**不阻止**我们画C原理图工作副本。

---

### PZ

`input signal shorted` 那个PZ case固定为：

**`PZ_INVALID_PORT_SETUP / NO_RESULT`**

`poles.txt`不得再使用。

但已有独立AC loop injection有有效结果，因此：

> **不要求PZ成功作为进入C原理图ECO的额外门。**

最终稳定性仍靠：

**AC loop + TRAN + 后续bench step response**

形成证据链即可。

这符合实际模拟电路工程，不需要为了有一个“PZ PASS”把时间花在求解器上。

---

# 9. C的器件数目标重新调整

由于我现在明确：

- 保留U12；
- TPS7A37需要2个反馈电阻；
- 保留目前双22 µF直到Ceff闭合；

所以之前的 **83件** 不再作为合理预期。

现在更可信的是：

\[
\boxed{\text{约90件上下}}
\]

大致 **88–94个实际贴装器件**，最终以ECO后的BOM实数为准。

从176件降到约90件，依旧接近：

\[
49\%
\]

的器件数量下降。

而且这次减少的是：

- 4个ROW运放通道对应的大量外围；
- 一整级3.3V LM73100；
- 两颗74LVC08；
- 一颗1G17；
- VEXC buffer；
- 大量串联分压器；
- 重复模拟补偿的候选件；

不是为了凑数字硬删安全电容。

我认为这个版本比“强行83”更像真正能做出来的科研测量板。

---

# 10. 下一包300 min：批准，但范围稍作修改

我批准：

**`CIRCUIT-SIMPLIFICATION-C-POWER-AND-SCHEMATIC-CLOSEOUT-V1`**

**总预算300 min。**

| 项目 | 范围 |
|---|---|
| 电源/料号闭合 | ≤60 min；官方新增资料≤4；LDO候选≤2，但 **TPS7A3701为主方案** |
| C原理图working copy | ≤120 min；copy≤1、session≤2、save≤6、capture≤6、net audit≤4、ERC≤2、PDF≤1 |
| 有限电气验证 | ≤60 min；OP/AC/PZ合计≤16、TRAN≤4，每次≤180 s，实际启动即扣次数 |
| 完整交付 | ≤60 min；真实BOM计数、net diff、风险表、仿真结果、未闭合项 |
| placement | **0** |
| native PCB搬件 | **0** |
| routing / copper / Gerber | **0** |
| manufacturing / procurement / bench | **0** |
| local Git / system changes | **0** |

本包**允许真正修改隔离的C原理图working copy**，不再是read-only。

必须按本回复冻结的电源方向实施：

> **U9 LM73100 → V5 → TPS7A3701 → V3V3；U11监V5、U12监V3V3。**

LP5912从C主方案退出，不再花时间证明它。

本包有限TRAN优先给：

**5 V正常启动 → 3.3 V启动、brownout、board-OFF/debug-ON backfeed、ROW enable/reset联锁**。

如果器件宏模型覆盖不了OFF反灌，就做解析最坏边界并明确 `HOLD`，不为了获得绿色结果修改宏。

完整16R矩阵和PZ**不要求在这个包重跑**。旧失败继续作为HOLD证据；不要浪费300 min修solver。

原理图关闭后，如果电源/ERC/net audit无新的Important问题，就提交C版完整BOM和原理图PDF给我审。**仍然不进入PCB。**

这一轮的目标已经很清楚：先把“约90件的C电路”真正画成一个电气自洽的原理图，而不是继续围绕83这个估算数字做删件游戏。
