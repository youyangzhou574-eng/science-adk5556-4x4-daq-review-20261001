import unittest,math
from progress_protocol import ProgressReceiver,FrameFault
from protocol import generate_frame
class ProgressTests(unittest.TestCase):
    def fresh(self):
        v=ProgressReceiver();v.reset(1,0);v.configure(1,100,[6]*4,3);return v
    def frame(self,v,fid,start):
        for s in range(8):
            t=start+1.2*(s+1)
            p={'frame_id':fid,'state_index':s,'completion_ms':t,'sample_count':32*(s+1)}
            v.heartbeat(v.epoch,t+.1,v.seen_id,p)
        return v.complete(v.epoch,fid,start+9.6,start+9.8,generate_frame(fid)[1])
    def healthy(self,first=1):
        v=self.fresh();self.assertFalse(self.frame(v,first,100));self.assertTrue(self.frame(v,(first+1)%2**32,110));self.assertTrue(v.data_valid);return v
    def repeat(self,v,t):
        v.heartbeat(v.epoch,t,v.seen_id,{'frame_id':v.seen_id,'state_index':7,'completion_ms':119.6,'sample_count':256})
    def test_01_normal_states_and_two_frames(self):self.healthy()
    def test_02_frozen_progress_despite_heartbeats(self):
        v=self.healthy()
        for t in [120,121,122]:self.repeat(v,t)
        self.assertFalse(v.tick(122.2));self.assertFalse(v.data_valid)
    def test_03_heartbeat_missing_latency(self):
        v=self.healthy();self.assertFalse(v.tick(124.3));self.assertFalse(v.data_valid)
    def test_04_fault_in_each_state_with_queue_and_tick_jitter(self):
        for state in range(8):
            v=self.healthy()
            for s in range(state+1):
                t=120+1.2*(s+1);p={'frame_id':3,'state_index':s,'completion_ms':t,'sample_count':32*(s+1)}
                v.heartbeat(1,t+.5,2,p)
            onset=t+.001
            invalid=None
            for k in range(1,11):
                now=t+.5+k
                v.heartbeat(1,now,2,p);v.tick(now)
                if not v.data_valid:invalid=now;break
            self.assertIsNotNone(invalid);self.assertLessEqual(invalid-onset,10)
    def test_05_timestamp_cannot_fake_state_advancement(self):
        v=self.healthy();p={'frame_id':2,'state_index':7,'completion_ms':120.1,'sample_count':256}
        with self.assertRaises(FrameFault):v.heartbeat(1,120.2,2,p)
        self.assertFalse(v.data_valid)
    def test_06_skip_and_bad_count_rejected(self):
        v=self.healthy();p={'frame_id':3,'state_index':2,'completion_ms':121.2,'sample_count':96}
        with self.assertRaises(FrameFault):v.heartbeat(1,121.3,2,p)
        self.assertFalse(v.data_valid)
        v=self.healthy();p={'frame_id':3,'state_index':0,'completion_ms':121.2,'sample_count':1}
        with self.assertRaises(FrameFault):v.heartbeat(1,121.3,2,p)
    def test_07_wrap_and_epoch_keep_receive_clock(self):
        v=self.healthy(0xfffffffe);self.assertTrue(self.frame(v,0,120))
        v.reset(2,130);v.configure(2,230,[6]*4,3)
        with self.assertRaises(FrameFault):v.heartbeat(1,231.3,None,{'frame_id':1,'state_index':0,'completion_ms':231.2,'sample_count':32})
        self.assertFalse(v.data_valid)
        with self.assertRaises(FrameFault):v.reset(3,0)
        v=self.healthy()
        with self.assertRaises(FrameFault):v.reset(1,120)
        self.assertFalse(v.data_valid)
        v=self.healthy()
        with self.assertRaises(FrameFault):v.configure(1,120,[5]*4,3)
        self.assertFalse(v.data_valid)
    def test_08_timeout_replay_and_two_new_frames_recover(self):
        v=self.healthy();v.tick(123)
        self.repeat(v,123.1);self.assertFalse(v.data_valid)
        with self.assertRaises(FrameFault):v.complete(1,2,119.6,123.2,generate_frame(2)[1])
        self.assertFalse(self.frame(v,3,130));self.assertTrue(self.frame(v,4,140));self.assertTrue(v.data_valid)
    def test_09_pgood_and_bad_sample_immediate(self):
        v=self.healthy();v.pgood(False,120);self.assertFalse(v.data_valid)
        v=self.healthy()
        with self.assertRaises(FrameFault):v.sample(0,0,6)
        self.assertFalse(v.data_valid)
        v=self.healthy()
        with self.assertRaises(FrameFault):v.sample((123<<16)|(5<<7),0,5)
        self.assertFalse(v.data_valid)
    def test_10_complete_requires_observed_full_progress(self):
        v=self.fresh()
        with self.assertRaises(FrameFault):v.complete(1,1,109.6,109.8,generate_frame(1)[1])
        self.assertFalse(v.data_valid)
    def test_11_invalid_future_nonfinite_progress_and_bounds(self):
        for value in [float('nan'),float('inf'),121.5]:
            v=self.healthy()
            with self.assertRaises(FrameFault):v.heartbeat(1,121.3,2,{'frame_id':3,'state_index':0,'completion_ms':value,'sample_count':32})
            self.assertFalse(v.data_valid)
if __name__=='__main__':unittest.main()
