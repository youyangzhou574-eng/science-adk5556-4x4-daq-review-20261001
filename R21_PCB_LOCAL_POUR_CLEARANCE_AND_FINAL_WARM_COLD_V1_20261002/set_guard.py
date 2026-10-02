from pathlib import Path
import json
P=Path(__file__).parent;old='6c25a449ce9ab470f4c1db4bd85120e6cad325b0f291f573b07c6aaa4d353ee1';new='7efd53fbc610430d096d3e416ed545dafaea621ce2f02ed4c02d0ed9d65ed701'
for n in('capture_routing.js','drc_routing.js','save_only.js'):
 f=P/n;text=f.read_text('utf8');assert old in text;f.write_text(text.replace(old,new),'utf8')
b=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'));b.update({'sessionCommandAttempts':2,'preSessionParserFailures':1,'sessionAccountingNote':'Warm session reserved1 before invocation. Initial incorrect session open command rejected MISSING_SUBCOMMAND, no sessionId/GUI created. Correct known open command completed the same reserved warm session. No debit was removed/backdated; only one actual session exists. Cold may create the second actual session; both command logs retained.'});(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),'utf8')
print('Known script guards bound to GUI-observed isolated project UUID; parser failure retained separately from actual session creation.')
