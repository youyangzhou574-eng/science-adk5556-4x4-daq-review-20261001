from floorplan_core import *
import csv,hashlib
base=json.loads((P/'BASELINE_P1_FULL_PLACEMENT.json').read_text());final=json.loads((P/'LOCAL_FINAL_FULL101_PLACEMENT.json').read_text());before=base['positions'];after=final['positions'];targets=json.loads((P/'FUNCTIONAL_TARGET_REGISTER.json').read_text());rows=[]
for r,ee in targets.items():
 for a,owner,n,kind in ee:
  assert net(r,a)is not None and net(r,a)==net(owner,n)
  old=dist(pad(r,a,before[r]),pad(owner,n,before[owner]));new=dist(pad(r,a,after[r]),pad(owner,n,after[owner]))
  rows.append({'ref':r,'pad':a,'owner':owner,'ownerPin':n,'net':net(r,a),'kind':kind,'beforeMm':old,'afterMm':new,'deltaMm':new-old})
with(P/'ALL172_FUNCTIONAL_EDGES_BEFORE_AFTER.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
frozen=[]
for r in ['U2','U5']+['RF'+str(i)for i in range(4)]+['CF'+str(i)for i in range(4)]+['R_ADC'+str(i)for i in range(4)]+['C_ADC'+str(i)for i in range(4)]+[r for v in base['banks'].values()for tier in v['tiers']for r in tier]:
 assert before[r]==after[r];frozen.append(r)
assert len(frozen)==34
channel=[]
for i in range(4):
 rr=[q for q in rows if q['ref']=='R_ADC'+str(i)];assert len(rr)==2 and all(abs(q['deltaMm'])<1e-12 for q in rr)
 channel.append({'channel':i,'TIA_RADC_ADCtwoStubSumMm':sum(q['afterMm']for q in rr),'unchanged':True})
companions=[q for q in rows if q['ref']in ['RD_TOP','RD_B1','C_DIV']]
with(P/'VEX_DIVIDER_COMPANION_EDGES_BEFORE_AFTER.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(companions)
flags={'frozen34ADC_TIAExactCoordinates':frozen,'channelsInherited':channel,'meanTIA_RADC_ADCStubMm':sum(q['TIA_RADC_ADCtwoStubSumMm']for q in channel)/4,'maxTIA_RADC_ADCStubMm':max(q['TIA_RADC_ADCtwoStubSumMm']for q in channel),'newNativeOrPerformanceQualification':False,'VEXCompanionProxyChanges':companions}
(P/'FROZEN_ANALOG_AND_COMPANION_COMPARISON.json').write_text(json.dumps(flags,indent=2),encoding='utf-8')
print(json.dumps(flags))
