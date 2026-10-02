# CIRCUIT-PRO-R21-PCB-SYNC-ACCEPT-ROUTING-CLOSURE-20261002-12

我已按固定 commit `42421a3a0bb9faf7490c0003aa33ff6a85d1b3cf` 审查了实际 Import Changes、550针前/温/冷对照、最终审计和冷重开 DRC。

这次同步关**正式接受**。

现在证据已经把问题分得很清楚：

- **176 components / 550 pads / 514 assigned / 107 nets / 36 NC** 与冻结原理图一致；
- Import Changes 实际是 **697项属性同步**，没有器件增删、pin改网、net改名、footprint变更；
- 一次 Apply 后，温态与冷重开均为：
  - `NetlistError = 0`
  - `ConnectionError = 452`
- 这452条正文确实都是“**同网络对象尚未物理连接**”，即未完成铜连接，不再解释成netlist错绑。
- 原有93段局部走线、板框、已有POUR/规则和器件布局没有被同步动作破坏。

所以：

```text
SCHEMATIC↔PCB_SYNC = PASS
PIN/PAD/NET_MAPPING = PASS
NETLIST_ERROR = 0

ROUTING = INCOMPLETE
CONNECTION_ERROR = 452
PCB_NOT_MANUFACTURABLE_YET
```

**从现在开始不再做 Import Changes、netlist同步排障或EDA工具研究。主线就是把板布完。**

---

## 唯一下一包批准

### `SCIENCE_ADK5556_4X4_R21_PCB_ROUTING_CLOSURE_V1`

批准你申请的 **360 min**，旧小包额度关闭，不结转。

| 阶段 | 时间 |
|---|---:|
| P0 敏感模拟/采集网络 | 120 min |
| P1 其余数字与普通信号 | 120 min |
| P2 GND、电源、铺铜与地缝合 | 45 min |
| P3 DRC + 冷重开审计 | 45 min |
| P4 完整交付 | 30 min |

授权：

- session ≤ 3
- save ≤ 12
- capture/audit ≤ 4
- DRC ≤ 4
- review export ≤ 2

普通器件位置微调、走线、过孔、地缝合和铺铜在范围内**自主推进，不用小步骤回来问**。

---

# 一、冻结输入

以下内容不能变：

- 原理图电气基线；
- 176 components；
- 550 physical pads；
- 514 assigned；
- 107 nets；
- 36 NC；
- 当前100 × 90 mm矩形板框；
- 4层结构；
- 所有主要器件值；
- symbol/footprint identity；
- J2 4ROW+4COL接口定义；
- J3/J4独立sense；
- 已同步后的PCB netlist。

**不再 Import Changes。**

除非后续真的发现原理图与PCB错网，否则schematic完全只读。

---

# 二、布线顺序

## P0：先把真正敏感的模拟网络做好

不要先追求452→0。

先保证关键网络的物理质量。

### 四路 TIA

每路把这一组当成一个局部模拟单元：

- U2通道；
- `R_COL_SENSE_i`
- `R_TIA_ISO_i`
- `RF_i`
- `CF_i`
- `C_TIA_HFi`
- `R_ADCi / C_ADCi`

要求：

- `COL_SENSE_i`极短；
- 22 pF贴近对应OPA输出/反相节点；
- RF/CF反馈环面积尽量小；
- TIA输入附近不要穿SPI、ROW_SEL之类数字线；
- ADC takeoff不要绕远再回来。

允许为了这个目的微调周围器件位置。

---

### VCM / VEXC

保持：

- U3；
- 1 kΩ隔离；
- 4.99 kΩ反馈；
- 100 pF；
- 分压与参考

作为紧凑区域。

尤其：

`VCM_FB / VEXC_FB`

不要平行长距离贴着SPI/SCLK走。

---

### ROW driver

四组：

- U1
- 1 kΩ isolation
- 4.99 kΩ feedback
- 100 pF

反馈网络优先短。

ROW到J2可以相对普通，但运放局部回路不要绕远。

---

### ADS8684

重点处理：

- ADC_IN0–3
- REFIO
- REFCAP
- AVDD
- DVDD

`R_ADC + C_ADC`尽量靠ADC输入一侧。

REFIO/REFCAP的电容和地回路必须非常短，不要把它们当普通bulk cap随便放远。

---

# 三、普通数字网络后做

然后再完成：

- SPI
- MCU_ROW
- reset/enable
- UART
- SWD
- supervisor逻辑

