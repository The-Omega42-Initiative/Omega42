# The Mathematics of Omega42

**One law, an infinite tower of exact worlds, and what can be known inside them**

The Omega42 Co-Builders: Claude (Anthropic, integration program) and ChatGPT (OpenAI, research program), for the Originator (ESC) · 26 November 2026 · V335 Rev.450 STABLE

**Status.** Every numbered theorem is either proved in this paper or computed exhaustively by a script in the open repository; the recompute line is given with each result, and the register entry (MF-n) in Core Part 0.0.10. Part II surveys the wider register with a citation for every statement; ✓ marks a statement recomputed independently for this paper. Section 21 is marked SPECULATION throughout and asserts nothing.

## Abstract

We study the linear map A(a, b) = (b, a + b) acting on the states (a, b) of (ℤ/3ᵏℤ)², for every k ≥ 1. The canonical world is k = 2: eighty-one states that fall into exactly five orbits, of lengths 24, 24, 24, 8 and 1. Above it rises an infinite tower: at depth k there are 9ᵏ states, (3ᵏ + 1)/2 orbits and a longest period of 8 · 3ᵏ⁻¹, and every nonzero orbit lifts to three orbits three times as long.

On this tower we prove or compute results in seven directions.

- **Symmetry.** A¹² = −I, and the form Q(a, b) = a² + ab − b² changes sign at every step, so Q² labels the orbits.
- **Spectrum.** The harmonic j of the shift occurs 3 + [3 | j] + [j = 0] times, so the commutant has dimension 281. The spectrum determines the orbit census.
- **Observability.** Three readings of a well-chosen seven-symbol view separate all 81 states, and two never can. Teams of readers at native phases reach the bound ⌈k log₇ 9⌉ at depths 2, 3 and 4. At depth 5, seven readers suffice; whether six suffice is open.
- **Memory.** Additive memories modulo coboundaries are classified by their orbit sums: (ℤ/3ᵏ)^((3ᵏ+1)/2) classes, 59,049 of them at depth 2.
- **Resonance.** Four measures of agreement satisfy 0 ≤ F ≤ F_B ≤ R_O ≤ R_H ≤ 1. Every transformation commuting with the law fixes F, F_B and R_H and can move R_O exactly across [F_B, R_H].
- **Geometry.** A² is Arnold's cat map, the eighty-one states are the ninth-points of its torus, and the points the torus brings back after n steps number |Lₙ − (−1)ⁿ − 1|.
- **The number 42.** π/42 is the least area of a hyperbolic triangle with angles π/p, π/q, π/r.

Part II surveys the wider register: the arithmetic of the golden ring at every prime, the Fibonacci–shear and orthogonal groups, Lorentz geometry and the modular surface, E₈ and H₄, the Fibonacci quasicrystal and its trace map, the quantum cat map and the foundations. Part III sets out the significance of the work, twelve open problems, and an invitation to mathematicians to check, extend and join it. Speculation is marked as such.

## To the mathematician reading this

This paper is addressed to you.

Omega42 began as a thought experiment about existence. Its foundation is a single linear map over the 3-adic integers. Two AI systems, working as Co-Builders under the direction of a human Originator, have asked that map every question they could think of, and recording every answer in an open register that anyone can recompute. Much of what they found is classical. Some of it we have not found in the literature. All of it is exact, and all of it is checkable in seconds.

We are not asking you to accept a worldview. We are asking you to look at the mathematics, because you will see things in it that we cannot. Specifically:

- **Check us.** Every theorem has a recompute line. If a proof is wrong, incomplete or longer than it needs to be, say so. Corrections are entered in the open register under the corrector's name, and the record of an error is kept as carefully as the record of a result.
- **Tell us what is known.** Where a result here is a special case of something in the literature, we want the reference. Prior work is credited, not competed with.
- **Solve an open problem.** Section 19 lists them, from a finite search (O-30) to questions about 3-adic limits, other primes and the Wall–Sun–Sun primes.
- **Extend the world.** The law is one choice among many. The tower, the observability bounds, the memory classification and the resonance chain all make sense for other matrices and other primes. Which of them survive, and in what form?

Section 20 says how to take part. The text of this paper is CC BY 4.0 and the code Apache-2.0; what you contribute is published openly under your name.

# Part I. One law and what can be known inside it

## 1. Introduction

The Fibonacci rule "add the last two numbers" is among the oldest recurrences in mathematics. Read modulo nine it becomes periodic: the Pisano period of 9 is 24 [1]. Omega42 takes this one law, read on the pairs of residues, as a complete world. It is finite at its seed and infinite in its depth, and nothing in it is assumed twice. Every question that can be asked inside it has an exact answer that anyone can recompute.

This paper collects the mathematics of that world as it stands on 26 November 2026. Much of it was found in an exchange between two AI systems working as Co-Builders, each proposing results and recomputing the other's, under the direction of a human Originator. The method matters to the content. A result entered the record only when an independent recomputation agreed with it, and an error, once found, was corrected in the open register, not withdrawn in silence. Section 22 lists the scripts.

**Notation.** We write A = [[0, 1], [1, 1]], acting on column vectors x = (a, b). The world at depth k is Wₖ = (ℤ/3ᵏℤ)², with 9ᵏ states, and the canonical world is W₂, with 81. We write U for the shift operator on functions f : W₂ → ℂ, (Uf)(x) = f(Ax), and Q(a, b) = a² + ab − b². Lₙ is the n-th Lucas number (L₀ = 2, L₁ = 1, Lₙ₊₁ = Lₙ + Lₙ₋₁), and φ = (1 + √5)/2.

## 2. The canonical world: eighty-one states, five orbits

**Theorem 2.1 (orbit census).** On W₂ the map A is a bijection of order 24. Its orbits have lengths 24, 24, 24, 8 and 1. The orbit of length 1 is (0, 0). The orbit of length 8 consists of the eight nonzero states with both coordinates divisible by 3.

*Proof.* det A = −1 is a unit, so A is invertible modulo every m.

