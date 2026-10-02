这条新增要求我已经并入 02，不会先执行旧的 ECO-A。重新按“**合理最简，而不是只删几颗电阻**”审了一遍后，我的统一裁定是：

> **A 保留为低风险后备路线；主路线改为 C。**  
> C 不再锁死现有 15 个 IC，也不锁死 256 effective + 32 dummy 的旧采样合同。  
> 但 C **继续保留 4 路列 TIA + ADS8684**，重点把“4 个行运放、行选择方式、VCM/VEXC缓冲、电源链、监督逻辑和外围保护”重新集成。
>
> 这样不是从 176 降到 145，而是有依据地做到**约 83 个贴装器件**，约减少 **53%**。这是我认为在你现有精度、8线矩阵和100 fps要求下，风险与复杂度之间更合理的位置。

这里的 **83 是工程候选，不是性能 PASS**；最终仍需有限 SPICE/数值资格确认。

---

# 一、这次找到的关键案例，确实说明我们的电路还能大幅简化

最关键的不是 RTD 参考板，而是一篇**和我们拓扑几乎一模一样的 4×4 无单元开关被动电阻矩阵**。

### 1. Kim 等：4×4共享ROW/COL，只用一个行驱动运放

2016 年 Sensors 论文 *High-Accuracy, Compact Scanning Method and Circuit for Resistive Sensor Arrays* 研究的就是共享行列的无源电阻阵列。作者比较了三种零电位扫描：

- Type I：数字buffer直接驱行，简单，但开关/驱动器 `RON` 引起误差；
- Type II：**每一行一个运放**，精度高，但元件多；
- Type III：**所有行共用一个运放**，再用两组同步开关分别切换“输出路径”和“反馈采样路径”。

关键之处是第二组开关把**选中行真实电压反馈到运放反相输入**。因此即使输出开关有 `RON`，压降也处在反馈环内被补偿。

他们真的做了 **4×4 电阻阵列 PCB**：

- Type I 最大误差达到 30.7%；
- 每行独立运放的 Type II：约 0.1%；
- **单运放 Type III：同样约 0.1%**；
- Type II 和 Type III 的实测瞬态上升时间基本相同；
- 原型甚至使用 `RON≈125 Ω` 的 CD4051B，仍通过反馈把行电压误差压了下来。:chatgpt-content-reference{index="0"}

这篇文献直接说明：

> **我们现在 U1 用四个 OPA388 通道分别驱 ROW0–3，并不是高精度 4×4 电阻矩阵唯一可靠的实现。可以把4个行运放压缩成1个，而且不是靠猜。**

