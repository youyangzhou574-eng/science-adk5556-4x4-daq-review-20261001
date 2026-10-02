# CIRCUIT-PRO-R21-J2-FFC-FPC-REQUIREMENT-CORRECTION-AND-LOCAL-ECO-20261002-20

这次用户需求纠正成立，而且属于**真实产品接口需求变化**，不是19号之后又空转重做。

之前的 `1718560008 + 22012087` Molex KK254 方案虽然电气上通过了，但它是离散导线压接壳体体系，**不符合用户现在明确确认的“FFC/FPC软排线插入、翻盖/ZIF锁紧”接口形态**。因此旧方案保留为历史合格实现证据，但从现在开始不再作为最终J2产品接口。

当前状态更新为：

```text
SCHEMATIC_CORE = ACCEPTED
PCB_CORE_ELECTRICAL = ACCEPTED

OLD_J2_KK254_ELECTRICAL_EVIDENCE = RETAINED_HISTORY
OLD_J2_KK254_USER_REQUIREMENT_CONFORMANCE = SUPERSEDED

J2_REQUIRED_INTERFACE = 8P FFC/FPC ZIF
J2_FINAL_INTERFACE_CONFORMANCE = HOLD_FOR_LOCAL_ECO

MANUFACTURING_RELEASE = FALSE
GERBER_RELEASE = FALSE
BENCH_RELEASE = FALSE
```

## 默认板线标准直接冻结，不再反复问0.5还是1.0 mm

用户没有现成软排线可兼容，所以我同意直接替项目选一套标准：

| 项目 | 本轮默认冻结 |
|---|---|
| 板端J2 | **Molex 2005290081** |
| 类型 | 8P、1.00 mm pitch、SMT、right-angle、Front-Flip ZIF |
| PCB侧接点 | **Bottom contact** |
| 排线标准 | 8芯、1.00 mm pitch FFC |
| 默认排线 | **Molex Premo-Flex 154670229** |
| 排线端型 | **Type A / same-side contacts** |
| 默认长度 | **102 mm** |
| 电气针序 | 1–8 = ROW0–3、COL0–3 |

Molex当前官方页面把 `2005290081`列为8回路、1.00 mm、Front Flip、Bottom Contact、SMT、ZIF的FFC/FPC连接器，并明确列出15467/15167/15267/98267等Premo-Flex系列作为配套线缆系列。:chatgpt-content-reference{index="0"} 官方15467系列表中，`154670229`是8回路、1.00 mm、102 mm、Type A同面触点FFC，因此我把它定为本项目**无现成线材时的默认验证线**。:chatgpt-content-reference{index="1"}

这里的Type A不是随便定的。我们默认以后板端和测试夹具/阵列端按同一接触面逻辑设计，使两端导电面无需人为翻转；如果最终阵列本身直接做成FPC尾巴，则阵列尾部只需按J2的**bottom-contact插入方向**设计，不必真的购买第二根标准FFC。

Hirose `FH12-8S-1SH(55)`保留为**唯一备用候选**，不进入并行设计。它同样是8P、1.0 mm、bottom-contact、ZIF，官方页面还明确给出适配FFC/FPC厚度0.3 mm，并提供2D/3D和ECAD footprint。:chatgpt-content-reference{index="2"} 只有Molex实际footprint在当前板边无法局部落下、官方drawing不满足机械要求或现实供应失败，才切换Hirose；否则不再比较第三种连接器。

## 针序完全冻结

这次接口物理形态可以改，但4×4测量架构不能改：

```text
J2.1  ROW0
J2.2  ROW1
J2.3  ROW2
J2.4  ROW3
J2.5  COL0
J2.6  COL1
J2.7  COL2
J2.8  COL3
```

仍然是：

\[
R_{ij}=ROW_i \leftrightarrow COL_j
\]

J2不增加GND，不增加VCC，不为了FFC方便重新排序ROW/COL。

---

# 唯一下一包批准

## `SCIENCE_ADK5556_4X4_R21_J2_FFC_FPC_INTERFACE_CORRECTION_V1`

批准 **240 min**，19号休眠条件制造包继续保持未启动，其240 min不继承、不转换。

| 阶段 | 时间 |
|---|---:|
| P0 精确板座/排线drawing资格 | 45 min |
| P1 J2最小原生ECO | 60 min |
| P2 warm/cold + 针序/局部机械验证 | 60 min |
| P3 接法与制造输入合同 | 25 min |
| P4 固定commit完整交付 | 50 min |

硬额度批准：

```text
official connector/cable sources <= 4
candidate connector families <= 2

copy <= 1
session <= 2
save <= 3
capture/audit <= 4
DRC <= 4
native export <= 1
normal pour rebuild <= 1
```

