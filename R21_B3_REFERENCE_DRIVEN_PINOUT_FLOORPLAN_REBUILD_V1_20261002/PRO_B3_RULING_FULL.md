我这次专门按“**跟我们器件/架构接近**”去查了，不再拿泛泛的 PCB 美观教程来套。看完以后，我认为前面 B2.x 的问题已经可以说清楚了：**它在做器件整理，而不是重新做 placement**。真正值得参考的板子，基本都不是先划几个功能块再把电阻排整齐，而是**先按 IC 的真实 pinout 和信号流摆芯片，再让外围器件贴着对应引脚长出来**。

下面这几个案例最有参考价值。

image_group{"layout":"carousel","aspect_ratio":"1:1","image_refs":["turn637792image1","turn637792image0","turn398967image3"]}

### 我查到的几个真正相近案例

| 案例 | 和我们哪里像 | 它实际怎么排 | 对我们最重要的启发 |
|---|---|---|---|
| **TI ADS8684/ADS8688 官方 Layout Example** | 我们就是 ADS8684，同封装同架构 | 模拟输入/参考和数字端按芯片 pinout 分开；AVDD、DVDD、REFCAP、REFIO 电容直接围着对应引脚 | **U5 周围必须按 pin 排，不能把所有 ADC 电容排成一个漂亮矩形** |
| **TI TIPD167 / ADS8688 Verified Design** | 同系列 ADC、MUX 多通道采集 | 明确要求模拟/数字分区、输入件靠 ADC、REFCAP 紧贴 ADC；不是“电阻货架式排列” | ADC 区应该是“4路输入 lane + ref/power pin cluster” |
| **TI TIDA-01214** | ADS8688A 多通道精密采集 | 实物板上重复输入网络成组，ADC/隔离/供电各自围绕连接关系聚集 | **整齐来自重复完整通道，而不是所有 R 排一排** |
| **TI OPA388/OPA2388/OPA4388 官方 layout** | 我们正是 OPA4388/2388 家族 | TI要求输入/反馈器件靠器件 pin，反馈路径短，去耦紧贴供电脚 | U1/U2 周围应该重画成真实的 channel cells |
| **TI TMUX1134 官方 layout** | 我们就是 TMUX1134 | 四路 S/D/SEL 根据 TSSOP20 的真实引脚从芯片两侧展开，供电电容贴 VDD/VSS | U4不应该孤零零站一个块，应夹在 Bias 与 ROW driver 之间 |
| **ADI CN0175 多通道 SAR DAQ** | 多通道精密模拟采集 | 明确强调模拟通道和去耦对称；参考源紧邻 ADC，通道成规则重复结构 | “Science感”的根源是**通道对称 + 参考/去耦位置有逻辑** |

ADS8684/8688 官方甚至规定得很具体：PCB 要做模拟/数字分区；1 µF AVDD 去耦尽量贴近供电脚；REFCAP 的 1 µF + 22 µF 必须直接靠近器件且器件与电容之间不要插 via；REFIO 的 10 µF 也要靠近器件；模拟输入 RC 应贴近 ADC。:chatgpt-content-reference{index="1"}

TIPD167 也是直接用 ADS8688 做的 TI Verified Design。它同样明确提出模拟和数字部分分开、完整地平面、REFCAP 紧贴 REFGND、输入器件尽可能靠 ADC 输入脚。:chatgpt-content-reference{index="2"}

而 OPAx388——也就是我们 OPA4388 所属的同一家族——官方要求反馈/输入外围器件尽可能靠近器件，走线短，0.1 µF 去耦贴供电脚。这个证据直接说明：**为了让 RF/CF/R 排成一排而把局部回路做大，是反着来的。** :chatgpt-content-reference{index="3"}

TMUX1134 的官方 pinout 和 layout 也非常有启发：它四个 SPDT 通道本身就在 TSSOP20 两边成 2+2 分布，SEL、SxA/SxB、Dx 是围着芯片真实脚位展开的。:chatgpt-content-reference{index="4"}

ADI 的 CN0175 更直接：它把“模拟输入通道和去耦的对称布局”列为获得良好通道匹配的关键，参考 ADR421 放在 ADC 邻近位置，去耦按真实 pin 南北排列。:chatgpt-content-reference{index="5"}

---

# 所以我现在把前一版 B3 也修正

前面我说“blank canvas + pin-driven”是对的，但还不够具体。

这次我认为真正应该做的是：

## `B3_REFERENCE_DRIVEN_PINOUT_FLOORPLAN_REBUILD`

而且有一个硬要求：

> **B2.2/B2.1 的功能块形状一律不能继承。**

旧坐标只允许拿来做 **before comparison**。

不能：