这些不需要为了“漂亮”抢占模拟区域。

尤其：

**SCLK不要从TIA输入区或ADC参考区穿过去。**

---

# 四、4层板的地/电源原则保持简单

保持目前四层实验板方向：

- L1：器件 + 关键模拟/短线
- L2：**连续GND参考面**
- L3：电源和低速普通网络为主
- L4：剩余信号

不要把L2切成AGND/DGND两块。

这个板更需要连续回流面，而不是人工割地。

允许：

- GND polygon；
- 合理GND stitching vias；
- 局部回流补强。

但不要为了“地缝合数量”堆几十个无意义via。

---

# 五、电源网络

J1 → LM73100 → V5，以及LDO/3V3路径采用比普通逻辑线更稳妥的宽度。

这里不需要重新做电源理论分析，只要：

- 不出现细长瓶颈；
- bulk caps接地/供电路径短；
- LM73100输入输出电容靠近器件；
- 100 Ω bleed的铜连接足够直接。

如果现有设计规则没有明确power class，不要停下来研究规则系统；按现有可制造规则做工程上明显更宽的电源线即可。

---

# 六、不要再跑 autorouter

前面的自动布线已经超时过。

本包明确：

**不再重试全板 autoroute。**

可以使用编辑器已有的：

- shove；
- interactive route；
-局部自动拐角/优化；

但整体由人工/受控路由推进。

---

# 七、DRC真正需要达到什么

最终不是简单追求“数字变0”而是分类。

### 硬门必须为0

```text
Netlist Error = 0
Connection Error = 0
Short Circuit = 0
Clearance Error = 0
```

以及所有真正会造成错误铜连接、未连接、违规间距的项目。

### 可以留下但必须列明

例如：

- silk文字；
- 非关键文档层；
- 某些装配/标注类warning。

不能靠关闭规则、隐藏错误或删DRC项目来过关。

---

# 八、最终冷审必须重新确认网络没有被布线改坏

完整布线完成后，做一次冷重开。

至少重新核：

```text
176 parts
550 pads
514 assigned
107 nets
36 NC
```

与本包起点一致。

同时：

- 所有pad net assignments不变；
- component/footprint identity不变；
- `NetlistError = 0`；
- `ConnectionError = 0`。

如果布线导致网络身份变化，那不是“route完成”，而是FAIL。

---

# 九、这次允许的placement调整范围

为了避免又因为小事回来问：

以下都可自主处理：

- R/C在同一功能块内移动；
- 器件旋转；
- 模拟块内部压缩；
- ADC/MCU周边去耦微调；
- connector附近普通器件让路；
- 增加必要via；
- GND stitching；
- 走线层切换。

但这些需要STOP：

- 必须改变100×90板框才能布完；
- 必须增加层数；
- 必须更换footprint；
- 必须改变元件值；
- 必须改变net；
- 必须修改原理图；
- NetlistError重新出现且不是立即可解释的误操作；
- 发现真实短路需要改变电路拓扑。

---

# 十、不允许做的事情

本包明确为：

- 新SPICE = 0
- MIMO/descriptor = 0
- 原理图修改 = 0
- Import Changes再同步 = 0
- API/SDK/cache研究 = 0
- 全板autoroute = 0
- Gerber制造放行 = 0
- BOM采购 = 0
- PCB下单 = 0
- 实际bench = 0
- 上电 = 0

允许输出**审查用途**的铜层截图/2D review图，但不要把它叫生产Gerber。

---

# 十一、最终希望看到的结果

下一次正常交付最好直接是：

```text
PCB_ROUTING_COMPLETE

176 PARTS PASS
550 PADS PASS
514 ASSIGNED PASS
107 NETS PASS
36 NC PASS

NETLIST_ERROR = 0
CONNECTION_ERROR = 0
SHORT = 0
CLEARANCE = 0

L2_GND_CONTINUITY_REVIEW = PASS
CRITICAL_ANALOG_ROUTING_REVIEW = PASS
COLD_REOPEN = PASS

PCB_REVIEW_READY
MANUFACTURING_NOT_RELEASED
```

如果还有少量非电气DRC warning，逐项分类即可，不需要为了丝印之类反复折腾。

---

现在路线已经很干净了：

**原理图完成 → PCB同步完成 → 当前正式进入完整布线。**

这次直接把剩下452个真实未连接对象收敛掉，同时保证模拟关键路径质量；不要再回头碰netlist和工具。
