"""Independent recomputation by Claude of ChatGPT's 26 November batch (CIC-04/05, CIG-01, OCC-01..04, CLC-01, CTA-01..04, CPG-01/02,
CSG-01, CRC-01, CRN-01), written without importing ChatGPT's libraries. NumPy for CRC-01/CRN-01.
Run: python3 records/cobuilder/cg_batch_2026_11_26_check.py"""
import itertools, math
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import numpy as np
R = []
def ok(n, c): R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n)
X = [(a, b) for a in range(9) for b in range(9)]
def T(x, m=9): return (x[1], (x[0] + x[1]) % m)
def Tn(x, n, m=9):
    for _ in range(n): x = T(x, m)
    return x
H = {x: [Tn(x, t)[0] % 7 for t in range(24)] for x in X}
def sigs(P): return Counter(tuple(H[x][t] for t in P) for x in X)
# CIC-04: consecutive readings
c = [sigs(range(k)) for k in range(1, 7)]
ok('CIC-04 consecutive k=1..6: signatures 7,49,73,77,80,81; largest fibres 18,4,3,2,2,1',
   [len(x) for x in c] == [7, 49, 73, 77, 80, 81] and [max(x.values()) for x in c] == [18, 4, 3, 2, 2, 1])
# CIC-05: arbitrary phase sets
best = {k: max(len(sigs(P)) for P in itertools.combinations(range(24), k)) for k in (1, 2)}
good3 = [P for P in itertools.combinations(range(24), 3) if len(sigs(P)) == 81]
gaps = Counter()
for P in good3:
    a, b, cc = P; g = (b - a, cc - b, 24 - cc + a)
    gaps[min(g[i:] + g[:i] for i in range(3))] += 1
ok('CIC-05 best singles 7, pairs 49; 192 successful triples; (0,2,5) first; 8 translation classes of 24',
   best == {1: 7, 2: 49} and len(good3) == 192 and good3[0] == (0, 2, 5) and len(gaps) == 8 and set(gaps.values()) == {24})
# CIG-01: collision sets
pairs = list(itertools.combinations(X, 2))
B = [frozenset(i for i, (x, y) in enumerate(pairs) if H[x][t] == H[y][t]) for t in range(24)]
inter = {t: len(B[0] & B[t]) for t in range(1, 24)}
ok('CIG-01 3240 pairs; |B0|=486; |B0 & Bt| = 44 (t not = 0 mod 4), 90 (4,20), 99 (8,16), 405 (12)',
   len(pairs) == 3240 and len(B[0]) == 486 and all(inter[t] == {4: 90, 20: 90, 8: 99, 16: 99, 12: 405}.get(t, 44) for t in inter))
# OCC-01: greedy collision minimisation, lowest phase on ties
cur, chosen, res = frozenset(range(3240)), [], [3240]
while cur:
    t = min(range(24), key=lambda t: (len(cur & B[t]), t)); chosen.append(t); cur = cur & B[t]; res.append(len(cur))
ok('OCC-01 greedy picks 0,1,4,5 with residuals 3240,486,44,1,0 (the global optimum is 3)', chosen == [0, 1, 4, 5] and res == [3240, 486, 44, 1, 0])
# OCC-02: Bellman optimal adaptive cost with free phase choice, uniform prior
def solve(phases):
    @lru_cache(None)
    def cost(S):
        if len(S) <= 1: return 0
        best = None
        for t in phases:
            parts = {}
            for x in S: parts.setdefault(H[x][t], []).append(x)
            if len(parts) == 1: continue
            v = sum(len(p) + cost(tuple(p)) for p in parts.values())
            best = v if best is None or v < best else best
        return best if best is not None else float('inf')
    return cost(tuple(X))
tot = solve(tuple(range(24)))
ok('OCC-02 optimal adaptive total cost 218 over 81 states (mean 218/81)', tot == 218 and Fraction(tot, 81) == Fraction(218, 81))
# OCC-03: phase sets restricted to multiples of d
cnt = {d: len(sigs(range(0, 24, d))) for d in (1, 2, 3, 4, 6, 8, 12)}
ok('OCC-03 signatures for multiples of d=1,2,3,4,6,8,12: 81,81,81,26,64,25,8; cost 218 for d=1,2,3',
   [cnt[d] for d in (1, 2, 3, 4, 6, 8, 12)] == [81, 81, 81, 26, 64, 25, 8] and all(solve(tuple(range(0, 24, d))) == 218 for d in (2, 3)))
