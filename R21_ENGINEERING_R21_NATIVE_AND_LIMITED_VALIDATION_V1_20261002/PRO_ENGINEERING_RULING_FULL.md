# CIRCUIT-PRO-R21-ENGINEERING-CONVERGENCE-AND-NATIVE-R21-20261002-08

**项目：`SCIENCE_ADK5556_4X4_DAQ_REPLICA`**

我已按固定 commit `a84792c61cff00990cab0a9b2a72de4a86586d7b` 阅读本次 descriptor 阻断回执。现在正式把路线收回来：

> **07号 descriptor 包到此结案，作为历史分析证据保存；`DESCRIPTOR_EXTRACTION_NOT_QUALIFIED` 不再是 R2.1 原理图的工程硬门。后续禁止继续开发 MIMO / descriptor / reference-normalization 方法来阻塞原理图。**

本次 REF2 所谓 21.7% 差异发生在约 \(4\times10^{-8}\) 的内部小响应上，绝对差约 \(9\times10^{-9}\)，它**不是VCM实际输出误差，更不是电路物理失稳证据**。ROW、loaded TIA以及processed follower的普通AC对照已经做到约0.1%甚至更好。这里继续修 descriptor 已经偏离“把4×4电阻阵列采集板做出来”的主目标。

---

## 一、工程目标现在统一

用户真实需求是：

**传感单元约 1–7 kΩ，变化量约10%。**

此前 `0.8–8 kΩ` 不删除，而是重新定义成**设计保护带/guard band**：

| 范围 | 工程含义 |
|---|---|
| **1–7 kΩ** | 正常工作和精度验收范围 |
| **约10%阻值变化** | 必须能够稳定辨识的实际信号变化 |
| **0.8–8 kΩ** | 设计保护带，用于检查输出余量、饱和、电流和异常边缘；不要求保护带每一点都取得最终1%实测精度声明 |

正常工作目标继续保持：

- 4×4、8线；
- E = 0.25 V；
- VCM = 2.5 V；
- VEXC = 2.25 V；
- Rf = 4.99 kΩ；
- Cf = 2.2 nF；
- ADC 0–5.12 V；
- 100完整帧/s；
- 正常1–7 kΩ范围最终校准后平均误差目标≤1%；
- 帧间重复性目标≤0.2%。

这次不再因为“理论还能证明得更完整”而扩大任务。

---

# 二、R2.1电路现在冻结成工程候选

直接进入原理图的成熟ECO如下：

| 模块 | R2.1冻结候选 |
|---|---|
| ROW驱动 | OPA4388，输出1 kΩ；远端反馈4.99 kΩ；输出→反相端 **100 pF** |
| VCM/VEXC | OPA2388，输出1 kΩ隔离；4.99 kΩ远端反馈；**100 pF** HF反馈 |
| TIA | OPA4388；COL→反相端10 kΩ；Rf=4.99 kΩ、Cf=2.2 nF；运放输出→TIA tap 1 kΩ；输出→反相端 **22 pF** |
| ADC输入 | 100 Ω + 10 nF |
| RESET | J3.5外部NRST通过 **1.00 kΩ** 直接进入PGOOD/MCU_NRST；10 kΩ上拉和现有钳位保留 |
| RESET接口定义 | active-low open-drain/open-collector，释放Hi-Z，正常拉低要求VOL≤0.4 V |
| 采集 | 八状态：BLANK0→ROW0→BLANK1→ROW1→BLANK2→ROW2→BLANK3→ROW3 |
| 数据资格 | 保留现有progress watchdog、epoch、防重放、连续两完整帧恢复合同 |
| 参考/ADC去耦 | 保留R2已经补齐的独立REFIO/REFCAP和AVDD/DVDD bulk+HF结构 |
| 电源保护 | 保留R2已有反向阻断、supervisor、PGOOD、硬件使能与限流/钳位结构 |

**不再扫第三轮补偿参数。**

除非有限工程验证出现明确正常工作失败，否则这些数值不再变化。

---

# 三、哪些旧HOLD退出工程主线

以下内容继续保留在历史记录中，但**不再阻止R2.1审查原理图**：

`DESCRIPTOR_EXTRACTION_NOT_QUALIFIED`  
`REFERENCE_REALIZATION_AND_INTERNAL_CERTIFICATE_HOLD`  
`EXACT_LOW_FREQUENCY_POINTS_FULL_NETWORK_HOLD`  
`COUPLED_MODEL_CONVERGENCE_HOLD`  
历史的 `RESET_THRESHOLD_ENVELOPE_HOLD`

以后只有普通工程仿真或实测真的发现振荡，才重新打开稳定性深挖。

