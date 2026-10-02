from pathlib import Path
import json,datetime,hashlib
P=Path(__file__).parent;a=json.loads((P/'FINAL_EVIDENCE_AUDIT.json').read_text('utf8'));b=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
# Hash local preserved original, without rewriting it or publishing an account database.
a['savedLocalProjectSHA256']=sha(P/'SCIENCE_ADK5556_4X4_R21_J2_FFC_WORK.eprj2');(P/'FINAL_EVIDENCE_AUDIT.json').write_text(json.dumps(a,indent=2),'utf8')
b['finishedUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();b['elapsedMinutes']=round((datetime.datetime.fromisoformat(b['finishedUTC'])-datetime.datetime.fromisoformat(b['startUTC'])).total_seconds()/60,3);assert b['elapsedMinutes']<240
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),'utf8')
receipt=f'''# COMPLETE Pro20 J2 FFC/FPC interface correction — warm implementation, cold closure blocked

本次已经将温态J2改为用户要的**8芯薄软排线翻盖/ZIF插槽**。真实温态176器件/552pads/514assigned/107nets/36普通NC+2机械空网，8个信号顺序正确、其他175器件完整字典及pad-net/坐标不变；warm Connection/Short/Clearance/NetlistError全部0。**独立cold证据、实际epro2导出和原生接触面文字未完成，PCB_REVIEW_READY=false**。本包是完整真实阻断回执，不能称最终FFC原生工程合格，不能制造或上电。

## 需求和授权

包SCIENCE_ADK5556_4X4_R21_J2_FFC_FPC_INTERFACE_CORRECTION_V1，R20 assistant e6a49512-c971-43fa-ba72-ce9cfaea120a/parentuser6f5fedf6-4c30-442b-b4c0-10bdb7a52b69，完整PRO_FFC_ECO_RULING_FULL.md。用户原文“不是这个8针 是那种排线的插槽 你搜一下pcb软排线转接口”，照片后答“对”，只确认类型。Molex2005290081+154670229的8P1mm成套是Pro20授权默认，不冒称用户已回答1mm、无现成线材或实物匹配。

旧17/18/19 KK2541718560008+22012087合同保留历史并superseded；原电气验证历史不改写，新接口不继承旧KK制造就绪结论。原正常1–7kΩ约10%变化/0.8–8k保护带、4×4/8线和主电路主值不变。

## P0 官方来源和机械范围

4个逻辑官方来源：Molex2005290081 exact产品页，2005290002/2005291002PSD000revB2024-05-29五页drawingbundle（URL0061，表明确0081）；154670229 exact产品页及154670001PSD000revA2023-04-04。OFFICIAL_SOURCE_INDEX.json逐项URL/bytes/SHA。完整原PDF/HTML/长extract及全页render仅本地保留，公开自己的摘要/官方链接和hash；不冒称第三方全文全上传。初Python网络超时、nodefetch成功及失败回执保留，不改系统网络/代理。

8P1mm、FrontFlip、bottom-contact、SMT；signal0.4×1.0mm/1mm pitch，fitting nails2×1.3mm、中心±6.3mm/向前2.7mm，厂家8P A13.2/B7.0/C11.6mm。闭合高度1.9±0.2，打开约3.95mm。默认线8芯/TypeA同面/102±3mm/加强厚0.30±0.05；厂家注明配200529系列。线暴露3.5±0.5对座推荐±0.3仍需供应商全公差确认，未虚报制造资格。

温态J2信号行x6.5/y39mm，90°，Pin1在y35.5、Pin8y42.5。厂家body外形5.3mm深/13.2宽，但相对信号焊盘的body datum没有资格。原图误称保守x1.2..6.5框，实际native assembly artwork局部y−0.5..4.8经90°转到x1.7..7.0，原框漏右0.5mm；一次终审已降格为位置未核准的示意框，原图BEFORE_REVIEW保留，body datum/邻件机械检查HOLD。板框100×90不动；从左边水平插入、导体朝PCB。实际pad坐标支持电气布局审查，不能以图框证明body不越板边/邻件/翻盖，actual enclosure/full mated3D/翻盖全扫掠没有验证。两图是实际warm源重建，含简化绘字/2D body envelope，不是CAD截图/真实装配照/3D/制造图。

## P1 温态实现与边界

仅一自有副本，工作文件本地SCIENCE_ADK5556_4X4_R21_J2_FFC_WORK.eprj2。J2 PCB/SC Name和manufacturerId实际2005290081；通用设备HDR和FP旧KK元数据仍存在，不以它们证明准确catalog器件。八新Top SMT signal+两个Top机械焊片，均无孔；MP1/MP2真实空网不接GND，552不能凑550。

其他175器件完整字典/坐标/pad-net、非J2 schematic、rules/layers全相同；899原有main LINE记录、297旧VIA、4POUR边界逐项相同。只截短7个J2 terminal lead-in至x450mil边界、删3个local lead-in，加23local6milLINE和8hole12/diam24milVIA，保留7旧远端/net/layer/width，切点旧直线残差最大{a['maxCutPointYResidualMil']:.12g}mil（浮点运算非rawbytes相等）。新增铜都在J2局部，非J2主模拟铜未重新布线。929实际LINE/305VIA，4正常POURED派生改变，不能声称整块派生填铜bytes冻结。

一次官方GUI Tools→Pour Manager→Rebuild All，4原边界/network/priority未改。首次warmDRC报告NetlistError1；GUI导入变更预览仅J2 FFC Cable属性一条，应用该属性后FFC_WARM_DRC_02实返回ok=true/value=[]。不是发现电路短路或ROW/COL错接。之后一次GUI Save All，星标消失；保存动作真实，但独立持久化读回未资格。

封装初始工作source含6字符串，finalize source实际只有J2、1、ROW、COL、FFC INSERT五个。CONTACT PCB缺失，旧Footprint ATTR和D3_ATTRIBUTE仍在，尽管setter返回true、FPtab显示新name。PCB旧3D其他属性清空不等封装D3删净。保留这两份真实源和失败事实；不把true当实际更改成功、不追查API、不以companion替代20号原生接触面要求。

## P2 冷态失败和执行偏差

温态session092e9f5a-1bbb-487c-af46-1cf0675c22d9官方closed。随后Alt_L+F4没有真正关闭GUI，立即list仍旧window50594452；执行者未先确认空窗口就启cold，coldsession6dd33def-779b-4dd7-a5a6-7c5a4419bda1/render2，后核有第二window124587128。**独立cold前置未落实，这是本地执行偏差**，不甩给软件或研究工具原因。

FFC_COLD_DRC与FFC_COLD_DRC_READY均返回EXECUTION_ERROR“指定的主题消息在对应的画布内没有相关订阅”，没有DRC数值。最后FFC_COLD_FULL_NATIVE返回“获取所有器件失败”，未到getProjectFile，实际epro2=0。第二次失败前GUI可见载入，然而曾操作的是旧window；根因未确认，不能称重开已经正确。上述DRC2/capture1/export1预扣完整保留，不把调用报错解释为send失败/物理错误或全0。

最后通过实际窗口X按钮正常关闭两项目及应用、两session官方closed；FINAL_OWN_GUI_STATE.json fresh windows=[]。无本包solver，从未启动仿真。下次必须先空窗口确证，再只操作fresh返回的新window，做一次正常原生DRC/导出；不是升级证明或修执行器。

## 预算、STOP与冻结

240min，实耗sources4/candidate1/copy1/session2/save3/captureaudit4/DRC4/export1/normalPour1。capture4内3实际full warm、1cold失败；DRC4内2warm结果、2cold失败；export1为未达到File的保守预扣，成功File0。全部原生硬额满；elapsed{b['elapsedMinutes']}min。旧warm-close误命令close被拒、正确session close随后成功，不新增session，不回写失败。

STOP_COLD_CAPTURE_DRC_EXPORT_UNVERIFIED_HARD_QUOTAS_USED。没有再CAD/edit/pour/analysis。Gerber/采购/制造/bench/上电/本地Git/system/新库资料之外范围全部0，旧17输入eprj2/epro2 SHA未变。旧性能/供电/容量/WCET/实物故障/CAM/外壳等HOLD继续，不因warmDRC0提升为制造可靠性PASS。

一次fresh-context whole-package终审Critical0/Important1/Minor2；Important框包络过度声称一次文档修复降格HOLD，Minor预扣reason意图/浮点措辞作账说明，不二次review/科学重算。

本地工作文件SHA {a['savedLocalProjectSHA256']}，SQLite只读发现非空users.password及账户字段，未输出值、不修改库，原文件**不进入公开GitHub或ZIP**。没有标准epro2成功导出，因此不能交一个账户SQLite冒充安全原生导出。公开完整own源与可读证据；原工程完整留本地，明确缺真实epro2。

## 交付清单与下一唯一包申请

[全552 pad-net](ACTUAL_552_PAD_NET.csv)、[J2实际10pad](J2_ACTUAL_SIGNAL_AND_MECHANICAL_PADS.csv)、[原生五字符串](J2_NATIVE_SILK.csv)、[局部边界](LOCAL_BOUNDARY_MAIN_SEGMENT_CHECK.csv)、[完整审计](FINAL_EVIDENCE_AUDIT.json)、[GATES](GATES.json)、[budget](EXECUTION_BUDGET.json)、[全板可读图](PCB_FINAL_WARM_REVIEW.png)、[J2局部图](J2_FFC_ACTUAL_WARM_DETAIL.png)，以及六接口/制造合同。完整warm来源、原case脚本、所有失败CLI stdout/stderr/json及官方sourcehash保留。ZIP只包含公开许可的own文件，排原账户工程及第三方bulk，不是“全原始文件无排除”。

按**用户明确要求更多有界执行时间、次数和自主推进范围**，在此次正常报告集中申请唯一180min **R21_J2_FFC_FINAL_LOCAL_LABEL_AND_GUI_COLD_CLOSURE_V1**：已知正常编辑CONTACT侧文字/旧3D及名称40、真正全关后的正常GUI冷态DRC/原生导出60、审阅交付80；copy0/session2/save2/capture3/DRC2/export1/pour0/sources0/candidate0。禁止LINE/VIA/网/值/规则/主电路/板框变化0，不重做20包或工具研究。普通实现范围内自主，不逐小步请示；未完整新裁定不执行，旧剩候选额不继承。本请求不是扩大模型平台额度，制造采购bench仍0。

完整GitHub本次新目录/固定commit一次性交付；每个send有owner本聊天、nextCheck与接续monitor，消息历史暂旧/读取超时不当send失败，不重发。网页逐附件已读未验证、不设额外ACK门。

END-OF-COMPLETE-R21-J2-FFC-FPC-WARM-IMPLEMENTED-COLD-BLOCKED-RECEIPT
'''
(P/'COMPLETE_FFC_CORRECTION_RECEIPT.md').write_text(receipt,'utf8')
(P/'README.md').write_text('''# Pro20: J2 FFC/FPC warm implementation, cold closure blocked

[Complete receipt](COMPLETE_FFC_CORRECTION_RECEIPT.md) · [Final evidence](FINAL_EVIDENCE_AUDIT.json) · [Gates](GATES.json) · [Budget](EXECUTION_BUDGET.json).

User wants an 8-core thin ribbon ZIF slot. Warm actual 176/552/514/107/36+2 mechanical, DRC0. Cold qualification and safe native epro2 export failed; CONTACT-side native text missing, legacy library/3D metadata remains. Review evidence only, PCB_REVIEW_READY=false. No manufacturing/powerup.

![Actual warm local detail](J2_FFC_ACTUAL_WARM_DETAIL.png)

[Connector spec](J2_FFC_FPC_CONNECTOR_SPEC.md) · [Cable spec](J2_FFC_CABLE_SPEC.md) · [Pinout/orientation](J2_PINOUT_AND_ORIENTATION.md) · [Actual 10 pads](J2_ACTUAL_SIGNAL_AND_MECHANICAL_PADS.csv) · [Fab contract](FABRICATION_INPUT_CONTRACT.md) · [Open items](MANUFACTURING_OPEN_ITEMS.md) · [Failure/next scope](CLOSURE_FAILURE_AND_NEXT_SCOPE.md) · [Official sources](OFFICIAL_SOURCE_INDEX.json).

Images reconstructed from warm native source, not 3D or cold evidence. Local .eprj2 account database excluded from public files; full third-party documents excluded, official links+SHA retained. Native work file preserved locally without modification.
''','utf8')
print(json.dumps({'receiptBytes':len(receipt.encode()),'elapsedMinutes':b['elapsedMinutes'],'nativeFileSuccess':0,'publicRawDB':False}))
