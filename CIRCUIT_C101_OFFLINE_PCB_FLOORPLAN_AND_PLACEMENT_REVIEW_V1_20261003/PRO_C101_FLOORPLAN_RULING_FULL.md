可以收口了。我把 `b1b4413...` 里的 C101 最终回执、强制图纸补充、冷态101件 BOM、363-pin 全连接和温冷语义审计重新核了一遍。我的集中裁定是：

> **接受 C101 作为本项目当前唯一的“电气功能基线”，但接受对象必须是“原理图 + `DRAWING_ANNOTATION_ADDENDUM.md` + actual BOM/pin map”这一配套集合，不接受旧注释残留的 PDF 单独作为最终原理图。**
>
> 因此，**可以进入离线 PCB placement/floorplan 阶段**；不需要再因为 ERC 只有 warn count 或旧R2文字去开 API/ERC 工具研究包。

这一次不再卡主线。

---

## 一、C101 电气基线：正式接受

我认可下面这些事实已经形成足够的工程闭环：

- **101 structural / 101 populated / 0 DNP**
- `36R + 44C + 7 protection + 10IC + 4J`
- 相对176件减少75件，约 **42.6%**
- 363 pin 中323 connected、40 intentional NC
- 所有pin/net均匹配C101计划
- warm/cold **101个器件身份、值、footprint、pin set、net map全部一致**
- PMEG2010BER方向实际为 `A→V3V3、C→V5`
- U12已经真正换成单颗 `RT0603BRD0716K9L`
- 原12颗假DNP已经彻底删除
- TPD4E05U06的TI厂家/MPN已经修正
- 其余97件没有发生非授权变化

这已经满足我上轮要求的“**电气结构真正落地 + independent cold reopen**”。

所以状态改为：

```text
C101_ELECTRICAL_BASELINE_ACCEPTED = true
C_SCHEMATIC_ACCEPTED = true        # 仅指“配套addendum审查集”
PCB_PLACEMENT_ELIGIBLE = true
```

但要同时保留：

```text
DRAWING_STANDALONE_RELEASE = false
ERC_DETAIL_HOLD = true
LEGACY_ANNOTATION_HOLD = true
SYSTEM_PERFORMANCE_ACCEPTED = false
PCB_ROUTING_RELEASED = false
BENCH_RELEASED = false
MANUFACTURE_RELEASED = false
```

这里的 `C_SCHEMATIC_ACCEPTED=true` **绝不代表那6页PDF自己就是最终生产图纸**。

---

# 二、ERC 752 warnings：保留 HOLD，但不再阻挡 placement

这一点我专门区分。

目前唯一得到的是：

`[{type: warn, count: 752}]`

没有warning body，所以当然不能说：

> “ERC 0错误、没有Critical/Important。”

这个结论没有证据。

但是，我们现在已经独立获得了：

- 363/363 pin计划匹配；
- 101/101器件实际匹配；
- warm/cold net map一致；
- 40个NC明确可解释；
- 没有发现额外器件或隐藏net差异。

因此，对于**纯离线 placement/floorplan**这种不改变网络的工作：

> **ERC_DETAIL_HOLD 不再是 blocking gate。**

它只在后续：

**native PCB routing / fabrication release**

之前必须关闭。

也就是说以后不要再为了“把752个warning导出来看看”停住整个项目。

等到真正准备 routing 时，如果现有ERC接口仍不能给明细，再做一次**极小范围人工net/drive sanity check**即可，不允许演变成EDA工具研究。

---

# 三、旧R2文字：强制Addendum已经足够承担当前功能说明

我接受你现在的处理方式。

旧PDF里以下内容确实已经失效：

- 四行运放 + AND逻辑；
- Schmitt/HW_ENABLE；
- remote-sense TIA；
- 两颗LM73100；
- 旧3.1085 V监督阈值；
- 旧48k/frame等实现口径。

而 `DRAWING_ANNOTATION_ADDENDUM.md` 已经逐页明确写出了 C101 当前状态：

- Page1：TPS7A3701 + REF3025 + PMEG2010BER
- Page2：single OPA388 + dual 4:1 TMUX1109
- Page3：direct TIA
- Page4：双bulk有效容量仍HOLD
- Page5：PB1 = ROW_MUX_EN，无U13/14/15
- Page6：U11/U12分开监督，U12=16.9k/10k

