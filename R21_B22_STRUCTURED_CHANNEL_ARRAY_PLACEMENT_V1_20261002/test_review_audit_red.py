from pathlib import Path
import json
P=Path(__file__).parent
s=(P/'independent_audit.py').read_text()
start=s.index('arraychecks=[]');end=s.index("assert all(a['actualCoordinatePatternPASS']")
checks=s[start:end]
def passes(template,pos):
 scope={'N':{'templates':[template]},'pos':pos,'old':pos,'verify_template':None}
 # The old audit has no verifier; malformed unknown/central/pitch declarations defaulted through.
 exec(checks,scope)
 return scope['arraychecks'][0]['actualCoordinatePatternPASS']
badCentral={'name':'badcentral','kind':'CENTRAL_POSITIONAL_MIRROR','refs':['a','b'],'axisCenter':[0,0],'rotation':0}
badPitch={'name':'badpitch','kind':'PIN_FACING_MIRROR_2_PLUS_2','refs':['a','b','c','d'],'pitchXmm':99,'pitchYmm':99,'rotation':0}
p={'a':[-1,-1,0],'b':[1,-1,0],'c':[1,1,0],'d':[-1,1,0]}
out={'wrongCentralRejected':not passes(badCentral,p),'wrongPitchRejected':not passes(badPitch,p)}
print(json.dumps(out));assert all(out.values()),'Declared template audit defaults accepted incorrect geometry'