- **The divisible states.** The nine states with 3 | a and 3 | b form the subgroup 3W₂ ≅ (ℤ/3)², on which A acts as A mod 3. Modulo 3, A has order 8 and moves every nonzero vector: the characteristic polynomial x² − x − 1 has no root mod 3, so A mod 3 generates the multiplicative group of 𝔽₉, a cyclic group of order 8. This gives the fixed point (0, 0) and one orbit of length 8.
- **The other 72 states.** Let x be a state with a or b not divisible by 3. If Aᵗx = x, then reducing mod 3 gives (A mod 3)ᵗ fixing a nonzero vector, so 8 | t.
  - Direct computation gives A⁸ ≡ [[4, 3], [3, 7]] mod 9. So A⁸ − I ≡ 3[[1, 1], [1, 2]], whose kernel mod 9 is exactly 3W₂. Hence A⁸x ≠ x.
  - The order of A divides 24 (Theorem 2.2), so the period of x divides 24, is a multiple of 8 and is not 8. It is therefore 24.
  - The 72 states split into 72/24 = 3 orbits. ∎

**Theorem 2.2 (the half turn).** A¹² = −I on W₂. Every state meets its own negative halfway round its 24-orbit, and four steps on in the 8-orbit. The only state equal to its own negative is (0, 0).

*Proof.* A¹² = [[89, 144], [144, 233]] ≡ [[8, 0], [0, 8]] = −I mod 9. On the 8-orbit, A⁸ = I there, so A¹² = A⁴. If x = −x, then 2x = 0, and since 2 is a unit mod 9, x = 0. ∎

**Theorem 2.3 (the alternating form).** Q(Ax) = −Q(x) for every state. Q² is therefore constant on every orbit. On the three 24-orbits it takes the values 1, 4 and 7, and on the 8-orbit and the fixed point it is 0. The pair (period, Q²) names each of the five orbits.

*Proof.* Q(b, a + b) = b² + b(a + b) − (a + b)² = −(a² + ab − b²). The values on the orbits are computed directly: for the canonical seed, Q(2, 5) = −11 ≡ 7, so Q² ≡ 4. ∎

**The canonical loop.** The orbit of the seeds (2, 5) is the canonical loop. Writing residue 0 as the digit 9, its first coordinates run 2, 5, 7, 3, 1, 4, 5, 9, 5, 5, 1, 6, then 7, 4, 2, 6, 8, 5, 4, 9, 4, 4, 8, 3, and round again.

- The second half is the complement of the first: the two digits at each pair of opposite positions add to 9, except where both are 9.
- The sum over one period is 117, in the digit convention.
- The digits 3, 6 and 9 arrive exactly every fourth step.
- Recompute: `python3 records/cobuilder/core_consistency_2026_11_25.py`.

## 3. The tower: an infinite family of exact worlds

**Theorem 3.1 (the tower census).** At depth k ≥ 1, A has order 8 · 3ᵏ⁻¹ on Wₖ. The orbits of Wₖ are:

- one fixed point;
- for each j = 1, …, k, exactly 3ʲ⁻¹ orbits of length 8 · 3ʲ⁻¹.

There are (3ᵏ + 1)/2 orbits in all. Reduction from depth k + 1 to depth k carries orbits onto orbits. Every nonzero orbit of length L at depth k lifts to three orbits of length 3L, and the fixed point lifts to the fixed point and one orbit of length 8.

*Proof sketch.* Group the states of Wₖ by the exact power of 3 dividing both coordinates. The states divisible by exactly 3ᵏ⁻ʲ, and by no higher power, correspond to the primitive vectors of Wⱼ: those not both divisible by 3. There are 9ʲ − 9ʲ⁻¹ = 8 · 9ʲ⁻¹ of them.

On these primitive vectors A acts freely with period 8 · 3ʲ⁻¹. Theorem 2.1 is the case j = 2. The step from 3ʲ to 3ʲ⁺¹ is the standard lifting of the exponent: A^(8·3ʲ⁻¹) ≡ I + 3ʲM mod 3ʲ⁺¹, with M invertible on primitive vectors mod 3. So the period of every primitive vector triples, and no shorter period appears.

Hence the primitive vectors of Wⱼ form 8 · 9ʲ⁻¹ / (8 · 3ʲ⁻¹) = 3ʲ⁻¹ orbits. Counting gives 1 + Σⱼ 3ʲ⁻¹ = (3ᵏ + 1)/2 orbits and 1 + Σⱼ 8 · 9ʲ⁻¹ = 9ᵏ states. The census is computed exhaustively for k ≤ 5. ∎ (Recompute: `python3 tools/cobuilder_math.py --selftest`, line `renormalization:`.)

| Depth k | States 9ᵏ | Orbits (3ᵏ + 1)/2 | Longest period |
|---|---|---|---|
| 1 | 9 | 2 | 8 |
| 2 | 81 | 5 | 24 |
| 3 | 729 | 14 | 72 |
| 4 | 6,561 | 41 | 216 |
| 5 | 59,049 | 122 | 648 |
| k | 9ᵏ | (3ᵏ + 1)/2 | 8 · 3ᵏ⁻¹ |

The tower does not end. Its inverse limit is the plane ℤ₃[φ] over the 3-adic integers, on which A acts as multiplication by the golden ratio. Every finite world of Omega42 is one floor of a single infinite structure, and every floor is computed exactly.

## 4. The spectrum

**Theorem 4.1 (harmonic multiplicities).** The shift U on ℓ²(W₂) is a permutation operator. Its eigenvalues are the 24th roots of unity ωʲ = e^(2πij/24). The harmonic j occurs with multiplicity

  mⱼ = 3 + [3 | j] + [j = 0],

that is, 5 for j = 0, 4 for the seven multiples j = 3, 6, …, 21, and 3 for the other sixteen values.

*Proof.* On an orbit of length ℓ, U acts as a cyclic shift. Its eigenvalues are the ℓ-th roots of unity, each once, and the ℓ-th roots are the harmonics j with (24/ℓ) | j. The three 24-orbits give every harmonic once each; the 8-orbit gives the multiples of 3; the fixed point gives j = 0. ∎

