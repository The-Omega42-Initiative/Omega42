"""O-30 settled (paper, Theorem 5.7 and Lemma 5.6): six native phases of the aperture a mod 7 separate all 59,049 states of W_5 (Claude, 27 November 2026).

Statement. At depth 5 (W_5 = (Z/243)^2, the law A = [[0,1],[1,1]] of order 648), the readings
r_t(x) = (A^t x).a mod 7 at the six phases T = (0, 5, 44, 199, 243, 562) take 59,049 distinct values: every state
is identified by its six readings. Since 7^5 = 16,807 < 59,049, no five readings can do so (Theorem 5.3), so six is
least, and the single native aperture attains the counting bound at depth 5 as it does at depths 2, 3 and 4
(Theorems 5.4, 5.7). Every shift T + s (mod 648) separates too, since A^s permutes the states.

Lemma 5.6 (difference criterion). Write d = y - x and delta_t = (A^t d).a in [0, 243). Then (A^t y).a = (A^t x).a + delta_t
or that minus 243, so r_t(y) = r_t(x) forces delta_t = 0 or 243 = 5 (mod 7). Hence if no nonzero d has
delta_t mod 7 in {0, 5} at every t in T, the readings at T separate W_5. (The converse fails: a difference can pass
the test at every phase yet never meet the wrap pattern a collision needs.)

Three independent certificates, each must hold:
  1. direct count: the 59,049 six-reading histories are distinct (pure Python, no numpy);
  2. the difference criterion: no nonzero difference has delta_t mod 7 in {0, 5} at all six phases (pure Python);
  3. the kernel (records/osl/kernel.js, under Node, where present) reports separation 59,049 for T at depth 5.
Refutation: one pair of distinct states with equal readings at the six phases.
Run: python3 o30_check.py [path/to/kernel.js]"""
import json, os, subprocess, sys
q, N = 243, 648
T = (0, 5, 44, 199, 243, 562)
R = []
def ok(name, c): R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + name)

def first_coords(x):
    """(A^t x).a for t = 0 .. N-1."""
    a, b, out = x[0], x[1], []
    for _ in range(N): out.append(a); a, b = b, (a + b) % q
    return out

# order: A^648 = I and no smaller power of the form 648/p is I
def apply(x, n):
    a, b = x
    for _ in range(n): a, b = b, (a + b) % q
    return (a, b)
ok('A^648 fixes (0, 1) and (1, 0); A^324 = -I and A^216 is not I', apply((0, 1), 648) == (0, 1) and apply((1, 0), 648) == (1, 0)
   and apply((0, 1), 324) == (0, q - 1) and apply((1, 0), 324) == (q - 1, 0) and apply((0, 1), 216) != (0, 1))

# 1. direct count
hist = set()
for a in range(q):
    for b in range(q):
        fc = first_coords((a, b))
        hist.add(tuple(fc[t] % 7 for t in T))
ok('direct count: %d distinct histories of %d states' % (len(hist), q * q), len(hist) == q * q)

# 2. difference criterion
bad = 0
for a in range(q):
    for b in range(q):
        if (a, b) == (0, 0): continue
        fc = first_coords((a, b))
        if all(fc[t] % 7 in (0, 5) for t in T): bad += 1
ok('difference criterion: %d nonzero differences pass the test at all six phases' % bad, bad == 0)
# the lemma's arithmetic: 243 = 5 mod 7
ok('243 = 5 (mod 7), the wrap term of the lemma', 243 % 7 == 5)

# 3. the kernel
kp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kernel.js')
if os.path.exists(kp):
    r = subprocess.run(['node', '-e', 'const K=require(process.argv[1]);console.log(K.separation(%s,5))' % json.dumps(list(T)), kp],
                       capture_output=True, text=True, timeout=900)
    ok('kernel: separation(T, 5) = %s' % r.stdout.strip(), r.stdout.strip() == str(q * q))
else:
    print('SKIP kernel: records/osl/kernel.js is not present (research record R-01, awaiting verification)')

# contrast: the best set published before (paper, Theorem 5.4) leaves eight pairs
old = (141, 155, 211, 282, 338, 409)
hold = set()
for a in range(q):
    for b in range(q):
        fc = first_coords((a, b)); hold.add(tuple(fc[t] % 7 for t in old))
ok('the earlier set (141, 155, 211, 282, 338, 409) gives %d, as published (59,041)' % len(hold), len(hold) == 59041)
print('%d of %d checks PASS' % (sum(R), len(R)))
sys.exit(0 if all(R) else 1)
