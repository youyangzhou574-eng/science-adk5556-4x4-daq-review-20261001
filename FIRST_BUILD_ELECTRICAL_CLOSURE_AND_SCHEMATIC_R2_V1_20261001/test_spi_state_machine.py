import unittest
from spi_state_machine import Pipeline,Validity,decode,FrameFault
def samples():
 return [(state,ch,(32000<<16)|(ch<<12)|(6<<7))for state in ['BLANK_PRE','ROW0','ROW1','ROW2','ROW3','BLANK_POST']for ch in range(4)for _ in range(8)]
class SpiRegression(unittest.TestCase):
 def test_manual_command_frame_returns_old_channel_then_nop_returns_new(self):
  pipe=Pipeline(initial_channel=0)
  self.assertEqual(pipe.transfer(0xC800,123)['returned_channel'],0)
  self.assertEqual(pipe.transfer(0x0000,456)['returned_channel'],2)
 def test_incorrect_channel_or_range_tag_rejects_payload(self):
  # 16 leading bits, 16 conversion bits, 9 metadata bits, 7 padding bits.
  good=(0x1234<<16)|(2<<12)|(6<<7)
  self.assertEqual(decode(good,expected_channel=2,expected_range=6)['code'],0x1234)
  with self.assertRaises(FrameFault):decode(good,expected_channel=1,expected_range=6)
  with self.assertRaises(FrameFault):decode(good,expected_channel=2,expected_range=0)
 def test_power_fault_and_two_complete_recovery_frames(self):
  v=Validity();v.power_good(True,0)
  with self.assertRaises(FrameFault):v.configure(range_readback=[6]*4,feature_readback=3,time_ms=20)
  v.configure(range_readback=[6]*4,feature_readback=3,time_ms=100)
  self.assertFalse(v.complete_frame(110,1,samples()));self.assertTrue(v.complete_frame(120,2,samples()))
  v.power_good(False,120.001);self.assertFalse(v.valid)
  v.power_good(True,130)
  with self.assertRaises(FrameFault):v.configure(range_readback=[0,6,6,6],feature_readback=3,time_ms=230)
  self.assertFalse(v.valid)
  v.configure(range_readback=[6]*4,feature_readback=3,time_ms=230)
  self.assertFalse(v.complete_frame(240,3,samples()));self.assertTrue(v.complete_frame(250,4,samples()))
 def test_incomplete_frame_and_same_timestamp_cannot_qualify(self):
  v=Validity();v.power_good(True,0);v.configure([6]*4,3,100)
  with self.assertRaises(FrameFault):v.complete_frame(110,1,samples()[:-1])
  self.assertFalse(v.valid);self.assertFalse(v.configured)
  v.configure([6]*4,3,210)
  self.assertFalse(v.complete_frame(220,1,samples()))
  with self.assertRaises(FrameFault):v.complete_frame(220,2,samples())
  self.assertFalse(v.valid)
 def test_duplicate_frame_rejects_recovery(self):
  v=Validity();v.power_good(True,0);v.configure([6]*4,3,100)
  self.assertFalse(v.complete_frame(110,1,samples()))
  with self.assertRaises(FrameFault):v.complete_frame(120,1,samples())
  self.assertFalse(v.valid)
 def test_bad_tag_revokes_previously_valid_state(self):
  v=Validity();v.power_good(True,0);v.configure([6]*4,3,100)
  v.complete_frame(110,1,samples());v.complete_frame(120,2,samples());self.assertTrue(v.valid)
  bad=samples();state,ch,word=bad[0];bad[0]=(state,ch,word^(1<<7))
  with self.assertRaises(FrameFault):v.complete_frame(130,3,bad)
  self.assertFalse(v.valid);self.assertFalse(v.configured)
if __name__=='__main__':unittest.main()
