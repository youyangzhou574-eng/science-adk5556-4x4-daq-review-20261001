import pathlib
P=pathlib.Path(__file__).resolve().parent
f=P/'eco_feedback.js';s=f.read_text('utf8')
assert 'for(const p of all)if(p.getState_ComponentType()' in s
s=s.replace('for(const p of all)if(p.getState_ComponentType()', 'for(const p of await eda.sch_PrimitiveComponent.getAll())if(p.getState_ComponentType()')
f.write_text(s,'utf8')
(P/'FEEDBACK_RUNTIME_NOTE.md').write_text('First feedback operation failed before added passives/save: second target enumeration kept a deleted port in the original all snapshot. The next getAllPins on the deleted object raised retrieval failure. Fresh current component enumeration fixes that ordinary implementation error. Predebit1 retained; no new library/API/theory investigation. Rerun replaces only the two exact anchor ports again; no added parts existed because the addition loop had not been reached. Actual File Audit B remains authoritative.\n','utf8')
