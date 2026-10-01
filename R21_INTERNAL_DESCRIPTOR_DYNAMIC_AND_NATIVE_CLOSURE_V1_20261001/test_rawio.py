import unittest
from rawio import op_values
from pathlib import Path
class Raw(unittest.TestCase):
 def test_voltage_and_branch_current_with_same_name_do_not_collide(self):
  p=Path(__file__).resolve().parent/'results/follower_exact/op.raw';v=op_values(p)
  self.assertEqual(v['vdd'],5.);self.assertIn('branch:vdd',v)
if __name__=='__main__':unittest.main()
