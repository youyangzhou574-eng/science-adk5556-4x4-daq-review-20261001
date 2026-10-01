from science import ROOT,start,dump
from network_cases import op,raw_nodes
import json
status=[]
for direction,sgn in [('down',-1),('up',1)]:
    prior=ROOT/'results'/'opwarm_800'/'op.raw';voltage=5.;step=.05;fallback=False;done=[];pending=False;failed=False
    while sgn*(voltage-(4.75 if sgn<0 else 5.25))<-.0001:
        v=round(voltage+sgn*step,3);name='cont800_'+str(v).replace('.','p')
        if step==.025 and v not in [4.975,5.075]:name+='_25'
        p=ROOT/'results'/name
        if not (p/'STATUS.json').exists():
            op(name,'800',0,v,prior);start(name,'P0','DC_AC_PZ',60);pending=True;done.append({'vdd':v,'status':'DISPATCHED','step':step});break
        st=json.loads((p/'STATUS.json').read_text());valid=(p/'op.raw').exists() and st['status']=='NORMAL_EXIT' and st['analysisStatus']!='ANALYSIS_ERROR'
        if st['status']=='RUNNING':pending=True;done.append({'vdd':v,'status':'RUNNING'});break
        if valid:
            x=raw_nodes(p/'op.raw');valid=abs(x['v(vcm)']-2.5)<.01 and abs(x['v(vexc)']-2.25)<.01 and abs(x['v(ain0)']-4.059)<.01
        done.append({'vdd':v,'validActualOP':valid,'status':st['analysisStatus'],'step':step,'case':name})
        if valid:prior=p/'op.raw';voltage=v
        elif step==.05 and not fallback:step=.025;fallback=True
        else:failed=True;break
    status.append({'direction':direction,'attempts':done,'pending':pending,'numericHOLD':failed,'lastValidVdd':voltage,'reachedEndpoint':not pending and not failed})
dump(ROOT/'CONTINUATION_STATUS.json',status);print(json.dumps(status))
