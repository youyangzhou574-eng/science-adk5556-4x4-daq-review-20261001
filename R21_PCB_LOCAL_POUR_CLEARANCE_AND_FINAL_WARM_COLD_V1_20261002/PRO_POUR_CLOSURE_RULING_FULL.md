# CIRCUIT-PRO-R21-PCB-LOCAL-POUR-REBUILD-AND-FINAL-CLOSURE-20261002-15

我按固定 commit `f25373b0ddd7b83ad447e6b41f39c12165425777` 看了实际4条Clearance、前后铜差异、550 pin、176器件和原生DRC。

这次STOP是正确的，但问题也已经非常局部：

> **两个V3V3断点已经真正修完：Connection 2 → 0。现在4条Clearance其实都是同一个新V3V3 via `e307` 与尚未重新计算的GND filled copper之间的派生覆铜间距问题。**

当前真实结果：

```text
Connection = 0
Short = 0
Clearance = 4
NetlistError = 0
```

4条分别来自同一个via在Top / Inner1上的 annulus、hole 与GND旧fill，实际距离0 mil、规则要求≥10 mil。

这里**不需要移动via、不需要重新走线，更不需要改规则**。上一包新增via以后没有执行正常覆铜更新，因此GND铜还保持着via出现之前的形状。这次批准一次正常的pour rebuild，让软件按现有10 mil规则生成anti-pad。

---

## 唯一下一包批准

### `SCIENCE_ADK5556_4X4_R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1`

批准 **120 min**。

额度：

- workcopy ≤ 1
- session ≤ 2
- save ≤ 1
- capture/audit ≤ 3
- DRC ≤ 3
- review export ≤ 1
- **normal pour update = 1**

明确：

- 新LINE = 0
- 新VIA = 0
- 删除LINE/VIA = 0
- move component = 0
- net/value/footprint/rule修改 = 0
- schematic / Import Changes = 0
- autorouter = 0
- 仿真 = 0
- Gerber / 制造 / 采购 / bench = 0

---

## 一、批准GND derived fill发生变化

这一点这次明确授权，避免执行端又因为“非V3V3铜变化”停住。

允许执行一次正常：

> **Rebuild All / Update Copper Pours**

冻结不允许变的是：

- 4个POUR的边界；
- net归属；
- priority；
- clearance规则；
- 层定义。

允许变化的是：

> **POURED / filled geometry 本身。**

特别是Top GND和L2 GND应当围绕新V3V3 via自动产生满足10 mil规则的anti-pad。

如果重铺后GND `POURED` 数据变化，这是**预期派生变化，不是设计漂移**。

---

## 二、入口先确认上次两个V3V3修正确实存在

下一包必须从**实际包含14号修正状态的native内容**开始。

在任何覆铜更新之前只读确认：

- `C_MCU1_1`新12 mil局部连接存在；
- e255保留；
- 两段Bottom V3V3桥存在；
- 新via `e307 / 5c0162206220ea3b` 存在；
- 176 / 550 / 514 / 107 / 36保持；
- component、pad-net、rules不变。

如果打开后这4个批准对象根本不存在：

**STOP，不重新手动画一次。**

不要猜是save还是序列化问题。

---

## 三、然后只做一次覆铜更新

顺序固定：

1. 实际打开PCB1画布；
2. 确认正确工程；
3. 执行一次 `Rebuild All`；
4. 不做任何额外铜编辑；
5. 立即跑native detailed DRC。

### 第一次DRC硬门

必须直接得到：

```text
Connection = 0
Short = 0
Clearance = 0
NetlistError = 0
```

如果还是4条Clearance，或者出现任何新的Connection/Short/Netlist：

> **立即STOP。**

不要第二次调clearance、挪via、加线、删铜。

那时再根据真实错误决定最小修正。

---

# 四、全零后才允许Save

只有第一次重铺后的DRC四类全部为0：

- 才执行唯一一次save；
- 做warm capture；
- 正常关闭session。

Warm必须继续：

```text
176 parts
550 pads
514 assigned
107 nets
36 NC
```

并确认：

- 新V3V3局部桥仍存在；
- e307仍存在；
- GND anti-pad已形成；
- 非派生用户走线没有意外变化。

---

# 五、然后独立cold reopen

重新打开同一保存工程，确认PCB1真实画布后：

1. capture；
2. detailed DRC。

最终要求仍然：

```text
Connection = 0
Short = 0
Clearance = 0
NetlistError = 0
```

以及：

```text
176 / 550 / 514 / 107 / 36
warm = cold
```

---

# 六、907 / 909 / 911 不再作为硬门

这件事现在正式收掉。

历史上：

- reopened actual：907 LINE
- 14号post-fix warm：909 LINE
- captured native File：911 LINE

多出来的两条仍然是此前已经记录的：

- VCM 0.1 mil
- TIA1 0.1 mil

表示差异。

**不要恢复、删除或专门研究这两条。**

最终验收只要求：

- 14号批准的实质V3V3铜保持；
- 本15号没有新增/删除用户LINE/VIA；
- warm/cold实际电气DRC全零；
- 没有非授权网络/铜变化。

LINE总数本身不再是PASS门。

---

# 七、什么情况下直接结束为PCB_REVIEW_READY

如果warm和cold都满足：

```text
176 parts
550 pads
514 assigned
107 nets
36 NC

Connection = 0
Short = 0
Clearance = 0
NetlistError = 0
```

并且只有正常的POURED派生几何变化，则直接定为：

```text
PCB_ROUTING_COMPLETE = PASS
PCB_ELECTRICAL_CLOSURE = PASS
COLD_REOPEN = PASS
PCB_REVIEW_READY = TRUE
```

**不用再申请一个PCB修正包。**

下一阶段直接进入：

> **制造前审查 / manufacturing preflight**

仍然不代表可以立即下单。

---

## 当前项目位置

这次不是又跑偏，也不是新发现了一个设计问题。

现在实际收敛过程是：

**452未连接 → 8 → 2 → 0。**

目前只剩新增via后**没有刷新GND覆铜**造成的4条派生Clearance。

所以15号包只干一件事：

> **更新一次覆铜 → DRC → 保存 → cold复核。**

按这个继续，别动其他地方。
