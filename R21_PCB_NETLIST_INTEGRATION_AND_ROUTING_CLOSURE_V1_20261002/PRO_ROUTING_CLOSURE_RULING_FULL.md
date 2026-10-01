我看完这次 PCB 包的状态，先给结论：

**这次没有跑偏。方向是对的，但停在了 PCB 真正开始收敛前的一个关键节点。**

前面我们已经把容易绕进去的东西（MIMO、descriptor、稳定性数学、EDA工具问题）全部停掉了。现在主线非常明确：

> 原理图冻结 ✅  
> PCB 工程启动 ✅  
> Floorplan 完成部分 ✅  
> 网络/封装继承检查完成 ✅  
> **现在卡点是 PCB 内部网络整合 + 正常布线收敛，而不是电路方案问题。**

---

## 当前 PCB 状态判断

### 已经接受的部分

这些可以冻结：

### 1. 原理图 → PCB 数据继承

报告里：

- 176器件
- 550 pads
- 514/514 pin connection
- 107 nets
- 36 NC

和 accepted schematic 一致。

这个说明：

**不是原理图错，也不是导入PCB后器件丢失。**

这一关通过。

---

### 2. 初始板框

当前：

- 100 mm × 90 mm
- 4层板
- 实验室验证板

这个作为第一版没有问题。

现在不要重新纠结尺寸。

后面如果发现：

- TIA区域拥挤
- ADC参考区域不够
- 接口位置不好

再调整。

---

### 3. 初步布局方向

当前应该保留：

```
J2传感接口

       ↓

ROW DRIVER

       ↓

TIA ARRAY

       ↓

ADC

       ↓

MCU/SPI
```

这个信号链方向正确。

不要重新布局推翻。

---

# 真正的问题在哪里？

现在有两个问题。


---

# 问题1：PCB Netlist Compiler 没闭合

报告：

> 452 Connection Error
> 1 Netlist Error


这个是当前第一优先级。

注意：

这不是说：

“452根线都错了”。

更可能是：

PCB工具内部认为：

- 原理图网络
- PCB网络
- pad绑定

没有完全同步。

尤其你报告里这个：

> 107net1有真实514成员，net2为空

这个很像：

某一次 setNetlist / update PCB 后留下空网络或者网络映射残留。

所以下一步不能直接疯狂布线。

必须先：

## PCB_NETLIST_INTEGRATION

目标：

让：

```
Schematic Net
      =
PCB Net
      =
Pad Connection
```

三者一致。

---

# 下一包我同意：

## SCIENCE_ADK5556_4X4_R21_PCB_NETLIST_INTEGRATION_AND_ROUTING_CLOSURE_V1

但是路线调整一下。

不要把360分钟全部花在routing。

顺序必须：

---

# Phase 1：网络整合（最高优先）

预算：

60 min


目标：

不是改电路。

只处理：

- 空net删除
- 原理图同步
- pad-net重新绑定
- 检查是否存在孤立pad
- 检查dangling connection


通过门：

必须达到：

```
Netlist Error = 0

Connection Error = 0
或者明确为未布线ratsnest，而不是connection错误
```

这里要区分：

### 正常：

未布线：

```
Net A:
U1.1 ---- J2.3
(airwire)
```

这是正常。

---

### 错误：

```
U1.1 expected NetA
Pad belongs NetB
```

这是必须修。

---

# Phase 2：模拟核心区域布线

不要全板auto route。

禁止。

这个板最关键不是数量，是模拟性能。

优先：

## TIA区域

每一路：

OPA4388

↓

Rf 4.99k

↓

Cf 2.2nF

↓

COL

要求：

- feedback loop最短
- RF/CF贴近运放
- 不穿数字区域


四路：

```
TIA0
TIA1
TIA2
TIA3
```

先手工。


---

## ADC区域

重点：

ADS8684：

- REFIO
- REFCAP
- AVDD
- AIN0~AIN3


必须：

- 短
- 干净
- 连续GND参考


---

## VCM/VEXC

重点：

不要让：

```
MCU SPI
数字线
```

穿过。

---

# Phase 3：普通数字/电源布线

最后：

- SPI
- UART
- SWD
- GPIO
- 电源普通线


这些不用过度优化。

---

# Phase 4：DRC

这里不要再犯前面的错误。

不要看到：

> DRC很多

马上进入工具研究。


只看：

三类：

## 1. 真错误

例如：

- 短路
- 未连接
- clearance


处理。

---

## 2. PCB规则提醒

例如：

- silkscreen
- text overlap

记录即可。

---

## 3. 模板默认

忽略。

---

# 我认为现在不要做的事情

明确禁止：

❌ 不再研究EDA API  
❌ 不研究SDK/cache  
❌ 不研究MIMO  
❌ 不重新验证OPA稳定性  
❌ 不重新改原理图  
❌ 不做SPICE  
❌ 不生成Gerber制造文件  


这些都会再次偏离。

---

# 关于PCB是否已经“完成”

目前：

不是。

准确状态：

```
Schematic:
ACCEPTED

PCB:
Floorplan completed
Partial routing completed

PCB electrical closure:
NOT COMPLETE

Manufacturing:
NOT READY
```

距离真正PCB完成还有：

1. Netlist clean
2. 完整布线
3. DRC审查
4. 关键电源/模拟review
5. 输出制造文件（未来）

---

# 下一包预算建议

我接受申请，但稍微改：

## R21_PCB_NETLIST_AND_ROUTING_CLOSURE_V1

360 min：

|任务|时间|
|-|-:|
|Netlist整合|60 min|
|关键模拟布线|120 min|
|普通布线|90 min|
|DRC+冷审+交付|90 min|

允许：

- session ≤3
- save ≤12
- capture ≤4
- DRC ≤4

禁止：

- PCB制造
- Gerber发布
- 下单

---

另外提醒一个关键点：

这次报告里有一句：

> autoRouting 49.75s 超时

这个不要继续尝试。

这个板不是靠autorouter完成的。

4×4阵列 + TIA + ADC，本质是**模拟采集板**。

正确路线就是：

**工程师手动关键路径 + 工具辅助普通连接。**

---

所以当前一句话总结：

> **现在已经回到正确主线了。下一步不是再修电路，而是把PCB从“导入正确”推进到“网络闭合+模拟布线完成”。**

这一步完成以后，才是真正进入“板子能不能打”的阶段。