现有32项协议/进度看门狗逻辑已经有可接受的离线证据，因此：

`FAULT_LATENCY_LOGIC_CONTRACT_PASS`

继续成立。

硬件端仍标：

`HARDWARE_WCET_AND_LATENCY_BENCH_PENDING`

---

# 四、现在只做有限工程验证

## A. DC / 工作点

不再大规模扫参。

至少覆盖正常及保护带这些典型模式：

| 模式 | 用途 |
|---|---|
| all 0.8 kΩ | 最大电流/输出高端保护带 |
| all 1 kΩ | 正常低阻端 |
| all 3.3 kΩ | 中间工作点 |
| all 7 kΩ | 正常高阻端 |
| all 8 kΩ | 输出低端保护带 |
| checker 1 kΩ / 7 kΩ | 邻居差异 |
| target 7 kΩ + neighbors 1 kΩ | 高阻目标、低阻邻居 |
| target 1 kΩ + neighbors 7 kΩ | 低阻目标、高阻邻居 |
| 单点 +10% | 实际变化响应 |
| 一行/多点约10%变化 | 阵列变化场景 |

只需要回答几个工程问题：

**有没有饱和、有没有越ADC范围、行驱动电流是否合理、输出余量是否足够、10%变化是否产生足够ADC码差。**

现有固定校准、线阻和INL有限域结果可直接引用，不需要因为R2.1只改高频无源件而从零重复全部数学工作。

---

## B. 短暂态

最多跑 **12个正常暂态**。

优先6个：

`4ROW + 1TIA` × 800 Ω / 8000 Ω / high-target  
`1ROW + 4TIA` × 800 Ω / 8000 Ω / high-target

统一：

\[
t_{\rm switch}\approx3\ \mu s
\]

仿真只需要到切换后约：

\[
330\sim350\ \mu s
\]

不再跑9.6 ms整帧。

检查：

\[
t_{\rm switch}+300\mu s
\]

附近以及随后有效采样窗口：

- ADC输入残余目标≤100 µV；
- 没有持续增长振荡；
- 没有正常工作削顶；
- 稳态基准用本case自身后段结果。

### 很重要的规则

如果一个大宏模型case **只是数值很慢/不收敛**：

记录：

`MACROMODEL_NUMERICAL_LIMIT`

然后继续工程任务。

**不再因此启动新的稳定性数学研究，也不再阻止R2.1原理图。**

只有观察到真实的：

- 电压持续增长；
- 长时间不衰减振铃；
- 正常输出削顶；
- 300 µs明显达不到要求；

才算电路设计问题。

---

# 五、100 fps不重新设计

八状态候选仍为：

每状态约1.2 ms，

\[
8\times1.2=9.6\ {\rm ms}
\]

留约：

\[
0.4\ {\rm ms}
\]

给软件整理。

继续保留progress watchdog。

本包只要求：

- 状态时间表自洽；
- 288次传输/32 dummy/256有效样本自洽；
- 相邻blank差分正确；
- 原32项合同在最终修改后完整回归一次。

**不写新的第二套状态机。**

真实100 fps、SPI WCET、DMA调度以后由台架验证。

---

# 六、RESET也不再理论扩张

1 kΩ direct-reset方案直接进R2.1审查图。

25°C解析结果此前已经有合理低电平裕量。

BAT54S在20–30°C的保证数据不完整，不再为了这几度温差重新设计整条复位路径。

状态写成：

`RESET_DIRECT_PATH_DESIGN_ACCEPTED / 20–30C_BENCH_CONFIRMATION_PENDING`

±5 V、掉电强注入、60 s热等仍属于：

`FAULT_PROTECTION_HOLD`

它们不阻止**审查版R2.1原理图**，但继续阻止故障试验及最终制造放行。

---

# 七、现在允许直接做R2.1原生工程

这一点与之前最大的区别是：

> **不再要求先把所有动态理论门全部关闭以后才允许画R2.1。**

完成基础工作点检查后，没有发现明确正常工作错误，就直接从冻结R2开工作副本做R2.1 ECO。

只做这些改动：

1. ROW加入/确认100 pF；
2. VCM/VEXC加入/确认100 pF；
3. TIA加入/确认22 pF；
4. NRST串阻改1.00 kΩ direct方案；
5. 确认八状态和progress watchdog设计备注；
6. 修四个 `C_ADC` Value元数据；
7. 修明显文字、端口、箭头和跨页可读性；
8. 不改主架构、E、Rf、ADC、OPA和100 fps；
9. 不因旧MIMO/descriptor文件去改电路。

---