---

## P0必须先把几个机械事实钉死

CAD之前只核官方drawing，不猜：

- `2005290081`推荐land pattern；
- 8个signal pad编号方向；
- 两侧hold-down / anchor pad到底是机械还是电气对象；
- 适用FFC厚度；
- FFC插入方向；
- bottom-contact方向；
- front-flip开启所需空间；
- `154670229` Type-A端面与板端bottom-contact是否匹配。

如果Molex官方drawing证明当前默认组合不匹配，才允许切唯一备用Hirose，不继续第三轮选型。

---

# P1允许真正改J2，而且这次允许pad总数变化

现有KK254 J2是8个PTH孔；FFC连接器会变成SMT signal pads，并很可能有固定焊片/机械锚脚。

所以这次**不再强迫550 pads这个历史数字保持不变**。

验收分成：

```text
8 SIGNAL CONTACTS:
ROW0 ROW1 ROW2 ROW3 COL0 COL1 COL2 COL3

MECHANICAL / RETENTION PADS:
separately classified
no fake signal nets
```

不能为了凑550：

- 删除厂家要求的固定焊片；
- 把机械pad偷接GND；
- 把anchor算NC后忽略其制造作用。

其余175器件的原有pad-net必须保持。

允许的CAD范围只有J2周围：

- J2 symbol/identity；
- 精确footprint；
- 必要局部fanout；
- Pin1/FFC插入方向标识；
- 必要局部器件让位；
- 局部pour rebuild。

允许为了新插座局部移动J2附近普通器件，但**不允许改100×90 mm板框，也不允许进入主模拟区重新布局**。

---

# P2验收门

FFC ECO完成后warm必须先满足：

```text
ROW/COL 8 signal mapping = exact
other 175 component core = unchanged
non-J2 primary copper = unchanged

Connection = 0
Short = 0
Clearance = 0
NetlistError = 0
```

然后save、完全关闭、独立cold reopen，再次要求四类全0。

最终不再要求“550 pads”；改为：

> **原有非J2 pad-net严格不漂移 + 新J2的8个signal contacts严格正确 + 合法mechanical pads完整存在。**

此外必须实际检查：

- 插槽body不越板边；
- 翻盖有打开空间；
- FFC可以从板边水平插入；
- 不和邻件发生明显机械冲突；
- Pin1和接触面方向在图面可识别。

---

# 这次必须重新把丝印做好

上一次KK方案我接受了mandatory companion替代完整ROW/COL丝印。

但既然现在**本来就必须重新做J2 footprint**，这次没有理由继续保留这个历史妥协。

新FFC J2至少要有：

```text
J2
PIN1 mark
ROW side / COL side indication
FFC INSERT direction
CONTACT SIDE indication
```

不要求把8个完整网名挤成一排影响可读性，但Pin1和插入/接触方向必须原生丝印清楚。

---

# P3把旧KK合同正式标为 superseded

新交付里更新：

- `J2_FFC_FPC_CONNECTOR_SPEC.md`
- `J2_FFC_CABLE_SPEC.md`
- `J2_PINOUT_AND_ORIENTATION.md`
- `J2_ACTUAL_SIGNAL_AND_MECHANICAL_PADS.csv`
- `FABRICATION_INPUT_CONTRACT.md`
- `MANUFACTURING_OPEN_ITEMS.md`

并明确：

```text
1718560008 + 22012087
= HISTORICAL SUPERSEDED INTERFACE

2005290081 + 154670229 default FFC standard
= CURRENT USER-REQUIREMENT INTERFACE
```

旧17/18/19报告不重写，只通过新包建立supersession关系。

---

# STOP条件

这次只有以下情况回来，不为小问题停：

- Molex官方drawing证明默认FFC/connector组合不机械兼容；
- 必须改ROW/COL顺序；
- 必须改板框；
- FFC插入空间与关键模拟器件发生无法局部解决的冲突；
- 其它175器件core或主模拟铜发生漂移；
- warm/cold出现不能在J2局部解释的Short/NetlistError。

局部clearance、局部fanout、mechanical anchor、局部pour变化都在授权范围内，不需要逐项回来请示。

---

## 当前最重要的纠正

这次不再把“8针”理解成8根独立电线。

用户要的是：

> **8芯薄软排线直接插进PCB上的ZIF/翻盖FFC/FPC座。**

我同意直接按 **8P / 1.00 mm / ZIF / bottom-contact** 做新J2，并以Molex `2005290081` + Premo-Flex `154670229`作为无现成排线时的默认板线标准。这个选择解决的是产品接口形态本身，值得做一次局部ECO。

其余电路和PCB主体不重开。