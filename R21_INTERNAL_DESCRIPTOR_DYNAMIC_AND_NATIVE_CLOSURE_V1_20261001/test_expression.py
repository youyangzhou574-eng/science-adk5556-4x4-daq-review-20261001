import unittest,numpy as np
try:from expression import evaluate,table,NonDifferentiable
except ImportError:evaluate=table=NonDifferentiable=None

class ExpressionTests(unittest.TestCase):
 def test_limit_branch_and_remote_bound_gradient(self):
  self.assertTrue(callable(evaluate),'evaluate missing')
  r=evaluate('LIMIT(3*V(a,b),V(lo),V(hi))',{'a':2.,'b':0.,'lo':-1.,'hi':4.},['a','b','lo','hi'],{},lambda x:x)
  self.assertEqual(r.v,4.);np.testing.assert_equal(r.g,[0,0,0,1])
 def test_if_compound_voltage_and_inactive_branch(self):
  self.assertTrue(callable(evaluate),'evaluate missing')
  r=evaluate('IF((V(a)>10m | V(b)>10m),GAIN*V(a,b),0)',{'a':.02,'b':-.01},['a','b'],{'gain':2},lambda x:x)
  self.assertAlmostEqual(r.v,.06);np.testing.assert_equal(r.g,[2,-2])
 def test_exact_kink_has_no_chosen_gradient(self):
  self.assertTrue(callable(evaluate),'evaluate missing')
  with self.assertRaises(NonDifferentiable):evaluate('IF(V(a)>0,V(a),0)',{'a':0.},['a'],{},lambda x:x)
 def test_table_active_segment(self):
  self.assertTrue(callable(table),'table missing')
  r=table('TABLE {V(a)} = (0,1) (10,21) (20,31)',{'a':5},['a'],{},lambda x:x);self.assertEqual(r.v,11);self.assertEqual(r.g[0],2)

if __name__=='__main__':unittest.main()
