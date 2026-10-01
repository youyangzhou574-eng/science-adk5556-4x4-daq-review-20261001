import unittest
from protocol import Validator,FrameFault,decode,generate_frame,STATES,difference
class Tests(unittest.TestCase):
 def setUp(self):
  self.v=Validator();self.v.reset(1,0);self.v.configure(1,100,[6]*4,3)
 def frame(self,i,t,epoch=1):return self.v.complete(epoch,i,t,t+.1,generate_frame(i)[1])
 def test_two_consecutive(self):self.assertFalse(self.frame(1,110));self.assertTrue(self.frame(2,120))
 def test_gap_10_seconds(self):
  self.frame(1,110)
  with self.assertRaises(FrameFault):self.frame(2,10110)
  self.assertEqual(self.v.good,0)
 def test_jump(self):
  self.frame(1,110)
  with self.assertRaises(FrameFault):self.frame(100,120)
 def test_duplicate(self):
  self.frame(1,110)
  with self.assertRaises(FrameFault):self.frame(1,120)
 def test_wrap(self):self.assertFalse(self.frame(0xffffffff,110));self.assertTrue(self.frame(0,120))
 def test_old_epoch(self):
  with self.assertRaises(FrameFault):self.frame(1,110,0)
 def test_old_capture(self):
  with self.assertRaises(FrameFault):self.v.complete(1,1,99,110,generate_frame(1)[1])
 def test_late_receive(self):
  with self.assertRaises(FrameFault):self.v.complete(1,1,110,120,generate_frame(1)[1])
 def test_no_new_data(self):
  self.frame(1,110);self.frame(2,120);self.v.heartbeat(1,120.2,2)
  self.assertFalse(self.v.tick(125.21));self.assertEqual(self.v.good,0)
 def test_data_expiry_despite_heartbeats(self):
  self.frame(1,110);self.frame(2,120)
  for t in (121,122,123,124,125,126,127,128,129,130):self.v.heartbeat(1,t,2)
  self.assertFalse(self.v.tick(131));self.assertEqual(self.v.good,0)
 def test_recovery_requires_two(self):
  self.frame(1,110);self.frame(2,120);self.v.tick(131)
  self.assertFalse(self.frame(3,140));self.assertTrue(self.frame(4,150))
 def test_expired_frames_cannot_replay(self):
  self.frame(1,110);self.frame(2,120);self.assertFalse(self.v.tick(1000))
  for i,t in ((1,110),(2,120)):
   with self.assertRaises(FrameFault):self.frame(i,t)
  self.assertFalse(self.v.valid)
 def test_duplicate_cannot_seed_recovery(self):
  self.frame(1,110);self.frame(2,120)
  for rx in (120.15,120.2):
   with self.assertRaises(FrameFault):self.v.complete(1,2,120,rx,generate_frame(2)[1])
  self.assertFalse(self.frame(3,130));self.assertTrue(self.frame(4,140))
 def test_receiver_clock_cannot_reverse(self):
  self.frame(1,110);self.v.tick(115)
  with self.assertRaises(FrameFault):self.v.heartbeat(1,114,1)
  with self.assertRaises(FrameFault):self.v.tick(113)
  self.assertFalse(self.v.valid)
 def test_nonfinite_time_rejected(self):
  for x in (float('nan'),float('inf'),-float('inf')):
   with self.assertRaises(FrameFault):self.v.tick(x)
   with self.assertRaises(FrameFault):self.v.heartbeat(1,x,None)
 def test_new_epoch_keeps_receiver_clock(self):
  self.frame(1,110);self.v.tick(1000)
  with self.assertRaises(FrameFault):self.v.reset(2,0)
  self.v.reset(2,1001);self.v.configure(2,1101,[6]*4,3)
  self.assertFalse(self.frame(1,1111,2));self.assertTrue(self.frame(2,1121,2))
 def test_missing_sample(self):
  with self.assertRaises(FrameFault):self.v.complete(1,1,110,110.1,generate_frame(1)[1][:-1])
 def test_bad_label(self):
  x=generate_frame(1)[1];x[0]=(x[0][0],x[0][1],x[0][2]^(1<<12))
  with self.assertRaises(FrameFault):self.v.complete(1,1,110,110.1,x)
 def test_event_counts_and_edges(self):
  events,samples=generate_frame(0);self.assertEqual(len(events),288);self.assertEqual(len(samples),256);self.assertEqual(sum(x['dummy']for x in events),32)
  self.assertEqual([x['state']for x in events[::36]],list(STATES))
  for x in events:
   self.assertEqual(x['sample_channel'],x['returned_channel'])
   self.assertLess(x['cs_fall_us'],x['cs_rise_us'])
   self.assertIn(sum(x['row_select']),[0,1])
 def test_independent_wire_vectors(self):
  # Literal cycles 1..16 precede B15; cycles17..32 code;33..41 tags;42..48 zeros.
  # Table13/14 and mode1 falling-edge capture of previously launched bit.
  for code,ch,dev,ran,bits in [
   (0xa5c3,2,0,6,'0000000000000000' '1010010111000011' '0010' '00' '110' '0000000'),
   (0x8001,3,0,6,'0000000000000000' '1000000000000001' '0011' '00' '110' '0000000'),
   (0xffff,1,0,6,'0000000000000000' '1111111111111111' '0001' '00' '110' '0000000')]:
   self.assertEqual(decode(int(bits,2),ch,ran)['code'],code)
 def test_adjacent_difference(self):
  _,s=generate_frame(0);d=difference(s)
  self.assertEqual(len(d),16)
  self.assertEqual(d['ROW0_CH0']['D_code'],100)
  self.assertEqual(d['ROW3_CH3']['D_code'],400)
if __name__=='__main__':unittest.main()
