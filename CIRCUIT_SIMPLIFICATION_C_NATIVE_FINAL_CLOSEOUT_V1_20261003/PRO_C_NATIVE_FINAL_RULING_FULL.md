我已经把 `6d45a931...` 这一版的 `COMPLETE_C_POWER_RECEIPT.md`、实际 BOM、391-pin 映射、GATES、功耗边界和图纸检查重新核过。结论是：**这个103贴装件的C候选已经值得收口，不需要再改架构，也不需要重新碰 full-matrix/PZ 求解器。** 现在只剩几处很具体的工程修正。

我批准你申请的 **240 min 最小收口包**，但先把五项裁定冻结如下。

## 1. 电源架构接受，但 TPS7A37 必须补一颗外部反灌保护二极管

现在这条逻辑本身可以保留：

`U11(V5 supervisor) → PWR5_OK → TPS7A3701 EN`

以及：

`U12(V3V3 supervisor) → PGOOD → MCU NRST`

再通过现有 BAT54XY 支路实现：

`PWR5_OK low → PGOOD low`

这个上电顺序其实很合理：V5先合格，才启用3.3 V；3.3 V再合格，才释放MCU。

真正没有闭合的是**突然拔掉5 V时 TPS7A3701 的反向电流条件**。TPS7A37官方明确要求，为保证内部反向阻断，应在移除VIN之前先把EN拉低；而当前U11的传播延迟没有一个足够强的最坏值证明“任何拔电速度下EN一定先低”。:chatgpt-content-reference{index="0"}

所以不再试图用时序把这个问题证明掉。直接增加一颗：

**`D_LDO_REV = PMEG2010BER`**

连接方式：

**Anode → V3V3，Cathode → V5。**

TI官方明确推荐 LDO 的 `OUT→IN` Schottky 作为反向电流保护方法，它会优先旁路内部反向路径，而且正常5 V/3.3 V工作时处于反偏。:chatgpt-content-reference{index="1"} 我选择 PMEG2010BER 而不是小信号BAT54，是因为它是20 V / 1 A器件，1 A时最大VF约450 mV，能更从容地承受44 µF级3.3 V储能的掉电瞬态。:chatgpt-content-reference{index="2"}

这样之后：

> **TPS7A37反向安全不再依赖“U11一定来得及先关EN”。**

U11→EN仍保留，用于正常brownout/关断排序；但是它从“器件生存的唯一保证”降为正常时序控制。

这也意味着 `U9_BLEED` 和 `U10_BLEED` 都继续保留。新二极管可能在掉电瞬间把V3V3储能送入本地V5轨，但U9反向阻断隔离J1，V5的100 Ω bleed和板内负载负责消耗这部分能量。

原来的 board-OFF/debug-ON ≤0.39 V解析结果不能直接拿来冒充新拓扑结果；但新增的是额外泄放路径，从物理上不会形成新的升压源。下一包重新算一次即可。

---

## 2. 12个“两脚全NC”的DNP补偿件：全部从正式C原理图删除

这里我不接受继续把它们称为“可恢复补偿位”。

现在：

`R_COL_SENSE0..3`  
`R_TIA_ISO0..3`  
`C_TIA_HF0..3`

两端实际都是NC，因此它们只是12个画在原理图上的空壳，并不能通过后焊实现旧补偿网络。

**正式C版直接删除这12个designator。**

但保留唯一明确的恢复合同。如果后续直接TIA在真实板上出现稳定性问题，恢复方案只能是重新做一个有界ECO，恢复原来的完整拓扑：

```text
OPA4388 OUT = TIA_DRVx
      │
      ├── C_TIA_HF 22pF ───── COL_SENSEx
      │
   R_TIA_ISO 1k
      │
     TIAx
      │
 RF 4.99k || CF 2.2nF
      │
     COLx
      │
 R_COL_SENSE 10k
      │
 COL_SENSEx → OPA4388 IN-
```

也就是说：

> **direct-TIA 是C版正式候选；旧remote-sense补偿是明确的后备拓扑，而不是12个假的DNP占位。**

