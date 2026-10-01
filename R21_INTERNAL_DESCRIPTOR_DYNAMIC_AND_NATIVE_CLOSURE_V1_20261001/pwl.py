"""Static quadratic corner tangent; inferred candidate, native-qualified only where tested."""
def tangent(x,m):
 xx,yy=m['x_array'],m['y_array'];assert len(xx)==len(yy)and len(xx)>=2 and all(b>a for a,b in zip(xx,xx[1:]))
 assert m.get('fraction',True)and m.get('limit',False),'Only actual PSA parameter family supported'
 slopes=[(b-a)/(d-c)for a,b,c,d in zip(yy,yy[1:],xx,xx[1:])]
 for j,xc in enumerate(xx):
  width=xx[1]-xx[0]if j==0 else xx[-1]-xx[-2]if j==len(xx)-1 else min(xx[j]-xx[j-1],xx[j+1]-xx[j])
  radius=m.get('input_domain',.01)*width
  if radius>0 and abs(x-xc)<=radius:
   left=slopes[j-1]if j>0 else 0.;right=slopes[j]if j<len(slopes)else 0.;d=x-xc
   return yy[j]+(left+right)*d/2+(right-left)*(d*d/radius+radius)/4,(left+right)/2+(right-left)*d/(2*radius)
 if x<xx[0]:return yy[0],0.
 if x>xx[-1]:return yy[-1],0.
 for j in range(len(slopes)):
  if xx[j]<=x<=xx[j+1]:return yy[j]+slopes[j]*(x-xx[j]),slopes[j]
 raise ValueError('PWL interval not located')
