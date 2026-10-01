"""Actual macro-expression subset, branch-aware forward-mode Jacobian."""
import ast,re,numpy as np
from spice_flatten import number,constant
class NonDifferentiable(ValueError):pass
class Dual:
 def __init__(self,v,g):self.v=float(v);self.g=np.asarray(g,dtype=float)
 def cast(self,x):return x if isinstance(x,Dual)else Dual(x,np.zeros_like(self.g))
 def __add__(self,x):x=self.cast(x);return Dual(self.v+x.v,self.g+x.g)
 __radd__=__add__
 def __neg__(self):return Dual(-self.v,-self.g)
 def __sub__(self,x):return self+(-self.cast(x))
 def __rsub__(self,x):return self.cast(x)-self
 def __mul__(self,x):x=self.cast(x);return Dual(self.v*x.v,self.g*x.v+x.g*self.v)
 __rmul__=__mul__
 def __truediv__(self,x):x=self.cast(x);return Dual(self.v/x.v,(self.g*x.v-x.g*self.v)/x.v**2)
 def __rtruediv__(self,x):return self.cast(x)/self

def evaluate(expr,op,variables,params,node):
 n=len(variables);index={v:i for i,v in enumerate(variables)};values={};counter=0
 def voltage(m):
  nonlocal counter
  names=[node(s.strip().lower())for s in m[1].split(',')];names+=['0']if len(names)==1 else []
  d=Dual(0,np.zeros(n))
  for sign,name in zip((1,-1),names):
   if name!='0':
    g=np.zeros(n);g[index[name]]=1;d+=sign*Dual(op[name],g)
  key='_voltage_'+str(counter);counter+=1;values[key]=d;return key
 text=re.sub(r'(?i)\bV\(([^()]*)\)',voltage,expr.strip().strip('{}'))
 text=re.sub(r'(?<![\w.])((?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?[a-df-zA-DF-Z][a-zA-Z]*)',lambda m:str(number(m[0])),text)
 text=text.replace('||',' or ').replace('&&',' and ').replace('|',' or ').replace('&',' and ').replace('^','**')
 tree=ast.parse(text.strip(),mode='eval')
 scalar=lambda x:x if isinstance(x,Dual)else Dual(x,np.zeros(n))
 def boundary(a,b,label):
  if abs(a-b)<=1e-12*max(1,abs(a),abs(b)):raise NonDifferentiable((label,a,b))
 def walk(q):
  if isinstance(q,ast.Constant):return scalar(q.value)
  if isinstance(q,ast.Name):return values[q.id]if q.id in values else scalar(params[q.id.lower()])
  if isinstance(q,ast.UnaryOp):return -walk(q.operand)if isinstance(q.op,ast.USub)else walk(q.operand)
  if isinstance(q,ast.BinOp):
   a,b=walk(q.left),walk(q.right)
   if isinstance(q.op,ast.Add):return a+b
   if isinstance(q.op,ast.Sub):return a-b
   if isinstance(q.op,ast.Mult):return a*b
   if isinstance(q.op,ast.Div):return a/b
   if isinstance(q.op,ast.Pow):
    assert not np.any(b.g),'variable exponent unsupported';boundary(a.v,0,'power0');return Dual(a.v**b.v,b.v*a.v**(b.v-1)*a.g)
  if isinstance(q,ast.Compare):
   assert len(q.ops)==1,'chained comparison unsupported';a,b=walk(q.left).v,walk(q.comparators[0]).v;boundary(a,b,'comparison kink')
   return {ast.Gt:lambda:a>b,ast.Lt:lambda:a<b,ast.GtE:lambda:a>=b,ast.LtE:lambda:a<=b}[type(q.ops[0])]()
  if isinstance(q,ast.BoolOp):
   vals=[bool(walk(x))for x in q.values];return any(vals)if isinstance(q.op,ast.Or)else all(vals)
  if isinstance(q,ast.Call):
   fn=q.func.id.lower()
   if fn in ('if','ternary_fcn'):return walk(q.args[1]if walk(q.args[0])else q.args[2])
   args=[walk(a)for a in q.args]
   if fn in ('min','max'):
    a,b=args;boundary(a.v,b.v,fn+' kink');return a if (a.v<b.v if fn=='min'else a.v>b.v)else b
   if fn=='limit':
    a,lo,hi=args;boundary(a.v,lo.v,'LIMIT lower kink');boundary(a.v,hi.v,'LIMIT upper kink');return lo if a.v<lo.v else hi if a.v>hi.v else a
   if fn=='abs':
    a=args[0];boundary(a.v,0,'ABS kink');return a if a.v>0 else -a
   if fn=='pwr':
    a,b=args;assert not np.any(b.g);boundary(a.v,0,'PWR kink');return Dual(abs(a.v)**b.v,b.v*abs(a.v)**(b.v-1)*np.sign(a.v)*a.g)
  raise ValueError(('unsupported behavior AST',ast.dump(q),expr))
 return scalar(walk(tree.body))

def table(expr,op,variables,params,node):
 m=re.search(r'(?i)TABLE\s*\{([^}]*)\}',expr);assert m,expr;x=evaluate(m[1],op,variables,params,node)
 pairs=[(constant(a,params),constant(b,params))for a,b in re.findall(r'\(([^(),]+),([^(),]+)\)',expr[m.end():])];assert len(pairs)>=2
 for a,b in pairs:
  if abs(x.v-a)<=1e-12*max(1,abs(a)):raise NonDifferentiable(('TABLE knot',x.v,a))
 if x.v<pairs[0][0]:return Dual(pairs[0][1],np.zeros_like(x.g))
 if x.v>pairs[-1][0]:return Dual(pairs[-1][1],np.zeros_like(x.g))
 for (a,b),(c,d)in zip(pairs,pairs[1:]):
  if a<x.v<c:return Dual(b+(d-b)*(x.v-a)/(c-a),x.g*(d-b)/(c-a))
 raise ValueError('TABLE segments not monotone')