已有约79.6°局部相位裕度和阶跃结果，只足以支持“direct-TIA值得作为候选继续”，不等于证明它在完整16R矩阵中已经通过性能验证。

因此 `FULL_MATRIX_DYNAMIC_PERFORMANCE_HOLD` 保留，但**不再阻止原理图收口**。

---

## 3. U12改成真正单颗精密电阻；VEX 18k/162k接受

### U12

当前用：

`10k + 4.99k + 1k + 1k = 16.99k`

没有继续保留四颗的必要。

采用真实存在的：

**`RT0603BRD0716K9L` = 16.9 kΩ / 0.1% / 25 ppm/°C / 0603**

这个料号当前确实存在且在售。:chatgpt-content-reference{index="3"}

配合10.0 kΩ bottom，TPS3890标称阈值变为约：

\[
V_{\mathrm{TH}}
=1.15\left(1+\frac{16.9}{10}\right)
\approx3.094\;V
\]

相比现有3.104 V只下移约10 mV，对STM32G031 1.7–3.6 V工作范围仍非常保守。STM32本身也具有POR/PDR及可编程BOR。:chatgpt-content-reference{index="4"}

所以：

> **U12_TOP0..3 四颗 → 一颗16.9k。**

直接再减少3个贴装件。

### VEX

18k/162k继续接受。

它仍然严格保持：

\[
V_{EXC}=0.9V_{CM}=2.25V
\]

只是Thevenin等效从9 kΩ变成16.2 kΩ。

搭配100 nF：

\[
\tau = 1.62\,ms
\]

一阶网络达到1%约需7.5 ms左右。

这不是扫描期间的问题，因为VEX不是每一行重新建立；因此冻结一个简单合同即可：

> **V5/VCM建立后至少10 ms才允许进入第一次MEASURE。**

无需为了恢复9 kΩ再改回10k/90k。

---

## 4. TPD4E05U06电气部分可以解除HOLD；FFC机械继续HOLD

当前两个器件使用的是：

**`TPD4E05U06DQAR`**

其实际pin mapping我与TI最新版数据表逐脚核对：

- 1、2、4、5 = 四路I/O；
- 3、8 = GND；
- 6、7、9、10 = NC；
- DQA = 10-pin USON，2.5 × 1.0 mm。

这和当前实际原理图完全一致。TI官方器件也是4通道、5.5 V standoff、0.5 pF典型输入电容、±12 kV IEC contact。:chatgpt-content-reference{index="5"}

因此下一版只需要把元数据补正规：

**Manufacturer = Texas Instruments**  
**MPN = TPD4E05U06DQAR**

不再因为库模板 maker 字段为空把它保留为电气material HOLD。

但它的合同必须写清：

> **它是J2被动电阻阵列接口的ESD保护，不是持续DC过压/反灌保护。**

这和当前J2“只接被动4×4电阻阵列”的合同一致。

另一方面，J2虽然名称已经是 `2005290081`，当前原理图对象仍继承了旧 footprint metadata。因此：

**FFC/FPC实际pitch、top/bottom contact、actuator方向、板边mating corridor继续保持机械HOLD。**

这不阻塞原理图电气接受，但阻塞最终PCB机械放行。

---

## 5. ADS8684所有双22 µF先全部保留

这一条直接接受当前实现。

此次不删除：

- `C_ADC_REFIO + C_REFIO_B`
- `C_REFCAP_BULKA/B`
- `C_AVDD9A/B`
- `C_AVDD30A/B`
- `C_DVDD34A/B`

以及相应2.2 µF/100 nF近端去耦。

Murata自己明确提醒X7R类MLCC的实际电容随DC bias变化，并要求用准确型号在SimSurfing等工具中检查。:chatgpt-content-reference{index="6"}

因此没有准确Ceff数据前：

> **双22 µF保留是正确的工程选择。**

`MLCC_CEFF_HOLD`继续存在，但它现在是**元器件有效容量/最终硬件资格HOLD**，不是继续阻止C原理图收口的理由。

