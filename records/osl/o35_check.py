"""O-35: the memory classes of the limit. Memories g: W_k -> Z/3^k modulo coboundaries are classified by orbit sums (paper
Theorem 6.1). Lifting g' = iota o g o pi (iota(s) = 3s) maps depth k to k + 1 (Theorem 20.1). Claim: the direct limit of these
lifting maps is the Pruefer group Z(3^inf) = Q_3/Z_3, carried by the still point: after k lifts a memory's class depends on
its still-point value s alone, which survives as 3^j s, injectively. Checked on random memories, k = 1..3, lifted up to depth 5."""
import random, sys
def orbits(q):
    seen = {}; orbs = []
    for a in range(q):
        for b in range(q):
            if (a, b) in seen: continue
            x = (a, b); O = []
            while x not in seen: seen[x] = len(orbs); O.append(x); x = (x[1], (x[0] + x[1]) % q)
            orbs.append(O)
    return orbs
ORB = {k: orbits(3 ** k) for k in range(1, 6)}
def sums(g, k):
    q = 3 ** k; return [sum(g[x] for x in O) % q for O in ORB[k]]
def lift(g, k):
    q = 3 ** (k + 1); return {x: (3 * g[(x[0] % 3 ** k, x[1] % 3 ** k)]) % q for O in ORB[k + 1] for x in O}
rng = random.Random(42); R = []
for k in range(1, 4):
    for trial in range(5):
        g = {x: rng.randrange(3 ** k) for O in ORB[k] for x in O}
        s0 = g[(0, 0)]; g0 = {x: (s0 if x == (0, 0) else 0) for x in g}; gg, hh = g, g0
        for j in range(1, 6 - k):
            gg = lift(gg, k + j - 1); hh = lift(hh, k + j - 1); S = sums(gg, k + j); H = sums(hh, k + j)
            still = S[[i for i, O in enumerate(ORB[k + j]) if O == [(0, 0)]][0]]
            R.append(still == (3 ** j * s0) % 3 ** (k + j))
            if j >= k: R.append(S == H)      # after k lifts the class depends on the still-point value alone
    # injectivity: distinct still-point values stay distinct after lifting
    for s1 in range(3 ** k):
        for s2 in range(s1 + 1, 3 ** k): R.append((3 * s1) % 3 ** (k + 1) != (3 * s2) % 3 ** (k + 1))
ok = all(R); print('still point survives as 3^j s, injectively; after k lifts the class depends on it alone:', 'PASS' if ok else 'FAIL', len(R), 'checks')
sys.exit(0 if ok else 1)