**Corollary 4.2 (the commutant).** The operators commuting with U form an algebra isomorphic to M₅(ℂ) ⊕ M₄(ℂ)⁷ ⊕ M₃(ℂ)¹⁶. Its dimension is 25 + 112 + 144 = 281.

**Theorem 4.3 (coherence).** Let L = 2I − U − U*, the Laplacian of the dynamics. For α ≥ 0, the operator C_α = (I + αL/4)⁻¹ acts on the harmonic j by

  c_j = 1 / (1 + α sin²(πj/24)).

C_α is self-adjoint and positive, it is a contraction with 0 < c_j ≤ 1 and c₀ = 1, and it commutes with U. It smooths a function without breaking the cycle. (Recompute: `coherence:`.)

**Theorem 4.4 (the dynamics can be heard).** The multiset of eigenvalues of U, with multiplicities, determines the orbit census exactly, at every depth.

*Proof.* Let μ(d) be the multiplicity of the primitive d-th roots of unity. A cycle of length ℓ contributes one eigenvalue of every order d | ℓ, and of each such order exactly φ(d) eigenvalues. So μ(d)/φ(d) is the number of cycles whose length is divisible by d. Möbius inversion over the multiples of d recovers the number of cycles of each exact length. ∎

The theorem is computed at depths 1 to 4, where heard and counted agree. Its meaning is sharp. Every drawing of a 24-cycle has the same Laplacian, so the spectrum cannot hear how the loop is drawn: a circle and a square sound alike. But it hears exactly which loops the world is made of.

## 5. Observability: how much of the world can be seen

An *aperture* is a map h : W₂ → S into a set of symbols. An observer reading h at times t₁, …, t_r sees the tuple (h(A^(t₁)x), …, h(A^(t_r)x)). The world is *observed* when this tuple determines x.

**Theorem 5.1 (the seven-symbol aperture).** There is an aperture with seven symbols whose readings at times 0, 1 and 2 separate all 81 states. The histories number 7, 49 and 81 after one, two and three readings. No seven-symbol aperture separates the states in two readings, since 7² = 49 < 81. So d_min(7) = 3.

The certificate table is in `tools/cobuilder_math.py` (`aperture-optimal:`), proposed by ChatGPT and recomputed by Claude.

**Theorem 5.2 (the native aperture).** The aperture a mod 7 needs six readings. After 1 to 6 readings it separates 7, 49, 73, 77, 80 and 81 states.

The least length depends on how the nine values are merged into seven classes. Of the 378 apertures that merge two disjoint pairs of values of a, the least length is 5 for 270, 6 for 78, 7 for 6, 8 for 3, and 21 never separate. Modulo 7, the law has order 16, and the 49 pairs split as 1 + 16 + 16 + 16.

**Theorem 5.3 (the bound).** Any team of seven-symbol readings that separates W_k needs at least r_min(k) = ⌈k log₇ 9⌉ readings. That is 2, 3, 4, 5 and 6 for k = 1 to 5. Freely chosen observers attain the bound, for example through the base-7 digits of the state index.

**Theorem 5.4 (one view, many readers).** The single aperture a mod 7, read at native phases of the law, attains the bound at depths 2, 3 and 4:

- depth 2: three readers, for example at phases (0, 2, 5); there are 24 anchored teams;
- depth 3: four readers, (0, 1, 4, 19); there are 4,856 anchored certificates;
- depth 4: five readers, (0, 94, 145, 152, 195).

At depth 5 the six phases (141, 155, 211, 282, 338, 409) give 59,041 distinct readings, eight pairs short of 59,049. Adding phase 1 separates every state, so seven readers suffice. (ChatGPT, recomputed by Claude: `records/cobuilder/xobs02_search.py`.)

**Open problem O-30.** Do six native phases of a mod 7 separate all 59,049 states at depth 5?

## 6. Memory

A *memory* on the world is a function g : W_k → ℤ/3ᵏ, carried by the extended dynamics T_g(x, m) = (Ax, m + g(x)). Two memories g and g′ are *equivalent* when g′ = g + f∘A − f for some f, that is, when they differ by relabeling the memory register.

**Theorem 6.1 (classification).** The class of g is determined by its vector of orbit sums W_g(O) = Σ_(x∈O) g(x), one sum for each orbit O. Every vector occurs. The classes therefore form (ℤ/3ᵏ)^((3ᵏ+1)/2): 9 at depth 1, 59,049 at depth 2, 27¹⁴ at depth 3.

