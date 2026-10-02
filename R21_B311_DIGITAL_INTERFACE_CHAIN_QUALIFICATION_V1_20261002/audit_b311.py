from b31_core import *
from digital_chain import series_paths
import hashlib
def csvout(n,rows):
 with (P/n).open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def audit():
 pos=json.loads((P/'PLACEMENT_B31.json').read_text())['positions'];assert set(pos)==set(G)
 pads=[{'ref':r,'pad':p['number'],'net':p['net'],'xy':list(newpad(r,p,pos[r]))} for r in sorted(G) for p in G[r]['pads']]
 resistors=sorted(r for r in G if r.startswith(('R_J3_','R_J4_')))
 paths=series_paths(pads,['U7'],['J3','J4'],resistors)
 # Seven actual series entries = five real signal/reset + two supply-sense reference paths.
 expected={'R_J3_3':('U7.24','J3.3','SWDIO','SWDIO_EXT'),'R_J3_4':('U7.25','J3.4','SWCLK','SWCLK_EXT'),'R_J3_5':('U7.6','J3.5','PGOOD','MCU_NRST_EXT'),'R_J4_3':('U7.19','J4.3','UART_TX','UART_TX_EXT'),'R_J4_4':('U7.21','J4.4','UART_RX','UART_RX_EXT')}
 signal=[q for q in paths if q['resistor'] in expected];supply=[q for q in paths if q['resistor'] not in expected]
 assert len(signal)==5 and {q['resistor'] for q in signal}==set(expected)
 for q in signal:
  ex=expected[q['resistor']];assert (q['orderedNodes'][0],q['orderedNodes'][-1],q['insideNet'],q['outsideNet'])==ex
 spi=[math.dist(pt(pos,'U5',a),pt(pos,'U7',b)) for a,b in [(1,14),(36,13),(37,12),(38,11)]]
 assert all(pd('U5',a)['net']==pd('U7',b)['net'] for a,b in [(1,14),(36,13),(37,12),(38,11)])
 baseScale=max(float(np.mean(spi)),max(math.dist(pos['U7'][:2],pos[j][:2]) for j in ['J3','J4']))
 for q in signal:q.update({'scaleReferenceMm':baseScale,'lengthScreenLimitMm':2*baseScale+5,'stretchLimit':2,'screenPass':q['stretch'] is not None and q['stretch']<=2 and q['functionalLengthWithResistorSpanMm']<=2*baseScale+5})
 for q in supply:q.update({'use':'rail sense reference only, not source power; U7.4 just sameV3V3 node, not driver','partValueOhm':4990})
 save('DIGITAL_INTERFACE_CHAIN_AUDIT.json',{'signalPaths':signal,'supplySenseReferencePaths':supply,'seriesRefsAll7':resistors,'screenDefinition':'predeclared qualitativeProinterpretation: stretch<=2 includingRspan, total<=2*max(meanactualSPI,MCU-interfacecentre scales)+5mm, exactsame-net two-wire legs; not electrical/performance qualification','meanSPIActualMm':float(np.mean(spi)),'SPIActual4Mm':spi,'scaleReferenceMm':baseScale,'completeSignal5':True,'allSignalsScreenPass':all(q['screenPass'] for q in signal),'oldMacroScoresRewritten':False,'oldRankingCoverageChanged':False})
 csvout('DIGITAL_INTERFACE_CHAINS.csv',[{k:v for k,v in q.items() if k!='orderedNodes'}|{'node1':q['orderedNodes'][0],'node2':q['orderedNodes'][1],'node3':q['orderedNodes'][2],'node4':q['orderedNodes'][3]} for q in signal])
 branch=[]
 for r,p in [('U11',6),('U12',6),('U15',2)]:
  assert pd(r,p)['net']==pd('U7',6)['net']==pd('R_J3_5',2)['net']=='PGOOD'
  branch.append({'from':r+'.'+str(p),'net':'PGOOD','toMCU':'U7.6','straightToMCUMm':math.dist(pt(pos,r,p),pt(pos,'U7',6)),'toInterfaceInside':'R_J3_5.2','straightToInterfaceRMm':math.dist(pt(pos,r,p),pt(pos,'R_J3_5',2)),'meaning':'same-net NRST/PGOOD monitor-Schmitt branch geometry; driver direction, timing/reset/fault qualification not inferred'})
 save('NRST_PGOOD_BRANCH_AUDIT.json',branch)
 protections=[]
 for r in sorted(G):
  if r.startswith(('D_J3_','D_J4_')):
   protections.append({'ref':r,'signalPad3Net':pd(r,3)['net'],'GNDpad1Net':pd(r,1)['net'],'railPad2Net':pd(r,2)['net'],'toSameNetInsideSeriesPins':[rr+'.'+p['number'] for rr in resistors for p in G[rr]['pads'] if p['net']==pd(r,3)['net']],'note':'clamp not treated as series conductor toGND/V3V3; does not close protection fault qualification'})
 save('DIGITAL_PROTECTION_BRANCH_REGISTER.json',protections)
 shapes={r:physical(r,v) for r,v in pos.items()};bodies={r:body(r,v) for r,v in pos.items()};coll=[];bcoll=[];minGap=999;npairs=0
 for a,b in itertools.combinations(sorted(pos),2):
  npairs+=1;minGap=min(minGap,shapes[a].distance(shapes[b]))
  if shapes[a].intersection(shapes[b]).area>1e-8:coll.append([a,b])
  if bodies[a].intersection(bodies[b]).area>1e-8:bcoll.append([a,b])
 kr=[]
 for k in keys:
  d=math.dist(pt(pos,k['ic'],k['icPad']),pt(pos,k['passive'],k['passivePad']));kr.append(k|{'actualMm':d,'deltaMm':d-k['limit'],'passNoIncrease':d<=k['limit']+1e-6})
 csvout('KEY106_FRESH_AUDIT.csv',kr)
 # Independently recompute each savedrole geometry; register denotes expected complete set.
 register=json.loads((P/'CHANNEL_CELL_REGISTER.json').read_text());fExpected={'TIA':{'HF','SENSE','ISO','RF','CF','CLAMP'},'ROW':{'HF','SENSE','ISO','CLAMP'}};ch=[]
 for f,rs in fExpected.items():
  sub=[x for x in register if x['family']==f];assert len(sub)==4*len(rs)
  assert {(x['channel'],x['role']) for x in sub}==set(itertools.product(range(4),rs))
  ic='U2' if f=='TIA' else 'U1'
  for x in sub:
   i=x['channel'];a=(pt(pos,ic,[1,7,8,14][i])+pt(pos,ic,[2,6,9,13][i]))/2;s=np.array([1 if i<2 else -1,-1 if i in [0,3] else 1]);centre=(np.array(pos[x['ref']][:2])-a)*s
   ch.append({'family':f,'channel':i,'role':x['role'],'ref':x['ref'],'actualCanonicalCentreMm':centre.tolist(),'expectedCanonicalCentreMm':x['canonicalCentreMm'],'centreDeviationMm':float(np.linalg.norm(centre-x['canonicalCentreMm'])),'angleUnchanged':pos[x['ref']][2]==x['rotation'],'pass':np.linalg.norm(centre-x['canonicalCentreMm'])<1e-5 and pos[x['ref']][2]==x['rotation']})
 save('CHANNEL_REPEATABILITY_FRESH_AUDIT.json',ch)
 physicalMaxX=max(s.bounds[2] for s in shapes.values());edge=[]
 for r in ['J3','J4']:
  bb=shapes[r].bounds;edge.append({'ref':r,'centreX':pos[r][0],'rightPhysicalEdgeX':bb[2],'allGeometryRightEdgeX':physicalMaxX,'edgeInsetMm':physicalMaxX-bb[2],'passPlanningRightEdge':physicalMaxX-bb[2]<=2})
 save('INTERFACE_RIGHT_EDGE_AUDIT.json',edge)
 manifest=json.loads((P/'INPUT_MANIFEST.json').read_text());hashes=[]
 for v in manifest:
  src=hashlib.sha256(Path(v['source']).read_bytes()).hexdigest().upper();copy=hashlib.sha256((P/v['copy']).read_bytes()).hexdigest().upper();hashes.append(v|{'sourceNowSHA':src,'copyNowSHA':copy,'pass':src==copy==v['SHA256']})
 save('INPUT_SHA_VERIFICATION.json',hashes)
 ncs=[p for p in pads if not p['net']];count={'parts':len(pos),'pads':len(pads),'assigned':sum(bool(p['net']) for p in pads),'nets':len({p['net'] for p in pads if p['net']}),'ordinaryNC':sum(p['ref']!='J2' for p in ncs),'mechanicalEmpty':sum(p['ref']=='J2' for p in ncs)}
 j2={p['pad']:p['net'] for p in pads if p['ref']=='J2'};assert j2=={**{str(i+1):'ROW'+str(i) for i in range(4)},**{str(i+5):'COL'+str(i) for i in range(4)},'MP1':'','MP2':''}
 out=count|{'pairCount':npairs,'bodyCollisionPairs':bcoll,'physicalProxyCollisionPairs':coll,'minGapMm':minGap,'key106NoIncrease':all(x['passNoIncrease'] for x in kr),'keyMaxDeltaMm':max(x['deltaMm'] for x in kr),'channelRepeatability':all(x['pass'] for x in ch),'signal5ScreenPass':all(x['screenPass'] for x in signal),'rightEdgePass':all(x['passPlanningRightEdge'] for x in edge),'all18SourceCopySHAUnchanged':all(x['pass'] for x in hashes),'coordinatesChanged':False,'macroCandidateCount':0,'CAD_RELEASED':False,'USER_VISUAL_ACCEPTANCE':'PENDING','oldScoreRankingQualification':False,'actualDigitalFunctionalChainQualification':'READONLY_GEOMETRY_ONLY'}
 out['readOnlyQualificationPass']=count=={'parts':176,'pads':552,'assigned':514,'nets':107,'ordinaryNC':36,'mechanicalEmpty':2} and not(coll or bcoll) and all(out[k] for k in ['key106NoIncrease','channelRepeatability','signal5ScreenPass','rightEdgePass','all18SourceCopySHAUnchanged'])
 save('FINAL_READONLY_AUDIT.json',out);print(json.dumps({'digitalPaths':signal,'edge':edge,'summary':out}))
if __name__=='__main__':audit()
