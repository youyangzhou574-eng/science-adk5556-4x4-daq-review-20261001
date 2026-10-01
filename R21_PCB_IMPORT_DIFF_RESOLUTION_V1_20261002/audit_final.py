from pathlib import Path
import json,csv,hashlib,collections,zipfile,datetime
p=Path(__file__).resolve().parent
prior=p.parent/'R21_PCB_NETLIST_INTEGRATION_AND_ROUTING_CLOSURE_V1'
old=json.loads((prior/'CLOSURE_CAPTURE_C_COLD.json').read_text('utf8'))['parsed']['value']
new=json.loads((p/'COLD_ACTUAL_CAPTURE.json').read_text('utf8'))['parsed']['value']
sch=json.loads((p.parent/'R21_PCB_FLOORPLAN_AND_LAYOUT_V1/ACCEPTED_SCHEMATIC_JLC_NETLIST.json').read_text('utf8'))
warm=json.loads((p/'AFTER_SYNC_ACTUAL_PCB.enet').read_text('utf8'))
cold=json.loads(new['netlist'])
(p/'COLD_ACTUAL_PCB.enet').write_text(new['netlist'],'utf8')
(p/'COLD_ACTUAL_PCB_SOURCE.txt').write_text(new['source'],'utf8')
def pins(d):return {(c['props']['Designator'],str(n)):str(v.get('net','')) for c in d['components'].values() for n,v in c['pinInfoMap'].items()}
a,b,c=pins(sch),pins(warm),pins(cold)
assert a==b==c and len(c)==550
with (p/'BEFORE_AFTER_NETLIST_COMPARE.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['Ref','Pin','Schematic','Before','WarmAfter','ColdAfter','PASS'])
 before=pins(json.loads((prior/'ACTUAL_PCB_JLC_NETLIST.json').read_text('utf8')))
 for k in sorted(a):w.writerow([*k,a[k],before[k],b[k],c[k],a[k]==before[k]==b[k]==c[k]])
def geom(part):
 return {k:part[k] for k in ('id','ref','uniqueId','x','y','rotation','layer','pads')} | {'footprintUUID':part['footprint']['uuid'],'deviceUUID':part['device']['uuid'],'manufacturerId':part.get('manufacturerId') or ''}
# Device.uuid includes the same name/source/uuid dictionary; library identity roots may change with the copy.
o={x['ref']:geom(x) for x in old['parts']};n={x['ref']:geom(x) for x in new['parts']}
differences=[{'ref':r,'field':k,'before':o[r].get(k),'after':n[r].get(k)} for r in o for k in o[r] if o[r].get(k)!=n[r].get(k)]
(p/'GEOMETRY_AUDIT_DIFFERENCES.json').write_text(json.dumps(differences,indent=2,ensure_ascii=False)+'\n','utf8')
print(json.dumps(differences[:8],ensure_ascii=False))
assert o==n, 'Physical component/pad geometry changed'
def records(src,allowed):
 out=[]
 for line in src.splitlines():
  if '||' not in line:continue
  h,t=line.split('||',1);h=json.loads(h)
  if h['type'] in allowed:
   try: body=json.loads(t.rstrip('|'))
   except json.JSONDecodeError:
    print('Unparsed exported source record',line[:250]); raise
   out.append(json.dumps([h,body],sort_keys=True,ensure_ascii=False))
 return collections.Counter(out)
geometry_types={'LINE','POLY','POUR','PAD_NET','PRIMITIVE','LAYER_PHYS','RULE','RULE_SELECTOR','RULE_TEMPLATE'}
assert records(old['source'],geometry_types)==records(new['source'],geometry_types),'Copper/pad/rule source changed'
native=p/'SCIENCE_ADK5556_4X4_R21_PCB_SYNC_REVIEW.epro2'
z=zipfile.ZipFile(native);assert z.testzip() is None
epru=z.read(next(x for x in z.namelist() if x.endswith('.epru'))).decode('utf8')
sections=[];cur=[]
for line in epru.splitlines():
 if line.startswith('{"type":"DOCHEAD"'):
  if cur:sections.append(cur)
  cur=[]
 cur.append(line)
if cur:sections.append(cur)
pcbs=[s for s in sections if json.loads(s[0].split('||',1)[1].rstrip('|')).get('docType')=='PCB']
assert len(pcbs)==1
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'components':len(new['parts']),'pads':len(c),'assigned':sum(bool(v) for v in c.values()),'NC':sum(not v for v in c.values()),'nets':len(set(c.values())-{''}),'fullPinMappingSchematicBeforeWarmCold':'PASS','componentPositionsRotationsPadShapesNetAssignmentsDeviceFootprintMPNUnchanged':'PASS with four header MPN absence representations None->empty; no physical MPN change','93LinesOutlinePourPadNetRulesUnchanged':'PASS actual cold saved workfile versus prior capture','exportedEpro2CRC':'PASS','exportedEpro2ColdReopen':'NOT separately done; GUI and headless cold reopened the delivered eprj2 workfile. epru has historical/tombstone records and is retained opaque; no parser/API research.','warmGUI_DRC':{'total':452,'ConnectionError':452,'NetlistError':0},'coldGUI_DRC':{'total':452,'ConnectionError':452,'NetlistError':0},'routingComplete':False,'DRCclean':False,'nativeBytes':native.stat().st_size,'nativeSHA256':hashlib.sha256(native.read_bytes()).hexdigest().upper(),'onlyOneApply':True,'manufacturePowerupReleased':False}
(p/'FINAL_ACTUAL_AUDIT.json').write_text(json.dumps(summary,indent=2)+'\n','utf8')
print(json.dumps(summary))
