from placement_geometry import *
import csv,itertools,hashlib
B=json.loads((P/'PLACEMENT_B21.json').read_text());N=json.loads((P/'PLACEMENT_B22.json').read_text())
old=B['positions'];pos=N['positions'];results={}
assert set(pos)==set(G)and len(G)==176
pads=[(r,str(v['number']),v['net'])for r in sorted(G)for v in G[r]['pads']]
assert len(pads)==552
results['identity']={'components':len(G),'pads':len(pads),'assigned':sum(bool(v[2])for v in pads),'nets':len(set(v[2]for v in pads if v[2])),'ordinaryNC':sum(not v[2]and v[1]not in ('MP1','MP2')for v in pads),'mechanicalEmpty':[v for v in pads if not v[2]and v[1]in('MP1','MP2')]}
results['inputSHA']=[]
for r in json.loads((P/'INPUT_MANIFEST.json').read_text()):
 actual=hashlib.sha256(Path(r['source']).read_bytes()).hexdigest(); copied=hashlib.sha256((P/r['name']).read_bytes()).hexdigest()
 # placement_geometry.py local copy can change only if documented; currently identical.
 assert actual==r['SHA256']and copied==r['SHA256']
 results['inputSHA'].append(dict(r,sourceAndCopyUnchanged=True))
results['macroICandInterfaceFrozen']=all(tuple(old[r])==tuple(pos[r])for r in G if(r.startswith('J')and'_'not in r)or(r.startswith('U')and'_'not in r))
assert results['macroICandInterfaceFrozen']
overlap={}
for name,func in [('body',body),('physicalProxy',physical)]:
 ss={r:func(r,pos[r])for r in G}
 overlap[name]=[{'a':r,'b':s,'areaMm2':ss[r].intersection(ss[s]).area}for r,s in itertools.combinations(sorted(G),2)if ss[r].intersection(ss[s]).area>1e-8]
assert not overlap['body']and not overlap['physicalProxy'];results['overlap']=overlap;results['allPairsEach']=15400
rows=list(csv.DictReader((P/'KEY_PIN_DISTANCE_B22.csv').open(encoding='utf-8-sig')))
for r in rows:
 q,s=r['icRef'],r['passiveRef'];qp=next(v for v in G[q]['pads']if str(v['number'])==r['icPad']);sp=next(v for v in G[s]['pads']if str(v['number'])==r['passivePad'])
 actual=math.dist(newpad(q,qp,pos[q]),newpad(s,sp,pos[s]))
 assert abs(actual-float(r['B22Mm']))<1e-8 and actual<=float(r['B21Mm'])+1e-6
results['94ActualPinDistances']={'count':len(rows),'maximumIncreaseMm':max(float(r['B22MinusB21Mm'])for r in rows),'minimumDeltaMm':min(float(r['B22MinusB21Mm'])for r in rows)}
# Additional real-net direct pin-local checks for IC decaps not in the inherited94.
extra=[]
for q,s in [('U4','C_MUX'),('U13','C_U13'),('U14','C_U14'),('U15','C_U15'),('U11','U11_VDD_C'),('U11','U11_SENSE_C'),('U11','U11_CT_C'),('U12','U12_VDD_C'),('U12','U12_SENSE_C'),('U12','U12_CT_C')]:
 for sp in G[s]['pads']:
  if not sp['net']or sp['net']=='GND':continue
  matches=[qp for qp in G[q]['pads']if qp['net']==sp['net']]
  if not matches:continue
  for qp in matches:
   a=math.dist(newpad(q,qp,old[q]),newpad(s,sp,old[s]));b=math.dist(newpad(q,qp,pos[q]),newpad(s,sp,pos[s]))
   extra.append(dict(ic=q,icPad=qp['number'],passive=s,passivePad=sp['number'],net=sp['net'],beforeMm=a,afterMm=b,deltaMm=b-a,passNoIncrease=b<=a+1e-6))
results['extraDecapPinLocalChecks']=extra;results['extraDecapAllNoIncrease']=all(x['passNoIncrease']for x in extra)
# Independently verify declared row/mirror coordinates rather than trust metadata.
arraychecks=[]
for t in N['templates']:
 rr=t['refs'];kind=t['kind'];ok=True
 if kind=='EQUAL_PITCH_ROW':
  ax=0 if t['axis']=='x'else 1;other=1-ax
  ok=max(pos[r][other]for r in rr)-min(pos[r][other]for r in rr)<1e-8 and len(set(pos[r][2]for r in rr))==1
  if len(rr)>1:ok=ok and all(abs(pos[rr[i+1]][ax]-pos[rr[i]][ax]-t['pitchMm'])<1e-8 for i in range(len(rr)-1))
 if kind=='PIN_FACING_MIRROR_2_PLUS_2':
  ok=len(set(pos[r][2]for r in rr))==1 and abs(pos[rr[0]][1]-pos[rr[1]][1])<1e-8 and abs(pos[rr[2]][1]-pos[rr[3]][1])<1e-8 and abs(pos[rr[0]][0]-pos[rr[3]][0])<1e-8 and abs(pos[rr[1]][0]-pos[rr[2]][0])<1e-8
 if kind=='FOUR_CHANNEL_TWO_ROW':
  a=rr[:4];b=rr[4:]
  ok=len(set(pos[r][2]for r in rr))==1 and all(abs(pos[a[i]][0]-pos[b[i]][0])<1e-8 for i in range(4))and all(abs(pos[a[i+1]][0]-pos[a[i]][0]-t['pitchXmm'])<1e-8 for i in range(3))and len(set(round(pos[r][1],8)for r in a))==1 and len(set(round(pos[r][1],8)for r in b))==1
 arraychecks.append({'name':t['name'],'kind':kind,'refs':rr,'actualCoordinatePatternPASS':bool(ok)})
assert all(a['actualCoordinatePatternPASS']for a in arraychecks)
results['arrayChecks']=arraychecks
results['scope']={'CAD':0,'nativeDRC':0,'routing':0,'FFCExactActuator':'HOLD','userVisualAcceptance':'PENDING'}
(P/'INDEPENDENT_FINAL_AUDIT.json').write_text(json.dumps(results,indent=2),encoding='utf8')
print(json.dumps({'identity':results['identity'],'geometryPASS':True,'94PASS':True,'extraDecapAllNoIncrease':results['extraDecapAllNoIncrease'],'extraViolations':[x for x in extra if not x['passNoIncrease']],'templates':len(arraychecks)},ensure_ascii=True))