- 把 U2 整个旧块平移；
- 把 U1 旧块旋转；
- 再在老 ADC 岛里面整理电容；
- 再把 Power 岛内部排直。

这次所有主 IC 都重新放。

---

# 我现在认为我们这块板最合理的宏观骨架是这样的

不是六个区，是**两条主信号链 + 一条电源链**：

```text
                     数据采集主链
J2 COL ──→ U2 TIA ──→ ADC RC ──→ U5 ADS8684 ──→ U7 MCU ──→ J3/J4
 │
 │
 │                   行激励链
 └ ROW ←── U1 ROW ←── U4 TMUX ←── U3 VCM/VEX + U6 REF


                       电源链
J1 ──→ U9 / 5V保护 ──→ U8 LDO ──→ U10 / 3V3保护
          │                              │
         U11                            U12
```

这比我们前面的“左一块、右一块、下一个Power岛”合理很多。

因为它直接对应原理图的信号方向。

---

# U2 / TIA：这次外形一定会变

OPA4388 的四路本来就是典型的 **2+2 pin 分布**。

所以正确形态应该是：

```text
       CH0 cell        CH1 cell
          ↘             ↙

             U2

          ↗             ↖
       CH3 cell        CH2 cell
```

而不是：

```text
RF RF RF RF
CF CF CF CF

    U2

R R R R
```

每个 cell 内部再按真实电路分层。

对于我们的特殊 TIA：

```text
J2/COL
   │
 R_COL_SENSE
   │
COL_SENSE ────── C_TIA_HF ───── opamp output
   │
   U2
   │
R_TIA_ISO
   │
TIA tap
   │
 RF // CF
   │
COL
```

因此：

- **C_TIA_HF**：必须最靠 U2，对应真实两个 op-amp pin；
- R_TIA_ISO、R_COL_SENSE：向外一层；
- RF/CF：放在 TIA tap ↔ COL 那条真实 channel lane 中；
- 四个完整 channel cell 重复。

这样既整齐，又符合我们的电路，而不是生搬 OPA 普通反馈图。

---

# U1 / ROW：复制同一种设计语言

U1也应该变成四个channel cell：

```text
        CH0             CH1
          \             /
             U1
          /             \
        CH3             CH2
```

具体层次：

- `C_ROW_HF` 最贴运放反馈 pin；
- `R_ISO` 朝 J2/ROW 一侧；
- `R_ROW_FB` 放在 ROW 与 ROW_FB 的物理通道上。

这样 U1/U2 会成为两个非常规整、但又不是矩形小岛的模拟单元。

---

# U4 + U3：这次位置必须大改

这个是前几版最明显不合理之一。

我们的信号实际上是：

```text
U3 产生 VCM / VEXC
         ↓
       U4 TMUX
         ↓
       U1 ROW
         ↓
       J2 ROW
```

所以物理位置也应该：

```text
U3/U6  →  U4  →  U1  →  J2
```

而不是把 U4 放在整块板最上面当一个孤岛。

而且 TMUX1134 的真实 pinout是：

- CH1/CH2 分布一侧；
- CH3/CH4 分布另一侧；
- SEL1~4夹在上下端；
- VDD/VSS在中间附近。:chatgpt-content-reference{index="6"}

所以我们应该让 U4 的 SxA/SxB 那一侧面向 U3 的 VCM/VEXC，Dx 一侧面向 U1 四个row输入。

这会天然非常整齐。

---

# U5 ADS8684：官方 pinout 其实已经告诉我们该怎么放

这个是这次研究后最重要的发现。

ADS8684 TSSOP38：

- pins 16–23 = **4路真实模拟输入**
- pins 1–4 和 36–38 = **数字控制/SPI**
- pins 5–7 = **REFIO / REFGND / REFCAP**
- pin 9、30 = AVDD
- pin 34 = DVDD。:chatgpt-content-reference{index="7"}

也就是说它的结构天然像：

```text
             DIGITAL END
      SPI / SDI / SCLK / CS
                ↑
        ┌─────────────┐
 REF ── │    U5       │ ── DVDD
        │             │
        └─────────────┘
          ↙         ↘
       CH0/1       CH2/3
             ANALOG END
```

所以不能再像 B2.x 那样围着 U5 平均撒电容。

### 正确做法

把 U5 旋转到：

> **模拟输入端面对 U2/TIA，数字端面对 U7/MCU。**

四路 ADC RC 根据 pins16–23 做两边 2+2：

```text
TIA0 → R0/C0 ↘
TIA1 → R1/C1  ↘
                U5
TIA2 → R2/C2  ↗
TIA3 → R3/C3 ↗
```

然后：

