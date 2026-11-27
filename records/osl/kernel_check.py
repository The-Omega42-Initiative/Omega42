"""Independent check of the Omega42 mathematical kernel (records/osl/kernel.js), version 1, 27 November 2026.

Three sources must agree on every quantity: (1) the figures published in the paper (docs/OMEGA42_MATHEMATICAL_PAPER.md),
(2) a Python recomputation written separately from the kernel (harmonic multiplicities by numerical eigenvalues of the
shift, not by the orbit rule the kernel uses), and (3) the kernel itself, run under Node. Any disagreement fails the
check. Run: python3 records/osl/kernel_check.py   (exit 0: every check passes; needs node on the PATH)."""
import json, math, os, subprocess, sys
from itertools import combinations
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
R = []
def ok(name, cond):
    R.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name)

# ---- Python reference, written independently of kernel.js -------------------------------------------------------
def law(x, q): return (x[1], (x[0] + x[1]) % q)
def apply_n(x, n, q):
    for _ in range(n): x = law(x, q)
    return x
def py_orbits(q):
    seen, out = set(), []
    for a in range(q):
        for b in range(q):
            if (a, b) in seen: continue
            o, y = [], (a, b)
            while y not in seen: seen.add(y); o.append(y); y = law(y, q)
            out.append(o)
    return out
def py_census(q):
    c = {}
    for o in py_orbits(q): c[len(o)] = c.get(len(o), 0) + 1
    return c
def pisano(m):
    a, b, n = 0, 1 % m, 0
    while True:
        a, b, n = b, (a + b) % m, n + 1
        if (a, b) == (0, 1 % m): return n
def py_read(x, t, q): return apply_n(x, t, q)[0] % 7
def py_sep(phases, q):
    return len({tuple(py_read((a, b), t, q) for t in phases) for a in range(q) for b in range(q)})
def py_reach(ops, q, seed=(2, 5)):
    seed = (seed[0] % q, seed[1] % q)
    f = {'A': lambda a, b: (b, (a + b) % q), 'V': lambda a, b: (2 * a % q, 2 * b % q),
         'C': lambda a, b: (3 * a % q, 3 * b % q), 'S': lambda a, b: (a, (3 * a + b) % q)}
    dist = {seed: 0}; todo = deque([seed])
    while todo:
        x = todo.popleft()
        for o in ops:
            y = f[o](*x)
            if y not in dist: dist[y] = dist[x] + 1; todo.append(y)
    return len(dist), max(dist.values())
def py_mult_numeric(q):
    """Eigenvalue multiplicities of the shift (Uf)(x) = f(Ax) on functions on W_k, by numerical eigenvalues."""
    import numpy as np
    n = q * q; U = np.zeros((n, n))
    for a in range(q):
        for b in range(q):
            y = law((a, b), q); U[a * q + b, y[0] * q + y[1]] = 1.0
    N = 8 * q // 3
    ev = np.linalg.eigvals(U)
    m = [0] * N
    for z in ev: m[int(round((math.atan2(z.imag, z.real) / (2 * math.pi)) * N)) % N] += 1
    return m

# ---- The kernel, under Node ----------------------------------------------------------------------------------------
JS = r"""
const K = require(process.argv[1]);
const out = {};
out.version = K.VERSION;
out.order = [1,2,3,4,5].map(k => K.order(k));
out.census = [1,2,3,4,5].map(k => K.census(k));
out.orderMod = [7, 9, 11, 27].map(m => K.orderMod(m));
out.halfTurn = K.states(2).every(x => { const y = K.power(x, 12, 2); return y[0] === (9 - x[0]) % 9 && y[1] === (9 - x[1]) % 9; });
out.qAlt = [2,3].map(k => K.states(k).every(x => K.Q(K.step(x, Math.pow(3,k)), k) === (Math.pow(3,k) - K.Q(x, k)) % Math.pow(3,k)));
out.q2 = K.orbits(2).map(o => [o.length, (K.Q(o[0], 2) * K.Q(o[0], 2)) % 9]).sort((p, r) => p[0] - r[0] || p[1] - r[1]);
out.loop = K.canonicalLoop();
out.sep = [1,2,3,4,5,6].map(n => K.separation([...Array(n).keys()], 2));
let triples = 0; for (let a = 0; a < 24; a++) for (let b = a + 1; b < 24; b++) for (let c = b + 1; c < 24; c++) if (K.separation([a, b, c], 2) === 81) triples++;
out.triples = triples;
out.recon = K.states(2).every(x => { const r = K.reconstruct([0, 2, 5], K.history(x, [0, 2, 5], 2), 2); return r.length === 1 && r[0][0] === x[0] && r[0][1] === x[1]; });
out.reach = ['AVC', 'ACS', 'AVCS', 'A'].map(o => { const r = K.reach(o, 2); return [r.reached, r.depth]; });
out.reach3 = ['ACS', 'AVCS'].map(o => { const r = K.reach(o, 3); return [r.reached, r.depth]; });
out.mult2 = K.multiplicities(2); out.mult3 = K.multiplicities(3);
out.cat = K.states(2).every(x => { const y = K.catMap(x, 2); return y[0] === (x[0] + x[1]) % 9 && y[1] === (x[0] + 2 * x[1]) % 9; });
out.inverse = [2,3].map(k => K.states(k).every(x => { const y = K.back(K.step(x, Math.pow(3,k)), Math.pow(3,k)); return y[0] === x[0] && y[1] === x[1]; }));
out.negPower = K.states(2).every(x => { const y = K.power(K.power(x, 5, 2), -5, 2); return y[0] === x[0] && y[1] === x[1]; });
out.errors = [];
for (const bad of [() => K.modulus(0), () => K.modulus(7), () => K.reach('AX', 2), () => K.reconstruct([0, 1], [1], 2), () => K.orderMod(1)])
  { try { bad(); out.errors.push(false); } catch (e) { out.errors.push(e instanceof RangeError); } }
console.log(JSON.stringify(out));
"""

