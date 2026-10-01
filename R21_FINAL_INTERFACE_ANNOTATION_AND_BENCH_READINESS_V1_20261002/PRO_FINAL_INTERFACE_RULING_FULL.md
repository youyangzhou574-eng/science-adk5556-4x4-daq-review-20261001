# CIRCUIT-PRO-R21-FUNCTIONAL-NETLIST-REVIEW-AND-BENCH-READINESS-20261002-10

我按固定 commit `149e6706b024f490e3285dfdd310d17061a32cad` 又做了一遍你之前特别要求的**两层检查**：一层看嘉立创实际落图，一层不相信计划网表本身、重新沿着电路功能追线。

结论先说：

> **嘉立创实际 pin-net 落实这一层通过了；主采集电路功能连线我也没有发现新的架构级错误。**
>
> **但是我额外抓到 1 个真实的外部接口连线设计问题，所以当前这版我还不想直接叫“最终 bench-ready”。**

这正是你之前让我“别光看514/514”的原因。

---

## 一、嘉立创实际落实：接受 PASS

这一层证据足够扎实：

- Audit A：168 parts / 498/498 / 104 nets / 36 NC；
- Audit B：172 / 506/506 / 106 / 36；
- Audit C：176 / 514/514 / 106 / 36；
- 独立冷重开 D：仍然 **176 / 514/514 / 106 / 36**；
- C/D 的 **514 个 pin-net 与 106 个网络成员集合完全一致**；
- 器件核心字段、物理 pin、NC 坐标冷重开保持一致；
- 四个22 pF已经从之前撞件的位置移到独立空白行，并真实连接：
  `TIA_DRV_i ↔ COL_SENSE_i`；
- U3.2/U3.6现在实际分别是 `VCM_FB / VEXC_FB`；
- RESET实际已经是1 kΩ；
- 四个ADC输入电容字段实际是10 nF。

所以之前那个“电容压在别的器件上造成整板并网”的错误已经**真正修掉**了，不是表格上假修。

`PIN_NET_IMPLEMENTATION_PASS`  
`COLD_REOPEN_PASS`

这两项我接受。

---

# 二、我重新手工追了核心电路，主采集链目前是对的

我没有只拿 `PLAN_FINAL.json` 自证，而是重新对关键IC官方pinout和实际net走了一遍。

### VCM / VEXC

OPA2388实际：

- U3.1 → `VCM_DRV`
- U3.2 → `VCM_FB`
- U3.3 → 2.5 V reference
- U3.7 → `VEXC_DRV`
- U3.6 → `VEXC_FB`

和OPA2388真实的 OUT/−IN/+IN pinout相符。:chatgpt-content-reference{index="0"}

反馈现在是：

`VCM_DRV → 1k → VCM`

`VCM → 4.99k → VCM_FB`

`VCM_DRV → 100p → VCM_FB`

VEXC同构。

**这是我们要的隔离后远端DC反馈 + 高频补偿结构。**

---

### 四个ROW

例如ROW0：

`TMUX1134 → ROW_CMD0 → OPA4388 +IN`

`OPA output ROW_DRV0 → 1k → ROW0`

`ROW0 → 4.99k → ROW_FB0 → OPA −IN`

`ROW_DRV0 → 100p → ROW_FB0`

这也是正确的。

TMUX1134实际pin mapping也匹配官方：SEL=0选择B端，SEL=1选择A端；现在B端是VCM，A端是VEXC，因此：

- `ROW_SEL=0` → VCM（blank）
- `ROW_SEL=1` → VEXC（active）

与八状态逻辑一致。:chatgpt-content-reference{index="1"}

---

### 四个TIA

例如CH0现在实际是：

`COL0 → 10k → COL_SENSE0 → U2 −IN`

U2 `+IN → VCM`

`U2 output TIA_DRV0 → 1k → TIA0`

主反馈：

`TIA0 → 4.99k || 2.2nF → COL0`

ADC：

`TIA0 → 100Ω → ADC_IN0`

`ADC_IN0 → 10nF → GND`

新增HF补偿：

`TIA_DRV0 → 22pF → COL_SENSE0`

这和我们最终冻结的结构一致。

OPA4388各通道实际OUT/−IN/+IN编号也与TI pinout一致。:chatgpt-content-reference{index="2"}

---

### ADC

ADS8684关键pin实际也是对的：

