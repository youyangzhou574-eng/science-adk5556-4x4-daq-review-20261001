from pathlib import Path
import json
P=Path(__file__).resolve().parent
before={}
for name in ['TIMING_CAPTURE_PLAN.md','COMPLETE_BENCH_PREP_RECEIPT.md','build_preparation.py','finish_preparation.py']:
 p=P/name;s=p.read_text('utf8');before[name]='4通道×9次×25us=1200us' in s
 s=s.replace('每状态4通道×9次×25us=1200us','每状态先等待300us，再4通道×9次×25us=900us，合计1200us')
 s=s.replace('每状态4×9×25us、9600us+400us','每状态900us采集+300us等待=1200us、8状态9600us+400us')
 p.write_text(s,'utf8')
p=P/'ACCEPTED_SCHEMATIC_BASELINE.md';s=p.read_text('utf8');records=json.loads((P/'ACCEPTED_BASELINE_SHA.json').read_text('utf8'))['records']
base='https://github.com/youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001'
c='fbb7c0ed5f322f078583fadbdb353efe835e4c01';folder='R21_FINAL_INTERFACE_ANNOTATION_AND_BENCH_READINESS_V1_20261002'
s+='\n## 强制配套和完整实际证据的固定链接\n\n[已接受基线目录]('+base+'/tree/'+c+'/'+folder+')。以下全部固定在同一接受版本；本准备包不复制原生。\n\n'
for r in records:
 n=r['baseline_relative_path'];s+='- ['+n+']('+base+'/blob/'+c+'/'+folder+'/'+n+')\n'
p.write_text(s,'utf8')
for name in ['COMPLETE_BENCH_PREP_RECEIPT.md','finish_preparation.py']:
 p=P/name;s=p.read_text('utf8');s=s.replace('允许的真实上电次数、每次供电时间、限流和硬断电门必须由release具体裁定后登记；','集中拟议上限3次正常空载供电、每次<=15s、累计<=45s（不是60s热应力试验），仅供Pro按实体条件评估；任一异常第一次即停、不自动重试。最终允许次数/时长、限流和硬断电门必须由release具体裁定后登记；');p.write_text(s,'utf8')
p=P/'COMPLETE_BENCH_PREP_RECEIPT.md';s=p.read_text('utf8').replace('单次fresh-context终审结果见FINAL_REVIEW.md。','单次fresh-context终审Critical0/Important2（等待300us加法漏写、基线配套固定URL缺失）/Minor0，已在一次文档pass修正并静态核对；原冻结源未改、没有二次review或新增科学测试。详见FINAL_REVIEW.md/FINAL_REVIEW_DOCUMENT_FIX_CHECK.json。');p.write_text(s,'utf8')
check={'beforeTimingWordingBad':before['TIMING_CAPTURE_PLAN.md'],'afterTimingExplicit300Plus900': '合计1200us' in (P/'TIMING_CAPTURE_PLAN.md').read_text('utf8'),'receiptExplicit300Plus900':'900us采集+300us等待=1200us' in (P/'COMPLETE_BENCH_PREP_RECEIPT.md').read_text('utf8'),'fixedBaselineURLsPresent':all('/blob/'+c+'/'+folder+'/'+r['baseline_relative_path'] in (P/'ACCEPTED_SCHEMATIC_BASELINE.md').read_text('utf8') for r in records),'links':len(records),'frozenSourcesEdited':False,'extraScientificTests':0,'secondReview':False}
assert all(check[k] for k in ['beforeTimingWordingBad','afterTimingExplicit300Plus900','receiptExplicit300Plus900','fixedBaselineURLsPresent'])
(P/'FINAL_REVIEW_DOCUMENT_FIX_CHECK.json').write_text(json.dumps(check,indent=2)+'\n','utf8');print(json.dumps(check))
