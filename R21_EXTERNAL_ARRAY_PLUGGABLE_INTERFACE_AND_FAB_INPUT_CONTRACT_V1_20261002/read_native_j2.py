from pathlib import Path
import json,zipfile
P=Path(__file__).parent
z=zipfile.ZipFile(P.parent/'R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1'/'SCIENCE_ADK5556_4X4_R21_PCB_CLOSED_REVIEW.epro2')
raw=z.read(next(n for n in z.namelist() if n.endswith('.epru'))).decode('utf8')
active=None; rows=[]
for ln in raw.splitlines():
 if '||' not in ln:continue
 try:h,q=ln.split('||',1);h=json.loads(h);q=json.loads(q.rstrip('|'))
 except:continue
 if h['type']=='DOCHEAD':active=q.get('uuid') if q.get('docType')=='FOOTPRINT' else None
 if active=='87b2e6ab0bf2243f':rows.append({'header':h,'data':q})
(P/'J2_GENERIC_FOOTPRINT_SOURCE.json').write_text(json.dumps(rows,indent=2),'utf8')
for r in rows:
 if r['header']['type'] in ['PAD','CANVAS','POLY','LINE']:print(json.dumps(r))
