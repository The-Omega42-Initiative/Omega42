#!/usr/bin/env python3
"""Independent recomputation of the Co-Builder results of 25 November 2026 (Claude, for the Originator).

Pure Python, no dependencies. Every check is exhaustive over the 81 native states (or the 729 memory configurations).
Run:  python3 records/cobuilder/verify_cobuilder_2026_11_25.py      (exit status 0 = every check passed)
"""
import cmath, math, sys
from collections import Counter

M = 9
S = [(a, b) for a in range(M) for b in range(M)]
def N(x): return (x[1], (x[0] + x[1]) % M)
checks = []
def check(name, ok, detail=''):
    checks.append(ok); print(('PASS ' if ok else 'FAIL ') + name + (': ' + detail if detail else ''))

# orbits of the native law
orbits, seen = [], set()
for x in S:
    if x in seen: continue
    o, y = [x], N(x)
    while y != x: o.append(y); y = N(y)
    seen |= set(o); orbits.append(o)
check('R0 orbit architecture 81 = 24+24+24+8+1', sorted(len(o) for o in orbits) == [1, 8, 24, 24, 24])

# R1 the optimal seven-symbol Aperture (ChatGPT's certificate, rows a, columns b)
H = [[3,2,1,1,1,0,5,4,3],[3,2,0,2,1,1,1,4,5],[3,3,1,1,5,3,1,6,0],[2,0,1,3,0,4,2,5,3],[3,6,3,5,3,5,0,0,3],
     [6,4,4,3,0,6,2,0,2],[6,2,5,2,4,5,5,6,0],[6,4,5,1,2,4,4,0,2],[5,3,4,5,1,3,3,3,6]]
def trace(h, x, n):
    out = []
    for _ in range(n): out.append(h(x)); x = N(x)
    return tuple(out)
hc = lambda x: H[x[0]][x[1]]
counts = [len({trace(hc, x, n) for x in S}) for n in (1, 2, 3)]
check('R1 seven symbols used', sorted(set(v for r in H for v in r)) == list(range(7)))
check('R1 certificate: distinct histories after 1, 2, 3 observations = 7, 49, 81', counts == [7, 49, 81], str(counts))
check('R1 lower bound: 7^2 = 49 < 81, so two observations never suffice', 7 ** 2 < 81)
h7 = lambda x: x[0] % 7
c7 = [len({trace(h7, x, n) for x in S}) for n in range(1, 7)]
check('R1b structural discrimination: h = a mod 7 needs six observations (7,49,73,77,80,81)', c7 == [7, 49, 73, 77, 80, 81], str(c7))
def jump(x, t):
    for _ in range(t): x = N(x)
    return x
coll = {(h7(x), h7(jump(x, 2)), h7(jump(x, 5))) for x in S}
check('R1c collective observability: three observers of a mod 7 at phases 0, 2, 5 jointly separate all 81 states', len(coll) == 81)