因此现在执行规则冻结为：

> **任何后续人员看到C101 PDF，都必须与Addendum一起看。**

这足以做：

- 电气review；
- placement；
- 功能分区；
- 初步走线策略。

但它仍不能做：

- standalone production drawing；
- 装配依据；
- manufacturing release。

以后真正进入routing前，再把旧注释在native schematic里统一更新一次即可。**不是现在。**

---

# 四、J2机械问题：我顺手把官方资料核清了，placement阶段已经够用了

这里有一个好消息。

你现在指定的：

**Molex 2005290081**

官方确认确实是：

- 8 circuit
- **1.00 mm pitch**
- **ZIF**
- **Front Flip**
- **Bottom Contact**
- **Right Angle**
- SMT
- 1.90 mm mated height

也就是你一直要求的那种薄型FFC/FPC翻盖接口，并不是KK/排针。:chatgpt-content-reference{index="0"}

所以对下一轮**离线floorplan**，我们已经可以确定其机械拓扑：

```text
PCB内部                  板边 / FFC出线方向
analog front-end → J2 ║  →→→ FFC
                         ↑
                       right-angle
                       front-flip
```

并且因为它是 **bottom-contact**，后续实际FPC金手指朝向必须按这个条件采购/设计。:chatgpt-content-reference{index="1"}

真正还没闭合的是：

- 当前native footprint metadata仍是旧 `MOLEX_1718560008...`
- precise pad/courtyard/body geometry尚未真正替换
- FFC插入/翻盖操作空间尚未在native PCB中确认

所以：

```text
FFC_MECHANICAL_HOLD = true
```

仍保留。

但是：

> **这不阻止离线布局设计。**

下一版布局里 J2必须直接使用“2005290081机械占位/keepout”，**不能再使用旧171856的body尺寸去排布**。

---

# 五、真正进入placement前，我只再冻结几条机械规则

这些直接沿用你之前的要求，不需要再问：

### J2

**必须贴板边。**

因为它是right-angle FFC connector，FFC方向要朝板外，接口外侧保持：

- FFC insertion corridor
- actuator翻盖空间
- cable bending allowance

禁止把模拟电阻、电容或IC放到FFC插入方向。

---

### J3 / J4

目前具体最终侧插型号仍没锁。

所以offline floorplan允许把它们定义成：

**“边缘接口保留区”**

但不能假装知道最终connector body。

逻辑保持：

```text
PCB内部 → 串阻/钳位 → J3/J4 → PCB外
```

接口外侧不放器件。

等型号冻结以后再把placeholder换成实际机械模型。

---

### J1

同理。

没有具体5 V插头型号之前：

- 放板边；
- U9、入口电容紧跟板内侧；
- 外侧留mating corridor。

---

# 六、101件PCB不要按“功能区散成六个岛”排

下一版我希望桌面端不要重复B311时期的问题。

C101减少到101件以后，已经足够做出一个很干净的**主信号流布局**。

我建议整个板的主要逻辑方向是：

```text
                       ┌──────── J3 SWD
                       │
J2 FFC                  │       MCU
ROW/COL                 │        │
  │                     │        │
  ▼                     │        └──────── J4 UART
┌────────┐   ┌─────────┐│
│ROW     │   │ADC      ││
│driver  │   │ADS8684  ││
│OPA388  │   │         ││
│TMUX1109│   └────▲────┘│
└───┬────┘        │      │
    │             │      │
    │  4×COL TIA  │      │
    └─→OPA4388────┘      │
                         │
      REF / VCM / VEXC   │
                         │
          POWER ─────────┘
J1 → LM73100 → TPS7A37
```

更具体地说：

> **J2 + ROW/MUX + TIA + ADC应该形成一个非常紧凑的模拟核心。**

不要为了“区块分明”把：

- ROW driver摆左上；
- TIA摆左下；
- ADC摆中间；
- REF单独摆很远；

这种布局会把本来短的高阻/反馈路径重新拉长。

---

# 七、下一轮的两个layout候选，我希望只差“宏观排列”

既然申请里允许：

`candidate <= 2`

那就只做两个真正有意义的版本。

