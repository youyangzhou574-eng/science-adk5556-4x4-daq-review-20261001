from pathlib import Path
import json
P=Path(__file__).parent
(P/'DEFERRED_MINOR_LEDGER.md').write_text('''# 唯一终审Minor记录，不扩实施

M01 J2_FOOTPRINT_DIMENSION_CHECK.json中的nativeAssociationAndWarmColdPending是历史阶段值；最终以WARM_GATE.json和COLD_QUALIFIED_GATE.json为当前工程资格，不改历史。

M02 8针CSV使用API捕获舍入x196.9mil，body来自component x196.8504mil，约0.00126mm展示差；示意图/CSV不作为精密制造坐标，精确原生File保留。无第二review/工具修理。

Important I01仅一次文档修复披露原生ROWCOL文字缺项，原生不变；已列J2_ECO_CONFORMANCE_HOLD并集中请求接受mandatory图或新最小补字预算，尚未批准替代。
''','utf8')
b=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'));b['finalReview']={'Critical':0,'Important':1,'ImportantDisposition':'One documentation disclosure fix; physical silk text still missing, new unified decision required','Minor':2,'minorDisposition':'deferred ledger, no native rework or second review'};(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),'utf8')
assert 'J2_ECO_CONFORMANCE_HOLD' in (P/'COMPLETE_J2_INTERFACE_RECEIPT.md').read_text('utf8');assert json.loads((P/'GATES.json').read_text('utf8'))['J2_ECO_CONFORMANCE_HOLD']
print('Single Important document fix statically confirmed, native unchanged; Minor retained')
