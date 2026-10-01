from pathlib import Path
from processed import parse
from rawio import op_values
from mna import build
from offline_budget import debit
from science import require_technical_review
import json,numpy as np,csv,traceback
r=Path(__file__).resolve().parent;debit('processed_follower_all_variables_12point_AC',note='Actual expanded PSA deck including all generated algebraic variables; native exact AC qualification, preserve all failures')
try:
 es=parse((r/'results/follower_listing/stdout.log').read_text(errors='replace'),str(r/'results/follower_listing/stdout.log'));op=op_values(r/'results/follower_exact/op.raw')
 m=build(es,op);rows=[]
 for j,hz in enumerate([.01,.1,1,10,100,1e3,1e4,1e5,1e6,1e7,1e8,3e8]):
  a=np.loadtxt(r/'results/follower_exact'/('ac_%02d.txt'%j),skiprows=1);native=complex(a[1],a[2]);desc=m.transfer(2j*np.pi*hz,'vin','out');rows.append([hz,native.real,native.imag,desc.real,desc.imag,abs(desc-native)/max(abs(native),1e-9)])
 with (r/'results/PROCESSED_FOLLOWER_EXACT_AC_COMPARISON.csv').open('w',newline='')as f: w=csv.writer(f);w.writerow(['frequencyHz','nativeReal','nativeImag','descriptorReal','descriptorImag','relativeComplexError']);w.writerows(rows)
 np.savez(r/'results/PROCESSED_FOLLOWER_DESCRIPTOR.npz',E=m.E,A=m.A,Bvin=m.B['vin'],variables=m.variables)
 (r/'results/PROCESSED_FOLLOWER_STAMP_MAP.json').write_text(json.dumps({'variables':m.variables,'stamps':m.stamps,'expandedElements':len(es),'nativeOPKeys':list(op),'descriptorVariablesMissingOP':sorted(set(m.variables)-set(op))},indent=2))
 result={'maxRelativeComplexError':max(x[-1]for x in rows),'dimension':len(m.variables),'expandedElements':len(es),'nativeOPKeys':len(op),'status':'LOCAL_12_POINT_ONLY_PASS'if max(x[-1]for x in rows)<=.002 else 'LOCAL_AC_FAIL','LINEARIZED_MNA_DESCRIPTOR_QUALIFIED':False,'internalSpectrumAvailable':False,'PWLFormula':'inferred quadratic corner candidate, two actual OP tangents match native primitive probes'}
except Exception as e:result={'status':'EXTRACTION_FAIL','error':repr(e),'traceback':traceback.format_exc(),'LINEARIZED_MNA_DESCRIPTOR_QUALIFIED':False}
(r/'PROCESSED_FOLLOWER_QUALIFICATION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if result['status']in ('LOCAL_AC_FAIL','EXTRACTION_FAIL'):require_technical_review('DESCRIPTOR_EXTRACTION_NOT_QUALIFIED','processed_follower')
