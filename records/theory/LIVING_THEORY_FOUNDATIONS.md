# The Living Theory of Existence: mathematical foundations

Generated from the register by records/theory/theory_foundations.py. Each territory lists the exact results its chapter may cite. A reading built on them is marked GENERATED-Omega42 (Core L-551 (5)); a correspondence with the observable world is PENDING, FOR APPLICATION (L-490).

## Origin

*Why does existence possess structure?*

| Result | What the chapter may cite | Status | Inherited | Recompute |
|---|---|---|---|---|
| MF-01 | The 81 states are the ring Z[phi]/9, the law is multiplication by phi. *Z[φ]/9 ≅ Z[i]/9 by φ ↦ 5 + i* | EXACT | EXACT | `python3 tools/space_prob.py --selftest` ("phi -> 5 + i, a ring isomorphism of Z[phi]/9 onto Z[i]/9") |
| MF-02 | The norm N(a + b phi) = a^2 + ab - b^2, the invariant that tells the orbits apart. *N(a + bφ) = a² + ab − b² ≡ x² + y² (mod 9)* | EXACT | EXACT | `python3 tools/space_prob.py --selftest` ("the norm goes to x^2 + y^2") |
| MF-10 | The five orbits carry the only invariant measures: the structure has exactly five sectors. *the invariant probability measures are the mixtures of the five orbit-uniform measures; sector probabilities are kept by U_T for every basis state and every state* | EXACT | EXACT | `python3 tools/foundations.py --selftest` ("sector probabilities kept") |
| Companion 130.2 and 131.2 | The premise's two numbers, the 24-cycle and the 81 states, force the arithmetic Z/9 | EXACT | EXACT | `python3 records/necessity/nine.py` |

## Time

*How do succession, recurrence and direction arise?*

