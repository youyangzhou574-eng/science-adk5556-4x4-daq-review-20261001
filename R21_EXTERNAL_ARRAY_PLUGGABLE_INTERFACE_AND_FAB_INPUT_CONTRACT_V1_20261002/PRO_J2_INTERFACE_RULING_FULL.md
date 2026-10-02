# CIRCUIT-PRO-R21-MANUFACTURING-PREFLIGHT-ACCEPT-PLUGGABLE-J2-ECO-20261002-17

我已经按固定 commit `0b5b553f8077778fceb5bf2358faf6a99c5b93b0` 审了制造前矩阵、open items、J2实际接线和你新增的“**单排8针、可插拔、不是焊8根线**”要求。

先定结论：

> **制造前只读包接受。PCB主体不需要返工。**
>
> 但用户这个J2需求是真正的产品接口需求，当前通用 `HDR-M_2.54_1x8P` 还不能算完成。下一步只做一个**J2局部制造接口ECO**，不动主采集电路、不重布整板。

目前preflight没有发现无条件必须改主板铜/电路的其它问题；37项里18项限定PASS、16项PENDING、0项无条件ECO_REQUIRED，这个结论我接受。

---

## J2我直接给出默认方案，不再让你反复补信息

用户给的信息已经够用了：

- 单排8位；
- 板端可插拔；
- 线束端有匹配接头；
- 不能直接把8根线焊在PCB；
- ROW0–3 / COL0–3顺序保持。

因此默认冻结为 **2.54 mm Molex KK 254 wire-to-board体系**，这样和现在J2的2.54 mm单排8针电气间距最接近，改动最小。

### 首选板端

**Molex KK 254 RPC `1718560008`**

- 8 circuit；
- 单排；
- 2.54 mm pitch；
- Through-hole；
- vertical；
- friction lock；
- partially shrouded；
- 对接有极性方向。Molex当前官方页面也把它列为active的8位KK 254 PCB header。:chatgpt-content-reference{index="0"}

这比现在裸排针更符合你说的“**插槽式插拔**”。

### 线束端

优先使用 **KK 254 8位压接壳体 `22012087` / 22-01-2087**：

- 8 circuit；
- 单排；
- 2.54 mm；
- receptacle；
- friction ramp / locking。:chatgpt-content-reference{index="1"}

Molex自己的KK 254 wire-to-board参考手册同时给出了带锁扣receptacle、RPC header和24–30 AWG压接端子的系列组合，并说明friction-lock用于保持可靠插合。:chatgpt-content-reference{index="2"}

压接端子**暂不锁死MPN**，等实际线径确定。官方手册给了24–30 AWG的多种端子，例如 `08-50-0113 / 08-52-0101` 等。:chatgpt-content-reference{index="3"}

---

## 一个备用机械方向

如果实际检查发现竖直插拔影响操作空间，只允许一个备选：

**Molex `1718570008`**

同样：

- KK 254
- 单排8位
- 2.54 mm
- through-hole
- friction lock

但为**90° right-angle**。:chatgpt-content-reference{index="4"}

选择规则很简单：

> **默认1718560008竖直；只有实际板边/插拔空间不合适才换1718570008。**

不再引入JST-XH、双排IDC等第三套标准。

---

# J2针序完全不改

最终线束从pin1开始固定：

| Pin | Net | 阵列 |
|---:|---|---|
| 1 | ROW0 | 第0行 |
| 2 | ROW1 | 第1行 |
| 3 | ROW2 | 第2行 |
| 4 | ROW3 | 第3行 |
| 5 | COL0 | 第0列 |
| 6 | COL1 | 第1列 |
| 7 | COL2 | 第2列 |
| 8 | COL3 | 第3列 |

16个待测电阻还是：

\[
R_{ij}: ROW_i \leftrightarrow COL_j
\]

**不加GND、不加电源、不改变8线架构。**

并要求PCB丝印明确：

`1 / ROW0`

或者至少：

- Pin 1三角/圆点；
- `ROW0–ROW3`
- `COL0–COL3`

防止线束反插或编号错位。

---

# 唯一下一包批准

## `SCIENCE_ADK5556_4X4_R21_EXTERNAL_ARRAY_PLUGGABLE_INTERFACE_AND_FAB_INPUT_CONTRACT_V1`

