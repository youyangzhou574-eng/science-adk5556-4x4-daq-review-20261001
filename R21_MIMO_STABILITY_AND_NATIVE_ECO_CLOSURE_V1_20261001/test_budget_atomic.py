import tempfile,unittest,json,datetime
from pathlib import Path
import science
class AtomicBudgetTests(unittest.TestCase):
    def test_transient_and_op_both_charged_before_mutation(self):
        old=science.ROOT
        try:
            with tempfile.TemporaryDirectory() as td:
                science.ROOT=Path(td);(science.ROOT/'cases').mkdir();(science.ROOT/'cases'/'x.cir').write_text('.control\nop\ntran 1n 1u\n.endc\n')
                now=datetime.datetime.now(datetime.timezone.utc).isoformat();b={'startedUTC':now,'totalMaxMinutes':360,'phase':'P0','phaseStartedUTC':now,'limits':{'P0':{'minutes':60}},'globalLimits':{'DC_AC_PZ':128,'transient':64},'used':{'transient':64},'cases':[]}
                path=science.ROOT/'EXECUTION_BUDGET.json';science.dump(path,b);before=path.read_bytes()
                with self.assertRaises(AssertionError):science.register('x','P0','normal')
                self.assertEqual(before,path.read_bytes())
                b['used']['transient']=63;science.dump(path,b);science.register('x','P0','normal');after=json.loads(path.read_text());self.assertEqual(after['used'],{'transient':64,'DC_AC_PZ':1})
        finally:science.ROOT=old
if __name__=='__main__':unittest.main()
