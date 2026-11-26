"""Recomputation of Part III of the mathematical paper (information across depths and worlds): ChatGPT's extensions EXT-01 to EXT-08
of 26 November 2026, checked independently. Needs NumPy for the resonance checks. Run: python3 records/cobuilder/paper_part3_check.py"""
import math
import numpy as np
R = []
def ok(n, c): R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n)

def orbits(m, step):
    seen, out = set(), []
    for a in range(m):
        for b in range(m):
            if (a, b) in seen: continue
            o, x = [], (a, b)
            while x not in seen: seen.add(x); o.append(x); x = step(x, m)
            out.append(o)
    return out
fib = lambda x, m: (x[1], (x[0] + x[1]) % m)
census = lambda m: sorted(len(o) for o in orbits(m, fib))

# EXT-02: the commutant of the shift has dimension sum over pairs of orbits of gcd(lengths) = (5*27^k + 8)/13
for k in range(1, 6):
    L = []
    for j in range(1, k + 1): L += [8 * 3**(j - 1)] * 3**(j - 1)
    L.append(1)
    D = sum(math.gcd(a, b) for a in L for b in L)
    ok('EXT-02 commutant dimension at depth %d = %d = (5*27^k+8)/13' % (k, D), D * 13 == 5 * 27**k + 8 and (k > 3 or sorted(L) == census(3**k)))

# EXT-01: memory lifting. g on W_k (values mod 3^k), pulled back to W_(k+1) with s -> 3s; classes are orbit-sum vectors
def lift_kernel_image(k):
    m, M = 3**k, 3**(k + 1)
    Ok, O1 = orbits(m, fib), orbits(M, fib)
    # the map on orbit sums: a delta of weight 1 at the representative of orbit i of depth k, pulled back, has orbit sums at depth k+1
    idx = {x: i for i, o in enumerate(Ok) for x in o}
    cols = []
    for i, o in enumerate(Ok):
        r = o[0]
        cols.append([sum(3 for y in o2 if (y[0] % m, y[1] % m) == r) % M for o2 in O1])
    # image of (Z/3^k)^c: span of cols with coefficients mod 3^k (coefficient s -> s*col, col already carries the factor 3)
    # count image and kernel by brute force on orbit-sum vectors (small k)
    import itertools
    imgs = set(); ker = 0
    for coef in itertools.product(range(m), repeat=len(Ok)):
        v = tuple(sum(c * col[t] for c, col in zip(coef, cols)) % M for t in range(len(O1)))
        imgs.add(v); ker += all(x == 0 for x in v)
    return len(Ok), ker, len(imgs)
for k in (1, 2):
    c, ker, im = lift_kernel_image(k)
    ok('EXT-01 memory lifting depth %d -> %d: kernel 3^(c-1) = %d, image 3^(kc-c+1) = %d' % (k, k + 1, ker, im), ker == 3**(c - 1) and im == 3**(k * c - c + 1))

# EXT-05 / EXT-06: the 7-world and the 11-world
def bystrata(p, k):
    cen = {}
    for L in census(p**k): cen[L] = cen.get(L, 0) + 1
    return cen
ok('EXT-05 mod 7: 1 + 3 x 16', bystrata(7, 1) == {1: 1, 16: 3})
ok('EXT-05 mod 49: 1 + 3 x 16 + 21 x 112; (7^2+1)/2 = 25 orbits', bystrata(7, 2) == {1: 1, 16: 3, 112: 21} and sum(bystrata(7, 2).values()) == 25)
F = [0, 1]
for _ in range(20): F.append(F[-1] + F[-2])
Q = [[F[15] - 1, F[16]], [F[16], F[17] - 1]]
ok('EXT-05 A^16 - I = 7 x [[87,141],[141,228]], not divisible by 49, quotient invertible mod 7',
   Q == [[609, 987], [987, 1596]] and all(x % 7 == 0 for r in Q for x in r) and Q[0][0] % 49 and (87 * 228 - 141 * 141) % 7)
