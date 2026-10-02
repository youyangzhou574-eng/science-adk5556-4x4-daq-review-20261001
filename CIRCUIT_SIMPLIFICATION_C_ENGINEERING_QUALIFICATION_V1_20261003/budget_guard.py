import copy
from datetime import datetime

def precharge(budget, costs, now):
    if budget['stop']:
        raise RuntimeError('sticky STOP')
    if now >= datetime.fromisoformat(budget['deadlineUTC'].replace('Z','+00:00')):
        raise RuntimeError('total deadline')
    for key, amount in costs.items():
        if not isinstance(amount,int) or amount < 1:
            raise RuntimeError('invalid charge')
        if budget['actual'][key]+amount > budget['limits'][key]:
            raise RuntimeError('quota '+key)
    result=copy.deepcopy(budget)
    for key, amount in costs.items():
        result['actual'][key]+=amount
    return result
