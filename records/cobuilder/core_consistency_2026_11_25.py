#!/usr/bin/env python3
"""Independent recomputation of arithmetic statements in the Core Specification V335 Rev.450 STABLE (docs/, main b0ed7e3),
made for the Originator's consistency check of 25 November 2026 (Claude). The statements are the same in the Core on main (b0ed7e3)
and on release/2026-11-25 (bcd978b); the MF-194 to MF-204 checks cover the entries added on release/2026-11-25. It complements tools/consistency_check.py, which checks
the documents' cross-references, versions, hashes and wording, by recomputing what the Core states about numbers.
Pure standard library, exhaustive over the finite spaces. Exit status 0 = every check passed.

Notation here follows the Core: A is the law, A(a, b) = (b, a + b) mod 9; P0..P23 is the canonical cycle from (P0, P1) = (2, 5),
written as digits 1..9 (residue 0 shown as 9)."""
import sys
from math import gcd
from collections import Counter

checks = []
def check(ref, ok, detail=''):
    checks.append(bool(ok)); print(('PASS ' if ok else 'FAIL ') + ref + (': ' + detail if detail else ''))

M = 9
def law(x, m=M): return (x[1], (x[0] + x[1]) % m)
def dr(n): return 0 if n == 0 else 1 + (n - 1) % 9
S = [(a, b) for a in range(M) for b in range(M)]