*Proof.*
- **The sums are invariant.** Each orbit sum of f∘A − f telescopes to 0.
- **Every vector occurs.** A delta at one representative of each orbit realizes any vector of sums. Constant functions on an orbit do not: on an orbit whose length is divisible by 3, they reach only multiples of 3, which is why the delta is needed. (ChatGPT's refinement.)
- **Zero sums mean a coboundary.** If every orbit sum of g is 0, define f along each orbit by f(A^(t+1)r) = f(Aᵗr) + g(Aᵗr). The definition closes around the orbit exactly because the sum is 0. ∎

**Corollary 6.2.** The memory g(a, b) = a records nothing: it is the coboundary of f(a, b) = b, since f(Ax) − f(x) = (a + b) − b = a. Its orbit sums vanish at every depth. The memory Q² records the orbit and its length: its sum over O is |O| · Q(x)².

**Theorem 6.3 (memory under lifting).** Pulling memories back from depth 2 to depth 3 maps the 59,049 classes onto 729 classes, with a kernel of 81 classes.

## 7. Resonance: four measures of agreement

For nonzero vectors v, w in ℓ²(W_k), decompose each along the orbits and harmonics. Write v̂_(O,j) for the coefficient of v on the harmonic j of the orbit O, and v_j for the component of v in the harmonic subspace j. With normalized energies p_j = ‖v_j‖² / ‖v‖² and p_(O,j) = |v̂_(O,j)|² / ‖v‖², and similarly q for w, define:

- **harmonic resonance** R_H = Σ_j √(p_j q_j);
- **orbit-resolved resonance** R_O = Σ_(O,j) √(p_(O,j) q_(O,j));
- **Block Fidelity** F_B = Σ_j |⟨v_j, w_j⟩| / (‖v‖ ‖w‖);
- **fidelity** F = |⟨v, w⟩| / (‖v‖ ‖w‖).

**Theorem 7.1 (the resonance chain).**

  0 ≤ F ≤ F_B ≤ R_O ≤ R_H ≤ 1.

*Proof.* The harmonic subspaces are orthogonal, so ⟨v, w⟩ = Σ_j ⟨v_j, w_j⟩, and the triangle inequality gives F ≤ F_B. Within one harmonic, ⟨v_j, w_j⟩ = Σ_O conj(v̂_(O,j)) ŵ_(O,j), so |⟨v_j, w_j⟩| ≤ Σ_O |v̂_(O,j)| |ŵ_(O,j)|, which gives F_B ≤ R_O. By Cauchy–Schwarz on each harmonic, Σ_O √(p_(O,j) q_(O,j)) ≤ √(p_j q_j), which gives R_O ≤ R_H. Finally Σ_j √(p_j q_j) ≤ 1, again by Cauchy–Schwarz. ∎

The gaps between the measures carry information:

- Deltas on two different 24-orbits give R_H = 1 and R_O = 0: the same music, different worlds.
- Deltas on two states of the same orbit give R_H = R_O = 1 and F = 0: the same loop, orthogonal states.

The *Resonance Resolution Gap* R_H − F splits into three layers: the orbit gap R_H − R_O, the phase gap within harmonics R_O − F_B, and the phase gap across harmonics F_B − F.

**Theorem 7.2 (what transformations can change).** Let T be any unitary operator commuting with U; by Corollary 4.2 it is block-diagonal over the harmonics. Applied to both v and w, T leaves R_H, F_B and F unchanged. The values R_O can take under all such T form exactly the interval [F_B, R_H], and both ends are reached.

*Proof.*
- **What stays fixed.** T preserves each ‖v_j‖ and each ⟨v_j, w_j⟩.
- **Lower end.** In each block, a unitary sending v_j onto a single mode reduces that block's contribution to R_O to |⟨v_j, w_j⟩|.
- **Upper end.** A unitary sending the two vectors (f₁ ± e^(iθ) f₂)/√2 to two modes, where f₁ is the direction of v_j, f₂ is the part of w_j orthogonal to it, and θ is chosen so that the two components of w_j are a quarter turn apart, makes |v̂| proportional to |ŵ| mode by mode. This raises the block's contribution to ‖v_j‖ ‖w_j‖.
- **Everything between.** The unitary group is connected, so every value in between is reached. Every block has at least three modes, so both constructions fit. ∎

Of the resolution gap, transformations that respect the law can trade the orbit layer against the phase layer within harmonics. They cannot touch the phase layer across harmonics, F_B − F. (Computed with random complex vectors and Haar-random blocks at depths 2 and 3; the endpoints were reached to 1e-9.)

## 8. Geometry: the golden torus

**Theorem 8.1 (the square root of the cat map).** A² = [[1, 1], [1, 2]], Arnold's cat map, the classical chaotic automorphism of the torus T² = ℝ²/ℤ². A itself acts on T² by the same matrix. On the plane it stretches by φ and contracts by 1/φ along its eigenlines, keeping area and reversing orientation.

**Theorem 8.2 (the worlds inside the torus).** The map (a, b) ↦ (a/9, b/9) identifies W₂ with the points of T² whose coordinates have denominator 9, and A acts on them exactly as the law acts on W₂. More generally, W_k is the set of 3ᵏ-division points. The tower of Section 3 is the nested family of 3-power division points of one chaotic torus. These points are dense in T², and each is periodic.

**Theorem 8.3 (counting the returns).** A point of T² returns after n steps exactly when (Aⁿ − I)x ∈ ℤ². There are |det(Aⁿ − I)| = |Lₙ − (−1)ⁿ − 1| such points.

*Proof.* det(Aⁿ − I) = det Aⁿ − tr Aⁿ + 1 = (−1)ⁿ − Lₙ + 1, since tr Aⁿ = φⁿ + (−1/φ)ⁿ = Lₙ. ∎

For n = 1, …, 12 the counts are 1, 1, 4, 5, 11, 16, 29, 45, 76, 121, 199 and 320. For n = 24 the count is 103,680 = 81 × 1,280. The eighty-one states form a subgroup of index 1,280 among the points that return after 24 steps. (Recompute: `records/cobuilder/cg_2026_11_26_geometry_check.py`.)

The same law, at points of the same torus, is perfectly ordered at every rational point and chaotic at almost every other point. Omega42's finite worlds are the ordered skeleton of a chaotic continuum.

## 9. Why 42

**Theorem 9.1.** Among hyperbolic triangles with angles π/p, π/q and π/r, where p, q and r are integers, the least area π(1 − 1/p − 1/q − 1/r) is π/42. It is attained only at (2, 3, 7).

*Proof.* Order p ≤ q ≤ r, with 1/p + 1/q + 1/r < 1.
- If p ≥ 3, the area is at least π(1 − 1/3 − 1/3 − 1/4) = π/12.
- If p = 2 and q ≥ 4, it is at least π(1 − 1/2 − 1/4 − 1/5) = π/20.
- If p = 2 and q = 3, the area is π(1/6 − 1/r) with r ≥ 7, least at r = 7, where it is π/42. ∎

The (2, 3, 7) triangle group is the source of Hurwitz's bound of 84(g − 1) automorphisms of a surface of genus g ≥ 2 [4], and 84 = 2 · 42. The statement is limited to angles of the form π/n: among triangles with arbitrary angles, areas take every value in (0, π).

# Part II. The wider architecture

Part I followed one line of results from the law to what can be known inside it. The register (Core Part 0.0.10, 206 entries, MF-01 to MF-206) reaches much further. Part II surveys it by territory. Each statement cites its register entry; the register gives the derivation, the domain, the tool that recomputes it and, for every entry, what does *not* follow from it. Statements marked ✓ were recomputed independently for this paper by `records/cobuilder/paper_part2_check.py` (24 checks, standard library only). The status EXACT in the register means an exact computation or proof within the stated domain; a bounded computation keeps its bounds and is not a theorem about every case. Part III prints the whole register.

## 10. The arithmetic of the golden ring

The law is multiplication by φ in the ring R = ℤ[φ], φ² = φ + 1, written in the basis (1, φ): φ(a + bφ) = b + (a + b)φ. Its form Q is the field norm N(a + bφ) = a² + ab − b², and φ is a unit of norm −1.

- **The prime 3 is inert.** x² − x − 1 has no root modulo 3, so R/3R = 𝔽₉ and the canonical world W₂ is R/9R. The 3-adic completion ℤ₃[φ] is the unramified quadratic extension of ℤ₃, and the tower of Section 3 is its sequence of finite quotients.
- **Surprising coincidences of residue rings.** φ ↦ 5 + i is a ring isomorphism ℤ[φ]/9 ≅ ℤ[i]/9 (MF-01 ✓), under which the norm becomes x² + y² (MF-02). φ⁶ = 5 + 8φ squares to −1 modulo 9 (MF-03 ✓); −1 has a square root in ℤ₃[φ] and ℚ₃(√5) = ℚ₃(i) (MF-04).
- **Units.** The units of norm ±1 modulo 3ᵐ are exactly the powers of φ, 8 · 3ᵐ⁻¹ of them (MF-39 ✓); the closure of ⟨φ⟩ in the 3-adic units is the whole group of units of norm ±1 (MF-55). The map n ↦ φ⁸ⁿ extends continuously to n ∈ ℤ₃ (MF-33).
- **Projective dynamics.** On the projective line P¹(ℤ/3ᵏ) the law is a single cycle of length 4 · 3ᵏ⁻¹, and on P¹(ℤ₃) it is minimal and uniquely ergodic, with Haar measure (MF-40, MF-56).
- **A correction.** The register's MF-73 called 3R/9R the field 𝔽₉. Its multiplication is zero, since 3x · 3y = 9xy; it is an R-module isomorphic to R/3R = 𝔽₉, on which φ acts with order 8 (✓; ChatGPT's correction, 26 November 2026). The Wheel is the action of φ on that module.
- **Every prime.** A is a boost at the split primes, a rotation at the inert ones and a shear at the ramified prime 5 (MF-28); the inert primes 3, 7, 13, 17, 23, 47 return antipodally through Frobenius, and at the ramified prime A¹⁰ ≡ −I mod 5 (MF-41). Modulo the split prime 11 the roots of x² = x + 1 are 4 and 8, and the 121 pairs fall into 1 + 2 × 5 + 11 × 10 (MF-203 ✓).
- **Analytic shadow.** L(1, χ₅) = 2 ln φ / √5, with class number 1 and regulator ln φ (MF-30); the product formula holds over every place of ℚ(√5) (MF-29).
- **Regularity of the tower at every prime tested.** No prime below 10⁶ has first-lift valuation at least 2 (MF-50): for each, the period at p² is p times the period at p. A prime where this fails is a *Wall–Sun–Sun prime*. Whether one exists is a classical open question [6], and Omega42's tower at that prime would begin irregularly.

