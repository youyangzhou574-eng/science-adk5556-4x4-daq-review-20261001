from pathlib import Path
import sys,json,csv,traceback,numpy as np
from processed import parse
from rawio import op_values
from mna import build
from offline_budget import debit
r=Path(__file__).resolve().parent;name=sys.argv[1];case=next(c for c in json.loads((r/'LOCAL_QUALIFICATION_CASES.json').read_text())if c['name']==name)
debit(name+'_processed_exact_AC',note='12 exact actual primitive transfer qualifications, complete processed variable map')
dest=r/'results'/name
try:
 status=json.loads((dest/'STATUS.json').read_text());assert status['status']=='NORMAL_EXIT'and status['analysisStatus']!='ANALYSIS_ERROR',status
 es=parse((dest/'stdout.log').read_text(errors='replace'),str(dest/'stdout.log'));op=op_values(dest/'op.raw');m=build(es,op);missing=sorted(set(m.variables)-set(op));assert not missing,missing
 rows=[]
 for j,hz in enumerate([.01,.1,1,10,100,1e3,1e4,1e5,1e6,1e7,1e8,3e8]):
  a=np.loadtxt(dest/('ac_%02d.txt'%j),skiprows=1);assert abs(a[0]-hz)<1e-10*max(1,hz)
  for k,out in enumerate(case['outputs']):
   native=complex(a[1+2*k],a[2+2*k]);desc=m.transfer(2j*np.pi*hz,case['source'],out);rows.append([hz,out,native.real,native.imag,desc.real,desc.imag,abs(desc-native),abs(desc-native)/max(abs(native),1e-9),abs(native)<1e-9])
 with (dest/'DESCRIPTOR_AC_COMPARISON.csv').open('w',newline='')as f:w=csv.writer(f);w.writerow(['frequencyHz','output','nativeReal','nativeImag','descriptorReal','descriptorImag','absoluteError','relativeComplexError','belowAbsoluteFloor']);w.writerows(rows)
 np.savez(dest/'DESCRIPTOR.npz',E=m.E,A=m.A,B=m.B[case['source']],variables=m.variables)
 (dest/'STAMP_MAP.json').write_text(json.dumps({'variables':m.variables,'nativeOPKeys':list(op),'stamps':m.stamps},indent=2))
 result={'status':'EXACT_POINT_PASS'if max(x[-2]for x in rows)<=.002 else 'EXACT_POINT_FAIL','dimension':len(m.variables),'elements':len(es),'maxRelativeComplexError':max(x[-2]for x in rows),'samples':len(rows),'LINEARIZED_MNA_DESCRIPTOR_QUALIFIED':False,'internalSpectrumAvailable':False,'majorOutputFloor':1e-9}
except Exception as e:result={'status':'EXTRACTION_FAIL','error':repr(e),'traceback':traceback.format_exc(),'LINEARIZED_MNA_DESCRIPTOR_QUALIFIED':False}
(dest/'QUALIFICATION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if result['status']in ('EXTRACTION_FAIL','EXACT_POINT_FAIL'):
 b=json.loads((r/'EXECUTION_BUDGET.json').read_text());b['scienceStopped']=True;b['stopReason']='DESCRIPTOR_EXTRACTION_NOT_QUALIFIED';b['stopCase']=name;(r/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2));print('STICKY_SCIENCE_STOP')
