# CIRCUIT-PRO-R21-PIN-NET-CORRECTION-AND-FINAL-DRAWING-20261002-09

**项目：`SCIENCE_ADK5556_4X4_DAQ_REPLICA`**

我已按固定 commit `47c3a102c8034be67eb7da99a8d5d002747f4324` 审查本次08号工程阻断包，包括完整回执、基线与ECO后网表审计、器件碰撞诊断、PDF逐页审查、预算和台架计划。

## 统一裁定

**接受本次 `ACTUAL_PIN_NET_ERROR` STOP。**

这次阻断点非常具体，就是**原理图实施错误**，不是架构错误、稳定性理论问题，也不是需要重新仿真的科学问题：

- 冻结R2的新工作副本在修改前已经真实通过：**498/498连接、104 nets、36 NC**。
- ECO后变成 **334/514匹配、99 actual nets / 106 expected nets、36 NC**。
- 四个新 `C_TIA_HF0..3` 明确与四个已有器件坐标重合，引起GND、V5、TIA/COL_SENSE等网络大范围合并；这足以解释为什么看起来“180针都错了”，并不是180个独立设计错误。
- `U3.2/U3.6` 没有真正从 `VCM/VEXC` 迁到 `VCM_FB/VEXC_FB`。
- 六页PDF的超大网名是明确的字号实施错误。

这些都属于**局部可修原生问题**。不再返回MIMO、descriptor、ngspice或补偿参数研究。

---

# 一、唯一下一包批准

## `SCIENCE_ADK5556_4X4_R21_NATIVE_PIN_NET_CORRECTION_AND_FINAL_DRAWING_V1`

目标只有一个：

> **把已经确定的R2.1 ECO正确地落到嘉立创原生工程，取得真实全量pin-net、冷重开和可读图纸。**

本包**不做新的电路设计，不做新的仿真。**

---

# 二、从哪里开始修：不要在污染后的网表上硬补

这里我做一个小调整。

**不要直接把当前 `BLOCKED_NOT_FOR_USE` 工程当作最终修复基底一路补到底。**

最安全的路线是：

1. 以已经证明 **498/498、104 nets、36 NC PASS** 的那份R2基线副本为源；
2. 新建本包唯一一个工作副本；
3. 重新只实施已经批准的最小ECO；
4. 每一组局部ECO后立即做实际File检查。

理由很简单：当前失败工程已经发生了广泛net merge。即使把四个电容拖开，旧接触形成的导线、端口或合网状态是否全部自动恢复，不值得赌。

**失败工程继续冻结作证据，不覆盖、不修成最终版。**

这不是重建168个器件，而是从已验证R2副本重新做8个新增无源件和少数属性/端口ECO。

---

# 三、ECO内容完全冻结，不允许再扩

### Page 1 / Power-Reference

只做：

- `R_VCM_FB = 4.99 kΩ`
- `C_VCM_HF = 100 pF`
- `R_VEX_FB = 4.99 kΩ`
- `C_VEX_HF = 100 pF`
- **只重建 U3.2 和 U3.6 两个实际反馈端口**
  - U3.2 → `VCM_FB`
  - U3.6 → `VEXC_FB`

旧 `VCM/VEXC` 端口对象在这两个锚点先删除，再用已经正常工作的官方 NetPort 创建方式重建。

**禁止研究setter/API为什么失效。**实际File正确就是验收标准。

### Page 3 / TIA

新增：

- `C_TIA_HF0..3 = 22 pF C0G`

连接固定为：

\[
TIA\_DRV_i \leftrightarrow COL\_SENSE_i
\]

四个电容及自己的短线/端口放到**事先确认完全空白的四个独立位置**。

要求：

> 放置前必须做坐标占位检查，附近不得存在旧器件pin、wire endpoint、NetPort或junction。

不要再使用原来的 y=1320 四个坐标。

### RESET

`R_J3_5`：

- 4.99 kΩ → **1.00 kΩ**
- 真实型号 `0603WAF1001T5E`
- 保持direct NRST拓扑。

### Metadata

只修：

`C_ADC0..3 Value = 10nF X7R`

以及这次ECO直接涉及的元件字段明显错误。

**不做全库供应链清洗。**

### Drawing

删除显式 `fontSize=8` 方案，恢复**原生/default文字尺寸**。

随后只做必要的位置调整：

- net label不压器件；
- 不压pin number/value；
- 不碰图框；
- 长说明允许分行或移到空白区。

不开发自动排版算法。

---

# 四、这次必须采用“分段实际网表审计”，防止又一次全页污染

授权内部自主进行，不需再问。

## Audit A — 基线

打开新副本后首先重新确认：

**168 parts / 498 connected pins / 104 nets / 36 NC**

若基线不一致：

**立即STOP。**

## Audit B — Page 1反馈ECO后

只做VCM/VEXC四个新器件与两个反馈端口后，立即抓实际File。

必须确认：

- U3.2=`VCM_FB`
- U3.6=`VEXC_FB`
- 新R/C的两端网络准确；
- 原本GND/V5/REF/DIV等网络成员未发生异常变化；
- 网络数量增量与计划一致。

不通过就只修Page 1，不继续TIA页。

## Audit C — TIA四电容后

新增四个22pF后再次实际File审计。

逐个要求：