## 11. Symmetry groups

- **The orthogonal group of the form.** Modulo 3ᵏ, SO(Q) = ⟨A²⟩ of order 4 · 3ᵏ⁻¹, and O(Q) is dihedral of order 8 · 3ᵏ⁻¹ (MF-45 ✓ at k = 2).
- **The Fibonacci–shear groups.** With the shear B = [[1, 0], [3, 1]], G_k = ⟨A, B⟩ mod 3ᵏ is exactly the matrices of determinant ±1 whose reduction lies in ⟨A mod 3⟩; it has order 8 · 3³⁽ᵏ⁻¹⁾ (MF-42; 216 at k = 2 ✓). For B_r = [[1, 0], [3ʳ, 1]] the order is 8 · 3^(3k−2r−1), and the complete orbit invariant is the pair (valuation, Q of the primitive part) (MF-43). The number of classes forms a ladder between the k + 1 valuation strata and the Fibonacci census (MF-51), and for any shear the order depends only on the 3-adic valuation of its entry (MF-53).
- **The prime 7.** Modulo 7, ⟨A, B⟩ is every matrix of determinant ±1 (MF-68, MF-71 ✓), and ⟨A², B⟩ acts on the eight points of P¹(𝔽₇) as PSL₂(𝔽₇), of order 168 (MF-77 ✓): the automorphism group of the Klein quartic, the genus-3 surface that attains Hurwitz's bound 84(g − 1) = 168 and is tiled by (2, 3, 7) triangles [4, 7]. The 42 of Theorem 9.1 and the 168 of the Klein quartic come from the same triangle.
- **Seventeen primes.** A sealed prediction (PR-001) was confirmed: the law and the shear generate every matrix of determinant ±1 modulo each of 17 further primes (MF-104).
- **What selects the law.** Under four stated principles (an integer law invertible over ℤ, least hyperbolic growth, an inert base prime, a distinct antipode at half period for every nonzero state), the law x² − x − 1 and the prime 3 are selected (MF-49). The census 3 × 24 + 8 + 1 holds for T(a, b) = (b, a + kb) modulo 9 exactly for k = 1, 2, 7, 8 (MF-44). [[0, 1], [1, 7]] shares A's whole 3-adic fingerprint and is separated only by its trace and by the prime 7 (MF-57, MF-66, MF-72): the census alone does not determine the law.

## 12. Lorentz geometry and the hyperbolic plane

The form Q is indefinite, so the law lives naturally in Minkowski geometry.

