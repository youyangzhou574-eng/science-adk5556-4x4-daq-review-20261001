# 唯一 whole-package fresh-context 终审

审查日期：2026-10-02。范围：本目录冻结规格、计划、源脚本、CSV/JSON、已有审计与三张最终 PNG。执行 executing-plans 的一次最终独立审查；未运行生成脚本、几何重算、科学数据重放、CAD、联网、Git 写操作或第二轮审查。本次唯一新增文件为本报告。

## 已确认的优点与证据边界

- A/B 的 CSV 均为 176 行、176 个唯一 Designator，含坐标、角度、功能、约束、来源和限制；普通件实际重新组成行列，不只是旧功能框搬动。
- BODY_SOURCE_REGISTER 与 extraction audit 一致：175 个 native component-shape、1 个 J2 官方尺寸保守规划包络；552 pad 映射的记录最大残差 0.0017655193 mm。来源和公差资格的区别已公开说明。本审查未重新打开原生档案，因此这里确认的是冻结证据链内部一致性。
- body 的 local polygon 经自身角度和平移，pad 经实际位置相对中心的角度差和平移，ADC 的 90° 整块变换公式一致。body 自然包络、physical pad+body 包络、3 mm 建议板边政策有区别，没有把全部操作留白写成 PCB 材料。
- 已有 74 行 before/A/B 表数值保持；已记录的 body overlap 在 A2、B2、B3 为零，A1/B1 的真实失败保留。下文指出 pad proxy 检查范围缺陷，因此其零不能扩展为全体检查通过。
- 三张 PNG 已实际查看：主体布局、颜色分类、FFC 朝向、自然包络和 A/B 差异可读，没有 trace/via/pour/ratsnest。小 IC 的位号略挤不影响本次主体判断。
- 预算账本记录 A 2/3、B 3/3、images 3/3；原生、制造、bench 门保持关闭，没有依据说人已选 B。

## Critical

无。未发现现有包已经修改原生 PCB、释放制造或产生即时不可逆后果的证据。

## Important

### I1 — FFC 的 STOP 条款必须反映为本阶段接收阻断，不能只顺延到下阶段

位置：PRO_PLACEMENT_RULING_FULL.md:431；GATES.json:2、17；COMPLETE_PLACEMENT_RECEIPT.md:28、30、52；extract_geometry.py 的 J2 特例与 build_candidates.py 的 cable/opening 矩形。

现有报告诚实承认精确 housing/actuator 注册未确定，但仍把阶段写成 READY_FOR_HUMAN_REVIEW，并将闭合工作安排在“选定后”的原生机械准备中。原裁定明确把“FFC官方body/actuator空间无法根据已有资料确定”列为本阶段 STOP。13.4 × 5.8 的工程矩形、10 mm 插线和 2 mm 侧向政策、3.95 mm 侧视 reference 本身没有提供 actuator 全开平面扫掠相对 signal/MP datum 的可审计上界；不能仅凭没有 body 撞入这个自定义区域认定 STOP 已解除。

影响：接收方容易将 A/B 选择理解为布局包已按 Pro23 闭合、仅待原生实施，越过一个显式先决条件。CAD_RELEASED=false 降低即时风险，但不消除本阶段接收语义错误。

具体修复：用一次报告/门状态修订将本包标为“已生成 A/B 视觉草案，Pro23 placement 接收 HOLD/STOP：FFC body/actuator datum 尚未闭合”；保留三图供视觉讨论，明确视觉偏好不是完整布局接收。不得宣称人选 A/B 自动解除该门。若已有冻结证据确实能推出保守完整扫掠，应列出尺寸、基准、方向和包络包含关系；否则由用户/Pro 明确接受此项例外或授权后续有界闭合。当前不新增资料研究、不改几何、不重导图。

### I2 — 74-pair 表不是裁定所列关键邻接的完整 coverage

位置：build_candidates.py:93–98；KEY_PIN_DISTANCE_COMPARISON.csv；CONSTRAINT_BLOCKS.json；COMPLETE_PLACEMENT_RECEIPT.md:36。

距离枚举只将 R/C 开头的位号视为 passive，故 POWER5/POWER3 中的 U9_IN_CAP、U9_OUT_CAP、U10_IN_CAP、U10_OUT_CAP 全被漏掉，表中没有 POWER5/POWER3 行。它们的真实器件名和 C1206 footprint 已表明其为电容；同网关联也存在，分别应涉及 U9.5/V5_IN、U9.6/V5、U10.5/V3_LDO、U10.6/V3V3 与相应 cap.1。TIA 指定 RF0–3、CF0–3 同样未入表：其 COLn/TIAn 网经 R_COL_SENSE/R_TIA_ISO 与 U2 相连，纯“直接同网 IC pad”筛选会静默丢失，而规格并未把关键关系限定为直接同网。