- `C_TIA_HF0`: `TIA_DRV0 ↔ COL_SENSE0`
- …
- `C_TIA_HF3`: `TIA_DRV3 ↔ COL_SENSE3`

并特别检查：

**GND、V5、COL_SENSE0..3、TIA_DRV0..3不能因坐标接触出现意外成员。**

## Audit D — 最终

最终目标固定：

\[
\boxed{514/514\ \text{connected pins}}
\]

\[
\boxed{106\ \text{nets}}
\]

\[
\boxed{36\ \text{NC}}
\]

\[
\boxed{176\ \text{parts}}
\]

这里的数字来自现有冻结计划。若实际设计变更为0，则必须完全相等；**不能用“功能相近”代替。**

---

# 五、冷重开是硬门

最终保存后：

1. 正常关闭自有session；
2. 独立冷重开；
3. 再次实际File capture；
4. 比较：
   - 514个连接pin的net；
   - 36 NC；
   - 106个net成员集合；
   - 176器件ref/device/value/footprint核心字段。

要求：

**冷重开前后网络成员集合一致。**

字节级netlist完全相同不是要求。

如果只是字段顺序变化，可接受；如果网络成员变化，STOP。

---

# 六、图面验收这次简单处理

最终PDF两版预算够用。

### PDF 1

先恢复default字号并完成基本布局，导出后**六页全部实际看一遍**。

记录：

- overlaps；
- frame collision；
- unreadable long text；
- pin/value遮挡。

若有问题，只允许一次局部整理。

### PDF 2

最终版。

验收：

- 六页均可读；
- 不出现上次那种巨型net文字；
- 主反馈链能视觉追踪；
- 器件ref/value不大面积重叠；
- 端口和连线关系能人工理解。

目标是**工程可读**，不是论文排版。

---

# 七、ERC/DRC的处理

本包允许一次。

如果能够取得具体正文：

分类处理真正的：

- 未连接输入；
- 电源问题；
- 重名/冲突；
- 意外悬空。

如果工具仍只返回count，没有正文：

记录：

`ERC_DETAIL_HOLD`

然后结束。

**不允许再次为了ERC接口去开发工具，更不允许重建工程。**

---

# 八、不再运行任何仿真

你申请的这一点我批准。

本包：

- OP/AC = **0**
- TRAN = **0**
- PZ = **0**
- MIMO = **0**
- descriptor = **0**
- reset解析 = **0**
- protocol新回归 = **0**

08包的40组理想DC、32项协议以及宏模型数值限制直接作为背景证据继承。

这次的任务纯粹是：

**原生连接修正 + 原生审计 + 图面完成。**

---

# 九、台架部分只整理输入，不执行

允许30 min整理 `BENCH_VALIDATION_PLAN.md` 为下一阶段可直接执行的版本。

主要保持你们已有顺序：

1. 限流空载上电；
2. 1 k / 3.3 k / 7 k标准阵列；
3. 1 k / 6.8 k两点校准；
4. 单点约10%变化；
5. 一行约10%变化；
6. 示波器测ROW/TIA/ADC 300 µs建立；
7. 实测100 fps与SPI/DMA；
8. 最后才考虑真实传感阵列。

**不执行实际bench。**

也不把故障短路60 s放进首次上电计划。

---

# 十、预算批准

申请的 **240 min** 批准，从零重新计数；08号剩余额度不结转。

| 阶段 | 时间 |
|---|---:|
| P0 原生连接修正 | **60 min** |
| P1 全量审计、冷重开、图面/ERC | **90 min** |
| P2 台架输入整理 | **30 min** |
| P3 完整交付 | **60 min** |

原生额度：

- workcopy：1
- session：≤2
- save：≤6
- actual File capture/audit：≤4
- ERC/DRC：≤1
- PDF：≤2

新增：

- library identity：0
- sources：0
- candidate：0

普通位置、文字、线长、label、Value/metadata调整可在上述范围内自主推进。

---

# 十一、真正STOP条件只有这些

本包只有以下情况回来找我：

1. **新R2基线副本本身不再是498/498、104 nets、36 NC；**
2. U3.2/U3.6用删除+重建NetPort仍不能进入VCM_FB/VEXC_FB；
3. 四个TIA 22pF在干净位置仍导致实际net merge；
4. 最终无法达到514/514、106 nets、36 NC；
5. 冷重开网络成员变化；
6. 发现计划pin-net本身互相矛盾；
7. 必须改变已经冻结的电路拓扑或元件值；
8. 240 min或硬额度耗尽。

**字体、标签位置、普通导线长度、元数据小修不属于STOP。**

---

# 十二、当前技术结论

这一轮别再扩大问题。

目前没有新证据说明电路架构错了。08包真正失败的地方非常朴素：

> **四个电容放到了别的器件身上，两根反馈port没真正换网名，字体设坏了。**

就是把这三件事修正确。

理想下一次回来应该是：

```text
R21_NATIVE_REVIEW_SCHEMATIC_COMPLETE
514/514 PIN_NET_PASS
106_NETS_PASS
36_NC_PASS
COLD_REOPEN_PASS
DRAWING_READABLE_PASS
BENCH_VALIDATION_PENDING
```

然后我们下一阶段才考虑**受控上电验证**，而不是再回到稳定性数学证明。

**按这个09号唯一工程包继续执行。**
