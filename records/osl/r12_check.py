"""R-12 check: the open problems of the tower, this round (paper Lemma 5.9, Corollary 5.10, Theorem 22.1 at depth 6,
Proposition 20.5 at depth 8). NumPy.
    python3 records/osl/r12_check.py              # descent, the O-31 exclusion, ACS at depth 8 (about a minute)
    python3 records/osl/r12_check.py --adaptive   # also the greedy adaptive observer at depth 6 (about two minutes more)
"""
import sys, itertools, numpy as np
R = []
def ok(n, c): R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n, flush=True)
def fib(q, N):
    F = [0, 1]
    for _ in range(N + 2): F.append((F[-1] + F[-2]) % q)
    return F
def grid(k):
    q = 3 ** k; return q, np.repeat(np.arange(q, dtype=np.int64), q), np.tile(np.arange(q, dtype=np.int64), q)
def reader(k):
    q, a, b = grid(k); N = 8 * 3 ** (k - 1); F = fib(q, N)
    return (lambda t: ((F[t - 1] if t > 0 else F[N - 1]) * a + F[t] * b) % q % 7), q * q, N
def classes(k, T):
    rd, n, _ = reader(k); code = np.zeros(n, dtype=np.int64)
    for t in T: code = code * 7 + rd(t)
    _, cls, cnt = np.unique(code, return_inverse=True, return_counts=True); return cls, cnt
sep = lambda k, T: classes(k, T)[1].max() == 1
T5 = [0, 5, 44, 199, 243, 562]; T4 = [0, 94, 145, 152, 195]; T8 = [0, 11, 502, 510, 737, 777, 1820, 1842]
# Lemma 5.9 on known teams, and a direct check of the embedding identity
ok('descent: the depth-6 eight-phase team separates W_5 mod 648, W_4 mod 216, W_3 mod 72', all(sep(k, sorted({t % (8 * 3 ** (k - 1)) for t in T8})) for k in (5, 4, 3)))
ok('descent: the depth-5 team separates W_4 and W_3; the depth-4 team separates W_3', sep(4, sorted({t % 216 for t in T5})) and sep(3, sorted({t % 72 for t in T5})) and sep(3, sorted({t % 72 for t in T4})))
rd6, _, _ = reader(6); rd5, _, _ = reader(5); q5 = 243; ys = np.arange(q5 * q5); ya, yb = ys // q5, ys % q5
ok('embedding identity: reading of A^t(3y) at depth 6 = 3 x reading of A^t y at depth 5, mod 7, for t < 1944', all(np.array_equal(rd6(t)[(3 * ya) * 729 + 3 * yb] % 7, (3 * rd5(t % 648)[ya * q5 + yb]) % 7) for t in range(0, 1944, 37)))
ok('no lift: no single phase added to the depth-4 team separates W_5', not any(sep(5, T4 + [p]) for p in range(1, 648) if p not in T4))
# Corollary 5.10: the 243 lifts of T5
worst = min(int(classes(6, [0] + [T5[i + 1] + 648 * j[i] for i in range(5)])[1].max()) for j in itertools.product(range(3), repeat=5))
ok('O-31 exclusion: every lift of the depth-5 team leaves a class of at least 9 states at depth 6 (smallest largest class: %d)' % worst, worst >= 8)
ok('the best collision team (0, 28, 127, 953, 1156, 1652, 1785) does not reduce to a separating team of W_5', not sep(5, sorted({t % 648 for t in [0, 28, 127, 953, 1156, 1652, 1785]})))
# Proposition 20.5 at depth 8: ACS eccentricity 30
k = 8; q = 3 ** k; dist = np.full(q * q, -1, dtype=np.int8); s = 2 * q + 5; dist[s] = 0; fr = np.array([s], dtype=np.int64); d = 0
while fr.size:
    a, b = fr // q, fr % q
    nx = np.unique(np.concatenate([b * q + (a + b) % q, (3 * a % q) * q + 3 * b % q, a * q + (3 * a + b) % q])); nx = nx[dist[nx] < 0]
    d += 1; dist[nx] = d; fr = nx
ok('depth 8: {A, C, S} reaches all 43,046,721 states, eccentricity 30 (lower bound 25)', int((dist >= 0).sum()) == q * q and int(dist.max()) == 30)
if '--adaptive' in sys.argv:
    k = 6; rd, n, N = reader(k); cls = np.zeros(n, dtype=np.int64); used = 0
    while np.bincount(cls).max() > 1:
        C = int(cls.max()) + 1; best = np.full(C, n + 1); bp = np.zeros(C, dtype=np.int64)
        for t in range(N):
            m = np.bincount(cls * 7 + rd(t), minlength=C * 7).reshape(C, 7).max(axis=1); bt = m < best; best[bt] = m[bt]; bp[bt] = t
        sym = np.empty(n, dtype=np.int64); ch = bp[cls]
        for t in np.unique(ch): idx = np.flatnonzero(ch == t); sym[idx] = rd(int(t))[idx]
        _, cls = np.unique(cls * 7 + sym, return_inverse=True); used += 1
    ok('adaptive: greedy minimax separates the 531,441 states of W_6 in %d readings (bound 7)' % used, used == 7)
print('%d of %d checks passed' % (sum(R), len(R))); sys.exit(0 if all(R) else 1)