# Fact 1
F = [0, 1]
while len(F) < 60: F.append(F[-1] + F[-2])
per = next(p for p in range(1, 60) if F[p] % 9 == 0 and F[p + 1] % 9 == 1)
s117 = sum((f % 9) or 9 for f in F[:24])   # digits 1..9: residue 0 counted as 9 (residues alone sum to 99)
check('Fact 1: Pisano period pi(9) = 24; one period sums to 117 in digits 1..9; dr(117) = 9', per == 24 and s117 == 117 and dr(117) == 9, 'period %d, sum %d' % (per, s117))
# Fact 2
units = [u for u in range(1, 9) if gcd(u, 9) == 1]
prim = [g for g in units if len({pow(g, k, 9) for k in range(1, 7)}) == 6]
check('Fact 2: (Z/9)x = {1,2,4,5,7,8}; primitive roots exactly {2,5}; 2 x 5 = 1 mod 9', units == [1, 2, 4, 5, 7, 8] and prim == [2, 5] and 10 % 9 == 1)
# Fact 3
orbit2, x = [], 1
for _ in range(6): orbit2.append(x); x = 2 * x % 9
check('Fact 3: doubling 1->2->4->8->7->5->1; the digit set of 1/7 = 0.142857...', orbit2 == [1, 2, 4, 8, 7, 5] and set(str(10**6 // 7)) == set('142857') and set(map(int, '142857')) == set(units))
# Fact 4
check('Fact 4: dr(6n) only 3, 6, 9 in the pattern 6,3,9; dr(5n) covers 1..9 for n = 1..9',
      [dr(6 * n) for n in range(1, 10)] == [6, 3, 9] * 3 and sorted(dr(5 * n) for n in range(1, 10)) == list(range(1, 10)))
# the canonical cycle
P, x = [], (2, 5)
for _ in range(24): P.append(x[0] if x[0] else 9); x = law(x)
check('canonical cycle closes after 24 steps from (2, 5)', x == (2, 5), ' '.join(map(str, P)))
# Fact 5 and the Introduction's wording
check('Fact 5: P(i) + P(i+12) has digital root 9 for all 12 pairs; sum is 9, or 18 where both are 9 (P7, P19)',
      all(dr(P[i] + P[i + 12]) == 9 for i in range(12)) and [i for i in range(24) if P[i] == 9] == [7, 19]
      and all(P[i] + P[i + 12] in (9, 18) for i in range(12)))
check('"Twelve steps on, the cycle is its own negative": A^12 = -I on all 81 states',
      all((lambda y: [y := law(y) for _ in range(12)][-1])(s) == ((-s[0]) % 9, (-s[1]) % 9) for s in S))
# Fact 6
qr = sorted({(t * t) % 9 for t in range(9)})
check('Fact 6: quadratic residues mod 9 = {0,1,4,7}; 5 is not one; x^2 = x + 1 has no root mod 9',
      qr == [0, 1, 4, 7] and 5 not in qr and not any((t * t - t - 1) % 9 == 0 for t in range(9)))
# 0.0.9.9
def mat(k):
    Mx = [[1, 0], [0, 1]]
    for _ in range(k): Mx = [[Mx[0][1], (Mx[0][0] + Mx[0][1]) % 9], [Mx[1][1], (Mx[1][0] + Mx[1][1]) % 9]]
    return Mx
def order(k):
    for n in range(1, 50):
        if mat((k * n) % 24) == [[1, 0], [0, 1]]: return n
check('0.0.9.9: A^2, A^3, A^4, A^6, A^8, A^12 have orders 12, 8, 6, 4, 3, 2', [order(k) for k in (2, 3, 4, 6, 8, 12)] == [12, 8, 6, 4, 3, 2])
check('0.0.9.9: A^6 is a square root of -I (A^12 = -I)', mat(12) == [[8, 0], [0, 8]])
cnt = Counter(P)
check('0.0.9.9: in the canonical cycle 4 and 5 appear five times, every other digit twice',
      cnt[4] == 5 and cnt[5] == 5 and all(cnt[d] == 2 for d in range(1, 10) if d not in (4, 5)), str(dict(sorted(cnt.items()))))
# 1.8 Crown
check('1.8: Crown {P3,P7,P11,P15,P19,P23} = exactly the positions with values in {3,6,9}',
      [i for i in range(24) if P[i] in (3, 6, 9)] == [3, 7, 11, 15, 19, 23])
check('1.8: each low Crown member\'s antipode is the matching high member (P3->P15, P7->P19, P11->P23)',
      all(dr(P[i] + P[i + 12]) == 9 for i in (3, 7, 11)))
# orbit architecture and K1
seen, orbs = set(), []
for s in S:
    if s in seen: continue
    o, y = [], s
    while y not in seen: seen.add(y); o.append(y); y = law(y)
    orbs.append(o)
check('0.5 / R0: 81 = 24 + 24 + 24 + 8 + 1', sorted(map(len, orbs)) == [1, 8, 24, 24, 24])
full = [o for o in orbs if {(v[0] if v[0] else 9) for v in o} == set(range(1, 10))]
check('1.8.3 K1: exactly the three period-24 orbits take all nine values 1..9', len(full) == 3 and all(len(o) == 24 for o in full))
# MATH-38 at k = 2
m2 = 81; seen2, orbs2 = set(), []
for a in range(m2):
    for b in range(m2):
        if (a, b) in seen2: continue
        o, y = [], (a, b)
        while y not in seen2: seen2.add(y); o.append(y); y = law(y, m2)
        orbs2.append(o)
longest = max(map(len, orbs2))
full2 = [o for o in orbs2 if {v[0] % 9 for v in o} == set(range(9))]
check('1.8.3 / MATH-38 at k = 2: longest period mod 81 is 8 x 3^3 = 216, and the complete-spectrum orbits are exactly the longest',
      longest == 216 and {len(o) for o in full2} == {216} and len(full2) == sum(1 for o in orbs2 if len(o) == 216), '%d orbits of 216' % len(full2))
# FP-ArmNorm and Catalan
def seq(s, n):
    x = s
    for _ in range(n): x = law(x)
    return x[0]
normA = lambda a, b: (a * a + a * b - b * b) % 9
normB = lambda a, b: (b * b - a * b - a * a) % 9
lhs = {s: (seq(s, 0) * seq(s, 12) - seq(s, 18) ** 2) % 9 for s in S}
which = [n for n, f in (('a^2+ab-b^2', normA), ('b^2-ab-a^2', normB)) if all(lhs[s] == f(*s) for s in S)]
check('FP-ArmNorm: Anchor x Antipode - Yin^2 = the norm of the state, all 81 states; F(18) = 2584 = 1 mod 9',
      bool(which) and F[18] == 2584 and 2584 % 9 == 1, 'holds with the norm ' + (which[0] if which else 'NEITHER'))
# MF-17 at depth 1
allX = [((p, q), (r, t)) for p in range(9) for q in range(9) for r in range(9) for t in range(9)]
A1 = ((0, 1), (1, 1))
def conj(X, Am):
    AX = [[sum(Am[i][k] * X[k][j] for k in range(2)) % 9 for j in range(2)] for i in range(2)]
    return tuple(tuple(sum(AX[i][k] * Am[j][k] for k in range(2)) % 9 for j in range(2)) for i in range(2))
def act_order():
    Xs = allX
    for n in range(1, 25):
        Mn = mat(n); Mn = (tuple(Mn[0]), tuple(Mn[1]))
        if all(conj(X, Mn) == X for X in Xs): return n
check('MF-17 at depth 1: X -> A X A^T on the 6,561 matrices mod 9 has order 12, half of 24', act_order() == 12)

# ---- The register entries added by the Core upgrade on release/2026-11-25 (bcd978b): MF-194 to MF-204, recomputed independently
def hist(s, phases):
    out, y, t = [], s, 0
    for d in sorted(phases):
        while t < d: y = law(y); t += 1
        out.append(y[0] % 7)
    return tuple(out)
counts, first = [], Counter()
for r in range(1, 7):
    H = Counter(hist(s, range(r)) for s in S); counts.append(len(H))
for s in S:
    for r in range(1, 7):
        H = Counter(hist(t2, range(r)) for t2 in S)
        if H[hist(s, range(r))] == 1: first[r] += 1; break
def order_mod(m):
    x, n = law((1, 0), m), 1
    Mx = ((0, 1), (1, 1))
    st = [(a, b) for a in range(m) for b in range(m)]
    for n in range(1, 200):
        if all((lambda y: [y := law(y, m) for _ in range(n)][-1])(v) == v for v in st): return n
def census(m):
    seen, L = set(), Counter()
    for a in range(m):
        for b in range(m):
            if (a, b) in seen: continue
            n, y = 0, (a, b)
            while y not in seen: seen.add(y); y = law(y, m); n += 1
            L[n] += 1
    return L
check('MF-194: a mod 7 gives 7, 49, 73, 77, 80, 81 histories after 1..6 readings; first resolution at rounds 2..6 for 25, 44, 4, 6, 2 states',
      counts == [7, 49, 73, 77, 80, 81] and [first[r] for r in range(2, 7)] == [25, 44, 4, 6, 2] and first[1] == 0, '%s; %s' % (counts, dict(first)))
c7 = census(7)
check('MF-194: modulo 7 the law has order 16 and the 49 pairs split 1 + 16 + 16 + 16', order_mod(7) == 16 and c7 == Counter({1: 1, 16: 3}), str(dict(c7)))
m = {j: sum(1 for o in orbs if j % (24 // len(o)) == 0) for j in range(24)}
check('MF-195: multiplicities 3 + [3|j] + [j=0]; sum m^2 = 281; sum (m-1)^2 = 143',
      all(m[j] == 3 + (j % 3 == 0) + (j == 0) for j in range(24)) and sum(v * v for v in m.values()) == 281 and sum((v - 1) ** 2 for v in m.values()) == 143)
x0 = orbs[[len(o) for o in orbs].index(24)][0]
def Tg(st): x, mm = st; return (law(x), (mm + (1 if x == x0 else 0)) % 9)
st, n = Tg((x0, 0)), 1
while st != (x0, 0): st = Tg(st); n += 1
check('MF-197: a unit sum on one 24-orbit gives a single memory cycle of length 216', n == 216)
def rounds2(d):
    for r in range(1, 40):
        H = {tuple((hist(s, [t])[0], hist(s, [t + d])[0]) for t in range(r)) for s in S}
        if len(H) == 81: return r
check('MF-199: two observers at phases 0 and d need 5,4,3,2,2,2,2,2,3,4,5,6,5,4,3,2,2,2,2,2,3,4,5 rounds for d = 1..23',
      [rounds2(d) for d in range(1, 24)] == [5, 4, 3, 2, 2, 2, 2, 2, 3, 4, 5, 6, 5, 4, 3, 2, 2, 2, 2, 2, 3, 4, 5])
roots = [t for t in range(11) if (t * t - t - 1) % 11 == 0]
ordm = lambda g, p: next(k for k in range(1, p) if pow(g, k, p) == 1)
c11 = census(11)
check('MF-203: mod 11, x^2 = x + 1 has roots 4 and 8, of orders 5 and 10; the 121 pairs split 1 + 2 x 5 + 11 x 10',
      roots == [4, 8] and ordm(4, 11) == 5 and ordm(8, 11) == 10 and c11 == Counter({1: 1, 5: 2, 10: 11}), str(dict(c11)))
negfix = [s for s in S if ((-s[0]) % 9, (-s[1]) % 9) == s]
Qv = lambda a, b: (a * a + a * b - b * b) % 9
q2 = sorted((len(o), sorted({Qv(*v) ** 2 % 9 for v in o})) for o in orbs)
check('MF-204: U^12 eigenspaces 41 and 40 (only (0,0) is its own negative); Q^2 is 0 on the 8-cycle and the still point and 1, 4, 7 on the 24-orbits',
      negfix == [(0, 0)] and 1 + (81 - 1) // 2 == 41 and q2[0][1] == [0] and q2[1][1] == [0] and sorted(q[1][0] for q in q2[2:]) == [1, 4, 7], str(q2))

print('RESULT: %d checks, %d failed' % (len(checks), checks.count(False)))
sys.exit(0 if all(checks) else 1)
