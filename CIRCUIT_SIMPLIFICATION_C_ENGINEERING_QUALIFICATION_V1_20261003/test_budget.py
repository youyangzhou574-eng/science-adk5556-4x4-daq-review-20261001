import unittest
from datetime import datetime, timezone, timedelta
import budget_guard

class BudgetGuardTests(unittest.TestCase):
    def setUp(self):
        self.now=datetime(2026,10,2,18,34,13,tzinfo=timezone.utc)
        self.b={'stop':False,'deadlineUTC':'2026-10-03T00:34:13Z','limits':{'OP_AC_PZ':32,'TRAN':8},'actual':{'OP_AC_PZ':31,'TRAN':8}}
    def test_compound_rejection_never_partially_charges(self):
        old=dict(self.b['actual'])
        with self.assertRaises(RuntimeError):budget_guard.precharge(self.b,{'OP_AC_PZ':1,'TRAN':1},self.now)
        self.assertEqual(self.b['actual'],old)
    def test_sticky_stop_rejects_unused_capacity(self):
        self.b['stop']=True
        with self.assertRaises(RuntimeError):budget_guard.precharge(self.b,{'OP_AC_PZ':1},self.now)
    def test_deadline_rejects_before_launch(self):
        with self.assertRaises(RuntimeError):budget_guard.precharge(self.b,{'OP_AC_PZ':1},self.now+timedelta(hours=7))
    def test_valid_compound_charge(self):
        self.b['actual']['TRAN']=0
        result=budget_guard.precharge(self.b,{'OP_AC_PZ':1,'TRAN':1},self.now)
        self.assertEqual(result['actual'],{'OP_AC_PZ':32,'TRAN':1})
        self.assertEqual(self.b['actual']['OP_AC_PZ'],31)
if __name__=='__main__':unittest.main()
