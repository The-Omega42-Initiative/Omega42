"""OmegaSL Tier III extension: the operations that the mathematical paper (docs/OMEGA42_MATHEMATICAL_PAPER.md, Sections 17 to 23) adds
to the Omega42 Structural Language, with exact reference semantics, the typing of the Tier 1 operators, and worked examples.
Proposed (CONSTRUCTED as language, EXACT as arithmetic); the canonical language stays Companion Part 214 and tools/osl.py.

    python3 records/osl/tier3_ext.py --examples     # worked phrases with their computed results
    python3 records/osl/tier3_ext.py --selftest     # exhaustive checks of every type and identity used
Standard library only.
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'tools'))
import osl
M = 9
S81 = [(a, b) for a in range(M) for b in range(M)]
A = lambda s: osl.A(s, 1)

# --- Tier 1 operator types (Section 23.1): LAWFUL-REVERSIBLE, LAWFUL-ACTUALIZING, EXTERNAL ---------------------------------
def optype(op):
    f = osl.OPS[op]
    lawful = all(f(A(s)) == A(f(s)) for s in S81)
    inj = len({f(s) for s in S81}) == 81
    return 'LAWFUL-REVERSIBLE' if lawful and inj else 'LAWFUL-ACTUALIZING' if lawful else 'EXTERNAL' if inj else 'EXTERNAL-ACTUALIZING'

# --- state operations across depth (Sections 3, 19) -------------------------------------------------------------------------
def REDUCE(s, k=2):                        # W_k -> W_(k-1)
    m = 3**(k - 1); return (s[0] % m, s[1] % m)
def LIFT(s, k=2):                          # the nine preimages in W_(k+1)
    m = 3**k; return [(s[0] + m * i, s[1] + m * j) for i in range(3) for j in range(3)]
def period(s, m=M):
    n, t = 1, ((s[1]) % m, (s[0] + s[1]) % m)
    while t != s: t = (t[1] % m, (t[0] + t[1]) % m); n += 1
    return n
def ORBIT(s, m=M):
    o, t = [s], ((s[1]) % m, (s[0] + s[1]) % m)
    while t != s: o.append(t); t = (t[1] % m, (t[0] + t[1]) % m)
    return o

# --- coupling (Section 17.2) -------------------------------------------------------------------------------------------------
def PAIR(x, y, m=M): return (x[0] * y[1] - x[1] * y[0]) % m
def COUPLE(x, y, m=M): b = PAIR(x, y, m); return ((x[0] + b * y[0]) % m, (x[1] + b * y[1]) % m)

# --- memory (Sections 6, 20) -------------------------------------------------------------------------------------------------
def MEMORY(g, m=M):                        # the class of a memory g: its orbit-sum vector, one entry per orbit, in census order
    seen, out = set(), []
    for s in sorted(S81 if m == M else [(a, b) for a in range(m) for b in range(m)]):
        if s in seen: continue
        o = ORBIT(s, m); seen.update(o); out.append((len(o), sum(g(t) for t in o) % m))
    return out
def MEMORY_LIFT(k): c = (3**k + 1) // 2; return dict(kernel=3**(c - 1), image=3**(k * c - c + 1))

# --- fields: refinement, coarsening, detail (Section 19) ---------------------------------------------------------------------
def REFINE(v, k=2):                        # dict state -> value on W_k  ->  W_(k+1)
    m, M1 = 3**k, 3**(k + 1); return {(a, b): v[(a % m, b % m)] / 3 for a in range(M1) for b in range(M1)}
def COARSEN(w, k=2):                       # adjoint of REFINE
    m = 3**k; out = {s: 0.0 for s in [(a, b) for a in range(m) for b in range(m)]}
    for (a, b), x in w.items(): out[(a % m, b % m)] += x / 3
    return out
def DETAIL(w, k=2):
    back = REFINE(COARSEN(w, k), k); return {s: w[s] - back[s] for s in w}

# --- transformations, worlds, inquiry (Sections 20 to 22) --------------------------------------------------------------------
def COMMUTANT(k): return (5 * 27**k + 8) // 13
def WORLD(p, k=1):                         # comparative only: the census of the law modulo p^k (never the substrate; L-423)
    m = p**k; seen, cen = set(), {}
    for a in range(m):
        for b in range(m):
            if (a, b) in seen: continue
            o = ORBIT((a, b), m); seen.update(o); cen[len(o)] = cen.get(len(o), 0) + 1
    return dict(sorted(cen.items()))
def INQUIRE(C, view=lambda s: s[0] % 7, phases=range(24)):
    """Greedy minimax: the phase whose readings split the candidate set C most evenly in the worst case."""
    def worst(t):
        cnt = {}
        for s in C: cnt[view(osl.A(s, t))] = cnt.get(view(osl.A(s, t)), 0) + 1
        return max(cnt.values())
    return min(phases, key=worst)
def KNOWLEDGE(n_before, n_after): return math.log2(n_before / n_after)

def examples():
    P0 = osl.STATE['P0']
    print('Tier 1 types:', {op: optype(op) for op in osl.OPS})
    print('P0 =', P0, '| P0 C =', osl.say('P0 C'), osl.NAME[osl.say('P0 C')], '| P0 C C =', osl.say('P0 C C'), '  (actualization: Theorem 17.4)')
    print('P0 N C =', osl.say('P0 N C'), '= P0 C N =', osl.say('P0 C N'), '  (C is lawful)')
    print('P0 S N =', osl.say('P0 S N'), '!= P0 N S =', osl.say('P0 N S'), '  (S is external)')
    print('LIFT P0 ->', LIFT(P0), '| periods mod 27:', sorted({period(t, 27) for t in LIFT(P0)}))
    y = (1, 0); print('PAIR P0 (1,0) =', PAIR(P0, y), '| COUPLE =', COUPLE(P0, y), '| after two steps both ways:', COUPLE(osl.A(P0, 2), osl.A(y, 2)), osl.A(COUPLE(P0, y), 2))
    print('MEMORY of g(a,b)=a:', MEMORY(lambda s: s[0]), '  (a coboundary: all sums 0)')
    print('MEMORY_LIFT 2 -> 3:', MEMORY_LIFT(2), '| COMMUTANT depth 1..4:', [COMMUTANT(k) for k in range(1, 5)])
    print('WORLD 7:', WORLD(7), '| WORLD 11:', WORLD(11), '| WORLD 3, 2:', WORLD(3, 2))
    C = list(S81); hidden = P0; steps = []
    while len(C) > 1:
        t = INQUIRE(C); r = osl.A(hidden, t)[0] % 7; C = [s for s in C if osl.A(s, t)[0] % 7 == r]; steps.append((t, r, len(C)))
    print('INQUIRE: hidden P0 found in', len(steps), 'readings', steps, '| KNOWLEDGE =', round(KNOWLEDGE(81, 1), 5), 'bits')

def selftest():
    ok = []
    T = {op: optype(op) for op in osl.OPS}
    ok.append(T == {'N': 'LAWFUL-REVERSIBLE', 'R': 'LAWFUL-REVERSIBLE', 'X': 'LAWFUL-REVERSIBLE', 'V': 'LAWFUL-REVERSIBLE', 'C': 'LAWFUL-ACTUALIZING',
                    'S': 'EXTERNAL', 'Y': 'LAWFUL-REVERSIBLE', 'H': 'LAWFUL-REVERSIBLE', 'F': 'LAWFUL-REVERSIBLE'})
    ok.append(all(osl.OPS['C'](osl.OPS['C'](s)) == (0, 0) for s in S81))
    ok.append(all(REDUCE(t, 3) == s for s in S81 for t in LIFT(s)) and len({t for s in S81 for t in LIFT(s)}) == 729)
    ok.append(all(COUPLE(osl.A(x, 2), osl.A(y, 2)) == osl.A(COUPLE(x, y), 2) for x in S81 for y in S81))
    ok.append(all(s == 0 for _, s in MEMORY(lambda s: s[0])))
    ok.append(MEMORY_LIFT(2) == dict(kernel=81, image=729) and COMMUTANT(2) == 281)
    ok.append(WORLD(7) == {1: 1, 16: 3} and WORLD(11) == {1: 1, 5: 2, 10: 11})
    v = {s: (s[0] * 7 + s[1] * 3) % 5 - 2.0 for s in S81}; w = REFINE(v)
    ok.append(abs(sum(x * x for x in w.values()) - sum(x * x for x in v.values())) < 1e-9 and all(abs(COARSEN(w)[s] - v[s]) < 1e-9 for s in S81))
    d = DETAIL({s: float((s[0] * s[1]) % 5) for s in [(a, b) for a in range(27) for b in range(27)]})
    ok.append(all(abs(x) < 1e-9 for x in COARSEN(d).values()))
    worst = 0
    for h in S81:
        C, n = list(S81), 0
        while len(C) > 1:
            t = INQUIRE(C); r = osl.A(h, t)[0] % 7; C = [s for s in C if osl.A(s, t)[0] % 7 == r]; n += 1
        worst = max(worst, n)
    ok.append(worst == 3)
    print('TIER III EXTENSION SELFTEST: %d checks, %d failed' % (len(ok), ok.count(False)))
    return all(ok)

if __name__ == '__main__':
    if '--examples' in sys.argv: examples()
    else: sys.exit(0 if selftest() else 1)
