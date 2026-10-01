from pathlib import Path
import json,numpy as np,csv,traceback
from spice_flatten import flatten
from rawio import op_values
from mna import build
from offline_budget import debit
from science import require_technical_review
r=Path(__file__).resolve().parent;debit('follower_exact_12point_descriptor_AC',note='12 exact AC comparisons and primitive Jacobian/128-variable source mapping; no modelpole conclusion')
try:
 f=flatten((r/'cases/follower_exact.cir').read_text(),source=str(r/'cases/follower_exact.cir'));op=op_values(r/'results/follower_exact/op.raw');m=build(f,op);np.savez(r/'results/FOLLOWER_DESCRIPTOR.npz',E=m.E,A=m.A,Bvin=m.B['vin'],variables=m.variables)
 (r/'results/FOLLOWER_STAMP_MAP.json').write_text(json.dumps({'variables':m.variables,'primitiveStamps':m.stamps,'originalPrimitiveCount':len(f),'actualOPVariables':len(op),'compatibilityGeneratedAlgebraicVariablesNotYetReconciled':True},indent=2),encoding='utf-8')
 rows=[]
 for j,hz in enumerate([.01,.1,1,10,100,1e3,1e4,1e5,1e6,1e7,1e8,3e8]):
  a=np.loadtxt(r/'results/follower_exact'/('ac_%02d.txt'%j),skiprows=1);assert abs(a[0]-hz)<=1e-10*max(1,hz);native=complex(a[1],a[2]);desc=m.transfer(2j*np.pi*hz,'vin','out');error=abs(desc-native)/max(abs(native),1e-9);rows.append([hz,native.real,native.imag,desc.real,desc.imag,error,abs(native)<1e-9])
 with (r/'results/FOLLOWER_EXACT_AC_COMPARISON.csv').open('w',newline='')as fh:
  w=csv.writer(fh);w.writerow(['frequencyHz','ngspiceReal','ngspiceImag','descriptorReal','descriptorImag','relativeComplexError','belowAbsoluteFloor']);w.writerows(rows)
 result={'status':'PASS_12_EXACT_TRANSFER_POINTS_ONLY'if max(x[5]for x in rows)<=.002 else 'FAIL_AC_JACOBIAN_COMPARISON','maxRelativeComplexError':max(x[5]for x in rows),'pointCount':12,'dimension':len(m.variables),'internalPoleCertificate':False,'compatibilityVariableMappingComplete':False,'LINEARIZED_MNA_DESCRIPTOR_QUALIFIED':False};(r/'FOLLOWER_AC_QUALIFICATION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
except Exception as e:
 require_technical_review('DESCRIPTOR_EXTRACTION_NOT_QUALIFIED','original_follower_exception')
 raise
if result['status']=='FAIL_AC_JACOBIAN_COMPARISON':require_technical_review('DESCRIPTOR_EXTRACTION_NOT_QUALIFIED','original_follower')
