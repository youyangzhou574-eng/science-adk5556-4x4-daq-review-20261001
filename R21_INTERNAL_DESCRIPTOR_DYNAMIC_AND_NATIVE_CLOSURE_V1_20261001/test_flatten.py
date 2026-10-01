import unittest
try:from spice_flatten import number,flatten
except ImportError:number=flatten=None

class FlattenTests(unittest.TestCase):
 def test_spice_milli_and_mega(self):
  self.assertTrue(callable(number),'number missing');self.assertEqual(number('1M'),.001);self.assertEqual(number('1MEG'),1e6);self.assertEqual(number('140F'),140e-15);self.assertEqual(number('-10MV'),-.01)
 def test_subckt_parameter_scope_and_source_mapping(self):
  self.assertTrue(callable(flatten),'flatten missing')
  s='title\n.subckt amp IN+ OUT params: gain=2\nR1 IN+ local {gain*1k}\nE1 OUT 0 local 0 1\n.ends\nX1 input output amp params: gain=3\n'
  f=flatten(s);self.assertEqual(len(f),2);self.assertEqual(f[0].nodes,['input','x1.local']);self.assertEqual(f[0].params['gain'],3);self.assertEqual(f[0].line,3);self.assertEqual(f[0].name,'r.x1.r1')
 def test_two_instances_model_scope_preserved(self):
  self.assertTrue(callable(flatten),'flatten missing')
  s='t\n.subckt a p n\nS1 p n p n sw\n.model sw vswitch(ron=10m roff=1e12 von=.01 voff=0)\n.ends\nX1 one 0 a\nX2 two 0 a\n';f=flatten(s);self.assertEqual(len(f),2);self.assertEqual(f[0].model['ron'],.01);self.assertNotEqual(f[0].name,f[1].name)
 def test_continuation_and_parent_pin(self):
  self.assertTrue(callable(flatten),'flatten missing')
  f=flatten('t\n.subckt a p n params: r=1k\nR1 p n {r}\n.ends\nX1 hi 0 a params:\n+ r=2k\n');self.assertEqual(f[0].params['r'],2000);self.assertEqual(f[0].nodes,['hi','0'])
if __name__=='__main__':unittest.main()