def main():
    kpath = os.path.join(HERE, 'kernel.js')
    try:
        r = subprocess.run(['node', '-e', JS, kpath], capture_output=True, text=True, timeout=600)
    except FileNotFoundError:
        print('FAIL node is not on the PATH'); return 1
    if r.returncode != 0:
        print('FAIL the kernel did not run:', r.stderr[:500]); return 1
    K = json.loads(r.stdout)

    # Theorem 3.1: order 8*3^(k-1); one fixed point and, for each j <= k, 3^(j-1) orbits of length 8*3^(j-1).
    for k in range(1, 6):
        q = 3 ** k
        want = {1: 1}
        for j in range(1, k + 1): want[8 * 3 ** (j - 1)] = 3 ** (j - 1)
        got_js = {int(L): n for L, n in K['census'][k - 1].items()}
        ok('depth %d: order %d (paper 8*3^(k-1) = %d)' % (k, K['order'][k - 1], 8 * 3 ** (k - 1)), K['order'][k - 1] == 8 * 3 ** (k - 1) == pisano(q))
        ok('depth %d: census %s, as Theorem 3.1 and the Python recount' % (k, dict(sorted(want.items()))), got_js == want == py_census(q))
        ok('depth %d: %d orbits = (3^k + 1)/2' % (k, sum(want.values())), sum(got_js.values()) == (3 ** k + 1) // 2)
    ok('order of A modulo 7, 9, 11, 27: 16, 24, 10, 72 (Theorems 21.1, 21.2)', K['orderMod'] == [16, 24, 10, 72] == [pisano(m) for m in (7, 9, 11, 27)])
    ok('A^12 = -I on W_2 (Theorem 2.2)', K['halfTurn'] and all(apply_n((a, b), 12, 9) == ((-a) % 9, (-b) % 9) for a in range(9) for b in range(9)))
    ok('Q(Ax) = -Q(x) at depths 2 and 3 (Theorem 2.3)', all(K['qAlt']))
    ok('(period, Q^2) names the five orbits: (1,0), (8,0), (24,1), (24,4), (24,7) (Theorem 2.3)', K['q2'] == [[1, 0], [8, 0], [24, 1], [24, 4], [24, 7]])
    paper_loop = [2, 5, 7, 3, 1, 4, 5, 9, 5, 5, 1, 6, 7, 4, 2, 6, 8, 5, 4, 9, 4, 4, 8, 3]
    y, py_loop = (2, 5), []
    for _ in range(24): py_loop.append(y[0] or 9); y = law(y, 9)
    ok('the canonical loop, as printed in the paper; its sum is 117', K['loop'] == paper_loop == py_loop and sum(paper_loop) == 117)
    ok('native aperture: 7, 49, 73, 77, 80, 81 states after 1 to 6 readings (Theorem 5.2)', K['sep'] == [7, 49, 73, 77, 80, 81] == [py_sep(range(n), 9) for n in range(1, 7)])
    py_triples = sum(py_sep(p, 9) == 81 for p in combinations(range(24), 3))
    ok('192 of the 2,024 phase triples separate all 81 states (Theorem 5.5)', K['triples'] == 192 == py_triples)
    ok('readings at phases 0, 2, 5 reconstruct every state of W_2 uniquely', K['recon'])
    want_reach = [(81, 16), (81, 10), (81, 6), (24, 23)]
    ok('reach from (2, 5) on W_2 under AVC, ACS, AVCS, A: %s' % want_reach, [tuple(x) for x in K['reach']] == want_reach == [py_reach(o, 9) for o in ('AVC', 'ACS', 'AVCS', 'A')])
    ok('reach on W_3 under ACS and AVCS agrees with the Python recount: %s' % K['reach3'], [tuple(x) for x in K['reach3']] == [py_reach(o, 27) for o in ('ACS', 'AVCS')])
    for k, key in ((2, 'mult2'), (3, 'mult3')):
        num = py_mult_numeric(3 ** k)
        ok('depth %d: harmonic multiplicities equal the numerical eigenvalues of the shift (sum %d, omega^0 has %d) (Theorem 4.1)' % (k, sum(num), num[0]),
           K[key] == num and sum(num) == 9 ** k and num[0] == (3 ** k + 1) // 2)
    ok('A^2 is the cat map [[1, 1], [1, 2]] (Theorem 8.1)', K['cat'])
    ok('the inverse law undoes the law at depths 2 and 3; negative powers invert positive ones', all(K['inverse']) and K['negPower'])
    ok('invalid input raises a RangeError in each of 5 cases', K['errors'] == [True] * 5)
    print('kernel version %s: %d of %d checks PASS' % (K['version'], sum(R), len(R)))
    return 0 if all(R) else 1

if __name__ == '__main__':
    sys.exit(main())
