"""Independent recomputation of the register results surveyed in Part II of the mathematical paper (docs/OMEGA42_MATHEMATICAL_PAPER.md).
Standard library only. Run: python3 records/cobuilder/paper_part2_check.py"""
import cmath, itertools, math
R = []
def ok(name, cond): R.append((name, bool(cond))); print(('PASS ' if cond else 'FAIL ') + name)

def mul(X, Y, m): return [[(X[0][0]*Y[0][0]+X[0][1]*Y[1][0]) % m, (X[0][0]*Y[0][1]+X[0][1]*Y[1][1]) % m],
                          [(X[1][0]*Y[0][0]+X[1][1]*Y[1][0]) % m, (X[1][0]*Y[0][1]+X[1][1]*Y[1][1]) % m]]
def key(X): return (X[0][0], X[0][1], X[1][0], X[1][1])
def closure(gens, m):
    I = [[1, 0], [0, 1]]; seen = {key(I): I}; fr = [I]
    while fr:
        nf = []
        for X in fr:
            for g in gens:
                Y = mul(X, g, m); k = key(Y)
                if k not in seen: seen[k] = Y; nf.append(Y)
        fr = nf
    return seen
A = [[0, 1], [1, 1]]; B = [[1, 0], [3, 1]]
# Z[phi] arithmetic: (a, b) = a + b phi, phi^2 = phi + 1
def zm(x, y, m): a, b = x; c, d = y; return ((a*c + b*d) % m, (a*d + b*c + b*d) % m)
def zpow(x, n, m):
    r = (1, 0)
    for _ in range(n): r = zm(r, x, m)
    return r
def N(x, m): a, b = x; return (a*a + a*b - b*b) % m
# MF-01: phi -> 5 + i respects phi^2 = phi + 1 mod 9
ok('MF-01 (5+i)^2 = (5+i)+1 mod 9', ((25 - 1) % 9, 10 % 9) == ((5 + 1) % 9, 1))
# MF-03: phi^6 = 5 + 8 phi and its square is -1 mod 9
ok('MF-03 phi^6 = 5+8phi, (phi^6)^2 = -1 mod 9', zpow((0, 1), 6, 10**6) == (5, 8) and zm((5, 8), (5, 8), 9) == (8, 0))
# MF-39: units of norm +-1 mod 3^m are exactly the powers of phi, 8*3^(m-1) of them
for m in (1, 2, 3):
    M = 3**m; units = {(a, b) for a in range(M) for b in range(M) if N((a, b), M) in (1, M - 1)}
    pw = set(); x = (1, 0)
    while True:
        pw.add(x); x = zm(x, (0, 1), M)
        if x == (1, 0): break
    ok('MF-39 norm +-1 units = powers of phi mod 3^%d (%d)' % (m, len(pw)), units == pw and len(pw) == 8 * 3**(m - 1))
# MF-45: matrices keeping Q up to nothing (O(Q)) mod 9 number 8*3 = 24; SO = <A^2> of order 12
def Qv(v, m): return (v[0]*v[0] + v[0]*v[1] - v[1]*v[1]) % m
O = [X for X in itertools.product(range(9), repeat=4)
     if all(Qv(((X[0]*a + X[1]*b) % 9, (X[2]*a + X[3]*b) % 9), 9) == Qv((a, b), 9) for a in range(9) for b in range(9))]
SO = [X for X in O if (X[0]*X[3] - X[1]*X[2]) % 9 == 1]
ok('MF-45 |O(Q) mod 9| = 24, |SO(Q) mod 9| = 12 = |<A^2>|', len(O) == 24 and len(SO) == 12 and len(closure([mul(A, A, 9)], 9)) == 12)
# MF-42: <A, B> mod 9 has order 8*3^3 = 216
ok('MF-42/97 |<A, B> mod 9| = 216', len(closure([A, B], 9)) == 216)
# MF-68/71: <A, B> mod 7 is every matrix of determinant +-1 (672); MF-77: <A^2, B> acts on P^1(F7) as a group of order 168
G7 = closure([A, B], 7)
ok('MF-71 <A, B> mod 7 = all det +-1 matrices (672)', len(G7) == 672 and all((k[0]*k[3] - k[1]*k[2]) % 7 in (1, 6) for k in G7))
P1 = [(1, t) for t in range(7)] + [(0, 1)]
def pnorm(v):
    a, b = v[0] % 7, v[1] % 7
    if a: inv = pow(a, -1, 7); return (1, b * inv % 7)
    return (0, 1)
