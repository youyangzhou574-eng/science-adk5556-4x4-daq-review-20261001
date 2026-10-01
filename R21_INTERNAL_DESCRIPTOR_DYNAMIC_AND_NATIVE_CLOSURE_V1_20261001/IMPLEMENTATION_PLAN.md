# Internal descriptor qualification implementation plan

> Agentic workers: executing-plans inline; TDD and one final fresh-context review. Existing explicit continuous user technical authorization and approved07 design override repeated design approval/localGit skill steps; no localGit/checkpoint or deleted evidence.

**Goal:** 专用完整宏模型MNA extractor与内部pole证书，资格后六七宏短窗，全部门通过才条件原生。
**Spec:** PRO_DESCRIPTOR_RULING_FULL.md，assistant104a4b67-268e-428d-b069-1490441ec58a。
**Architecture:** 原厂model层级flatten保留source行/instance路径；真正OP各内部节点/voltage branch作工作点；R/C/V/I/E/G/H/S及原模型实际VALUE/IF/LIMIT/TABLE/PWR解析Jacobians组成sE−A，保留全部内部动态，不minimal reduction。先局部fixture/AC对照，finite/infinite staircase稳定后才全网，任何真实primitive无法正确线性化即HOLD。
**Tech:** 既有Python/NumPy/SciPy/ngspice47，原模型SHA不变，-n -D ngbehavior=psa，无安装/新执行器。

## Global constraints

- 480min，P0/P1/P2/P3/P4分别150/120/100/80/30。全局与phase分别计时，stickySTOP不靠余量解除。
- actualOP/AC/PZ192；offline/descriptor diagnostic48，含失败/重放，实际求解同步扣各分析；normalTRAN64/full-long1≤8min/reset96/protocol48/source8/candidate2。
- native copy1/session2/save8/captureaudit4/ERC2/PDF2，未通过descriptor/full内部/数值不变性/七宏动态和既有RESET/protocol门之前全0。
- frozen4x4/8线800–8000Ω、E.25/Rf4.99k/Cf2.2nF/100fps、OPA模型，禁止第三补偿扫描/PCB/bench/Git/system。
- P0局部资格OP/AC由07§6/20明确授权；§15禁止的是未资格前新全网端口AC。保留此解释，不将局部资格变成全网数据权限。
- 独立source节点、全部内部branch保留；switch不可微/边界不挑导数；不忽略unsupportedprimitive；只有完整staircase结构资格后才能有限QZ认证。

## Review focus

- subckt局部model与参数作用域、含+/-节点名、续行回指。
- V/I方向与E/H约束符号，capacitor全MNA stamp、hidden内部变量不能删除。
- IF/LIMIT/TABLE激活分支和boundary；PSpice VSWITCH compatibility是否与固定Ron/Roff假设一致。
- 高指数descriptor不能用简单rankE当finitecount，尺度不变性与near-axis保守分类。
- 来源/工作点/实际分析原子预算、AC精确频点与nearzero floor范围不能虚报。

## Task1 extractor and local qualification (P0)

Files: spice_flatten.py/expression.py/mna.py/descriptor.py/test_*.py/cases/results/evidence。
- [ ] TDD实现数值单位、层级params/flatmapping；实际模型primitive完整inventory。
- [ ] TDD标准R/C/V/I/E/G/H/behaviorstamp、sourceJacobian/source源行映射；非光滑boundaryHOLD。
- [ ] 解析RC/controlledfeedback/algebraicconstraint/stable-unstable/hidden fixture真实有限pole与infinite结构对照；纯数学diag逐case计。
- [ ] 真ngspice follower/ROW/loadedTIA/VCM-VEXC/4macro exact12freq+交越采样对照≤.2%/1%/.5deg；任何primitive失败必须保存OP/原表达式/对照/原因并STOP。
- [ ] regularity/finite-infinite staircase门与AC资格门都真PASS才进入P1。

## Conditional downstream

- [ ] Task2 P1四真实状态D0-D3 full/reference同维descriptor；删跨block primitiveJacobian互项保留自项，FULL_TO_REFERENCE_STAMP_DIFF.csv回指；finitepoles τ=1e-7max(1,|λ|)/condition/等价scale维数不变。
- [ ] 正确characteristicfinite determinant比的真RHP弧/原点/增大R独立crosscheck；数值crosscheckHOLD按07非独立硬门，内部证书不可绕过。
- [ ] Task3 P2六七宏3us→353us，300us之后≤100uV/无增长/削顶，RESET/protocol有限收口。
- [ ] Task4 P3最小ECO/冷重开/audit/ERC/PDF仅全部硬门PASS，旧master/旧native不改。
- [ ] Task5 P4完整或阻断报告/可读附件/固定公开GitHubcommit/一次摘要send，送达历史、回复owner+nextCheck+接续monitor。

No path uses port-only第五/第六归一化。遇到真正无法支持/资格的primitive保存失败，STOP后不继续实际SPICE。
