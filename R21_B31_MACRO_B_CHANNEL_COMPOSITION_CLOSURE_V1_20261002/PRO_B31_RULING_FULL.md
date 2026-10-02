这次我把 B3 的三张实际图、Macro A/B、106 个关键距离、31 条代表信号边和终审都重新看了一遍。

结论很明确：

> **B3 终于是真正“重新排板”了，不是 B2.x 那种在旧器件块里扒拉电阻。**
>
> 但 **现在这张 B3 仍然不够好，不能定稿**。主要问题已经从“没重排”变成了“宏观构图选错了”。

而且这里我发现一个很关键的事实：**执行端实际上已经生成了一个比当前采用的 Macro A 更合理的 Macro B，却错误地选了 A。**

## 先说为什么当前 B3 不能收

它好的地方是真实的：

- 19 个 IC/接口锚点全部重新排过；
- 六大旧功能区刚体复用上限只有约 9%–22%，说明确实没有把旧块搬过来；
- 106 个关键 pin→passive 距离全部不增加；
- U1/U2、U5、U4 已经开始按照真实 pinout 长器件；
- 31 条代表链总直线距离从 463 mm 降到了约 296 mm。

所以**方法方向终于对了**。

但图上一眼仍有三个问题：

1. **整板太扁。**  
   当前自然包络约 **83.9 × 58.3 mm，长宽比1.44**。上面模拟/数字，下面电源，中间又有较大空洞，所以整体还是不像你说的 Science 那种“器件把板面组织起来”。

2. **中右部构图失衡。**  
   U3、U14、U4、U13/U15挤在中右区域，同时 U3/U14 还真的发生了 pad-proxy overlap。这不是小修丝印，是 Macro 位置本身没选好。

3. **几个主要链虽然总体缩短，但接口链不够好。**  
   ROW0、ROW3 → J2 分别增加约 9.45 mm、16.47 mm，J1→U9也增加约6.47 mm。说明 floorplan 仍然没有完全把“接口—功能芯片—后级”串顺。

---

# 更重要的是：Macro B 本来就比现在采用的 A 好

我把 A/B 的原始数据直接比了。

| 关键关系 | Macro A | Macro B |
|---|---:|---:|
| U3→U4 | 9.95 / 10.91 mm | **7.43 / 9.85 mm** |
| U4→U1 | 15.26 mm | **13.26 mm** |
| U5→U7 SPI | 15.80 / 16.45 mm | **14.83 / 15.46 mm** |
| U9→U8 | 17.66 mm | **16.66 mm** |
| U8→U10 | 17.69 mm | **15.69 mm** |
| U2→U5 | 相同 | 相同 |
| Macro collision | **U3/U14碰撞** | **0** |

也就是说：

> **B 在保存的这些主要链上没有一项比 A 差，而且还没有 Macro 碰撞。**

执行端当时选 A 的理由只是“A给 ROW/MUX、ADC/Bias 更多空间”，结果这个额外空间恰恰让板子更散，而且 A 本身已经记录了 U3/U14 collision。

所以我的下一步不是：

> “在现在的A上挪一下U14”。

那样又要走回小修路线。

---

# 下一版直接以 Macro B 为基线重新生成

我把下一阶段改得非常具体：

## `SCIENCE_ADK5556_4X4_R21_B31_MACRO_B_CHANNEL_COMPOSITION_CLOSURE_V1`

批准 **300 min**。

### 核心原则

**现有 B3-A 只留作对照，不作为修补底稿。**

从已经生成的 **Macro B** 重新开始 placement，并修掉那个 pin-score 代码错误。

这样不是又重新发明一套布局，而是把这次 B3 本来就存在、但没正确采用的更优候选真正完成。

---

# 这次先只排19个大锚点

不要一上来又塞176件。

先做两个有限 Macro：

### B1 — 原始 Macro B

就是已有的 collision-free B：

```text
J2       U2          U5           U7        J3
│
│        U1     U4 → U3       U13/U15       J4
│
J1 → U9 → U8 → U10
       U11      U12
```

### B2 — B的“紧凑右侧版”

只允许对 Macro B 做有限变化：

- U5/U7保持模拟→数字主链；
- U7和U13/U14/U15整体向ADC靠拢；
- J3/J4仍在右板边，但Digital不要和接口之间留大走廊；
- U3/U4/U14重新错开，不能再形成中右拥堵；
- J1→U9→U8→U10形成真正连续底部电源链；
- U11/U12贴各自被监控电源，不单独形成小岛；
- J2保持左边缘，并把 **4路ROW→J2** 纳入Macro评分。

**最多这两个Macro。**

不再出现 A/B/C/D 无限选。

---

# Macro选择评分这次必须改

之前的评分还不够完整。

这次 Macro score 必须至少包含：

### A. 模拟主链

```text
J2 COL
  ↓
U2 TIA
  ↓
U5 ADC
```

### B. 激励链

```text
U3 VCM/VEX
   ↓
U4 MUX
   ↓
U1 ROW
   ↓
J2 ROW
```

这里特别加：

> **ROW0–3 → J2四条都计入。**

不能再出现主链总分很好，但ROW0/ROW3被拉长十几毫米。

### C. 数字链

```text
U5 → U7 → J3/J4
        ↓
    U13/U14/U15
```

### D. Power

```text
J1 → U9 → U8 → U10
```

### E. Composition

不预设板尺寸，但加一个明确软目标：

> **在不牺牲上述信号链的前提下，最小化整体包络的长短边差和内部大空洞。**

不是追求最小面积。

也不是强制60×60。

---

