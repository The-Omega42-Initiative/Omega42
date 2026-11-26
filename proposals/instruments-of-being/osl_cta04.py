"""CTA-04 exact interaction and commutation."""
from osl_cta03 import factorize, multiply
def reorder(c,h,k=2):
    q=3**k
    return factorize(multiply(c,h,q),k,"HC")
def compose(left,right,k=2):
    q=3**k
    h,c=left; j,d=right
    j1,c1=reorder(c,j,k)
    return multiply(h,j1,q),multiply(c1,d,q)
def commutes(c,h,k=2):
    q=3**k
    return multiply(c,h,q)==multiply(h,c,q)
def selftest():
    for k in (1,2,3):
        q=3**k; total=comm=0
        for a in range(q):
            for b in range(q):
                if (a*a+a*b-b*b)%3==0: continue
                C=(a,b,b,(a+b)%q)
                for c in range(q):
                    for d in range(q):
                        if d%3==0: continue
                        H=(1,0,c,d)
                        J,D=reorder(C,H,k)
                        assert multiply(J,D,q)==multiply(C,H,q)
                        assert commutes(C,H,k)==(b*c%q==0 and b*(d-1)%q==0)
                        total+=1; comm+=commutes(C,H,k)
        assert total==48*3**(4*k-4)
        assert comm==2*3**(3*k-1)
if __name__=="__main__": selftest()
