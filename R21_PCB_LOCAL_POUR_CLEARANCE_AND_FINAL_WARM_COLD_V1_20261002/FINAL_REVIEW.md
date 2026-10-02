# R21 pour closure — fresh-context final review

审查范围仅为本目录现有证据；一次整包只读终审，未启动CAD、DRC、仿真、网页、Git或追加native操作。仅写本审查文件。

结论：按15号工程门，现有证据支持 PCB_ROUTING_COMPLETE / PCB_ELECTRICAL_CLOSURE / COLD_REOPEN PASS，PCB_REVIEW_READY=true。此结论不放行制造、采购、Gerber、bench或上电。下一只读manufacturing preflight仍为未批准申请。

## Findings

- Critical：0。
- Important（新增未解决阻断项）：0。
- Minor：1。SAVED_WARM_CAPTURE.json 与 COLD_CAPTURE_AND_NATIVE.json 的API netlist导出文字并非完全相同：解析JSON后唯一差异为 /components/gge83/props/Description 中 U+FFFD 替代字符的位置（温态“温��系数”，冷态“电��:75V”）。这是可读附件说明文字完整性限制；parts对象、原生ATTR、PAD_NET和电气网络均严格相同，不是器件值或连线漂移。不能把整个API netlist字符串称作严格相等，也不宜把该损坏Description直接作为制造物料描述。保留现有原始证据即可；不要求CAD重开、工具修复或额外审查。

## 已核实的证据

完整阅读15号裁定、完整receipt、GATES、预算、ENTRY/WARM/COLD审计、工程接受解释、原生DRC和开关session记录、actualFile及warm/cold差异、绘图说明与未批准下一申请；实际查看两个PNG。

1. AFTER_REBUILD_DRC 与 COLD_DRC 原始调用分别属于两个不同session，同一冻结项目/PCB；returncode=0、parsed.ok=true、value=[]。唯一save发生于重铺后DRC成功之后，saved=true；warm官方close早于cold open，两个官方close均成功。
2. 直接解析entry/warm/cold原始capture，三者均为176/550/514/107/36。所有parts逐对象相同；非派生原生LINE909、VIA297、COMPONENT、PAD_NET、ATTR、POUR4、规则、层等一致。DOCHEAD的client/time/version有正常会话元数据差异，不能声称全文/字节相等。
3. 独立遍历warm/cold原始POURED：4对象、215处数值差、最大2.1032064978498966e-12，无对象增删、结构差异。完整数据没有被舍入或过滤；rawPOUREDStrictEqual=false与工程consistent=true明确分开，原COLD_AUDIT PASS=false保留。15号允许正常派生fill变化；结合真实DRC与全部非派生铜一致，工程接受并未虚报严格浮点相等。本目录内不重新验证14号历史比对的外部证据，也不推断内部序列化机制。
4. 352个入口API owner差异均只改变libraryUuid，before/after精确对应记录的旧/新owner；去除该单字段后内容逐项一致，无实际device/footprint UUID/name漂移。
5. cold返回的actual File base64解码与落盘epro2逐字节一致：722159 bytes，SHA256 C2D53B0B6BB438D7C916BE24CB0B0D6AE5C7D884E7784EEFFED90E61505BEE6C。原始返回constructor=File/tag=[object File]。nativeFile的911LINE与actual909仅多已明示的两个0.1mil短段；未将其升级为硬门，未建议编辑。现有native差异记录保留完整POURED差异。
6. 两PNG可读，e307 Top/Inner1避让可见；图中及说明均限制为工程审阅，线宽/封装省略/圆弧近似已披露。它们不能替代制造图或实体电气验证。

## 执行控制与范围说明

实际预算copy1/session2/save1/captureaudit3/DRC2/exportBatch1/pourUpdate1在次数上限内；三条startup命令中的第一条parser拒绝且无sessionId，未误记为第三个已创建session。第三capture的原调用确实将cold全量capture和actualFile组合为一批。两PNG属于同一次只读绘图批次。

cold预扣失败后顺序编排仍执行DRC，是实际执行控制偏差，不因最终DRC成功而消失。预算与receipt已明确事后真实UTC debit，不回填、不追认例外；此终审不为该偏差补授权。它不改变原生DRC证据，也未导致新增设计修改或次数超额；终态禁止继续native操作，故不作为尚需本包修复的阻断项。

GUI退出情况依赖本包SESSION_GUI_LIFECYCLE记录；本次未重新查询应用状态。冻结外部源文件未访问，冻结hash保持声明只限本包记录；线上上传/固定commit/逐附件读取未在本次离线范围验证。receipt中未来发布措辞不得当作已完成发布证据。

无需再开PCB修正包。本审查不批准下一阶段；保持制造/bench未放行，提交既有完整工程证据和有界只读preflight申请即可。
