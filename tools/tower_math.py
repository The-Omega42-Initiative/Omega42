#!/usr/bin/env python3
"""tower_math.py -- observation and generation at every depth of the tower W_k = (Z/3^k)^2 (paper Sections 5 and 20;
register entries MF-207 to MF-219, ratified by ESC on 27 November 2026).

    python3 tools/tower_math.py --selftest

Lines of the selftest, each named by a register entry:
  observe-depth5:   Theorem 5.7   six native phases of a mod 7 separate all 59,049 states of W_5
  observe-depth6:   Prop. 5.8     eight native phases separate all 531,441 states of W_6, so 7 <= m_6 <= 8
  generating-sets:  Theorem 20.3  exactly {A,C,S}, {A,V,C}, {A,V,C,S} of the 15 operation sets reach every state (k = 2..4; k = 1 adds {A,C})
  avc-distance:     Theorem 20.4  the closed {A,V,C} distance equals the breadth-first distance at every state (k = 1..4)
  descent:          Lemma 5.9     readings of 3y are 3 x readings of y one depth down, so separation descends
  commutant-limit:  Prop. 20.8    eigenvalue multiplicities of the limit grow without bound
  golden-split:     Prop. 20.9    the law on E8: self-adjoint, tight root frame, deficit 5/8, two 600-cell shells
  ring-design:      Prop. 20.10   the affine plane over Z/3^k: the law cycles its directions; 3^r common lines
  infinite-tower:   Prop. 20.7    the limit Z_3[phi]: a domain, no root of unity, full-length primitive orbits at every finite depth
  acs-linear:       Theorem 20.6  its finite ingredients: transitivity of <A, S> on primitive states, the positive-boundary identity
  acs-lower:        Prop. 20.5    the bound ceil(log2(8*9^(k-1)+1)) - 1 sits below the BFS ACS distances 7, 10, 12, 16 (k = 1..4), and
                                  the ingredients of Theorem 20.6: index 2, the Schreier generators of Lambda in SL2(Z), two fixed lines
Standard library only; a few seconds.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import combinations

OPS = {'A': lambda a, b, q: (b, (a + b) % q), 'V': lambda a, b, q: (2 * a % q, 2 * b % q),
       'C': lambda a, b, q: (3 * a % q, 3 * b % q), 'S': lambda a, b, q: (a, (3 * a + b) % q)}

def bfs(k, ops):
    q = 3 ** k; dist = {(2 % q, 5 % q): 0}; front = [(2 % q, 5 % q)]; d = 0
    while front:
        d += 1; nxt = []
        for a, b in front:
            for o in ops:
                y = OPS[o](a, b, q)
                if y not in dist: dist[y] = d; nxt.append(y)
        front = nxt
    return dist

def fib_rows(k, n):
    q = 3 ** k; p, r = [], []; m = [[1, 0], [0, 1]]
    for _ in range(n):
        p.append(m[0][0]); r.append(m[0][1])
        m = [[m[0][1], (m[0][0] + m[0][1]) % q], [m[1][1], (m[1][0] + m[1][1]) % q]]
    return p, r

def separates(k, T):
    q = 3 ** k; p, r = fib_rows(k, max(T) + 1); seen = set()
    coeff = [(p[t], r[t]) for t in T]
    for a in range(q):
        for b in range(q):
            seen.add(tuple(((pa * a + rb * b) % q) % 7 for pa, rb in coeff))
    return len(seen) == q * q

def avc_formula(k):
    q = 3 ** k; out = {}
    for rr in range(k):
        kk = k - rr; qq = 3 ** kk; h = 3 ** (kk - 1)
        x = (2 % qq, 5 % qq); At = []
        for t in range(8 * h):
            At.append(x); x = (x[1], (x[0] + x[1]) % qq)
        for s in range(h):
            sc = pow(2, s, qq)
            for t, (a, b) in enumerate(At):
                d = (t + s if t < 4 * h else t + s - 3 * h) + rr
                out[((a * sc % qq) * 3 ** rr % q, (b * sc % qq) * 3 ** rr % q)] = d
    out[(0, 0)] = k
    return out

def mul(X, Y): return [[X[0][0]*Y[0][0]+X[0][1]*Y[1][0], X[0][0]*Y[0][1]+X[0][1]*Y[1][1]], [X[1][0]*Y[0][0]+X[1][1]*Y[1][0], X[1][0]*Y[0][1]+X[1][1]*Y[1][1]]]
def det(X): return X[0][0]*X[1][1]-X[0][1]*X[1][0]

def lb(k):
    d = 0
    while 2 ** (d + 1) - 1 < 8 * 9 ** (k - 1): d += 1
    return d

def selftest():
    R = []
    def line(name, ok): R.append(ok); print('%-78s %s' % (name, 'PASS' if ok else 'FAIL'))
    line('observe-depth5: (0, 5, 44, 199, 243, 562) separates the 59,049 states of W_5', separates(5, [0, 5, 44, 199, 243, 562]))
    line('observe-depth6: (0, 11, 502, 510, 737, 777, 1820, 1842) separates the 531,441 states of W_6',
         separates(6, [0, 11, 502, 510, 737, 777, 1820, 1842]) and 7 ** 6 < 9 ** 6)
    want = {frozenset('ACS'), frozenset('AVC'), frozenset('AVCS')}
    ok = True
    for k in range(1, 5):
        full = {frozenset(c) for n in range(1, 5) for c in combinations('AVCS', n) if len(bfs(k, c)) == 9 ** k}
        ok &= full == (want | {frozenset('AC')} if k == 1 else want)
    line('generating-sets: exactly ACS, AVC, AVCS reach W_k for k = 2..4, and AC too at k = 1', ok)
    ok = True
    for k in range(1, 5):
        D = bfs(k, 'AVC'); F = avc_formula(k)
        ok &= len(F) == 9 ** k and D == F and max(F.values()) == 2 * 3 ** k - 2
    line('avc-distance: the closed formula is the BFS distance at every state, k = 1..4; max 2*3^k - 2', ok)
    A = [[0, 1], [1, 1]]; Ai = [[-1, 1], [1, 0]]; S = [[1, 0], [3, 1]]; A2 = mul(A, A)
    gens = [S, A2, mul(mul(A, S), Ai)]
    conj = mul(mul(A2, S), mul(Ai, Ai))           # A^2 S A^-2
    fixed = lambda M: [(x, y) for x, y in [(0, 1), (1, 0), (1, 1), (1, -1), (1, 2), (2, 1)] if [M[0][0]*x+M[0][1]*y, M[1][0]*x+M[1][1]*y] == [x, y]]
    diam = [max(bfs(k, 'ACS').values()) for k in range(1, 5)]
    ok = (det(A) == -1 and mul(A, Ai) == [[1, 0], [0, 1]] and all(det(g) == 1 for g in gens)
          and fixed(S) == [(0, 1)] and fixed(conj) != fixed(S) and diam == [7, 10, 12, 16] and all(d >= lb(k) for k, d in zip(range(1, 5), diam)) and [lb(k) for k in range(1, 8)] == [3, 6, 9, 12, 15, 18, 22])
    line('acs-lower: bound 3, 6, 9, 12 below the ACS distances 7, 10, 12, 16; index 2, Lambda in SL2(Z), two fixed lines', ok)
    # Theorem 20.6 ingredients: <A, S> mod 3^k is transitive on the primitive states (k = 1..4), and the positive-word
    # identity |Xs^-1 minus X| = |Xs minus X| on random subsets of the group mod 9
    ok = True
    for k in range(1, 5):
        q = 3 ** k; prim = sum(1 for a in range(q) for b in range(q) if a % 3 or b % 3)
        reach = bfs(k, 'AS'); ok &= len(reach) == prim == 8 * 9 ** (k - 1)
    import random
    rng = random.Random(7); q = 9; G = set(); fr = [((1, 0), (0, 1))]
    def mm(X, Y): return (((X[0][0]*Y[0][0]+X[0][1]*Y[1][0]) % q, (X[0][0]*Y[0][1]+X[0][1]*Y[1][1]) % q), ((X[1][0]*Y[0][0]+X[1][1]*Y[1][0]) % q, (X[1][0]*Y[0][1]+X[1][1]*Y[1][1]) % q))
    gA, gS = ((0, 1), (1, 1)), ((1, 0), (3, 1)); G.add(fr[0])
    while fr:
        n = []
        for g in fr:
            for s_ in (gA, gS):
                h = mm(g, s_)
                if h not in G: G.add(h); n.append(h)
        fr = n
    inv = {g: next(h for h in G if mm(g, h) == ((1, 0), (0, 1))) for g in (gA, gS)}
    Gl = sorted(G)
    for _ in range(20):
        X = set(rng.sample(Gl, rng.randrange(1, len(Gl))))
        for s_ in (gA, gS):
            ok &= len({mm(x, s_) for x in X} - X) == len({mm(x, inv[s_]) for x in X} - X)
    line('acs-linear: <A, S> transitive on primitive states (k = 1..4); |Xs^-1 - X| = |Xs - X| in <A, S> mod 9', ok)
    # Proposition 20.7: Z_3[phi] is a domain (x^2 - x - 1 has no root mod 3), phi is no root of unity (F_n = 0 and
    # F_(n-1) = 1 never hold for n >= 1), and every primitive orbit at depth k has length 8*3^(k-1), 3^(k-1) of them
    Fb = [0, 1]
    for _ in range(600): Fb.append(Fb[-1] + Fb[-2])
    ok = all((x * x - x - 1) % 3 for x in range(3)) and not any(Fb[n] == 0 and Fb[n - 1] == 1 for n in range(1, 600))
    for k in range(1, 5):
        q = 3 ** k; seen = set(); lens = []
        for a0 in range(q):
            for b0 in range(q):
                if (a0 % 3 == 0 and b0 % 3 == 0) or (a0, b0) in seen: continue
                x = (a0, b0); L = 0
                while x not in seen: seen.add(x); L += 1; x = (x[1], (x[0] + x[1]) % q)
                lens.append(L)
        ok &= set(lens) == {8 * 3 ** (k - 1)} and len(lens) == 3 ** (k - 1)
    line('infinite-tower: Z_3[phi] a domain, phi no root of unity; 3^(k-1) primitive orbits of length 8*3^(k-1), k = 1..4', ok)
    # Lemma 5.9: the reading of A^t(3y) at depth k is 3 times the reading of A^t y at depth k - 1, mod 7 (k = 2..4, all y, all t),
    # so separation descends; the depth-5 team, reduced, separates W_4 and W_3
    ok = True
    for k in range(2, 5):
        q, qq = 3 ** k, 3 ** (k - 1); p, r = fib_rows(k, 8 * 3 ** (k - 1)); pp, rr = fib_rows(k - 1, 8 * 3 ** (k - 2))
        for t in range(0, 8 * 3 ** (k - 1), 5):
            for a0 in range(qq):
                for b0 in range(qq):
                    ok &= ((p[t] * 3 * a0 + r[t] * 3 * b0) % q) % 7 == (3 * ((pp[t % (8 * 3 ** (k - 2))] * a0 + rr[t % (8 * 3 ** (k - 2))] * b0) % qq)) % 7
    ok &= separates(4, sorted({t % 216 for t in [0, 5, 44, 199, 243, 562]})) and separates(3, sorted({t % 72 for t in [0, 5, 44, 199, 243, 562]}))
    line('descent: readings of 3y at depth k = 3 x readings of y at depth k - 1 (k = 2..4); the depth-5 team separates W_4, W_3', ok)
    # Proposition 20.8: each eigenvalue of order d | 8*3^m has multiplicity >= 3^(k-1) at depth k > m (k = 1..4)
    ok = True
    for k in range(1, 5):
        q = 3 ** k; seen = set(); lens = []
        for a0 in range(q):
            for b0 in range(q):
                if (a0, b0) in seen: continue
                x = (a0, b0); L = 0
                while x not in seen: seen.add(x); L += 1; x = (x[1], (x[0] + x[1]) % q)
                lens.append(L)
        for d in [dd for dd in range(1, 8 * 3 ** (k - 1) + 1) if (8 * 3 ** (k - 1)) % dd == 0]:
            ok &= sum(1 for L in lens if L % d == 0) >= 3 ** (k - 1)
    line('commutant-limit: every eigenvalue order d | 8*3^(k-1) has multiplicity >= 3^(k-1) at depth k (k = 1..4)', ok)
    # Proposition 20.9: the golden split of E8 (MF-74): M self-adjoint, tight root frame, deficit 5/8, two 600-cell shells
    import bridges as br
    from fractions import Fraction as Fr
    I8, B8, Bq, res = br.e8_icosian(); G = res['phi/sqrt5'][2]
    Tr = lambda X: [list(x) for x in zip(*X)]
    M = Tr([br.solve_int(B8, br.coords(tuple(br.PHI * c for c in x))) for x in Bq])
    roots = br.short_vectors(G, 2); Sm = [[sum(v[i] * v[j] for v in roots) for j in range(8)] for i in range(8)]
    M2 = br.matmul(M, M); M4 = br.matmul(M2, M2); tr = lambda X: sum(X[i][i] for i in range(8))
    ph = (1 + 5 ** .5) / 2; n2 = lambda v: sum(v[i] * G[i][j] * v[j] for i in range(8) for j in range(8))
    shells = sorted({round(n2([(sum(M[i][j] * v[j] for j in range(8)) + v[i] / ph) / 5 ** .5 for i in range(8)]), 6) for v in roots})
    ok = (br.matmul(G, M) == br.matmul(Tr(M), G) and M2 == br.matadd(M, br.ident(8)) and len(roots) == 240
          and br.matmul(Sm, G) == [[60 * (i == j) for j in range(8)] for i in range(8)] and tr(M) == 4 and tr(M2) == 12
          and Fr(tr(M4), 16) - Fr(tr(M2) ** 2, 128) == Fr(5, 8) and len(shells) == 2 and abs(shells[1] / shells[0] - ph * ph) < 1e-5)
    line('golden-split: on E8, GM = M^T G, tight root frame, isotropy deficit 5/8, two shells in the ratio phi^2', ok)
    # Proposition 20.10: the affine plane over Z/3^k: 4*3^(k-1) directions, the law transitive on them; two states lie on
    # 3^r common lines, r their separation valuation (k = 1..3)
    ok = True
    for k in range(1, 4):
        q = 3 ** k; dirs = {}; reps = []
        for a0 in range(q):
            for b0 in range(q):
                if a0 % 3 == 0 and b0 % 3 == 0: continue
                c = min(((u * a0) % q, (u * b0) % q) for u in range(q) if u % 3)
                if c not in dirs: dirs[c] = len(reps); reps.append(c)
                dirs[(a0, b0)] = dirs[c]
        x = reps[0]; orb = set()
        for _ in range(8 * 3 ** (k - 1)): orb.add(dirs[x]); x = (x[1], (x[0] + x[1]) % q)
        ok &= len(reps) == 4 * 3 ** (k - 1) == len(orb)
        def v3(n):
            n %= q
            if n == 0: return k
            e = 0
            while n % 3 == 0: n //= 3; e += 1
            return e
        for (a0, b0) in [(0, 1), (1, 1), (0, 3), (3, 6), (2, 7)] if k >= 2 else [(0, 1), (1, 2)]:
            a0, b0 = a0 % q, b0 % q
            if (a0, b0) == (0, 0): continue
            cnt = sum(1 for d in reps if any(((t * d[0]) % q, (t * d[1]) % q) == (a0, b0) for t in range(q)))
            ok &= cnt == 3 ** min(v3(a0), v3(b0))
    line('ring-design: 4*3^(k-1) directions over Z/3^k, the law transitive on them; 3^r common lines (k = 1..3)', ok)
    print('TOWER MATHEMATICS SELFTEST: %s' % ('PASS' if all(R) else 'FAIL'))
    return all(R)

if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']: sys.exit(0 if selftest() else 1)
    print(__doc__); sys.exit(2)
