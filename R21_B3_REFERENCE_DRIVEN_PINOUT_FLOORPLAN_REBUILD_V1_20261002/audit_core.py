import math,json,hashlib
import numpy as np
def rigid_reuse(old,new,tol=.5):
 refs=sorted(set(old)&set(new));a=np.array([old[r][:2] for r in refs]);b=np.array([new[r][:2] for r in refs]);best={'matched':0,'count':len(refs),'fraction':0,'angle':None,'translation':None}
 # Full SO(2) rotation candidates from every labelled distinct pair, plus cardinal angles.
 angles=[0,math.pi/2,math.pi,3*math.pi/2]
 for i in range(len(refs)):
  for k in range(i):
   u=a[i]-a[k];v=b[i]-b[k]
   if np.linalg.norm(u)>1e-9 and np.linalg.norm(v)>1e-9:angles.append(math.atan2(v[1],v[0])-math.atan2(u[1],u[0]))
 for theta in angles:
  rot=np.array([[math.cos(theta),-math.sin(theta)],[math.sin(theta),math.cos(theta)]]);ar=a@rot.T;diff=b-ar
  translations=list(diff)+[diff.mean(axis=0)]
  for t in translations:
   n=int((np.linalg.norm(ar+t-b,axis=1)<=tol+1e-9).sum())
   if n>best['matched']:best={'matched':n,'count':len(refs),'fraction':n/len(refs),'angle':math.degrees(theta),'translation':t.tolist()}
 return best
def identity_digest(g):
 d={r:{k:v[k] for k in ['ref','name','footprintUuid','footprintName','bodyLocalPolygonsMm'] if k in v}|{'pads':sorted([(p['number'],p['net'],p.get('shape'),p.get('nativeLayer')) for p in v['pads']],key=lambda x:x[0])} for r,v in g.items()}
 return hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest()