批准 **180 min**。

### P0 — 成套连接器核实：45 min

只核：

- `1718560008`；
- 备用 `1718570008`；
- `22012087`；
- 官方mating/dimensional drawing；
- 推荐PCB孔径、body envelope；
- Pin1方向；
- 实际线径对应terminal。

官方连接器资料≤4，候选≤2。

如果官方图明确证明上述housing/header不能正常配套，才STOP，不自己猜配。

---

### P1 — 最小J2 ECO：30 min

这次允许修改schematic和PCB，但范围只到J2。

允许：

- J2 generic header → 最终选定的KK254准确MPN；
- 对应manufacturer footprint；
- body/courtyard/silkscreen；
- pin1标识；
- 必要时仅J2附近短距离fanout调整。

禁止：

- 改J2 pin-net次序；
- 改ROW/COL网络；
- 改任何其它器件值；
- 改主电路；
- 重布整板。

如果新连接器仍是8个PTH pad，那么设计层面预期仍是：

- 176 components
- 550 pads
- 514 assigned
- 107 nets
- 36 NC

但**不要把这些数字预先强制成真**：若厂家footprint包含合法的机械定位孔或非电气pad，应单独记为mechanical feature，而不是为了维持550去删正确机械结构。

---

### P2 — PCB局部温/冷验证：45 min

ECO后必须：

1. Import Changes只针对J2身份/footprint；
2. 检查J2周围body、板边和现有铜；
3. 必要局部reroute；
4. Rebuild pour；
5. native DRC。

Warm要求：

```text
Connection = 0
Short = 0
Clearance = 0
NetlistError = 0
```

然后save、关闭、独立cold reopen。

Cold仍要求四类全部0。

同时必须证明：

- J2.1–8仍对应原ROW/COL；
- 其余175器件pin-net没有变化；
- 主模拟区铜没有变化；
- connector body不越板边；
- 插头方向存在真实机械空间。

---

### P3 — 制造合同与交付：60 min

更新：

- `FABRICATION_INPUT_CONTRACT.md`
- `MANUFACTURING_OPEN_ITEMS.md`
- `J2_CONNECTOR_AND_HARNESS_SPEC.md`
- `J2_PINOUT_AND_KEYING.md`
- `MANUFACTURING_PREFLIGHT_MATRIX.csv`

其中要明确：

**板端MPN + 线端housing + terminal范围 + pin1方向 + 线束8芯顺序。**

---

# 制造工艺其他PENDING暂时不要卡这个接口ECO

当前还没选板厂，所以以下继续PENDING即可：

- stackup；
- 板厚；
- 铜厚；
- finish；
- mask；
- stencil/reflow；
- panel/fiducial。

特别是U5/U9/U10约0.09–0.097 mm阻焊桥的问题：

**现在不改footprint。**

等目标板厂明确工艺能力；如果厂商CAM拒绝，再做一次集中manufacturing ECO。

---

# 本包范围

批准：

- copy ≤1
- session ≤2
- save ≤2
- capture/audit ≤3
- DRC ≤3
- export ≤1
- official connector sources ≤4
- candidate ≤2

禁止：

- 主电路仿真
- MIMO / descriptor
- 全板reroute
- 新功能电路
- Gerber生产放行
- 下单
- 采购
- 制造
- bench / 上电

---

## 真正STOP条件

只有这些回来：

1. 官方资料证明首选/备选KK254无法和线端成套配合；
2. 新J2机械body与现有板边/关键器件发生实质冲突，局部移动无法解决；
3. 必须改变ROW/COL pin顺序；
4. 必须改板框；
5. J2局部ECO后出现无法在局部解决的Short/NetlistError；
6. 其它175器件或主模拟铜发生漂移。

普通silkscreen、connector周围几根短线、局部pour变化不属于STOP。

---

## 当前阶段一句话

现在PCB主体已经通过电气review。

**当前唯一真正还没产品化的是“待测阵列怎么插上去”。**

我这里已经把它从模糊的“找个8针插槽”收敛成：

> **Molex KK 254，8位、单排、2.54 mm、带摩擦锁的板线连接器体系。**

下一包只把J2从“通用裸排针”换成**确切可插拔的板端+线端成套接口**，然后局部DRC/cold复核。

这样解决的是实际使用问题，不是又开始绕理论。
