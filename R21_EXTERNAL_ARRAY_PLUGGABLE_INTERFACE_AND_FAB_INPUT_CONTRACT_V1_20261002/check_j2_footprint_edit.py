from pathlib import Path
import json
P=Path(__file__).parent;v=json.loads((P/'J2_BODY_AND_COURTYARD_ECO.json').read_text('utf8'))['parsed']['value'];rows=[]
for ln in v['source'].splitlines():
 if '||' not in ln:continue
 h,q=ln.split('||',1);h=json.loads(h);q=json.loads(q.rstrip('|'));rows.append((h,q))
pads=[q for h,q in rows if h['type']=='PAD'];assert len(pads)==8
for p in pads:
 assert abs(p['hole']['width']*.0254-1.14)<.0001
 assert abs(p['hole']['height']*.0254-1.14)<.0001
 assert abs(p['defaultPad']['width']*.0254-1.70)<.0001
 assert abs(p['defaultPad']['height']*.0254-1.70)<.0001
assert [p['num'] for p in pads]==[str(i) for i in range(1,9)]
assert all(abs(p['centerX']-(-350+i*100))<1e-6 and p['centerY']==0 for i,p in enumerate(pads))
out={'eightPads':True,'holeMm':1.14,'copperMm':1.7,'pitchMm':2.54,'pinCoordinatesUnchanged':True,'annulusNominalMm':.28,'annulusAtMaxHole1_19Mm':.255,'sourceDimensionsPASS':True,'nativeAssociationAndWarmColdPending':True,'threeDNotQualified':True}
(P/'J2_FOOTPRINT_DIMENSION_CHECK.json').write_text(json.dumps(out,indent=2),'utf8');print(json.dumps(out))
