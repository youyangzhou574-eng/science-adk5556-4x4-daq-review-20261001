from pathlib import Path
import json,hashlib
P=Path(__file__).parent;f=P/'LOCAL_FINAL_FULL101_PLACEMENT.json'
assert not (P/'LOCAL_FINAL_PRE_METADATA_CLARIFICATION.json').exists(),'Single metadata clarification'
raw=f.read_bytes();d=json.loads(raw);before=json.dumps(d['positions'],sort_keys=True).encode();imgSHA=hashlib.sha256((P/'P1_ROW_LOCAL_FULL101_REVIEW.png').read_bytes()).hexdigest()
(P/'LOCAL_FINAL_PRE_METADATA_CLARIFICATION.json').write_bytes(raw)
for key in ['attempt','stages','placementOrder','oldCoordinatesUsed']:
 if key in d:d['inheritedBaseline_'+key]=d.pop(key)
d.update(localAttempt=1,localScope='CIRCUIT-C101-J2-ROW-ADJACENCY-LOCAL-CLOSEOUT-V1',acceptedFullP1CoordinatesUsedAsExplicitLocalInput=True,oldPartialCoordinatesUsed=False)
f.write_text(json.dumps(d,indent=2),encoding='utf-8')
assert before==json.dumps(d['positions'],sort_keys=True).encode()and imgSHA==hashlib.sha256((P/'P1_ROW_LOCAL_FULL101_REVIEW.png').read_bytes()).hexdigest()
(P/'METADATA_ONLY_CLARIFICATION_SHA.json').write_text(json.dumps({'originalJSONsha256':hashlib.sha256(raw).hexdigest(),'clarifiedJSONsha256':hashlib.sha256(f.read_bytes()).hexdigest(),'positionsCanonicalSHAUnchanged':hashlib.sha256(before).hexdigest(),'imageSHAUnchanged':imgSHA,'localPlacements':1,'newCoordinatesImagesScience':0},indent=2),encoding='utf-8')
print(json.dumps({'onlyInheritedMetadataClarified':True,'positionsImageUnchanged':True}))
