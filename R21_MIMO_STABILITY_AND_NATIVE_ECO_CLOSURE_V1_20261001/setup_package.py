from pathlib import Path
import json,hashlib,datetime
from science import ROOT,OLD,EXE,dump,sha
expected={'OPA4388_ORIGINAL.LIB':'958ff133418bd47522015057497858263e73b9e6d75860ef9c0b6fdabed5cd0d','OPAx388.LIB':'bb9c6c7ac80dc7ff1ac5b698c05c53f0a8d55babb1ab210150d9bd910a6bf8e4'}
for name,h in expected.items():assert sha(ROOT/'models'/name)==sha(OLD/'models'/name)==h
assert sha(EXE)=='22d5cae2bd32b2e39157a8d27bf457122f68285b72a9ebefdf41551b628233ab'
dump(ROOT/'INPUT_VERIFIED.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'models':expected,'executor':str(EXE),'executorSHA256':sha(EXE),'frozenCommits':['da6ca87b9f49c5af03a16c24af6186d7c5c2e0d3','c13555a330f8ad676750b8fec5d5d42bfc0b5edb','a3e22772f368322dd9de671ab816c09e3b7f1b72']})
assert not (ROOT/'EXECUTION_BUDGET.json').exists()
dump(ROOT/'EXECUTION_BUDGET.json',{'startedUTC':'2026-10-01T12:50:12.878000+00:00','totalMaxMinutes':360,'phase':'P0','phaseStartedUTC':'2026-10-01T12:50:12.878000+00:00','limits':{'P0':{'minutes':60},'P1':{'minutes':120},'P2':{'minutes':60},'P3':{'minutes':90},'P4':{'minutes':30}},'globalLimits':{'DC_AC_PZ':128,'transient':64,'diagnostics':16,'full_long':1,'reset_corners':96,'protocol_tests':48,'sources':8,'reset_candidates':2,'library':4,'copy':1,'session':2,'save':8,'capture_audit':4,'ERC':2,'PDF':2},'used':{},'cases':[],'nativeGate':'NOT_ENTERED','countConvention':'one actually dispatched combined OP+AC or OP+PZ netlist is one DC_AC_PZ case, consistent with accepted previous39/32 case accounting; every command also retained; transient cases containing OP charge BOTH; diagnostic attribute always additionally charged; no new stage resets global counts'})
print('INPUT_SHA_PASS; NEW_BUDGET_FROM_ZERO_360MIN')
