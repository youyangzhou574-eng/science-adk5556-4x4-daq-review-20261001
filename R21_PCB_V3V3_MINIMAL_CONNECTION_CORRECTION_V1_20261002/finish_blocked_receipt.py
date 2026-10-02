from pathlib import Path
import json,hashlib,datetime,collections
P=Path(__file__).parent
def read(n):return json.loads((P/n).read_text('utf8'))
def write(n,q):(P/n).write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n','utf8')
d=read('ACTUAL_CAPTURE_VS_NATIVE_FILE_DIFF.json');numbers=[];struct=[]
def walk(a,b,path):
 if isinstance(a,(float,int))and not isinstance(a,bool)and isinstance(b,(float,int))and not isinstance(b,bool):
  if a!=b:numbers.append({'path':path,'capture':a,'file':b,'absoluteDifference':abs(a-b)})
 elif type(a)!=type(b):struct.append({'path':path,'capture':a,'file':b})
 elif isinstance(a,dict):
  if a.keys()!=b.keys():struct.append({'path':path,'keysDifferent':True})
  for k in a.keys()&b.keys():walk(a[k],b[k],path+'/'+str(k))
 elif isinstance(a,list):
  if len(a)!=len(b):struct.append({'path':path,'lengths':[len(a),len(b)]})
  for i,(x,y)in enumerate(zip(a,b)):walk(x,y,path+'/'+str(i))
 elif a!=b:struct.append({'path':path,'capture':a,'file':b})
for x in d['POURED']['changed']:walk(x['capture'],x['file'],x['id'])
representation={'LINE':d['LINE'],'POURED':{'captureCount':d['POURED']['captureCount'],'fileCount':d['POURED']['fileCount'],'changedObjects':len(d['POURED']['changed']),'added':d['POURED']['addedInFile'],'missing':d['POURED']['missingInFile'],'structuralDifferences':struct,'numericDifferenceCount':len(numbers),'maxAbsoluteNumericDifference':max((x['absoluteDifference']for x in numbers),default=0),'allNumericDifferences':numbers},'cause':'UNKNOWN; representation difference retained, no tool research','actualNativeDRCAuthoritative':True}
write('CAPTURE_NATIVE_REPRESENTATION_SUMMARY.json',representation)
protected=[]
for name,sha in [('SCIENCE_ADK5556_4X4_R21_ROUTING_CLOSURE_WORK.eprj2','FCD73BF2620447E7906D4014628F58F2C497410366B985E6FB0932D6322772BE'),('SCIENCE_ADK5556_4X4_R21_PCB_ROUTED_REVIEW.epro2','5603E205FCB5170DE00A125DCD7A6271665D78BED153E4B6B489ABEAF8F8FB6E')]:
 f=P.parent/'R21_PCB_ROUTING_CLOSURE_V1'/name;got=hashlib.sha256(f.read_bytes()).hexdigest().upper();protected.append({'path':str(f),'bytes':f.stat().st_size,'expected':sha,'actual':got,'PASS':got==sha})
