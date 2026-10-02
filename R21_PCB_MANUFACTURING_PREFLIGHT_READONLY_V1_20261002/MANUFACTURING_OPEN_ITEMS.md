# 真正影响制造/装配的开放项
当前PCB_REVIEW_READY保持，制造release=false。已完成一次只读preflight，不循环重开已结束的PCB修正或理论包。

1. **PENDING_INPUT — 板厂、stackup与材料**：板厚/公差、外内铜厚、介质、finish、mask颜色及公差未定。6mil=.1524mm；厚铜可能不覆盖。需要一份匹配现有geometry的工艺合同。
2. **PENDING_INPUT — 小阻焊桥与钢网/land接受**：U9/U10最小估计约.090081mm，U5约.096774mm；当前pad扩展约.05mm。若选工艺要求至少.10mm桥，现有桥不能无条件PASS；请fab确认生产mask开口/是否允许合桥或更小桥及回流短路控制。未选供应商时不把自动CAM修正当已批准，也不直接认定全板须改。若供应商明确拒绝，集中提出最小mask/footprint ECO，不本包执行。
3. **PENDING_INPUT — 焊接流程**：RPW/DSE底部焊盘不可默认手焊可验；贴装、钢网厚度/开口、回流、检验方法未定。U5/U7/TPS land与manufacturer example非严格同，需assembler acceptance。
4. **PENDING_INPUT — J1–J4具体MPN/机械**：generic header有正确2.54mm pitch与原生1.0–1.2mm钻孔，但manufacturer/MPN为空；需针截面/镀层/配套插头/外壳/板厚配合和pin1接线表。不能据此下单。
5. **PENDING_INPUT — 装配留距、定位/拼板、丝印极性**：175 nominal body无相交≠完整courtyard/3D/toolspace合格；U6该body未覆盖。工艺边/fiducial/固定结构及生产丝印可见性待确认，本包不新增。
6. **PENDING_INPUT — 制造数据和授权**：未生成Gerber/drill/钢网/CPL/panel数据；其生成及板厂CAM审查需独立授权。没有订单、制造、上电或台架release。
7. **PENDING_INPUT — 实测准备实物**：已有13个可探pad候选，不缺点位证据；样机/仪器/探头/操作人员及安全上电合同仍缺。这个条目不否定PCB制造几何。

**ECO_REQUIRED：当前无已证实无条件必须修改铜/net/器件的项目。** 具体工艺若不接受细阻焊桥/land，才提交集中最小制造ECO建议；不回去修Description或历史PDF文字。旧annotation与LINE909/911差异不列为生产阻断。


用户本包明确问排线接口：现有J2只是单排8针2.54mm排针，不是已冻结的IDC排线座；成品双排IDC不能直接插。实际线缆/阵列端接口已在本聊天询问，等待用户输入。接线表见EXTERNAL_ARRAY_J2_WIRING.md。此项保持PENDING_INPUT；明确不兼容才提出最小接口ECO，不以电气数量PASS替代外部接入可用性。
