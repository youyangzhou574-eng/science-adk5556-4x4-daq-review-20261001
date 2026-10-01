from pathlib import Path
import json,re,collections,csv,datetime
R=Path(__file__).resolve().parent
def dump(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=R/'science.py';s=p.read_text()
s=s[:s.index('def init():')]+'''def init():
    raise RuntimeError('Legacy initializer disabled: no budget reset; package setup is immutable')

def analysis_commands(net):
    commands=[];inside=False
    for index,line in enumerate(net.splitlines()):
        line=line.strip().lower()
        if line=='.control':inside=True;continue
        if line=='.endc':inside=False;continue
        if line.startswith('*') or not line:continue
        word=line.split()[0]
        if inside and word in ['op','optran','ac','pz','tran']:commands.append(word)
        elif index>0 and not inside and word in ['.op','.ac','.pz','.tran']:commands.append(word[1:])
    return commands

def analysis_charges(commands,kind,net):
    charges={}
    count=sum(x in ['op','ac','pz'] for x in commands)
    if count:charges['DC_AC_PZ']=count
    count=commands.count('tran')
    if count:charges['transient']=count
    if kind in ['diagnostics','full_long'] or '.options method=gear' in net:charges['diagnostics']=1
    if kind=='full_long':charges['full_long']=1
    return charges

def require_technical_review(reason,source):
    p=ROOT/'EXECUTION_BUDGET.json';b=json.loads(p.read_text(encoding='utf-8'))
    if not b.get('scienceStopped'):
        b['scienceStopped']=True;b['scienceStoppedUTC']=utc();b['scienceStopReason']=reason
    b.setdefault('technicalReviewEvents',[]).append({'UTC':utc(),'reason':reason,'source':source})
    dump(p,b)

'''+s[s.index('def register('):]
a=s.index('    charges=set()');z=s.index('    assert name not in',a)
s=s[:a]+'''    commands=analysis_commands(net)
    charges=analysis_charges(commands,kind,net)
    assert any(x in charges for x in ['DC_AC_PZ','transient']),'NO_ANALYSIS_DECLARED'
    for category,count in charges.items():
        assert b['used'].get(category,0)+count<=b['globalLimits'][category],'COUNT_STOP:'+category
'''+s[z:]
s=s.replace("for category in charges:b['used'][category]=b['used'].get(category,0)+1","for category,count in charges.items():b['used'][category]=b['used'].get(category,0)+count")
s=s.replace("'commands':re.findall(r'(?im)^\\s*\\.?\\s*(op|optran|ac|pz|tran)\\b',net)","'commands':commands,'chargeCounts':charges")
p.write_text(s,encoding='utf-8')
import science
# Save original classifications before a conservative recount; no execution is authorized.
b=json.loads((R/'EXECUTION_BUDGET.json').read_text());dump(R/'evidence'/'PRE_REVIEW_BUDGET.json',b)
counts=collections.Counter();rows=[]
for c in b['cases']:
    commands=science.analysis_commands((R/'cases'/(c['name']+'.cir')).read_text())
    c['originalCommands']=c['commands'];c['commands']=commands
    c['originalCharges']=c['charges'];c['chargeCounts']=science.analysis_charges(commands,c['kind'],(R/'cases'/(c['name']+'.cir')).read_text())
    counts.update(commands);rows.append({'case':c['name'],'OP':commands.count('op'),'AC':commands.count('ac'),'PZ':commands.count('pz'),'TRAN':commands.count('tran'),'OPTRAN_initialization':commands.count('optran')})
assert dict(counts)=={'op':49,'pz':3,'ac':24,'optran':6},counts
b['originalUsed']=b['used'].copy();b['used']['DC_AC_PZ']=76
b['actualAnalysisInvocations']=dict(counts);b['solverProcessCases']=49
b['accountingCorrection']='Conservative directive count: 49 OP + 24 AC + 3 PZ = 76; 6 optran DC initializations separately disclosed. Original 49 combined-case classification retained.'
b['reviewControlDeviation']={'firstThresholdResultUTC':'2026-10-01T13:23:41+00:00','subsequentHybridDispatchUTC':'2026-10-01T13:41:58+00:00','postThresholdSolverCases':8,'actualStopUTC':b.get('scienceStoppedUTC',b.get('stoppedUTC')),'explanation':'Technical review flag did not lock runner; 8 crosscheck cases launched. Conservatively recorded execution-control deviation; no retrospective exception or backdated STOP. Sticky linkage now repaired.'}
dump(R/'EXECUTION_BUDGET.json',b)
with (R/'ACTUAL_ANALYSIS_COMMAND_INDEX.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for name in ['analyze_mimo.py','analyze_hybrid.py']:
    p=R/name;s=p.read_text().replace('from science import ROOT,dump','from science import ROOT,dump,require_technical_review')
    if name=='analyze_mimo.py':
        old="'provisionalPASS':allfinite and delta<1e-3 and float(sv[minindex,-1])>=.20 and tail<.10"
        assert old in s;s=s.replace(old,"'provisionalPASS':False,'missingQualifications':['full-network scalar crosscheck','independent repeated column','reference D qualification','general noncommuting fixture']")
        s=s.replace("    np.savez(ROOT/'results'/(tag+'_MATRIX.npz')", "    if result['dangerReviewRequired']:require_technical_review('sigma_min_I_plus_L below 0.20',tag)\n    np.savez(ROOT/'results'/(tag+'_MATRIX.npz')")
    else:
        s=s.replace("np.savez(ROOT/'results'/'HYBRID_MIMO.npz'","if result['sigmaMin']<.20:require_technical_review('sigma_min_I_plus_L below 0.20',tag)\nnp.savez(ROOT/'results'/'HYBRID_MIMO.npz'")
    p.write_text(s,encoding='utf-8')
# Enforce false in saved result without claiming a new mathematical qualification.
p=R/'mimo_blank_800_RESULT.json';o=json.loads(p.read_text());o['provisionalPASS']=False;o['missingQualifications']=['full-network scalar crosscheck','independent repeated column','reference D qualification','general noncommuting fixture'];dump(p,o)
p=R/'finalize_mimo.py';s=p.read_text(encoding='utf-8')
s=s.replace("['ac.txt','hybrid.txt','op.txt']","['ac.txt','hybrid.txt']")
insert="""    from network_cases import raw_nodes
    opcount=0
    for raw in (ROOT/'results').glob('*/op.raw'):
        if 'Operating Point' not in raw.read_text(errors='replace'):continue
        nodes=raw_nodes(raw)
        if nodes:
            import csv
            with raw.with_suffix('.csv').open('w',newline='',encoding='utf-8') as out:
                w=csv.writer(out);w.writerow(['node','voltage_V']);w.writerows(sorted(nodes.items()))
            opcount+=1
"""
s=s.replace("    b=json.loads((ROOT/'EXECUTION_BUDGET.json').read_text());",insert+"    b=json.loads((ROOT/'EXECUTION_BUDGET.json').read_text());")
s=s.replace("全局计数不是互斥阶段额度：实际DC/AC/PZ netlist工况", "全局计数不是互斥阶段额度：保守实际DC/AC/PZ分析指令次数")
start=s.index('每个combinedOP+AC/PZ');end=s.index('临时隔离账',start)
s=s[:start]+'''保守逐指令重计49 OP＋24 AC＋3 PZ＝76次，剩余52次；另6条optran是DC初始化，单列披露。原49合并工况账作为PRE_REVIEW_BUDGET.json保留，不能把旧39/32偏差视为合并计数的授权。新runner按每条OP/AC/PZ预扣，TRAN和诊断属性同时计数；只解析.control分析块和合法点分析指令，标题PZ不计。
终审还发现第一次open矩阵RESULT在13:23:41UTC写出σ<0.20标志，但程序没有同步锁runner；13:41:58UTC仍启动8个hybrid交叉诊断，13:47:42UTC才写科学STOP。初衷是进行有界本地方法交叉检查，但本回执按保守口径明确记录执行控制偏差，不追认STOP例外，不回填假停止时间。8例数据和计数全部保留。现已将σ阈值与不可自行解除的STOP联动，缺资格时provisionalPASS固定false；禁用旧240min初始化器，避免复位新账。隔离测试先RED再GREEN，修复没有运行新SPICE。
'''+s[end:]
s=s.replace('尚剩DC/AC/PZ79个','尚剩DC/AC/PZ52次')
s=s.replace("'readableCSV':count,","'readableAC_CSV':count,'readableOP_CSV':opcount,")
s=s.replace('fixture和数学/原子预算测试','fixture和数学/原子预算/STOP联动测试、保留的独立终审结果')
p.write_text(s,encoding='utf-8')
dump(R/'evidence'/'FINAL_REVIEW_AND_CORRECTIONS.json',{'reviewer':'mimo_final_review','critical':0,'important':3,'findings':['8 post-threshold diagnostics before manual STOP','49 process cases actually contain 76 OP/AC/PZ analyses','provisional PASS omitted qualification prerequisites'],'corrections':['sticky threshold STOP linked','conservative command recount 76 with original preserved','PASS false pending explicit qualifications','legacy 240min initializer disabled','raw OP readable voltage exports'],'noNewSPICE':True,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()})
print(json.dumps({'processCases':49,'actualDC_AC_PZ':76,'diagnostics':15,'normalTransient':0,'native':0,'scientificSTOP':b['scienceStopped']}))
