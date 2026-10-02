import unittest,json,copy
from b31_core import P
from audit_b31 import channel_audit
class AuditRegression(unittest.TestCase):
 def setUp(self):self.pos=json.loads((P/'PLACEMENT_B31.json').read_text())['positions']
 def test_real_complete_cells_pass(self):self.assertTrue(all(x['pass'] for x in channel_audit(self.pos)))
 def test_missing_clamp_fails(self):
  del self.pos['D_ROW3'];self.assertFalse(channel_audit(self.pos)[1]['pass'])
 def test_one_role_position_change_fails(self):
  self.pos['RF2'][0]+=.1;self.assertFalse(channel_audit(self.pos)[0]['pass'])
 def test_wrong_iso_orientation_fails(self):
  self.pos['R_ISO0'][2]+=180;self.assertFalse(channel_audit(self.pos)[1]['pass'])
if __name__=='__main__':unittest.main()
