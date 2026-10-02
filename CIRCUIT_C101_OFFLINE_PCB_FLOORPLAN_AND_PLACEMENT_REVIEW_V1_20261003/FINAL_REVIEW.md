# 单次 fresh 最终审查：C101 离线布局阻断包

审查结论：可以作为如实披露的 PARTIAL/BLOCKED 证据包收口；不能作为合格 layout、101 件 placement 或后续 CAD/routing 放行。未发现未披露的 Critical 或 Important 问题。仅有一项图例精度的文档说明建议，允许在既定一次 doc/disclosure 处置中处理；不需要也不允许新增坐标、第三图、优化器研究或第二次审查。

审查对象严格限定本目录。已完整阅读 PRO_C101_FLOORPLAN_RULING_FULL.md（2a9ac0f3 / parent b77）、COMPLETE_C101_FLOORPLAN_RECEIPT.md、README.md、GATES、预算/ledger、冷态身份与连接、物理几何、target register、partial audit、全部 placement 失败日志及四份执行源码快照、提取/几何/审计/渲染源码，并实际查看两张既有 PNG。未运行这些会写文件或产生坐标的脚本，未启动 CAD/API/SPICE、未查网络来源、未生成图、未访问其他项目。只写本 FINAL_REVIEW.md。

## 1. 事实与计数核查

本次只读结构核查得到：

- C101_IDENTITY_AND_NETS 的 101 个条目与本目录 cold capture 的实际部件对象逐个相等；物理几何也是 101 身份。
- 363 个物理 signal pad 的 ref-number/net 全部与 cold pinNetMap 一致，40 个 NC，323 个 connected；ALL_PINS.csv 为 363 行。
- FUNCTIONAL_TARGET_REGISTER 有 87 个目标器件、172 条目标边；逐边核查部件 pin 与 owner pin 的 net 均相等且非空。该结果不是全网电气性能或路由资格。
- INPUT_MANIFEST 指定的六个本地副本 SHA256 均与冻结值一致。本次审查没有越出目录重新读取原文件；原文件仍一致的历史证据来自 INPUT_SHA_VERIFICATION。
- P1 实际 positions=89，缺 12；P2=88，缺 13，无额外身份。二者分别只能形成 3916 和 3828 个已放件 pair。ALL_PLACED_AND_UNPLACED_101.csv 每候选保持 101 行，缺件没有假坐标。
- 距离 CSV 每候选 172 行；P1 有 149 个已放引脚代理距离、23 个 UNPLACED，P2 有 147/25。缺件距离没有以零冒充有效结果。
- receipt 与 README 当前字节哈希一致；两图显著标明 PARTIAL 89/101、88/101、缺件列表、all5050 HOLD、非 native/routing 和不可选为终稿。

PARTIAL_PLACEMENT_AUDIT 的 body/pad proxy 交叠 0/0 是已放件检查结果。审计源码对全部已放件组合检查，没有功能类别过滤；既有结果没有被文字扩张为全 5050 对合格。本审查不重算科学结果或重新运行几何生成。

## 2. P2 续段的独立评估

续段披露与现存代码、日志和预算事件一致，可以保留“同一预扣 pass3 的未执行 P2 半段”的表述：

1. pass1 在建立 D_DBG0 target 时即 same-net guard 失败，尚未进入候选循环；失败计入 placement1。
2. pass2 在 P1 RF0 模板合法性 guard 失败；循环异常重新抛出，所以 P2 没有开始。
3. pass3 原脚本在进入两候选循环前已预扣一次，P1 在 C_AVDD9_HF 搜索失败后重新抛出异常，留下 89 件；P2 尚未执行。
4. continuation 入口要求 spent.placement=3、预算未 STOP、P1 pass3 partial 存在、P2 pass3 partial/placement 不存在；循环中明确跳过 P1，仅首次执行 P2。P2 在 C_AVDD9B 失败，留下 88 件。
5. 本次将两个 pass3 快照从 config 定义到结尾逐字比较，删除续段唯一的 `if continuation and name=='P1':continue` 行之后完全相等。也就是说 anchors/config、全部 targets、5.4 mm feedback template、排序、0.5 mm lattice、8.2 mm 搜索半径、成本和合法性条件没有在续段改变。当前 create_two_floorplans.py 与 P2 续段执行快照哈希相同。

