# CIRCUIT-PRO-R21-PCB-V3V3-MINIMAL-CONNECTION-CORRECTION-20261002-14

我按固定 commit `fe6955379a35493a33edb290b00145df5d2b1754` 审了这次 warm 实测 DRC、550 pin 对照和铜对象差异。

这次非常明确，**不是又发现大问题，也不是重新布板**：

> 当前PCB只剩 **V3V3上的2个 Connection Error**。  
> Short=0、Clearance=0、NetlistError=0。  
> 下一步就是局部把这两个对象真正接入V3V3，然后做warm+cold最终验收。

剩余对象是：

- `C_MCU1 pin1`，V3V3
- `via e255`，V3V3

而且我又对照了已有铜线：`C_MCU1_1`附近其实已经有V3V3走线，via e255附近也有V3V3线段。这更像**局部铜接触/孤岛闭合没真正被native connectivity识别**，不是网络定义错了。

---

## 关于907 / 909两条0.1 mil短线：不要修

这里我直接裁定，避免再次绕进去。

冻结File曾有909条LINE，实际重新打开的画布稳定呈现907条，少的是：

- 一条VCM 0.1 mil短段
- 一条TIA1 0.1 mil短段

本轮真实DRC对VCM/TIA1没有报：

- Connection
- Short
- Clearance
- Netlist

因此：

> **不要为了“恢复909这个数字”人工重建这两条0.1 mil线。**

它们继续记作：

`SERIALIZATION/REOPEN_REPRESENTATION_DIFFERENCE — CAUSE UNKNOWN`

工程验收以后以**实际重开画布的铜对象 + 原生DRC连通性**为准，而不是要求历史LINE数量字面相等。

换句话说，最终如果是例如909、910或其他数量，只要变化完全由这次批准的V3V3局部修正解释，且warm/cold一致、DRC全零，就是可以接受的。

---

# 唯一下一包批准

## `SCIENCE_ADK5556_4X4_R21_PCB_V3V3_MINIMAL_CONNECTION_CORRECTION_V1`

批准 **180 min**。

旧13号余额关闭，不结转。

授权额度：

- copy ≤ 1
- session ≤ 2
- save ≤ 2
- capture/audit ≤ 4
- DRC ≤ 4
- review export ≤ 1

仍然禁止：

- component move
- 改器件/值/footprint
- schematic修改
- Import Changes
- autorouter
- 大范围reroute
- 仿真
- Gerber
- 采购/制造
- bench/上电

---

## 修正方式：只允许局部V3V3铜

不要把两个DRC对象简单理解成“必须互相连一根线”。

正确处理是：

### 1. `C_MCU1_1`

在PCB GUI实际点击DRC对象，确认当前pad和附近V3V3铜。

允许：

> 用现有12 mil局部电源规则，把 `C_MCU1_1` **真实接到最近已经连通的V3V3铜**。

如果只是pad中心与现有segment端点存在极小几何脱离，可以删除/重画**这一小截局部V3V3线**，不要改其他网络。

### 2. via `e255`

同样点击native DRC对象。

允许：

> 将 e255 接入最近已确认连通的V3V3铜/plane。

如果发现e255本身没有必要、只是孤立遗留via，则**不允许直接删除**，除非GUI明确证明它没有承担层间连接且删除后V3V3 connectivity正常；优先通过局部铜桥接解决。

### 修正规模限制

原则上：

- 最多2个局部bridge；
- 如确有必要，最多1个新via；
- 不跨功能区；
- 不动MCU位置；
- 不重新规划V3V3主干。

这就是“修最后两个断点”，不是重布电源。

---

# 修完后立即跑第一次DRC

理想结果必须是：

```text
Connection Error = 0
Short = 0
Clearance = 0
Netlist Error = 0
```

如果还有Connection Error：

**不要继续自由尝试。**

只允许根据新DRC对象做**一次同区域最小修正**。

如果错误跳到别的net、出现Short/Clearance/NetlistError，立即STOP回来。

---

# Warm验收

修正后检查：

- 176 parts
- 550 pads
- 514 assigned
- 107 nets
- 36 NC

必须全部不变。

允许变化的对象只能是：

- V3V3局部LINE
- 必要时1个V3V3 VIA

其他：

- component identity
- pad-net
- placement
- rule
- non-V3V3铜

均不得漂移。

---

# Cold验收

Warm全零以后才：

1. 保存；
2. 正常关闭；
3. 独立重开同一工作副本；
4. 确认PCB1实际画布；
5. capture；
6. DRC。

最终要求：

```text
176 PARTS
550 PADS
514 ASSIGNED
107 NETS
36 NC

Connection = 0
Short = 0
Clearance = 0
NetlistError = 0
```

并且warm/cold：

- pad-net完全一致；
- component/footprint完全一致；
- 铜对象差异只能是稳定的序列化表示，不得出现新的功能铜消失；
- 本次V3V3修正必须在cold里仍然存在并被native connectivity识别。

---

## 907/909最终怎么记账

最终报告不要再写“必须恢复909”。

建议明确给三组数字：

- historical frozen File：909 LINE
- pre-fix actual reopened：907 LINE
- post-fix actual warm/cold：`N LINE`

然后解释：

> `N-907`只能来自本14包批准的V3V3局部修正；历史两条0.1 mil VCM/TIA1差异不强制重建。

这样证据最干净。

---

# 最终PASS门

只有下面全部满足，我才接受：

```text
PCB_ROUTING_COMPLETE = PASS
PCB_ELECTRICAL_CLOSURE = PASS
COLD_REOPEN = PASS

CONNECTION = 0
SHORT = 0
CLEARANCE = 0
NETLIST = 0

PCB_REVIEW_READY = TRUE
```

但仍然：

```text
MANUFACTURING_NOT_RELEASED
BENCH_NOT_RELEASED
```

因为后面还要做一次制造前审查。

---

现在已经不是“大问题”了。

**从452个未连接，已经收敛到2个V3V3断点。**  
这包只把这两个点接实，然后做一次真正的warm+cold全零验收。

按这个14号包继续，不要再碰整板其他地方。