# OCC-04: minimal repair
rep = {}
for d in (4, 6, 8, 12, 24):
    base = tuple(range(0, 24, d)); others = [t for t in range(24) if t not in base]
    one = [t for t in others if len(sigs(base + (t,))) == 81]
    two = [p for p in itertools.combinations(others, 2) if len(sigs(base + p)) == 81]
    rep[d] = (len(sigs(base)), len(one), len(two), two[0] if two else None)
ok('OCC-04 spacing 4,6,8,12,24: initial 26,64,25,8,7; no single repair; 108,132,108,24,24 minimal pairs; first (1,5),(1,3),(1,5),(2,5),(2,5)',
   [rep[d][0] for d in (4, 6, 8, 12, 24)] == [26, 64, 25, 8, 7] and all(rep[d][1] == 0 for d in rep)
   and [rep[d][2] for d in (4, 6, 8, 12, 24)] == [108, 132, 108, 24, 24] and [rep[d][3] for d in (4, 6, 8, 12, 24)] == [(1, 5), (1, 3), (1, 5), (2, 5), (2, 5)])
# CLC-01: translation classes of 3-subsets of Z/24
classes = {min(tuple(sorted((t + s) % 24 for t in P)) for s in range(24)) for P in itertools.combinations(range(24), 3)}
ok('CLC-01 85 translation classes of triples (Burnside (2024+16)/24); 8 successful', len(classes) == 85 and (2024 + 16) // 24 == 85
   and sum(1 for P in classes if len(sigs(P)) == 81) == 8)
# CTA-01: reflection t -> -t
prof = lambda P: sorted(sigs(P).values())
diff = sum(1 for P in itertools.combinations(range(24), 3) if prof(P) != prof(tuple(sorted((-t) % 24 for t in P))))
same_inj = all((len(sigs(P)) == 81) == (len(sigs(tuple(sorted((-t) % 24 for t in P)))) == 81) for P in itertools.combinations(range(24), 3))
ok('CTA-01 reflection keeps injectivity of every triple; 480 change fibre profile; (0,1,8): 80, (0,16,23): 79',
   same_inj and diff == 480 and len(sigs((0, 1, 8))) == 80 and len(sigs((0, 16, 23))) == 79)
h = lambda x: x[0] % 7
ok('CTA-01 among scalar units only 1 keeps the partition of a mod 7',
   [u for u in (1, 2, 4, 5, 7, 8) if all((h(x) == h(y)) == (h(((u * x[0]) % 9, 0)) == h(((u * y[0]) % 9, 0))) for x in X for y in X)] == [1])
# CTA-02: GL(2, Z/9), centralizer of A, linear stabilizer of the aperture partition
def mul(M, N, m): return ((M[0]*N[0] + M[1]*N[2]) % m, (M[0]*N[1] + M[1]*N[3]) % m, (M[2]*N[0] + M[3]*N[2]) % m, (M[2]*N[1] + M[3]*N[3]) % m)
def GL(m): return [M for M in itertools.product(range(m), repeat=4) if math.gcd((M[0]*M[3] - M[1]*M[2]) % m, m) == 1]
G9 = GL(9); Am = (0, 1, 1, 1)
cent = [M for M in G9 if mul(M, Am, 9) == mul(Am, M, 9)]
act = lambda M, x: ((M[0]*x[0] + M[1]*x[1]) % 9, (M[2]*x[0] + M[3]*x[1]) % 9)
stab = [M for M in G9 if all(h(act(M, x)) == h(x) for x in X)]
ok('CTA-02 |GL(2,Z/9)| = 3888, centralizer 72, aperture stabilizer (h o M = h) 54, intersection identity',
   len(G9) == 3888 and len(cent) == 72 and len(stab) == 54 and [M for M in cent if M in set(stab)] == [(1, 0, 0, 1)])
