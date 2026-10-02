# B2.1 唯一 whole-package 终审

结论：Critical 0 / Important 0 / Minor 1。现有包可作为本阶段离线视觉选择材料交付；最终视觉选择仍由用户/Pro 决定，CAD_RELEASED=false。未发现需要第四轮 placement、第二张图或第二次 review 的问题。

本次为 executing-plans 所要求的一次独立 fresh-context 终审。审查只读取已保存源、JSON/CSV、七输入哈希与唯一 PLACEMENT_B2_VS_B21.png，并写本文件；没有执行包内 Python、重算几何/距离/占用指标、联网、CAD/API/Git 或新增 agent。以下碰撞和面积结论来自已保存运行结果与完整源遍历的交叉审查，不冒称独立几何复跑。

## 审查覆盖与证据

- 已完整阅读 PRO_B21_RULING_FULL.md、COMPLETE_B21_RECEIPT.md、GATES.json、EXECUTION_BUDGET.json、PLAN_AND_LEDGER.md、FROZEN_AND_MOVED_REGISTER.json，以及 refine_top_band.py、placement_geometry.py、render_b21.py、prepare_renderer.py、write_receipt.py 和 initialize_stage.py 的阶段初始化逻辑。已读 B2/B21 保存的指标、28 个 finiteTrials、约束 membership/classes、176 坐标及全部 94 距离行，并核对相应源 pad/net。
- 七份 INPUT_SHA_MANIFEST 输入当前 SHA256 全部匹配。ACTUAL_GEOMETRY 有 176 器件、552 pad 条目；B2/B21 positions 与最终坐标 CSV 均为 176 条。逐器件显示的前后坐标和冻结寄存器相符；最终 CSV 的 X/Y/角度与 B21 JSON 无不一致。94 行 B21 表继承的所有 B2 列逐行与 B2 原表一致。
- 实际变化仅 U4、C_MUX、R_SEL_PD0..3 六件统一 X−28 mm，Y 与角度不变。CONSTRAINT_BLOCKS 的 MUX 恰含 U4/C_MUX 两件，四个 R_SEL_PD 属自由 C 类；源 net 分别连接 ROW_SEL0..3/GND，且对应 U4 选择端。TIA/ROW、REFERENCE、ADC、MCU/Logic、Power、J1/J2/J3/J4 及其余总计 170 件均保持原坐标与角度。没有拆 microblock；未改变 J2 插入方向。
- 只选上部获准 MUX 子集是合理的最小动作。授权允许 Bias/MUX/Digital 移动，并不要求所有可动块都必须移动。现有图显示 U4 已进入 TIA 上方空带；保留 Bias/Digital 避免扩大动作范围。U4/C_MUX 的共同刚体平移保持其内部关系；94 关键 pair 不包含该 B 级 pair，回执已明确区分。
- 全局 audit 对 sorted(G) 的 itertools.combinations(...,2) 完整遍历，无 sameblock 或同组豁免；body 与 body+保守 pad proxy 分别审查，阈值为交叠面积 >1e-8 mm²。保存结果每类 15,400 对、0 相交，与 176 器件完整枚举吻合。有限试点阶段覆盖六件对固定 physical 并集、六件内部两两及 FFC 规划 keepout；最终 audit 覆盖全体，最终 keepout 又检查冻结件。不能将该结果读成零距离接触被排除、制造间距或原生 DRC 合格。
- 94 行已保存 B21Mm 均与 B2Mm 相同，B21MinusB2Mm 均为 0。对应 pad 编号和源 net 一致；16 个 RF/CF 功能 pair 经 R_TIA_ISO/R_COL_SENSE 的异网关系与源电阻两端 net 对应，未当成直接同网。其余 78 行为直接网关系。所有 94 pair 的端点都属于冻结件；距离保持结论与变更范围一致，不证明原距离的电气性能资格。
- 28 个记录是本轮内部 7×4 有限平移点：六个 VALID，其余为碰撞/左界拒绝；唯一选定 (-28,0) 对应已保存左带指标 84、score 84.2。没有证据显示 28 轮或新候选体系。预算已记录本阶段 placement 1/1、图 1/1，累计 placement 3/3；执行结束应关闭 ACTIVE 状态并保存实际结束时间，不因此再运行几何或渲染。

## 图与指标的正确边界

已通过 view_image 查看唯一现有 3600×1800 对照图。左右使用同一 draw 函数、相同 x/y limits 与 equal aspect；自然 body 包络均为约 71×63.5 mm。J2 方向和中下部骨架在两侧保持，六件左移清楚可见。左上空带得到局部打断，右上仍明显留白；不能据此宣称顶部已完全连续、整体完全均匀或用户已满意。

266→84 mm² 指固定左上目标带 x=0.5..38.5、y=56..63 中的完整 1 mm 空格最大矩形；266→205 mm² 是全 bbox 的同类指标，两个范围不可混用。B2 保存的 largestEmptyRectMm 对应上述目标带；B21 finiteTrials 的选定条目对应 84。CV 0.416648→0.400006 是有限改善，bodyFraction 0.181578 与 bbox 不变。图中的虚线是自然 body 包络，未定义制造板框。

FFC 精确厂家 body/完整 actuator sweep 的 HOLD 继续有效；这不否定已允许的本阶段离线规划，也不能借本轮代理碰撞结果变成机械 PASS。native component-shape 与保守 pad 矩形代理的来源限制已在回执、图注和 BODY_SOURCE_REGISTER 中保留。原生搬件、板框、布线、温冷闭合及制造均未获本轮放行。

## Findings

Critical：无。

Important：无。

Minor 1 — 源文件应明确作为执行留档，而非整个目录的一键复跑入口。prepare_renderer.py 在生成时读取相邻旧 B2 的 render_b2.py；initialize_stage.py 依赖相邻 B2/通信目录并重写本阶段初始预算。最终 render_b21.py 自身已保存完整绘图逻辑，其实际计算输入都在本包，故不影响现有图或坐标的审查。本包适合审计当前冻结结果，但“全部 own 源”不等于“所有准备脚本可脱离外部工程任意重跑”。建议仅在 README/回执补一句：初始化/准备脚本是历史源留档，不得重跑或重置预算；无须补图、重算或重开工作。

## 审查保留项

源中 176/552/15,400 与左带 before=266 使用固定值；本次已用输入结构和冻结 B2 指标核对其适用性。after 取 VALID trial 的最小值，本次最小值确实是选定 (-28,0)，未发生选中方案与报告数值错配。这是针对本次冻结输入的审查，未认证其为任意输入通用工具。

FINAL_ARTIFACT_VERIFICATION 是原执行器的结构回执，不等同于本审查独立运行几何；本次额外核对了 CSV/JSON、原 B2 列继承和源 net。初次 PowerShell quoting 失败由 COMPLETE_B21_RECEIPT 明示为发生在 Python/image 启动前；本目录没有该次原始 shell 日志，审查不将文字说明提升成独立重放证明，也没有发现额外图或额外 reservation。

本审查不代替最终视觉选择，不认证 CAD、路由可行性、制造或 bench。预算封存后停止；不追加第四轮、第二图、第二 review 或工具研究。
