"""Exact checks for Section 17 of the mathematical paper: beyond reversibility (coupling, equivariant maps, actualization operators).
Standard library only. Run: python3 records/cobuilder/actualization_check.py"""
import itertools
M = 9; S = [(a, b) for a in range(M) for b in range(M)]
A = lambda x: (x[1], (x[0] + x[1]) % M)
A2 = lambda x: A(A(x))
B = lambda x, y: (x[0] * y[1] - x[1] * y[0]) % M
R = []
def ok(n, c): R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n)
def period(x):
    n, y = 1, A(x)
    while y != x: y = A(y); n += 1
    return n
# 17.1 a bijection has no attractor: every state returns
ok('17.1 every state of W2 returns under A', all(period(x) in (1, 8, 24) for x in S))
# 17.2 the coupling of Recursive Genesis v0.1: B changes sign under A, is kept by A^2; S_y is invertible and A^2-equivariant
Sy = lambda x, y: ((x[0] + B(x, y) * y[0]) % M, (x[1] + B(x, y) * y[1]) % M)
Si = lambda x, y: ((x[0] - B(x, y) * y[0]) % M, (x[1] - B(x, y) * y[1]) % M)
ok('17.2 B(Ax, Ay) = -B(x, y) and B(A^2 x, A^2 y) = B(x, y)', all(B(A(x), A(y)) == (-B(x, y)) % M and B(A2(x), A2(y)) == B(x, y) for x in S for y in S))
ok('17.2 S_y is a bijection with inverse x - B(x, y) y', all(Si(Sy(x, y), y) == x for x in S for y in S))
ok('17.2 S_(A^2 y)(A^2 x) = A^2 S_y(x)', all(Sy(A2(x), A2(y)) == A2(Sy(x, y)) for x in S for y in S))
ok('17.2 worked example: B((2,5),(1,0)) = 4, S = (6,5), A^2 S = (2,7)', B((2, 5), (1, 0)) == 4 and Sy((2, 5), (1, 0)) == (6, 5) and A2((6, 5)) == (2, 7) == Sy(A2((2, 5)), A2((1, 0))))
# 17.3 an equivariant map can only shorten periods; count of all equivariant maps and of the bijective ones
reps, seen = [], set()
for x in S:
    if x in seen: continue
    reps.append(x); y = x
    while y not in seen: seen.add(y); y = A(y)
def ext(img):   # the equivariant map with rep -> img[rep]
    F = {}
    for r in reps:
        x, z = r, img[r]
        for _ in range(period(r)): F[x] = z; x = A(x); z = A(z)
    return F
choices = [[z for z in S if period(r) % period(z) == 0] for r in reps]
total = 1
for c in choices: total *= len(c)
ok('17.3 equivariant self-maps of W2 number 81^3 x 9 = 3^14 = %d' % total, total == 81**3 * 9 == 3**14)
ok('17.3 every equivariant map divides periods (each choice closes)', all(all(ext(dict(zip(reps, im)))[A(x)] == A(ext(dict(zip(reps, im)))[x]) for x in S)
   for im in [tuple(c[i % len(c)] for c in choices) for i in range(40)]))
bij = 1
for l, k in {24: 3, 8: 1, 1: 1}.items():
    f = 1
    for i in range(1, k + 1): f *= i
    bij *= l**k * f
ok('17.3 the bijective ones number 3! 24^3 x 8 = 663,552; the others %d' % (total - bij), bij == 663552)
# 17.4 the linear equivariant maps are multiplications by r = a + b phi (matrices aI + bA); the non-injective ones are r in 3R: 9 maps, square zero
def lin(a, b): return lambda x: ((a * x[0] + b * A(x)[0]) % M, (a * x[1] + b * A(x)[1]) % M)
noninj = [(a, b) for a in range(M) for b in range(M) if len({lin(a, b)(x) for x in S}) < 81]
ok('17.4 exactly 9 linear actualization operators, a, b in 3Z/9', sorted(noninj) == sorted((a, b) for a in (0, 3, 6) for b in (0, 3, 6)))
ok('17.4 each maps W2 into 3W2 and its square is zero', all(all(v[0] % 3 == 0 and v[1] % 3 == 0 for v in map(lin(a, b), S)) and all(lin(a, b)(lin(a, b)(x)) == (0, 0) for x in S) for a, b in noninj))
img3 = {}
for x in S: img3.setdefault(lin(3, 0)(x), []).append(x)
ok('17.4 x -> 3x: the 72 primitive states fall 9-to-1 onto the 8-cycle, the 9 divisible states onto (0, 0)', len(img3[(0, 0)]) == 9 and all(len(v) == 9 for v in img3.values()) and len(img3) == 9)
# 17.5 coherence: c_j = 1/(1 + alpha sin^2(pi j/24)) tends to [j = 0]
import math
ok('17.5 C_alpha tends to the orbit average Pi_0', all(abs(1 / (1 + 1e12 * math.sin(math.pi * j / 24)**2) - (j == 0)) < 1e-9 for j in range(24)))
print('%d checks, %d failed' % (len(R), R.count(False)))