ok('EXT-06 mod 11: 1 + 2 x 5 + 11 x 10', bystrata(11, 1) == {1: 1, 5: 2, 10: 11})
ok('EXT-06 mod 121: + 2 x 55 + 131 x 110; 1 + k + 6(11^k - 1)/5 = 136 orbits', bystrata(11, 2) == {1: 1, 5: 2, 10: 11, 55: 2, 110: 131} and sum(bystrata(11, 2).values()) == 1 + 2 + 6 * 120 // 5)

# EXT-07: adaptive observation of W2 needs exactly three seven-symbol readings
ok('EXT-07 two adaptive readings give at most 7^2 = 49 < 81 leaves; the native team (0, 2, 5) of a mod 7 separates W2',
   49 < 81 and len({tuple((lambda y: y[0] % 7)(s) for s in [x, fib(fib(x, 9), 9), fib(fib(fib(fib(fib(x, 9), 9), 9), 9), 9)]) for x in [(a, b) for a in range(9) for b in range(9)]}) == 81)

# EXT-03 / EXT-04: refinement J, resonance persistence, detail decomposition
def basis(k):
    m = 3**k; P = 8 * 3**(k - 1); Os = orbits(m, fib); index = {(a, b): a * m + b for a in range(m) for b in range(m)}
    E = []   # (orbit id, harmonic j, vector)
    for oi, o in enumerate(Os):
        L = len(o)
        for t in range(L):   # eigen-index on this orbit
            j = t * (P // L); e = np.zeros(m * m, complex)
            for s, x in enumerate(o): e[index[x]] = np.exp(2j * np.pi * j * s / P) / np.sqrt(L)
            E.append((oi, j, e))
    return E, P
def measures(v, w, E):
    nv, nw = np.linalg.norm(v), np.linalg.norm(w)
    F_ = abs(np.vdot(v, w)) / (nv * nw)
    co = {}
    for oi, j, e in E: co.setdefault(j, []).append((np.vdot(e, v), np.vdot(e, w)))
    FB = sum(abs(sum(np.conj(a) * b for a, b in c)) for c in co.values()) / (nv * nw)
    RO = sum(abs(a) * abs(b) for c in co.values() for a, b in c) / (nv * nw)
    RH = sum(np.sqrt(sum(abs(a)**2 for a, _ in c) * sum(abs(b)**2 for _, b in c)) for c in co.values()) / (nv * nw)
    return np.array([F_, FB, RO, RH])
def J(v, k):
    m, M = 3**k, 3**(k + 1); out = np.zeros(M * M, complex)
    for a in range(M):
        for b in range(M): out[a * M + b] = v[(a % m) * m + (b % m)] / 3
    return out
rng = np.random.default_rng(42)
E2, _ = basis(2); E3, _ = basis(3)
worst = 0; isom = 0
for _ in range(6):
    v = rng.normal(size=81) + 1j * rng.normal(size=81); w = rng.normal(size=81) + 1j * rng.normal(size=81)
    a, b = measures(v, w, E2), measures(J(v, 2), J(w, 2), E3)
    worst = max(worst, np.max(np.abs(a - b))); isom = max(isom, abs(np.linalg.norm(J(v, 2)) - np.linalg.norm(v)))
    ok('  chain 0 <= F <= F_B <= R_O <= R_H <= 1 holds (%.4f %.4f %.4f %.4f)' % tuple(a), all(np.diff(np.r_[0, a, 1]) >= -1e-12))
ok('EXT-03 J is an isometry and keeps F, F_B, R_O, R_H from depth 2 to depth 3 (max deviation %.1e)' % worst, worst < 1e-9 and isom < 1e-9)
Uv = lambda v, k: np.array([v[(lambda x: x[0] * 3**k + x[1])(fib((a, b), 3**k))] for a in range(3**k) for b in range(3**k)])
v = rng.normal(size=81)
ok('EXT-03 J intertwines the shift: U_3 J = J U_2', np.allclose(Uv(J(v, 2), 3), J(Uv(v, 2), 2)))
Jm = np.zeros((729, 81))
for i in range(81):
    e = np.zeros(81); e[i] = 1; Jm[:, i] = J(e, 2).real
P_ = Jm @ Jm.T
ok('EXT-04 JJ* is an orthogonal projection of rank 81; the detail space has dimension 648 = 8 x 9^2',
   np.allclose(P_ @ P_, P_) and np.allclose(P_, P_.T) and round(np.trace(P_)) == 81 and 729 - 81 == 8 * 81)

# Theorem 22.1: the greedy minimax adaptive observer of a mod 7 attains ceil(k log_7 9) at depths 2 to 5
def greedy(k):
    m, P = 3**k, 8 * 3**(k - 1)
    x = np.repeat(np.arange(m), m); y = np.tile(np.arange(m), m); tab = np.zeros((m * m, P), np.int8)
    for t in range(P): tab[:, t] = x % 7; x, y = y, (x + y) % m
    worst, stack = 0, [(np.arange(m * m), 0)]
    while stack:
        C, d = stack.pop()
        if len(C) <= 1: worst = max(worst, d); continue
        sub = tab[C]; mx = np.stack([(sub == s).sum(0) for s in range(7)]).max(0); t = int(mx.argmin())
        if mx[t] == len(C): return None
        for s in range(7):
            part = C[sub[:, t] == s]
            if len(part): stack.append((part, d + 1))
    return worst
for k in (2, 3, 4, 5):
    b = math.ceil(k * math.log(9) / math.log(7) - 1e-12)
    ok('Theorem 22.1 greedy adaptive observer at depth %d needs %s readings, the bound %d' % (k, greedy(k), b), greedy(k) == b)
# Corollary 21.3: inert primes, order 2(p+1), regular lifting; census (p+1)/2 at k = 1 and (p^2+1)/2 at k = 2 when full and regular
def mat_pow_mod(n, mod):
    R_, B = [[1, 0], [0, 1]], [[0, 1], [1, 1]]
    while n:
        if n & 1: R_ = [[(R_[0][0]*B[0][0]+R_[0][1]*B[1][0]) % mod, (R_[0][0]*B[0][1]+R_[0][1]*B[1][1]) % mod], [(R_[1][0]*B[0][0]+R_[1][1]*B[1][0]) % mod, (R_[1][0]*B[0][1]+R_[1][1]*B[1][1]) % mod]]
        B = [[(B[0][0]*B[0][0]+B[0][1]*B[1][0]) % mod, (B[0][0]*B[0][1]+B[0][1]*B[1][1]) % mod], [(B[1][0]*B[0][0]+B[1][1]*B[1][0]) % mod, (B[1][0]*B[0][1]+B[1][1]*B[1][1]) % mod]]
        n >>= 1
    return R_
full = []
for p in [q for q in range(3, 60) if all(q % d for d in range(2, q))]:
    if any((r * r - r - 1) % p == 0 for r in range(p)): continue   # split or ramified
    order = min(n for n in range(1, 2 * (p + 1) + 1) if mat_pow_mod(n, p) == [[1, 0], [0, 1]])
    regular = mat_pow_mod(order, p * p) != [[1, 0], [0, 1]]
    if order == 2 * (p + 1) and regular: full.append(p)
    if p <= 13:
        c1 = len(census(p))
        ok('Corollary 21.3 p = %d: order %d (max %d), regular %s, %d orbits mod p' % (p, order, 2 * (p + 1), regular, c1), (c1 == (p + 1) // 2) == (order == 2 * (p + 1)))
ok('Corollary 21.3 p = 7 at k = 2: (49 + 1)/2 = 25 orbits', len(census(49)) == 25)
print('inert primes below 60 of full order with regular lifting:', full)
print('%d checks, %d failed' % (len(R), R.count(False)))