- 1 SDI → MOSI
- 2 RST/PD → ADC_RESET_N
- 5 REFIO
- 7 REFCAP
- 9/30 AVDD → 5 V
- 34 DVDD → 3.3 V
- 36 SDO
- 37 SCLK
- 38 CS

且RST/PD确实是**低有效**，长低电平会进入power-down，所以当前硬件门控方向没有接反。:chatgpt-content-reference{index="3"}

---

### MCU / supervisor / RESET

STM32G031K8T6：

- pin6确实是NRST；
- 11–14对应PA4–PA7，可以承担SPI；
- 7–10对应PA0–PA3，可用于四路ROW控制。

实际图里U7.6=`PGOOD`，因此两个TPS3890 open-drain reset和外部NRST最终确实都作用在MCU reset节点。:chatgpt-content-reference{index="4"}

TPS3890实际：

- pin1 SENSE
- pin2 GND
- pin3 MR
- pin4 VDD
- pin5 CT
- pin6 open-drain RESET

当前U11/U12把MR固定高、VDD接3.3 V、RESET并到PGOOD，这个方向正确。:chatgpt-content-reference{index="5"}

两个monitor分压我也重新算了一眼：

- 5 V监控约在 **4.83 V** 一带触发；
- 3.3 V监控约在 **3.10 V** 一带触发；

和TPS389001约1.15 V可调threshold吻合。:chatgpt-content-reference{index="6"}

---

### BAT54S钳位方向

这个我也专门重新核了，因为这种三脚二极管最容易画反。

BAT54S：

- pin1 = A1
- pin2 = K2
- pin3 = K1/A2

所以现在大量接口采用：

- pin1 → GND
- pin2 → supply
- pin3 → signal

确实形成：

`GND → signal`

和：

`signal → supply`

两方向Schottky clamp。

**方向没有画反。** :chatgpt-content-reference{index="7"}

---

# 三、但是我这次发现了一个新的实际设计问题：V3V3_EXT两只4.99k实际上并联了

这是当前唯一我认为应该在bench准备前修掉的连接问题。

最终实际网络成员现在是：

`V3V3_EXT = J3.1 + J4.1 + R_J3_1.1 + R_J4_1.1`

而：

- `R_J3_1 = 4.99k` → V3V3
- `R_J4_1 = 4.99k` → V3V3

所以实际电路等效成：

\[
4.99k\parallel4.99k \approx 2.495k\Omega
\]

从 `V3V3_EXT` 到板上 `V3V3`。

这和原本备注中“J3、J4各自通过4.99 kΩ限流的3.3 V sense接口”并不完全一致。

### 正常工作下

问题不大。

两个接口本来就是高阻的target-voltage sense，所以正常测3.3 V基本不会因此失败。

### 但故障/外接设备边界下

它会把我们原本认为的4.99 kΩ限流**减半**。

如果一个外部设备误向这个节点灌电，实际故障电流约是之前按单4.99k估计的两倍。

而且J3和J4两个“外部3.3 V sense”口在电阻**之前已经直接相连**。

因此它不是致命架构问题，但它确实属于：

`FUNCTIONAL_NETLIST_MINOR_CORRECTION_REQUIRED`

这次必须修，而不能因为514/514就放过去。

---

# 四、这个问题怎么修非常简单

我建议不换器件、不重新设计：

把现在一个共同：

`V3V3_EXT`

拆成两个网：

`V3V3_EXT_SWD`

和

`V3V3_EXT_UART`

变成：

`J3.1 → R_J3_1 4.99k → V3V3`

`J4.1 → R_J4_1 4.99k → V3V3`

这样每一个外部接口才真正拥有自己的4.99 kΩ串联限流。

器件数量仍：

**176**

连接pin数量仍：

**514**

NC仍：

**36**

只是net由：

**106 → 107**

这是纯粹的net label/连接拆分，不改主电路。

---

# 五、还有一个我不建议现在改，但bench必须重点看的地方：SWD串联4.99k偏大

现在：

SWDIO / SWCLK也是4.99 kΩ串联。

从保护角度很好，但作为高速数字接口，**4.99 kΩ明显比一般SWD串阻大**。

它不一定不能用——低SWD时钟大概率可以工作——但是30 cm线缆、输入电容和4.99 kΩ组合后，高速边沿可能变慢。