H = closure([mul(A, A, 7), B], 7)
perms = {tuple(pnorm((X[0]*p[0] + X[1]*p[1], X[2]*p[0] + X[3]*p[1])) for p in P1) for X in H}
ok('MF-77 <A^2, B> mod 7 acts on P^1(F7) as a group of order 168', len(perms) == 168)
# MF-84 and MF-103: A^2 conjugated by the swap is [[2,1],[1,1]]
A2 = [[1, 1], [1, 2]]; S = [[0, 1], [1, 0]]
ok('MF-84 swap.A^2.swap = [[2,1],[1,1]] (cat map, figure-eight monodromy)', mul(mul(S, A2, 100), S, 100) == [[2, 1], [1, 1]])
# MF-86: primitive periodic points of the law on the torus by Moebius inversion
def L(n):
    x, y = 2, 1
    for _ in range(n): x, y = y, x + y
    return x
fix = {n: abs(L(n) - 1 - (-1)**n) for n in range(1, 9)}
def mob(n):
    r, k, p = 1, n, 2
    while p * p <= k:
        if k % p == 0:
            k //= p
            if k % p == 0: return 0
            r = -r
        p += 1
    return -r if k > 1 else r
prim = [sum(mob(n // d) * fix[d] for d in range(1, n + 1) if n % d == 0) for n in range(1, 9)]
ok('MF-86 primitive periodic points 1, 0, 3, 4, 10, 12, 28, 40', prim == [1, 0, 3, 4, 10, 12, 28, 40])
ok('Theorem 8.3 |L_24 - 2| = 103,680 = 81 x 1,280', abs(L(24) - 2) == 103680 == 81 * 1280)
# MF-83: (1, F_(2n-1), F_(2n+1)) solves x^2 + y^2 + z^2 = 3xyz
F = [0, 1]
for _ in range(60): F.append(F[-1] + F[-2])
ok('MF-83 Markov triples (1, F_2n-1, F_2n+1), n = 1..20', all(1 + F[2*n - 1]**2 + F[2*n + 1]**2 == 3 * F[2*n - 1] * F[2*n + 1] for n in range(1, 21)))
# MF-95 and MF-136: cosh(2 ln phi) = 3/2; the golden boost has gamma = L_4/2 = 7/2
phi = (1 + 5**.5) / 2
ok('MF-95 2 arccosh(3/2) = 4 ln phi; MF-136 gamma = L_4/2 = 7/2', abs(2 * math.acosh(1.5) - 4 * math.log(phi)) < 1e-12 and L(4) == 7)
# MF-88/177: the Fibonacci fusion matrix in the basis (1, tau) is A, Perron eigenvalue phi
ok('MF-88 fusion matrix of tau is A, quantum dimension phi', [[0, 1], [1, 1]] == A and abs(phi * phi - phi - 1) < 1e-12)
# MF-188: sqrt5 = phi + 1/phi and sqrt5 - 2 = phi^-3
ok('MF-188 sqrt5 = phi + 1/phi, sqrt5 - 2 = phi^-3', abs(5**.5 - phi - 1/phi) < 1e-12 and abs(5**.5 - 2 - phi**-3) < 1e-12)
# MF-129/130/148/163: the trace map
def tr(t, m): x, y, z = t; return ((2*x*y - z) % m, x, y)
def orbit_census(m):
    seen, cen = set(), {}
    for t in itertools.product(range(m), repeat=3):
        if t in seen: continue
        n, u = 0, t
        while True:
            seen.add(u); u = tr(u, m); n += 1
            if u == t: break
        cen[n] = cen.get(n, 0) + 1
    return cen
c9 = orbit_census(9)
ok('MF-148 trace map mod 9: 2x1, 2x2, 1x3, 9x4, 8x6, 3x8, 9x12, 21x24', c9 == {1: 2, 2: 2, 3: 1, 4: 9, 6: 8, 8: 3, 12: 9, 24: 21})
def period(m): c = orbit_census(m); return math.lcm(*c)
ok('MF-163 trace-map period 12 mod 3, 24 mod 9, 72 mod 27', period(3) == 12 and period(9) == 24 and period(27) == 72)
def FV(t): x, y, z = t; return x*x + y*y + z*z - 2*x*y*z - 1
t = (0.37, -1.21, 0.58); ok('MF-129 Fricke-Vogt invariant kept by the trace map', all(abs(FV(t) - FV(t := (2*t[0]*t[1] - t[2], t[0], t[1]))) < 1e-9 for _ in range(6)))
u = (0, 0, 5); seq = [u]
for _ in range(6): u = tr(u, 10**9); seq.append(u)
ok('MF-130 (0, 0, a) returns after exactly six steps', seq[6] == (0, 0, 5) and all(s != (0, 0, 5) for s in seq[1:6]))
# MF-184/185: A^2 has N orbits on the N^2 labels at N = 3^k (so the quantum cat map has simple spectrum)
def orbits(M, m):
    seen, n = set(), 0
    for a in range(m):
        for b in range(m):
            if (a, b) in seen: continue
            n += 1; v = (a, b)
            while v not in seen: seen.add(v); v = ((M[0][0]*v[0] + M[0][1]*v[1]) % m, (M[1][0]*v[0] + M[1][1]*v[1]) % m)
    return n
ok('MF-185 A^2 has 3, 9, 27 orbits on the labels mod 3, 9, 27', [orbits(A2, 3**k) for k in (1, 2, 3)] == [3, 9, 27])
# MF-186: the kernel U(j,k) = w^(j^2 - jk + k^2/2)/sqrt N is unitary for odd N (1/2 read mod N)
def U(Nn):
    h = pow(2, -1, Nn); w = cmath.exp(2j * cmath.pi / Nn)
    return [[w**((j*j - j*k + k*k*h) % Nn) / Nn**.5 for k in range(Nn)] for j in range(Nn)]
def unitary(M):
    n = len(M); return all(abs(sum(M[i][k] * M[j][k].conjugate() for k in range(n)) - (i == j)) < 1e-9 for i in range(n) for j in range(n))
ok('MF-186 quantum cat kernel unitary for N = 3, 5, 7, 9, 11', all(unitary(U(n)) for n in (3, 5, 7, 9, 11)))
# MF-203: mod 11, roots 8 and 4 of x^2 = x + 1, census 1 + 2x5 + 11x10
cen = {}; seen = set()
for a in range(11):
    for b in range(11):
        if (a, b) in seen: continue
        v, n = (a, b), 0
        while True:
            seen.add(v); v = (v[1], (v[0] + v[1]) % 11); n += 1
            if v == (a, b): break
        cen[n] = cen.get(n, 0) + 1
ok('MF-203 mod 11: roots 4 and 8; census 1 + 2x5 + 11x10', all((r*r - r - 1) % 11 == 0 for r in (4, 8)) and cen == {1: 1, 5: 2, 10: 11})
# MF-73 qualified: 3R/9R has zero multiplication (3x.3y = 9xy), so it is not a field; as an R-module it is R/3R = F9, where phi acts with order 8
ok('MF-73 qualified: products in 3R/9R vanish; phi acts on it with order 8',
   all(zm((3*a, 3*b), (3*c, 3*d), 9) == (0, 0) for a in range(3) for b in range(3) for c in range(3) for d in range(3))
   and min(n for n in range(1, 25) if zpow((0, 1), n, 3) == (1, 0)) == 8)
print('%d checks, %d failed' % (len(R), sum(1 for _, c in R if not c)))
