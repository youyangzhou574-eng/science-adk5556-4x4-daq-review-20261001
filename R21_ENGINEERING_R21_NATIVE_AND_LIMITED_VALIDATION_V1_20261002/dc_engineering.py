"""Bounded ideal DC screening, not a macro model or precision certificate."""
import numpy as np,csv,json
from budget import ROOT,charge
patterns={f'all_{r}':np.full((4,4),float(r)) for r in [800,1000,3300,7000,8000]}
patterns['checker_1k_7k']=np.array([[1000 if (i+j)%2==0 else 7000 for j in range(4)] for i in range(4)],float)
for name,base,target in [('target7k_neighbors1k',1000,7000),('target1k_neighbors7k',7000,1000),('single_plus10pct',3300,3630)]:
 a=np.full((4,4),float(base));a[0,0]=target;patterns[name]=a
a=np.full((4,4),3300.);a[0,:]*=1.1;patterns['row_plus10pct']=a
charge('offline','10 matrices x 4 selected rows ideal DC',40)
records=[]
for name,a in patterns.items():
 for row in range(4):
  currents=.25/a[row,:];tap=2.5+4990*currents;ain=tap/(1+100/1e6)
  drv=tap+1000*(currents+tap/(100+1e6));row_drv=2.25-1000*sum(currents)
  for col in range(4):
   records.append(dict(pattern=name,row=row,col=col,R_ohm=a[row,col],sensor_uA=currents[col]*1e6,TIA_tap_V=tap[col],ADC_V=ain[col],TIA_driver_V=drv[col],ROW_driver_V=row_drv,code_ideal=ain[col]/5.12*65536,rail4p75_driver_margin_V=4.75-drv[col],guardband=bool(np.any((a<1000)|(a>7000))),precision_status='BENCH_PENDING'))
with (ROOT/'DC_ENGINEERING_40_GROUPS.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=records[0].keys());w.writeheader();w.writerows(records)
delta=[]
for r in [1000,3300,7000]:
 v0=(2.5+4990*.25/r)/(1+100/1e6);v1=(2.5+4990*.25/(r*1.1))/(1+100/1e6)
 delta.append({'R_ohm':r,'delta10pct_V':v1-v0,'delta10pct_codes':(v1-v0)/5.12*65536,'scope': 'ideal signal size only; 7000->7700 is guardband'})
s={'scope':'40 ideal selected-row DC groups / 160 cell outputs; exact virtual grounds, no line R/opamp offsets/clamp leakage/ADC INL; not new SPICE','max_TIA_driver_V':max(x['TIA_driver_V'] for x in records),'min_ROW_driver_V':min(x['ROW_driver_V'] for x in records),'ADC_min_V':min(x['ADC_V'] for x in records),'ADC_max_V':max(x['ADC_V'] for x in records),'max_sensor_uA':max(x['sensor_uA'] for x in records),'delta10pct':delta,'normal_clipping':False,'guardband_current_power':'ideal sensor max78.125uW at800; no fault/thermal certification','bleed5p25_99ohm_W':5.25**2/99,'acceptance':'native entry screening only; goals mean<=1%, frame repeatability<=0.2% BENCH_PENDING'}
assert all(0<x['ADC_V']<5.12 and 0<x['ROW_driver_V']<4.75 and x['TIA_driver_V']<4.75 for x in records)
(ROOT/'DC_ENGINEERING_SUMMARY.json').write_text(json.dumps(s,indent=2)+'\n','utf8');print(json.dumps(s))
