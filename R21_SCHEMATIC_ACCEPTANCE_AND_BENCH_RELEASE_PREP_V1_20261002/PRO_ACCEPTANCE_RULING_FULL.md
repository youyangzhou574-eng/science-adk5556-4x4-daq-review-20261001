# CIRCUIT-PRO-R21-SCHEMATIC-ACCEPT-AND-BENCH-READINESS-20261002-11

我按固定 commit `fbb7c0ed5f322f078583fadbdb353efe835e4c01` 重新看了完整回执、最终冷重开审计、接口拆分检查、GATES、图面审查和接口 companion。

这次可以给一个比较明确的工程结论：

> **R2.1 原理图的电气连接现在可以接受为工程基线。**
>
> 不再因为旧备注、PDF少显示4个网名、ERC只有count，继续修改电路或阻塞主线。

## 当前正式状态

| 项目 | 裁定 |
|---|---|
| 主采集拓扑 | **PASS** |
| J3/J4 3.3 V sense拆分 | **PASS** |
| 嘉立创实际pin-net | **514/514 PASS** |
| 网络数 | **107 PASS** |
| NC | **36 PASS** |
| 器件 | **176 PASS** |
| 独立冷重开 | **PASS** |
| 冷热网络成员一致 | **PASS** |
| 原理图电气基线 | **ACCEPTED** |
| PDF主体可读 | **PASS with companion** |
| PDF独立成套发布 | HOLD |
| 实物性能 | 尚未验证 |
| Bench上电 | **NOT RELEASED** |
| PCB layout | **NOT STARTED** |

这次接口修改也很干净：从09版到现在实际上只变了4个pin的外侧网名，`J3.1/R_J3_1.1 → V3V3_EXT_SWD`，`J4.1/R_J4_1.1 → V3V3_EXT_UART`；剩余510个连接pin、36个NC和176个器件核心字段都没变。两个4.99 kΩ现在真正各自独立，不再形成2.495 kΩ并联路径。冷重开以后网络成员完全保持。

---

## 图上的4个网名不显示：不再修

我这次明确裁定：

**不需要为了 Page 5 四个 sense 网名没有打印出来，再打开嘉立创原生工程。**

原因很简单：

- actual netlist是正确的；
- 冷重开是正确的；
- `INTERFACE_TOPOLOGY_COMPANION.md` 已明确给出真实连接；
- `DRAWING_ANNOTATION_ADDENDUM.md` 已把NRST 1 kΩ、旧300 µs说明、八状态等历史备注纠正清楚。

所以：

`LEGACY_ANNOTATION_HOLD`  
`INTERFACE_NET_LABEL_DRAWING_HOLD`

从现在开始只属于**文档质量HOLD**，不是电路设计HOLD。

现有原生工程和PDF直接冻结，不再冒险为了几个文字把正确netlist改坏。

等以后真要出PCB/制造归档时，再单独做一版“生产文档清洁版”即可。

---

## 现在真正剩下的是实物验证，而不是继续设计电路

当前应该保留的风险都属于bench阶段：

- `REFERENCE_CAPACITANCE_BENCH_HOLD`：实际MLCC偏压、启动；
- `HARDWARE_WCET_PENDING`：100 fps、SPI/DMA/ISR真实时序；
- `SWD_SERIES_RESISTOR_BENCH_CHECK`：4.99 kΩ SWD串阻从低速开始验证；
- 300 µs实体建立时间；
- 1–7 kΩ实际精度；
- 约10%阻值变化可辨识；
- 帧间SD≤0.2%；
- reset在20–30°C实际动作；
- `FAULT_PROTECTION_HOLD`：异常短路、反灌、热行为。

这些都**不应该再回头改原理图，除非实测真的发现问题。**

---

# 唯一下一包

## `SCIENCE_ADK5556_4X4_R21_SCHEMATIC_ACCEPTANCE_AND_BENCH_RELEASE_PREP_V1`

这个包彻底退出EDA修改阶段。

目标是：

> **冻结已通过的R2.1原理图，整理成真正可以拿到实验台上执行的测试合同。**

不允许修改任何电气连接、阻容值或器件。

### 需要交付

首先冻结一个“Accepted Schematic Baseline”，至少记录：

`commit fbb7c0ed...`  
`epro2 SHA`  
`514 pins / 107 nets / 36 NC / 176 parts`  
以及 companion/addendum 是该审查版图纸的强制配套文件。

然后把已有 `BENCH_VALIDATION_PLAN.md` 收敛成真正可执行的台架输入，给出以下几个文件即可：

- `FIRST_POWERUP_PRECHECK.md`：上电前逐项检查；
- `BENCH_TEST_MATRIX.csv`：1 k / 3.3 k / 7 k、棋盘、约10%变化等全部工况；
- `EXPECTED_NODE_RANGES.csv`：V5、3V3、VCM、VEXC、ROW、TIA、ADC正常预期范围；
- `BENCH_STOP_CRITERIA.md`：什么时候必须马上断电；
- `CALIBRATION_AND_ACCEPTANCE.md`：1 k / 6.8 k两点校准、≤1%、≤0.2%等验收口径；
- `TIMING_CAPTURE_PLAN.md`：300 µs、SPI/DMA、100 fps该怎么抓波形。

其中第一次真正上电仍然不在这个包里。

---

## 台架首轮应该怎么分阶段

后续真放行bench时也不要一股脑全做。

第一阶段应该只是：

**限流电源 + 空载板**

看：

V5、V3V3、VCM≈2.5 V、VEXC≈2.25 V、PGOOD、NRST、ADC参考、电源电流是否合理。

这些正常以后才接：

**1 k / 3.3 k / 7 k标准电阻阵列。**

然后再做：

校准 → 10%变化 → 300 µs波形 → 100 fps。

**短路、±故障、60 s热测试不允许混入首次上电。**

---

# 新预算

批准你们申请的 **240 min** 新包预算，旧10号余额关闭，不结转。

| 阶段 | 时间 |
|---|---:|
| 最终原理图基线冻结与接收矩阵 | 45 min |
| Bench合同/标准阵列/预期值/停止条件 | 75 min |
| 首次上电release checklist准备 | 60 min |
| 完整固定commit交付 | 60 min |

本包明确：

**EDA原生编辑 = 0**  
**copy/session/save/capture/PDF = 0**  
**仿真 = 0**  
**MIMO/descriptor = 0**  
**新协议代码 = 0**  
**PCB = 0**  
**采购 = 0**  
**制造 = 0**  
**实际bench = 0**

只读使用现有证据和现有厂家资料即可。

---

## 下一次真正需要我裁定什么

这个准备包回来后，我只需要决定一件事情：

> **是否正式放行“受控首次上电 Bench Phase 1”。**

到那时候才给：

- 电源限流值；
- 仪器连接；
- 哪些节点先量；
- 正常阈值；
- 异常立即停机阈值；
- 一次允许做哪些实验。

而不是再改原理图。

---

### 当前项目一句话状态

**原理图电气设计现在已经可以冻结。**

目前不是“原理图还有没有画错”的阶段了，而是：

**R2.1 schematic accepted → bench准备中 → PCB尚未开始。**

这次后面不要再因为几个文字、ERC count或者理论问题把路线绕回去。
