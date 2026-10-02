from pathlib import Path
import json,sys,datetime
P=Path(__file__).parent/'EXECUTION_BUDGET.json'
def reserve(kind,count,reason):
    b=json.loads(P.read_text(encoding='utf-8-sig'))
    now=datetime.datetime.now(datetime.timezone.utc)
    if b['status']!='ACTIVE' or now>datetime.datetime.fromisoformat(b['deadlineUTC'].replace('Z','+00:00')):
        raise RuntimeError('STOP: stage inactive or wallclock exhausted')
    used=b['actual'].get(kind,0)
    if used+count>b['limits'][kind]:raise RuntimeError('STOP: quota '+kind)
    b['actual'][kind]=used+count
    b['reservations'].append({'utc':now.isoformat(),'kind':kind,'count':count,'reason':reason})
    P.write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':reserve(sys.argv[1],int(sys.argv[2]),sys.argv[3])