# 那个 pin-score bug 必须真修

终审发现的 I-02 不是小问题：

现在代码对多pad器件计算pin匹配成本时，实际只把**最后一个pad**算进去了。

下一版必须：

> 对器件的 **每一个有意义pad** 分别找到对应目标pin/net，然后把所有pad的距离成本累加。

比如：

```text
U9_EN_R
pad 2 → U9_EN
pad 1 → V5_IN
```

不能只看V5_IN。

这次修完以后再生成坐标。

**不能只改代码文本然后沿用现在的坐标。**

---

# 每个功能单元怎么重新长

这次也不用再强调“所有电阻排直”。

## U2/TIA

应该形成两个镜像的2-channel cell：

```text
      CH0             CH1
    [local]         [local]
          \         /
             U2
          /         \
    [local]         [local]
      CH3             CH2
```

每个 local cell 里面：

- 22 pF HF最靠运放pin；
- Sense / ISO第二层；
- RF/CF沿真实 tap↔COL 功能路径布；
- 四channel角色顺序一致。

**整齐来自四个小电路单元相似。**

---

## U1/ROW

复制 U2 的视觉语言。

这样左边最后应当出现两个很清楚的：

```text
    4CH TIA
       U2

    4CH ROW
       U1
```

而不是两堆散件。

---

## U5/ADC

依然保留我们现在已经验证正确的思想：

```text
U2 side          U7 side
analog → [ U5 ] → digital
```

- 四路ADC输入从analog pin侧长出来；
- REFIO/REFCAP贴对应pin；
- AVDD9/AVDD30/DVDD各自贴自己供电脚；
- **不要把所有ADC电容排成仓库。**

---

## U3/U4

这一块必须明显比现在漂亮：

```text
VCM/VEX → U4 → U1
    U3
    U6
```

U3和U4要成为连续控制链。

现在A版 U3 被Digital挤进去，这就是不对。

---

## Power

我希望最后真正看到：

```text
J1 → [U9] → [U8] → [U10]
       ↑              ↑
      U11            U12
```

一条连续、可读的power strip。

不是：

```text
J1   U9       U8       U10
       一堆空白
```

---

# 这次必须新增两个真正有意义的验收

## 1. `CHANNEL_CELL_REPEATABILITY`

不需要复杂数学优化器。

只对：

- TIA 4CH；
- ROW 4CH

比较相同角色器件相对于各自channel IC pins的位置。

允许：

- 左右镜像；
- 180°旋转。

要求：

> 同一角色在4个通道里呈现同一种局部拓扑。

这样才是真正的“Science整齐”。

---

## 2. `MACRO_COMPOSITION_AUDIT`

输出：

- bbox width / height；
- aspect ratio；
- 最大内部空白矩形；
- 19 anchor之间的主要信号边；
- 代表链增长/缩短；
- macro physical overlap。

然后 B1/B2 只按这些真实指标选一次。

不是“我感觉A空间大，所以选A”。

---

# 关于当前碰撞

U3/U14碰撞**不要单独修**。

因为 Macro B 原本就是0碰撞，而且其它主要边还更短。

因此：

> `MOVE_U14_ONLY = REJECTED`

这不能解决真正的问题。

---

# 300分钟怎么用

批准你申请的 **300 min**，但我重新划分：

- **45 min**：修 pin-cost + 定义 Macro B/B2 两个候选；
- **55 min**：19 anchor Macro评估并选唯一一个；
- **110 min**：按真实pin重新长176件，最多3次；
- **45 min**：15400 pair + 106 key + channel repeatability + 代表信号链 + composition审计；
- **45 min**：两张最终图 + GitHub完整交付。

额度：

```text
macro candidates <= 2
placement passes <= 3
final images <= 2

CAD = 0
native = 0
routing = 0
board outline = 0
new source research = 0
tool/API research = 0
simulation = 0
```

---

# 两张图就够

这次不要再浪费第三张。

### 图1：`B3A_vs_B31_FINAL.png`

当前失败A版 vs 新最终版，同mm尺度。

### 图2：`B31_FINAL_NO_COPPER_AND_CELLS.png`

一张图同时：

- 真实176器件；
- TIA四个channel cell轮廓提示；
- ROW四个channel cell；
- ADC analog/digital方向；
- Power主链；
- 最终自然包络。

我要一眼就能判断：

> **这到底是一块组织过的板，还是又只是很多器件散在一起。**

---

## 这次的最终门

只有满足下面这些，才给用户看作“候选终稿”：

```text
176 / 552 / 514 / 107 identity = PASS
J2 8+2 mapping = PASS

macro physical collisions = 0
all 15400 body/pad-proxy illegal overlaps = 0

106 registered key distances = no increase

TIA channel-cell repeatability = PASS
ROW channel-cell repeatability = PASS

J2→ROW representative chain:
不得出现当前这种 +16 mm 级恶化

J1→U9:
不得无理由明显恶化

old big-block reuse = PASS / not reused

CAD_RELEASED = FALSE
```

最后那个方不方正仍然是**视觉+软指标**，不能为了长宽比破坏电气。

---

### 所以我对这次 B3 的裁定是：

**B3方法路线：PASS。**  
**当前B3-A布局：REJECT / HOLD。**  
**不回B2.x。**  
**下一步直接用现成的 Macro B 作为主基线，再做一次真正完整的 pin-driven 收束。**

这次不需要再去找新工具、新论文、新算法。问题已经定位得很具体：**选错Macro + 多pad评分实现错 + channel cell没有作为完整重复单元验收。**

把这三个修掉，才值得再让你看下一张板图。