assert all(x['PASS']for x in protected)
f=P/'SCIENCE_ADK5556_4X4_R21_V3V3_MINIMAL_WORK.eprj2';write('FROZEN_INPUT_AND_WORK_COPY_HASHES.json',{'protected':protected,'workCopyAfterClose':{'bytes':f.stat().st_size,'SHA256':hashlib.sha256(f.read_bytes()).hexdigest().upper(),'explicitSave':False,'qualifiedCold':False,'note':'Do not infer persistence from a file hash; failure native export is the preserved actual state.'}})
write('GUI_SESSION_LIFECYCLE.json',{'sessionId':'1c4328a9-c1fb-4e47-bb24-0b973e25517a','officialStatus':'closed','source':'CLOSE_V3V3_WARM.json','GUIwindowId':333494,'normalCloseClickedOnce':True,'freshOwnAppWindowInventory':[],'confirmedUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'explicitSave':False,'coldOpened':False,'solverStarted':False})
(P/'OFFLINE_REPORT_INITIAL_FAILURES.txt').write_text('Offline report preparation failures retained. No CAD or scientific rerun followed these failures.\n1. Initial strict capture-vs-native assertion failed: LINE=false and POURED=false; other captured object classes true. Fixed report to retain full difference and assert only the equal classes.\n2. Created-ID evidence comprehension used h["id"] on DOCHEAD with no id: KeyError: id. Changed to h.get("id") and reran the same offline report script. All new LINE/VIA IDs were then confirmed in actual native File.\nNeither failure is a board electrical result; both are evidence-report script corrections.\n','utf8')
s=read('BLOCKED_EVIDENCE_SUMMARY.json');budget=read('EXECUTION_BUDGET.json')
write('GATES.json',{'status':'BLOCKED','stickySTOP':budget['status'],'ConnectionError':0,'Short':0,'ClearanceError':4,'NetlistError':0,'warmElectricalClosure':False,'cold':'NOT_STARTED','PCB_REVIEW_READY':False,'MANUFACTURING_NOT_RELEASED':True,'BENCH_NOT_RELEASED':True,'componentAndPadIdentity':True,'nonV3V3CopperUnchangedPrePost':True,'nativeFailureCaptureQualifiedForUse':False,'savedProjectPersistenceVerified':False})
write('NEXT_BOUNDED_REQUEST.json',{'requestedByUser':'User explicitly requested more bounded execution time/counts/autonomy in the next normal report; this request does not grant budget.','proposedPackage':'R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1','minutes':120,'timeAllocation':{'localDerivedPourUpdate':20,'warmColdVerification':40,'delivery':45,'reserve':15},'limits':{'copy':1,'session':2,'save':1,'captureaudit':3,'DRC':3,'reviewExport':1,'normalPourUpdate':1},'scope':'Keep the current two V3V3 bridges and one via. One known normal derived pour update to create required antipads; GND filled polygons may change only as required by the new V3V3 via. No parameter/net/rule or new line/via edits. If ordinary native pour update still fails, STOP and report. Pro must explicitly approve derived non-V3V3 copper update before execution.','componentMove':0,'newLine':0,'newVia':0,'schematic':0,'ImportChanges':0,'library':0,'simulation':0,'Gerber':0,'procurement':0,'manufacture':0,'actualBench':0,'approved':False})
body=f'''# R21 PCB V3V3 minimal correction — BLOCKED, NOT FOR USE

本包按14号裁定执行两个局部V3V3桥接，真实未连接从2降为0；立即原生DRC新增4项Clearance Error，因此按停止门结束。不是电气闭合PASS，不是可制造PCB。未继续修铜/刷新覆铜/保存/cold。所有失败证据保留。

## 输入、范围与实际操作

唯一裁定：CIRCUIT-PRO-R21-PCB-V3V3-MINIMAL-CONNECTION-CORRECTION-20261002-14，assistant f80cab79-8653-407b-9416-a808f358290c，parentuser 504704c5-3b28-483b-a977-6d9a0a433581；全文见PRO_V3V3_CORRECTION_RULING_FULL.md。180min，从零，最多2个局部bridge/1个必要via。GUI实际确认正确工作副本PCB1画布和层栏，点击两个native DRC对象，查看局部铜后使用既有官方LINE/VIA操作。没有工具/API/SDK研究。

1. C_MCU1 pin1：只删除旧V3V3短线c131c12ef419b393，重画12mil Top线a9e5041778cdb40e，从native DRC精确pad中心(3200.7865,1822.8346)mil到既有main-plane via26(3160.05,1822.8)mil。
2. e255：保留原via d9d6381bb71f0d80；12mil Bottom桥(3317.55,1830.7)→(3340,1830.7)→(3380,1790.7)mil，新增LINE 9a5309ba44b7aefd/4e5c023ee9440731；新增唯一V3V3 via5c0162206220ea3b，显示e307，hole12/diameter24mil，落在V3V3 main plane。未跨功能区、未移MCU、未改主干。

候选静态几何筛查使用6mil，低于这次native DRC实际要求10mil；对新增via还排除了已填充GND多边形，假定正常antipad行为能提供间距，却没有执行覆铜更新。这是本地规划遗漏，不是工具bug、不证明物理不稳定，也不能把静态筛查称为native PASS。保留候选与两种已拒绝局部走法的原记录。14号只允许V3V3 LINE/VIA变化，所以发现GNDfill错误后未擅自更新非V3V3铜。

## 原生DRC和停止点

PRE_DRC：Connection2/Short0/Clearance0/Netlist0。FIRST_POSTFIX_DRC：Connection0/Short0/Clearance4/Netlist0。

4项均为新via e307与原GND填充铜：Top(1)和Inner1(15)分别报annulus与hole；minDistance=0mil，shouldBe≥10mil。它们是两个层的同一via区域四条原生错误，不是四个独立架构故障。详细对象/层/位置见ACTUAL_FOUR_CLEARANCE_ERRORS.csv及FIRST_POSTFIX_DRC.json。原GND填充未重建，前后POURED严格不变。此事实与antipad更新遗漏相符；尚未以实际更新/DRC证明修复，不能称只是陈旧缓存或已解决。

STOP_NEW_V3V3_VIA_TO_GND_FILLED_CLEARANCE 保持。唯一session已官方closed，GUI正常关闭一次后fresh app inventory为空；无solver。未做同区域第二pass，因该例外只允许剩余Connection Error，不允许Clearance Error继续。

## 全量身份与铜差异

温态176parts/550pads/514assigned/107非空padnet/36NC。550逐针网络、176完整核心字典/坐标全部PASS，rule严格相同。PRE→POST完整ID+body多重集合：COMPONENT/PAD_NET/ATTR/POUR/POURED/POLY/RULE严格相同；仅V3V3 LINE新增3/删除1，V3V3 VIA新增1，没有其他网络铜改动。原始全量差异及550/176可读CSV随包交付。

historical frozen native File909 LINE；pre-fix actual reopened907；post-fix actual warm909=907+3−1，VIA296→297。按14号不重建历史VCM137f992f55430857/TIA121f945bfa3a6372f两条0.1mil短线。

实际失败File有911 LINE，恰比warm多上述历史两条；COMPONENT/PAD_NET/ATTR/VIA/POUR/POLY/RULE严格一致。POURED4对象中{representation['POURED']['changedObjects']}有数值变化：{len(numbers)}项，最大绝对差{representation['POURED']['maxAbsoluteNumericDifference']:.17g}；结构差异{len(struct)}项。保留完整差异，不声称rawbytes/几何严格相同，不调查序列化原因。此表示差异不是新的人工重建；本次3条LINE和1VIA的ID全在真实失败File中。

## 失败原生与保护

SCIENCE_ADK5556_4X4_R21_V3V3_BLOCKED_NOT_FOR_USE.epro2：{s['nativeFileBytes']}bytes，SHA256 {s['nativeFileSHA256']}。这是STOP后只读捕获的实际native File，保存了未显式save的失败画布状态；不是已通过warm/cold的持久化工程。工作eprj2也保存供审查，但其hash不证明未保存修改已持久化。禁止装配/制造/上电。冻结旧routing工作eprj2与review epro2逐字节SHA均未变，见FROZEN_INPUT_AND_WORK_COPY_HASHES.json。

## 实耗及未完成项

copy1/session1/save0/captureaudit3/DRC2/reviewExport0；localBridge2/newVia1/sameAreaSecondPass0。capture3=pre完整capture、STOP后失败完整capture、实际native File捕获。STOP后的两次捕获只保存证据，没有CAD mutation或save。没有新增review图，nativeGUI已有实际观察文本；cold/session2/save/PDF/Gerber/覆铜更新/仿真/器件移动/改值/Import/库/制造采购/actualbench/localGit/system均0。

PCB_REVIEW_READY=false；warmElectricalClosure=false；cold NOT_STARTED。旧剩余额度关闭，不解除STOP。制造/bench仍未放行；不虚报真实100fps、精度或实物电源可靠性。

离线报告脚本最初严格File比较失败及DOCHEAD无id的KeyError见OFFLINE_REPORT_INITIAL_FAILURES.txt；两次仅修报告逻辑，保留差异，无CAD重跑或科学计算。

## 唯一下一包请求（未批准）

按用户明确提出的更多有界时间/次数/自主范围要求，在本次正常报告集中申请R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1，120min（局部derived pour20/温冷40/交付45/预留15），copy1/session2/save1/captureaudit3/DRC3/reviewExport1/normalPourUpdate1。只保留现有两局部桥和via，对其执行一次已知正常覆铜更新产生10mil规则所需antipad；明确申请由此必要的GND derived fill变化，不改网/值/规则/器件/走线via，不研究API。native DRC未全0或其他真实错误立即STOP。warm全0才save/close/independentcold，再全量身份/铜及DRC验收。新增LINE/VIA、移件、Import、schematic、库、仿真、Gerber、制造/采购/bench均0。此处只是请求，不执行；如Pro不接受该更新范围则保留BLOCKED。

完整交付将包含所有原始capture/File/source/CLI/GUI文本/失败DRC/可读CSV/索引/manifest及ZIP，每个源文件单独可读下载。网页实际逐附件阅读未验证，不设额外ACK门。发送一次后记录owner、nextCheck和接续monitor，避免发完停住。

END-OF-COMPLETE-R21-PCB-V3V3-MINIMAL-CORRECTION-CLEARANCE-BLOCKED-RECEIPT
'''
(P/'COMPLETE_V3V3_CORRECTION_RECEIPT.md').write_text(body,'utf8')
(P/'README.md').write_text('''# R21 V3V3 correction: BLOCKED NOT FOR USE

[Complete receipt](COMPLETE_V3V3_CORRECTION_RECEIPT.md) · [Ruling14](PRO_V3V3_CORRECTION_RULING_FULL.md) · [Gates](GATES.json) · [Actual budget](EXECUTION_BUDGET.json)

Two original V3V3 Connection Errors eliminated; four new native Clearance Errors. STOP; no save/cold/pour update. Manufacturing/bench not released.

- [Actual4 errors](ACTUAL_FOUR_CLEARANCE_ERRORS.csv), [raw immediate nativeDRC](FIRST_POSTFIX_DRC.json)
- [All550 pad nets](ALL_550_PAD_NET_COMPARE.csv), [176 core identity](ALL_176_CORE_COMPARE.csv)
- [Full PRE→POST copper diff](NATIVE_PRE_POST_OBJECT_DIFF.json), [capture-vs-File representation](CAPTURE_NATIVE_REPRESENTATION_SUMMARY.json)
- [Blocked actual nativeFile](SCIENCE_ADK5556_4X4_R21_V3V3_BLOCKED_NOT_FOR_USE.epro2), [actual source](ACTUAL_POSTFIX_FAILURE_PCB_SOURCE.txt), [native extracted source](FAILURE_PCB_DOCUMENT_FROM_NATIVE_FILE.txt)
- [Close lifecycle](GUI_SESSION_LIFECYCLE.json), [protected SHA and workcopy](FROZEN_INPUT_AND_WORK_COPY_HASHES.json)
- [Unapproved bounded next request](NEXT_BOUNDED_REQUEST.json)

NativeFile preserves unsaved failure state. This is not a saved/cold-qualified PCB. All raw failures retained; no LFS pointer-only delivery.
''','utf8')
print(json.dumps({'receiptBytes':(P/'COMPLETE_V3V3_CORRECTION_RECEIPT.md').stat().st_size,'POUREDnumericDiffs':len(numbers),'maxDiff':representation['POURED']['maxAbsoluteNumericDifference'],'structDiffs':len(struct),'fileAddedLINE':[x['id']for x in d['LINE']['addedInFile']],'sourceFrozen':True}))
