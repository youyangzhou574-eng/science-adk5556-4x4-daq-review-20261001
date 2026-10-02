from floorplan_core import *
import csv,hashlib
TARGET=json.loads((P/'FUNCTIONAL_TARGET_REGISTER.json').read_text(encoding='utf-8'))
summary={};rows=[]
for name in ['P1','P2']:
 q=json.loads((P/(name+'_PASS3_PARTIAL.json')).read_text(encoding='utf-8'));pos=q['positions'];missing=sorted(set(G)-set(pos));audit=allpairs(pos)
 icpads=sum(len(G[r]['pads'])for r in pos);fully=[]
 for r,edges in TARGET.items():
  for n,ic,pin,role in edges:
   if r not in pos or ic not in pos:
    rows.append([name,r,n,ic,pin,role,net(r,n),net(ic,pin),'','UNPLACED']);continue
   assert net(r,n)==net(ic,pin),(r,n,ic,pin)
   length=dist(pad(r,n,pos[r]),pad(ic,pin,pos[ic]));rows.append([name,r,n,ic,pin,role,net(r,n),net(ic,pin),length,'ACTUAL_SAME_NET_EUCLIDEAN_PROXY_NOT_ROUTED'])
  if r in pos:fully.append(r)
 outline=box(0,0,50,50);jc=pos['J2'][1];keep=box(-10,jc-8,8,jc+8)
 violations=[r for r,v in pos.items()if r!='J2'and shape(r,v).intersects(keep)]
 outboard=[r for r,v in pos.items()if not outline.covers(shape(r,v))]
 feedback=[];filters=[]
 for i,(out,minus)in {0:[1,2],1:[7,6],2:[8,9],3:[14,13]}.items():
  entry={'channel':i,'feedback':[]}
  for t in ['RF','CF']:
   r=t+str(i);e=TARGET[r];stub=sum(dist(pad(r,x[0],pos[r]),pad(x[1],x[2],pos[x[1]]))for x in e);entry['feedback'].append({'ref':r,'twoLeadStubSumMm':stub})
  feedback.append(entry)
  ra='R_ADC'+str(i);cc='C_ADC'+str(i);ain=[16,18,21,23][i]
  filters.append({'channel':i,'RIAtoADCPinStubSumMm':sum(dist(pad(ra,x[0],pos[ra]),pad(x[1],x[2],pos[x[1]]))for x in TARGET[ra]),'filterCapSignalPadToAINmm':dist(pad(cc,next(t['number']for t in G[cc]['pads']if t['net']==net('U5',ain)),pos[cc]),pad('U5',ain,pos['U5']))})
 summary[name]={'status':'PARTIAL_NOT_VALID_FULL_PLACEMENT','plannedBoardMm':[50,50],'aspectRatio':1.,'actualPlacedCount':len(pos),'actualAllIdentities':101,'unplaced':missing,'placedPhysicalPads':icpads,'all363PinMapFrozen':True,'actualPartialPairs':audit,'all5050PairQualification':False,'FFCReserveViolation':violations,'outsidePlanningBoard':outboard,'feedbackStubMetrics':feedback,'filterSignalMetrics':filters,'J2Geometry':'conservative FFC14x7 placeholder; signaltaildatum/range not manufacturer qualified','nativeCADDRCPerformed':False,'globallyShortestRoutingProven':False}
 assert not audit['physicalProxyCollisions']and not audit['bodyCollisions']and not violations and not outboard
(P/'PARTIAL_PLACEMENT_AUDIT.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
with(P/'FUNCTIONAL_PIN_DISTANCE_PARTIAL.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.writer(f);w.writerow(['candidate','part','pin','owner','ownerPin','role','partNet','ownerNet','distanceMm','status']);w.writerows(rows)
with(P/'ALL_PLACED_AND_UNPLACED_101.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.writer(f);w.writerow(['candidate','ref','status','xMm','yMm','rotation','footprintUUID','actualSCHpinCount'])
 for name in ['P1','P2']:
  pos=json.loads((P/(name+'_PASS3_PARTIAL.json')).read_text())['positions']
  for r in sorted(G):w.writerow([name,r,'PLACED'if r in pos else'UNPLACED',*(pos[r]if r in pos else['','','']),G[r]['footprintUuid'],len(G[r]['pads'])])
checks=[]
for row in json.loads((P/'INPUT_MANIFEST.json').read_text()):
 source=Path(row['path']);copy=P/row['localCopy'];checks.append({'path':row['path'],'SHA256':row['sha256'],'originalStillSame':hashlib.sha256(source.read_bytes()).hexdigest().upper()==row['sha256'],'copyStillSame':hashlib.sha256(copy.read_bytes()).hexdigest().upper()==row['sha256']})
assert all(r['originalStillSame']and r['copyStillSame']for r in checks)
(P/'INPUT_SHA_VERIFICATION.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps({name:{'placed':q['actualPlacedCount'],'unplaced':len(q['unplaced']),'partialPairs':q['actualPartialPairs']['pairs'],'full5050Pass':False}for name,q in summary.items()}))
