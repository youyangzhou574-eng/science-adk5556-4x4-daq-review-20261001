"""60 bounded analytic cases. No SPICE/thermal/hardware fault experiment."""
import itertools,csv,json
from science import ROOT,dump
def run():
    rows=[];leak=2e-6+2*.25e-6+5e-6+.07e-6+10e-6
    # Extra 10uA conservatively assigns ST's aggregate pad base leakage to NRST.
    # BAT54S 2uA is guaranteed only at25C; hot-temperature typical curves are NOT bounds.
    for vdd,rs,rpu,rint,sign in itertools.product([3.065,3.6],[990,1010],[9900,10100],[25000,float('inf')],[-1,1]):
        g=1/rs+1/rpu+(0 if rint==float('inf')else 1/rint)
        v=(.4/rs+vdd/rpu+(0 if rint==float('inf')else vdd/rint)+sign*leak)/g
        rows.append({'kind':'external_OD_assert_25C','VDD_V':vdd,'Rseries_Ohm':rs,'RexternalPU_Ohm':rpu,'RinternalPU_Ohm':rint,'leak_A':sign*leak,'NRST_V':v,'threshold_V':.3*vdd,'margin_V':.3*vdd-v,'status':'PASS_SCOPED_25C'})
    for vdd,rpu,rint,sign in itertools.product([3.065,3.6],[9900,10100],[25000,float('inf')],[-1,1]):
        g=1/rpu+(0 if rint==float('inf')else 1/rint);v=vdd+sign*leak/g
        rows.append({'kind':'HiZ_release_25C','VDD_V':vdd,'RexternalPU_Ohm':rpu,'RinternalPU_Ohm':rint,'leak_A':sign*leak,'NRST_V':v,'threshold_V':.7*vdd,'margin_V':v-.7*vdd,'status':'PASS_SCOPED_25C'})
    for vdd,fault,rs in itertools.product([0,3.6],[-5,5],[990,1010]):
        clamp=-.4 if fault<0 else vdd+.4;current=(fault-clamp)/rs
        rows.append({'kind':'fault_current_illustrative_clamp','VDD_V':vdd,'fault_V':fault,'Rseries_Ohm':rs,'assumed_clamp_V':clamp,'resistor_current_A':current,'resistor_power_W':current*current*rs,'status':'CURRENT_BOUND_ONLY_FAULT_PROTECTION_HOLD'})
    for state in ['U11_assert_U12_HiZ','U12_assert_U11_HiZ','both_assert','both_HiZ']:
        current=(3.6-.25)*(1/9900+1/25000)+leak
        rows.append({'kind':'parallel_TPS_OD','state':state,'required_sink_A':current,'guaranteed_sink_test_A':.002,'NRST_V':.25 if state!='both_HiZ' else 3.6,'threshold_V':.9195,'status':'PASS_SCOPED'if current<.002 else'HOLD'})
    assert len(rows)==60
    for row in rows:
        if 'margin_V'in row:assert row['margin_V']>0
    keys=sorted({k for row in rows for k in row})
    with(ROOT/'results'/'RESET_60_CORNERS.csv').open('w',encoding='utf-8',newline='')as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
    assert_rows=[x for x in rows if x['kind']=='external_OD_assert_25C'];release=[x for x in rows if x['kind']=='HiZ_release_25C']
    high=max(x['NRST_V']for x in assert_rows)
    j={'case_count':60,'normal_25C_leak_bound_A':leak,'assert_max_NRST_V':high,'conservative_unpaired_low_threshold_V':.9195,'conservative_unpaired_assert_margin_V':.9195-high,'release_min_margin_V':min(x['margin_V']for x in release),'max_TPS_sink_required_A':rows[-1]['required_sink_A'],'normal_low_high_scope':'SCOPED_25C_ANALYTIC_PASS','active_gate':'RESET_DIRECT_PATH_HOLD','reason':'BAT54S frozen datasheet only guarantees reverse current at25C; elevated temperature curve is typical. +/-fault clamp voltages, backfeed, transients and 60s thermal not validated. Do not infer whole-domain or bench release.'}
    dump(ROOT/'RESET_RESULTS.json',j);print(json.dumps(j,indent=2))
if __name__=='__main__':run()
