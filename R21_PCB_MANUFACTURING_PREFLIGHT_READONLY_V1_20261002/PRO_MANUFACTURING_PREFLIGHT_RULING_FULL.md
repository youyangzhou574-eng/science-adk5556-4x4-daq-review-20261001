# CIRCUIT-PRO-R21-PCB-ENGINEERING-CLOSURE-ACCEPT-MANUFACTURING-PREFLIGHT-20261002-16

我已按固定 commit `e9c1b72f4d1659bb9a7a1dbe4a82e7937c5fe86a` 审阅15号完整回执、warm/cold原生DRC、工程接受文件和终审。

这次可以正式收口：

> **PCB布线、电气闭合、冷重开三项全部接受。当前PCB进入 `PCB_REVIEW_READY`。**
>
> 不再开PCB修正包，不再回去动铜、覆铜、网络或原理图。

当前最终工程状态接受为：

```text
PCB_ROUTING_COMPLETE = PASS
PCB_ELECTRICAL_CLOSURE = PASS
COLD_REOPEN = PASS
PCB_REVIEW_READY = TRUE

Connection = 0
Short = 0
Clearance = 0
NetlistError = 0

176 parts
550 pads
514 assigned
107 nets
36 NC
```

warm与独立cold两次真实native DRC都明确返回 `ok=true, value=[]`，这一点足以作为当前EDA电气闭合证据。

---

## 一、15号表示差异怎么裁定

### POURED的215个极小浮点差异

最大只有约：

\[
2.1\times10^{-12}
\]

并且：

- 对象增删=0；
- 结构变化=0；
- LINE/VIA、component、pad-net、rule、POUR boundary全部一致；
- warm/cold原生DRC均全0。

因此正式接受为：

> **稳定的派生覆铜表示差异，不是PCB设计漂移。**

不需要追查内部序列化原因。

---

### 909 vs native File 911 LINE

多的仍是此前那两条0.1 mil的 VCM/TIA1表示短段。

15号已经证明实际重开工程、warm/cold DRC全0，所以：

> **这个LINE数量差异不再是任何工程HOLD。**

不恢复、不删除、不研究。

---

### cold DRC预扣控制偏差

这属于**执行流程记账偏差**，不是设计证据失效。

保留原始记录即可；因为实际第二次cold DRC：

- 没有修改工程；
- 在批准的DRC总次数内；
- 返回有效native结果；
- 最终没有继续CAD mutation。

所以它**不阻止技术接受**，但也不从历史记录中抹掉。

---

# 二、冻结新的PCB基线

从现在开始制造前审查统一引用：

### Accepted PCB baseline

- commit：`e9c1b72f4d1659bb9a7a1dbe4a82e7937c5fe86a`
- native：`SCIENCE_ADK5556_4X4_R21_PCB_CLOSED_REVIEW.epro2`
- SHA256：

`C2D53B0B6BB438D7C916BE24CB0B0D6AE5C7D884E7784EEFFED90E61505BEE6C`

这版冻结。

**制造前审查期间不得重新保存一次“更干净”的PCB。**

---

# 三、唯一下一阶段批准

## `SCIENCE_ADK5556_4X4_R21_PCB_MANUFACTURING_PREFLIGHT_READONLY_V1`

批准申请的 **180 min**。

这一步不是继续画PCB，而是回答：

> **如果以后要把这块板真正交给板厂，这个冻结设计在工艺、封装、装配、测试可达性上还有没有明显制造风险？**

全程只读。

---

## P0 — 制造输入与stackup合同：45 min

基于当前冻结的：

- 100 × 90 mm
- 4层
- L1 signal/components
- L2 continuous GND
- L3 power / signal
- L4 signal

整理：

`FABRICATION_INPUT_CONTRACT.md`

需要明确而不是猜测：

- 板厚；
- 铜厚；
- 外层/内层最小线宽线距；
- 最小钻孔；
- 最小via pad/annular ring；
- solder mask规则；
- surface finish；
- 最小铜到板边；
- castellated/controlled impedance是否需要；
- 阻燃等级等。

目前这些**没有用户/板厂冻结值的，全部写PENDING**。

允许查≤6个官方板厂/元器件资料，只为验证普通工艺可制造性，不扩大成供应链研究。

---

# 四、P1 — 冻结PCB制造规则审查：45 min

重点不是再跑EDA DRC，而是检查当前真实设计几何有没有明显制造边缘项。

尤其逐项审：

### 6 mil短颈

已有小IC出口约6 mil。

需要确认目标普通4层工艺是否覆盖。

### Via

当前典型：

