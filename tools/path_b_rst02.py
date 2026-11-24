import numpy as np
H=np.array([[1,1,1],[1,-1,0],[1,1,-2]],float)/np.sqrt([3,2,6])[:,None]
def analysis(x):
    x=np.asarray(x,dtype=complex); n=x.size
    if n in (1,3): return x.copy()
    if n<9 or n%9: raise ValueError('length must be a power of three')
    y=H@x.reshape(3,n//3)
    mask=np.arange(n//3)%3==0
    return np.concatenate((y[1:].ravel(),y[0,~mask],analysis(y[0,mask])))
def synthesis(c):
    c=np.asarray(c,dtype=complex); n=c.size
    if n in (1,3): return c.copy()
    if n<9 or n%9: raise ValueError('length must be a power of three')
    d=n//3; mask=np.arange(d)%3==0
    y=np.empty((3,d),complex); y[1:]=c[:2*d].reshape(2,d)
    y[0,~mask]=c[2*d:n-n//9]; y[0,mask]=synthesis(c[n-n//9:])
    return (H.T@y).ravel()
if __name__=='__main__':
    rng=np.random.default_rng(42)
    for k in range(1,11):
        n=3**k; x=rng.normal(size=n)+1j*rng.normal(size=n); x/=np.linalg.norm(x)
        c=analysis(x); z=synthesis(c)
        err=np.linalg.norm(z-x); energy=abs(np.vdot(c,c)-1)
        assert len(c)==n and err<1e-12 and energy<1e-12
        print(n, f'{err:.3e}',f'{energy:.3e}')
