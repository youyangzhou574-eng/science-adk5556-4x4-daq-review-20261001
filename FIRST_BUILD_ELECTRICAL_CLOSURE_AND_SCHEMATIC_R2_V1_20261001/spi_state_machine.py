"""Offline sequencing and payload-contract model. Not a hardware SPI driver."""
import pathlib,json,csv,collections
class FrameFault(ValueError):pass
class Pipeline:
 def __init__(self,initial_channel=0):self.channel=initial_channel
 def transfer(self,command,code):
  result={'command':command,'conversion_channel_at_CS_fall':self.channel,'returned_channel':self.channel,'code':code}
  if command in [0xC000,0xC400,0xC800,0xCC00]:self.channel=(command-0xC000)//0x400
  elif command!=0:raise FrameFault('unsupported acquisition command')
  result['current_channel_after_CS_rise']=self.channel
  return result
def decode(word,expected_channel,expected_range):
 if not(0<=word<2**48):raise FrameFault('48-bit frame required')
 ch=(word>>12)&15;device=(word>>10)&3;ran=(word>>7)&7
 if ch!=expected_channel or ran!=expected_range or device!=0:raise FrameFault('SDO channel/range/device mismatch')
 return {'code':(word>>16)&65535,'channel':ch,'range':ran,'device':device}
class Validity:
 def __init__(self):self.valid=False;self.pgood=False;self.configured=False;self.good_frames=0;self.ready_since=None;self.configured_at=None;self.last_frame_id=None;self.last_frame_time=None
 def power_good(self,good,time_ms):
  self.pgood=bool(good)
  self.valid=False;self.configured=False;self.good_frames=0
  self.ready_since=time_ms if good else None
 def configure(self,range_readback,feature_readback,time_ms):
  if not self.pgood or self.ready_since is None or time_ms-self.ready_since<100:
   self.valid=False;raise FrameFault('power/reference wait not satisfied')
  if range_readback!=[6]*4 or feature_readback!=3:
   self.valid=False;self.configured=False;raise FrameFault('range/feature readback mismatch')
  self.configured=True;self.good_frames=0;self.valid=False;self.configured_at=time_ms;self.last_frame_id=None;self.last_frame_time=None
 def fault(self,time_ms):
  self.valid=False;self.configured=False;self.good_frames=0
  self.ready_since=time_ms if self.pgood else None
  self.configured_at=None;self.last_frame_id=None;self.last_frame_time=None
 def complete_frame(self,time_ms,frame_id,samples):
  try:
   if not self.pgood or not self.configured:raise FrameFault('unqualified frame')
   previous=self.last_frame_time if self.last_frame_time is not None else self.configured_at
   if time_ms-previous<10-1e-9:raise FrameFault('frame period/qualification not satisfied')
   if self.last_frame_id is not None and frame_id<=self.last_frame_id:raise FrameFault('duplicate/out-of-order frame')
   counts=collections.Counter()
   for state,ch,word in samples:
    if state not in ['BLANK_PRE','ROW0','ROW1','ROW2','ROW3','BLANK_POST']or ch not in range(4):raise FrameFault('invalid state/channel')
    decode(word,ch,6);counts[(state,ch)]+=1
   required={(state,ch):8 for state in ['BLANK_PRE','ROW0','ROW1','ROW2','ROW3','BLANK_POST']for ch in range(4)}
   if dict(counts)!=required:raise FrameFault('incomplete/duplicated channel-state samples')
   self.last_frame_id=frame_id;self.last_frame_time=time_ms
   self.good_frames+=1;self.valid=self.good_frames>=2;return self.valid
  except (FrameFault,ValueError,TypeError):
   self.fault(time_ms);raise FrameFault('frame fault: abort and requalify reference/configuration')


def generate_trace():
 p=pathlib.Path(__file__).resolve().parent;pipe=Pipeline();rows=[];t=0;validity=Validity();validity.power_good(True,0);validity.configure([6]*4,3,100);qualified=[]
 # Six states: blank-before, rows0..3, blank-after. Eight valid samples/channel.
 for frame in range(3):
  frame_samples=[]
  for state in ['BLANK_PRE','ROW0','ROW1','ROW2','ROW3','BLANK_POST']:
   t+=300
   for ch in range(4):
    d=pipe.transfer(0xC000+ch*0x400,0);rows.append({'frame':frame,'state':state,'time_us':t,'intended_channel':ch,'dummy':True,**d});t+=25
    for sample in range(8):
     d=pipe.transfer(0,32000+ch);assert d['returned_channel']==ch
     word=(d['code']<<16)|(ch<<12)|(6<<7);decoded=decode(word,ch,6);frame_samples.append((state,ch,word))
     rows.append({'frame':frame,'state':state,'time_us':t,'intended_channel':ch,'dummy':False,'sample':sample,**d,'decoded_code':decoded['code']});t+=25
  assert t==(frame+1)*10000-2800
  t+=2800
  qualified.append(validity.complete_frame(100+t/1000,frame,frame_samples))
 with(p/'SPI_OFFLINE_TRACE.csv').open('w',encoding='utf-8-sig',newline='')as f:
  fields=list(dict.fromkeys(k for r in rows for k in r));w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 result={'frames':3,'software_frame_validity':qualified,'qualified_frame_sample_contract':'6 states x4channels x8tagged samples, unique monotonic frame IDs, >=10ms; bad/incomplete frame immediately revokes software validity','transfer_frames':len(rows),'dummy_frames':sum(x['dummy']for x in rows),'valid_channel_samples':sum(not x['dummy']for x in rows),'conversion_period_us':25,'spi_clock_Hz':4000000,'clocks_per_SPI_frame':48,'SPI_wire_time_us':12,'states_per_frame':6,'valid_samples_per_channel_state':8,'active_acquisition_us':7200,'padding_us':2800,'complete_frame_Hz':100,'initialization':{'reference_wait_ms':100,'datasheet_reference_powerup_ms_at22uF':15,'reference_wait_status':'100ms engineering guard for44uF, not a proven settlement bound; HOLD','channel_range_registers':{'05h':6,'06h':6,'07h':6,'08h':6},'feature_register_03h':3,'readback_required':True},'invalidity':'PGOOD loss clears valid immediately in software model; packet tag/range exceptions must trigger abort/reinit; hardware latency unverified','recovery':'power qualified +100ms guard +register readback +two complete good frames','bit_alignment_assumption':'48 clocks, falling-edge SDO, rising-edge capture; 16 leading bits,16data,9metadata,7padding; unverified on silicon','scope':'offline logic model only; hardware SPI, ADC multiplexer settling and frame noise remain HOLD'}
 (p/'SPI_OFFLINE_SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':generate_trace()