因此没有发现 P1 重放、已放件调整、P2 搜索规则更换、退款或隐匿第四次优化的证据。此判断以目录内保存的执行记录为界；不是操作系统级完整历史取证。最终预算 candidate2/2、placement3/3、image2/2 和 STOP 必须原样保留，不能把这种续段解释再次用于启动任何新坐标。

## 3. 几何、机械和指标的证据边界

J2 提取分支明确跳过旧 KK body/pad 模型，改为显式 14×7 mm FFC planning placeholder；cold footprint metadata 仍旧值，报告已说明未修 native。8P/1 mm/right-angle/bottom-contact/front-flip 是拓扑条件，14×7 和规划焊尾不是厂家准确 datum、max courtyard 或制造封装。两个机械空网占位只在 metadata 中表示，不能视为实际焊盘/装配已验证；当前 FFC_MECHANICAL_HOLD 足以承接这个限制。

J1/J3/J4 已明确为边缘保留区加既有电气代理，最终侧插 body/mating 未知；没有把未知模型作为准确连接器资格。保留区空置及板内 proxy 结果只适用于已放件，不外推完整机械闭合。

RF/CF 四通道角色模板可识别，反馈与 ADC 指标严格属于实际同网 pin 的 Euclidean stub；报告已排除实际铜线、绕障碍、回流、全局最短、精度/100fps 和性能 PASS。有限贪心/8.2 mm 半径失败不能证明 50 mm 板数学不可行，回执已正确披露。缺件和部分空白不能作为越过硬预算继续优化的理由。

图例文档建议（Minor，不要求重画）：渲染的 reserve 轮廓是示意，不与合法性检查矩形逐点相同。例如 J2 图中外侧带到 x=-8，合法性矩形到 x=-10；J3/J4 图上虚线以连接器中心绘制，检查使用 x=44..60 的矩形。建议在一次 doc/disclosure 处置中加一句“图中接口虚线/阴影为示意；检查矩形以已保存 placement 源码 reserves 定义为准，仍非厂家机械资格”。不得因此生成第三图或改变坐标。

## 4. Gates 与交付界限

C101 电气基线接受来自 Pro 对原理图+强制 addendum+actual BOM/pin map 的配套接受，不是本轮重新授予的电气/系统性能 PASS。既有 ERC_DETAIL、LEGACY_ANNOTATION、FFC、MLCC Ceff、动态性能 HOLD 保留，不应重新阻挡如实的离线失败证据交付，也不应为关闭它们越门研究。

ALL101_PLACED、ALL5050_GEOMETRY_PASS、LAYOUT_REVIEW_READY、CAD_RELEASED、routing/bench/manufacture 继续 false。两 partial 图不得要求用户二选一，不宣称美观优胜或推荐作 native 模板。source/CAD/session/save/export/SPICE/PCB/routing/via/pour/Gerber/制造采购bench/localGit/system=0 与保存的范围/脚本记录一致；本审查没有执行其中任何操作。

本次审查时公开 manifest/ZIP/固定 commit 尚未在目录中形成，故不声称已完成公共交付或对其内容作通过认证。允许既定一次文档处置和正常交付：完整自有源码、cold101/net、几何、失败快照/日志、两个 partial、两图、指标和预算应可复核；metadata-stripped epro2 可引用既有固定 commit 并明确它是旧176 PCB 输入、非本轮 native 输出，避免重复发布 native。不得包含账户 SQLite、私有上下文或第三方 bulk PDF。发布前 manifest/ZIP 的完整性属于交付核验，不是再次 layout 审查。

最终 disposition：BLOCKED_LAYOUT / HONEST_PARTIAL_PACKAGE_ACCEPTABLE_FOR_DELIVERY。唯一必要后续为文档说明及冻结证据交付；保持 STOP，不进行二审。
