from pathlib import Path
import json, collections, datetime, hashlib
P = Path(__file__).resolve().parent
def read(n): return json.loads((P/n).read_text('utf8'))
def write(n,v): (P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf8')
warm=read('PCB_FINAL_WARM_CAPTURE.json')['parsed']['value']
cold=read('PCB_FINAL_COLD_CAPTURE.json')['parsed']['value']
def records(src):
    out=[]; types=collections.Counter()
    for line in src.splitlines():
        z=line.split('||')
        if len(z)!=2: continue
        h=json.loads(z[0]); b=json.loads(z[1].rstrip('|'))
        if h['type']=='DOCHEAD': continue
        types[h['type']]+=1
        out.append(json.dumps([h,b],sort_keys=True,ensure_ascii=False))
    return collections.Counter(out), dict(types)
a,types=records(warm['source']); b,ctypes=records(cold['source'])
assert a==b and types==ctypes
assert warm['parts']==cold['parts']
write('WARM_COLD_FULL_RECORD_FIXPASS.json',{'allNonDOCHEADRecordsEqual':True,'recordTypes':types,'allPartsAndPadsEqual':True,'rawSourceBytesEqual':False,'scope':'offline document evidence only; no EDA call; corrects PAD/POLYLINE omission in historical helper','historicalHelperRetained':True})
q=read('EXECUTION_BUDGET.json'); final=read('FINAL_ALL_SESSIONS.json')
assert not any(o['label']=='FINAL_ALL_SESSIONS' for o in q['operations'])
q['operations'].append({'label':'FINAL_ALL_SESSIONS','kind':final['command'][1],'startUTC':final['started_utc'],'ok':final['parsed']['ok'],'error':final['parsed'].get('error'),'timeout':final.get('outer_timeout',False)})
q['counts']['session']+=1
q['counts']['createdHeadlessSessions']=4
q['counts']['officialCommandRecords']=len(q['operations'])
q['nonCommandAttempts']=[
 {'label':'CREATE_BATCH_00_PRELAUNCH','kind':'prelaunch','error':'WinError 206 command length','childProcessesStarted':0,'timestampExact':'NOT_RECORDED','source':'retained failure receipt and empty CREATE_BATCH_00 stdout/stderr'},
 {'label':'CLEARANCE_STATIC_ASSERTION','kind':'offline helper attempt','error':'wrong vertical-segment assumption; assertion before mutation','EDAProcessesStarted':0,'timestampExact':'NOT_RECORDED','source':'retained failure receipt'},
 {'label':'FIX_CLEARANCE_MISSING_CODE_FILE','kind':'prelaunch','error':'missing code file before CLI child launch','childProcessesStarted':0,'timestampExact':'NOT_RECORDED','source':'session summary; not reconstructing absent exact traceback'}]
q['finalDocumentSnapshotUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat()
q['snapshotScope']='Native stop time retained; final native list + read-only review/document pass included. Publication lifecycle recorded separately in delivery directory.'
write('EXECUTION_BUDGET.json',q)
request='用户新增要求：下次向网页端报告时，请同时申请更多的工作预算，包括适合当前项目的执行时间、计算或试验次数及自主推进范围，说明所需额度与用途，以减少反复请示。明确注明这是用户提出的要求。此次只在下一次正常报告中申请，不单独追加一次报告；获批前仍遵守当前预算和停止条件。'
write('USER_BOUNDED_BUDGET_REQUEST_SOURCE.json',{'source':'direct user message in local chat 01a0ecae-ab07-7010-aae5-f49da19c75dc','exactUserText':request,'thisPackageApprovalSource':'PRO_PCB_RULING_FULL.md + USER_PCB_AUTHORIZATION.json','nextRequestApproved':False})
receipt='''# R2.1 PCB 布局和局部布线阻断审查回执

本包：SCIENCE_ADK5556_4X4_R21_PCB_FLOORPLAN_AND_LAYOUT_V1。

当前完成的是可审查的功能布局与局部布线，尚未完成完整第一版 PCB。状态为 BLOCKED_NOT_FOR_MANUFACTURE_OR_POWERUP；不采购、不制造、不上电。

用户已明确批准常规矩形四层实验室验证板，尺寸随布局确定，机械要求未定。授权原文见 USER_PCB_AUTHORIZATION.json。网页完整 PCB 建议 assistant 9b8f6e19-5d0f-4747-8f44-582967be7705 / parent 96b76437-21e2-4c34-8249-e9cfc03e3710，保存在 PRO_PCB_RULING_FULL.md，时间范围 360 min。此前空载 bench 申请被拒绝，未执行。原理图仍冻结于接受基线 fbb7c0ed5f322f078583fadbdb353efe835e4c01。

实际 PCB 有 176 器件、550 个物理焊盘；514/514 已赋网连接焊盘、107 个非空赋值网络、36/36 NC 与接受原理图逐项相同。实际器件与封装解析名称及焊盘编号符合原接受基线。该结论限于实际焊盘赋值，不代表原生 compiler 网表比对通过。

板框暂定 100×90 mm，四层已启用。176 器件按 ROW/TIA、参考、ADC、MCU 和电源功能手动分区；不是自动布局结果。保存了 93 条 L1 导线、一个闭合板框、一个 L2 GND 铺铜边界。46 条初始局部路径覆盖 16/24 个局部网络组；完整布线未完成。L2 尚无填铜、缝合、所有地焊盘连通或连续回流证明。外部重绘的绿色背景不能当作实际铜面。

最终原生详细 DRC 为 0 条 clearance、452 条 Connection Error、1 条 Netlist Error，共 453 行明细。452 是错误条目数，不是独立网络数。两条初始 5.9 mil 间距错误已修正，并经原生 DRC 验证消除；这不能称 DRC clean。原生网表比对仍给出 107 个 net1 网络而 net2 成员为空。补齐 176 个原始 uniqueID、官方明确 JLCEDA setNetlist 返回 true/save true 后，该比对结果仍未改变。保留实际赋值 PASS 与 compiler 失败之间的矛盾，不能放行制造。

唯一自动布线调用约 49.75 s 超时，返回明确提示可能仍运行。只读核对无新线后，官方关闭自有 session 再继续，没有重试自动布线。另一次 deprecated 默认网表读取同样超时；关闭自有 session 后仅转用已知官方实际 File 导出和明确 JLCEDA 接口。未开展 API/SDK、DB、cache、profile 或激活调查。

最终暖态与独立冷打开的全部器件、焊盘、坐标及全部非 DOCHEAD source 记录多重集合相同，raw source bytes 不同。历史 helper 错筛 PAD/POLYLINE、漏掉实际 PAD_NET/POLY；终审独立全量复核和 WARM_COLD_FULL_RECORD_FIXPASS.json 已补证，不回写历史失败。9 项原冻结输入 fresh SHA 全部相同；另附 13 项继承 ledger，不能称本轮 fresh 13 项认证。

主要原生审查文件 SCIENCE_ADK5556_4X4_R21_PCB_BLOCKED_REVIEW.epro2：763271 bytes，SHA256 0A7C888194A248939E6FA9C08ECD597F17FD2E4430C35FF368851C372B3F3CE3。真实 File base64 逐字节相同、archive CRC 正常；其中 COMPONENT176/PAD_NET550/LINE93/POLY1/POUR1/ATTR529 的 id+body 对应最终 cold 捕获。eprj2 保留为工作容器证据；同一路径冷打开已核验，但不宣称整个工作容器内部全语义与 epro2 字节等价。工作容器 mtime 早于最后 setNetlist/save 返回，单凭时间戳不能推出持久化成功或失败；网表比对失败始终保留。

所有四个自有 headless session 已官方 closed。实际计数见 EXECUTION_BUDGET.json：99 个已保存官方命令记录，其中 doc54/invoke34/session6/open4/functions1，16 次 successful saved=true；session6 是命令数，实际创建 session4。另列 WinError206、静态断言和缺失脚本 prelaunch 三个尝试，子 EDA 进程均 0，精确时间/未保存 traceback 不补造。原停止快照约 39.62 min；只读终审、文档修正及发布时间分别留账。新仿真、bench、采购、制造、本地 Git 写入和系统改动均 0。没有安装或引入新执行器。

一次终审 Critical0；Important2 为已披露的完整网络/布线和地平面阻断。Minor3 已通过一次文档和离线证据修正处理，见 FINAL_DOCUMENT_FIXPASS.md；不追加终审或新 EDA。两张 PNG 是实际 native pad/line 坐标的外部重绘，使用保守包络，适合粗布局审查；不是 editor 截图、原生 PDF、Gerber、courtyard/DFM 或填铜认证。没有生成虚假的 PDF/Gerber。

## 集中请求下一工程包（仅申请，尚未批准）

请先裁定此临时功能布局及唯一支持的原生网表整合路线，再进入完整布线。用户明确要求在正常报告同时申请更多有界时间、次数及自主范围，原文保存在 USER_BOUNDED_BUDGET_REQUEST_SOURCE.json。

建议唯一 PCB_NETLIST_INTEGRATION_AND_ROUTING_CLOSURE_V1，360 min：已知原生整合45 / 常规完整布线180 / 详细 DRC 与冷重开审查75 / 交付60。申请 copy1/session≤3/save≤12/captureaudit≤4/DRC≤4/reviewexport≤2。一般布局、布线、已知 DRC 修正本地自主累计。网表矛盾必须先解决，不能直接豁免制造连通性；不得回到工具内部研究。若当前支持接口无法完成，明确报告一次必需的用户 UI 操作或可操作交接，不反复修工具。原理图电气基线冻结；所有新仿真、采购、制造、上电、bench、本地 Git/系统改动仍为 0。以上不是当前剩余时间的自动延续，也不是已批准额度。

END-OF-COMPLETE-R21-PCB-FLOORPLAN-AND-LOCAL-ROUTING-BLOCKED-RECEIPT
'''
(P/'COMPLETE_PCB_RECEIPT.md').write_text(receipt,'utf8')
(P/'FINAL_DOCUMENT_FIXPASS.md').write_text('''# 一次最终文档和证据修正

终审 Minor1：保留原 helper 和 WARM_COLD_COMPARE，新增全部非 DOCHEAD 记录核对，覆盖真实 PAD_NET/POLY；仅重读保存数据，没有新 EDA。

Minor2：官方命令记录从98更新至99，包含 FINAL_ALL_SESSIONS；区分6个 session命令与4个实际 session，三项原未列尝试另列。缺失精确时间和 traceback 明示未知，不补造。停止快照不回填，发布生命周期另记。

Minor3：完整回执改为可读中文，加入直接用户更多预算原文与当前360min来源定位，未来申请保持未批准。

Important1/2 工程阻断保持；没有修改PCB、改网、补线、填铜、新仿真或再审查。epro2主要原生证据及eprj工作容器范围已明确。完整PCB目标尚未达到。
''','utf8')
assert len(q['operations'])==99 and q['counts']['session']==6
assert types['PAD_NET']==550 and types['POLY']==1
print(json.dumps({'records':types,'officialCommands':99,'docFixOnly':True},ensure_ascii=False))
