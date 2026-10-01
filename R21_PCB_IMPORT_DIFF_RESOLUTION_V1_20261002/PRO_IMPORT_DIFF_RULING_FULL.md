我看了这次 R21 PCB Netlist Integration 的结果，**这次路线是正确的，没有跑偏**。

而且这一次比前面几次重要，因为它终于把问题从“猜测工具问题”拉回到了一个明确工程问题：

> **不是原理图错，不是封装错，不是网络设计错，而是 PCB 编辑器内部的 schematic ↔ PCB netlist 同步状态没有闭合。**

现在不要继续做 routing，也不要研究 JLCEDA 接口。

---

# 当前状态判断

## 1. 原理图基线：保持 ACCEPT

确认：

- 176 components
- 550 pads
- 514 assigned pins
- 107 nets
- 36 NC

与 accepted schematic 一致。

这个已经不用再动。

---

## 2. PCB现状

当前：

✅ PCB文件存在  
✅ 器件布局存在  
✅ 部分线存在  
✅ 网络信息基本继承  

但是：

❌ PCB netlist compiler 未通过


核心错误：

```
PCB and schematic netlist does not match.
Click Import Changes
```

这个是关键。

---

# 现在真正的问题是什么？

之前看到：

> 452 Connection Error

容易误判。

现在证据说明：

这452个不是：

“线路连接错”。

而是：

```
同一个net里面的两个对象目前没有物理铜连接
```

例如：

```
NET_TIA0

U2.OUTA
 |
RF0
 |
CF0
 |
COL0


但是PCB上：
U2.OUTA ---- RF0

CF0 ---- COL0

中间没有route

```

DRC自然说：

> same network objects disconnected

这是**未布线状态**。

不是电路错误。

---

真正阻塞的是唯一：

```
NetlistError
```

也就是：

PCB内部保存的网络表 ≠ 当前原理图网络表

---

# 下一步应该怎么做？

这次不要再申请大包。

下一步非常明确：

## PCB_NETLIST_DIFF_RESOLUTION_V1

目标只有一个：

获取 Import Changes 的真实差异。

---

## 操作顺序

你或者Codex执行：

### Step 1

打开当前PCB工程：

不要：

- 修改原理图
- 删除器件
- 重新导入
- 重新布线


只打开。


---

### Step 2

点击：

```
Design
 ↓
Import Changes
```

或者 DRC Error 里面：

```
PCB and schematic netlist does not match
 ↓
Import Changes
```


---

### Step 3

不要直接Apply。

先记录：

差异列表：

需要重点看：

### A. Net变化

例如：

```
Old:
TIA0

New:
TIA0_1

```

这种。


---

### B. Pin变化

例如：

```
U3.2
Old Net:
VCM

New Net:
VCM_FB

```

---

### C. Component变化

例如：

```
C_ADC0
added
removed
changed

```

---

# 我预计可能的根因排序

根据现在证据：

## 可能性1（最高）

### PCB保存的是旧netlist

因为：

之前经历：

- 原理图修改
- U3反馈端重建
- TIA电容迁移
- 接口调整

PCB可能保存了旧版本网络。

---

## 可能性2

### 某些局部网络名称变化

比如：

之前：

```
VCM_FB
```

后来：

```
VCM_FB1
```

PCB里面残留。


---

## 可能性3

### 空net/残留net

之前已经出现：

> net2为空

所以可能还有：

```
旧网络存在
但是没有pad
```

---

# 现在绝对不要做的事情

不要：

❌ 删除PCB重新导入  
❌ Import Changes直接全部接受  
❌ 修改原理图去迎合PCB  
❌ 清理网络名字  
❌ 开始布线  
❌ DRC反复跑  


因为现在必须先知道：

**谁是正确源头。**

目前规则：

> schematic 是master，PCB跟随schematic。

---

# 下一包建议

不要240分钟。

这个问题应该小包解决。

## R21_PCB_IMPORT_DIFF_RESOLUTION_V1

预算：

60 min足够。

任务：

1. 获取Import Changes diff
2. 分类：
   - 可接受同步
   - 错误同步
   - 历史残留
3. 保存diff证据
4. 决定一次同步动作

交付：

- IMPORT_CHANGE_DIFF.csv
- BEFORE_AFTER_NETLIST_COMPARE.csv
- 同步后冷重开检查


通过门：

```
schematic netlist
=
PCB netlist

NetlistError=0
```

然后才进入：

```
Routing closure
```

---

# 当前阶段一句话

现在：

```
原理图:
✅ 已冻结

PCB:
✅ 基础布局完成

PCB网络:
⚠️ 同步未闭合

布线:
⏸ 等待

制造:
❌ 未进入
```

这一步其实是PCB设计里面非常正常的一关。

之前真正绕偏的是花大量精力证明电路数学稳定；现在已经回到工程主线：

**先让CAD里的网络状态正确 → 再布线 → 再DRC → 最后才考虑打板。**

这次不要继续扩大范围，先拿 Import Changes 差异。拿到差异以后基本就是一次性收尾。