| Result | What the chapter may cite | Status | Inherited | Recompute |
|---|---|---|---|---|
| MF-11 | The law's generator has spectrum k(2 pi/24), k = -11 to 12: time in 24 steps. *H, the principal logarithm of U_T, has spectrum k(2π/24), k = −11 to 12, and exp(−iH) = U_T; its five zero modes are the sector-uniform states* | EXACT | EXACT | `python3 tools/foundations.py --selftest` ("exp(-iH) = U_T on every basis state") |
| MF-204 | The half turn A^12 = -I: every state meets its negative at mid-cycle. *the half turn U^12 has eigenspaces of dimension 41 (+1) and 40 (-1); A^12 = -I, so every state is carried to its negative, and (0, 0) is the one state equal to its own negative; Q^2, with Q = a^2 + ab - b^2, is 1, 4 and * | EXACT | EXACT | `python3 tools/cobuilder_math.py --selftest` ("half-turn:") |
| MF-198 | At each finer depth every moving orbit lifts to three orbits three times as long: the cycle deepens without changing its law. *from modulus 3^k to 3^(k+1) each nonzero orbit of length L lifts to three orbits of length 3L and the still point to the still point and one 8-cycle; the harmonic l has multiplicity m_l = [l = 0] + sum_(j = 1..k) 3^(j - * | EXACT | EXACT | `python3 tools/cobuilder_math.py --selftest` ("renormalization:") |
| MF-13 | A coarse entropy is constant for a kept partition and returns with period 12 otherwise. *a coarse entropy is constant for a partition the law keeps and returns with period 12 for one it does not* | EXACT | EXACT | `python3 tools/foundations.py --selftest` ("the norm-class entropy is constant") |

## The Infinite Tower

*Can complexity grow without changing the law?*

| Result | What the chapter may cite | Status | Inherited | Recompute |
|---|---|---|---|---|
| MF-31 | The worlds mod 3^m number (3^m + 1)/2, labeled by the norm. *the worlds mod 3^m number (3^m + 1)/2, and the primitive ones are labelled one to one by +-Q* | EXACT | EXACT | `python3 tools/beyond.py --selftest` ("worlds labelled by the norm up to sign") |
| MF-32 | Each world embeds in the next, with its law, by s -> 3s. *sigma(s) = 3s embeds the family mod 3^(m-1) in the family mod 3^m with its law, and Q(3s) = 9 Q(s)* | EXACT | EXACT | `python3 tools/beyond.py --selftest` ("sigma(s) = 3s equivariant, injective, Q scaled by 9") |
| MF-42 | The law and the shear generate exactly the group of determinant +-1 over <A mod 3>, at every depth. *the Fibonacci-shear group G_k = <A, B> mod 3^k, B = [[1,0],[3,1]], is exactly {det = +-1, reduction in <A mod 3>}, of order 8*3^(3(k-1)), and its orbits are exactly the k + 1 valuation strata* | EXACT | EXACT | `python3 tools/fsg.py --selftest` ("F.9 cubing lifts") |
| MF-195 | The harmonic multiplicities of the law's shift. *the shift U of the law on functions of the 81 states has the harmonic j = 0 to 23 with multiplicity m_j = 3 + [3 | j] + [j = 0]; the operators commuting with U have dimension sum m_j^2 = 25 + 7 x 16 + 16 x 9 = 281, and t* | EXACT | EXACT | `python3 tools/cobuilder_math.py --selftest` ("harmonics:") |
| MF-201 | The counting bound for observation at every depth. *an observer team of seven-symbol readings that separates the 9^k states at depth k needs at least r_min(k) = ceil(k log_7 9) readings, 2, 3, 4, 5 and 6 for k = 1 to 5, and freely constructed observers attain it with the * | EXACT | EXACT | `python3 tools/cobuilder_math.py --selftest` ("observer-bound:") |

## Observation

*How much must be seen to know a state?*

| Result | What the chapter may cite | Status | Inherited | Recompute |
|---|---|---|---|---|
| MF-193 | Three seven-symbol readings separate the 81 states, and two never can. *a seven-symbol aperture h on the 81 states separates them all in three observations, the histories numbering 7, 49 and 81 after one, two and three steps; since 7^2 = 49 < 81 no seven-symbol aperture does it in two, so d_* | EXACT | EXACT | `python3 tools/cobuilder_math.py --selftest` ("aperture-optimal:") |
| MF-194 | The native aperture a mod 7 resolves 7, 49, 73, 77, 80 and 81 states in turn. *the structural aperture h = a mod 7 separates 7, 49, 73, 77, 80 and 81 states after 1 to 6 observations, and resolves a state first at round 2 for 25 states, 3 for 44, 4 for 4, 5 for 6 and 6 for 2; modulo 7 the law has o* | EXACT | EXACT | `python3 tools/cobuilder_math.py --selftest` ("aperture-mod7:") |
| MF-202 | Fixed native teams reach the bound at depths 2 to 4. *one shared aperture a mod 7 read at native phases of the law separates every state: at depth 2 by 24 anchored three-observer teams, (0, 2, 5) among them; at depth 3 by four observers (0, 1, 4, 19), one of 4,856 anchored * | EXACT | EXACT | `python3 tools/cobuilder_math.py --selftest` ("native-phases:") |
| MF-207 | And at depth 5, with six readings. *six native phases (0, 5, 44, 199, 243, 562) separate the 59,049 states of W_5 (paper Theorem 5.7)* | EXACT | EXACT | `python3 tools/tower_math.py --selftest` ("observe-depth5:") |
| MF-208 | At depth 6 eight readings suffice; whether seven do is open. *eight native phases (0, 11, 502, 510, 737, 777, 1820, 1842) separate W_6: 7 <= m_6 <= 8 (paper Proposition 5.8)* | EXACT | EXACT | `python3 tools/tower_math.py --selftest` ("observe-depth6:") |

## Generation

*How much diversity arises from few operations, and how fast is it reached?*

| Result | What the chapter may cite | Status | Inherited | Recompute |
|---|---|---|---|---|
| MF-35 | Every primitive state generates the whole; the units act freely and transitively. *every primitive state generates the whole family under Z[phi], and the units act on the primitive states transitively and freely* | EXACT | EXACT | `python3 tools/beyond.py --selftest` ("unique expression: each primitive state generates the whole, units transitive and free") |
| MF-209 | Exactly three sets of the four native operations reach every state, at every depth. *from (2, 5) exactly {A, C, S}, {A, V, C} and {A, V, C, S} reach every state of W_k, k >= 2 (paper Theorem 20.3)* | EXACT | EXACT | `python3 tools/tower_math.py --selftest` ("generating-sets:") |
| MF-210 | With doubling the farthest state is 2*3^k - 2 steps away: the world is exponentially wide. *the {A, V, C} distance of A^t V^s (2, 5) is t + s for t < 4h, h = 3^(k-1), else t + s - 3h, and its largest value is 2*3^k - 2 (paper Theorem 20.4)* | EXACT | EXACT | `python3 tools/tower_math.py --selftest` ("avc-distance:") |
| MF-211 | With the shear at least about 3.17k steps are needed; paper Theorem 20.6 (awaiting audit) gives at most c*k. *the largest distance from (2, 5) under {A, C, S} at depth k is at least ceil(log2(8*9^(k-1) + 1)) - 1, about 3.17k (paper Proposition 20.5)* | EXACT | EXACT | `python3 tools/tower_math.py --selftest` ("acs-lower:") |

## Space

*How does geometry emerge from relationships?*

| Result | What the chapter may cite | Status | Inherited | Recompute |
|---|---|---|---|---|
| MF-05 | The Hermitian matrices over Z[phi]/9 form a 3 + 1 space with an interval. *the Hermitian matrices over Z[φ]/9 form a 3 + 1 space with interval det X = t² − z² − x² − y²; 621 null vectors mod 9, 443961 mod 81* | EXACT | EXACT | `python3 tools/foundations.py --selftest` ("621 null vectors mod 9") |
| MF-06 | The law keeps that interval, mod 9 and mod 81. *X ↦ A X Aᵀ keeps the interval, mod 9 and mod 81* | EXACT | EXACT | `python3 tools/foundations.py --selftest` ("the interval is kept mod 81") |
| MF-07 | Its identification with the real Lorentz group is conditional on AP-SPACE. *over R ⊗ Z[φ, i] (AP-SPACE), X ↦ A X Aᵀ is an element of SO⁺(3,1), proper and orthochronous* | CONDITIONAL on AP-SPACE | CONDITIONAL on AP-SPACE | `python3 tools/foundations.py --selftest` ("A acts in SO+(3,1): proper and orthochronous") |
| MF-15 | The boost of rapidity 2 ln phi, conditional on AP-SPACE. *the action X -> AXA^T is the Lorentz matrix L_A with eigenvalues φ², φ⁻², −1, −1: a boost of rapidity 2 ln φ and a half-turn in a spacelike plane* | CONDITIONAL on AP-SPACE | CONDITIONAL on AP-SPACE | `python3 tools/geometric.py --selftest` ("L_A in SO+(3,1), eigenvalues phi^2, phi^-2, -1, -1") |

## Not yet grounded

- **Matter, Energy.** Register readings exist (MF-60 and others) but rest on AP-SPACE; the chapters are written as GENERATED-Omega42 readings until an exact ground is found.
- **Life, Consciousness, Intelligence (as experience), Meaning.** No register entry yet; the chapters are interpretation, marked GENERATED-Omega42, and may cite the Observation and Generation results as their mathematical analogues.