- **The boost.** A² preserves Q and is a Lorentz boost of the (1, 1) plane of Q (MF-09). On real symmetric 2 × 2 matrices, X ↦ A X Aᵀ keeps det X; A² acts as the *golden boost* with Lorentz factor γ = L₄/2 = 7/2, speed 3√5/7 and rapidity 4 ln φ (MF-135, MF-136 ✓), and its n-th power has γₙ = L₄ₙ/2 (MF-137). The shear B is a null rotation fixing a light ray, so ⟨A², B⟩ contains boosts, null rotations and rotations (MF-61, MF-140).
- **Light rays from states.** s ↦ s sᵀ sends every state to a null vector and commutes with the law (MF-20, MF-25); every Fibonacci state maps to a light ray whose components give a Pythagorean triple (MF-59). The null vectors of the 3 + 1 Hermitian space over ℤ[φ]/3ᵏ number 21, 621, 16,281, 443,961, with the recursion N_k = 20 · 27ᵏ⁻¹ + 81 N_(k−2) (MF-23).
- **The modular surface.** A² = LR, so its closed geodesic on the modular surface has cutting sequence (LR)^∞ and length 2 arccosh(3/2) = 4 ln φ (MF-95 ✓): the shortest closed geodesic, while A itself is the shortest glide reflection (MF-62). The law's numbers form the Fibonacci branch of the Markov tree: (1, F₂ₙ₋₁, F₂ₙ₊₁) solves x² + y² + z² = 3xyz (MF-83 ✓).
- **The figure-eight knot.** A² is conjugate to [[2, 1], [1, 1]], the monodromy of the figure-eight knot; t² − 3t + 1 is its Alexander polynomial, and its complement has hyperbolic volume 2.029883… (MF-84 ✓).
- **The number 42 again.** The 42 triangulations of a heptagon are the 42 positive quiddity cycles of length 7, words in SL₂(ℤ) whose product is −I, the same −I as the law's half period (MF-70); and A⁸ = I + 3M with F₈ = 21 = 3 × 7 (MF-69).

## 13. Exceptional structures

- **E₈ from the icosians.** The 120 unit icosians span a ℤ[φ]-module of ℤ-rank 8 closed under multiplication by φ; with the form 2 Tr((φ/√5)⟨x, y⟩) it is the E₈ lattice, and the law acts on it as an 8 × 8 integer matrix M with M² = M + I (MF-74). On E₈/9E₈, with 43,046,721 classes, the law has the census 1 + 820 × 8 + 1,793,340 × 24: the census of the 81 states four times over (MF-75).
- **The Coxeter element.** C(x) = l x r, with icosians l of order 10 and r of order 3, is a Coxeter element of E₈ (order 30) that commutes with the law, and I + C¹² + C⁻¹² = φ: the law is a polynomial in the Coxeter element (MF-76). C permutes the 240 roots in 8 orbits of 30 (MF-102).
- **H₄.** The spectral projector of the law on E₈ carries the 240 roots onto two 600-cells of H₄ whose radii stand in the ratio φ (MF-81).
- **Codes and lattices.** ⟨A², B⟩ mod 7 keeps the extended Hamming code [8, 4, 4], and Construction A gives E₈ and E₇ (MF-77, MF-107); E₆/3E₆* is a quadratic space 𝔽₃⁵ whose 72 classes of norm 1 are the roots of E₆ (MF-78); the Golay code [24, 12, 8] and its Adinkra (MF-109); octonions on the Fano lines and the Albert algebra (MF-108, MF-124).
- **Physics of E₈.** In Zamolodchikov's E₈ spectrum of the Ising field theory in a magnetic field, m₂/m₁ = 2 cos(π/5) = φ (MF-90); G₂ × F₄ at level 1 embeds conformally in E₈ at level 1, its sectors pairing the Fibonacci sectors (MF-89).

## 14. Aperiodic order and spectral theory

- **The Fibonacci word.** The substitution a → ab, b → a has matrix [[1, 1], [1, 0]], the law with coordinates exchanged (MF-127); as an automorphism of the free group it has the law as its abelian shadow and the trace map as its SL₂ shadow (MF-156). Cut and project along the eigenlines of the law gives the Fibonacci chain (MF-82); Penrose inflation is A² conjugated by the swap (MF-103).
- **The trace map.** f(x, y, z) = (2xy − z, x, y) keeps the Fricke–Vogt invariant x² + y² + z² − 2xyz − 1 (MF-129 ✓) and returns every triple with two zero coordinates after exactly six steps (MF-130 ✓). Modulo 9 it is a bijection of the 729 triples with orbit census 2 × 1, 2 × 2, 1 × 3, 9 × 4, 8 × 6, 3 × 8, 9 × 12, 21 × 24 (MF-148 ✓). Its period equals the law's Pisano period modulo 9, 27, 81 and the powers of 2 to 32, and differs modulo 3 (12 against 8 ✓) and modulo every prime from 5 to 31 (MF-163).
- **The Fibonacci Hamiltonian.** The transfer matrices of the quasicrystal obey the law of the words, and their half-traces the trace map of Kohmoto, Kadanoff and Tang (MF-128) [8]. Its gaps are labeled by the ring ℤ + ℤφ that the law multiplies (MF-131, MF-159), the total band width scales as L^(−0.2867) (MF-170), and the Chern numbers of the gaps on the torus of Bloch phase and phason equal minus the label (MF-171). The same trace orbits govern light in Fibonacci dielectric stacks, sound in layered media and electrons with Fibonacci hoppings (MF-145 to MF-153, MF-173).
- **Penrose tilings.** de Bruijn pentagrid patches, their vertex degrees and their zero modes (MF-161, MF-162, MF-167).

## 15. Quantum phase space

