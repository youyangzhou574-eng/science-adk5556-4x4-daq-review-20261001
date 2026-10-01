import unittest,numpy as np
from spice_flatten import flatten
try:from mna import build
except ImportError:build=None

class MNA(unittest.TestCase):
 def test_psa_switch_control_input_resistance_is_retained(self):
  model={'type':'vswitch','ron':10.,'roff':1e12,'voff':0.,'von':1.}
  from spice_flatten import Element
  e=Element('s1','s',['out','0','ctrl','0'],'m',{},'fixture',1,'',model)
  m=build([e],{'out':2.,'ctrl':2.})
  self.assertEqual(-m.A[m.variables.index('ctrl'),m.variables.index('ctrl')],1e-12)
  self.assertEqual(-m.A[m.variables.index('out'),m.variables.index('out')],.1)
 def test_rc_voltage_branch_constraint_and_transfer(self):
  self.assertTrue(callable(build),'build missing');m=build(flatten('t\nV1 in 0 1\nR1 in out 1k\nC1 out 0 1u\n'),{})
  self.assertEqual(len(m.variables),3);self.assertAlmostEqual(m.transfer(100j,'v1','out'),1/(1+.1j));self.assertEqual(np.linalg.matrix_rank(m.E),1)
 def test_controlled_voltage_and_current_signs(self):
  self.assertTrue(callable(build),'build missing');m=build(flatten('t\nV1 in 0 1\nE1 v 0 in 0 2\nG1 out 0 in 0 .001\nR1 out 0 1k\n'),{})
  self.assertAlmostEqual(m.transfer(0j,'v1','v'),2);self.assertAlmostEqual(m.transfer(0j,'v1','out'),-1)
 def test_current_sensed_voltage_source(self):
  self.assertTrue(callable(build),'build missing');m=build(flatten('t\nV1 in 0 1\nVsense in r 0\nR1 r 0 1k\nH1 out 0 Vsense 2k\n'),{})
  self.assertAlmostEqual(m.transfer(0j,'v1','out'),2)
 def test_nonzero_internal_behavior_jacobian_retained(self):
  self.assertTrue(callable(build),'build missing');m=build(flatten('t\nV1 in 0 1\nG1 out 0 VALUE={LIMIT(2*V(in),-10,10)}\nR1 out 0 1\n'),{'in':1,'out':-2})
  self.assertAlmostEqual(m.transfer(0j,'v1','out'),-2)

if __name__=='__main__':unittest.main()
