我接受这次 `055c733...` 的 P1 作为**完整101件、50×50 mm、可评审的离线布局基线**，但 I1 不建议“带着这个取舍直接进 native”。现在还没动原生 PCB，修这个方向问题的成本最低，所以我选：

> **执行一次唯一的 J2/ROW 局部修正。**  
> 不旋转 J2、不改 1–8 针序、不动 ADC/TIA bank、不重排整板，只把 ROW 宏真正拉回 ROW0–3 一侧。

I1 不是电气 FAIL。现在的 11–17 mm 代理长度本身没有违反一个已建立的电气上限；问题在于它和我们已经冻结的布局意图相反：ROW0–3 实际在 J2 的下半部，而 U4/U1 被放到了 COL 一侧上方。如果现在直接进入 native，这个错误的机械假设就容易被“冻结成事实”。

### 唯一允许动的范围

下一包只允许调整这组 ROW 宏：

- `U4 TMUX1109`
- `U1 OPA388`
- `C_MUX`
- `C_ROW_OP`
- `R_SEL_PD0`
- `R_SEL_PD1`
- `R_ENABLE_PD`

`RD_TOP / RD_B1 / C_DIV` 如果为了维持 VEXC→U1 的紧凑关系确实需要，可以随 U1 做**局部伴随移动**；除此之外不动。

以下全部冻结：

**J2方向和ROW/COL针序、U2、U5、全部16颗ADC bank、RF/CF、R_ADC/C_ADC、电源区、U6、U7、J1/J3/J4、50×50 mm板框。**

尤其禁止为了“解决I1”去旋转J2或交换 ROW/COL 顺序。当前J2规划定义继续是：

- ROW0–3：`y=25.5…28.5 mm`
- COL0–3：`y=29.5…32.5 mm`

因此调整应该发生在 **ROW宏**，不是接口定义。

### 局部调整的工程目标

不是给它新设一个拍脑袋的“必须小于X mm才工作”的电气指标，而是做明确的相对改进。

调整后必须同时满足：

1. **101/101仍全部放齐**，50×50不变，body/pad proxy overlap仍为0，所有接口reserve仍无侵犯。
2. U4必须从现在明显位于COL侧的状态，移动到**ROW pad group邻近侧**；优先使U4中心落到ROW/COL分界附近或其ROW侧，而不是继续位于COL0–3上方。
3. 对ROW0–3，J2→U4的 **8条 drive/sense 代理距离都不得比当前对应值更长**；目标是明显缩短现在约11.4–11.9 mm的drive和15.3–16.7 mm的sense。
4. 当前同一ROW的drive/sense路径差约3.9–4.8 mm，应尽量缩小；这是**布局优化指标**，不是性能PASS门。
5. `U1.1↔U4.8 (ROW_DRV)` 和 `U1.4↔U4.9 (ROW_FB)` 也要随宏整体保持紧凑，不能为了靠近J2而把U1甩到远处。
6. **U2/U5/TIA/ADC现有结果完全不得退化**，因为这些器件不允许移动。当前 `TIA→R_ADC→U5` mean/max 8.776/10.863 mm 和 RF/CF 结果直接继承，不重新优化。

换句话说，最合理的形态应该接近：

```text
                     板内
               U1 OPA388
                   │
            ROW_DRV / ROW_FB
                   │
               U4 TMUX1109
                   │
        ROW0 ROW1 ROW2 ROW3
                   │
J2 FFC  ║══════════╪══════════
        COL0 COL1 COL2 COL3
                   │
             U2 / TIA 区
```

不是现在这种 **U4/U1越过ROW区跑到COL上方** 的关系。

---

## 120 min 最小收口包：批准

批准：

**`CIRCUIT-C101-J2-ROW-ADJACENCY-LOCAL-CLOSEOUT-V1`**

范围严格按你申请的：

- 既有接口几何/方向合同：30 min
- ROW宏唯一一次局部调整：30 min
- 全101几何 + 363 pin/net + 关键距离复核：30 min
- 一张完整最终图 + 收口交付：30 min

硬额度：

`source=0`  
`candidate=1`  
`placement≤1`  
`image≤1`

仍然全部为0：

**CAD / session / save / export / schematic/BOM / SPICE / PCB native / routing / copper / via / pour / Gerber / procurement / manufacture / bench / install / system / localGit。**

这一次 `placement≤1` 的含义也很明确：**不是再跑一个顺序贪心优化器。** 直接以当前完整P1为基础，对上述ROW宏做一次有目的的局部调整，然后做全101复核。

如果一次局部调整找不到合法位置：

> 保留当前完整P1 + `J2_PIN_SIDE_ROW_ADJACENCY_HOLD=true`，停止；不要第二次偷偷重排，更不要回整体布局。

---

## 通过这次局部修正后的状态

如果上面6条全部满足，我允许直接推进为：

```text
OFFLINE_FULL101_REVIEW_READY = TRUE
ALL_MACRO_LAYOUT_INTENTS_ACCEPTED = TRUE
J2_PIN_SIDE_ROW_ADJACENCY_HOLD = FALSE
NATIVE_PLACEMENT_ELIGIBLE = TRUE
```

这里的 `NATIVE_PLACEMENT_ELIGIBLE` 仅表示：

> **可以把这101件离线坐标作为下一阶段原生 PCB placement 的输入。**

仍然不代表：

```text
PCB_ROUTING_RELEASED = FALSE
FFC_MECHANICAL_QUALIFIED = FALSE
ERC_DETAIL_HOLD = TRUE
MLCC_CEFF_HOLD = TRUE
SYSTEM_PERFORMANCE_ACCEPTED = FALSE
BENCH_RELEASED = FALSE
MANUFACTURE_RELEASED = FALSE
```

所以这不是再开一轮大布局，而是把现在唯一剩下的**宏观方向错误**修掉。ADC bank、TIA和101件全量已经收得不错，不需要再动。
