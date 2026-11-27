"""R-04 check: exact readings of three numbers from the historical Construct archive.

M-01  The moduli n whose Fibonacci period divides 24 are exactly the divisors of 144.
      Proof ingredient: A^24 - I = [[F23-1, F24], [F24, F25-1]], and the gcd of its entries is 144.
M-02  Over one period (24 steps) of the law mod 9, 6 terms are multiples of 3 and 18 are not.
M-03  At depth 5 the half-turn phase is 324 = 18^2 (A^324 = -I mod 243); order 648.
Exits 0 when every check holds. Pure Python, under a second.
"""
from math import gcd
import sys

def pisano(n):
    a, b, i = 0, 1, 0
    while True:
        a, b = b, (a + b) % n
        i += 1
        if a == 0 and b == 1 % n:
            return i

def matpow(M, e, m):
    R = [[1, 0], [0, 1]]
    while e:
        if e & 1:
            R = [[(R[0][0]*M[0][0]+R[0][1]*M[1][0]) % m, (R[0][0]*M[0][1]+R[0][1]*M[1][1]) % m],
                 [(R[1][0]*M[0][0]+R[1][1]*M[1][0]) % m, (R[1][0]*M[0][1]+R[1][1]*M[1][1]) % m]]
        M = [[(M[0][0]*M[0][0]+M[0][1]*M[1][0]) % m, (M[0][0]*M[0][1]+M[0][1]*M[1][1]) % m],
             [(M[1][0]*M[0][0]+M[1][1]*M[1][0]) % m, (M[1][0]*M[0][1]+M[1][1]*M[1][1]) % m]]
        e >>= 1
    return R

checks = []
def check(name, ok):
    checks.append(ok)
    print(("PASS " if ok else "FAIL ") + name)

F = [0, 1]
while len(F) < 30:
    F.append(F[-1] + F[-2])
g = gcd(gcd(F[23] - 1, F[24]), F[25] - 1)
check("gcd(F23-1, F24, F25-1) = 144", g == 144)
check("F12 = 144", F[12] == 144)
divs = [d for d in range(2, 145) if 144 % d == 0]
period_divides_24 = [n for n in range(2, 20001) if 24 % pisano(n) == 0]
check("{n <= 20000 : pi(n) | 24} = divisors of 144", period_divides_24 == divs)
check("pi(9) = 24 and pi(144) = 24", pisano(9) == 24 and pisano(144) == 24)

seq = [0, 1]
while len(seq) < 24:
    seq.append((seq[-1] + seq[-2]) % 9)
check("one period mod 9: 6 multiples of 3, 18 others", sum(x % 3 == 0 for x in seq) == 6 and sum(x % 3 != 0 for x in seq) == 18)

A = [[0, 1], [1, 1]]
m = 3 ** 5
check("depth 5: A^324 = -I", matpow(A, 324, m) == [[m - 1, 0], [0, m - 1]])
check("depth 5: A^648 = I, order 648", matpow(A, 648, m) == [[1, 0], [0, 1]] and all(matpow(A, 648 // p, m) != [[1, 0], [0, 1]] for p in (2, 3)))
check("324 = 18^2", 324 == 18 ** 2)

print(f"{sum(checks)} of {len(checks)} checks passed")
sys.exit(0 if all(checks) else 1)