TPS7A37对这一点也没有新的冲突，因为官方明确说明其稳定于 **≥1 µF ceramic output capacitance**，架构对输出电容值/ESR相对不敏感。:chatgpt-content-reference{index="7"}

---

# 这次修改后，C版应从103件变成101件

不是为了凑数，这是自然结果：

| 类别 | 当前实际 | 收口目标 |
|---|---:|---:|
| R | 39 | **36** |
| C | 44 | **44** |
| Protection | 6 | **7** |
| IC | 10 | **10** |
| J | 4 | **4** |
| DNP占位 | 12 | **0** |
| **实际贴装/结构总数** | **103 + 12 DNP** | **101** |

变化来源很简单：

U12四颗上臂 → 一颗：**−3**  
增加LDO OUT→IN Schottky：**+1**  
12颗假DNP从结构中删除：**−12 structural only**

所以最终应该是一张**约101件、没有假DNP占位**的真正C原理图。

这比上一版“115 structural”干净得多，而且没有拿ADC电容和接口安全功能换数字。

---

# full-matrix / PZ 的最终处理

这两个不在下一包重跑。

`full16R OP aborted` 保持：

**`NUMERICAL_UNRESOLVED`**

它继续阻止：

**≤1% mean error PASS、≤0.2% SD PASS、100 fps system PASS。**

但不再阻止原理图电气架构的接受。

旧PZ：

**`PZ_INVALID_PORT_SETUP / NO_RESULT`**

继续归档，`poles.txt`永久不作为证据。

已有AC/TRAN只支持：

> single-row remote-feedback 和 direct-TIA 是有合理局部动态行为的**candidate architecture**。

不能升级为完整阵列动态证书。

后续真正判断这些性能，最终还是要依靠有效整机模型或实际bench；没必要现在为了让一个PZ文件变绿去研究求解器。

---

# 240 min 收口包：批准

包名建议冻结：

**`CIRCUIT-SIMPLIFICATION-C-NATIVE-FINAL-CLOSEOUT-V1`**

总额 **240 min**，按你申请的框架执行。

唯一允许的一组原理图修改就是：

> 加 `D_LDO_REV=PMEG2010BER`；U12四上臂改成单颗16.9k；删除12个NC DNP；补正两个TPD的TI MPN/manufacturer；VEX 18k/162k保持；所有ADC bulk保持；其余C架构不再改。

工程额度保持：

**source≤2、power candidate≤1、copy1、session≤2、save≤4、capture≤3、audit≤3、ERC≤1、PDF≤1、OP/AC/PZ≤8、TRAN≤2且单次≤180 s。**

240 min 分配维持：

`45 min 电源/料值 + 45 min DNP/material + 90 min native warm/cold + 60 min交付`

其中这次真正重要的是 **第二个session必须用于cold reopen**。不再把两个session都花在同一次建图过程上。

OP/TRAN不是必做指标；只有新增反灌二极管或电源节点确实需要核一个静态/简单掉电边界时才运行。**不允许借这8+2次数重新尝试full-matrix或PZ。**

本包结束时唯一的关闭门是：

> `101 populated/structural target` 与实际BOM一致；391-pin变化后的全部pin/net重新闭合；cold reopen一致；ERC没有新的Critical/Important；六页图纸能够独立识别主要功能和net；TPD材料身份已修正。

若这些满足，可以将状态推进为：

**`C_SCHEMATIC_ACCEPTED = true`**  
**`PCB_PLACEMENT_ELIGIBLE = true`**

但仍保持：

**`SYSTEM_PERFORMANCE_ACCEPTED = false`**  
**`PCB_ROUTING_RELEASED = false`**  
**`BENCH_RELEASED = false`**  
**`MANUFACTURE_RELEASED = false`**

所以这240分钟不是再做一轮研究，而是**把现在已经基本成形的C版原理图真正关掉**。下一步再开始做你真正关心的、基于这101件版本的规整PCB布局。
