import itertools,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
rows=[]
for vdd,ext,rs,rp,ileak in itertools.product([3.065,3.6],[0,.2],[4990*.99,4990*1.01],[47000*.99,47000*1.01],[-5e-6,5e-6]):
 vin=(vdd/rp+ext/rs+ileak)/(1/rp+1/rs)
 rows.append({'vdd':vdd,'external_low':ext,'series_ohm':rs,'pullup_ohm':rp,'gate_input_leak_A':ileak,'input_low_V':vin})
rec={'corner_count':len(rows),'input_low_max_V':max(x['input_low_V']for x in rows),'disconnected_high_min_V':3.065-5e-6*47000*1.01,'NRST_VIL_min_V':.3*3.065,'reset_sink_load_upper_A':3.6/(10000*.99)+3.6/25000+30e-6,'G07_VOL_reference_V':.4,'off_external_positive_V3_upper_V':5.5*100/(4990*.99+47000*.99+100)+30e-6*100,'negative_fault_current_upper_A':5.5/(4990*.99),'old_divider_nominal_V':3.3*4990/(10000+4990),'status':'DIVIDER_CONFLICT_REMOVED_IN_CANDIDATE; FULL_RESET_GATE_HOLD','holds':['Schmitt threshold guaranteed envelope for entire rail range not explicitly available in source table','normal open drain leakage/release allocation not independently guaranteed','negative fault comparison is absolute current limit, not continuous thermal proof'],'corners':rows}
(ROOT/'results/RESET_CORNERS.json').write_text(json.dumps(rec,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in rec.items()if k!='corners'},indent=2))
if __name__=='__main__':pass
