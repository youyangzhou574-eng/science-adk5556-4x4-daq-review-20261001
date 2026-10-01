import unittest,numpy as np
from mimo_math import return_difference
class MimoMathTests(unittest.TestCase):
    def test_bilateral_coupled_closure(self):
        rng=np.random.default_rng(5556);y=rng.normal(size=(5,6,6))+1j*rng.normal(size=(5,6,6));y+=np.eye(6)*20
        l,r,d,g=return_difference(y)
        self.assertTrue(np.allclose(g,d@r))
        self.assertTrue(np.allclose(g,y[:,:3,:3]+y[:,:3,3:]+y[:,3:,:3]+y[:,3:,3:]))
    def test_scalar_loaded_Tian_identity(self):
        y=np.array([[[1e-5,2e-7],[.1,1e-3]]],dtype=complex)
        l,r,d,g=return_difference(y)
        self.assertAlmostEqual(l[0,0,0],(.1+2e-7)/.00101)
    def test_decoupled_known_gain(self):
        y=np.zeros((1,4,4),complex);y[0,:2,:2]=np.eye(2)*1e-5;y[0,2:,2:]=np.eye(2)*.001;y[0,2:,:2]=np.array([[.1,.015],[.005,.1]])
        l,r,d,g=return_difference(y);self.assertTrue(np.allclose(l[0],np.array([[.1,.015],[.005,.1]])/.00101))
if __name__=='__main__':unittest.main()
