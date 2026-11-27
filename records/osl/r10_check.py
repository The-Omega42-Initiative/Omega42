"""R-10 check: the inverse limit W_inf = Z_3^2 = Z_3[phi] (depth programme D-4).
(1) x^2 - x - 1 is irreducible mod 3, so Z_3[phi] is a domain (the unramified quadratic ring);
(2) phi is no root of unity: x^2 - x - 1 divides no x^n - 1 over Q (n <= 2000), so A has no periodic point but 0 on W_inf;
(3) the spectrum of A on L^2(W_inf) is the union of the finite spectra: at depth k the eigenvalue of order d has multiplicity
    #{orbits of W_k whose length d divides}; for each d dividing 8*3^m these counts grow without bound with k (k = 1..6).
Pure Python; a few seconds."""
import sys
from collections import Counter
R = []
def ok(n, c): R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n)
ok('x^2 - x - 1 has no root mod 3', all((x * x - x - 1) % 3 for x in range(3)))
# x^n mod (x^2 - x - 1) over Z: x^n = F_n x + F_(n-1); equals 1 iff F_n = 0 and F_(n-1) = 1
F = [0, 1]
for _ in range(2001): F.append(F[-1] + F[-2])
ok('x^n = F_n x + F_(n-1) is never 1 for 1 <= n <= 2000, so phi is no root of unity', all(not (F[n] == 0 and F[n - 1] == 1) for n in range(1, 2001)))
def census(k):
    q = 3 ** k; seen = bytearray(q * q); c = Counter()
    for s in range(q * q):
        if seen[s]: continue
        a, b = divmod(s, q); L = 0
        while not seen[a * q + b]:
            seen[a * q + b] = 1; L += 1; a, b = b, (a + b) % q
        c[L] += 1
    return c
C = {k: census(k) for k in range(1, 7)}
mult = lambda k, d: sum(n for L, n in C[k].items() if L % d == 0)
rows = {d: [mult(k, d) for k in range(1, 7)] for d in (1, 2, 3, 8, 24, 72)}
for d, r in rows.items(): print('  order %2d: multiplicity at k = 1..6: %s' % (d, r))
ok('every listed eigenvalue order has multiplicity growing strictly from the depth where it appears', all(all(x < y for x, y in zip([v for v in r if v], [v for v in r if v][1:])) for r in rows.values()))
ok('the eigenvalue 1 has multiplicity (3^k + 1)/2, the number of orbits', rows[1] == [(3 ** k + 1) // 2 for k in range(1, 7)])
print('%d of %d checks passed' % (sum(R), len(R))); sys.exit(0 if all(R) else 1)