### Candidate P1：横向信号流

```text
J2 → ROW/TIA → ADC → MCU → J3/J4

        ↓
      REF

J1 → POWER
```

优点：

- 最直观；
- 模拟路径极短；
- 排线→前端→ADC是单方向；
- 最适合接近方形PCB。

**这是我优先的版本。**

---

### Candidate P2：L形咬合

```text
J2 → analog front-end
          │
          ▼
         ADC → MCU → J3/J4

POWER / REF 沿底边
J1
```

优势：

- 可以更好利用方形板；
- 电源和数字区可以L形包住模拟核心；
- 接口都比较容易贴边。

两个候选都禁止回到：

> “每个功能区周围留一大圈空地。”

C101已经不需要这么干。

---

# 八、下一240 min离线placement包：批准

我批准你提出的下一包，但正式名称和范围冻结为：

**`CIRCUIT-C101-OFFLINE-PCB-FLOORPLAN-AND-PLACEMENT-REVIEW-V1`**

总预算：

**240 min**

具体分配：

| 阶段 | 预算 |
|---|---:|
| C101基线/硬约束合同 | 30 min |
| 功能分区 + pin驱动floorplan | 120 min |
| 全101器件几何/飞线/反馈路径审查 | 45 min |
| 2个候选图 + 比较 + 最终建议 | 45 min |
| **总计** | **240 min** |

允许：

- `candidate <= 2`
- 最终placement调整 `<=3`
- 输出图 `<=2`
- 使用当前 **101 actual identity/value/pin/net**
- 使用实际封装尺寸/已有真实几何
- J2用 **2005290081官方机械拓扑**作placeholder，不得用旧171856 body
- 对未冻结J1/J3/J4采用明确edge mechanical reserve，而不是猜型号
- 可以自行优化板框长宽，使其尽量接近方形
- 可以旋转/重新排列全部101件
- **旧B311坐标不得作为主seed**

禁止：

- CAD/native save
- EDA session
- 原生PCB移动
- 铜皮
- routing
- via
- pour
- Gerber
- 新SPICE
- 原理图修改
- BOM修改
- 制造/采购/bench
- 本地Git/system

也就是说这是：

> **真正从101件C101重新设计PCB摆放逻辑，而不是编辑旧176件PCB。**

---

# 九、这个包的唯一验收标准

下一轮回来我不需要再看一堆工具日志。

我要看到的是：

1. **101个器件一个都不少；**
2. J2/J1/J3/J4全部在合理板边；
3. J2外侧FFC操作区没有器件；
4. 四个TIA通道几何重复、紧凑；
5. `COL → OPA4388 → RF/CF` 反馈回路最短；
6. `TIA → R_ADC/C_ADC → ADS8684` 最短；
7. REF3025、VCM/VEXC离模拟核心近；
8. ADS8684全部reference/AVDD/DVDD电容围着对应pin放，而不是整齐排成一排但离芯片很远；
9. MCU/SWD/UART形成数字小区；
10. U9/TPS7A37/U11/U12及大电容形成紧凑电源链；
11. 模拟核心与开关电源不存在——目前是LDO，所以重点变成数字边沿和接口与TIA的距离；
12. 轮廓接近方形、留白自然，不人为制造巨大空区。

然后给我：

- **P1**
- **P2**
- 两者尺寸
- 关键反馈环长度/ADC连接长度/接口机械风险比较
- 你推荐哪一版

就够。

---

所以从现在开始状态正式推进为：

```text
C101_ELECTRICAL_BASELINE_ACCEPTED = TRUE
C_SCHEMATIC_ACCEPTED_WITH_ADDENDUM = TRUE
PCB_PLACEMENT_ELIGIBLE = TRUE

ERC_DETAIL_HOLD = TRUE
LEGACY_ANNOTATION_HOLD = TRUE
FFC_MECHANICAL_HOLD = TRUE
MLCC_CEFF_HOLD = TRUE
FULL_MATRIX_DYNAMIC_PERFORMANCE_HOLD = TRUE

PCB_ROUTING_RELEASED = FALSE
BENCH_RELEASED = FALSE
MANUFACTURE_RELEASED = FALSE
```

**接下来不用再碰电路架构了。开始把这101件板真正排漂亮。**
