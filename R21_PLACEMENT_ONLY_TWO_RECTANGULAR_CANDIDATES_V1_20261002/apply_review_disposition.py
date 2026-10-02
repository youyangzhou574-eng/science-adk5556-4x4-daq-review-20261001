from pathlib import Path
import json, shutil, datetime
P=Path(__file__).parent
for n in ('COMPLETE_PLACEMENT_RECEIPT.md','GATES.json','README.md','FINAL_ARTIFACT_VERIFICATION.json'):
    shutil.copyfile(P/n,P/('BEFORE_REVIEW_'+n))
p=P/'COMPLETE_PLACEMENT_RECEIPT.md';s=p.read_text(encoding='utf8')
s=s.replace('## 交付结果','## 交付结果\n\n**终审结论：本包完整接收 HOLD / STOP。以下两套图只作为未接收视觉草案。FFC body/actuator datum 尚未闭合，触及 Pro23 显式停止条件；关键距离 coverage 和全局 pad proxy 检查也未闭合。不得因选定 A/B 就解除门，不能称 Pro23 全要求通过。唯一终审 Critical0 / Important3 / Minor2，全文 FINAL_REVIEW.md；本轮只作一次证据范围与门状态修订，不重算、不改图、不增加 CAD。**')
s=s.replace('| body overlap / 保守pad包络overlap | 0 / 0 | 0 / 0 |','| body overlap（已有模型）/ pad proxy子集结果 | 0 / 部分组合0，完整性UNKNOWN | 0 / 部分组合0，完整性UNKNOWN |')
s=s.replace('| 1mm采样最大空白矩形面积/mm² |','| 全bbox内1mm中心采样空白proxy/mm²，非周边连续空白 |')
s=s.replace('两方案保守开盖/插线2D访问包络内无其它器件body；','两方案自定义规划开盖/插线2D区域内无其它器件body；该区域未证明包含实际翻盖全开扫掠，不能解除本阶段FFC STOP。')
s=s.replace('74pair before/A/B全表见KEY_PIN_DISTANCE_COMPARISON.csv；','已列出的74pair before/A/B全表见KEY_PIN_DISTANCE_COMPARISON.csv；该表不是完整关键邻接 coverage。U9_IN_CAP/U9_OUT_CAP/U10_IN_CAP/U10_OUT_CAP因位号筛选遗漏，RF0–3/CF0–3经串联件关联而不满足直接同网筛选，也未列出。它们按坐标生成仍在刚性块，但未补算指定pad距离；详见REVIEW_DISPOSITION.md与KEY_CONSTRAINT_COVERAGE_GAPS.csv。')
s=s.replace('A第二遍0，B第二遍0，B第三遍仅重整下部控制件，0。','A第二遍body0，B第二遍body0，B第三遍仅重整下部控制件、body0。pad proxy报告零为不完整遍历子集：groups为块名→位号列表，却用groups.get(ref)判断同块，跨块可能None==None被跳过。原始结果保留，不回填全局PASS，不据此推断存在实际碰撞。')
s=s.replace('冻结4个输入文件SHA末次全不变；','冻结4个输入文件SHA末次全不变；源脚本另从旧CANDIDATE_B_PLAN.json读取membership，未纳入该四项SHA清单；本包保存了派生CONSTRAINT_BLOCKS和候选membership，但原样再生成输入冻结不完整，见终审M2。')
s=s.replace('当前交的是带机械限制的placement人工选择包，GATES表明CAD_RELEASED=false / userSelectionRequired=true。请用户与Pro看A/B，选定后再给一次有界原生搬件+新板框+重布线+warm/cold/实际epro2的统一阶段。FFC精确body注册、通用header匹配壳体、真实插拔/装配条件在原生机械准备中仍须明确，不能由本次几何空白代替。','当前交的是Pro23停止门下的A/B未接收视觉草案与完整阻断回执。GATES表明PLACEMENT_ACCEPTED=false / CAD_RELEASED=false；视觉偏好可以先讨论，但不等于完整布局接收。请Pro集中裁定FFC机械资料限据及两项关键检查缺口的有界闭合或明确工程接收路线；不继续修工具研究、不重开旧21。只有新统一范围成立才能补证或原生实施，不能由几何空白代替真实插拔条件。')
s=s.replace('必须先有人选A/B且下一统一工程范围成立。','必须先裁定本次STOP和缺项、有人选A/B且下一统一工程范围成立；此次480min建议是上限申请，不是默认展开验证工具研究。')
p.write_text(s,encoding='utf8')
g=json.loads((P/'GATES.json').read_text(encoding='utf8'));g.update(stage='PLACEMENT_VISUAL_DRAFTS_COMPLETE_ACCEPTANCE_BLOCKED',scienceSTOP='FFC_BODY_ACTUATOR_DATUM_UNCLOSED_PRO23_STOP',PLACEMENT_ACCEPTED=False,KEY_DISTANCE_FULL_COVERAGE_HOLD=True,PAD_PROXY_FULL_COVERAGE_HOLD=True,PERIPHERAL_CONTINUOUS_BLANK_METRIC_HOLD=True,REPRODUCTION_INPUT_FREEZE_INCOMPLETE=True)
g['geometryOverlapAudit']['A_padProxy']='PARTIAL_COVERAGE_ZERO_NOT_GLOBAL_PASS';g['geometryOverlapAudit']['B_padProxy']='PARTIAL_COVERAGE_ZERO_NOT_GLOBAL_PASS';g['keyDistancesMaintained']='ONLY_LISTED_74_PAIRS_TRUE_FULL_REQUIRED_COVERAGE_UNCLOSED'
(P/'GATES.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf8')
b=json.loads((P/'EXECUTION_BUDGET.json').read_text(encoding='utf8'));b.update(status='BLOCKED_RECEIPT_COMPLETE_NO_MORE_GEOMETRY_OR_IMAGES',stopUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),stopReason=g['scienceSTOP'])
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf8')
(P/'KEY_CONSTRAINT_COVERAGE_GAPS.csv').write_text('required_parts,function,evidence_in_current_package,missing_evidence,status\nU9_IN_CAP;U9_OUT_CAP;U10_IN_CAP;U10_OUT_CAP,power input/output capacitors,rigid block coordinate construction,actual IC-pad to cap-pad before A B distance rows,HOLD\nRF0;RF1;RF2;RF3;CF0;CF1;CF2;CF3,TIA feedback network,rigid block coordinate construction,functionally associated pad pairs through series elements,HOLD\n',encoding='utf8')
(P/'REVIEW_DISPOSITION.md').write_text('''# 唯一终审一次文档修订

Critical0 / Important3 / Minor2。I1–I3均保留技术HOLD，不虚报修复：FFC完整body/actuator datum缺口触及Pro23 STOP；74pairs只限已列74项、power caps和RF/CF缺项列入CSV；pad proxy字典使用错误导致跨块组合漏检，全局UNKNOWN。body检查不受该跳过影响，原模型body0可限据保留。

Minor M1：最大空白仅全bbox中心采样proxy，不是周边连续空白；ceil边缘可能越界。Minor M2：额外旧membership文件未入四项输入hash，派生块保留，重生成冻结不完整。

本次只修改接收门和证据范围，保存BEFORE_REVIEW原文/门/README/核验。全部坐标、三图、原几何结果与失败不变；没有代码补算、几何第四轮、第四次图片导出、CAD或第二review。source仍保留已发现错误以保留实际生成依据，禁止将原脚本当已修完整检查器继续使用。
''',encoding='utf8')
r=P/'README.md';r.write_text('# Pro23 A/B未接收视觉草案：完整接收HOLD\n\nFFC body/actuator datum STOP；关键距离与pad proxy完整覆盖未闭合。详见COMPLETE_PLACEMENT_RECEIPT.md、FINAL_REVIEW.md、REVIEW_DISPOSITION.md及GATES.json。三图和176器件坐标可供视觉讨论，不是已实施PCB。\n\n'+r.read_text(encoding='utf8'),encoding='utf8')
v=P/'FINAL_ARTIFACT_VERIFICATION.json';j=json.loads(v.read_text(encoding='utf8'));j['reviewDisposition']='Prior structural verification preserved; pad global and key full coverage NOT QUALIFIED. No recomputation. See FINAL_REVIEW and GATES.';v.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf8')
t=P/'prepare_github_delivery.py';s=t.read_text(encoding='utf8').replace('# Latest: Pro23 two placement-only candidates; choose before native implementation','# Latest: Pro23 A/B visual drafts; placement acceptance BLOCKED').replace('Candidate selection and new approved native rerouting phase required before board changes.','FFC body/actuator datum STOP, key-distance full coverage and pad-proxy full coverage HOLD; drawings are unaccepted visual drafts. Choosing A/B does not release these gates. New unified bounded ruling required before further geometry or board changes.');t.write_text(s,encoding='utf8')
print('One report/gate disposition complete; original images/coordinates retained, no recomputation.')
