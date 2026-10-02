import unittest,math
from audit_core import rigid_reuse,identity_digest
class AuditTest(unittest.TestCase):
 def test_rotated_translated_old_block_fails(self):
  a={str(i):(i%4,i//4) for i in range(12)};b={r:(20-y,10+x) for r,(x,y) in a.items()}
  self.assertGreater(rigid_reuse(a,b)['fraction'],.7)
 def test_not_reusing_old_relative_shape(self):
  a={str(i):(i%4,i//4) for i in range(12)};b={r:(x*3+y*.2,y*4+x*.3) for r,(x,y) in a.items()}
  self.assertLessEqual(rigid_reuse(a,b)['fraction'],.7)
 def test_identity_ignores_position_but_not_net(self):
  a={'r':{'pads':[{'number':'1','net':'A'}],'name':'r','xMm':1,'rotation':90}}
  b={'r':{'pads':[{'number':'1','net':'A'}],'name':'r','xMm':9,'rotation':0}}
  self.assertEqual(identity_digest(a),identity_digest(b));b['r']['pads'][0]['net']='B';self.assertNotEqual(identity_digest(a),identity_digest(b))
if __name__=='__main__':unittest.main()
