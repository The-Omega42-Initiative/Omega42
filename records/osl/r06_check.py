"""R-06 check: SME-01 (the world mod 144), M-02 phases, and exact readings of the historical assertions.
Pure Python; a few seconds."""
import sys
from math import gcd, sqrt, isqrt
from collections import Counter
R = []
def ok(name, c):
    R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + name)

def orbits(m):
    seen = set(); sizes = []
    for a in range(m):
        for b in range(m):
            if (a, b) in seen: continue
            x = (a, b); L = 0
            while x not in seen:
                seen.add(x); L += 1; x = (x[1], (x[0] + x[1]) % m)
            sizes.append(L)
    return Counter(sizes)

# SME-01
o16, o9, o144 = orbits(16), orbits(9), orbits(144)
ok('mod 16: 16 orbits, lengths 1, 3, 6x2, 12x4, 24x8', o16 == Counter({1: 1, 3: 1, 6: 2, 12: 4, 24: 8}))
ok('mod 9: 5 orbits, lengths 1, 8, 24x3', o9 == Counter({1: 1, 8: 1, 24: 3}))
pred = Counter()
for m, cm in o16.items():
    for n, cn in o9.items():
        pred[m * n // gcd(m, n)] += cm * cn * gcd(m, n)
ok('mod 144: census equals the CRT product (870 orbits; 861 of length 24)', o144 == pred and sum(o144.values()) == 870 and o144[24] == 861)
ok('mod 144: lengths 1, 3, 6x2, 8, 12x4, 24x861', o144 == Counter({1: 1, 3: 1, 6: 2, 8: 1, 12: 4, 24: 861}))
lens = [L for L, c in o144.items() for _ in range(c)]
mult = {d: sum(1 for L in lens if L % d == 0) for d in (1, 2, 3, 4, 6, 8, 12, 24)}
ok('mod 144: eigenvalue multiplicities by root order 870, 868, 868, 866, 867, 862, 865, 861',
   [mult[d] for d in (1, 2, 3, 4, 6, 8, 12, 24)] == [870, 868, 868, 866, 867, 862, 865, 861])
def comm(c): l = [L for L, k in c.items() for _ in range(k)]; return sum(gcd(x, y) for x in l for y in l)
ok('commutant dimensions: 281 (mod 9), 2,926 (mod 16), 17,916,106 (mod 144)', (comm(o9), comm(o16), comm(o144)) == (281, 2926, 17916106))
x = (2, 5); seen = set()
while x not in seen: seen.add(x); x = (x[1], (x[0] + x[1]) % 144)
ok('the seed (2, 5) has period 24 mod 144', len(seen) == 24)

# M-02, canonical orbit
x = (2, 5); pos = []
for t in range(24):
    if x[0] % 3 == 0: pos.append(t)
    x = (x[1], (x[0] + x[1]) % 9)
ok('canonical orbit mod 9: a-coordinate divisible by 3 exactly at phases 3, 7, 11, 15, 19, 23', pos == [3, 7, 11, 15, 19, 23])

# UH-01 digital root
ok('reduction mod m is unchanged by appending a zero digit exactly for m | 9', [m for m in range(1, 200) if all((10 * n) % m == n % m for n in range(1, 5 * m + 5))] == [1, 3, 9])
ok('in base b the same holds exactly for m | b - 1 (b = 2..16)', all([m for m in range(1, 100) if all((b * n) % m == n % m for n in range(1, 300))] == [d for d in range(1, 100) if (b - 1) % d == 0] for b in range(2, 17)))
# UH-02 phi
best = min(((t + sqrt(t * t - 4 * N)) / 2, t, N) for t in range(0, 60) for N in (1, -1)
           if t * t - 4 * N > 0 and isqrt(t * t - 4 * N) ** 2 != t * t - 4 * N and (t + sqrt(t * t - 4 * N)) / 2 > 1)
ok('the smallest real quadratic unit above 1 is phi (trace 1, norm -1)', best[1:] == (1, -1) and abs(best[0] - (1 + sqrt(5)) / 2) < 1e-12)
# UH-03 702
ok('702 = 27 x 26 = |AGL(1, 27)|', 702 == 27 * 26)
ok('702 is no order or orbit count of the tower, k = 1..12', all(702 not in (8 * 3 ** (k - 1), (3 ** k + 1) // 2) for k in range(1, 13)))
# UH-04 E6
ok('5 divides |W(E6)| = 51,840 and no |GL2(Z/3^k)| = 48 * 81^(k-1), so W(E6) embeds in no depth', 51840 % 5 == 0 and all((48 * 81 ** (k - 1)) % 5 for k in range(1, 30)))
print(f'{sum(R)} of {len(R)} checks passed')
sys.exit(0 if all(R) else 1)
