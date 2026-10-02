"""Read existing safe native archive and current saved warm JSON; no CAD calls."""
from pathlib import Path
import json,zipfile,hashlib,math,collections,csv
from shapely.geometry import Polygon,box
P=Path(__file__).parent; ROOT=P.parent
CURRENT=ROOT/'R21_J2_FFC_FPC_INTERFACE_CORRECTION_V1/FINAL_WARM_PCB.json'
ARCHIVE=ROOT/'R21_EXTERNAL_ARRAY_PLUGGABLE_INTERFACE_AND_FAB_INPUT_CONTRACT_V1/SCIENCE_ADK5556_4X4_R21_J2_PLUGGABLE_REVIEW.epro2'
FP=ROOT/'R21_J2_FFC_FPC_INTERFACE_CORRECTION_V1/J2_FINAL_WARM_FOOTPRINT_SOURCE.txt'
def rows(s):
    for line in s.splitlines():
        if '||' not in line:continue
        h,b=line.split('||',1);b=b.rstrip('|')
        if b:yield json.loads(h),json.loads(b)
def rotate(x,y,deg):
    a=math.radians(deg);return x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a)
def path_polygon(path):
    if any(isinstance(v,str) and v!='L' for v in path):return None
    vals=[v for v in path if isinstance(v,(float,int))]
    if len(vals)<6 or len(vals)%2:return None
    pts=[(vals[i]*.0254,vals[i+1]*.0254) for i in range(0,len(vals),2)]
    poly=Polygon(pts)
    return pts if poly.is_valid and poly.area>0 else None
pcb=json.loads(CURRENT.read_text(encoding='utf8'));parts=pcb['parts'];byref={c['ref']:c for c in parts}
assert len(parts)==len(byref)==176
docs={};current=None
with zipfile.ZipFile(ARCHIVE)as z:
    raw=z.read(next(n for n in z.namelist() if n.endswith('.epru'))).decode('utf8')
for h,b in rows(raw):
    if h['type']=='DOCHEAD':current=b['uuid'];docs[current]=[]
    if current:docs[current].append((h,b))
geometry={};bodyregister=[];padresidual=[]
for c in parts:
    ref=c['ref'];doc=docs[c['footprint']['uuid']]
    outlines=[path_polygon(b['path']) for h,b in doc if h['type']=='POLY' and b.get('layerId')==48]
    outlines=[p for p in outlines if p]
    if not outlines:
        outlines=[path_polygon(path) for h,b in doc if h['type']=='FILL' and b.get('layerId')==48 for path in b['path']]
        outlines=[p for p in outlines if p]
    if ref=='J2':
        # Official 13.2 +/-0.2 width and 5.3 reference depth, registered to
        # signal row and fitting-nail datum in sheet3 recommended land pattern.
        # Conservative 2D planning outline; not a manufacturer-verified exact body trace.
        outlines=[[(-6.7,-.3),(6.7,-.3),(6.7,5.5),(-6.7,5.5)]]
        body_source='Molex2005291002PSD000revB sheets1/3,3/3; conservative width/depth/land-datum planning envelope'
        body_status='OFFICIAL_DIMENSION_CONSERVATIVE_2D_ENVELOPE_NOT_EXACT_BODY_TRACE'
        localpads=[b for h,b in rows(FP.read_text(encoding='utf8')) if h['type']=='PAD']
    else:
        body_source='Existing actual native component-shape layer48; archive footprintUUID='+c['footprint']['uuid']
        body_status='NATIVE_COMPONENT_SHAPE_NOT_INDEPENDENT_MANUFACTURER_MAX_COURTYARD'
        localpads=[b for h,b in doc if h['type']=='PAD']
    if not outlines:
        if ref.startswith(('U','J')):raise RuntimeError('STOP_KEY_BODY_MISSING '+ref)
        body_status='BODY_PROVISIONAL_PAD_ONLY';body_source='PAD_ONLY_NO_BODY_EVIDENCE'
    lookup={str(b['num']):b for b in localpads};errs=[]
    for p in c['pads']:
        b=lookup.get(str(p['number']))
        if b is None:raise RuntimeError('STOP_PAD_NUMBER_MAPPING '+ref+'.'+p['number'])
        x,y=rotate(b['centerX'],b['centerY'],c['rotation'])
        errs.append(math.hypot(x+c['x']-p['x'],y+c['y']-p['y'])*.0254)
    maxerr=max(errs)
    # Actual capture pad centers use 0.1mil rounding; transformed source proof
    # checks <=.01mm, not byte equality or fabricated exact coincidence.
    if maxerr>.01:raise RuntimeError('STOP_FOOTPRINT_ROTATION_MAPPING '+ref+' '+str(maxerr))
    padresidual.append({'ref':ref,'maxLocalPadToActualCenterResidualMm':maxerr})
    geometry[ref]={'ref':ref,'xMm':c['x']*.0254,'yMm':c['y']*.0254,'rotation':c['rotation'],'layer':c['layer'],
      'bodyLocalPolygonsMm':outlines,'bodySource':body_source,'bodyStatus':body_status,
      'name':c['name'],'footprintUuid':c['footprint']['uuid'],'footprintName':c['footprint']['name'],
      'pads':[{'number':p['number'],'net':p['net'],'xMm':p['x']*.0254,'yMm':p['y']*.0254,'rotation':p['rotation'],'shape':p['pad'],'nativeLayer':p['layer']}for p in c['pads']]}
    bodyregister.append({'ref':ref,'bodyStatus':body_status,'bodySource':body_source,'localBodyAreaMm2':sum(Polygon(p).area for p in outlines),'maxLocalPadToActualCenterResidualMm':maxerr})

G=geometry['J2'];pads=G['pads'];assert len(pads)==10
for n in range(1,9):assert next(p['net']for p in pads if p['number']==str(n))==('ROW'+str(n-1)if n<=4 else'COL'+str(n-5))
assert all(p['net']=='' for p in pads if p['number'].startswith('MP'))
inputs=[CURRENT,ARCHIVE,FP,ROOT/'R21_J2_FFC_FPC_INTERFACE_CORRECTION_V1/sources_local_only/S2_connector_drawing.pdf']
manifest=[{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in inputs]
(P/'INPUT_SHA_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
(P/'ACTUAL_GEOMETRY.json').write_text(json.dumps(geometry,ensure_ascii=False,indent=2),encoding='utf8')
with(P/'BODY_SOURCE_REGISTER.csv').open('w',encoding='utf-8-sig',newline='')as f:
    w=csv.DictWriter(f,fieldnames=list(bodyregister[0]));w.writeheader();w.writerows(bodyregister)
(P/'GEOMETRY_EXTRACTION_AUDIT.json').write_text(json.dumps({'components':176,'pads':sum(len(c['pads'])for c in parts),'assigned':sum(bool(p['net'])for c in parts for p in c['pads']),
 'actualFootprintLocalPadMappings':sum(len(c['pads'])for c in parts),'maxMappingResidualMm':max(v['maxLocalPadToActualCenterResidualMm']for v in padresidual),
 'bodyStatuses':dict(collections.Counter(g['bodyStatus']for g in geometry.values())),
 'FFCConservativeOutline':True,'FFCExactBodyRegistrationManufacturerVerified':False,'CADOperations':0,'padResiduals':padresidual},indent=2),encoding='utf8')
print(json.dumps({'mapped':176,'pads':552,'maxMappingResidualMm':max(v['maxLocalPadToActualCenterResidualMm']for v in padresidual),'bodyStatuses':dict(collections.Counter(g['bodyStatus']for g in geometry.values()))}))