# 八、原生验收

R2.1完成后必须做：

| 项目 | 要求 |
|---|---|
| 计划pin-net vs 实际 | 一致 |
| 实际连接引脚 | 全量审计 |
| NC | 全量审计 |
| 冷重开 | 网络成员保持一致 |
| 器件字段 | MPN、value、footprint关键项核对 |
| ERC/DRC | 尽量获取正文；若工具仍只返回count，保留明确HOLD，不重建工程 |
| 图面 | 全页实际查看，无明显标签重叠、端口碰撞、不可读文字 |
| PDF | 最终审查版输出 |

如果ERC工具依旧只给数量：

`ERC_DETAIL_HOLD`

可以保留。

**不能为了取得ERC文字再重建168器件。**

---

# 九、受控台架验证只准备，不执行

本包增加一个：

`BENCH_VALIDATION_PLAN.md`

只写计划，不上电。

后续真正bench建议按：

**标准电阻阵列 → 示波器看ROW/TIA建立 → ADC/SPI → 100 fps → 真实传感阵列**

逐级推进。

台架重点验证：

- 1–7 kΩ；
- ±约10%变化；
- 300 µs建立；
- 100 fps；
- 校准后≤1%；
- 帧SD≤0.2%；
- 20–30°C reset；
- 实际参考电容启动；
- 实际噪声。

故障短路/60 s类测试继续单独审批，不能混在第一次上电里。

---

# 十、唯一下一包

## `SCIENCE_ADK5556_4X4_R21_ENGINEERING_R21_NATIVE_AND_LIMITED_VALIDATION_V1`

这是现在唯一主线。

### P0 — 范围和ECO冻结：40 min

核对冻结R2、R2.1成熟改动及1–7 kΩ正常范围/0.8–8 kΩ保护带。

不允许进入MIMO/descriptor研究。

### P1 — 有限工程验证：120 min

授权：

- 实际SPICE OP/AC合计≤32；
- normal transient≤12；
- 每个暂态≤180 s；
- 连续15 s仿真时间不推进即可STOP；
- offline有限DC/误差case≤48；
- reset解析≤32；
- protocol tests≤48。

**full-long=0。**

**PZ=0。**

**MIMO新研究=0。**

**descriptor新研究=0。**

### P2 — R2.1原生、连接和图面：240 min

授权：

- 工作副本1；
- session≤2；
- save≤8；
- capture/audit≤4；
- ERC/DRC≤2；
- PDF≤2；
- 新库身份≤4；
- 新原厂资料≤8；
- 元器件替代候选≤2，仅允许用于明确元数据/可获得性/RESET小修，不允许改变架构。

### P3 — 完整交付：80 min

GitHub一个新固定commit，一次完整正文与附件。

总上限：

\[
\boxed{480\ \text{min}}
\]

旧07余量关闭，不结转。

---

# 十一、真正的科学STOP现在只剩这些

只有以下情况才回来找我，不要小步骤反复请示：

1. **1–7 kΩ正常工作点出现实际饱和/越轨；**
2. 0.8–8 kΩ保护带出现可能损伤器件的电流/功耗；
3. 已经能跑完的普通宏模型显示明显增长振荡；
4. 300 µs建立在正常1–7 kΩ范围内明确失败；
5. 100 fps在现有八状态下算术上无法实现；
6. direct reset正常接口无法满足MCU门限；
7. 发现实际pin-net错误；
8. 必须更换OPA/ADC、改变0.25 V激励、4.99 kΩ主增益或8线架构；
9. 本包480 min或硬次数耗尽。

**“大型宏模型跑不完”“理论还不能严格排除hidden mode”“descriptor还有9 nV误差”都不再属于科学STOP。**

---

# 十二、最终状态定义

理想情况下，下一次回来应该是：

```text
R21_NATIVE_REVIEW_SCHEMATIC_COMPLETE
LIMITED_ENGINEERING_VALIDATION_COMPLETE
BENCH_VALIDATION_PENDING
```

并继续保留真正需要实物确认的：

`FAULT_PROTECTION_HOLD`  
`REFERENCE_CAPACITANCE_BENCH_HOLD`  
`HARDWARE_WCET_PENDING`  
必要时 `ERC_DETAIL_HOLD`  
`BENCH_NOT_RELEASED`

**PCB、制造、采购、真实上电依然全部为0。**

这次主线已经收回来了：**先把R2.1原理图做完整、做干净，把1–7 kΩ/10%变化这个实际任务有限验证清楚，然后进入受控实物验证。**

后面不再因为还能构造更严格的数学证明，就把电路项目重新变成稳定性理论研究。
