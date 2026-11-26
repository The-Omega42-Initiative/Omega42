"""CSG-01 exact spectral multiplicities and antipodal parity."""
def multiplicities(k=2):
    if type(k) is not int or k<1: raise ValueError("invalid depth")
    P=8*3**(k-1)
    return tuple(int(j==0)+sum(3**(m-1) for m in range(1,k+1) if j%3**(k-m)==0) for j in range(P))
def parity_dimensions(k=2):
    m=multiplicities(k)
    return sum(m[::2]),sum(m[1::2])
def selftest():
    for k in range(1,6):
        q=3**k; P=8*3**(k-1); seen=set(); counts=[0]*P
        for a in range(q):
            for b in range(q):
                x=(a,b); length=0
                while x not in seen:
                    seen.add(x); length+=1; x=(x[1],sum(x)%q)
                if length:
                    for j in range(0,P,P//length): counts[j]+=1
        assert tuple(counts)==multiplicities(k)
        assert parity_dimensions(k)==((q*q+1)//2,(q*q-1)//2)
if __name__=="__main__": selftest()
