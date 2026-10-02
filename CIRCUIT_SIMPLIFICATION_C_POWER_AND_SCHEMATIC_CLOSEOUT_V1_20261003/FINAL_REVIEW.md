# 一次 fresh-context 最终工程、证据与隐私审查

审查日期：2026-10-03。审查对象仅为本目录的 C 电源与原理图候选包。本次唯一写入为本文件；没有 CAD/API、原生保存、PDF 导出、SPICE、科学重算、PCB 操作、Git、系统变更或第二审查。

**结论：COMPLETE 回执基本诚实地交付了一个被阻断的候选设计，但不是 Pro 要求的已闭合、无 Important 问题的 C 电路。本次发现一项新的 Important 公开交付披露问题；实施者已在同一次获准收尾中报告完成原件排除、脱敏派生和文档披露，处置边界见下文。没有在本次限定检查中发现另一个尚未披露的 Important/Critical 功能问题；这不代表电路正确、可用或可放行。所有既有 release=false 与 STOP 保持。**

## 新发现及唯一收尾事项

### [Important / P1] 原始 native 也含作者元数据，公开排除范围不能只写私有 SQLite 与 raw CLI context

- 审查初始版本的 `COMPLETE_C_POWER_RECEIPT.md:18` 只明确整个 `.eprj2` 不公开，并报告三个 credential key 为零；`:23` 笼统承诺 native 与全套 source 公开。三个凭据字段为零不等于不存在个人/作者元数据。这是初始发现，不能拿该初始措辞代表随后修订的披露。
- 本次只检查字段存在性，没有打印任何私人字段值。`C_NATIVE_EXPORTED_PROJECT_SOURCE.epru` 的第 1、65、3876、3880、5028、6481、8237、9218、10709、12401、15258、15263 行含 12 个非空 `username` 记录，并出现 `user`、`nickname`、`avatar` 等 DOCHEAD 元数据。原始 `C_SCHEMATIC_CANDIDATE_LEGACY_PCB_NOT_FOR_USE.epro2` 的 `.epru` 成员也含这些记录。
- 审查期间收到并读取了已经另存的 `NATIVE_PUBLIC_PRIVACY_DERIVATIVE.json`。它记录移除 270 个 DOCHEAD user/client 字段、保留原始文件、不同 SHA256、其他内容未改变，并明确 `nativeReopenValidation=false`。本次读取派生 ZIP 的 JSON/epru 文本，所查 `username/nickname/avatar/user/client/password/access_token/refresh_token` 字段计数均为零。此项只支持所列字段的限定检查，不是通用隐私保证或原生可打开性认证。
- **必须披露的处理：**整个私有 `.eprj2`、原始 `.epro2`、原始提取 `.epru`、包含私人项目上下文的 raw CLI 文件均仅本地保留；公共 native 应仅指独立命名的 `C_SCHEMATIC_PUBLIC_METADATA_STRIPPED_LEGACY_PCB_NOT_FOR_USE.epro2`。公开源码只能使用已脱敏版本（包含 `ACTUAL_SCH_SOURCE`），公开清单应区分原件与派生件及各自哈希，不可将原件哈希当作派生件哈希。注明派生件仅离线去元数据、未重新打开、仍带历史 PCB、不能用于 C PCB。
- 本项可通过现有脱敏派生交付及一次明确的文档/清单披露处理，不要求且不允许额外 CAD 保存、重新打开、重导 PDF 或科学重试。本次未审定尚未完成的远端附件/最终 ZIP 清单；不能声称已验证公开交付无泄露。
- **当前处置记录：**实施者随后报告：原始 native 在 `PRIVACY_GUARD_RED.log` 因作者元数据被拒；独立派生件在 `PRIVACY_GUARD_GREEN.log` 通过，并记录 15131 个非 DOCHEAD 行及其他 archive 成员字节不变；原始 native/epru 已排除公开，receipt/ledger/privacy files 已更新。这一完成状态来自实施者提交的处置证据说明；本审查不再启动第二次检查或重算。结合本次已经直接读取的派生审计及限定字段零计数，P1 的处置方向充分，公开时必须继续执行上述排除/命名/哈希规则；最终发布清单不在本次认证范围内。

## 已披露的 Important 阻断：确认仍存在，不重复当作新缺陷