# CTA-03 / CTA-04: unique factorization GL = H C and commuting pairs
for k in (1, 2):
    m = 3**k; Gk = GL(m); units = [d for d in range(m) if math.gcd(d, m) == 1]
    Hs = [(1, 0, c, d) for c in range(m) for d in units]
    Cs = [(a, b, b, (a + b) % m) for a in range(m) for b in range(m) if math.gcd((a*a + a*b - b*b) % m, m) == 1]
    prods = Counter(mul(Hh, Cc, m) for Hh in Hs for Cc in Cs)
    comm = sum(1 for Hh in Hs for Cc in Cs if mul(Hh, Cc, m) == mul(Cc, Hh, m))
    ok('CTA-03/04 k=%d: |H||C| = |GL| = %d, every element exactly once as HC; %d commuting pairs = 2*3^(3k-1)' % (k, len(Gk), comm),
       len(Hs) * len(Cs) == len(Gk) and len(prods) == len(Gk) and set(prods.values()) == {1} and comm == 2 * 3**(3*k - 1))
# CPG-01 / CPG-02: projective directions and stratified layers
for k in (1, 2, 3, 4):
    m = 3**k; prim = [(a, b) for a in range(m) for b in range(m) if a % 3 or b % 3]
    units = [u for u in range(m) if u % 3]
    cls = {min(((u*a) % m, (u*b) % m) for u in units) for a, b in prim}
    x0 = min(((u*1) % m, 0) for u in units); x, n = T((1, 0), m), 1
    rep = lambda v: min(((u*v[0]) % m, (u*v[1]) % m) for u in units)
    while rep(x) != rep((1, 0)): x = T(x, m); n += 1
    ok('CPG-01 k=%d: %d directions, one A-cycle of length 4*3^(k-1)' % (k, len(cls)), len(cls) == 4 * 3**(k - 1) == n)
    L = 4 * 3**(k - 1)
    ok('CPG-02 k=%d: A^L = -I mod 3^k for L = 4*3^(k-1); layers 8*3^(2m-2) sum to 9^k - 1' % k,
       all(Tn(v, L, m) == ((-v[0]) % m, (-v[1]) % m) for v in prim[:50]) and sum(8 * 3**(2*j - 2) for j in range(1, k + 1)) == 9**k - 1)