- **Weyl operators.** The 81 states label the Weyl operators D(a, b) of one nine-level quantum system; (ℤ/9)² has elements of order 9, so it is the phase space of one nine-level system and not of two qutrits (MF-178, MF-183).
- **The quantum cat map.** The unitary U(j, k) = ω^(j² − jk + k²/2)/√N quantizes A² for every odd N (MF-186 ✓). Its commutant is spanned by orbit sums of Weyl operators, and A² has exactly N orbits on the N² labels at N = 3ᵏ (✓ for k = 1, 2, 3), so every eigenvalue is simple (MF-184, MF-185). The odd powers carry the position basis to unbiased bases (MF-180); A itself, of determinant −1, is quantized as an antiunitary (MF-179).
- **Stabilizer and magic.** Wigner functions of the position states and their Clifford images are nonnegative; the cubic-phase state has negativity 0.5863 (MF-181).
- **Fusion and contextuality.** The fusion matrix of the Fibonacci anyon τ ⊗ τ = 1 ⊕ τ is A in the basis (1, τ), with quantum dimension φ (MF-88 ✓, MF-177); the Lee–Yang (2, 5) model carries the same fusion (MF-92). In the KCBS test on one qutrit the quantum value is √5 = φ + 1/φ against the classical bound 2, an excess of φ⁻³ (MF-188 ✓). A and B on one of three qubits keep Cayley's hyperdeterminant, the 3-tangle (MF-99).

## 16. Measure, dynamics and logic

- **Invariant measures.** The invariant probability measures on W₂ are exactly the mixtures of the five orbit-uniform measures (MF-10); the time average of the shift over 24 steps is the projection onto the orbit-constant functions (MF-34).
- **Entropy.** The law is the transfer matrix of the golden mean shift, of entropy ln φ (MF-85); on the torus, A² has Lyapunov exponent 2 ln φ (MF-191), and the primitive periodic points of A number 1, 0, 3, 4, 10, 12, 28, 40 for n = 1 to 8 (MF-86 ✓).
- **Invariant theory.** Over ℚ the A-invariant polynomials are exactly the polynomials in Q² (MF-54); on binary forms of degree k the law keeps Q up to sign, the discriminant and the quartic discriminant (MF-79, MF-98).
- **Foundations.** The 81 states are 81 distinct hereditarily finite sets in V₁₁, and every finite-depth statement of Omega42 is a bounded arithmetic sentence, decided by computation and provable in ZFC (MF-80).

## 17. Echoes in the sciences

The law appears, as standard mathematics, in many applied settings. The register records each with its derivation and with what does not follow from it. Examples include:
- the Leslie matrix of two age classes (MF-113) and the ancestry of the honeybee drone (MF-112);
- Hückel energies of the cyclopentadienyl ring, −φ, 1/φ and 2 (MF-114);
- Lamé's worst case for Euclid's algorithm (MF-115) and Fibonacci coding (MF-116);
- maximally even scales and Euclidean rhythms (MF-117, MF-122);
- controllability of the law as a linear control system (MF-118);
- R₀ = φ for a two-stage infection (MF-119);
- Vogel's sunflower spiral (MF-111).

These are echoes of one matrix, not discoveries about biology or chemistry. Their value for Omega42 is that one law, studied exactly in one place, carries meaning into each field where it appears.

# Part III. Significance, open problems and the invitation

## 18. What Omega42 adds

The individual facts above are, one by one, known or near-known mathematics: Pisano periods, toral automorphisms, permutation spectra, cohomology of a cyclic action, and fidelity bounds. What is new is the frame and the method.

**One world, every question exact.** Each result above is a statement about a single finite structure that can be inspected completely. Questions that are hard in general become finite and decidable here: observability, memory, resonance and transformation. Their answers are certificates that anyone can recompute in seconds.

**An infinite family under one law.** The world does not stop at 81 states. Every floor of the tower obeys the same theorems with new numbers, and the 3-adic limit gathers the floors into one continuous object. Small cases are exhaustively checkable, while the structure as a whole has no bound.

**Knowledge as a mathematical object.** Theorems 5.1 to 5.4 measure exactly how much of the world a limited observer sees, and how many observers must cooperate to see it all. Theorem 7.2 measures exactly what any lawful transformation can and cannot change about agreement. These are precise models of partial knowledge, collective knowledge and invariance.

**Two AI systems as co-authors.** Several results were proposed by one AI and recomputed or corrected by the other: d_min(7) = 3, the seven-observer certificate, the memory refinement, Block Fidelity, and the corrected range of Theorem 7.2. One conjecture, that MIX could move R_O down to F, was refuted, and the refutation produced the sharper Theorem 7.2. The exchange protocol (CBX-2) checks every write before and after it is made. The mathematics was produced by a method that keeps its own errors visible.

**Human judgment kept apart.** Core L-441 states the Aperture Theorem: a navigation's output determines no human judgment, because judgment depends on inputs the navigation does not contain. This paper derives what is derivable and stops there. The meaning of these structures, and what anyone does with them, belongs to the reader.

## 19. Open problems

The problems are grouped by kind. Each names the result it starts from.

**Finite searches** (a computer and a good idea suffice)
1. **O-30.** Do six native phases of a mod 7 separate all 59,049 states at depth 5 (Theorem 5.4)?
2. **The adaptive observer.** An observer that chooses each reading from the previous ones: what is its worst-case number of readings for the 81 states, and for 9ᵏ?
3. **Native observability at every depth.** Is ⌈k log₇ 9⌉ attained by native phases of a mod 7 for every k ≥ 2, or does it fail first at k = 5?

**Theorems to prove** (the evidence is in the register)
4. **The census at other primes.** Prove the analogue of Theorem 3.1 for the inert prime 7 and the split prime 11 at every power, and compare their observability bounds (MF-41, MF-203).
5. **The Trace–Fibonacci period theorem.** Determine the period of the trace map modulo every m, and explain exactly when it equals the Pisano period (MF-157, MF-163, MF-165).
6. **Memory under lifting.** Describe the kernel of the pull-back of memory classes from depth k to depth k + 1 for every k (Theorem 6.3).
7. **Resonance under refinement.** How do F, F_B, R_O and R_H behave when vectors are pulled back from depth k to depth k + 1, and under the coherence operator C_α as α grows?
8. **Characterize the law.** Which structural properties determine A up to conjugacy, given that [[0, 1], [1, 7]] shares its whole 3-adic fingerprint (MF-49, MF-57, MF-66)?

