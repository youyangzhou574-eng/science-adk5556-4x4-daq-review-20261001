import unittest,tempfile,json,datetime
from pathlib import Path
import science

class ReviewGuards(unittest.TestCase):
    def test_exact_command_accounting(self):
        commands=science.analysis_commands('PZ title is not analysis\n.control\noptran 0 0 0 1n 100u\nop\nac dec 80 1 300Meg\npz a 0 b 0 cur pz\n.endc\n.end\n')
        self.assertEqual(commands,['optran','op','ac','pz'])
        self.assertEqual(science.analysis_charges(commands,'normal',''),{'DC_AC_PZ':3})
    def test_review_is_sticky_and_prevents_register_without_mutation(self):
        old=science.ROOT
        try:
            with tempfile.TemporaryDirectory() as td:
                science.ROOT=Path(td);(science.ROOT/'cases').mkdir()
                (science.ROOT/'cases'/'x.cir').write_text('case\n.control\nop\n.endc\n')
                now=datetime.datetime.now(datetime.timezone.utc).isoformat()
                p=science.ROOT/'EXECUTION_BUDGET.json';science.dump(p,{'startedUTC':now,'phase':'P0','phaseStartedUTC':now,'totalMaxMinutes':360,'limits':{'P0':{'minutes':60}},'globalLimits':{'DC_AC_PZ':128},'used':{},'cases':[]})
                science.require_technical_review('first','fixture')
                first=json.loads(p.read_text())['scienceStoppedUTC']
                science.require_technical_review('second','fixture2')
                before=p.read_bytes();self.assertEqual(json.loads(p.read_text())['scienceStoppedUTC'],first)
                with self.assertRaises(AssertionError):science.register('x','P0','normal')
                self.assertEqual(p.read_bytes(),before)
        finally:science.ROOT=old
    def test_legacy_initializer_cannot_reset_budget(self):
        old=science.ROOT
        try:
            with tempfile.TemporaryDirectory() as td:
                science.ROOT=Path(td);p=science.ROOT/'EXECUTION_BUDGET.json';p.write_text('{"scienceStopped":true}')
                before=p.read_bytes()
                with self.assertRaises(RuntimeError):science.init()
                self.assertEqual(p.read_bytes(),before)
        finally:science.ROOT=old

if __name__=='__main__':unittest.main()
