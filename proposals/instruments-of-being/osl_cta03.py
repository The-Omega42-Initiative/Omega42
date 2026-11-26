"""CTA-03 exact factorization at every power-of-three depth."""
from itertools import product
def multiply(m,n,q):
    a,b,c,d=m; e,f,g,h=n
    return tuple(x%q for x in (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h))
def inverse(m,q):
    a,b,c,d=m; z=pow((a*d-b*c)%q,-1,q)
    return tuple(x*z%q for x in (d,-b,-c,a))
def factorize(m,k=2,order="HC"):
    if type(k) is not int or k<1: raise ValueError("invalid depth")
    q=3**k
    a,b,r,s=m=tuple(x%q for x in m)
    if (a*s-b*r)%3==0: raise ValueError("singular matrix")
    if order=="CH":
        h,c=factorize(inverse(m,q),k,"HC")
        return inverse(c,q),inverse(h,q)
    if order!="HC": raise ValueError("invalid order")
    z=pow((a*a+a*b-b*b)%q,-1,q)
    c=(r*(a+b)-s*b)*z%q
    d=(s*a-r*b)*z%q
    return (1,0,c,d),(a,b,b,(a+b)%q)
def selftest():
    for k in (1,2,3):
        q=3**k; count=0
        for m in product(range(q),repeat=4):
            a,b,r,s=m
            if (a*s-b*r)%3==0: continue
            for order in ("HC","CH"):
                x,y=factorize(m,k,order)
                assert multiply(x,y,q)==m
            count+=1
        assert count==48*3**(4*(k-1))
        print(k,count)
if __name__=="__main__": selftest()