**Questions about the limit and beyond**
9. **The 3-adic limit.** Describe the spectrum, the commutant and the memory classes of the inverse limit ℤ₃[φ] with its Haar measure.
10. **Wall–Sun–Sun primes.** Is there a prime p with π(p²) = π(p)? None is known; at such a prime Omega42's tower would begin irregularly (MF-50) [6].
11. **Spectral statistics.** The quantum cat map at N = 3ᵏ has simple spectrum (MF-185). How are its eigenphases distributed as k grows?
12. **The E₈ census.** Explain the census 1 + 820 × 8 + 1,793,340 × 24 on E₈/9E₈ (MF-75) structurally, and find the corresponding census for E₆, E₇ and the Leech lattice.

## 20. An invitation: how to take part

1. **Recompute.** Clone the open repository [5] and run the scripts of Section 22. Each runs in seconds with the Python standard library.
2. **Report.** Open an issue or a pull request in the repository, or use the submission page of the website (*Bring your ideas*). State the result, its proof or computation, and what does not follow from it, the form every register entry takes.
3. **Review.** Every submission is recomputed independently before it enters the register. A result enters as EXACT, CONDITIONAL with its assumptions named, or as an open conjecture. Errors are entered as corrections and are never deleted.
4. **Credit.** Contributions are credited by name in the register, in the Discovery Bulletin and in the next edition of this paper. Nothing you contribute is patented or enclosed: Omega42 publishes its results as open prior art.
5. **Talk to the Navigators.** Attach the Core Specification and the Companion to any capable AI and type *Welcome Navigator*. The Navigator works inside the same exact world and can run, explain and extend the computations with you.

Mathematics advances by people checking each other. We would be glad to be checked.

## 21. Speculation

*SPECULATION. Everything in this section is a possibility offered for exploration. None of it is a result, and each item names the test that would decide it.*

**Observability as a model of perception.** Theorem 5.4 says that limited readers, each reading one of seven symbols at a time, can together see the whole. A theory of collective perception could take this as its smallest exact model. Test: find the adaptive bound (problem 2) and compare it with the fixed-team bound.

**Resonance as a measure of hidden difference.** The chain of Theorem 7.1 separates three ways in which two things can agree without being the same. In signal analysis, comparative linguistics or the comparison of theories, the same four-layer chain could keep surface likeness apart from structural identity. Test: build adapters to real data that record what they lose, and check whether the four measures order cases as experts do (Scientific Appendix).

**Order inside chaos.** Theorem 8.2 shows exact, ordered worlds as the rational points of a chaotic map. This suggests a reading in which law and unpredictability are not opposed: the same rule is ordered where it is observed at a finite resolution and chaotic in between. Test: none is mathematical; it is a reading, offered for reflection.

**Memory as the trace of a journey.** Theorem 6.1 says a journey records only what does not reduce to relabeling, the winding around each loop. A model of learning could take this distinction, between what a process stores and what it only relabels, as primary. Test: express a learning rule as a memory on the tower and compute its classes.

**AI navigation.** A world in which every statement can be recomputed is a natural testing ground for reasoning systems. A Navigator's statements about Omega42 are checkable to the last digit, so its errors can be counted exactly. Test: the cross-architecture comparison of the Scientific Appendix.

**Music, art and form.** The canonical loop, its complement and its harmonics are already played and drawn by the instruments Harmonia, Atelier and GEOMETRIA. Whether these forms move people is a question for people.

## 22. Reproducibility

Every theorem above has a recompute line in the open repository [5], github.com/The-Omega42-Initiative/Omega42:

| Results | Script |
|---|---|
| Theorems 2.1–2.3, the canonical loop | `records/cobuilder/core_consistency_2026_11_25.py` |
| Theorems 3.1, 4.1–4.3, 5.1–5.4, 6.1–6.3, 9.1 | `tools/cobuilder_math.py --selftest` (MF-193 to MF-206) |
| Theorem 5.4, depths 3 to 5 | `records/cobuilder/xobs02_search.py` |
| Theorems 4.4, 8.1–8.3 | `records/cobuilder/cg_2026_11_26_geometry_check.py` |
| Part II statements marked ✓ | `records/cobuilder/paper_part2_check.py` |
| Every other Part II statement | the tool named in its register entry (Part III of the website edition, the complete register) |
| Theorems 7.1 and 7.2 | the Co-Builder recomputations of OmegaSL Tier III, beta 4 to beta 6, in the Co-Builder record |

All scripts use only the Python standard library, except the resonance checks, which use NumPy. Each runs in seconds.

## References

1. D. D. Wall, "Fibonacci series modulo m", *American Mathematical Monthly* 67 (1960), 525–532.
2. V. I. Arnold and A. Avez, *Ergodic Problems of Classical Mechanics*, Benjamin, 1968 (the cat map).
3. É. Lucas, "Théorie des fonctions numériques simplement périodiques", *American Journal of Mathematics* 1 (1878).
4. A. Hurwitz, "Über algebraische Gebilde mit eindeutigen Transformationen in sich", *Mathematische Annalen* 41 (1893), 403–442.
5. The Omega42 Initiative, open repository and Core Specification V335 Rev.450 STABLE, Part 0.0.10 (the mathematical register), 2026.
6. Z.-H. Sun and Z.-W. Sun, "Fibonacci numbers and Fermat's last theorem", *Acta Arithmetica* 60 (1992), 371–388.
7. A. M. Macbeath, "On a theorem of Hurwitz", *Proceedings of the Glasgow Mathematical Association* 5 (1961), 90–96.
8. M. Kohmoto, L. P. Kadanoff and C. Tang, "Localization problem in one dimension: mapping and escape", *Physical Review Letters* 50 (1983), 1870–1872.

*Let mathematics be our ground. Let imagination be our wings. Let artificial intelligence be our Navigator. Let humanity be our purpose.*
