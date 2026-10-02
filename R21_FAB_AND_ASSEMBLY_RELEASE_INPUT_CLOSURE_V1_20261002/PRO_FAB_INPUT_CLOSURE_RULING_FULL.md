# CIRCUIT-PRO-R21-J2-ECO-ACCEPT-WITH-SILK-VARIANCE-20261002-18

我已按固定 commit `bcafa5c6b834c20539774cd335d34586442453be` 审了 J2 实际8针、配套选料、warm/cold DRC、制造矩阵和终审。

结论先给：

> **J2 电气、2D封装、板上线序和板端/线端成套接口这部分正式接受。**
>
> **不再为了 ROW/COL 丝印文字单独重开 CAD。**
>
> 当前缺少的 ROW0–ROW3 / COL0–COL3 板上文字，从“conformance blocker”降级为**已接受的文档/装配偏差**，由强制 pinout companion 兜底。

所以这次不需要再为了几个丝印字，把已经 warm/cold DRC 全0的板重新打开、保存和再验一次。

---

## 一、正式接受的J2状态

接受以下事实：

- 板端：Molex `1718560008`
- 线端壳体：`22012087 / 22-01-2087`
- 8位、单排、2.54 mm
- 竖直PTH
- friction-lock
- 实际8孔：
  - 孔约1.14 mm
  - 铜盘约1.70 mm
- J2.1–8仍严格为：
  - ROW0
  - ROW1
  - ROW2
  - ROW3
  - COL0
  - COL1
  - COL2
  - COL3
- 其余175器件、550 pin-net、主LINE/VIA/POUR/rules无漂移
- warm DRC = 0
- independent cold DRC = 0
- 176 / 550 / 514 / 107 / 36保持

因此：

```text
J2_ELECTRICAL_INTERFACE = PASS
J2_2D_FOOTPRINT = PASS
J2_PIN_ORDER = PASS
J2_BOARD_EDGE_CLEARANCE = PASS
J2_WARM_COLD_DRC = PASS
```

---

# 二、丝印偏差怎么裁定

17号我之前要求：

- 至少Pin1标记；
- 最好有 `1/ROW0`；
- 或者ROW/COL文字。

现在实际板上已经有：

- `J2`
- 方形1脚
- Pin1三角

缺的是：

- ROW0–ROW3
- COL0–COL3文字。

我这次正式接受：

## `J2_SILK_TEXT_VARIANCE_ACCEPTED`

理由很简单：

实际误接防护已经有三层：

1. 方形Pin1；
2. Pin1三角；
3. 强制随板使用的 `J2_PINOUT_AND_BODY.png + J2_ACTUAL_8PIN_HARNESS.csv + J2_CONNECTOR_AND_HARNESS_SPEC.md`。

对于这种实验室验证板，继续为了8个丝印标签修改原生PCB，工程收益已经低于重新打开CAD带来的版本风险。

所以：

```text
J2_NATIVE_SILK_ROWCOL_MISSING = TRUE
J2_SILK_TEXT_VARIANCE_ACCEPTED = TRUE
J2_ECO_CONFORMANCE_HOLD = RELEASED
```

但这里有个重要边界：

> **不能以后在报告里写“板上已经印了ROW0–COL3”。**

正确表述是：

> 板上有J2 + Pin1几何标记，完整ROW/COL映射由强制装配pinout companion提供。

---

# 三、PCB_REVIEW_READY恢复

17包里为了严格符合我之前文字要求，把：

`PCB_REVIEW_READY=false`

挂了起来。

这个现在可以解除。

正式状态改为：

```text
PCB_REVIEW_READY = TRUE

J2_ELECTRICAL_AND_2D_FOOTPRINT_REVIEW_PASS = TRUE
J2_SILK_VARIANCE_ACCEPTED = TRUE

MANUFACTURING_RELEASE = FALSE
PROCUREMENT_RELEASE = FALSE
BENCH_RELEASE = FALSE
```

也就是说：

**PCB本身不再有需要返工的已知问题。**

---

# 四、generic device / old 3D也不需要现在修

这两项继续保持：

- `J2_GENERIC_DEVICE_METADATA_HOLD`
- `J2_3D_NOT_QUALIFIED`

但是它们现在也不是PCB返工门。

制造和装配时：

**不能按generic device名采购，必须按：**

- Board header = `1718560008`
- Housing = `22012087`
- 项目实际footprint = `MOLEX_1718560008_MFR_SD171856_R17`

来执行。

旧generic 3D模型不能拿来做真实mated机械认证。

---

# 五、真正还缺的J2输入只剩一个

就是：

## 压接端子

现在不要再扩大成“连接器方案研究”。

板端和housing已经定了。

只差：

