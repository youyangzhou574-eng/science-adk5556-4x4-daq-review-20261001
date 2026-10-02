from b31_core import *
import shutil
out=P/'PASS1_AUDIT';out.mkdir()
for n in ['construct_b31.py','PLACEMENT_B31.json','CHANNEL_CELL_REGISTER.json','FULL_GEOMETRY_AND_IDENTITY_AUDIT.json','KEY_PIN_DISTANCE_B31.csv','ALL_552_PIN_MAP_B31.csv','PLACEMENT_B31.csv','CHANNEL_CELL_REPEATABILITY.json','OLD_BLOCK_RIGID_REUSE_AUDIT.json','REPRESENTATIVE_SIGNAL_EDGE_COMPARISON.csv','MACRO_COMPOSITION_AUDIT.json','FULL_AUDIT.log']:
 shutil.copyfile(P/n,out/n)
with (P/'PLAN_AND_LEDGER.md').open('a',encoding='utf8') as f:f.write('\nPass1 complete176, full15400 body/proxy0, keys106noincrease, both complete channel role templates PASS; ROW0/3 +7.31/+7.39mm vsB22, conservative local target+5 not met. Power input+2.545mm vsB22 but -3.921mm vsB3A: selected MacroB2 gives continuous three-regulator strip, shorter overall macro chains and narrower width; no native routing/physical result. All pass1 retained; pass2 changes only ROW common ISO/sense local role template, macro19 remains identical selectedB2. Hard Pro gate forbids ~+16mm ROW degradation and unjustified significant power degradation; +5 target is local conservative aim, not Pro verbatim.\n')
