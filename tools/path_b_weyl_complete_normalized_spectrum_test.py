import numpy as np
def occupied(k):
    if k==1:return {0,1,3}
    if k==2:return {0,1,2,4,5,7,8,10,11}
    return {j for j in range(4*3**(k-1)) if j%3} | {9*j for j in occupied(k-2)}
for k in range(1,7):
    n=3**k; L=4*n//3
    p=np.arange(n); q=p[:,None]
    K=np.exp(2j*np.pi*((pow(2,-1,n)*(q*q-2*q*p+2*p*p))%n)/n)/np.sqrt(n)
    V=K/np.trace(K)
    a=np.linalg.eigvals(V)
    j=np.rint(np.angle(a)*L/(2*np.pi)).astype(int)%L
    assert max(abs(a-np.exp(2j*np.pi*j/L)))<1e-8
    assert len(set(j))==n
    assert set(j)==occupied(k)
    print('PASS',k,n)
