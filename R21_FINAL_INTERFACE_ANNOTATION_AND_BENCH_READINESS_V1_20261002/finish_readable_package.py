from pathlib import Path
import json,csv,datetime,hashlib
from PIL import Image,ImageDraw,ImageFont
import budget
P=Path(__file__).resolve().parent
def write(name,s): (P/name).write_text(s.strip()+'\n','utf8')
def dump(name,x): write(name,json.dumps(x,ensure_ascii=False,indent=2))
budget.phase('P2')
ports={'12779b16da5e734e':'J3-1','7c23c94841413d8d':'R_J3_1-1','65ab4b7410ddfd9b':'J4-1','570009efa2576382':'R_J4_1-1'}
attrs=[]
for line in (P/'FINAL_PAGE_5_SOURCE.txt').read_text('utf8').splitlines():
 if '||' not in line: continue
 try:
  head,body=line.split('||',1); h=json.loads(head); a=json.loads(body.rstrip('|'))
 except (ValueError,json.JSONDecodeError): continue
 if h.get('type')=='ATTR' and a.get('parentId') in ports and a.get('key')=='Name': attrs.append(dict(pin=ports[a['parentId']],attribute=h['id'],**a))
assert len(attrs)==4
dump('INTERFACE_LABEL_SOURCE_EVIDENCE.json',{'source':'FINAL_PAGE_5_SOURCE.txt','attributes':attrs,'visualObservation':'Four renamed interface arrows have no visible net-name text in final PDF page5 PNG. Source retains correct names. valueVisible=null retained; no causal API conclusion or further investigation.','nativeFurtherEdits':0})
dump('DRAWING_VISUAL_REVIEW.json',{'pagesRenderedAndActuallyViewed':6,'generalLayout':'default font, engineering content readable; inherited R2 annotations remain','page5NewInterfaceNetNamesPrinted':False,'missingPrintedNames':['J3-1 V3V3_EXT_SWD','R_J3_1-1 V3V3_EXT_SWD','J4-1 V3V3_EXT_UART','R_J4_1-1 V3V3_EXT_UART'],'standaloneDrawingRelease':False,'companionRequired':['DRAWING_ANNOTATION_ADDENDUM.md','INTERFACE_TOPOLOGY_COMPANION.md','INTERFACE_TOPOLOGY_COMPANION.png','FINAL_514_PIN_NET_CHECKS.csv'],'PDFExports':1,'noMoreNativeEdits':True})
g=json.loads((P/'GATES.json').read_text('utf8'));g.update(INTERFACE_NET_LABEL_DRAWING_HOLD=True,DRAWING_STANDALONE_RELEASE=False,DRAWING_COMPANION_REQUIRED=True);dump('GATES.json',g)
with (P/'INTERFACE_TOPOLOGY_COMPANION.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.writer(f);w.writerow(['external_pin','external_net','resistor_external_pin','MPN','resistance','board_pin','board_net','purpose'])
 w.writerow(['J3-1','V3V3_EXT_SWD','R_J3_1-1','RT0603BRD074K99L','4.99k 0.1%','R_J3_1-2','V3V3','SWD voltage sense; not power input'])
 w.writerow(['J4-1','V3V3_EXT_UART','R_J4_1-1','RT0603BRD074K99L','4.99k 0.1%','R_J4_1-2','V3V3','UART voltage sense; not power input'])
write('INTERFACE_TOPOLOGY_COMPANION.md','''# Actual interface topology companion — review only

This readable companion is required with final native/PDF. Page5 has four empty arrows without printed new net names; actual cold-reopened netlist has the correct independent networks. This companion does not alter or replace the native evidence.

```text
J3.1 -- V3V3_EXT_SWD  -- R_J3_1.1 [4.99k] R_J3_1.2 -- V3V3 (board)
J4.1 -- V3V3_EXT_UART -- R_J4_1.1 [4.99k] R_J4_1.2 -- V3V3 (board)
```

The external-side pins are different nets; there is no direct external-side connection. The two resistors share only their board-side V3V3. They are no longer two parallel resistors between the same pair of nets. This is a topology statement, not a measured fault-protection claim. J3.1 and J4.1 are voltage-sense interfaces, not power inputs or auxiliary power outputs.

| Cold actual net | Complete members |
|---|---|
| V3V3_EXT_SWD | J3-1, R_J3_1-1 |
| V3V3_EXT_UART | J4-1, R_J4_1-1 |

Both MPNs remain RT0603BRD074K99L /4.99k 0.1% /R0603; resistor pin2 remains V3V3. Exactly these four connected pins changed from09; remaining510, all36NC and176 core component dictionaries/coordinates unchanged. See FUNCTIONAL_INTERFACE_SPLIT_CHECK.json, FINAL_514_PIN_NET_CHECKS.csv, FINAL_107_NETWORK_MEMBERS.csv and COLD_REOPEN_COMPARE.json.

![Readable topology](INTERFACE_TOPOLOGY_COMPANION.png)

SWD signal-series resistors remain4.99k. Any later authorized bench session begins near100kHz SWD and records connection, voltage and waveforms before increasing clock. This package does not execute a bench session or authorize power/fabrication.
''')
im=Image.new('RGB',(1600,630),'white');d=ImageDraw.Draw(im)
font='C:/Windows/Fonts/segoeui.ttf';ft=ImageFont.truetype(font,31);fs=ImageFont.truetype(font,25)
d.text((45,25),'R2.1 actual cold-reopened interface topology',font=ft,fill='#15304d')
d.text((45,76),'Review companion only - final PDF page5 omits these four net labels',font=fs,fill='#8b3100')
for y,j,net,r in [(210,'J3.1','V3V3_EXT_SWD','R_J3_1'),(400,'J4.1','V3V3_EXT_UART','R_J4_1')]:
 d.text((45,y-60),j+'  voltage sense',font=ft,fill='#15304d');d.line((65,y,900,y),fill='#15304d',width=5)
 d.text((365,y-47),net,font=ft,fill='#15304d');d.rectangle((900,y-25,1100,y+25),outline='#15304d',width=4)
 d.text((905,y-68),r+'  4.99k',font=fs,fill='#15304d');d.text((865,y+36),'pin1',font=fs,fill='#15304d');d.text((1095,y+36),'pin2',font=fs,fill='#15304d')
 d.line((1100,y,1390,y),fill='#15304d',width=5)
d.line((1390,210,1390,400),fill='#15304d',width=5);d.text((1245,138),'V3V3 (board)',font=ft,fill='#15304d')
d.text((45,535),'External nets are separate; each has one 4.99k path to board V3V3.',font=ft,fill='#15304d')
d.text((45,581),'Not power inputs. No bench, fabrication or power release.',font=fs,fill='#8b3100');im.save(P/'INTERFACE_TOPOLOGY_COMPANION.png')
old=P.parent/'R21_NATIVE_PIN_NET_CORRECTION_AND_FINAL_DRAWING_V1'
add=(old/'DRAWING_ANNOTATION_ADDENDUM.md').read_text('utf8')
add=add.replace('两次Text.modify(content)返回saved true但实际source/PDF未变。','09的两次尝试未改变备注；10仅一次官方Text.modify(value)分组尝试加save返回true，实际source/PDF仍未变。没有继续研究API或重试。')
add+='''\n## 本次10的接口修正与PDF缺字\n\nJ3.1/R_J3_1.1实际为V3V3_EXT_SWD；J4.1/R_J4_1.1实际为V3V3_EXT_UART；两电阻pin2仍V3V3，各4.99k，外侧不共网。四新端口在最终PDF页5只显示空箭头，网名没有打印。INTERFACE_NET_LABEL_DRAWING_HOLD保留，不能称独立PDF完整终版。必须同时读取INTERFACE_TOPOLOGY_COMPANION.md/PNG/CSV及最终实际514针CSV。原生/File连接通过不等于图面文字修复。\n\nJ3.1/J4.1只作电压sense，不作供电输入；保留4.99k SWD信号串阻，后续明确获准的台架从约100kHz开始。正常1–7k、0.8–8k保护带；约10%变化验证基点不得使终点超正常域。所有300us、100fps、WCET、容量与故障指标均待实体证据。\n'''
write('DRAWING_ANNOTATION_ADDENDUM.md',add)
bench=(old/'BENCH_VALIDATION_PLAN.md').read_text('utf8').replace('514针CSV/BOM/PDF+备注补充','本包107网/514针CSV/BOM/PDF+备注补充+接口接线图')
bench+='''\n## 10号裁定接口输入合同（仅准备）\n\n- J3.1/J4.1为独立电压sense，不能从这些脚供电。核J3.1—R_J3_1.1为V3V3_EXT_SWD，J4.1—R_J4_1.1为V3V3_EXT_UART，两R pin2为板上V3V3；每条独立4.99k。\n- SWD仍含4.99k信号串阻；后续获准台架从约100kHz开始，先记录VTref/NRST、连接成功和波形，再决定提高时钟；失败先核接线与信号，不因本方案授权改阻值。\n- 正常1–7k，两点1k/6.8k校准后独立验证；0.8–8k仅保护带，7k+10%=7.7k不计正常域PASS。需同时记录全16点邻居和原码，不能仅报告变化点。\n- 300us残余/100fps/288传输32dummy256有效/WCET仍仅验收目标；输入冻结、探头负载/带宽/校准不确定度/时间戳/原始示波器和SPI证据须记录。\n- ERC细节未知、四端口缺字和旧备注均须随审核资料明示。实际bench、采购、PCB、制造和上电为0；本合同不是执行批准。\n'''
write('BENCH_VALIDATION_PLAN.md',bench)
budget.phase('P3')
write('COMPLETE_FINAL_INTERFACE_RECEIPT.md','''# 10号工程接口修正与台架输入审查回执

包：SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_ANNOTATION_AND_BENCH_READINESS_V1。仅此电路项目。结论：独立sense接口和真实冷重开连接通过；图面文字未完全通过，受控台架输入合同已准备，BENCH_NOT_RELEASED。

## 接受裁定与边界

完整裁定CIRCUIT-PRO-R21-FUNCTIONAL-NETLIST-REVIEW-AND-BENCH-READINESS-20261002-10，assistant c5423032-70c8-4d72-bcf3-62290be0b7b4，parentuser c612a0f2-8827-4c4d-b233-3d31c0314123，原文PRO_FINAL_INTERFACE_RULING_FULL.md。Pro对核心采集设计给出CORE_ACQUISITION_TOPOLOGY_REVIEW_PASS；本包不把该审查扩为实物动态/精度/故障PASS。

批准180min、唯一工程包：只拆J3/J4外侧共网，一次既有文字接口尝试，冷重开及台架输入准备。停止新增MIMO、descriptor、参考归一化、验证工具和API研究。实际bench/PCB/制造/采购/仿真/协议新回归全0。主拓扑、主值、正常1–7k约10%/0.8–8k保护带、4x4/8wire、5V+3V3/VCM2.5/VEXC2.25/E.25/Rf4.99k/Cf2.2nF/100fps冻结。

## 真实问题与最终拓扑

09实际V3V3_EXT共有J3-1、J4-1、R_J3_1-1、R_J4_1-1，两4.99k跨同一对节点，约2.495k并联，是接口设计问题。本次实际拆为：

| 网 | 完整成员 |
|---|---|
| V3V3_EXT_SWD | J3-1、R_J3_1-1 |
| V3V3_EXT_UART | J4-1、R_J4_1-1 |

两R pin2仍V3V3，MPN RT0603BRD074K99L、4.99k0.1%、R0603不变。外侧不直接共网，每条独立4.99k；不是实测保护结论。FUNCTIONAL_INTERFACE_SPLIT_CHECK.json记录恰好四针变化，其余510针/V3V3成员/176器件核心字段坐标/36NC不变。没有更改SWD4.99k信号阻值、NRST1k或ADC10nF。

## 原生实现和独立冷重开证据

09合格副本复制一次，原输入四文件最终SHA全PASS。四旧NetPort在删除前完成枚举，四新NetPort和自有stub网名更新，save1；温态实际File、完整source及全量成员审计为176parts/514of514/107nets/36NC PASS。之后一次notes尝试+save2，关前快照，再关闭温态会话，独立冷会话实际File/native/PDF合并一次捕获后关闭。

冷态同为176/514of514/107/36；全部网络成员、NC、核心字段与pin坐标温态—关前—冷态严格一致。最终两actualnet rawbytes本次也相等（217784bytes、SHA F883F0820AB4925FBE6CA86158C5CD98F8588B78EA7AC4B2B23D804538FEB7BB3）。不把旧09的仅顺序变化混称此证据。

温态工具File.text辅助字符串含replacement字符标志，raw实际File bytes按UTF8严格解码0 replacement；冷态辅助字符串与raw相同且0 replacement。以保存的原始File bytes为准，没有重编码修改证据。ACTUAL_FILE_TEXT_ENCODING_NOTE.json保留这个辅助解码差异，未研究工具。

两自有session d0b1b000-2114-491a-98af-9ffe4a377097、aa4e43f6-d45b-46f7-b8c4-86a4c744b31d均官方closed，无pending，本包从未启动solver。FINAL_SESSION_STATUS.json/CLOSE_A/CLOSE_COLD为证据。

## 图面与备注：真实限制，不继续卡主线

10仅一次既有官方Text.modify(value)分组尝试，随后save返回true；实际source和PDF旧R2标题/备注没有改变。value字段取自已捕获source（计划初写text字段按实际source纠正），没有第二次尝试、原因调查或API研究。ANNOTATION_SINGLE_ATTEMPT_RESULT.json保留原值、期望值、实际未生效。LEGACY_ANNOTATION_HOLD和MCU_INTERFACE_NOTES_UPDATED=false。

唯一六页PDF已实际render并逐页查看，默认字号、主体工程内容可读。新发现页5四个新端口只有空箭头，V3V3_EXT_SWD/UART网名未打印；source正确Name值存在，valueVisible=null仅记录，不推断API原因。INTERFACE_NET_LABEL_DRAWING_HOLD，DRAWING_STANDALONE_RELEASE=false。不能称最终独立PDF图面完全PASS。

硬额度已耗尽，没有为此再打开/修改/保存/导出。交付新增INTERFACE_TOPOLOGY_COMPANION.md/CSV/PNG、DRAWING_ANNOTATION_ADDENDUM.md与实际514针CSV，完整表达两条接线并校正NRST1k、300us仅理想筛查、8状态/288/32/256/真实100fps待验。补充是审查资料，不冒充原生/PDF文字已修复。

## 台架输入合同与保留门

BENCH_VALIDATION_PLAN.md只准备、不执行：sense口不是电源口；保留4.99k SWD信号阻，从约100kHz开始的后续受控连接检查；正常1–7k两点校准、约10%全16点变化与邻居；保护带不计正常PASS；300us残余及实际100fps/WCET需完整波形/时序/原码证据。限流值依实体条件后续落实，不虚构已测条件。

ERC本包0，继承旧warncount1209无正文，不能称ERC clean；ERC_DETAIL_HOLD、FAULT_PROTECTION_HOLD、REFERENCE_CAPACITANCE_BENCH_HOLD、HARDWARE_WCET_PENDING、SWD_SERIES_RESISTOR_BENCH_CHECK、BENCH_NOT_RELEASED保留。原生连接PASS与核心设计审查PASS不解除这些门。

## 实耗、停止及交付物

copy1/1、session2/2、save2/2、captureaudit2/2、PDF1/1；ERC/库/资料/候选/OP_AC/TRAN/PZ/MIMO/descriptor/reset解析/协议新回归全部0。EXECUTION_BUDGET.json记录实际原子预扣及阶段时间。STOP=NATIVE_EXECUTION_COMPLETE_HARD_QUOTAS_USED_NO_MORE_EDITS，旧余量不继承。工程科学工作结束，余下仅回执审查/公开上传/回复接续。

| 文件 | bytes | SHA256 |
|---|---:|---|
| SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_REVIEW.epro2 | 498276 | 2821A51AFCF9BB474D895B53AE6C514A9B4B637CC3016054356FA7E43F3A97E9 |
| SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_REVIEW.pdf | 625864 | AADA353138FE3E381695BF30530AA1B5D8CDFD1C52577F5712CEA538976BC584 |
| SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_WORK.eprj2 | 2084864 | 3EDFD3654E577164F8222146BF4E3B898E90BD392A06AF525B67A1BFB1A6FC37 |

原始actualFile/source/CLI/stdout/stderr/notes失败、514针/107网/36NC/176BOMCSV、六页PNG、独立冷检查、预算/门/原裁定与台架输入合同全部随源文件直接上传，另有manifest和完整ZIP。原生工程仅审查，不授权装配/制造/上电。

## 下一次集中裁定申请（用户明确要求更多有界预算）

请统一验收两层：主采集设计＋本次真实独立sense/cold实现，接受文字补充的工程范围，并确定唯一下一包。不要再次因旧文字或工具理论卡住主线。用户明确要求更多有界执行时间/次数/自主推进范围以减少小步骤请示；本次集中提出240min最终工程接收与台架输入合同收敛（图面接收45、只读台架准备75、交付60、预留60），普通文件/检查/资料整理本地自主。

优先接受现有图面补充后只读接收。若四个网名缺字必须进入原生才可验收，请只批准一个最小显字工程子项：新副本1/session2/save1/captureaudit2/PDF1；限既有NetPort Name显示属性一次，不改任何网/元件/主值，不研究API，失败保留补充立即交付。新ERC/库/资料/候选/所有仿真/解析/新协议/实际bench/PCB/制造/采购0；没有获批前不执行。该请求不扩模型平台额度或安全/科学门。

END-OF-COMPLETE-R21-FINAL-INTERFACE-ANNOTATION-AND-BENCH-READINESS-RECEIPT
''')
# Fix a transcription only in prose; raw evidence remains unchanged.
r=(P/'COMPLETE_FINAL_INTERFACE_RECEIPT.md').read_text('utf8').replace('F883F0820AB4925FBE6CA86158C5CD98F8588B78EA7AC4B2B23D804538FEB7BB3','F883F0820AB4925FBE6CA86158C5CD98F8588B78EA7AC4B2B23D804538FEB7BB3'.replace('B7BB3','B7B3'));write('COMPLETE_FINAL_INTERFACE_RECEIPT.md',r)
write('README.md','''# R2.1独立sense接口修正审查包

[完整回执](COMPLETE_FINAL_INTERFACE_RECEIPT.md) · [真实拓扑接线图](INTERFACE_TOPOLOGY_COMPANION.md) · [图纸备注补充](DRAWING_ANNOTATION_ADDENDUM.md) · [台架输入合同：未执行](BENCH_VALIDATION_PLAN.md)

实际176parts/514of514/107nets/36NC，独立冷重开PASS。仅四针由共网拆成SWD/UART两独立外侧sense，每条4.99k，510其他针及元件主值不变。CORE拓扑由10号Pro独立审查通过，不代表实物指标。

**最终PDF页5四个新端口网名未打印，旧R2备注也仍在；必须连同接线图和补充阅读。BENCH_NOT_RELEASED，禁止按此审查包装配制造上电。**

- 原生：SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_REVIEW.epro2；工作副本.eprj2；六页PDF与六PNG。
- 实际证据：FINAL_514_PIN_NET_CHECKS.csv、FINAL_107_NETWORK_MEMBERS.csv、FINAL_36_NC.csv、FINAL_176_BOM.csv、两actualnet、全页source。
- 结构复核：FUNCTIONAL_INTERFACE_SPLIT_CHECK.json、COLD_REOPEN_COMPARE.json、FINAL_COLD_AUDIT.json。
- 限制：GATES.json、DRAWING_VISUAL_REVIEW.json、ANNOTATION_SINGLE_ATTEMPT_RESULT.json、ACTUAL_FILE_TEXT_ENCODING_NOTE.json。
- 原裁定/计划/预算/闭会话/冻结源SHA与全部原CLI证据保留。

本包新仿真/新协议/实际bench/PCB/制造/采购0；原生硬额度已用尽，禁止自行继续修字。公开manifest逐文件SHA及ZIP用于完整性核对。
''')
print('Readable companion, truthful receipt, addendum and bench contract prepared; no native operations')
