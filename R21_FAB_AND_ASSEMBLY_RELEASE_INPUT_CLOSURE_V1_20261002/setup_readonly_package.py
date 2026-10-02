from pathlib import Path
import json,datetime,hashlib,csv
P=Path(__file__).parent;old=P.parent/'R21_EXTERNAL_ARRAY_PLUGGABLE_INTERFACE_AND_FAB_INPUT_CONTRACT_V1';now=datetime.datetime.now(datetime.timezone.utc)
assert not(P/'EXECUTION_BUDGET.json').exists()
b={'package':'SCIENCE_ADK5556_4X4_R21_FAB_AND_ASSEMBLY_RELEASE_INPUT_CLOSURE_V1','rulingAssistant':'2da86929-7e15-401f-b181-d047d6f23b4d','parentUser':'0427f964-91d8-4fb7-9979-d05cad568565','startedUTC':now.isoformat(),'approvedMinutes':180,'status':'ACTIVE_READONLY_DOCUMENTS_ONLY','limits':{'existingFrozenEvidencePass':1,'manufacturingContractBatch':1,'officialNewSources':4,'terminalCandidates':2},'actual':{'existingFrozenEvidencePass':0,'manufacturingContractBatch':0,'officialNewSources':0,'terminalCandidates':0},'sourceLimitNote':'R18 only requested default contract, no broad research; conservative proposed4 sources/2terminalcaps retained as self-bounds, not claimed separately approved analyses','forbiddenActual':{k:0 for k in ['CADedit','session','save','capture','DRC','nativeExport','routing','pour','schematic','ImportChanges','simulation','Gerber','procurement','manufacturing','bench','powerup','localGit','system']},'nextScope':'Defaultfabsettings + structural176BOM +8wireharness + releasechecklist, no actualhardware orCAD'};(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),'utf8')
(P/'IMPLEMENTATION_PLAN.md').write_text('''# R18唯一制造/装配输入闭合包

冻结J2 acceptedcommit bcafa5c6b834c20539774cd335d34586442453be/actualnative801149F...；18接受丝印偏差，不再为工具文字/3D/genericdevice开CAD。P0普通四层默认制造合同45min；P1准确结构176BOM/缺件/极性与装配45min；P2已定8芯线束合同30min；P3区分PASS/下单前必填/CAM/装配/nonblocking45min；P4文档核对交付15min。总180min硬帽，不换算平台额度。新CAD/仿真/生产/采购/bench/Gerber/localGit/system全部0。

来源只读已有officialsource/frozenactualCSV/原生捕获、最多一次官方工艺页fresh验证；不重新研究API/909911/3D/metadata或独立回归。工程默认值是推荐输入，不假定用户已选厂/冻工艺。记录sourceSHA及参数状态。176个结构BOM准确ref/MPN/Value/Footprint/quantity核对，Description乱码不能authority，J2MPN+强制配套覆盖；J1/J3/J4真实缺MPN列出不选型冒充。无实际线径时terminal=PENDING_AWG，只选24–26AWG为建议范围不锁候选MPN。只生成/交叉核对文档与CSV，一次整包只读终审，GitHub新目录固定commit+一次摘要+接续owner/monitor。
''','utf8')
files={}
for f in old.rglob('*'):
 if f.is_file() and '__pycache__'not in f.parts:files[f.relative_to(old).as_posix()]={'bytes':f.stat().st_size,'SHA256':hashlib.sha256(f.read_bytes()).hexdigest().upper()}
(P/'FROZEN_J2_SOURCE_HASHES_BEFORE.json').write_text(json.dumps(files,indent=2),'utf8')
v=json.loads((old/'COLD_PCB.json').read_text('utf8'));net=json.loads(v['netlist']);parts={c['ref']:c for c in v['parts']};rows=[]
for uid,c in net['components'].items():
 q=c['props'];ref=q['Designator'];x=parts[ref];rows.append({'Designator':ref,'Manufacturer':q.get('Manufacturer',''),'MPN':q.get('Manufacturer Part',''),'Value':q.get('Value')or q.get('Name',''),'Name':q.get('Name',''),'Footprint':x['footprint']['name'],'Quantity':1,'missingManufacturer':not bool(q.get('Manufacturer')),'missingMPN':not bool(q.get('Manufacturer Part')),'DeviceName':q.get('DeviceName'),'supplierPart':q.get('Supplier Part',''),'pinCount':len(x['pads']),'rotation':x['rotation']})
assert len(rows)==176;missing=[r for r in rows if r['missingManufacturer']or r['missingMPN']];print(json.dumps({'startUTC':now.isoformat(),'frozenFiles':len(files),'BOM176':True,'missing':missing},ensure_ascii=False))
(P/'BOM_STRUCTURAL_176_FROM_COLD.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),'utf8')
