from pathlib import Path
import json
P=Path(__file__).parent;b=json.loads((P/'BASELINE_PCB.json').read_text('utf8'));refs=[x['ref'] for x in b['parts'] if x['footprint']['uuid']=='87b2e6ab0bf2243f'];assert refs==['J2'],refs
(P/'J2_SHARED_TEMPLATE_SCOPE.json').write_text(json.dumps({'footprintUuid':'87b2e6ab0bf2243f','baselineRefs':refs,'other175UseThisFootprint':False,'purpose':'Original project-local8pin footprint definition applies exclusivelyJ2; no account/library-wide update'},indent=2),'utf8');print(refs)
