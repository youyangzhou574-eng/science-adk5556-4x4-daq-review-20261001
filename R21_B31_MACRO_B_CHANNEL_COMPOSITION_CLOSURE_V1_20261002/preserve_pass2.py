from pathlib import Path
import shutil
P=Path(__file__).parent
# PASS1 code archive was copied after the pass2 edits; explicitly label as pass2-era snapshot, not claim original executed bytes.
(P/'PASS1_AUDIT/construct_b31.py').rename(P/'PASS1_AUDIT/construct_b31_PASS2_ERA_NOT_PASS1_EXECUTED.py')
with (P/'PLAN_AND_LEDGER.md').open('a',encoding='utf8') as f:f.write('\nPass2 counted failure NO_LOCAL_POSITION C_ROW_OP, partial/trace retained. Common ROW local template crowded its V5 cap; pass3 reserves both V5 caps from own pass1, changes common ROW ISO y from -2.1 to -1.5, finite iso candidates incl original radius, and includes all4 actual ISO2-to-J2 ROW edges in local group cost. No macro coordinate changed. PASS1 code backup timing was after pass2 edits, renamed PASS2_ERA_NOT_PASS1_EXECUTED, not exact-pass1-code evidence; pass1 coordinates/trace/audits original preserved. All actual code changes visible in current source and ledger.\n')