[原作者论文：High-Accuracy, Compact Scanning Method and Circuit for Resistive Sensor Arrays](https://www.mdpi.com/1424-8220/16/2/155?utm_source=chatgpt.com)

---

### 2. Wu 等：共享行列矩阵真正需要防的是“未选通旁路电流”

另一篇同年的 *An Improved Zero Potential Circuit for Readout of a Two-Dimensional Resistive Sensor Array* 专门分析二维共享ROW/COL阵列中的 **bypass current / crosstalk**。论文指出，简单切换某一条线而没有让未选通电极处于正确电位，会形成经其他电阻单元的旁路电流；作者甚至额外增加运放和采样通道来补偿这种旁路误差。:chatgpt-content-reference{index="2"}

这说明我们不能为了少器件做成：

`ROW mux → 一个ADC → 完事`

也不能随便把四个列TIA变成一个。

**四列各自保持虚拟VCM的TIA，恰恰是共享行列矩阵消除ghost/crosstalk的重要基础。**

[原作者论文：An Improved Zero Potential Circuit for Readout of a Two-Dimensional Resistive Sensor Array](https://www.mdpi.com/1424-8220/16/12/2070?utm_source=chatgpt.com)

---

### 3. TI ADS8688EVM：ADC周围没有必要像现在这么堆

ADS8688 是我们 ADS8684 的8通道同系列器件。TI 官方 EVM 文档直接提供原理图、BOM、PCB和layout。Figure 8-3 的 ADC 部分采用很常规的本地供电/reference电容和输入RC，没有目前板上那么多重复的大容量电容。:chatgpt-content-reference{index="4"}

不过你 02 里指出得对：

**不能因为EVM只有一颗，就认定我们的两颗22 µF一定多余。**

ADS8684 的有效电容要结合实际 MLCC 型号、DC bias、温漂、老化检查。因此 A/C 都把 ADC capacitance qualification 单独留下，而不是为了凑数量硬删。

[TI ADS8688EVM完整官方手册（含BOM、原理图、Layout）](https://www.ti.com/lit/ug/sbau230c/sbau230c.pdf?utm_source=chatgpt.com)

ADS8684本身仍很适合这个项目：4通道、16 bit、500 kSPS，而且已有集成AFE、1 MΩ输入、可编程量程、±20 V输入保护和片内4.096 V reference。:chatgpt-content-reference{index="6"}

---

# 二、路线 A：低风险精简——现在不再硬说145

A 的原则是：

**测量架构、15 IC和采样方式全部保留，只合并明显重复的外围。**

这一路我重新收紧以后，可靠口径应该是：

| | 原版 | A第一层 | A条件完成 |
|---|---:|---:|---:|
| R | 81 | **60** | 60 |
| C | 59 | 59 | **54** * |
| Protection pkg | 17 | 17 | **14** |
| IC | 15 | 15 | 15 |
| J | 4 | 4 | 4 |
| **总计** | **176** | **155** | **147** |

`*` 五颗大容量电容只有在**准确MLCC有效容量满足ADS8684要求**后才删。

所以 A 应该理解成：

> **155 是明确可推进的一级目标；147 是资格满足后的完整A。**

不是145硬目标。

### A里21颗电阻为什么现在可以比较有把握地处理

固定网表我又核了一遍：

`DIV_SEG1..8`、`U11_DIV1..4`、`U12_DIV1..3`、`U9/U10_OV_M` 全都只存在于自身串联链中，没有别的功能消费者。

而 LM73100 官方数据表本身使用 `PGTH = Open, PG = Open` 作为器件特性测试条件，所以当我们的PG输出本身不使用时，PGTH开放并不是非法工作模式。:chatgpt-content-reference{index="7"}

因此 A 可按：

- `10×10k VEXC链 → 10k/90k`
- U11 `32k/10k`
- U12 `17k/10k`
- U9/U10 OV分压各由 `10k+1k+1k → 10k+2k`
- 未使用PGTH网络移除

处理。

不过 32.0 kΩ、17.0 kΩ 等**最终实际料号、0.1%容差和TCR**仍需要在ECO前冻结；没有合适单颗时宁可采用精密网络，不能为了减少一个placement改阈值。

---

## A的保护不再用“ESD阵列=BAT54S”这种错误等效

02指出这一点完全正确。

纯ESD器件解决的是脉冲；原 BAT54S：

`接口 → 串阻 → Schottky → V3V3/GND`

还构成了**持续过压和板掉电外部驱动的限流/泄流路径**。

因此 A 不采用“7颗BAT54S全部换成2颗TPD4E05U06”作为默认。

更合适的是 **BAT54XY**。它在一个SOT363中集成“两组相互隔离的双Schottky串联结构”，官方应用明确包括 voltage clamping，因此两根信号可共用一个封装，而基本rail-clamp语义仍保留。:chatgpt-content-reference{index="8"}

于是数字接口：

**7 × BAT54S → 4 × BAT54XY**

而不是7→2。

这样 A 全保护版本最终约 **147件**，而不是靠改变安全合同凑145。

---

# 三、路线 C：真正重新做“合理最简”的4×4测阻板

这是我现在推荐的方案。

它不是把 A 再砍一点，而是重新组织功能块。

## 新结构

```text
                      ┌──── REF3025 ─── VCM = 2.500 V
                      │
                      └─ 10k/90k ───── VEXC = 2.250 V
                                         │
                                         ▼
                              ┌──────────────────┐
                              │ 1 × OPA388       │
                              │ remote-feedback  │
                              │ row driver       │
                              └────────┬─────────┘
                                       │
                         ┌─────────────▼─────────────┐
                         │ TMUX1109 dual 4:1         │
                         │ bank A: drive → selected ROW
                         │ bank B: selected ROW → FB │
                         └──────┬────┬────┬────┬─────┘
                                │    │    │    │
J2 FFC 8P                 ROW0 ROW1 ROW2 ROW3
─────────────────────────────────────────────────────
                R00 ... R33  外部4×4被动电阻矩阵
─────────────────────────────────────────────────────
                                │    │    │    │
                               COL0 COL1 COL2 COL3
                                │    │    │    │
                     ┌──────────▼────▼────▼────▼─────┐
                     │ OPA4388：4 × zero-potential TIA│
                     │ 每列 RF || CF                  │
                     └──────────┬────┬────┬────┬─────┘
                                │    │    │    │
                              RC anti-alias / settle
                                │    │    │    │
                     ┌──────────▼────▼────▼────▼─────┐
                     │ ADS8684 16-bit / 500 kSPS     │
                     └───────────────┬───────────────┘
                                     │ SPI
                              STM32G031K8
```

这其实就是把论文 Type III 现代化以后放进我们的板子。

TMUX1109是双4:1 precision mux，两个bank可以共同完成：

- bank A：运放输出 → 选中的ROW；
- bank B：同一ROW → 运放反馈端。

它典型 `RON≈2.5 Ω`，最大on-state leakage约3 nA，break-before-make，连续电流能力30 mA。:chatgpt-content-reference{index="9"}

相比2016论文用的 `RON≈125 Ω` CD4051B，我们这个条件实际上轻松得多。

---

# 四、为什么C可以把U1四行运放变成一个，而不增加明显测量误差

最坏0.8 kΩ情况下，一条选中行同时面对4个0.8 kΩ单元，相当于：

\[
R_{\rm eq}=200\Omega
\]

激励只有：

\[
\Delta V=2.50-2.25=0.25V
\]

所以整条ROW最大静态电流约：

\[
I_{\rm row,max}
=\frac{0.25}{200}
=1.25\,mA
\]

OPA388典型输出能力约60 mA、10 MHz GBW，而且本来就是零漂高精度放大器。:chatgpt-content-reference{index="10"}

TMUX1109允许30 mA连续电流。:chatgpt-content-reference{index="11"}

1.25 mA对两者都非常轻。

最重要的是：

> **TMUX的RON位于闭环内。**

ROW端电压不是简单的：

\[
V_{EXC}-I R_{ON}
\]

而是运放通过sense bank直接观察真正的ROW电压，并调节自身输出使ROW恢复到 VEXC。

这就是原作者Type III为什么能用125 Ω开关仍保持约0.1%实测误差。:chatgpt-content-reference{index="12"}

---

# 五、列端我反而不建议再激进

这里是“真正不能乱删”的核心。

C **继续留4个TIA**。

因为4个COL同时维持在 VCM，是未选中电阻不形成ghost/bypass current的关键条件。相关二维电阻阵列研究明确表明，未选通支路的旁路电流是共享行列架构的基本误差来源。:chatgpt-content-reference{index="13"}

所以我不建议做：

`4列 → 一个模拟MUX → 一个TIA`

这种看似少3个运放的结构。

它会让未选列失去真正的zero-potential constraint，随后必须再增加开关、补偿和算法，反而把最危险的误差引回来。

不过**当前每个TIA外围可以简化**。

现有每列：

`R_COL_SENSE + R_TIA_ISO + C_TIA_HF + RF + CF`

实际上是一套复杂remote-sense补偿。

C先评估退回标准：

```text
               RF
          ┌──/\/\/\──┐
          │          │
COL ──────┴─(-)OPA───┴──── TIA_OUT ─100Ω─→ ADC
          │    │
          │   CF
        (+)
         VCM
```

也就是保留：

- `RF0..3`
- `CF0..3`
- `R_ADC0..3`
- `C_ADC0..3`

而把：

- `R_COL_SENSE0..3`
- `R_TIA_ISO0..3`
- `C_TIA_HF0..3`

列为 **C验证后删除的12个placement**。

这12颗我不会直接删完就宣布稳定，而是必须过AC/PZ + TRAN。

---

# 六、速度上 C 完全不需要再被旧“256+32”绑住

这一点你最新反馈非常关键。

真正需求是：

> **16点 × 100完整帧/s。**

不是“每帧一定做288次SPI转换”。

甚至仅仅旧ADS8684都能500 kSPS。:chatgpt-content-reference{index="14"}

以现在 `RF=4.99 kΩ、CF=2.2 nF` 做一阶量级估计：

\[
f_p \approx
\frac{1}{2\pi R_FC_F}
\approx14.5\,kHz
\]

\[
\tau=R_FC_F\approx11\,\mu s
\]

一阶近似下：

- 到1%：约 **51 µs**
- 到0.1%：约 **76 µs**

所以旧的 **300 µs wait** 本身就相当保守。

C的首个协议候选可以由原来的：

`BLANK0/ROW0/BLANK1/ROW1/...`

改为类似：

```text
GLOBAL BLANK
ROW0
ROW1
ROW2
ROW3
```

每个ROW状态只需满足真实settling以后，再取例如8～16个有效样本/列。

即使暂定：

- 4 ROW；
- 每ROW × 4列 × 8样本；

也只有128个有效ADC结果/frame。

100 fps仅12.8k有效值/s，和ADS8684的500 kSPS不是一个数量级。

具体最后取8、16还是更多，不在现在拍死；由实测/噪声模型决定。

---

# 七、C 的信号幅值也非常合适

现有 ΔV=0.25 V 和 RF=4.99 kΩ可以继续用。

TIA变化幅度：

\[
\Delta V_{TIA}
=
\frac{0.25}{R_S}\times4.99k
\]

得到大约：

| 阻值 | TIA相对VCM变化 |
|---:|---:|
| 0.8 kΩ | 1.559 V |
| 1 kΩ | 1.248 V |
| 7 kΩ | 0.178 V |
| 8 kΩ | 0.156 V |

因此整个0.8–8 kΩ guard band都能放在5 V模拟域内。

即使在最不敏感的约7 kΩ附近：

- 10%阻值变化仍对应约 **16 mV量级**
- 1%变化约 **1.8 mV量级**

ADS8684 16 bit有充足数字分辨率；真正限制因素变成运放噪声、settling、串扰、RF精度和校准，而不是ADC码宽。

所以我不建议为了再少10颗器件，把 ADS8684直接删掉换 STM32 内部12-bit ADC。

STM32G031确实有12-bit ADC和硬件oversampling。:chatgpt-content-reference{index="15"}  
但对你要求的 **≤1% mean error + ≤0.2% sample SD**，尤其7–8 kΩ端，12-bit方案对INL、Vref和噪声余量过紧。减少一个ADC，却重新引入精度风险，不值得。

---

# 八、C 的电源部分还能真正少很多

现在3.3 V这条链：

```text
V5
↓
TPS7A20 (U8)
↓
V3_LDO
↓
LM73100 (U10)
↓
V3V3
↓
TPS3890 (U12)
```

再加 U13/U14/U15 做硬件逻辑联锁。

这对于一块受控实验DAQ来说确实偏重。

我的 C 方案改成：

```text
5V input
  │
 LM73100 U9
 reverse polarity / OVP / reverse blocking
  │
 V5
  ├──── TPS3890 U11 → precise 5V qualification
  │
  └──── LP5912-3.3
        reverse current protection
        soft-start
        output discharge
        PG
        ↓
       V3V3
```

LP5912已经集成：

- reverse-current protection；
- enable；
- power-good；
- output discharge；
- soft-start；
- thermal/short protection；

而且只要求1 µF输入和1 µF输出电容。:chatgpt-content-reference{index="16"}

因此 C 删除：

- U10 LM73100
- U12 TPS3890
- U13 SN74LVC08
- U14 SN74LVC08
- U15 SN74LVC1G17

并以 LP5912 的 PG + STM32自身的 POR/PDR/BOR/PVD完成数字域上电资格。

STM32G031本身确实具备POR/PDR、可编程BOR和PVD，不是依赖软件“猜电压”。:chatgpt-content-reference{index="17"}

但这里保留 U11：

> **5 V模拟域仍由独立1% TPS3890做精密监督。**

TPS3890本身就是1%阈值精度的独立supervisor。:chatgpt-content-reference{index="18"}

所以 C 并没有简单地把所有安全都扔给 MCU。

---

# 九、C为什么可以把U13/U14/U15拿掉

关键不是“软件替代硬件”，而是重新设置**硬件默认安全态**：

- TMUX1109 `EN` 外置下拉；
- A0/A1有确定的下拉；
- MCU未启动时 `EN=0`；
- **所有ROW物理断开，不会误激励任何传感单元**；
- 3.3V达到PG后 MCU才脱离reset；
- MCU完成初始化后才主动使能ROW mux；
- ADC hardware reset可和PG/reset网络关联，同时上电后再执行软件RESET。

因此原来 U14 的“每一行再经过一层AND gate防止MCU乱输出”的功能，改成了：

> **一个硬件EN直接把整个ROW驱动MUX关闭。**

这实际上比四个门电路更直接。

如果你最后坚持要求：

**“即使 MCU 软件完全失控，也必须有独立硬件第二级行禁止”**

那么 C 只需重新加 **1颗硬件gate/buffer**，不会退回原 U13/U14/U15 三颗逻辑。

---

# 十、C接口保护也不是直接砍掉

这里我接受02的修正。

## J2：8线传感器FFC

C必须冻结一条明确合同：

> **J2只允许连接被动电阻阵列，不允许外部有源电源从ROW/COL注入持续DC。**

在这个合同下，J2主要故障是ESD、插拔瞬态和被动传感器异常，而不是“外部5/12/24V持续灌电”。

因此8条J2线可用：

**2 × 4-channel低电容ESD array**

代替当前每个内部运放节点上的10颗BAT54S。

如果将来 J2 要兼容“外部有源传感器/带电驱动”，那这部分必须重新升级，83件目标不适用。

---

## J3/J4：SWD/UART

这里仍保留“板掉电、外部调试器有电”的真实场景。

所以不使用纯ESD TVS冒充rail clamp。

采用：

**7 BAT54S → 4 BAT54XY**

保留Schottky rail-clamp机制。BAT54XY本来就是两个隔离的双肖特基系列，官方用途包含voltage clamping。:chatgpt-content-reference{index="19"}

现有2个100 Ω BLEED中：

- **3.3 V rail bleed 暂时保留**，因为它仍参与掉电外部接口注入吸收；
- 5 V bleed只有在确认C版不存在外部信号向5 V rail注入的路径以后才能删除。

所以不会再出现“它看起来费电，所以DNP”的粗暴处理。

---

# 十一、C 的器件数量：不是145，而是约83

我按一个**保守、能画成原理图**的 C0 候选重新数：

| 类别 | 原176 | A完整条件版 | **C候选** |
|---|---:|---:|---:|
| R | 81 | 60 | **32** |
| C | 59 | 54 | **32** |
| D / protection package | 17 | 14 | **6** |
| IC | 15 | 15 | **9** |
| Connector | 4 | 4 | **4** |
| **总贴装** | **176** | **147** | **83** |

### C 的9颗IC

1. OPA388 —— 全阵列ROW driver  
2. TMUX1109 —— dual 4:1 row drive/sense mux  
3. OPA4388 —— 4列TIA  
4. ADS8684 —— 4ch ADC  
5. REF3025 —— 2.5V VCM  
6. STM32G031K8 —— MCU  
7. LM73100 —— 5V入口保护  
8. TPS389001 —— 5V精密监督  
9. LP5912-3.3 —— 3.3V LDO + reverse protection + PG

相对原15颗：

> **15 → 9。**

而且删掉的不是重复封装，而是真正取消了6个功能IC的位置。

---

### 32颗R大致组成

不是现在就冻结每个精确值，但预算明确：

- VEXC精密分压：2
- 4×RF：4
- ADC输入串阻：4
- ROW loop/compensation预留：1
- ROW mux A0/A1/EN默认态：3
- ADC CS/reset等默认态：约2
- U9 EN + OV：4
- U11分压：2
- LP5912 enable/PG：约2
- 3.3 V bleed：1
- J3/J4接口串阻：7

合计约 **32**。

---

### 32颗C

这里我故意没有极端压缩：

- 4×CF
- 4×ADC input C
- VEXC divider C
- ROW/TIA/MUX本地去耦
- ADS8684严格按照datasheet的AVDD/DVDD/REFCAP/REFIO需求
- MCU去耦+bulk
- REF3025
- U9
- U11
- LP5912
- 电源bulk
- 以及 **2个ADC有效容量qualification reserve**

所以32里已经包含一定余量。

如果最后准确MLCC在DC bias下证明一颗即可，C还有机会掉到 **80–81件**；但我现在不拿这个数字当目标。

---

# 十二、A和C真正的差别

| | A | **C** |
|---|---|---|
| 电阻 | 60 | **约32** |
| 电容 | 54–59 | **约32** |
| 保护封装 | 14–17 | **约6** |
| IC | 15 | **9** |
| 总数 | **147–155** | **约83** |
| ROW运放 | 4 | **1** |
| 列TIA | 4 | **4** |
| ADC | ADS8684 | **ADS8684** |
| VCM/VEX buffer | OPA2388 | **取消** |
| 3.3V二级LM73100 | 保留 | **取消** |
| 3.3V独立TPS3890 | 保留 | **由LP5912 PG + MCU BOR/PVD承担** |
| 数字安全逻辑 | U13/U14/U15 | **MUX硬件EN + PG/reset** |
| 旧288转换协议 | 保留 | **不冻结** |
| 架构风险 | 低 | 中等 |
| PCB复杂度改善 | 一般 | **非常明显** |
| 新仿真需求 | 少 | 较多 |
| 是否值得重新画板 | 一般 | **值得** |

---

# 十三、我的推荐：选 C

如果我们的目标只是“尽量少动原设计”，我会选A。

但现在你的要求已经变成：

> **“这板子看起来还是太复杂，查实际别人怎么做，合理地真正精简。”**

那继续在176件架构上挖10颗、20颗小阻容，确实意义不大。

而 C 有一个非常强的依据：

> **它最核心的改动——四个ROW运放压成一个——不是我凭直觉发明，而是已有4×4共享行列电阻阵列PCB实验验证的Type III zero-potential row-driver。**

而我们还保留了：

- 四列zero-potential TIA；
- 16-bit高速ADS8684；
- 精密2.5V reference；
- 5V独立保护和精密监督。

所以它不是为了漂亮做成“极简玩具板”。

我的目标定位是：

> **约80–85件，是当前性能要求下比较合理的“科研实验板简化点”。**

再往下压到50～60件，通常就要开始考虑：

- MCU内部12bit ADC；
- 一个TIA轮询四列；
- 取消独立5V supervisor；
- 显著弱化外部掉电/持续误接保护。

这些对你现在要求的≤1%/≤0.2%和共享矩阵串扰而言，性价比开始变差。

---

# 十四、C必须守住的风险合同

这几个不会因为用户要求“再简单一点”就偷偷放掉：

1. **J2仍是4ROW+4COL共8线被动阵列**，不增加第9/第10根sense线；因此所有串扰精度验证必须在这个条件下完成。
2. **0.8–8 kΩ只是阻值保护带，不是故障短路/开路定义。**
3. C必须覆盖0.8/1/7/8 kΩ和最坏相邻单元组合，重点检查unselected-row leakage、mux leakage、RON remote-feedback residual error、FFC寄生。
4. 四个列TIA不因“少器件”取消；只有12个复杂TIA补偿件通过AC/PZ/TRAN后才能删。
5. ADC电容必须按**实际型号有效电容**闭合；不能再拿名义22 µF直接判断。
6. J3/J4默认继续覆盖**板掉电、外部调试器/UART仍有电**；数字接口保护因此不简单换成ESD-only器件。
7. J2 C版的简化保护建立在**外部是被动电阻阵列**这一合同上；如果以后要接有源设备，这部分重新审。
8. 100 fps是硬目标，256+32不是；采样次数可以改变，但最终必须用settling+噪声/重复性证明，而不是仅凭500 kSPS算术。
9. `≤1% mean error / ≤0.2% sample SD`现在仍只是验收目标，任何SPICE通过都不能改写成实物PASS。

---

# 十五、这次统一360 min工程范围

我同意你02的原则：**一次给够范围，别每改一个阻值又回来问。**

但因为路线已从A升级到C，360 min内部重新分配。

## `CIRCUIT-SIMPLIFICATION-C-ENGINEERING-QUALIFICATION-V1`

**总预算：360 min，不追加零碎申请。**

| 阶段 | 时间 | 允许内容 |
|---|---:|---|
| C0 输入/料号闭合 | 60 min | ≤4份新增官方资料；≤2种保护候选；确认精密R、ADC有效C、LP5912、TMUX1109、保护拓扑 |
| C1 原理图工作副本 | 120 min | **仅C方案**；1份working copy、≤2 EDA session、≤6 save、≤6 capture、net-audit≤4、ERC≤2、PDF≤1 |
| C2 有限电气验证 | 110 min | OP/AC/PZ总计≤32；normal TRAN≤8；每个TRAN≤180 s；卡住即停 |
| C3 离线placement feasibility | 40 min | 仅在C电气门通过后；候选1版、调整≤2、图≤2；**不动native PCB** |
| C4 汇总交付 | 30 min | C器件表、before/after框图、风险HOLD、仿真结果、最终placement坐标建议 |
| **合计** | **360 min** | |

### C2优先验证顺序

只做和能否精简直接相关的内容：

- Type-III single-row-opamp + TMUX1109，在0.8/1/7/8 kΩ和最坏4并联负载下的DC误差；
- ROW FFC Cload + mux RON的loop stability / settling；
- 简化TIA的noise gain、phase margin、step response；
- 16个传感器极端阻值组合的未选通串扰；
- RF/CF + ADC RC的100 fps settling；
- 5V→3.3V启动、brownout、PG/reset；
- J3/J4 board-off外部驱动的解析/OP边界；
- MLCC Ceff没有准确模型的，直接标 **HOLD**，不拿宏模型“跑过”冒充有效容量PASS。

---

# 十六、本轮工程释放边界

为了让桌面端不再重复向你请示，我把权限也一次说清楚。

**本轮释放：**

> `CIRCUIT-SIMPLIFICATION-C-ENGINEERING-QUALIFICATION-V1`  
> **路线C作为唯一工程工作副本路线，允许在上述360 min/次数内做原理图working-copy ECO + 有限SPICE + net/ERC审核 + offline placement feasibility。**

**A不自动实施**，只作为C若出现基础物理门失败时的回退参考。

如果以下任一项失败：

- single-row-driver精度/稳定性；
- unselected-row crosstalk无法压到目标所需水平；
- 简化TIA无法稳定；
- 电源/掉电合同无法闭合；

则 C 标记 **HOLD**，保留证据，**不得偷偷加回一堆器件把C慢慢变成旧板，也不得自动改A**。

仍然明确为 **0**：

**PCB native搬件、铜皮、routing、铺地、Gerber、制造、采购、bench上电、固件烧写、系统安装、本地Git写入。**

等C的工作副本和有限验证回来以后，我们再看真正的PCB；那时布局面对的应该是**约83件的新板**，而不是继续对着176件老版“挪家具”。

这一次我建议就沿这个路线往下走。
