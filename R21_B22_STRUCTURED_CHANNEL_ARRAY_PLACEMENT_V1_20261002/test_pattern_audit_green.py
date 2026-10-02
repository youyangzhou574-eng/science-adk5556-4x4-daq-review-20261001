from pathlib import Path
import json
from pattern_audit import verify_template
P=Path(__file__).parent;n=json.loads((P/'PLACEMENT_B22.json').read_text());o=json.loads((P/'PLACEMENT_B21.json').read_text())['positions'];pos=n['positions']
results={}
results['all56actualDeclarations']=all(verify_template(t,pos,o)for t in n['templates'])
p={'a':[-1,-1,0],'b':[1,-1,0],'c':[1,1,0],'d':[-1,1,0]}
results['invalidCentralRejected']=not verify_template({'kind':'CENTRAL_POSITIONAL_MIRROR','refs':['a','b'],'axisCenter':[0,0],'rotation':0},p,p)
results['invalidDeclaredPitchRejected']=not verify_template({'kind':'PIN_FACING_MIRROR_2_PLUS_2','refs':['a','b','c','d'],'pitchXmm':99,'pitchYmm':99,'rotation':0},p,p)
results['unknownKindRejected']=not verify_template({'kind':'UNKNOWN','refs':['a']},p,p)
t=next(x for x in n['templates']if x['kind']=='FOUR_CHANNEL_TWO_ROW');bad=dict(t,pitchYmm=999)
results['invalidADCRowPitchRejected']=not verify_template(bad,pos,o)
t=next(x for x in n['templates']if x['kind']=='PIN_FORCED_BASELINE');q=dict(pos);r=t['refs'][0];q[r]=list(q[r]);q[r][0]+=.1
results['movedBaselineRejected']=not verify_template(t,q,o)
m=json.loads((P/'REQUIREMENT_ACCEPTANCE_MATRIX.json').read_text())
results['commonAxisRequirementHOLD']=next(x for x in m if x['requirement']=='BIAS VCM/VEX paired placement')['result']=='PARTIAL_CENTRAL_PAIRING_AXIS_MIRROR_HOLD'
print(json.dumps(results));assert all(results.values())