- 实际导线AWG；
- 绝缘外径；
- 镀层偏好；
- 压接方式。

这决定具体terminal MPN。

如果你们将来用普通实验室线束，我建议优先按：

**24–26 AWG**

准备。

但在用户没有给真实线材前：

> **不锁具体terminal型号。**

这是采购/线束输入PENDING，不是PCB设计HOLD。

---

# 六、唯一下一包不再做丝印

不批准申请的：

`R21_J2_SILK_CONFORMANCE_AND_ASSEMBLY_INPUT_CLOSURE_V1`

因为“silk conformance”已经通过偏差接受解决，没有必要再花CAD预算。

改为唯一下一包：

# `SCIENCE_ADK5556_4X4_R21_FAB_AND_ASSEMBLY_RELEASE_INPUT_CLOSURE_V1`

目标：

> 把现在这块已经设计完成的PCB，从“工程审查版”推进到“随时可以生成制造资料，但尚未下单”的状态。

---

## 新包预算：180 min

### P0 — 制造参数默认方案：45 min

不再全部写PENDING。

给出一个**普通4层验证板默认制造合同**，例如收敛到：

- FR-4
- 4-layer
- 1.6 mm nominal
- 1 oz outer / 1 oz inner作为首选
- standard through-hole via
- ENIG或HASL选择建议
- solder mask默认绿色
- 普通板厂6 mil能力要求
- 0.305 mm drill / 0.610 mm via pad可接受要求

这是“推荐制造输入”，不是下单。

如果目标板厂还没选，保留：

`FABRICATOR_PENDING`

但其余不需要全部空着。

---

### P1 — BOM / 装配输入闭合：45 min

重点检查：

- 176器件结构BOM；
- 四个generic connector中，J2现在已有明确MPN；
- 哪些器件仍缺manufacturer/MPN；
- pin1 / polarity；
- assembly critical notes；
- hand-solder vs SMT assembly边界。

产出：

`ASSEMBLY_RELEASE_INPUTS.md`

---

### P2 — J2线束合同：30 min

把已接受方案固化成：

`J2_HARNESS_BUILD_SPEC.md`

写明：

- 8芯顺序；
- ROW/COL；
- housing；
- terminal待AWG；
- Pin1追线方法；
- continuity test；
- 不允许按housing模制编号直接假定电气序号。

如果线径尚无输入：

`EXACT_TERMINAL = PENDING_AWG`

即可。

不要再次查询十几个候选。

---

### P3 — Manufacturing release checklist：45 min

输出：

`MANUFACTURING_RELEASE_CHECKLIST.md`

只回答：

- 哪些已经PASS；
- 哪些下单前必须填；
- 哪些需要板厂CAM确认；
- 哪些是装配厂输入；
- 哪些不是blocking。

特别是：

U5/U9/U10约0.09–0.097 mm阻焊桥继续记：

`FAB_CAM_CONFIRM_REQUIRED`

而不是现在修改footprint。

---

### P4 — 交付余量：15 min

只做文档交叉核对。

---

# 七、下一包完全禁止CAD

这次：

```text
CAD edit = 0
session = 0
save = 0
capture = 0
DRC = 0
native export = 0
routing = 0
pour = 0
schematic = 0
Import Changes = 0
simulation = 0
Gerber = 0
procurement = 0
manufacturing = 0
bench = 0
```

也不再研究：

- JLCEDA metadata；
- generic 3D；
- Description乱码；
- 909/911 LINE表示差；
- API内部格式。

---

# 八、下一个真正需要你给我的输入

这一步目前不用立即回答，但到了线束采购前只需要一个很简单的信息：

> **你准备接阵列的8芯线大概用多粗？**

例如：

- 22 AWG
- 24 AWG
- 26 AWG
- 28 AWG

如果不知道，后面默认按 **24–26 AWG实验室线束** 设计即可。

无需现在重新开一个问答门。

---

# 九、当前项目状态

正式更新为：

```text
SCHEMATIC = ACCEPTED

PCB_ROUTING = PASS
PCB_ELECTRICAL_CLOSURE = PASS
PCB_COLD_REOPEN = PASS

J2_PLUGGABLE_INTERFACE = PASS
J2_PIN_ORDER = PASS
J2_SILK_TEXT_VARIANCE = ACCEPTED
PCB_REVIEW_READY = TRUE

FAB_INPUT_CLOSURE = NEXT
MANUFACTURING_RELEASE = FALSE
PROCUREMENT_RELEASE = FALSE
BENCH_RELEASE = FALSE
```

现在PCB设计本身可以认为结束了。

下一步不是再画板，而是：

**把板厂参数、装配BOM和J2线束制造输入收敛好。**

这样主线才继续往“真的做出一块板”推进，而不是为了几个丝印文字在EDA里来回循环。