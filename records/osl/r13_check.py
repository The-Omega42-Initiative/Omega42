"""R-13 check: the golden split of E8 under the law (MF-74; paper candidate).
Uses tools/bridges.py's exact construction: the E8 Gram matrix G (form 2 Tr((phi/sqrt5)<x, y>)) and the law's matrix M.
Run from the repository root (main). Exact integer arithmetic except where marked (floats for the H4 shells)."""
import os, sys
sys.path.insert(0, os.path.join(os.getcwd(), 'tools'))
import bridges as br
from collections import Counter
R = []
def ok(n, c): R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n)
I, B, Bq, res = br.e8_icosian(); G = res['phi/sqrt5'][2]
T = lambda X: [list(r) for r in zip(*X)]
M = T([br.solve_int(B, br.coords(tuple(br.PHI * c for c in x))) for x in Bq])
mm = br.matmul
ok('M^2 = M + I (the law on E8, MF-74)', mm(M, M) == br.matadd(M, br.ident(8)))
ok('M is self-adjoint for the E8 form: G M = M^T G', mm(G, M) == mm(T(M), G))
roots = br.short_vectors(G, 2); ok('240 roots of norm 2', len(roots) == 240)
S = [[sum(r[i] * r[j] for r in roots) for j in range(8)] for i in range(8)]
ok('tight frame: sum over roots of r r^T G = 60 I', mm(S, G) == [[60 * (i == j) for j in range(8)] for i in range(8)])
MS = mm(mm(M, S), T(M)); M2 = mm(M, M)
ok('after the law: sum of (Mr)(Mr)^T G = 60 M^2', mm(MS, G) == [[60 * x for x in r] for r in M2])
trM = sum(M[i][i] for i in range(8)); trM2 = sum(M2[i][i] for i in range(8)); M4 = mm(M2, M2); trM4 = sum(M4[i][i] for i in range(8))
ok('tr M = 4, tr M^2 = 12: eigenvalues phi and -1/phi, four each', trM == 4 and trM2 == 12)
from fractions import Fraction as Fr
# K = (1/240) sum (Mr)(Mr)^T G = M^2/4; deficit tr((K - tr(K)/8 I)^2) = tr(M^4)/16 - tr(M^2)^2/(16*8)
deficit = Fr(trM4, 16) - Fr(trM2 * trM2, 16 * 8)
ok('isotropy deficit of the transformed root frame = 5/8 exactly (ChatGPT)', deficit == Fr(5, 8))
# H4 shells (floats): project each root on the phi-eigenspace, P+ = (M + phi^-1 I)/sqrt5
phi = (1 + 5 ** .5) / 2
def norm2(v): return sum(v[i] * G[i][j] * v[j] for i in range(8) for j in range(8))
shell = Counter()
for r in roots:
    p = [(sum(M[i][j] * r[j] for j in range(8)) + r[i] / phi) / 5 ** .5 for i in range(8)]
    shell[round(norm2(p), 6)] += 1
print('  squared lengths of the phi-projections of the 240 roots:', dict(shell))
ok('the phi-projections form two shells of 120 roots each, of squared lengths 2 phi/sqrt5 and 2/(phi sqrt5), ratio phi^2', len(shell) == 2 and set(shell.values()) == {120}
   and abs(max(shell) / min(shell) - phi * phi) < 1e-5 and abs(max(shell) - 2 * phi / 5 ** .5) < 1e-5)
# each shell is a 600-cell: normalized inner products lie in {+-1, +-phi/2, +-1/2, +-1/(2 phi), 0}
P = []
for r in roots:
    p = [(sum(M[i][j] * r[j] for j in range(8)) + r[i] / phi) / 5 ** .5 for i in range(8)]
    P.append(p)
def ip(u, v): return sum(u[i] * G[i][j] * v[j] for i in range(8) for j in range(8))
big = [p for p in P if norm2(p) > 1]; L = norm2(big[0])
allowed = [1, -1, phi / 2, -phi / 2, .5, -.5, 1 / (2 * phi), -1 / (2 * phi), 0]
vals = Counter()
for u in big[:30]:
    for v in big: vals[min(allowed, key=lambda a: abs(ip(u, v) / L - a))] += 1 if min(abs(ip(u, v) / L - a) for a in allowed) < 1e-9 else 10 ** 6
ok('each shell is a 600-cell (H4): normalized inner products in {+-1, +-phi/2, +-1/2, +-1/(2 phi), 0}, 12 nearest neighbors', sum(vals.values()) == 30 * 120 and vals[phi / 2] == 30 * 12)
print('%d of %d checks passed' % (sum(R), len(R))); sys.exit(0 if all(R) else 1)
