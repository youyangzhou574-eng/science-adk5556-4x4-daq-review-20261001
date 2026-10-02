import unittest,math
from pin_cost import matching_cost
class PadCost(unittest.TestCase):
 def test_first_pad_matters(self):
  self.assertEqual(matching_cost([('EN',(3,4)),('V5_IN',(0,0))],{'EN':[(0,0)],'V5_IN':[(0,0)]}),5)
 def test_each_pad_nearest_target(self):
  self.assertEqual(matching_cost([('X',(3,4)),('X',(6,8))],{'X':[(0,0),(3,4)]}),5)
 def test_unmapped_and_ground_do_not_fake_target(self):
  self.assertEqual(matching_cost([('OTHER',(3,4)),('GND',(0,4))],{'GND':[(0,0)]}),0)
if __name__=='__main__':unittest.main()
