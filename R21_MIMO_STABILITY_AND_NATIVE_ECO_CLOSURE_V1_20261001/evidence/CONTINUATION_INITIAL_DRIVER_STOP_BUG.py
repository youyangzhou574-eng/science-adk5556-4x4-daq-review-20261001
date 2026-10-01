from science import ROOT,start,dump
from network_cases import op,raw_nodes
import json
status=[]
for direction,values in [('down',[4.95,4.975]),('up',[5.05,5.10,5.15,5.20,5.25])]:
    prior=ROOT/'results'/'opwarm_800'/'op.raw';done=[];pending=False;ended=False
    for v in values:
        name='cont800_'+str(v).replace('.','p');p=ROOT/'results'/name
        if not (p/'STATUS.json').exists():
            op(name,'800',0,v,prior);start(name,'P0','DC_AC_PZ',60);pending=True;done.append({'vdd':v,'status':'DISPATCHED'});break
        st=json.loads((p/'STATUS.json').read_text());valid=(p/'op.raw').exists() and st['status']=='NORMAL_EXIT' and st['analysisStatus']!='ANALYSIS_ERROR'
        if st['status']=='RUNNING':pending=True;done.append({'vdd':v,'status':'RUNNING'});break
        if valid:
            x=raw_nodes(p/'op.raw');valid=abs(x['v(vcm)']-2.5)<.01 and abs(x['v(vexc)']-2.25)<.01 and abs(x['v(ain0)']-4.059)<.01
        done.append({'vdd':v,'validActualOP':valid,'status':st['analysisStatus']})
        if valid:
            prior=p/'op.raw'
            if direction=='down':
                # 50mV passed: use50mV chain; the25mV item is only the once fallback.
                if v==4.95:raise RuntimeError('down50mV succeeded; construct remaining regular chain explicitly')
                ended=True;break
        elif direction=='up' or v==4.975:ended=True;break
        # After4.95 failure, retry4.975 once from the original5V nodeset.
    status.append({'direction':direction,'attempts':done,'pending':pending,'numericHOLD':ended,'reachedEndpoint':prior.parent.name=='cont800_5p25'})
dump(ROOT/'CONTINUATION_STATUS.json',status);print(json.dumps(status))