| 项目 | 实际证据 | 审查判断 |
|---|---|---|
| U11 → LDO EN 与二极管复位联锁 | `C_ACTUAL_ALL_PINS.csv:10,246,322,326,354,360`；`C_ACTUAL_PARTS_AND_NETS.json` 的 `pinNetMap`；U11 VDD/MR 为 V5，U11-6 与 U8-4 同为 PWR5_OK，R_LDO_EN_PU 将其拉向 V5；D_DBG3-3 为 PGOOD、-5 为 PWR5_OK；U12-6 与 U7-6 同为 PGOOD | 实际不是 Pro 的直接共同 wired-AND 节点。按包内 BAT54XY 引脚语义，支路是 PGOOD → PWR5_OK 的候选低电源钳位路径。不能据此证明 NRST 保证为 LOW，更不能证明 EN 必定先于 VIN 掉电。回执第 9 行已经列为未批准 amendment，VOL/温度/延迟/反灌仍 HOLD。 |
| 12 个补偿 DNP 不可直接恢复 | `C_ACTUAL_ALL_PINS.csv` 的 R_COL_SENSE0..3、R_TIA_ISO0..3、C_TIA_HF0..3 每个两端均为空网且 NC=true；`RAW_NATIVE_BOM_FLAGS.json` 对应 12 个 no | 只是 12 个隔离占位符，未实现 Pro 要求的可恢复补偿位置。回执第 12 行明确承认，不可称“保留了可恢复网络”。直接 TIA 主拓扑的候选资格不等于正式批准删这 12 个器件。 |
| U12 及 VEX 料值例外 | `C_ACTUAL_BOM.csv:10-11,111-115`，`C_ACTUAL_ALL_PINS.csv:24-27,381-390`；build plan 中对应器件 | VEX 实际 18k/162k；U12 实际 10k+4.99k+1k+1k，后两颗为 1%。与回执第 10–11 行一致，不是准确单颗 17k。阈值、加载和启动不能被“名义比例相近”关闭。 |
| 材料、Ceff 与连接器 | 实际 BOM 中 D_FFC_ROW/COL 的缺失 maker 提示、保留双 DVDD 22uF；回执第 13–14 行与 GATES | TPD 供应商模板身份、MLCC Ceff、连接器和 FFC 机械配合未资格化；没有把模板电气匹配当成 TI 库存或完整材料认证。 |
| ERC / cold / drawing | `C_ERC.json` 的 warnings 仅 `{type:warn,count:772}`；`C_ACTUAL_WARM_AUDIT.json.auditDomain`；`EXECUTION_BUDGET.json.nativeIndependentCold=0`；`PDF_VISUAL_INSPECTION.md` | 772 条性质未知，不能推导“无新的 Important ERC”；391/391 只证明与候选 plan 的 warm 一致性。本次抽看实际 PDF PNG 第 1、5、6 页，确实稀疏、字体小、边距紧；不是独立可发布图纸。没有第二次 PDF 导出。 |

`PLAN_AND_LEDGER.md:10,16` 的 “same logical power qualification” 必须连同紧随其后的“未批准/未资格化”理解为设计意图，不是已证明等价。推荐在同一次文档披露中改为 “intended logical qualification, not demonstrated equivalent”；这是措辞澄清，不增加电气验证。

## 计数、范围与证据真实性

- 已读取 `PRO_C_POWER_RULING_FULL.md`、`C_NATIVE_BUILD_PLAN.json`、actual parts/net 与 pins、实际 BOM flags、warm audit、预算、gates、解析假设/CSV、primary source notes、PDF inspection、回执与 ledger。实际计数 115 structural / 103 populated / 12 DNP，与回执相符；103 不是 Pro 的约 88–94，也不是 83。回执正确写明差额，不应为了目标数量再删件。
- 主电源方向为 U9 → V5 → TPS7A3701 → V3V3；U11/U12 均保留，LDO 的 52.3k/30.1k、OVLO 的 34.8k/10k、外部 4.99k 与 1k 路径、100R bleed 有实际器件/网络佐证。这里只确认结构，不确认全部器件限值和动态行为。
- 解析 CSV 的 10 行明确标为 scalar analytic、conditional、HOLD。预算将其保守计入 OP/AC/PZ，但实际 SPICE=0、TRAN=0；没有把标量算式包装为启动、brownout、反灌或联锁瞬态。`ANALYTIC_POWER_BOUND_ASSUMPTIONS.md:5` 明确 OFF 边界排除外部 NRST push-pull-high，并把 3.6V 上限列为分析假设；因此它不能推广为任意 debugger/UART 的完全支持证明。
- 实际 native 仍包含历史 PCB；新 C 仅为原理图候选，不能把历史 176 件 PCB 与 103 件 C BOM 混称同一已同步板。公开派生文件不改变这点。
- budget 记载 session=2/2、save=6/6、PDF=1/1，cold=0，原生实施已 STOP。资料计费事件也坦承曾在读取后补记，不支持“所有事项一律事前扣费”的绝对叙述；现有 COMPLETE 回执没有声称所有资料都事前扣费。

## 明确拒绝判断的项目

不判断电源时序/反灌/二极管 VOL 的最坏情况是否合格；不重新核算 CSV 数值或引入新的 datasheet；不证明完整矩阵、≤1% 精度、≤0.2% 重复性、噪声、100 fps、PZ、全系统稳定性；不证明全部厂家 pin/footprint/MPN 真实性；不进行 cold-open、ERC 明细解释、PCB/机械/制造/采购/bench 认证；不把原始 `.eprj2` 打开来枚举账户信息；不审查其他工程；不认证尚未完成的公开附件上传、ZIP/manifest 或派生 native 重开结果。

最终处置：**BLOCKED_CANDIDATE_REVIEW_ONLY**。按上述已经报告的单次隐私处置及披露边界交付“诚实的阻断候选审查材料”，不能交付“accepted C circuit”。不得用本审查恢复任何 native/science 预算或开启第二次评审。
