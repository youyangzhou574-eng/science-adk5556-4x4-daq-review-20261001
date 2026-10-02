from floorplan_core import *
import csv
rows=[];summaries=[]
edges=[]
def edge(label,a,ap,b,bp):
 assert net(a,ap) is not None and net(a,ap)==net(b,bp),(label,a,ap,b,bp)
 edges.append([label,a,str(ap),b,str(bp),net(a,ap)])
edge('ROW_DRIVER_TO_MUX','U1',1,'U4',8);edge('MUX_FEEDBACK_TO_ROW_AMP','U4',9,'U1',4)
for i in range(4):
 edge('FFC_ROW'+str(i),'J2',i+1,'U4',[4,5,6,7][i]);edge('FFC_COL'+str(i),'J2',i+5,'U2',[2,6,9,13][i])
for name,a,ap,b,bp in [('MOSI','U5',1,'U7',14),('MISO','U5',36,'U7',13),('SCLK','U5',37,'U7',12),('CS','U5',38,'U7',11),('POWERINPUT','J1',1,'U9',5),('POWERLDO','U9',6,'U8',6),('ENABLE','U11',6,'U8',4),('RESET','U12',6,'U7',6)]:edge(name,a,ap,b,bp)
for r,ic,pin in [('R_J3_3','U7',24),('R_J3_4','U7',25),('R_J3_5','U7',6),('R_J4_3','U7',19),('R_J4_4','U7',21)]:
 edge(r+'_MCU','U7',pin,r,2);j='J3'if r.startswith('R_J3')else'J4';edge(r+'_EXTERNAL',r,1,j,int(r[-1]))
partial=json.loads((P/'PARTIAL_PLACEMENT_AUDIT.json').read_text())
for name in ['P1','P2']:
 pos=json.loads((P/(name+'_PASS3_PARTIAL.json')).read_text())['positions']
 for label,a,ap,b,bp,nn in edges:rows.append([name,label,a,ap,b,bp,nn,dist(pad(a,ap,pos[a]),pad(b,bp,pos[b])),'EUCLIDEAN_ONLY_NOT_COPPER'])
 metrics=partial[name];sums=[v['RIAtoADCPinStubSumMm']for v in metrics['filterSignalMetrics']];fb=[q['twoLeadStubSumMm']for c in metrics['feedbackStubMetrics']for q in c['feedback']]
 summaries.append([name,50,50,1.,metrics['actualPlacedCount'],len(metrics['unplaced']),sum(sums)/4,max(sums),min(fb),max(fb),'PARTIAL_NOT_SELECTABLE'])
with(P/'REPRESENTATIVE_ACTUAL_PIN_CHAIN_COMPARISON.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.writer(f);w.writerow(['candidate','role','fromRef','fromPin','toRef','toPin','actualSameNet','distanceMm','evidenceBoundary']);w.writerows(rows)
with(P/'CANDIDATE_COMPARISON.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.writer(f);w.writerow(['candidate','planningWidthMm','planningHeightMm','aspect','placed','unplaced','meanTIA_RADC_ADCPinStubSumMm','maxTIA_RADC_ADCPinStubSumMm','minRF_CFtwoLeadStubSumMm','maxRF_CFtwoLeadStubSumMm','status']);w.writerows(summaries)
print(json.dumps({'sameNetRepresentativeEdges':len(edges),'summary':summaries}))
