import unittest
try:from pwl import tangent
except ImportError:tangent=None
class PWL(unittest.TestCase):
 def test_positive_endpoint_native_follower_op_derivative(self):
  self.assertTrue(callable(tangent));m={'x_array':[0,10,22,45,53,60],'y_array':[11.47e-6,1.5e-4,3e-4,6.9e-4,9e-4,1.24e-3],'input_domain':.1,'fraction':True,'limit':True}
  self.assertAlmostEqual(tangent(.2500001316567726,m)[1],8.658125911920636e-6,places=17)
 def test_negative_endpoint_native_follower_op_derivative(self):
  self.assertTrue(callable(tangent));m={'x_array':[0,11,60],'y_array':[15.45e-6,3.35e-4,1.9e-3],'input_domain':.1,'fraction':True,'limit':True}
  self.assertAlmostEqual(tangent(-.2500001316567726,m)[1],1.122386189789580e-5,places=17)
if __name__=='__main__':unittest.main()
