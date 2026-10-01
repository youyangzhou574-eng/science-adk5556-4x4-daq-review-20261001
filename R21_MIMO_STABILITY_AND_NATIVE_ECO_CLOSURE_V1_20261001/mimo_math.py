"""Derived admittance return-difference; not an absolute pole certificate."""
import numpy as np
def return_difference(y):
    assert y.ndim==3 and y.shape[1]==y.shape[2] and y.shape[1]%2==0
    n=y.shape[1]//2
    d=y[:,:n,:n]+y[:,n:,n:];a=y[:,:n,n:]+y[:,n:,:n]
    l=np.linalg.solve(d,a);r=l+np.eye(n);g=d+a
    return l,r,d,g
def recover_y(columns,n,inductance=1e9):
    f=columns[0][:,0]
    assert all(np.array_equal(c[:,0],f) for c in columns)
    # Per stimulus:2N source-current vectors then2N actual target-port voltages.
    currents=np.stack([c[:,1:1+4*n:2]+1j*c[:,2:2+4*n:2] for c in columns],axis=2)
    voltages=np.stack([c[:,1+4*n::2]+1j*c[:,2+4*n::2] for c in columns],axis=2)
    y=np.linalg.solve(np.swapaxes(voltages,1,2),np.swapaxes(currents,1,2)).swapaxes(1,2)
    yl=1/(2j*np.pi*f*inductance)
    for i in range(n):
        y[:,i,i]-=yl;y[:,i+n,i+n]-=yl;y[:,i,i+n]+=yl;y[:,i+n,i]+=yl
    return f,y,np.linalg.cond(voltages)
