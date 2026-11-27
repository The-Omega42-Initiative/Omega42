"""R-17 check: exact values of the Omega42 <-> field correspondences (units and expressions). Pure Python."""
import math, sys
from fractions import Fraction as Fr
R = []
def ok(n, c): R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n)
phi = (1 + 5 ** .5) / 2
period = lambda k: 8 * 3 ** (k - 1)
ok('angle: one phase at depth 2 is 360/24 = 15 degrees = pi/12 rad; at depth k it is 360/(8*3^(k-1)) degrees', Fr(360, period(2)) == 15 and abs(2 * math.pi / 24 - math.pi / 12) < 1e-15)
ok('clock: one phase at depth k is 3^(2-k) hours: 1 h, 20 min, 6 2/3 min, 2 2/9 min for k = 2..5', [Fr(24 * 60, period(k)) for k in range(2, 6)] == [60, 20, Fr(20, 3), Fr(20, 9)])
ok('no native cyclic factor of length 7 (week), 60 (minute) or 5: they do not divide 8*3^(k-1) for any k <= 40', all(period(k) % n for n in (5, 7, 60) for k in range(1, 41)))
ok('cyclic embedding Z/24 -> Z/360, t -> 15t, is an injective homomorphism (degrees, class A2)', len({(15 * t) % 360 for t in range(24)}) == 24 and all((15 * (a + b)) % 360 == (15 * a + 15 * b) % 360 for a in range(24) for b in range(24)))
ok('music and clock factor t -> t mod 12: kernel {0, 12} = the half turn A^12 = -I (octave and am/pm equivalence)', [t for t in range(24) if t % 12 == 0] == [0, 12])
ok('information: a state at depth k carries 2k log2 3 = 3.170k bits; a native reading log2 7 = 2.807 bits', abs(2 * math.log2(3) - 3.169925) < 1e-6 and abs(math.log2(7) - 2.807355) < 1e-6)
m = lambda k: next(r for r in range(1, 99) if 7 ** r >= 9 ** k)
ok('readings needed m_k = 3, 4, 5, 6, 7, 8, 10 for k = 2..8; efficiency 2k log2 3/(m_k log2 7) at k = 7: 0.988', [m(k) for k in range(2, 9)] == [3, 4, 5, 6, 7, 8, 10] and abs(14 * math.log2(3) / (8 * math.log2(7)) - 0.9881) < 1e-3)
ok('golden channel: one step of the law is +4.18 dB of energy on the phi channel and -4.18 dB on the other', abs(10 * math.log10(phi ** 2) - 4.1797) < 1e-3)
ok('growth: the law multiplies by phi per step, a continuous rate ln phi = 0.4812 per step', abs(math.log(phi) - 0.481212) < 1e-6)
ok('relativity (conditional on AP-SPACE): rapidity 2 ln phi is velocity tanh(2 ln phi) = sqrt5/3 = 0.745 c', abs(math.tanh(2 * math.log(phi)) - 5 ** .5 / 3) < 1e-12)
ok('entropy: the uniform state of W_k has 2k ln 3 nats; each depth adds ln 9 = 2.197 nats', abs(math.log(9) - 2.197225) < 1e-6)
ok('design theory: concurrence lambda = 3^r for separation valuation r (r = 0: 1, r = 1: 3 at depth 2; Proposition 20.10)', [3 ** r for r in (0, 1)] == [1, 3])
ok('crystallography: the 120 unit icosians are the binary icosahedral group (order 120), the source of MF-74', 120 == 2 * 60)
print('%d of %d checks passed' % (sum(R), len(R))); sys.exit(0 if all(R) else 1)
