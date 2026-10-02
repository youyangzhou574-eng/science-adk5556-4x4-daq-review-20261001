我把 `9e36b8...` 这一包的阻断原因、缺件清单、两版部分坐标和链长重新核过。结论很明确：

> **这不是50×50 mm放不下，也不是C101太复杂，而是placement顺序错了。**  
> 两个候选剩下的几乎全是ADC/LDO/MCU相关电容；程序又把“8.2 mm局部邻域”当成了事实上的硬边界，结果低优先级器件先占位，真正必须贴近引脚的电容反而最后没地方。

所以我批准下一包，但不再让它沿着89/88件坐标继续补洞。**唯一工程收口路线是“ADC电容bank优先的层级式全量重排”**。

## 1. 旧P1/P2只作证据，不作新布局seed

当前P1虽然只放了89件，但有一个很有价值的信号：

- P1 `TIA → R_ADC → ADC pin` 直线代理 mean ≈ **11.41 mm**
- P2 ≈ **16.16 mm**
- P1 max ≈ **15.27 mm**
- P2 max ≈ **19.45 mm**

因此宏观上仍然是**横向P1方向更合适**。

但下一轮：

- 不继承89件坐标；
- 不把当前U5/U2/U7锚死；
- 不只扒拉那12颗未放电容；
- 不继续使用8.2 mm硬搜索半径。

旧P1/P2状态保持 `PARTIAL_NOT_SELECTABLE`，只用于说明为什么下一版应优先横向信号流。

---

# 2. 新布局必须按“宏单元”排序，而不是逐颗贪心

新的放置顺序冻结成下面这样。

### 第一优先级：接口和板边机械区

先锁：

- J2：左侧板边，2005290081保守占位和FFC外侧操作区；
- J1：下边或左下边；
- J3/J4：右侧边缘reserve。

这里只锁**机械区域**，不是锁周围小器件。

---

### 第二优先级：ADS8684整套bank，一次性占完整空间

这是本轮最重要的变化。

U5不能再先放芯片、后面一颗颗往8.2 mm里塞电容。应把下面这些视为一个整体宏：

**REFIO bank**
- `C_ADC_REFIO`
- `C_REFIO_B`

**REFCAP bank**
- `C_ADC_REFCAP`
- `C_REFCAP_BULKA`
- `C_REFCAP_BULKB`

**AVDD pin 9 bank**
- `C_ADCA1`
- `C_AVDD9_HF`
- `C_AVDD9A`
- `C_AVDD9B`

**AVDD pin 30 bank**
- `C_ADCA2`
- `C_AVDD30_HF`
- `C_AVDD30A`
- `C_AVDD30B`

**DVDD pin 34 bank**
- `C_ADCD`
- `C_DVDD34A`
- `C_DVDD34B`

也就是说：

> **先把U5 + 15颗ADC供电/reference电容一起排完，再允许其他器件占附近区域。**

层级必须是：

`100 nF / HF capacitor → 最靠对应pin`  
`2.2 µF → 第二圈`  
`22 µF bulk → 外圈`

不能为了“整齐”把五六颗22 µF排成一条漂亮直线但离对应pin很远。

---

# 3. 第三优先级才是 U2 TIA + 四路ADC输入

U2和U5形成一个共同模拟核心：

```text
J2
 │
 ▼
COL0..3
 │
 U2 OPA4388
 │
 RF||CF
 │
 TIA0..3
 │
 R_ADC
 ├── C_ADC → GND
 │
 U5 ADS8684
```

四路必须尽量做成重复模板。

这里优化顺序是：

1. `RF/CF ↔ U2` 最短；
2. `C_ADC ↔ U5 AIN pin` 最短；
3. `R_ADC` 横在U2与U5之间；
4. 然后才考虑视觉对齐。

上一版RF/CF代理大约5.8–6.2 mm已经偏松。下一轮不用设一个拍脑袋的硬毫米门，但应该明显比当前草稿更紧凑。

---

# 4. ROW端作为另一个独立紧凑宏

J2上半部分ROW直接服务：

- U4 TMUX1109
- U1 OPA388
- `R_SEL_PD0/1`
- `R_ENABLE_PD`
- `C_MUX`
- `C_ROW_OP`

这一组应该贴着J2的ROW侧。

特别要避免：

`J2 → 很长ROW走线 → U4 → 很长ROW_FB再回来`

单OPA + 双MUX的优势就是remote feedback，所以drive path和sense path都应该短而成对。

---

# 5. REF / VCM / VEXC 放在 ROW 和 TIA/ADC之间

建议形成：

```text
ROW core    REF/VCM/VEXC    TIA + ADC
```

U6、`C_REF`、`C_VCM_OUT`、`RD_TOP/RD_B1/C_DIV` 不再作为零散小区塞剩余空间。

特别是当前未放的 `C_DIV`，下一版应该和VEX divider一起预留，不应该最后才发现无位置。

---

# 6. 电源链也作为完整bank一次排完

同样处理：

```text
J1
 ↓
U9 LM73100
 ↓
V5
 ├─ U11
 └─ U8 TPS7A3701
      ↓
     V3V3
      └─ U12
```

同时一次放完：

