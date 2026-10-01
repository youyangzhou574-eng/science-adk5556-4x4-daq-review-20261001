"""Read the actual first `listing e` deck, including PSA algebraic wrappers."""
import re
from spice_flatten import Element,number
def parse(text,source='<listing e>'):
 cards=[]
 for line in text.splitlines():
  q=re.match(r'\s*(\d+)\s*:\s*(.*)',line)
  if not q:continue
  card=q[2].strip().lower()
  if card=='.end':break
  if int(q[1])!=1:cards.append((int(q[1]),card))
 models={}
 for ln,card in cards:
  if not card.startswith('.model '):continue
  q=re.match(r'\.model\s+(\S+)\s+(\w+)\s*\((.*)\)',card);assert q,card
  model={'type':q[2]}
  for name,value in re.findall(r'(\w+)\s*=\s*(\[[^]]*\]|[^\s)]+)',q[3]):
   model[name]=[number(v)for v in value.strip('[]').split()]if value.startswith('[')else value=='true'if value in ('true','false')else number(value)
  models[q[1]]=model
 out=[]
 for ln,card in cards:
  if not card or card[0]in '.*':continue
  t=card.split();kind=t[0][0];model={}
  if kind=='a':
   model=models[t[-1]]
   if model['type']=='pwl':assert t[1]=='%v'and t[3]=='%v';nodes=[t[4],'0',t[2],'0']
   elif model['type']=='pswitch':assert t[1]=='%gd'and t[4]=='%gd';nodes=t[5:7]+t[2:4]
   else:raise ValueError(('unsupported code model',card))
   args=t[-1]
  else:
   assert kind in 'rcvieghbs',('unhandled processed primitive',card)
   count=4 if kind in 'egs'else 2;nodes=t[1:1+count];args=' '.join(t[1+count:])
   if kind=='s':model=models[t[-1]]
  # Element.line here is ngspice listingCardNumber, NOT a physical log line.
  # Complete processed-to-original frozen LIB source bridge remains unqualified.
  out.append(Element(t[0],kind,nodes,args,{'temper':27.},source,ln,'',model,card,{}))
 return out