- hole 12 mil
- diameter 24 mil

换算约：

- 0.305 mm drill
- 0.610 mm pad

这通常不算激进，但要按目标板厂实际能力核一次。

### 10 mil clearance

确认符合选定普通工艺，不需要为追求更小线距重新设计。

### 电源线

12 / 16 / 20 mil局部与主干只做制造可行性检查。

**不再重新进行载流理论优化。**

### 铜到板边 / 铜皮孤岛 / 阻焊桥

重点看：

- 四个POUR；
- L2 GND；
- V3V3/V5；
- 新e307区域；
- J1/J2/J3/J4边缘区域。

---

# 五、P2 — Footprint / assembly / 可测试性：30 min

这一层比继续看DRC更重要。

至少检查：

- OPA4388 / OPA2388
- ADS8684
- STM32G031K8
- TMUX1134
- TPS389001
- LM73100
- BAT54S
- J1–J4

逐项：

- pad number ↔ device pin；
- footprint pitch；
- exposed pad（如有）；
- pin1方向；
- courtyard/器件间距；
- 是否存在手焊/贴装明显困难；
- 极性标识；
- 连接器方向。

另外生成：

`ASSEMBLY_AND_TEST_ACCESS_CHECKLIST.md`

至少标出以后实测最好能探到：

- V5_IN
- V5
- V3V3
- REF_2V5
- VCM
- VEXC
- PGOOD/NRST
- ROW0
- TIA0/TIA_DRV0
- ADC_IN0

这里不是要求现在一定新增test point。

只判断**现有器件脚/焊盘是否可以合理探测**。

如果未来确实无法安全探测某关键节点，再集中提一个manufacturing ECO建议；本包不修改。

---

# 六、P3 — 制造前接受矩阵：45 min

输出一个：

`MANUFACTURING_PREFLIGHT_MATRIX.csv`

每项只能落到：

- PASS
- PENDING_INPUT
- ECO_REQUIRED
- NOT_APPLICABLE

不要使用含糊的“应该没问题”。

还需要：

`MANUFACTURING_OPEN_ITEMS.md`

只列真正影响生产的事情。

例如：

- 板厚还没决定 → `PENDING_INPUT`
- 铜厚没决定 → `PENDING_INPUT`
- 某封装pad真的错 → `ECO_REQUIRED`
- PDF旧网名显示问题 → **不是制造阻断项**

---

# 七、预留15 min

只用于：

- 交叉核对；
- 收敛报告；
- 修普通文档错误。

**不能拿来开启CAD。**

---

# 八、本包明确禁止

本包所有这些都是0：

```text
new CAD edit = 0
session = 0
save = 0
capture = 0
DRC = 0
native export = 0
routing = 0
schematic edit = 0
simulation = 0
Gerber generation = 0
procurement = 0
manufacturing = 0
bench = 0
power-up = 0
```

普通只读解析现有native/CSV/PNG/规则证据允许。

---

# 九、这一步不要做成“又一轮过度验证”

这一点我特别强调。

制造前审查只回答三个问题：

1. **这个PCB几何按普通4层工艺能不能做？**
2. **这些封装和器件方向有没有明显制造风险？**
3. **如果要下单，目前还缺哪些具体输入？**

不要重新：

- 证明模拟稳定性；
- 做寄生仿真；
- 做SI/PI全板分析；
- 重算热仿真；
- 研究EDA内部格式；
- 因为一个Description乱码修库。

这些都不属于当前主线。

---

# 十、Minor：Description乱码怎么处理

终审提到API导出的某个Description里有U+FFFD乱码。

裁定：

> **这个字段不得作为制造BOM authority。**

制造BOM以后以：

- Designator
- Manufacturer
- Manufacturer Part Number
- Value
- Footprint
- Quantity

等经过核实的结构字段为准。

不修这个Description乱码。

---

# 十一、下一次希望看到什么

理想交付应该直接告诉我：

```text
PCB_MANUFACTURING_PREFLIGHT_COMPLETE

PCB geometry:
PASS / PENDING items

Footprints:
PASS / specific ECO item

Assembly:
PASS / specific ECO item

Stackup/fab settings:
explicit pending inputs

MANUFACTURING_RELEASE = FALSE
```

如果发现真实设计阻碍，**一次集中列出来**，不要每发现一个小项就开新包。

---

## 当前项目阶段一句话

现在已经从：

**原理图 → PCB同步 → 布线 → DRC → cold reopen**

全部走完。

当前正式进入：

> **制造前只读审查。**

PCB本身现在不用再修，除非制造preflight真正发现一个具体、可证实的生产问题。