- U9 IN/OUT cap
- U9 100R bleed
- OV/EN网络
- `C_PWR`
- `C_LDO_IN`
- `C_LDO_OUT`
- `C_LDO_FF`
- R_LDO_TOP/BOT
- D_LDO_REV
- U10_BLEED
- U11/U12所有sense/CT/VDD件

这样就不会出现上一版 `C_LDO_IN / OUT / C_PWR` 全部被拖到最后没位置。

---

# 7. MCU最后进入，而不是先占ADC附近黄金区

U7需要靠右，方便：

- SPI → ADS8684
- SWD → J3
- UART → J4

但除了SPI侧，MCU周围并不是精密模拟黄金区。

所以 `C_MCU1` 和 `C_MCU_BULK`跟U7一起走；当前缺失的 `C_MCU_BULK`下一版不能再被放置顺序遗漏。

---

# 8. 板尺寸：50×50仍是主目标，但不把它变成新的死门

我不批准“只要50×50放不下就继续无限挤”。

下一包规则是：

**Primary P1-FULL：50 × 50 mm**

优先完成横向信号流的101件全量布局。

如果在已经正确做了ADC bank-first、整体移动大IC之后，仍然无法同时满足：

- 101/101；
- 无body/pad-proxy overlap；
- J2操作区；
- J1/J3/J4边缘reserve；
- HF电容贴近相应pin；
- 四路TIA合理重复；

那么允许第二候选：

**P2-FULL：最多 52 × 50 mm 或 50 × 52 mm。**

这是约4%的单边放宽，仍然接近正方形。

不允许直接跳到55×55之类的大板。

这样第二候选真正回答的是：

> **为了不牺牲模拟布局，50 mm是否值得多给2 mm。**

比继续做一个信号路径明显更长的旧L形P2更有工程价值。

---

# 9. 两个候选不再平均花力气

下一轮的两候选定义为：

**P1-FULL：50×50，横向流，主方案。**

**P2-FULL：只有P1完整后仍存在明显拥挤/反馈路径劣化，或者P1在合理整体重排后无法全放，才启动；边长最多放宽2 mm。**

也就是说我不要求“为了用满candidate=2必须生成两个版本”。

如果P1已经：

- 101/101；
- 几何完整；
- 关键链明显合理；
- 机械reserve完整；

第二候选可以只做一次轻量对照，甚至不必消费全部placement额度。

---

# 10. 下一300 min批准

批准：

**`CIRCUIT-C101-BANK-FIRST-FULL-PLACEMENT-CLOSEOUT-V1`**

总预算 **300 min**。

- 60 min：建立bank/接口合同；
- 120 min：完整101件placement；
- 60 min：363-pin/geometry/关键链全量审查；
- 60 min：最多两张最终图和交付。

硬额度：

`source = 0`  
`candidate ≤ 2`  
`placement ≤ 4`  
`image ≤ 2`

四次placement不再解释成“脚本每失败一次就整版重跑”。

建议实际分配：

- Attempt 1：P1 bank-first初排；
- Attempt 2：P1全局调整；
- Attempt 3：P1最后完整收敛，或必要时启动P2；
- Attempt 4：只用于P2完整收敛/最终比较。

---

# 11. 这一次哪些东西绝对不能做

继续全部为0：

- CAD/session/save/export
- 原生PCB移动
- 原理图/BOM改动
- SPICE
- 铜线/routing
- via/pour
- Gerber
- 采购/制造/bench
- install/system/localGit

不研究新的优化器。

不因为某颗电容放不进去就删电容。

不因为50×50困难就改电路。

---

# 12. 下一包真正的PASS门

这次只有达到下面条件才允许出“候选图”：

1. **101/101全部有坐标；**
2. 101件全部在规划板框内；
3. 所有body/pad proxy无非法重叠；
4. J2 FFC corridor无侵犯；
5. J1/J3/J4 reserve无侵犯；
6. ADS8684五组供电/reference bank全部放齐；
7. 所有HF/100nF近端件先于bulk满足邻近优先级；
8. 四路 `U2→RF/CF→R_ADC/C_ADC→U5` 全部可识别且基本重复；
9. ROW drive/sense回路完整；
10. 363 pin net身份不变。

**任一不满足，就不许再画“漂亮的PARTIAL候选图”。**

这次图片额度只给**完整101件方案**。

如果300 min结束仍没有101/101，就只交坐标/失败表，不生成误导性的半成品图。

---

综合现有证据，我现在的工程判断是：

> **P1横向方案仍然值得保留，而且50×50有很大概率能闭合。现在最重要的不是再发明布局算法，而是把ADS8684周围那15颗电容当成一个整体先占地。**

所以状态保持：

```text
C101_ELECTRICAL_BASELINE_ACCEPTED = TRUE
PCB_PLACEMENT_ELIGIBLE = TRUE

CURRENT_LAYOUT = BLOCKED_PARTIAL
OLD_P1_P2 = EVIDENCE_ONLY

NEXT_ROUTE = BANK_FIRST_FULL101
PRIMARY_BOARD = 50x50
CONTINGENCY_BOARD <= 52x50 / 50x52

PCB_ROUTING_RELEASED = FALSE
```

这次就沿这一条路线收掉，不再围着最后十几颗电容反复打补丁。
