#!/usr/bin/env python3
"""Exact exponent-congruence certificate of two-level Weyl recursion."""
def verify(k):
    N=3**k; M=N//9; d=N//3
    invN=pow(2,-1,N)
    invM=pow(2,-1,M) if M>1 else 0
    for a in range(M):
        for b in range(M):
            for t in range(M):
                out={}
                for v in range(3):
                    j=3*t+v*d
                    dest=(j+3*b)%N
                    phase=(3*a*(j+3*b)-invN*9*a*b)%N
                    out[dest]=phase
                target=(t+b)%M
                phaseM=(a*(t+b)-invM*a*b)%M if M>1 else 0
                assert len(out)==3
                for v in range(3):
                    dest=3*target+v*d
                    assert out[dest]==(N//M)*phaseM%N,(k,a,b,t,dest)
    print(f'PASS N={N}, M={M}: W_N(3a,3b) J=J W_M(a,b)')

if __name__=='__main__':
    for k in (2,3,4,5):
        verify(k)