这些器件确实属于刚性块，代码保持组内距离的设计是合理的；本发现是指定证据 coverage 缺失，不能据此声称它们实际被拉散，更不意味着电路连接错误。

具体修复：补一张明确的 required-key-part → 实际约束/证据 coverage 清单，按功能角色而非位号前缀定义关键件；区分直接同网 pair 与通过串联件建立的功能 pair。就当前禁止新重算的冻结审查范围，先把“74 pairs 全部保持”限定为已列出的 74 项，明确列出四个 power caps 与 RF/CF 的距离表缺项及刚性块保留依据；将全覆盖接收标为未闭合。若后续批准补算，应单独补证，不覆盖当前 74 行或历史 PASS，且不得算作已经发生的 B 第四轮。

### I3 — pad/body proxy overlap 检查错误跳过不同功能块之间的大量器件组合

位置：build_candidates.py:82；placement_common.py 的 groups/membership 定义；GATES.json:7–8；COMPLETE_PLACEMENT_RECEIPT.md:18。

groups 是“块名 → 位号列表”，不是“位号 → 所属块”。`if groups.get(r)==groups.get(s): continue` 对许多不同块的器件会得到 None==None 并跳过 physical 检查。例如 U2 和 U5 不作为 groups 的 key，TIA 与 ADC 的这对会被跳过；大量组内 passive 与其它锁定块之间也是如此。body overlap 的判断在该 continue 之前，故其零结果不因这个错误自动失效；但“保守 pad 包络 overlap=0”只是实际遍历子集结果，不能称全 176 范围清零。

影响：近邻块的 pad 外伸碰撞可能漏检，从而误导下一阶段搬件；当前不能凭静态审查推断确实存在碰撞，也不能继续把全局零当已验证。

具体修复：本轮先把相关完整性状态改为 UNKNOWN/PARTIAL_COVERAGE，并在 receipt 说明该零来自不完整组合检查。未来被授权修正检查时，应遍历全部不同器件对；若有合理的同块豁免，应使用 membership 并显式记录豁免范围，且仍需说明原组内已验证依据。不以修 bug 为由绕过 B3/3 和 images3/3，当前保留原始几何报告不回填。

## Minor

### M1 — 最大空白 proxy 与“周边最大连续空白”不是同一指标

位置：PRO_PLACEMENT_RULING_FULL.md:327；build_candidates.py:139–155。

当前算法寻找整个自然 bbox 内的 1 mm 中心采样空矩形，没有要求矩形接触周边；中心点未落 body 也不能证明整个 cell 无 body。ceil(width/height) 还使边缘样本域可能超出实际 bbox。receipt 已称“1mm采样”而未冒称 DRC，限据基本诚实。建议报告明确写为全 bbox 采样 proxy；真正周边连续空白仍未交付，留待授权的下一次指标补证，不为润色启动额外几何轮次。

### M2 — 源脚本另依赖未纳入四项 SHA 清单的旧 membership 文件

位置：placement_common.py:8；INPUT_SHA_MANIFEST.json；FROZEN_INPUT_RECHECK.json。

脚本从旧 CANDIDATE_B_PLAN.json 读取功能 membership，四项冻结清单不含该文件。当前包已保存 CONSTRAINT_BLOCKS 和候选 membership，当前结果可审计，但“原样再生成”的输入冻结并不完整。建议在说明中注明这一额外依赖与当前冻结的派生成员表，后续允许整理源时改为使用本包冻结 membership 或补齐输入 manifest；本次不重跑。

## Declined to judge

- 原生 CAD、布线、warm/cold DRC、制造、采购、机壳三维装配与 bench：本阶段明确禁止，不能要求本包提前验证。
- 远端 GitHub 发布权限、通信是否发送成功：主任务另行处理，不属于本次几何/接收门静态终审。
- Molex 原图外部再次查证、完整 actuator 三维研究：本次明确禁止新资料/API/3D研究；该证据缺口已作为 I1 留在接收门，不假定可以忽略。
- 是否应选 A 或 B：由人决定，本审查不代选。

## Verdict

**本阶段完整接收：No / HOLD。三张现有 PNG 可以作为未接收的视觉草案展示。**

一次修复应优先纠正报告与 GATES 的证据范围、显式保留 STOP 和缺项；不能把修文案当成机械或几何缺口已解决。I1–I3 未闭合前不能称 Pro23 全部要求通过。保留 A/B 坐标、失败记录和最终三图，不增加 CAD/几何/image 预算，不发起第二轮 review。
