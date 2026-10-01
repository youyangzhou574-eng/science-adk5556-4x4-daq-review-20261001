import unittest
try:from processed import parse
except ImportError:parse=None
from mna import build
class Processed(unittest.TestCase):
 def test_generated_behavior_voltage_constraint_retained(self):
  self.assertTrue(callable(parse))
  m=build(parse('1 : title\n2 : vin in 0 1\n3 : b1 internal 0 v=ternary_fcn(v(in)>0,min(v(in)*2,10),0)\n4 : e1 out 0 internal 0 1\n5 : .end'),{'in':1,'internal':2,'out':2})
  self.assertIn('internal',m.variables);self.assertIn('branch:b1',m.variables)
  self.assertAlmostEqual(m.transfer(0j,'vin','out'),2)
 def test_pwl_smoothing_retains_both_new_algebraic_unknowns(self):
  self.assertTrue(callable(parse))
  es=parse('1 : title\n2 : .model p pwl(x_array=[0 10 20] y_array=[0 1 3] input_domain=.1 fraction=true limit=true)\n3 : a1 %v in %v out p\n4 : .end')
  m=build(es,{'in':10.1,'out':1.01});self.assertIn('out',m.variables);self.assertIn('branch:a1',m.variables)
  self.assertAlmostEqual(-m.A[m.variables.index('branch:a1'),m.variables.index('in')]*-1,.155)
if __name__=='__main__':unittest.main()
