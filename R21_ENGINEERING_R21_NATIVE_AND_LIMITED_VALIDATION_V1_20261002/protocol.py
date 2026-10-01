"""Executable receiver/sequence contract; no hardware driver or physical latency claim."""
import collections,pathlib,csv,json,math
STATES=tuple(s for i in range(4) for s in (f'BLANK{i}',f'ROW{i}'))
class FrameFault(ValueError):pass
def decode(word,ch,ran):
 if not isinstance(word,int)or not 0<=word<2**48:raise FrameFault('48 bits required')
 channel=(word>>12)&15;device=(word>>10)&3;rr=(word>>7)&7
 if (channel,device,rr)!=(ch,0,ran):raise FrameFault('channel/device/range mismatch')
 return {'code':(word>>16)&65535,'channel':channel,'range':rr,'device':device}
class Validator:
 def __init__(self):
  self.epoch=None;self.configured=False;self.reset_at=None;self.valid=False
  self.clock_watermark=None;self.seen_id=None;self.seen_capture=None;self.clear()
 def clear(self):self.valid=False;self.good=0;self.last_id=None;self.last_capture=None;self.last_receive=None;self.last_heartbeat=None
 def observe(self,time_ms):
  if type(time_ms)not in (int,float)or not math.isfinite(time_ms)or (self.clock_watermark is not None and time_ms<self.clock_watermark):
   self.clear();raise FrameFault('nonfinite or backwards receiver clock')
  self.clock_watermark=time_ms
 def reset(self,epoch,time_ms):
  self.observe(time_ms)
  if self.epoch is not None and epoch<=self.epoch:raise FrameFault('reset epoch must advance')
  self.epoch=epoch;self.reset_at=time_ms;self.configured=False;self.seen_id=None;self.seen_capture=None;self.clear()
 def configure(self,epoch,time_ms,ranges,feature):
  self.observe(time_ms)
  if epoch!=self.epoch or time_ms-self.reset_at<100 or ranges!=[6]*4 or feature!=3:raise FrameFault('unqualified configuration')
  self.configured=True;self.configured_at=time_ms;self.clear()
 def complete(self,epoch,frame_id,capture_ms,receive_ms,samples):
  try:
   self.observe(receive_ms)
   if not self.configured or epoch!=self.epoch:raise FrameFault('old/unqualified epoch')
   if type(frame_id)is not int or not 0<=frame_id<2**32:raise FrameFault('uint32 frame ID required')
   if type(capture_ms)not in (int,float)or not math.isfinite(capture_ms):raise FrameFault('finite capture time required')
   if self.seen_id is not None and not 0<(frame_id-self.seen_id)%2**32<2**31:raise FrameFault('replayed/backwards frame ID')
   if self.seen_capture is not None and capture_ms<=self.seen_capture:raise FrameFault('replayed capture time')
   if capture_ms<self.configured_at+9.6 or not 0<=receive_ms-capture_ms<=.5:raise FrameFault('old/stale capture')
   if self.last_id is not None:
    if frame_id!=(self.last_id+1)%2**32:raise FrameFault('frame sequence gap')
    if not 9.75<=capture_ms-self.last_capture<=10.25:raise FrameFault('frame period gap')
    if not 9.25<=receive_ms-self.last_receive<=10.75:raise FrameFault('receiver discontinuity')
   counts=collections.Counter()
   for state,ch,word in samples:
    if state not in STATES or ch not in range(4):raise FrameFault('invalid label')
    decode(word,ch,6);counts[(state,ch)]+=1
   if dict(counts)!={(s,c):8 for s in STATES for c in range(4)}:raise FrameFault('incomplete frame')
   self.seen_id=frame_id;self.seen_capture=capture_ms
   self.last_id=frame_id;self.last_capture=capture_ms;self.last_receive=receive_ms;self.last_heartbeat=receive_ms
   self.good+=1;self.valid=self.good>=2;return self.valid
  except (FrameFault,ValueError,TypeError):self.clear();raise FrameFault('discard frame; consecutive qualification cleared')
 def heartbeat(self,epoch,receive_ms,last_completed_id):
  self.observe(receive_ms)
  if epoch!=self.epoch or last_completed_id!=self.last_id:self.clear();raise FrameFault('heartbeat epoch/sequence/time mismatch')
  self.last_heartbeat=receive_ms
 def tick(self,now_ms):
  self.observe(now_ms)
  if self.last_receive is not None:
   if now_ms-self.last_heartbeat>4.5 or now_ms-self.last_capture>10.25:self.clear()
  return self.valid
def generate_frame(frame):
 events=[];samples=[];pipe=0
 for si,state in enumerate(STATES):
  i=si//2;row_select=tuple(int(state==f'ROW{k}')for k in range(4));start=si*1200
  for ch in range(4):
   for sample in range(9):
    t=start+300+(ch*9+sample)*25;command=0xc000+ch*0x400 if sample==0 else 0
    sampled_channel=pipe
    code=32000+ch+5*i+(100*(i+1)if state.startswith('ROW')else 0)
    word=(code<<16)|(sampled_channel<<12)|(6<<7)
    events.append({'frame':frame,'state':state,'state_start_us':start,'row_select':row_select,'cs_fall_us':t,'cs_rise_us':t+12.1,'command_hex':f'{command:04X}','target_channel':ch,'sample_channel':sampled_channel,'returned_channel':sampled_channel,'dummy':sample==0,'sample':sample-1,'word_hex':f'{word:012X}'})
    if sample==0:pipe=ch
    else:
     decode(word,ch,6);samples.append((state,ch,word))
 return events,samples
def difference(samples):
 groups=collections.defaultdict(list)
 for state,ch,word in samples:groups[state,ch].append(decode(word,ch,6)['code'])
 out={}
 for i in range(4):
  for ch in range(4):
   A=sum(groups[f'ROW{i}',ch])/8;B=sum(groups[f'BLANK{i}',ch])/8;D=A-B
   out[f'ROW{i}_CH{ch}']={'active_mean_code':A,'adjacent_blank_mean_code':B,'D_code':D,'D_V':D*5.12/65536,'G_ideal_S':D*5.12/65536/(.25*4990),'scope':'synthetic arithmetic fixture; fixed calibration supplied separately, no hardware measurement'}
 return out
if __name__=='__main__':
 root=pathlib.Path(__file__).resolve().parent;events,samples=generate_frame(0)
 with(root/'results/EIGHT_STATE_EVENTS.csv').open('w',encoding='utf-8',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(events[0]));w.writeheader();w.writerows(events)
 (root/'results/ADJACENT_BLANK_DIFFERENCES.json').write_text(json.dumps(difference(samples),indent=2),encoding='utf-8')
 print('events',len(events),'dummy',sum(x['dummy']for x in events),'valid',len(samples))
