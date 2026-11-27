"""R-05 check: Claude's review of ChatGPT's R-03 response.

1. ChatGPT's depth-6 eight-phase team separates all 531,441 states (direct count + difference criterion).
2. C-R3a: ChatGPT's closed formula for the {A,V,C} distance equals the BFS distance of EVERY state, k = 1..6.
3. C-R3b: the word-counting lower bound sits below the computed {A,C,S} diameters, k = 1..7.
4. Wrap feasibility: the best seven-phase team at depth 6 has 4 passing differences, and each of them
   yields actual collisions, so the refinement does not rescue it.
numpy; about a minute.
"""
import sys
import numpy as np

R = []
def ok(name, c):
    R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + name)

def first_rows(k, n):
    """Row 0 of A^t mod 3^k for t = 0..n-1, as arrays p[t], r[t]: first coord of A^t (a,b) = p a + r b."""
    q = 3 ** k
    p = np.zeros(n, dtype=np.int64); r = np.zeros(n, dtype=np.int64)
    M = np.array([[1, 0], [0, 1]], dtype=np.int64); A = np.array([[0, 1], [1, 1]], dtype=np.int64)
    for t in range(n):
        p[t], r[t] = M[0, 0], M[0, 1]
        M = (M @ A) % q
    return p, r

# ---------- 1. depth-6 eight-phase team ----------
k = 6; q = 3 ** k; order = 8 * 3 ** (k - 1)
T = [0, 11, 502, 510, 737, 777, 1820, 1842]
p, r = first_rows(k, order)
a = np.repeat(np.arange(q, dtype=np.int64), q); b = np.tile(np.arange(q, dtype=np.int64), q)
sig = np.zeros(q * q, dtype=np.int64)
for t in T:
    sig = sig * 7 + ((p[t] * a + r[t] * b) % q) % 7
ok('depth 6: eight phases give 531,441 distinct histories', len(np.unique(sig)) == q * q)
w = q % 7  # = 1
passing = np.ones(q * q, dtype=bool); passing[0] = False
for t in T:
    d = ((p[t] * a + r[t] * b) % q) % 7
    passing &= (d == 0) | (d == w)
ok('depth 6: no nonzero difference passes the criterion', not passing.any())

# ---------- 4. wrap feasibility for the best seven-phase team ----------
T7 = [0, 342, 773, 1134, 1350, 1649, 1755]
passing = np.ones(q * q, dtype=bool); passing[0] = False
for t in T7:
    d = ((p[t] * a + r[t] * b) % q) % 7
    passing &= (d == 0) | (d == w)
P = np.flatnonzero(passing)
ok('seven-phase team: 4 passing differences', len(P) == 4)
U = [(p[t] * a + r[t] * b) % q for t in T7]
colliding = []
for idx in P:
    da, db = idx // q, idx % q
    same = np.ones(q * q, dtype=bool)
    for j, t in enumerate(T7):
        dl = (p[t] * da + r[t] * db) % q
        same &= ((U[j] + dl) % q) % 7 == U[j] % 7
    colliding.append(int(same.sum()))
print('  passing differences', [(int(i // q), int(i % q)) for i in P], 'states colliding with x + d:', colliding)
ok('each passing difference yields actual collisions (wrap feasible)', all(c > 0 for c in colliding))
sig7 = np.zeros(q * q, dtype=np.int64)
for t in T7:
    sig7 = sig7 * 7 + ((p[t] * a + r[t] * b) % q) % 7
_, cnt = np.unique(sig7, return_counts=True)
pairs = int((cnt * (cnt - 1) // 2).sum())
print('  seven-phase team: colliding pairs', pairs)
ok('colliding pairs = half the ordered collisions over the 4 differences', 2 * pairs == sum(colliding))

# ---------- 2. C-R3a closed formula vs BFS for every state ----------
def bfs(k, ops):
    q = 3 ** k; N = q * q
    dist = np.full(N, -1, dtype=np.int64)
    seed = 2 * q + 5 % q
    dist[seed] = 0; front = np.array([seed]); d = 0
    while front.size:
        a, b = front // q, front % q
        nxt = []
        for o in ops:
            if o == 'A': na, nb = b, (a + b) % q
            elif o == 'V': na, nb = 2 * a % q, 2 * b % q
            elif o == 'C': na, nb = 3 * a % q, 3 * b % q
            elif o == 'S': na, nb = a, (3 * a + b) % q
            nxt.append(na * q + nb)
        nxt = np.unique(np.concatenate(nxt))
        nxt = nxt[dist[nxt] < 0]
        d += 1; dist[nxt] = d; front = nxt
    return dist

def formula(k):
    """ChatGPT's distance: layer r = 3-adic valuation; d = r + d_prim at depth k - r; zero needs k."""
    q = 3 ** k; N = q * q
    out = np.full(N, -1, dtype=np.int64)
    for rr in range(k):
        kk = k - rr; qq = 3 ** kk; h = 3 ** (kk - 1)
        # enumerate x = A^t V^s x0 mod 3^kk, 0 <= t < 8h, 0 <= s < h
        x0 = np.array([2 % qq, 5 % qq], dtype=np.int64)
        A = np.array([[0, 1], [1, 1]], dtype=np.int64)
        At = np.zeros((8 * h, 2), dtype=np.int64); v = x0.copy()
        for t in range(8 * h):
            At[t] = v; v = (A @ v) % qq
        for s in range(h):
            sc = pow(2, s, qq)
            pts = (At * sc) % qq
            t = np.arange(8 * h)
            dd = np.where(t < 4 * h, t + s, t + s - 3 * h) + rr
            # lift: states 3^rr * y mod 3^k, y = pts mod 3^kk -> (3^rr * y) is well defined mod 3^k
            ya, yb = (pts[:, 0] * 3 ** rr) % q, (pts[:, 1] * 3 ** rr) % q
            out[ya * q + yb] = dd
    out[0] = k
    return out

for kk in range(1, 7):
    D = bfs(kk, 'AVC'); F = formula(kk)
    ok(f'k={kk}: formula equals BFS distance at all {9**kk} states; max {F.max()} = 2*3^k-2',
       (F >= 0).all() and np.array_equal(D, F) and F.max() == 2 * 3 ** kk - 2)

# ---------- 3. C-R3b lower bound ----------
acs = [7, 10, 12, 16, 20, 23, 26]
for kk in range(1, 8):
    d = 0
    while (3 ** (d + 1) - 1) // 2 < 9 ** kk:
        d += 1
    ok(f'k={kk}: counting lower bound {d} <= ACS diameter {acs[kk-1]}', d <= acs[kk - 1] and d >= 2 * kk)
for kk in range(1, 6):
    ok(f'k={kk}: ACS diameter by BFS = {acs[kk-1]}', bfs(kk, 'ACS').max() == acs[kk - 1])

print(f'{sum(R)} of {len(R)} checks passed')
sys.exit(0 if all(R) else 1)
