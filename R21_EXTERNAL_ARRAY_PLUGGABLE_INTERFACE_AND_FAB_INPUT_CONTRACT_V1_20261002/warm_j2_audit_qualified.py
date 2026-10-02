from pathlib import Path
import json,collections
P=Path(__file__).parent
A=json.loads((P/'BASELINE_J2_BATCH.json').read_text('utf8'))['parsed']['value'];B=json.loads((P/'WARM_J2_BATCH.json').read_text('utf8'))['parsed']['value']
def rec(s):
 out=[]
 for l in s.splitlines():
  if '||' in l:
   h,q=l.split('||',1)
   try:out.append((json.loads(h),json.loads(q.rstrip('|'))))
   except ValueError:pass
 return out
def mult(rs,t):return collections.Counter(json.dumps([h['id'],q],sort_keys=True) for h,q in rs if h['type']==t)
a,b=A['pcb'],B['pcb'];pa={c['ref']:c for c in a['parts']};pb={c['ref']:c for c in b['parts']}
core={r:pa[r]==pb[r] for r in pa if r!='J2'}
net=lambda p:{(c['ref'],v['number']):v['net']for c in p['parts']for v in c['pads']}
ra,rb=rec(a['source']),rec(b['source']);copper={t:mult(ra,t)==mult(rb,t)for t in('LINE','VIA','POUR','PAD_NET')}
sc={}
for x,y in zip(A['schematic']['pages'],B['schematic']['pages']):
 ids={q['id'] for q in x['parts'] if q['ref']=='J2'}
 def filtered(s):
  out=[]
  for h,q in rec(s):
   if h.get('id') in ids or q.get('parentId') in ids:continue
   q=dict(q)
   if h['type']=='DOCHEAD':
    for key in ('client','updateTime','version'):q.pop(key,None)
   out.append(json.dumps([h['type'],h.get('id'),q],sort_keys=True))
  return collections.Counter(out)
 sc[x['page']['name']]=filtered(x['source'])==filtered(y['source'])
j=pb['J2'];coords={v['number']:(v['x'],v['y'],v['rotation'],v['layer']) for v in j['pads']};oldcoords={v['number']:(v['x'],v['y'],v['rotation'],v['layer'])for v in pa['J2']['pads']}
drc=json.loads((P/'WARM_J2_DRC.json').read_text('utf8'))['parsed'];r={'stage':'WARM','parts':len(pb),'pads':len(net(b)),'assigned':sum(bool(v)for v in net(b).values()),'nets':len({v for v in net(b).values()if v}),'NC':sum(not v for v in net(b).values()),'other175Core':all(core.values()),'other175Differences':[x for x,v in core.items()if not v],'all550PadNetSame':net(a)==net(b),'rulesSame':a['rules']==b['rules'],'primaryCopperSame':copper,'otherSchematicSourceSameExcluding3TransportHeaderFields':sc,'headerExclusions':['DOCHEAD.client','DOCHEAD.updateTime','DOCHEAD.version'],'J2positionSame':all(pa['J2'][k]==j[k]for k in('x','y','rotation','layer','uniqueId')),'J2padCoordinatesSame':coords==oldcoords,'J2name':j['name'],'J2footprint':j['footprint'],'J2pins':net(b)|{},'DRCempty':drc.get('ok') and drc.get('value')==[]}
r.pop('J2pins');r['PASS']=all((r['other175Core'],r['all550PadNetSame'],r['rulesSame'],all(copper.values()),all(sc.values()),r['J2positionSame'],r['J2padCoordinatesSame'],r['DRCempty'],j['name']=='1718560008',j['footprint']['name']=='MOLEX_1718560008_MFR_SD171856_R17',(r['parts'],r['pads'],r['assigned'],r['nets'],r['NC'])==(176,550,514,107,36)))
(P/'WARM_GATE.json').write_text(json.dumps(r,indent=2),'utf8');(P/'WARM_PCB.json').write_text(json.dumps(b,ensure_ascii=False),'utf8');(P/'WARM_SCHEMATIC.json').write_text(json.dumps(B['schematic'],ensure_ascii=False),'utf8');(P/'WARM_PCB_SOURCE.txt').write_text(b['source'],'utf8');print(json.dumps(r))
if not r['PASS']:raise SystemExit('STOP_SCOPE_OR_NET_DRIFT: inspect actual differences before any further CAD')
