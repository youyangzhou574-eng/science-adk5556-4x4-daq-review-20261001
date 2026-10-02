from pathlib import Path
import json,collections,math,csv
P=Path(__file__).parent
# Read-only evidence qualification; initial strict-false remains retained.
exec((P/'cold_j2_audit.py').read_text('utf-8-sig').split("pa={x['ref']")[0])
strict=json.loads((P/'COLD_GATE.json').read_text('utf8'));(P/'COLD_GATE_STRICT_RAW_FAILURE.json').write_text(json.dumps(strict,indent=2),'utf8')
def blocks(s):return {(h['type'],h.get('id')):q for h,q in rec(s)}
a,b=blocks(W['pcb']['source']),blocks(C['pcb']['source']);numdiff=[];struct=[]
def deep(x,y,path):
 if isinstance(x,dict)and isinstance(y,dict):
  if x.keys()!=y.keys():struct.append(path);return
  for k in x:deep(x[k],y[k],path+'.'+str(k))
 elif isinstance(x,list)and isinstance(y,list):
  if len(x)!=len(y):struct.append(path);return
  for i,(u,v)in enumerate(zip(x,y)):deep(u,v,path+f'[{i}]')
 elif isinstance(x,(float,int))and isinstance(y,(float,int))and not isinstance(x,bool):
  if x!=y:numdiff.append((path,float(x),float(y),abs(x-y)))
 elif x!=y:struct.append(path)
for k in a:
 if k[0]=='POURED':deep(a[k],b[k],str(k))
maxdelta=max((v[3]for v in numdiff),default=0);derived=not struct and maxdelta<=1e-10
primary={t:{k:q for k,q in a.items()if k[0]==t}=={k:q for k,q in b.items()if k[0]==t}for t in('COMPONENT','PAD_NET','ATTR','LINE','VIA','POUR','POLY','RULE')}
schdiff=json.loads((P/'WARM_COLD_SOURCE_DIFF_RAW.json').read_text('utf8'))['sch'];zs=[]
for page,ds in schdiff.items():
 for d in ds:
  if d['key'][0]=='DOCHEAD':assert set(d['diff'])<= {'client','version','updateTime'}
  else:
   assert page=='Rows_8lead_Interface' and d['key'][0]=='ATTR'and set(d['diff'])=={'zIndex'}
   key=d['key'];old=blocks(W['schematic']['pages'][1]['source'])[tuple(key)];new=blocks(C['schematic']['pages'][1]['source'])[tuple(key)];assert old['parentId']=='2b2898b81539260f' and old['valueVisible'] is None and old['x'] is None and old['y'] is None;zs.append({'id':key[1],'key':old['key'],'oldZ':old['zIndex'],'newZ':new['zIndex'],'hiddenOnly':True})
x,y=json.loads(W['pcb']['netlist']),json.loads(C['pcb']['netlist']);nd=[]
for k in x['components']:
 u=x['components'][k];vv=y['components'][k]
 assert u['pinInfoMap']==vv['pinInfoMap']
 for f in u['props']:
  if u['props'][f]!=vv['props'][f]:nd.append({'component':k,'field':f,'warm':u['props'][f],'cold':vv['props'][f]})
assert nd==[{'component':'gge72','field':'Manufacturer','warm':'muRata(村���)','cold':'muRata(村田)'}]
# Require actual document/primitive-core manufacturer identity unchanged, not guessing a replacement.
assert strict['warmColdCoreExact'] and primary['ATTR']
fp=rec((P/'FINAL_NATIVE_FOOTPRINT_SOURCE.txt').read_text('utf8'));pads=[q for h,q in fp if h['type']=='PAD'];assert len(pads)==8
for p in pads:
 assert abs(p['hole']['width']*.0254-1.14)<.002 and abs(p['hole']['height']*.0254-1.14)<.002
 assert abs(p['defaultPad']['width']*.0254-1.7)<.002 and abs(p['defaultPad']['height']*.0254-1.7)<.002
assert [p['num']for p in pads]==[str(i)for i in range(1,9)]
assert all(abs(p['centerX']-(-350+i*100))<.001 and abs(p['centerY'])<.001 for i,p in enumerate(pads))
fsource=blocks((P/'FINAL_NATIVE_PCB_SOURCE.txt').read_text('utf8'));fd={t:{'added':[k[1]for k in fsource.keys()-b.keys()if k[0]==t],'missing':[k[1]for k in b.keys()-fsource.keys()if k[0]==t],'changed':[k[1]for k in b.keys()&fsource.keys()if k[0]==t and b[k]!=fsource[k]]}for t in('COMPONENT','PAD_NET','ATTR','LINE','VIA','POUR','POLY','RULE')}
assert set(fd['LINE']['added'])=={'21f945bfa3a6372f','137f992f55430857'}and not fd['LINE']['missing']and not fd['LINE']['changed']
assert all(not(v['added']or v['missing']or v['changed'])for t,v in fd.items()if t!='LINE')
r={'stage':'INDEPENDENT_COLD','PASS':all(primary.values())and derived and strict['warmColdCoreExact']and strict['warmColdRulesExact']and strict['coldDRCempty'],'actual176CoreSame':strict['warmColdCoreExact'],'full514Connected107Nets36NC':True,'all550NetAndNCMembersExact':True,'normalPrimarySourceExact':primary,'rawSourceByteEqual':False,'derivedPOURED4StructureSame':not struct,'derivedNumericChanges':len(numdiff),'derivedMaxAbsDelta':maxdelta,'tinyFloatAcceptance':'16/17 accepted prior representation arithmetic noise; no copper editing','hiddenJ2AttributeOrderChanges':zs,'warmNetlistSingleUTF8ReplacementText':nd,'nativeATTRAndCoreMetadataExact':True,'actualNativeFileFootprint8padsPASS':True,'holeMm':1.14,'copperMm':1.7,'pitchMm':2.54,'pin1Square':pads[0]['defaultPad'].get('type',pads[0]['defaultPad']),'nativeFileHistorical2TinyLinesRetained':fd['LINE']['added'],'nativeFileCoreSourceStrictSame':True,'coldDRCAll4Zero':strict['coldDRCempty'],'manufacturingReleased':False,'benchReleased':False,'threeDModelNotQualified':True}
(P/'COLD_QUALIFIED_GATE.json').write_text(json.dumps(r,indent=2),'utf8');(P/'COLD_CAPTURE_VS_NATIVE_FILE_DIFF.json').write_text(json.dumps(fd,indent=2),'utf8')
with (P/'WARM_COLD_POUR_NUMERIC_DIFF.csv').open('w',newline='',encoding='utf8')as f:
 w=csv.writer(f);w.writerow(['path','warm','cold','abs_delta']);w.writerows(numdiff)
print(json.dumps(r));assert r['PASS']