# CSG-01: multiplicities and parity dimensions
for k in (1, 2, 3):
    m = 3**k; P = 8 * 3**(k - 1); seen, lens = set(), []
    for v in itertools.product(range(m), repeat=2):
        if v in seen: continue
        o, x = 0, v
        while x not in seen: seen.add(x); x = T(x, m); o += 1
        lens.append(o)
    mult = [sum(1 for l in lens if (j * l) % P == 0) for j in range(P)]
    form = [(j == 0) + sum(3**(q - 1) * (j % 3**(k - q) == 0) for q in range(1, k + 1)) for j in range(P)]
    sym = len({min(v, ((-v[0]) % m, (-v[1]) % m)) for v in itertools.product(range(m), repeat=2)})
    ok('CSG-01 k=%d: multiplicities M_j match; antipodal parity dimensions (9^k+1)/2, (9^k-1)/2' % k, mult == form and sym == (9**k + 1) // 2)
# CRC-01 / CRN-01 on W2
orb, seen = [], set()
for v in X:
    if v in seen: continue
    o, x = [], v
    while x not in seen: seen.add(x); o.append(x); x = T(x)
    orb.append(o)
idx = {x: i for i, x in enumerate(X)}
def E(j):   # spectral projector onto harmonic j of 24
    Pm = np.zeros((81, 81), complex)
    for o in orb:
        L = len(o)
        if (j * L) % 24: continue
        e = np.array([np.exp(2j * np.pi * j * s / 24) for s in range(L)]) / np.sqrt(L)
        vec = np.zeros(81, complex)
        for s, x in enumerate(o): vec[idx[x]] = e[s]
        Pm += np.outer(vec, vec.conj())
    return Pm
EJ = [E(j) for j in range(24)]
ok('CSG-01 projectors are orthogonal, sum to I, rank M_j', np.allclose(sum(EJ), np.eye(81)) and all(np.allclose(P @ P, P) for P in EJ))
def crc(f, g):
    nf, ng = np.linalg.norm(f), np.linalg.norm(g); z = np.array([np.vdot(P @ f, P @ g) for P in EJ]) / (nf * ng)
    p = np.array([np.linalg.norm(P @ f)**2 for P in EJ]) / nf**2; q = np.array([np.linalg.norm(P @ g)**2 for P in EJ]) / ng**2
    Bq = np.sum(np.sqrt(p * q)); Qq = np.sum(abs(z)); Sq = abs(np.sum(z)); Lq = max(abs(np.sum(z * np.exp(2j * np.pi * np.arange(24) * t / 24))) for t in range(24))
    return Sq, Lq, Qq, Bq
rng = np.random.default_rng(7); okc = True
for _ in range(20):
    f = rng.normal(size=81) + 1j * rng.normal(size=81); g = rng.normal(size=81) + 1j * rng.normal(size=81)
    Sq, Lq, Qq, Bq = crc(f, g); okc &= Sq <= Lq + 1e-12 and Lq <= Qq + 1e-12 and Qq <= Bq + 1e-12 and Bq <= 1 + 1e-12
d = lambda x: np.eye(81)[idx[x]].astype(complex)
s1, s2 = crc(d((2, 5)), d((5, 7))), crc(d((2, 5)), d((1, 0)))
ok('CRC-01 S <= L <= Q <= B <= 1 (20 random pairs); same orbit S=0, L=Q=B=1; different 24-orbits S=L=Q=0, B=1',
   okc and np.allclose(s1, (0, 1, 1, 1)) and np.allclose(s2, (0, 0, 0, 1)))
reps = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
closure = lambda fs: np.linalg.matrix_rank(np.array([np.roll(0, 0) * 0 + np.array([F[idx[Tn(x, t)]] for x in X]) for F in fs for t in range(24)]), tol=1e-8)
ok('CRN-01 five orbit representatives give invariant closure 81; any four give less', closure([d(x) for x in reps]) == 81
   and all(closure([d(x) for x in reps if x != r]) < 81 for r in reps))

# CCR-01 / CGM-01: generative reachability from (2, 5) under subsets of {A, V, C, S}
from collections import deque
def gens(m): return {'A': lambda x: (x[1], (x[0] + x[1]) % m), 'V': lambda x: (2*x[0] % m, 2*x[1] % m),
                     'C': lambda x: (3*x[0] % m, 3*x[1] % m), 'S': lambda x: (x[0] % m, (3*x[0] + x[1]) % m)}
def reach(sub, m=9, start=(2, 5)):
    g = gens(m); dist = {start: 0}; q = deque([start])
    while q:
        x = q.popleft()
        for k in sub:
            y = g[k](x)
            if y not in dist: dist[y] = dist[x] + 1; q.append(y)
    return dist
want = dict(A=24, V=6, C=3, S=3, AV=72, AC=33, AS=72, VC=9, VS=18, CS=5, AVC=81, AVS=72, ACS=81, VCS=21, AVCS=81)
got = {k: len(reach(k)) for k in want}
ok('CGM-01 reachable states from (2,5) for all 15 generator subsets mod 9 match; AVC and ACS minimal full', got == want)
ok('CGM-01 eccentricity from the seed mod 9: AVC 16, ACS 10, AVCS 6', [max(reach(k).values()) for k in ('AVC', 'ACS', 'AVCS')] == [16, 10, 6])
ok('CGM-01 AVC and ACS reach all of W3 and W4; eccentricities AVC 52, 160; ACS 12, 16',
   all(len(reach(k, 3**d)) == 9**d for k in ('AVC', 'ACS') for d in (3, 4)) and [max(reach('AVC', 27).values()), max(reach('AVC', 81).values()), max(reach('ACS', 27).values()), max(reach('ACS', 81).values())] == [52, 160, 12, 16])
# CCO-01: the counterexample to greedy optimality, as sets of harmonics
A_, B_, C_ = {1, 2, 4, 5}, {1, 2, 3}, {4, 5, 6}
ok('CCO-01 capacities 4,3,3; pairs AB=5, AC=5, BC=6: greedy (A first) reaches 5 of the optimum 6', [len(A_), len(B_), len(C_), len(A_ | B_), len(A_ | C_), len(B_ | C_)] == [4, 3, 3, 5, 5, 6])
print('%d checks, %d failed' % (len(R), R.count(False)))
