"""Original primitive descriptor stamps, full internal dynamic variables retained."""
from dataclasses import dataclass
import numpy as np,re
from scipy.linalg import solve
from spice_flatten import constant,number
from expression import evaluate,table,NonDifferentiable
from pwl import tangent

@dataclass
class Descriptor:
 E:np.ndarray;A:np.ndarray;B:dict;variables:list;stamps:list;branches:dict
 def transfer(self,s,source,out):
  x=solve(s*self.E-self.A,self.B[source],assume_a='gen');return x[self.variables.index(out)]

def build(elements,op):
 nodes=sorted(set(n for e in elements for n in e.nodes if n!='0'))
 branches={e.name:len(nodes)+j for j,e in enumerate(e for e in elements if e.kind in 'vehlb'or(e.kind=='a'and e.model['type']=='pwl'))};variables=nodes+['branch:'+name for name in branches];idx={n:j for j,n in enumerate(nodes)};n=len(variables);E=np.zeros((n,n));K=np.zeros((n,n));B={};stamps=[]
 def incidence(p,m):
  z=np.zeros(n)
  if p!='0':z[idx[p]]+=1
  if m!='0':z[idx[m]]-=1
  return z
 for e in elements:
  beforeK=K.copy();beforeE=E.copy();p,m=e.nodes[:2];iv=incidence(p,m);args=e.args;params=e.params
  def node(v):return '0'if v in ('0','gnd')else e.aliases.get(v,e.scope+'.'+v if e.scope else v)
  def value():return constant(args.split()[-1]if not args.strip().startswith('{')else args,params)
  def behavior():
   if re.search(r'(?i)\bTABLE\b',args):return table(args,op,variables,params,node)
   text=args[args.index('{')+1:args.rindex('}')];return evaluate(text,op,variables,params,node)
  if e.kind=='r':K+=np.outer(iv,iv)/value()
  elif e.kind=='c':E+=np.outer(iv,iv)*value()
  elif e.kind=='i':B[e.name]=-iv
  elif e.kind in 'vehlb':
   j=branches[e.name];K[:,j]+=iv;K[j,:]+=iv
   if e.kind=='v':B[e.name]=np.eye(n)[j]
   elif e.kind=='l':E[j,j]-=value()
   elif e.kind=='h':
    ctrl,gain=args.split();fullname='v.'+e.scope+'.'+ctrl.lower()if e.scope else ctrl.lower();K[j,branches[fullname]]-=number(gain)
   elif e.kind=='b':
    assert args.startswith('v='),('unqualified B family',e.original);K[j,:]-=evaluate(args[2:],op,variables,params,node).g
   elif re.search(r'(?i)\b(value|table)\b',args):K[j,:]-=behavior().g
   else:K[j,:]-=number(args)*incidence(*e.nodes[2:4])
  elif e.kind=='g':
   grad=behavior().g if re.search(r'(?i)\b(value|table)\b',args)else number(args)*incidence(*e.nodes[2:4]);K+=np.outer(iv,grad)
  elif e.kind=='a'and e.model['type']=='pwl':
   model=e.model;cp,cm=e.nodes[2:];x=op.get(cp,0)-op.get(cm,0);_,slope=tangent(x,model)
   j=branches[e.name];K[:,j]+=iv;K[j,:]+=iv;K[j,:]-=slope*incidence(cp,cm)
  elif e.kind=='s'or(e.kind=='a'and e.model['type']=='pswitch'):
   model=e.model
   if model['type']=='pswitch':model=dict(model,ron=model['r_on'],roff=model['r_off'],voff=model['cntl_off'],von=model['cntl_on'])
   if model['type']=='sw':model=dict(model,voff=model.get('vt',0)-abs(model.get('vh',0)),von=model.get('vt',0)+abs(model.get('vh',0)))
   assert model.get('type')in ('vswitch','pswitch','sw'),('unsupported switch family',model,e.original)
   cp,cm=e.nodes[2:];control=op.get(cp,0)-op.get(cm,0);voff,von=model['voff'],model['von'];assert von>voff
   if min(abs(control-voff),abs(control-von))<=1e-12*max(1,abs(control)):raise NonDifferentiable(('switch threshold',e.name,control,model))
   if voff<control<von:raise NonDifferentiable(('PSA_SWITCH_TRANSITION_JACOBIAN_NOT_QUALIFIED',e.name,control,model))
   resistance=model['ron']if control>von else model['roff'];K+=np.outer(iv,iv)/resistance
   if model['type']!='sw':
    ci=incidence(cp,cm);K+=np.outer(ci,ci)/model.get('r_cntl_in',1e12)
  else:raise ValueError(('unsupported stamp',e.kind,e.original))
  dk=K-beforeK;de=E-beforeE;entries=[]
  for matrix,label in [(dk,'K'),(de,'E')]:
   ii,jj=np.nonzero(matrix)
   entries.extend({'matrix':label,'row':int(i),'column':int(j),'value':float(matrix[i,j])}for i,j in zip(ii,jj))
  stamps.append({'element':e.name,'primitive':e.kind,'source':e.source,'line':e.line,'original':e.original,'entries':entries})
 return Descriptor(E,-K,B,variables,stamps,branches)
