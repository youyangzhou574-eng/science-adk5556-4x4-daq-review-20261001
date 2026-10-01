import unittest,numpy as np
from invariant_math import power_coordinates,characteristic_matrix,closed_contour_winding
class InvariantMathTests(unittest.TestCase):
 def test_power_and_closure(self):
  rng=np.random.default_rng(5556);v=rng.normal(size=6);i=rng.normal(size=6);vc,ic=power_coordinates(v,i)
  self.assertAlmostEqual(v@i,vc@ic)
  y=rng.normal(size=(6,6));g=characteristic_matrix(y)
  self.assertTrue(np.allclose(g,y[:3,:3]+y[:3,3:]+y[3:,:3]+y[3:,3:]))
 def test_stable_and_rhp_truth(self):
  for a,expected in [(np.array([[-1.,1000],[-.002,-3]]),0),(np.array([[-1.,4],[2,-1]]),1)]:
   self.assertEqual(closed_contour_winding(a,np.ones(2))['winding'],expected)
 def test_mixed_power_scaling_invariant(self):
  a=np.array([[-1.,4],[2,-1]])
  for scale in [np.array([.001,1000]),np.array([1000,.001])]:self.assertEqual(closed_contour_winding(a,scale)['winding'],1)
if __name__=='__main__':unittest.main()
