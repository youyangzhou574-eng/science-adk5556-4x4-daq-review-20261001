对，这个新阶段应该**正式替代旧22“直接进CAD重排”的路线**。现在先不碰原生PCB、不管现有铜怎么走，只把176个器件按真实封装和电气邻接关系排成两套完整的“无铜placement方案”，人工选完以后再进入一次真正的原生重排。

# CIRCUIT-PRO-R21-PLACEMENT-ONLY-TWO-CANDIDATES-20261002-23

批准唯一阶段：

## `SCIENCE_ADK5556_4X4_R21_PLACEMENT_ONLY_TWO_RECTANGULAR_CANDIDATES_V1`

**240 min，只做离线placement。**

旧22的“AutoLayout参考→直接重排→布线”不再执行；旧21的CONTACT文字/cold/export也暂不单独补，等选定placement后一起在最终原生实施包里闭合。

---

## 1. 本阶段输入怎么冻结

使用当前已保存FFC温态工程的真实器件数据作为placement authority：

- 176 components
- 552 pads
- 514 assigned
- 107 electrical nets
- 36普通NC
- J2额外2个mechanical unassigned pads
- J2 = `2005290081`
- 1–4 = ROW0–ROW3
- 5–8 = COL0–COL3
- MP1/MP2空网

**现有LINE/VIA/POUR全部不参与布局优化，也不绘制。**

100×90只作为背景参考，不是目标板框。

21号未保存的CONTACT文字也不作为placement输入；以后原生实施时重新补即可。

---

# 2. “先不管连线”具体是什么意思

你的想法对，但不能变成完全随机摆元件。

我们忽略：

- 现在铜怎么绕；
- 现在via在哪里；
- 旧线有多长。

但保留：

> **关键器件和它所属IC引脚之间的局部几何关系。**

换句话说，布局优化的约束对象从“旧铜线”换成“IC pin ↔ passive pad”。

---

## 3. 三档器件约束

### A级：局部锁定块

这些视为“超级器件”，整体搬、整体转可以，但内部不能为了填空被拉散：

**TIA每通道**

- U2对应运放pin
- R_COL_SENSE
- RF
- CF
- R_TIA_ISO
- C_TIA_HF

**ROW driver**

- U1
- 对应R_ISO
- R_ROW_FB
- C_ROW_HF

**VCM / VEXC**

- U3
- R_VCM/VEX相关反馈
- C_VCM_HF / C_VEX_HF
- REF相关关键件

**ADC**

- U5
- R_ADC/C_ADC
- REFIO
- REFCAP
- AVDD/DVDD贴身电容

**Power IC**

- U9/U10及输入输出电容

**MCU**

- U7与最贴身的电源去耦。

### 保持方法

不是看元件中心距，而是计算：

> **关键IC真实pad中心 → 对应无源器件最近相关pad中心的欧氏距离。**

每个关键pair保存：

`before_distance`

两个candidate都必须满足：

> **不得无理由劣于当前真实布局。**

最好保持或缩短。

如果某通道通过镜像/旋转排得更规整，可以镜像，但局部pin-pair距离仍作为约束。

---

### B级：模板化重复块

这些可以明显整理：

- 四路ADC RC
- 四路ROW无源件
- supervisor A/B
- reset/logic重复支路
- 部分保护件

要求形成：

- 同间距
- 同方向或规则镜像
- 行列纹理。

---

### C级：自由布局件

可以大胆为了板面规整重新排：

- 普通pull-up/down
- reset外围
- debug保护
- UART/SWD外围
- supervisor分压
- 普通逻辑
- 非关键bulk件。

这部分负责把大区“填完整”。

---

# 4. 两个正式candidate

不再搞AutoLayout第三套。

## Candidate A — 功能/操作优先

目标是：

> **信号流清楚、接口好插、功能区自然组成矩形。**

建议六区：

```text
┌─────────────────────────────────────────────┐
│ AFE / TIA       │ Excitation / Bias        │
│                 │                          │
├───── FFC ───────┼──────────────────────────┤
│ ROW / Sensor    │ ADC                      │
│                 │                          │
├─────────────────┼──────────────────────────┤
│ Power           │ Digital / Debug          │
└─────────────────────────────────────────────┘
```

重点：

- FFC必须在边缘；
- TIA和ROW占左侧大区；
- ADC居中；
- MCU/logic/debug形成一个完整右侧区域；
- Power形成底部或下侧连续区；
- 不追求各块面积完全一致。

这个方案更偏工程稳健。

---

## Candidate B — 矩形规整/视觉平衡优先

仍是相同6个功能区，但更强调：

- 大区边界对齐；
- 横纵基准线一致；
- 重复通道等距；
- 左右/上下视觉重量接近；
- 空白在整体包络内均匀分布。

例如：

```text
┌──────────────┬──────────────┐
│   TIA/AFE    │  Bias/Ref    │
├──────────────┼──────────────┤
│ FFC + ROW    │     ADC      │
├──────────────┼──────────────┤
│    Power     │ MCU/Digital  │
└──────────────┴──────────────┘
```