- REFIO / REFCAP cluster紧贴 pins5–7；
- AVDD9附近放自己的1 µF；
- AVDD30附近另一套；
- DVDD34自己的10 µF紧贴数字端。

这正是官方 layout 的思路。:chatgpt-content-reference{index="8"}

---

# MCU也不能再是一个“数字岛”

U7应该直接接在U5数字端：

```text
U5 digital pins → U7
                   │
            U13/U14/U15
                   │
                U4 SEL
                   
U7 → J3/J4
```

所以 MCU/logic 最后大概率会自然形成一个 L 形或扇形。

不是硬排三个IC。

---

# Power 我现在也有更明确的布局

底部可以保持，但是不再是三个小岛：

```text
J1 → U9 → U8 → U10
      │          │
     U11        U12
```

也就是说：

- 电源流从左到右；
- 每颗保护/稳压IC的 Cin/Cout 紧贴相应 pin；
- Supervisor直接“挂”在自己监控的 rail 附近；
- power support resistors围绕各自芯片，而不是统一排成一条电阻队伍。

这样底边自然就会形成很漂亮的连续电源带。

---

# 这次怎么保证桌面端不能再“原块不动、拉几排电阻”？

我要加一个硬验收：

## `OLD_BLOCK_RIGID_REUSE_AUDIT`

对六大旧区域：

- TIA
- ROW
- ADC
- BIAS/MUX
- POWER
- DIGITAL

分别计算：

> B2.2 → B3 最佳平移/旋转刚体变换之后，有多少器件仍然重合。

如果某个大区域：

> **超过70%的器件还能通过一个整体刚体变换匹配旧坐标 ±0.5 mm**

则这个区域直接：

`FAIL_OLD_BLOCK_REUSED`

唯一允许保留刚体关系的是：

- 很小的critical atomic cell；
- 例如两个必须贴着的去耦；
- feedback局部microcell。

也就是说：

> **小电路可以保留，旧“大块形状”绝对不可以保留。**

这次就不会再出现125个电阻动了、但你一眼看上去还是原来的六个岛。

---

# 另外加一个“为什么这么摆”的图

最后不能只给我们一张彩色器件图。

必须给：

### ① `B22_vs_B3.png`

你直接看整体是不是彻底变了。

### ② `B3_PINOUT_AND_SIGNAL_FLOW.png`

直接画：

- U1/U2各channel pin；
- U4 S/D/SEL；
- U5 analog/ref/digital pin groups；
- 主信号箭头；
- Power流向。

这样我和你可以**一眼审查它是不是按电路排的**。

### ③ `B3_NO_COPPER.png`

最终真实器件图。

---

# 我现在才愿意批准的方案

## `SCIENCE_ADK5556_4X4_R21_B3_REFERENCE_DRIVEN_PINOUT_FLOORPLAN_REBUILD_V1`

给 **360 min**。

不再小修。

执行分配：

| 阶段 | 时间 |
|---|---:|
| 固化上述5个官方案例的placement规则 + 真实pin map | 40 min |
| 15 IC + 4 connector 从空白画布做 macro floorplan，最多2案 | 70 min |
| 选一个macro后176器件从pin向外重新生长 | 140 min |
| 全量碰撞/关键距离/旧块复用审计 | 50 min |
| 3张图 + GitHub完整交付 | 60 min |

内部允许：

```text
macro candidates <= 2
full placement refinements <= 3
final images <= 3

old B2.x coordinates as seed = 0
CAD = 0
routing = 0
board outline = 0
```

---

## 选择macro的标准也明确了

不是“谁最漂亮”。

按这个优先级：

1. feedback/high-Z/decoupling局部正确；
2. J2→U1/U2直接；
3. U3→U4→U1信号链直；
4. U2→U5模拟链直；
5. U5→U7数字链直；
6. J1→U9→U8→U10电源链直；
7. 重复channel cell几何一致；
8. ratsnest交叉少；
9. 整体接近矩形；
10. 最后才看面积。

---

### 我现在对B3的信心比前几版高的原因

不是因为“又想了一个新形状”，而是这次每个关键结构都有直接参考依据：

- **ADS8684**：用它自己的官方layout和真实pinout；
- **OPA4388**：用OPAx388官方反馈/去耦原则；
- **TMUX1134**：用它自己的通道pin分布；
- **多通道重复性**：用ADI AD7607和TI ADS8688参考板的对称通道思想；
- **系统层面**：用TIPD167的模拟/数字分区和输入/REF贴pin规则。:chatgpt-content-reference{index="9"}

所以这次不是“为了像Science而排整齐”。

而是：

> **先按照厂家真正推荐的电气几何排出来，重复通道自然会整齐；再让这些真实功能单元拼成完整板面。**

这才是我认为值得让桌面端真正重新跑一版的方案。