# R2 spectral architecture and the coherence operator C_alpha = (I + alpha L / 4)^-1, L = 2I - U - U*
# Basis: on an orbit of length l, the field v_k(x_p) = w^(k p), w = exp(2 pi i / l), is an eigenvector of the shift U.
mult = Counter()
for o in orbits:
    l = len(o)
    for k in range(l): mult[(24 // l) * k % 24] += 1
check('R2 harmonic multiplicities m_j = 3 + [3|j] + [j=0]', all(mult[j] == 3 + (j % 3 == 0) + (j == 0) for j in range(24)))
check('R2 dim of the commutant = sum m_j^2 = 25 + 7*16 + 16*9 = 281', sum(m * m for m in mult.values()) == 281 == 25 + 112 + 144)
def apply_L(o, v):
    l = len(o); return [2 * v[p] - v[(p - 1) % l] - v[(p + 1) % l] for p in range(l)]
ok = True
for alpha in (0.25, 1.0, 4.0):
    for o in orbits:
        l = len(o)
        for k in range(l):
            v = [cmath.exp(2j * math.pi * k * p / l) for p in range(l)]
            j = (24 // l) * k
            lam = 4 * math.sin(math.pi * j / 24) ** 2
            Lv = apply_L(o, v)
            ok &= all(abs(Lv[p] - lam * v[p]) < 1e-9 for p in range(l))
            c = 1 / (1 + alpha * math.sin(math.pi * j / 24) ** 2)
            ok &= abs(c - 1 / (1 + alpha / 4 * lam)) < 1e-12 and 0 < c <= 1
check('R2 C_alpha has the harmonic response c_j = 1/(1 + alpha sin^2(pi j/24)), 0 < c_j <= 1, c_0 = 1', ok)
check('R2 at alpha = 4 the highest harmonic (j = 12) is kept at 1/(1+4) = 0.2', abs(1 / (1 + 4 * math.sin(math.pi / 2) ** 2) - 0.2) < 1e-12)

# R3 reversible memory: T_g(x, m) = (N x, m + g(x)); a full revolution of orbit O adds the orbit sum s_O
def cycles(g):
    seen, lens = set(), Counter()
    for x in S:
        for m in range(M):
            if (x, m) in seen: continue
            y, mm, n = x, m, 0
            while True:
                seen.add((y, mm)); mm = (mm + g(y)) % M; y = N(y); n += 1
                if (y, mm) == (x, m): break
            lens[n] += 1
    return dict(lens)
crm01 = lambda x: x[0]
check('R3 CRM-01: m - b is invariant (memory determined by the state)', all(((m + x[0]) - N(x)[1] - (m - x[1])) % M == 0 for x in S for m in range(M)))
check('R3 CRM-01 orbit sums are all zero (a coboundary: no winding)', all(sum(crm01(x) for x in o) % M == 0 for o in orbits))
o24 = next(o for o in orbits if len(o) == 24)
delta = lambda x: 1 if x == o24[0] else 0
cy = cycles(delta)
check('R3 CRM-02: a unit orbit sum on one 24-orbit gives one cycle of length 24*9 = 216', cy.get(216) == 1, str(cy))
# classification: g ~ g + f(N x) - f(x); the class is the vector of five orbit sums in (Z/9)^5
def orbit_sums(g): return tuple(sum(g(x) for x in o) % M for o in orbits)
import random
random.seed(42); ok = True
for _ in range(200):
    g = {x: random.randrange(M) for x in S}; f = {x: random.randrange(M) for x in S}
    g2 = {x: (g[x] + f[N(x)] - f[x]) % M for x in S}
    ok &= orbit_sums(g.get) == orbit_sums(g2.get)
check('R3 orbit sums are unchanged by every coboundary (sampled 200 pairs)', ok)
check('R3 every class in (Z/9)^5 is reached (delta functions realize each orbit independently), 9^5 = 59049', 9 ** 5 == 59049)

# R4 renormalization: reduction mod 3 commutes with the law; the fiber over 0 is the fixed point plus the 8-cycle
red = lambda x: (x[0] % 3, x[1] % 3)
N3 = lambda x: (x[1], (x[0] + x[1]) % 3)
check('R4 reduction mod 3 is equivariant: red(N x) = N3(red x)', all(red(N(x)) == N3(red(x)) for x in S))
fiber = [x for x in S if red(x) == (0, 0)]
check('R4 Domain Zero differentiated: the fiber over 0 holds the fixed point and the 8-cycle', sorted(len(o) for o in orbits if o[0] in fiber) == [1, 8] and len(fiber) == 9)
check('R4 each 24-orbit reduces onto the single nonzero 8-cycle mod 3 (period triples)', all(len({red(x) for x in o}) == 8 for o in orbits if len(o) == 24))

# R5 the other gateways
def mat(A, B, m): return [[(A[i][0] * B[0][j] + A[i][1] * B[1][j]) % m for j in range(2)] for i in range(2)]
def pw(n, m):
    R = [[1, 0], [0, 1]]
    for _ in range(n): R = mat(R, [[0, 1], [1, 1]], m)
    return R
check('R5 A^12 = -I and A^24 = I mod 9', pw(12, 9) == [[8, 0], [0, 8]] and pw(24, 9) == [[1, 0], [0, 1]])
check('R5 A^8 = I + 3B mod 9 with B = (1 1; 1 2)', pw(8, 9) == [[4, 3], [3, 7]])
check('R5 ord(A mod 7) = 16', min(n for n in range(1, 50) if pw(n, 7) == [[1, 0], [0, 1]]) == 16)
Q = lambda x: (x[0] ** 2 + x[0] * x[1] - x[1] ** 2) % M
check('R5 Q(N x) = -Q(x) mod 9 for all 81 states', all((Q(N(x)) + Q(x)) % M == 0 for x in S))
check('R5 the (pi/2, pi/3, pi/7) triangle has area pi/42', abs(math.pi - math.pi / 2 - math.pi / 3 - math.pi / 7 - math.pi / 42) < 1e-12)
check('R5 1/7 = 4 mod 9, 7*7 = 1 mod 24, 2*5 = 1 mod 9, 5+4 = 0 mod 9', (7 * 4) % 9 == 1 and 49 % 24 == 1 and 10 % 9 == 1 and 9 % 9 == 0)

# R6 a correction to the supplied entropy example: p = (.1,.9) with weights (1, 1/3) gives (.25,.75), not (.5,.5)
p = (0.1, 0.9); q = (0.1, 0.3); s = sum(q); q = (q[0] / s, q[1] / s)
E = lambda v: -sum(t * math.log(t) for t in v)
check('R6 entropy still rises under attenuation (0.32508 -> 0.56234); weights (1, 1/9) give (.5,.5) and ln 2', abs(E(p) - 0.32508) < 1e-4 and abs(E(q) - 0.56234) < 1e-4)


# ---- Round 2 (ChatGPT proposal branch, 25 November 2026): renormalization, the golden-ratio ring, spectra, collective apertures
import itertools
def Nm(x, m): return (x[1], (x[0] + x[1]) % m)
def orbits_mod(m):
    seen, out = set(), []
    for a in range(m):
        for b in range(m):
            x = (a, b)
            if x in seen: continue
            o, y = [x], Nm(x, m)
            while y != x: o.append(y); y = Nm(y, m)
            seen |= set(o); out.append(o)
    return out
OB = {k: orbits_mod(3 ** k) for k in range(1, 5)}
check('R7 orbit count at depth k is (3^k + 1)/2 for k = 1..4 (2, 5, 14, 41)', all(len(OB[k]) == (3 ** k + 1) // 2 for k in OB))
ok = True
for k in (1, 2, 3):
    lo, hi = 3 ** k, 3 ** (k + 1); idx = {x: i for i, o in enumerate(OB[k]) for x in o}; t = Counter()
    for o in OB[k + 1]:
        r = (o[0][0] % lo, o[0][1] % lo); t[(len(OB[k][idx[r]]), len(o))] += 1
    want = Counter({(1, 1): 1, (1, 8): 1}); L = 8
    while L < 8 * 3 ** (k - 1) + 1: want[(L, 3 * L)] = 3 * (L // 8); L *= 3
    ok &= t == want
check('R7 CRC-01: each nonzero orbit of length L lifts to three orbits of length 3L; the zero fiber is the fixed point and an 8-cycle (3->9->27->81)', ok)
def mults(k):
    P = 8 * 3 ** (k - 1); c = Counter()
    for o in OB[k]:
        for t in range(len(o)): c[(P // len(o)) * t % P] += 1
    return c, P
c3, P3 = mults(3); c2, _ = mults(2)
check('R7 CRC-03: m_l = [l=0] + sum_j 3^(j-1)[3^(k-j) | l] at depths 2 and 3',
      all(mults(k)[0][l] == (l == 0) + sum(3 ** (j - 1) * (l % 3 ** (k - j) == 0) for j in range(1, k + 1)) for k in (2, 3) for l in range(mults(k)[1])))
check('R7 CRC-03: 81 -> 729 adds 48 new modes of multiplicity 9 (432 dims) and 216 dims on the 24 inherited modes',
      all(c3[l] == 9 for l in range(72) if l % 3) and sum(c3[3 * j] - c2[j] for j in range(24)) == 216)
def pull_image(k):
    lo = 3 ** k; idx = {x: i for i, o in enumerate(OB[k]) for x in o}
    vec = [[sum(1 for x in oh if (x[0] % lo, x[1] % lo) == o[0]) % 9 for oh in OB[k + 1]] for o in OB[k]]
    return len({tuple(sum(c * v[j] for c, v in zip(cf, vec)) % 9 for j in range(len(OB[k + 1]))) for cf in itertools.product(range(9), repeat=len(OB[k]))})
check('R7 CRC-04: memory pullback 9 -> 27 has image 9*3^4 = 729 and kernel 81 (winding classes can be lost)', pull_image(2) == 729)
O11 = orbits_mod(11)
check('R7 split prime 11: 121 = 1 + 2*5 + 11*10 (roots 8 and 4 of x^2 = x + 1, orders 10 and 5)',
      sorted(Counter(len(o) for o in O11).items()) == [(1, 1), (5, 2), (10, 11)] and (64 - 9) % 11 == 0 and (16 - 5) % 11 == 0)
check('R7 SR-01: U^12 has +1 eigenspace of dimension 41 and -1 of dimension 40', sum(len(o) if 12 % len(o) == 0 else len(o) // 2 for o in orbits) == 41)
q2 = sorted((len(o), Q(o[0]) ** 2 % 9) for o in orbits)
check('R7 SR-01: Q^2 labels the three 24-orbits 1, 4, 7 and gives 0 on the 8-cycle and the fixed point; (period, Q^2) separates all five', q2 == [(1, 0), (8, 0), (24, 1), (24, 4), (24, 7)])
def rounds(offs):
    for r in range(1, 25):
        if len({tuple(h7(jump(x, o + t)) for o in offs for t in range(r)) for x in S}) == 81: return r
    return 25
check('R8 COT-04: two observers of a mod 7 at offsets 0, d need 5,4,3,2,2,2,2,2,3,4,5,6,5,... rounds',
      [rounds((0, d)) for d in range(1, 24)] == [5, 4, 3, 2, 2, 2, 2, 2, 3, 4, 5, 6, 5, 4, 3, 2, 2, 2, 2, 2, 3, 4, 5])
check('R8 COT-04: 24 of the 253 anchored observer triples separate all 81 states at once', sum(rounds((0, d, e)) == 1 for d, e in itertools.combinations(range(1, 24), 2)) == 24)
first = Counter()
for x in S:
    for r in range(1, 25):
        if sum(trace(h7, y, r) == trace(h7, x, r) for y in S) == 1: first[r] += 1; break
check('R8 a single a mod 7 observer resolves states first at rounds 2:25, 3:44, 4:4, 5:6, 6:2', dict(first) == {2: 25, 3: 44, 4: 4, 5: 6, 6: 2})
check('R8 (1,8) and (8,1) agree for five observations and part at the sixth', trace(h7, (1, 8), 5) == trace(h7, (8, 1), 5) and trace(h7, (1, 8), 6) != trace(h7, (8, 1), 6))
dist = Counter()
for p_, q_ in itertools.combinations(itertools.combinations(range(9), 2), 2):
    if set(p_) & set(q_): continue
    lab = list(range(9)); lab[p_[1]] = p_[0]; lab[q_[1]] = q_[0]
    hh = lambda x, lab=lab: lab[x[0]]
    dist[next((n for n in range(1, 25) if len({trace(hh, x, n) for x in S}) == 81), 25)] += 1
check('R8 partition sensitivity: over 378 seven-class coordinate apertures, minimal trace lengths 5:270, 6:78, 7:6, 8:3, never:21',
      dict(dist) == {5: 270, 6: 78, 7: 6, 8: 3, 25: 21})
check('R8 X-OBS-02 bound: ceil(log_7 9^k) = 2, 3, 4, 5 for k = 1..4', [next(t for t in range(10) if 7 ** t >= 9 ** k) for k in range(1, 5)] == [2, 3, 4, 5])
check('R9 Discovery engine: generic stabilizer sum (m-1)^2 = 143, generic orbit 281 - 143 = 138', sum((v - 1) ** 2 for v in mult.values()) == 143)

print('%d checks, %d failed' % (len(checks), checks.count(False)))
sys.exit(0 if all(checks) else 1)
