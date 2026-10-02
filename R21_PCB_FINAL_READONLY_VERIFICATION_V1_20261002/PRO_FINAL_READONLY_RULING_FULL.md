# CIRCUIT-PRO-R21-PCB-ROUTING-IMPLEMENTATION-ACCEPT-FINAL-READONLY-VERIFY-20261002-13

我按固定 commit `ce6a8fc78b7ea7b545b2c2c678484086eb8d8b85` 重新看了完整回执、最后成功DRC、最终native证据、cold失败日志和图面补充。

结论很明确：

> **这次PCB布线实施本身可以接受为“已完成候选”，但还不能叫 `PCB_REVIEW_READY`。**
>
> 现在缺的不是继续布线，也不是继续改板，而是对**最后一次已保存的native PCB**做一次真正有效的 warm + independent cold 只读核验。

最后一次有效DRC是在补最后8个连接之前，当时是：

- Connection = 8
- Short = 0
- Clearance = 0
- NetlistError = 0

之后已经真实增加15条电源桥和1个via并重铺铜，但最终cold capture和DRC都因为PCB画布没有真正激活而失败。这个失败**不能解释成电气错误**，但也不能追认成PASS。

所以当前状态是：

```text
ROUTING_IMPLEMENTATION = COMPLETE_CANDIDATE
FINAL_NATIVE_SAVED = YES

LAST_VALID_DRC:
  CONNECTION = 8   # before final bridges
  SHORT = 0
  CLEARANCE = 0
  NETLIST = 0

FINAL_DRC = HOLD
FINAL_COLD_IDENTITY = HOLD

PCB_REVIEW_READY = FALSE
```

## 这次不允许再改任何铜

正式批准唯一下一包：

### `SCIENCE_ADK5556_4X4_R21_PCB_FINAL_READONLY_VERIFICATION_V1`

**120 min，从零计数。**

这一包完全只读：

- copy = 0
- session ≤ 2
- save = 0
- capture/audit ≤ 4
- DRC ≤ 4
- review export ≤ 1

并且：

- routing edit = 0
- component move = 0
- via edit = 0
- pour rebuild = 0
- Import Changes = 0
- schematic edit = 0
- API/SDK研究 = 0
- 仿真 = 0
- Gerber = 0
- 制造/采购/bench = 0

---

## 核验顺序固定，避免再次出现“画布没准备好”

### Session 1 — warm verification

打开**当前最终工作工程**，不是旧副本。

先在GUI里实际确认：

- 正确工程名；
- `PCB1`页签已经打开；
- PCB画布真实显示；
- 顶层/内层/底层layer bar可见；
- 当前文档确实是PCB而不是project tree。

**只有看到这些以后**才消耗capture/DRC次数。

然后执行：

1. 全量pad/net/component capture；
2. native detailed DRC；
3. 读取最终铜对象。

要求实际看到：

- 176 parts
- 550 pads
- 514 assigned
- 107 nets
- 36 NC
- 909 LINE
- 296 VIA
- 4 POUR / 4 POURED

并和当前冻结最终native逐对象比较。

---

### Session 2 — independent cold verification

完全关闭第一session。

重新打开同一个最终 `.eprj2`。

再次**人工确认PCB1真实画布已经激活**，然后：

1. 冷态全量capture；
2. 冷态native DRC；
3. 与warm逐项比较。

不是靠sleep，不是靠“openDocument返回成功”，而是先确认实际GUI画布。

---

# 最终硬门

如果这次真正得到：

```text
NetlistError = 0
ConnectionError = 0
Short = 0
Clearance = 0
```

并且warm/cold满足：

```text
176 parts
550 pads
514 assigned
107 nets
36 NC

pad-net identity identical
component/footprint identity identical
copper geometry identical
```

则我授权直接定为：

```text
PCB_ROUTING_COMPLETE
PCB_ELECTRICAL_CLOSURE_PASS
COLD_REOPEN_PASS
PCB_REVIEW_READY
MANUFACTURING_NOT_RELEASED
```

不需要再回来讨论routing。

---

## 还要额外看两个0.1 mil短段

报告里有两个最终新增但来源没有独立确认的极短段：

- VCM
- TIA1

这次只读核验顺手检查：

- 确实属于正确net；
- 两端接的是预期同网对象；
- 不是悬浮铜；
- 没产生短路/间距问题；
- 若只是路由切分形成的极短同网segment，可保留。

**不要仅因为它们短就重新编辑。**

只有确认它们是错误铜，才STOP。

---

# 如果最终DRC不是0，怎么处理

这次也不要现场修。

如果仍有任何真实：

- Connection Error
- Short
- Clearance
- Netlist Error

就保存完整明细并STOP。

特别是如果还是那8个V5/V3V3对象中的某几个，就直接告诉我**剩哪几个pad/via**，下一次只做最小铜修正，不重新布整板。

如果失败仍然只是“画布没订阅/null pins”，在本包允许的第二session内再按上述“先实际打开PCB1画布”流程执行一次；**不研究工具内部原因，不循环重试。**

---

## 我接受的现有PCB工程事实

现在这版已经不再是早期floorplan：

- 909条实际铜线；
- 296个via；
- 4个实际POURED区域；
- L2 GND为连续单一filled区域，且没有信号track穿越；
- V5/V3V3主干用了16/20 mil，局部12 mil；
- 关键小IC出口存在6 mil短颈，这是正常的局部几何现实；
- TIA/ROW/VCM/VEXC/ADC等敏感网络已经按功能区布过；
- 没有AGND/DGND人为割裂；
- 上一次有效DRC的Short/Clearance/Netlist都已经为0。

所以现在**绝对不要再开一个“大布线包”**。

唯一任务就是：

> **确认最后保存下来的那一版，确实已经把最后8个连接闭合，而且冷重开后仍然如此。**

---

## 120 min分配

| 阶段 | 时间 |
|---|---:|
| GUI实际PCB画布准备与身份确认 | 30 min |
| warm + independent cold全量核验 | 45 min |
| 证据整理和最终交付 | 45 min |

旧360 min包余额关闭，不结转。

---

### 当前一句话

**板子大概率已经布完了，现在不是继续画，而是给最后保存的PCB做最终验收。**

如果这次只读DRC得到4类电气错误全0、warm/cold一致，下一步就不再是PCB布线，而是**制造前审查**。
