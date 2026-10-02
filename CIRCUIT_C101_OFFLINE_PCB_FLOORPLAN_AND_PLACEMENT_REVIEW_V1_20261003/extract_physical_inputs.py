from pathlib import Path
import json,zipfile,hashlib,math,collections
P=Path(__file__).parent
q=json.loads((P/'FINAL_COLD_CAPTURE_ACTUAL_PARTS_AND_NETS.json').read_text(encoding='utf-8'))
parts={t['ref']:t for page in q['pages'] for t in page['parts']}
assert len(parts)==101 and sum(len(t['pins']) for t in parts.values())==363
with zipfile.ZipFile(P/'C101_PUBLIC_METADATA_STRIPPED_LEGACY_PCB_NOT_FOR_USE.epro2')as z:
 data=z.read(next(n for n in z.namelist()if n.endswith('.epru')))
docs={};current=None
for line in data.splitlines():
 if b'||'not in line:continue
 header,rest=line.split(b'||',1)
 if not rest.startswith(b'{'):continue
 h=json.loads(header);v,_=json.JSONDecoder().raw_decode(rest.decode('utf-8'))
 if h['type']=='DOCHEAD':
  current=docs.setdefault(v['uuid'],{'docType':v['docType'],'lines':[]})
 elif current is not None:current['lines'].append([h['type'],v])
G={};missing=[];physicalPinCount=0
for ref,t in parts.items():
 uuid=t['footprint']['uuid'];doc=docs[uuid];assert doc['docType']=='FOOTPRINT'
 nets={str(x['number']):q['pinNetMap'].get(ref+'-'+str(x['number'])) for x in t['pins']}
 assert all(bool(nets[str(x['number'])] is None)==x['nc'] for x in t['pins']),ref+' NC/map mismatch'
 if ref=='J2':
  # Explicit conservative offline placeholder: not a manufacturing footprint.
  body=[[-3.5,-7],[-3.5,7],[3.5,7],[3.5,-7]]
  pads=[{'number':str(i+1),'x':2.5,'y':i-3.5,'w':1.,'h':.4,'angle':0,'net':nets[str(i+1)],'status':'planning tail center; not exact manufacturer pad datum'} for i in range(8)]
  G[ref]={'ref':ref,'body':[body],'pads':pads,'footprintUuid':uuid,'footprintName':t['footprint']['name'],'geometryStatus':'J2_2005290081_CONSERVATIVE_14x7_PLACEHOLDER_NOT_OLD_KK','mechanicalPadsPlannedNotNative':[{'number':'MP1','x':0,'y':-6.1,'net':None},{'number':'MP2','x':0,'y':6.1,'net':None}]};physicalPinCount+=8;continue
 polys=[];pads=[]
 for kind,v in doc['lines']:
  if kind in ['POLY','FILL']and v.get('layerId')==48:
   paths=v['path'] if isinstance(v['path'][0],list) else [v['path']]
   for path in paths:
    assert 'CIRCLE' not in path and 'A'not in path,'Nonpolygon actualbody needs explicit handling '+ref
    seq=[x for x in path if isinstance(x,(float,int))];assert len(seq)%2==0
    polys.append([[seq[i]*.0254,seq[i+1]*.0254]for i in range(0,len(seq),2)])
  if kind=='PAD':
   number=str(v['num']);d=v['defaultPad'];assert d['padType']in['RECT','OVAL','ELLIPSE','POLYGON']
   poly=None
   if d['padType']=='POLYGON':
    seq=[x for x in d['path'] if isinstance(x,(float,int))];assert len(seq)%2==0
    poly=[[seq[i]*.0254,seq[i+1]*.0254]for i in range(0,len(seq),2)]
    w=max(x[0]for x in poly)-min(x[0]for x in poly);hh=max(x[1]for x in poly)-min(x[1]for x in poly)
   else:
    if 'width'not in d or 'height'not in d:raise ValueError('Explicit unsupportedpad '+ref+' '+number)
    w=d['width']*.0254;hh=d['height']*.0254
   pads.append({'number':number,'x':v['centerX']*.0254,'y':v['centerY']*.0254,'w':w,'h':hh,'polygon':poly,'angle':v.get('padAngle',0),'net':nets.get(number),'nativePadType':d['padType'],'status':'native conservative rectangular pad proxy; native polygon retained'})
 assert polys,ref+' has no actualcomponent_shape'
 assert len({x['number']for x in pads})==len(pads),ref+' duplicatepad numbers'
 actual={x['number']for x in pads};required=set(nets)
 if actual!=required:missing.append({'ref':ref,'missing':sorted(required-actual),'extra':sorted(actual-required)})
 physicalPinCount+=len(pads)
 G[ref]={'ref':ref,'body':polys,'pads':pads,'footprintUuid':uuid,'footprintName':t['footprint']['name'],'geometryStatus':'ACTUAL_NATIVE_FOOTPRINT_COMPONENT_SHAPE_AND_PAD_PROXY_NOT_MANUFACTURER_COURTYARD'}
assert not missing,missing
assert physicalPinCount==363
(P/'C101_PHYSICAL_GEOMETRY.json').write_text(json.dumps(G,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'C101_IDENTITY_AND_NETS.json').write_text(json.dumps(parts,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'GEOMETRY_EXTRACTION_AUDIT.json').write_text(json.dumps({'parts':101,'actualSCHPins':363,'physicalSignalPads':physicalPinCount,'missingOrExtraPadNumbers':missing,'all101IdentityNetSources':'coldactual','usedOldB311WorldPositions':False,'J2OldKKExcluded':True,'J2ExactNativeFootprintReplaced':False,'J2MechanicalPlaceholderCount':2,'sourceAcquisitions':0,'unit':'native mil * .0254 mm','allOtherGeometryFromCurrentExportFootprintDocuments':True},indent=2),encoding='utf-8')
print(json.dumps({'parts':len(G),'physicalPads':physicalPinCount,'missing':missing}))
