"""Executable progress watchdog contract; 1ms tick/0.5ms transport are obligations,
not verified firmware timing. Frozen base validator and its 21 tests stay unchanged.
"""
import math
from protocol import Validator,FrameFault,decode
class ProgressReceiver(Validator):
    def __init__(self):
        self.pgood_ok=True;self.progress_seen=None;self.progress_received=None
        self.frame_states=set();self.heartbeat_received=None;super().__init__()
    def clear(self):
        super().clear();self.frame_states=set()
        # Keep progress_seen/time and the base replay/receive-clock watermarks.
    def reset(self,epoch,time_ms):
        try:super().reset(epoch,time_ms)
        except (FrameFault,ValueError,TypeError):self.clear();raise FrameFault('reset rejected; qualification cleared')
        self.progress_seen=None;self.progress_received=None;self.heartbeat_received=None;self.frame_states=set()
    def configure(self,epoch,time_ms,ranges,feature):
        try:super().configure(epoch,time_ms,ranges,feature)
        except (FrameFault,ValueError,TypeError):self.clear();raise FrameFault('configure rejected; qualification cleared')
        self.progress_received=time_ms;self.heartbeat_received=time_ms
    @property
    def data_valid(self):return bool(self.valid and self.pgood_ok and self.progress_seen is not None)
    def heartbeat(self,epoch,receive_ms,last_completed_id,progress=None):
        try:
            self.tick(receive_ms)
            if epoch!=self.epoch or not self.configured or last_completed_id!=self.seen_id:raise FrameFault('heartbeat epoch/completed-ID mismatch')
            self.heartbeat_received=receive_ms;self.last_heartbeat=receive_ms
            if progress is None:return self.data_valid  # no new progress; cannot reset its deadline
            fid=progress['frame_id'];state=progress['state_index'];cap=progress['completion_ms'];count=progress['sample_count']
            if type(fid)is not int or not 0<=fid<2**32 or type(state)is not int or not 0<=state<=7:raise FrameFault('progress integer/range')
            if type(cap)not in (float,int)or not math.isfinite(cap)or cap>receive_ms:raise FrameFault('progress source clock invalid')
            if type(count)is not int or count!=32*(state+1):raise FrameFault('progress sample count')
            current=(fid,state,cap,count)
            if self.progress_seen is not None:
                pf,ps,pc,pn=self.progress_seen
                if fid==pf and state==ps:
                    if current!=self.progress_seen:raise FrameFault('timestamp/count changed without genuine state advance')
                    return self.data_valid
                regular=(fid==pf and state==ps+1)or(fid==(pf+1)%2**32 and ps==7 and state==0)
                resync=not self.valid and self.good==0 and state==0 and 0<(fid-pf)%2**32<2**31
                if not(regular or resync) or cap<=pc:raise FrameFault('progress replay/sequence gap')
                if state==0:self.frame_states=set()
            elif state!=0:raise FrameFault('qualification starts with state0')
            if cap<self.configured_at or not 0<=receive_ms-cap<=.5:raise FrameFault('stale advancing progress')
            self.progress_seen=current;self.progress_received=receive_ms;self.frame_states.add(state)
            return self.data_valid
        except (KeyError,TypeError,ValueError,FrameFault):self.clear();raise FrameFault('progress rejected; qualification cleared')
    def complete(self,epoch,frame_id,capture_ms,receive_ms,samples):
        try:
            self.tick(receive_ms)
            if not self.pgood_ok or self.progress_seen is None:raise FrameFault('no eligible progress')
            fid,state,cap,count=self.progress_seen
            if (fid,state,count)!=(frame_id,7,256)or self.frame_states!=set(range(8)):raise FrameFault('full observed progress required')
            if not 0<=capture_ms-cap<=.1:raise FrameFault('complete-frame time not tied to last valid state sample')
            super().complete(epoch,frame_id,capture_ms,receive_ms,samples)
            return self.data_valid
        except (TypeError,ValueError,FrameFault):self.clear();raise FrameFault('complete rejected; qualification cleared')
    def tick(self,now_ms):
        self.observe(now_ms)
        stale_heartbeat=self.heartbeat_received is not None and now_ms-self.heartbeat_received>=4.5-1e-9
        stale_progress=self.progress_received is not None and now_ms-self.progress_received>=2.5-1e-9
        stale_frame=self.last_capture is not None and now_ms-self.last_capture>10.25
        if not self.pgood_ok or stale_heartbeat or stale_progress or stale_frame:self.clear()
        return self.data_valid
    def pgood(self,ok,time_ms):
        self.observe(time_ms)
        if type(ok)is not bool:self.clear();raise FrameFault('PGOOD must be Boolean')
        self.pgood_ok=ok
        if not ok:self.clear()
    def sample(self,word,ch,ran):
        try:
            if not self.configured or type(ch)is not int or ch not in range(4)or ran!=6:raise FrameFault('ADC state/configuration contract')
            return decode(word,ch,ran)
        except (FrameFault,TypeError,ValueError):self.clear();raise FrameFault('state-level ADC error; data invalid immediately')
