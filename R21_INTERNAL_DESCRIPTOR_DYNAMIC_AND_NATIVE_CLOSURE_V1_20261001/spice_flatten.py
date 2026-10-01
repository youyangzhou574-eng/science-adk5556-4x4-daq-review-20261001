"""Project-only source-preserving SPICE hierarchy reader; no general simulator."""
from dataclasses import dataclass,field
from pathlib import Path
import re,ast,operator,math

def number(s):
 m=re.fullmatch(r'([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)([a-zA-Z]*)',s.strip());assert m,('numeric value unsupported',s)
 suffix=m[2].lower();scale=next((v for k,v in [('meg',1e6),('t',1e12),('g',1e9),('k',1e3),('m',1e-3),('u',1e-6),('n',1e-9),('p',1e-12),('f',1e-15)]if suffix.startswith(k)),1.)
 return float(m[1])*scale

def constant(s,params):
 s=s.strip().strip('{}');s=re.sub(r'(?<![\w.])((?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?[a-df-zA-DF-Z][a-zA-Z]*)',lambda m:str(number(m[0])),s)
 tree=ast.parse(s.replace('^','**'),mode='eval')
 def walk(n):
  if isinstance(n,ast.Constant):return float(n.value)
  if isinstance(n,ast.Name):return params[n.id.lower()]
  if isinstance(n,ast.UnaryOp):return (-1 if isinstance(n.op,ast.USub)else 1)*walk(n.operand)
  if isinstance(n,ast.BinOp):return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}[type(n.op)](walk(n.left),walk(n.right))
  if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id.lower()=='pwr':return abs(walk(n.args[0]))**walk(n.args[1])
  raise ValueError(('constant AST unsupported',ast.dump(n)))
 return walk(tree.body)

def assignments(text,base):
 result=dict(base)
 for m in re.finditer(r'([a-zA-Z_][\w]*)\s*=\s*(\{[^}]*\}|[^\s]+)',text):result[m[1].lower()]=constant(m[2],result)
 return result

def statements(text,source):
 out=[];control=False
 for i,raw in enumerate(text.splitlines(),1):
  line=raw.strip()
  if line.lower()=='.control':control=True;continue
  if line.lower()=='.endc':control=False;continue
  if control or not line or line.startswith('*'):continue
  if line.startswith('+'):
   assert out,('orphan continuation',source,i);old=out[-1];out[-1]=(old[0]+' '+line[1:].strip(),old[1],old[2]);continue
  out.append((line,source,i))
 return out

def tokens(line):return re.findall(r'\{[^}]*\}|[^\s]+',line)

@dataclass
class Element:
 name:str;kind:str;nodes:list;args:str;params:dict;source:str;line:int;scope:str;model:dict=field(default_factory=dict);original:str='';aliases:dict=field(default_factory=dict)

def flatten(text,libraries=(),source='<memory>'):
 defs={};globalModels={};top=[];globalParams={'temp':27.};visited=set()
 def read(stmts,isTop):
  active=None;body=[];header=None
  for line,src,ln in stmts:
   low=line.lower();tt=tokens(line)
   if low.startswith(('.include ','.inc ')):
    p=Path(tt[1].strip('"\''));p=p if p.is_absolute()else Path(src).parent/p
    if str(p.resolve())not in visited:visited.add(str(p.resolve()));read(statements(p.read_text(encoding='utf-8'),str(p)),False)
   elif low.startswith('.subckt '):assert active is None;active=tt[1].lower();header=(tt[2:],src,ln);body=[]
   elif low.startswith('.ends'):
    assert active is not None;defs[active]=(header,body);active=None
   elif active is not None:body.append((line,src,ln))
   elif low.startswith('.model '):globalModels[tt[1].lower()]=parseModel(line)
   elif low.startswith('.param '):globalParams.update(assignments(line[7:],globalParams))
   elif isTop and not line.startswith('.')and ln!=1:top.append((line,src,ln))
  assert active is None,'unclosed subckt'
 def parseModel(line):
  t=tokens(line);tail=' '.join(t[2:]);typ=re.match(r'\w+',tail)[0].lower();body=tail[len(typ):].strip(' ()');model=assignments(body,{});model['type']=typ;return model
 for p in libraries:read(statements(Path(p).read_text(encoding='utf-8'),str(p)),False)
 read(statements(text,source),True)
 out=[]
 def emit(body,scope,pins,params,models):
  local=dict(models)
  for line,src,ln in body:
   if line.lower().startswith('.model '):local[tokens(line)[1].lower()]=parseModel(line)
  def node(s):return '0'if s.lower()in ('0','gnd')else pins.get(s.lower(),scope+'.'+s.lower()if scope else s.lower())
  for line,src,ln in body:
   if line.startswith('.'):continue
   t=tokens(line);kind=t[0][0].lower()
   if kind=='x':
    pi=next((i for i,x in enumerate(t)if x.lower().startswith('params:')),len(t));name=t[pi-1].lower();assert name in defs,('unknown subckt',name,src,ln)
    header,subbody=defs[name];ht=header[0];hi=next((i for i,x in enumerate(ht)if x.lower().startswith('params:')),len(ht));formal=ht[:hi];actual=t[1:pi-1];assert len(formal)==len(actual),(name,formal,actual)
    defaults=assignments(' '.join(ht[hi:]).replace('PARAMS:','').replace('params:',''),params);values=assignments(' '.join(t[pi:]).replace('PARAMS:','').replace('params:',''),defaults)
    child=(scope+'.'if scope else '')+t[0].lower();emit(subbody,child,{x.lower():node(y)for x,y in zip(formal,actual)},values,local);continue
   assert kind in 'rcvielghs',('unsupported primitive',kind,line,src,ln)
   n=4 if kind=='s'or (kind in 'eg'and not re.search(r'(?i)\b(value|table)\b',line))else 2
   nodes=[node(x)for x in t[1:1+n]];args=' '.join(t[1+n:]);model=local.get(t[-1].lower(),{})if kind=='s'else {}
   fullname=(kind+'.'+scope+'.'+t[0].lower())if scope else t[0].lower()
   out.append(Element(fullname,kind,nodes,args,dict(params),src,ln,scope,dict(model),line,dict(pins)))
 emit(top,'',{},globalParams,globalModels);return out