不是要求6块一样大，而是形成一个很明显的矩形整体。

如果为了“视觉对称”需要破坏A级局部距离，则Candidate B必须让步。

---

# 5. 板框这一步完全不定

两个方案都先排在“无限画布”概念里。

最后计算：

### A. Natural component envelope

真实器件/body摆完后的：

`xmin, xmax, ymin, ymax`

### B. Mechanical envelope

再加入：

- FFC插入空间；
- 翻盖开启空间；
- J1插拔；
- SWD/UART操作；
- 必要板边安全余量。

最后只输出：

> **Recommended enclosure / board envelope**

例如未来可能算出来是74×63、78×67之类。

但这包**不把任何数写回PCB板框**。

---

# 6. 不能只画“小方框”

这一点作为硬要求。

每套图必须用真实器件尺度：

优先级：

1. 已有原生footprint/body图形；
2. 已确认官方package/body尺寸；
3. 只有pad但body未资格的器件，画pad footprint并明显标：
   `BODY PROVISIONAL`
4. 没证据的不自行补厂家body。

尤其FFC必须区分：

- signal pads
- mechanical tabs
- 官方connector body
- actuator/opening方向
- cable insert keepout。

不能再拿assembly-artwork白框冒充厂家body。

---

# 7. 每套方案的完整交付

Candidate A、B各自必须有：

### `PLACEMENT_A.csv`
### `PLACEMENT_B.csv`

全部176个器件：

- Designator
- X
- Y
- Rotation
- Function block
- Constraint class A/B/C
- Body source
- Notes

不能只列20个功能块坐标。

还要有：

### 无铜PNG

- `PLACEMENT_A_NO_COPPER.png`
- `PLACEMENT_B_NO_COPPER.png`
- `PLACEMENT_AB_COMPARISON.png`

只显示：

- 器件真实尺度
- 位号或关键标签
- 功能区
- FFC方向
- 自然包络

**不显示trace/via/pour/ratsnest。**

---

# 8. 定量比较

两套都至少报告：

### 空间类

- natural bbox width/height
- body projected area / bbox area
- 六区面积比例
- 周边最大连续空白
- 4×4栅格占用均匀度

最后这个很适合衡量你说的：

> “是不是一边挤一边空”。

---

### 电气邻接类

只看placement，不看routing：

- TIA关键pin-passive距离
- ROW feedback距离
- VCM/VEX feedback距离
- ADC_IN RC距离
- REFIO/REFCAP距离
- power IC decoupling距离
- MCU decoupling距离

都列：

`before / A / B`

---

### 接口机械类

- FFC插入方向余量
- actuator opening 2D余量
- power/debug connector边缘可达性
- body overlap数量 = 0

---

# 9. 这一阶段不做什么

明确全0：

```text
CAD = 0
copy = 0
session = 0
save = 0
coordinate import = 0
DRC = 0
pour = 0
native export = 0
board outline edit = 0
routing = 0
simulation = 0
Gerber = 0
procurement/manufacturing = 0
bench/powerup = 0
```

也不再：

- 跑原生AutoLayout；
- 写新优化器；
- 安装插件；
- 迁移KiCad；
- 研究API/SDK；
- 拿旧铜长度作为目标函数。

---

# 10. 预算批准

批准你申请的 **240 min**：

- 外形/关键局部距离提取：60 min
- Candidate A/B完整176布局：90 min
- 几何/机械/取舍检查：45 min
- 可读图文 + GitHub固定commit：45 min

额度：

```text
formal candidates = 2
official sources <= 4，仅真正缺body尺寸时
geometry refinement <= 3 passes / candidate
final image exports <= 3
```

普通：

- 对齐
- 等距
- 旋转
- 功能区边界
- 白空间分配

在这个有界阶段内自行推进，不逐项回来问。

---

# 11. STOP条件

只有这些情况才停：

- 176 Designator无法完整映射；
- 真实footprint/body缺失到无法判断关键大器件占地；
- FFC官方body/actuator空间无法根据已有资料确定；
- 为形成矩形必须明显恶化A级关键局部距离；
- 两套方案都出现不可避免的器件body overlap。

非关键器件body资料缺失：

> 标`PROVISIONAL`继续，不开资料研究包。

---

# 12. 下一次进入原生CAD的门

这个placement包交回来以后，**不会自动实施**。

我们先一起看A/B。

只有你明确说：

> “用A”
>
> 或
>
> “B再按这里改一下，然后就用它”

才开下一包：

`PCB_NATIVE_REPLACEMENT_AND_REROUTING_V1`

那一包才允许：

- 真正搬176器件；
- 改板框；
- 删除旧铜；
- 重新布线；
- pour；
- CONTACT文字；
- warm/cold DRC；
- native epro2 export。

21号没闭合的cold/native问题也在那一次统一完成，不再单独处理。

---

所以现在路线正式改成：

**真实器件 → 两套纯placement → 人工选布局 → 反推板框 → 最后一次原生搬件+布线。**

这个顺序比之前合理得多，也最符合你现在真正关心的“板子本身看起来是不是一个完整、规整的产品”。
