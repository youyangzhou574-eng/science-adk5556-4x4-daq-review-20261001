"""Infrastructure regression only: temporary ledger, never launches an executor."""
import unittest,tempfile,json,datetime
from pathlib import Path
import science
class BudgetPreflightTests(unittest.TestCase):
    def test_diagnostic_also_charges_analysis_and_is_atomic(self):
        original=science.ROOT
        try:
            with tempfile.TemporaryDirectory() as td:
                science.ROOT=Path(td);(science.ROOT/'cases').mkdir()
                (science.ROOT/'cases'/'diag.cir').write_text('.control\nop\nac dec 1 1 10\n.endc\n.end\n')
                now=datetime.datetime.now(datetime.timezone.utc).isoformat()
                ledger={'startedUTC':now,'phase':'P0','phaseStartedUTC':now,'limits':{'P0':{'minutes':45,'AC_DC_PZ':32,'diagnostics':8}},'used':{'P0/AC_DC_PZ':32},'cases':[]}
                path=science.ROOT/'EXECUTION_BUDGET.json';science.dump(path,ledger);before=path.read_bytes()
                with self.assertRaises(AssertionError):science.register('diag','P0','diagnostics')
                self.assertEqual(path.read_bytes(),before)
        finally:science.ROOT=original
if __name__=='__main__':unittest.main()
