"""R-14 check: first exact results for ChatGPT's Universal Mathematical Interface Programme. Pure Python; about a minute.
(1) Observation codes at depth 2: the best minimum Hamming distance of native teams is 1, 1, 2, 2 for n = 3..6 readings,
    while Reed-Solomon codes over F_7 with 343 >= 81 words reach n - 2: 1, 2, 3, 4.
(2) The 9 states of depth 1 are the affine plane AG(2,3): 12 lines in 4 parallel classes, every pair of points on one line;
    the law permutes the 4 classes in a single 4-cycle, so it schedules the 4 rounds of the 9-treatment design cyclically.
(3) The golden channel: energy split 50/50 between the phi and -1/phi eigenspaces becomes phi^2 : phi^-2 after one step,
    i.e. 87.27% : 12.73%, total 1.5 times the input (ChatGPT's figures).
(4) Music: phase mod 12 is a homomorphism Z/24 -> Z/12 with kernel {0, 12}; the half turn A^12 = -I lies in it."""
import itertools, sys
R = []
def ok(n, c): R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n, flush=True)
q = 9; N = 24; F = [0, 1]
for _ in range(N + 2): F.append((F[-1] + F[-2]) % q)
S = [(a, b) for a in range(q) for b in range(q)]
rd = [[((F[t - 1] if t else F[N - 1]) * a + F[t] * b) % q % 7 for (a, b) in S] for t in range(N)]
best = {}
for n in range(3, 7):
    bd = 0
    for T in itertools.combinations(range(1, N), n - 1):
        W = [tuple(rd[t][i] for t in (0,) + T) for i in range(81)]
        if len(set(W)) < 81: continue
        bd = max(bd, min(sum(x != y for x, y in zip(W[i], W[j])) for i in range(81) for j in range(i + 1, 81)))
    best[n] = bd
ok('native observation codes at depth 2: best minimum distance 1, 1, 2, 2 for 3 to 6 readings', [best[n] for n in range(3, 7)] == [1, 1, 2, 2])
# Reed-Solomon [n, 3, n-2] over F_7 (evaluation of polynomials of degree < 3 at n distinct points), n = 3..6
def rs_dist(n):
    pts = list(range(n)); W = [tuple((c0 + c1 * x + c2 * x * x) % 7 for x in pts) for c0 in range(7) for c1 in range(7) for c2 in range(7)]
    return min(sum(a != b for a, b in zip(W[0], w)) for w in W[1:])     # linear code: distance = min weight
ok('Reed-Solomon over F_7 with 343 words: minimum distance 1, 2, 3, 4 for n = 3 to 6', [rs_dist(n) for n in range(3, 7)] == [1, 2, 3, 4])
P = [(a, b) for a in range(3) for b in range(3)]; dirs = [(1, 0), (0, 1), (1, 1), (1, 2)]
lines = {frozenset(((p[0] + t * d[0]) % 3, (p[1] + t * d[1]) % 3) for t in range(3)) for p in P for d in dirs}
ok('AG(2,3): 12 lines, every pair of the 9 points on exactly one line', len(lines) == 12 and all(sum(1 for L in lines if x in L and y in L) == 1 for x, y in itertools.combinations(P, 2)))
norm = lambda v: next(d for d in dirs if any(((k * d[0] - v[0]) % 3, (k * d[1] - v[1]) % 3) == (0, 0) for k in (1, 2)))
img = [norm((d[1], (d[0] + d[1]) % 3)) for d in dirs]
ok('the law cycles the 4 parallel classes: [1:0] -> [0:1] -> [1:1] -> [1:2] -> [1:0]', img == [dirs[1], dirs[2], dirs[3], dirs[0]])
phi = (1 + 5 ** .5) / 2; e1, e2 = .5 * phi ** 2, .5 * phi ** -2
ok('golden channel: 50/50 becomes 87.27% / 12.73%, total 1.5', abs(e1 / (e1 + e2) - .8727) < 5e-5 and abs(e1 + e2 - 1.5) < 1e-12)
ok('music: phase mod 12 is a homomorphism of Z/24 with kernel {0, 12}', all((a + b) % 24 % 12 == (a % 12 + b % 12) % 12 for a in range(24) for b in range(24)) and [t for t in range(24) if t % 12 == 0] == [0, 12])
# (5) the hybrid code: the 3 native readings (0, 2, 5) as message, Reed-Solomon parity over F_7 appended (systematic [n, 3, n-2])
def lag(m, x):
    s = 0
    for i in range(3):
        num = den = 1
        for j in range(3):
            if j != i: num = num * (x - j) % 7; den = den * (i - j) % 7
        s = (s + m[i] * num * pow(den, 5, 7)) % 7
    return s
H = []
for i in range(81):
    m = tuple(rd[t][i] for t in (0, 2, 5)); H.append(m + (lag(m, 3), lag(m, 4)))
dmin = lambda W: min(sum(x != y for x, y in zip(W[i], W[j])) for i in range(81) for j in range(i + 1, 81))
ok('hybrid: native readings (0, 2, 5) + Reed-Solomon parity reach distance 2 with 4 symbols and 3 with 5 (one error corrected)', dmin([h[:4] for h in H]) == 2 and dmin(H) == 3)
# (6) one construction for both designs: a primitive element of F_(3^n) cycles the (3^n - 1)/2 directions of AG(n, 3)
def directions_cycle(n, mul):
    pts = [p for p in itertools.product(range(3), repeat=n) if any(p)]
    canon = lambda v: min(v, tuple((2 * x) % 3 for x in v))
    D = sorted({canon(p) for p in pts}); start = D[0]; x = start; seen = []
    while True:
        seen.append(x); x = canon(mul(x))
        if x == start: break
    return len(seen) == len(D) == (3 ** n - 1) // 2
phi_mul = lambda v: (v[1], (v[0] + v[1]) % 3)                       # the law: multiplication by phi in F_9 = F_3[phi]
g_mul = lambda v: ((-v[2]) % 3, (v[0] + v[2]) % 3, v[1])           # multiplication by g in F_27 = F_3[g]/(g^3 - g + 1): g^3 = g - 1
ok('the law (phi in F_9) cycles the 4 directions of AG(2,3); g in F_27, g^3 = g - 1, cycles the 13 directions of AG(3,3)', directions_cycle(2, phi_mul) and directions_cycle(3, g_mul) and all((x ** 3 - x + 1) % 3 for x in range(3)))
print('%d of %d checks passed' % (sum(R), len(R))); sys.exit(0 if all(R) else 1)
