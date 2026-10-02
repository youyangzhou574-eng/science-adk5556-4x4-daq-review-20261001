from pathlib import Path
import datetime, json, hashlib, shutil
P=Path(__file__).parent;now=datetime.datetime.now(datetime.timezone.utc)
assert not (P/'EXECUTION_BUDGET.json').exists()
b={'package':'SCIENCE_ADK5556_4X4_R21_EXTERNAL_ARRAY_PLUGGABLE_INTERFACE_AND_FAB_INPUT_CONTRACT_V1','rulingAssistant':'9aa9447b-4ee7-435f-827a-c2c24055dff5','parentUser':'320de471-6b63-4a0f-ba41-1681d6d74928','startUTC':now.isoformat(),'approvedMinutes':180,'status':'ACTIVE_P0_QUALIFICATION','limits':{'copy':1,'session':2,'save':2,'captureaudit':3,'DRC':3,'export':1,'officialSources':4,'candidate':2},'actual':{'copy':0,'session':0,'save':0,'captureaudit':0,'DRC':0,'export':0,'officialSources':1,'candidate':1},'reservations':[{'utc':now.isoformat(),'kind':'officialSources','count':1,'reason':'Molex 1718560008 product source from official web search; no unrelated search results used'},{'utc':now.isoformat(),'kind':'candidate','count':1,'reason':'17 default vertical KK254 1718560008; right-angle is conditional fallback only'}],'scope':'Only J2 identity/footprint/body/marking/local fanout; other175 and main analog copper frozen','forbiddenActual':{'simulation':0,'MIMO':0,'descriptor':0,'wholeBoardReroute':0,'Gerber':0,'procurement':0,'manufacture':0,'bench':0,'powerup':0,'localGit':0,'system':0}}
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2)+'\n','utf8')
(P/'IMPLEMENTATION_PLAN.md').write_text('''# Ruling17 execution: J2 pluggable interface only

Binding spec PRO_J2_INTERFACE_RULING_FULL.md, one isolated package and later at most one native work copy. No local Git/worktree/staging; user prohibition overrides skill Git setup. No evidence deletion.

P0 45min: qualify official 1718560008 vertical default and 22012087 housing dimensional/mating documents, max4 official sources. Terminals selected only when real AWG known. No arbitrary claim of compatibility with user existing unspecified wire. Conditional1718570008 only if vertical local space truly fails. Candidate max2.
P1 30min: J2 accurate MPN/manufacturer footprint/body/pin1 only, native schematic then J2-only Import Changes. Eight ROW/COL pads order fixed, legitimate mechanical features separately counted. Local fanout permitted; no other components/values/net or board outline change.
P2 45min: normalpour, warm nativeDRC allfour0 then save, independentcold allfour0; compare all other175 pins/core and main analog user copper. Capture batches max3: baseline, warm, cold+actualFile. Save2 includes scoped schematic/PCB intermediate/final; never unbudgeted convenience saves.
P3 60min: full docs/spec/keying/contract/matrix, one fresh whole-package review, single immutable GitHub report handoff, successor reply owner/nextCheck/monitor.

STOP only actual17 conditions: official incompatible pair, unsolvable local mechanical clash, required ROWCOL reorder/boardoutline change, unresolved local Short/NetlistError, or other175/mainanalog drift. Ordinary silkscreen/local tracks/derived pour are allowed; no tools/theory research. Quota/time hard guards apply.
Verification is actual native/cold evidence, no fake code mirror tests or unnecessary simulation. Existing orchestration scripts adapted within native quota; no SDK/API study. Official drawings are authority; document unknowns visible.
''','utf8')
old=P.parent/'GITHUB_PCB_PREFLIGHT_DELIVERY_20261002'
for n in ['COMMUNICATION_STATE.json','PRO_PREFLIGHT_GITHUB_LINK_DELIVERY.json']:
 p=old/n;s=json.loads(p.read_text('utf8'));s.update(replyConsumed=True,replyAssistantId=b['rulingAssistant'],replyStatus='COMPLETE_NEW_J2_ENGINEERING_RULING_CONSUMED',nextCheckAtUTC=None,monitorState='DELETED_AFTER_RULING_CONSUMED',nextPackage=b['package']);p.write_text(json.dumps(s,indent=2)+'\n','utf8')
print(json.dumps({'startUTC':b['startUTC'],'package':b['package'],'CAD_not_started':True}))
