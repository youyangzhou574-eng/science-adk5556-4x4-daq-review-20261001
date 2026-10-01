from pathlib import Path
import json,csv,collections,hashlib,datetime
P=Path(__file__).resolve().parent
O=P.parent/'R21_PCB_FLOORPLAN_AND_LAYOUT_V1'
def load(n): return json.loads((P/n).read_text('utf8'))
def put(n,v): (P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf8')
def value(n): return load(n)['parsed']['value']
a=value('CLOSURE_CAPTURE_A.json');b=value('CLOSURE_CAPTURE_B.json');c=value('CLOSURE_CAPTURE_C_COLD.json')
assert a['parts']==b['parts']==c['parts']
def source_records(src):
    out=[]
    for ln in src.splitlines():
        z=ln.split('||')
        if len(z)!=2: continue
        h=json.loads(z[0]);body=json.loads(z[1].rstrip('|'))
        if h['type']!='DOCHEAD': out.append(json.dumps([h,body],sort_keys=True,ensure_ascii=False))
    return collections.Counter(out)
assert source_records(a['source'])==source_records(b['source'])==source_records(c['source'])
def members(n):
    result={}
    for comp in n['components'].values():
        ref=comp['props']['Designator']
        for number,pin in comp['pinInfoMap'].items():result[(ref,number)]=pin['net']
    return result
native=json.loads((P/'ACTUAL_PCB_JLC_NETLIST.json').read_text('utf8'))
schem=json.loads((O/'ACCEPTED_SCHEMATIC_JLC_NETLIST.json').read_text('utf8'))
actual=members(native); expected=members(schem)
assert actual==expected and len(actual)==550
rows=[]
for part in c['parts']:
    for pad in part['pads']:
        key=(part['ref'],pad['number']);assert actual[key]==pad['net']
        rows.append({'ref':part['ref'],'pad':pad['number'],'net':pad['net'],'x_mil':pad['x'],'y_mil':pad['y'],'NC':not bool(pad['net'])})
with (P/'ACTUAL_550_PADS.csv').open('w',encoding='utf8',newline='')as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
report={'officialPCB_JLCComponents':len(native['components']),'actualPhysicalPads':len(actual),'assignedConnections':sum(bool(n)for n in actual.values()),'nonemptyNets':len({n for n in actual.values()if n}),'NC':sum(not n for n in actual.values()),'all550OfficialJLCAndActualPadStatesMatchAccepted':True,'warmBeforeAfterColdPartsEqual':True,'allNonDOCHEADMultisetEqual':True,'rawBytesEqual':a['source']==c['source'],'nativeNetlistErrorGatePassed':False,'scope':'assigned net membership only; not copper continuity or native compiler acceptance'}
assert (report['officialPCB_JLCComponents'],report['assignedConnections'],report['nonemptyNets'],report['NC'])==(176,514,107,36)
put('P1_OFFICIAL_JLC_AND_COLD_AUDIT.json',report)
for n,v in [('WARM_A_SOURCE.txt',a['source']),('AFTER_SYNC_B_SOURCE.txt',b['source']),('COLD_C_SOURCE.txt',c['source'])]:(P/n).write_text(v,'utf8')
drc=value('CLOSURE_DRC_C_HEADLESS.json')['result'];details=[]
for group in drc:
    for subgroup in group['list']:
        for item in subgroup['list']:
            details.append({'category':group['name'],'subtype':subgroup['name'],'objects':';'.join(item['objs']),'description':item['explanation']['str'],'parameters':json.dumps(item['explanation'].get('param',{}),ensure_ascii=False)})
with (P/'FINAL_DRC_DETAILS.csv').open('w',encoding='utf8',newline='')as f:
    w=csv.DictWriter(f,fieldnames=list(details[0]));w.writeheader();w.writerows(details)
summary={g['name']:g['count']for g in drc};summary['Clearance Error']=0
assert summary['Connection Error']==452 and summary['Netlist Error']==1
assert all('is disconnected from other objects of the same network'in r['description']for r in details if r['category']=='Connection Error')
summary['connectionDescription']='Same-net object disconnected, consistent with unfinished copper/ratsnest; cannot prove final connectivity'
put('FINAL_DRC_SUMMARY.json',summary)
frozen=load('FROZEN_INPUT_SHA.json');check=[]
for item in frozen:
    d=Path(item['path']).read_bytes();assert len(d)==item['bytes']and hashlib.sha256(d).hexdigest().upper()==item['sha256'];check.append({**item,'PASS':True})
put('FROZEN_INPUT_FINAL_PASS.json',check)
q=load('EXECUTION_BUDGET.json');now=datetime.datetime.now(datetime.timezone.utc)
ops=[]
for path in sorted(P.glob('*.json')):
    try:r=json.loads(path.read_text('utf8'))
    except ValueError:continue
    if not isinstance(r,dict)or'command'not in r:continue
    parsed=r.get('parsed')or{};ops.append({'label':path.stem,'kind':r['command'][1],'ok':parsed.get('ok',False),'startUTC':r['started_utc'],'error':parsed.get('error')})
q.update(status='BLOCKED_P1_NO_MORE_NATIVE_OR_ROUTING',stop='NATIVE_NETLIST_ERROR_PERSISTS_AFTER_SINGLE_DOCUMENTED_SYNC',stoppedUTC=now.isoformat(),elapsedMinutes=(now-datetime.datetime.fromisoformat(q['startedUTC'])).total_seconds()/60,operations=ops,actualSavedTrue=1,stage2RoutingActions=0,remainingQuotaIsNotContinuationPermission=True)
put('EXECUTION_BUDGET.json',q)
put('GATES.json',{'nativeNetlistErrorZero':False,'actual550PadMappingUnchanged':True,'officialPCB_JLCMatchesAccepted':True,'remainingConnectionErrorsDescriptionOnlySameNetDisconnected':True,'allCopperConnectionsCertified':False,'fullRoutingComplete':False,'DRCClean':False,'manufactureReleased':False,'benchReleased':False,'stop':q['stop']})
(P/'EDITOR_SYNC_HANDOFF.md').write_text('''# 唯一可操作的编辑器交接

不是要求修软件或重新设计电路。请在嘉立创专业版打开本包 SCIENCE_ADK5556_4X4_R21_PCB_CLOSURE_WORK.eprj2 的 PCB1，在 DRC 的唯一 Netlist Error 行点击规则名 **Import Changes**。这是保存的原生错误正文明确提供的操作。查看并保存弹出的原理图/PCB差异明细，尤其是哪一器件/哪一针或哪个属性；不要直接接受改网或新器件，不改原接受原理图。

请把实际差异明细及必要操作回传本聊天，或由网页指定一条已支持的、可操作的编辑器同步路线。若差异窗口为空，也记录真实空结果，不能解释成 Netlist Error 自动通过。本包已做一次官方 importChanges+save，实际全部176/550及非DOCHEAD记录未变，冷DRC仍1条Netlist Error。没有继续查API/SDK/cache或再尝试全板autoroute。

只有确认该网络整合门通过才继续手工关键模拟布线；现在不要下单、出Gerber或上电。已有100×90四层布局及93段局部线保留，不推翻布局。
''','utf8')
(P/'COMPLETE_ROUTING_CLOSURE_RECEIPT.md').write_text('''# R2.1 PCB 网络整合阻断回执

包 SCIENCE_ADK5556_4X4_R21_PCB_NETLIST_INTEGRATION_AND_ROUTING_CLOSURE_V1。

本包按完整新裁定 e13aa5ff-3062-4aa7-859d-fd57ecbf7cd4 / parent230dd058-72ff-48be-ae8c-aa1fcdef32f9 执行。360min为60整合/120关键模拟/90普通布线/90DRC冷审交付；session≤3/save≤12/capture≤4/DRC≤4。用户PCB范围授权保留，不采购、不制造、不上电。已接受原理图和前包100×90四层功能布局不改。

P1实际取得官方 **明确JLCEDA格式 PCB网表**：176components、550pinInfoMap、514非空赋网、107nets、36NC。逐550项与原接受原理图官方JLC网表及实际pad状态完全一致。这个比以前仅typedpad检查多一层正式网表导出证据，但不等于native DRC比对通过。明确project/document对象的另一种已文档支持对比调用返回null，未把null算PASS，也不继续调查。

完成一次官方 importChanges(原schematicUUID)+save，updated/saved返回true。所有176器件/pad/positions状态在前A、后B、同路径独立冷C完全一致；全部非DOCHEAD source多重集合相同，rawbytes不同。没有删原107有效网络、没有误绑焊盘、没有改变任何旧线/板框/铺铜边界。10项前包冻结输入重新核SHA均不变。

随后首次DRC错误选择userInterface=true，在headless约29.75s超时，可能仍运行。这是本地参数选择错误，完整错误保存；官方关闭自有session后只调用已有正确headless参数check(true,false,true)，没有重复同一显示窗口调用或研究API原因。第二次取得完整原生详细树：**0clearance /452Connection Error /1Netlist Error**。452条正文全部“同网对象未连接”，符合未完成铜连接，不能说已经布线通过。唯一NetlistError正文明确提示点击规则名Import Changes查看差异；该真实门仍失败。

因此P1没有通过，未进入Phase2/3。没有新增任何route/placement/pour，不运行autoroute、SPICE、MIMO/descriptor，不重新改原理图。完整PCB仍NOT_COMPLETE，DRC不是clean，制造/上电未放行。停止继续尝试同步/工具修理，提出 EDITOR_SYNC_HANDOFF.md 的具体一次编辑器差异查看交接；不再申请一包盲修工具。

实耗copy1/session2/save尝试1成功1/capture3/DRC尝试2（超时1、完整返回1）。两自有session官方closed，未启动solver。完整360min余量与计数余量不构成继续绕过P1门的授权。工作eprj副本及全部官方网表、actual捕获source/CSV、DRC明细、CLI失败和关闭证据均随包提供。没有新native epro2/PDF/Gerber导出；此前固定native版本dfd80b342744aa21625fdf693dc1b1f81333ba56仍可审查，本包没有虚构新的已完成PCB。

请集中裁定/交接唯一支持的原生编辑器整合操作，获得实际Import Changes差异后再手工布线，不回工具内部研究。用户明确要求下一次正常报告申请足够有界预算；本次已有批准360min包在P1结束，不另要求无输入的新整合预算。仅在差异得到并路线可执行后，申请最多240min用于关键模拟90/普通连接75/DRC冷审45/交付30，session≤2/save≤10/capture≤3/DRC≤3；这是条件请求尚未批准。采购/制造/上电/bench/本地Git/system均0。

END-OF-COMPLETE-R21-PCB-NETLIST-INTEGRATION-EDITOR-HANDOFF-BLOCKED-RECEIPT
''','utf8')
(P/'README.md').write_text('''# R2.1 PCB 原生网络整合交接审查包

[完整回执](COMPLETE_ROUTING_CLOSURE_RECEIPT.md) · [具体编辑器交接](EDITOR_SYNC_HANDOFF.md) · [官方550项核对](P1_OFFICIAL_JLC_AND_COLD_AUDIT.json) · [实际焊盘CSV](ACTUAL_550_PADS.csv) · [453条DRC](FINAL_DRC_DETAILS.csv) · [预算](EXECUTION_BUDGET.json) · [门](GATES.json)。

本包 **BLOCKED_NOT_FOR_MANUFACTURE_OR_POWERUP**。一次常规同步未清除1条原生NetlistError；没有继续API研究或布线。明确格式官方网表匹配550项，不代表铜连接/完整PCB通过。

布局和原生epro2沿用 [前包固定版本](https://github.com/youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001/tree/dfd80b342744aa21625fdf693dc1b1f81333ba56/R21_PCB_FLOORPLAN_AND_LAYOUT_V1_20261002)。本包含独立工作副本、实际官方导出、温冷全量source/CSV、详细DRC和失败/关闭原始证据；不只有ZIP/LFS。
''','utf8')
print(json.dumps({'audit':report,'DRC':summary,'used':q['used'],'frozen':len(check),'minutes':q['elapsedMinutes']}))