这不是当前“连接画错”，因此我不建议现在又改设计。

但首轮调试必须：

> **ST-LINK/SWD先从低速开始，例如100 kHz量级，再逐渐提高。**

如果低速都不能稳定编程，再决定是否把SWD串阻降到更常规范围。

UART同理，普通115200附近大概率宽松得多。

所以标：

`SWD_SERIES_RESISTOR_BENCH_CHECK`

不作为当前原理图STOP。

---

# 六、其他我重点查的几个容易出错点目前没发现问题

例如：

- LM73100的IMON pin9现在直接接GND；TI明确允许IMON不用时接地，所以这里不是错误。:chatgpt-content-reference{index="8"}
- LM73100 DNC pin10保持NC，正确。:chatgpt-content-reference{index="9"}
- REF3025不要求输出电容才能稳定；其输入旁路要求也已经有供电去耦，因此这里没有发现缺失的强制输出电容。:chatgpt-content-reference{index="10"}
- TMUX1134 pin15为NC，当前确实没接。:chatgpt-content-reference{index="11"}
- SN74LVC08未使用门的输入拉低、输出NC，没有看到把逻辑输出直接短地的问题。

所以这次重新“从器件脚到功能”过一遍后，**没有发现需要推翻主采集架构的错误**。

---

# 七、因此当前状态不是“完全最终”，而是非常接近最终

我现在把状态定成：

```text
CORE_ACQUISITION_TOPOLOGY_REVIEW_PASS
NATIVE_PIN_NET_IMPLEMENTATION_PASS
COLD_REOPEN_PASS

V3V3_EXT_INTERFACE_SPLIT_REQUIRED
LEGACY_ANNOTATION_HOLD
ERC_DETAIL_HOLD

BENCH_NOT_RELEASED
PCB_NOT_STARTED
```

也就是说：

> **主电路现在可以认为已经审过；还剩一个很小的外部3.3V sense网络修正，再把旧备注处理一下，就进入台架准备。**

---

# 八、唯一下一包稍微调整一下

不再只叫 annotation package。

## `SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_ANNOTATION_AND_BENCH_READINESS_V1`

只允许三件事：

1. **拆分 `V3V3_EXT`**
   - J3和J4各自独立4.99k；
   - 预期最终：
     - 176 parts
     - 514 connected pins
     - **107 nets**
     - 36 NC；
   - 保存后冷重开再次全量比较。

2. **旧备注修正**
   - 只尝试既有官方文字接口；
   - 最多一次；
   - 如果还是写不进去，保留 `DRAWING_ANNOTATION_ADDENDUM.md`；
   - **备注不能再卡主线。**

3. **台架合同最终整理**
   - 不上电；
   - 加入：
     - SWD低速起步要求；
     - 两个V3V3 sense端口不得作供电输入；
     - 1–7 kΩ正常范围；
     - 0.8–8 kΩ保护带；
     - 300 µs；
     - 100 fps；
     - 两点校准；
     - 10%变化。

---

# 九、批准新的180 min

旧09包预算关闭，不结转。

新包：

| 阶段 | 时间 |
|---|---:|
| V3V3_EXT拆分 + 实际File/冷重开 | 45 min |
| annotation + 最终PDF核图 | 30 min |
| bench readiness合同 | 45 min |
| 完整交付 | 60 min |

总计：

\[
\boxed{180\text{ min}}
\]

授权：

- copy≤1
- session≤2
- save≤2
- capture/audit≤2
- PDF≤1
- ERC=0

仍然：

- 仿真0
- protocol新测试0
- reset解析0
- library/source/candidate 0
- 实际bench 0
- PCB 0
- 制造/采购 0

---

# 十、下一次我要求看到的最终结果

如果顺利，应该回来的是：

```text
176 PARTS
514/514 PIN_NET PASS
107 NETS
36 NC
COLD_REOPEN PASS

CORE_FUNCTIONAL_NETLIST PASS
DRAWING READABLE
BENCH_PLAN READY
BENCH_NOT_YET_EXECUTED
```

而不是再回来讨论MIMO、descriptor或者“有没有更严谨的稳定性证明”。

这一次我确实按你之前要求的方式重新看了**设计本身**。也正因为如此，才抓到了 `V3V3_EXT` 两只4.99k实际并联这个514/514审计本身看不出来的问题。
