from pathlib import Path
import json,hashlib,datetime,re
root=Path(__file__).resolve().parent
def write(n,o): (root/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
b=json.loads((root/'EXECUTION_BUDGET.json').read_text())
b.setdefault('originalTaggedUsed',dict(b['used']))
b['used']['P0/AC_DC_PZ']=39;b['used']['P1/transient']=20
b['scienceStopped']=True;b['budgetStatus']='P0_ANALYSIS_COUNT_EXCEEDED_BY_7_REQUIRES_EXPLICIT_REVIEW'
audit=[]
for row in b['cases']:
    text=(root/'cases'/(row['name']+'.cir')).read_text(errors='replace');charges={row['kind']}
    if row['phase']=='P0' and re.search(r'(?im)^\s*\.?\s*(op|optran|ac|pz)\b',text):charges.add('AC_DC_PZ')
    if row['phase']=='P1' and re.search(r'(?im)^\s*\.?\s*tran\b',text):charges.add('transient')
    row['strictCharges']=sorted(charges)
    if len(charges)>1:audit.append({'name':row['name'],'phase':row['phase'],'originalKind':row['kind'],'strictCharges':sorted(charges)})
assert len(audit)==8
write('EXECUTION_BUDGET.json',b)
write('evidence/BUDGET_CLASSIFICATION_AUDIT.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'originalTaggedUsed':b['originalTaggedUsed'],'strictUsed':b['used'],'dualCharges':audit,'P0Overrun':7,'cause':'diagnostic attribute incorrectly treated as disjoint analysis quota','newScienceStopped':True,'fix':'analysis plus diagnostic preflight before ledger mutation and Popen','infrastructureRegression':'BUDGET_PREFLIGHT_RED.log then BUDGET_PREFLIGHT_GREEN.log; no executor launched'})
write('evidence/INDEPENDENT_FINAL_REVIEW.json',{'reviewer':'coupled_final_review','readOnly':True,'importantFindings':['reset/configure rejection retained valid qualification','P0 diagnostic DC/AC executions excluded from analysis counter'], 'resolution':['new wrapper catches rejection and clears; existing test07 extended; RED reproduced and final32 GREEN','strict P0 count39/32 (+7) disclosed; special full transient counted20/32 and1/1; atomic multi-category budget preflight RED/GREEN; all new science blocked'], 'frozenBaseUnchanged':True,'noAdditionalSpiceProcesses':True,'nativeEntry':'HOLD'})
write('evidence/PLOT_VISUAL_REVIEW.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'viewed':['plots/RETURN_RATIO_METHODS.png','plots/SINGLE_TIA_SETTLING.png','plots/COUPLED_PROGRESS.png'],'result':'PASS legible axes/legends/no clipping; isolated scope and forced stop labels visible','scientificScope':'not full-board stability or bench'})
for n in ['protocol.py','test_protocol.py']:
    assert (root/n).read_bytes()==(root.parent/'R2_VERIFICATION_AND_MINIMAL_ECO_V1'/n).read_bytes()
i=json.loads((root/'INPUT_VERIFIED.json').read_text());checks=[]
for m in i['models']:
    for p in [root/'models'/m['file'],root.parent/'R2_VERIFICATION_AND_MINIMAL_ECO_V1'/'models'/m['file']]:
        h=hashlib.sha256(p.read_bytes()).hexdigest();assert h==m['sha256'];checks.append({'file':str(p),'sha256':h,'PASS':True})
assert hashlib.sha256(Path(i['executor']).read_bytes()).hexdigest()==i['executor_SHA256']
write('evidence/FINAL_FROZEN_INPUT_RECHECK.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'models':checks,'executorUnchanged':True,'frozenProtocolAndTestsUnchanged':True})
p=root/'finalize_package.py';t=p.read_text(encoding='utf-8')
t=t.replace('回归通过。RED基线11项中8项失败，修复后32项通过，所有日志保存。','回归通过。RED基线11项中8项失败；终审另发现健康状态下旧epoch reset/错误configure会抛异常却保留资格，扩充现有test_07先RED复现，再仅修新wrapper立即clear，最后32项GREEN。冻结基类与原21项未改。所有日志保存。')
t=t.replace('正常暂态19次，另1次完整10宏模型短窗诊断，共20个暂态过程；','正常暂态实际20次（含1次同时扣特殊完整模型诊断），共20个暂态过程；')
t=t.replace('P0 AC/DC/PZ工况32/32，数值诊断7/8；P1完整静态AC24/24，正常暂态19/32，PZ4/12，完整10宏模型短窗诊断1/1（60s）；','**预算执行偏差：P0实际DC/AC/PZ分析39/32，超额7。** 原账把7次含DC/AC的诊断当成额外互斥额度，这是执行分类错误，不是新增授权；原标签账及全部失败证据保留在BUDGET_CLASSIFICATION_AUDIT.json。诊断属性7/8必须同时扣分析次数。已停止所有新科学运行，原数据保留供裁定；不声称预算全PASS，不要求追认就视作自动放行。runner已改为按实际分析与诊断属性双扣、所有额度预检通过后才记账/启动；隔离临时账的1项基础设施RED/GREEN验证没有调用求解器。P1完整静态AC24/24，正常暂态实际20/32，PZ4/12，完整10宏模型短窗同时扣特殊诊断1/1（60s）；')
t=t.replace('数值方法/排序/容差诊断≤16，reset解析','数值方法/排序/容差诊断属性≤16且同时计入其DC/AC/PZ或暂态次数（不是额外分析额度），reset解析')
t=t.replace("'BENCH':'NOT_RELEASED'","'BENCH':'NOT_RELEASED','RESOURCE_EXECUTION':'P0_COUNT_OVERRUN_7_REQUIRES_REVIEW'")
p.write_text(t,encoding='utf-8')
print(json.dumps({'strictP0':39,'P1Transient':20,'scienceStopped':True,'frozenChecks':'PASS'}))
