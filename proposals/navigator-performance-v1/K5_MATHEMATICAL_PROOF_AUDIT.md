# Ω42 K5 — Mathematical Proof Audit and Tower Consistency

**Status:** additive review proposal on `navigator-performance-kernel-v1`; non-canonical pending Builder review.  
**Scope:** canonical finite tower, orbit invariant Λ, order/census/lifting, and frozen K1/K2 selection criteria.  
**Not a theorem-prover:** the accompanying audit utility checks proof-obligation metadata and dependency integrity. It does not certify mathematical validity.

## 1. Convention lock

Use one symbol for each level:

- Generic exponent: (n\geq1), modulus (3^n).
- Canonical Ω42 depth: (d\geq1), with (n=2d).
- Canonical modulus: (9^d=3^{2d}).
- Ring: (R_n=(\mathbb Z/3^n\mathbb Z)[\phi]), where (\phi^2=\phi+1).
- State: (x=a+b\phi\leftrightarrow(a,b)).
- Transition: (T(a,b)=(b,a+b)), multiplication by (\phi).
- Norm: (Q(a,b)=N(x)=a^2+ab-b^2).

The generic (3^n) statements below apply at every (n); canonical Ω42 depth (d) means substitute (n=2d). Never call generic exponent (n) “Ω42 depth”.

## 2. Algebraic preliminaries

### Lemma 2.1 — Transition and norm

Multiplication by (\phi) gives
[
\phi(a+b\phi)=b+(a+b)\phi,
]
hence (T(a,b)=(b,a+b)). The conjugate of (\phi) is (1-\phi), so
[
N(a+b\phi)=(a+b\phi)(a+b(1-\phi))
=a^2+ab-b^2.
]
Also (N(\phi)=-1), therefore
[
Q(T(a,b))\equiv-Q(a,b)\pmod{3^n}.
]
The norm up to sign is invariant.

### Lemma 2.2 — Unit criterion and valuation

The polynomial (X^2-X-1) has no root modulo 3 (test residues 0, 1, 2). Thus
[
R_1\cong\mathbb F_9.
]
An element (a+b\phi\in R_n) is a unit exactly when ((a,b)\not\equiv(0,0)\pmod3). If
[
r=\min(v_3(a),v_3(b),n),qquad x=3^r u,
]
then (u) is a unit in (R_{n-r}), unless (r=n), which is the zero state. Since the norm of a unit is a unit,
[
v_3(Q(a,b))=2r
]
when interpreted below the modulus' truncation; equivalently the divided norm (Q(a,b)/9^r) is a unit modulo (3^{n-r}) for every nonzero state.

## 3. Exact order of the transition

Let
[
A=\begin{pmatrix}0&1\\1&1\end{pmatrix}.
]
Modulo 3, (A^4=-I) and (A^8=I), so the order is 8. Direct integer multiplication gives
[
A^8=I+3C,qquad
C=\begin{pmatrix}4&7\\7&11\end{pmatrix},
qquad \det(C)=-5\not\equiv0\pmod3.
]
Inductively, if (A^{8\cdot3^j}=I+3^{j+1}C_j) with (C_j\equiv C\pmod3), then cubing gives
[
A^{8\cdot3^{j+1}}
=(I+3^{j+1}C_j)^3
\equiv I+3^{j+2}C_j\pmod{3^{j+3}}.
]
Thus the first nonzero 3-adic order of (A^{8\cdot3^j}-I) is exactly (j+1). Since the order modulo 3 is 8, the exact order modulo (3^n) is
[
\operatorname{ord}_{3^n}(A)=8\cdot3^{n-1}.
]
This is an all-(n) argument; finite matrix checks are corroboration, not the proof.

## 4. Norm-surjectivity and the complete orbit invariant

### Lemma 4.1 — Norm surjectivity on units

The residue-field norm (\mathbb F_9^\times\to\mathbb F_3^\times) is onto: the multiplicative groups are cyclic of orders 8 and 2, and the norm is (z\mapsto z^4).

Lift this one 3-adic digit at a time. For (j\geq1),
[
N(1+3^jz)
\equiv1+3^j\operatorname{Tr}(z)\pmod{3^{j+1}}.
]
The trace (\mathbb F_9\to\mathbb F_3) is onto (in particular, (\operatorname{Tr}(1)=2\ne0)). Therefore a correction factor (1+3^jz) can adjust the next norm digit arbitrarily. Induction proves
[
N:R_n^\times\twoheadrightarrow(\mathbb Z/3^n\mathbb Z)^\times.
]

### Lemma 4.2 — Powers of φ are precisely the norm ±1 units

The unit group has size
[
|R_n^\times|=3^{2n}-3^{2n-2}=8\cdot3^{2n-2}.
]
The target unit group has size (2\cdot3^{n-1}). By surjectivity, the preimage of ({+1,-1}) has size
[
\frac{|R_n^\times|}{2\cdot3^{n-1}}\cdot2
=8\cdot3^{n-1}.
]
Every power of (\phi) has norm (\pm1), and the order result above says there are exactly (8\cdot3^{n-1}) such powers. Hence
[
\langle\phi\rangle
=\{u\in R_n^\times:N(u)=\pm1\}.
]

### Theorem 4.3 — Complete orbit classification

For units (x,y\in R_n^\times), they lie in the same (T)-orbit exactly when
[
N(x)\equiv\pm N(y)\pmod{3^n}.
]
Indeed, (y/x) is a unit, and the norm condition is equivalent to (N(y/x)=\pm1), which by Lemma 4.2 is equivalent to (y/x\in\langle\phi\rangle).

For a nonzero state (x=3^r u), reduce to the unit (u\in R_{n-r}^\times). Its orbit is classified by
[
r=\min(v_3(a),v_3(b),n),\qquad
c=\frac{Q(a,b)}{9^r}\pmod{3^{n-r}},
]
where (c\sim-c). The zero state is a separate fixed orbit. Therefore Λ is complete at every finite depth (n), and in canonical Ω42 notation (n=2d).

**Status:** proof reconstructed from the stated ring and group facts. Builder should compare each lemma with the canonical Companion Part 102 proof before adopting this text as normative.

## 5. Orbit census and lifting

At valuation (r<n), set (m=n-r). Unit orbits are cosets of (\langle\phi\rangle), so their number is
[
\frac{|R_m^\times|}{8\cdot3^{m-1}}=3^{m-1},
]
and each has period (8\cdot3^{m-1}). Add the zero fixed point. Thus, modulo (3^n), there are:
- one fixed zero orbit;
- for each (m=1,\ldots,n), exactly (3^{m-1}) orbits of length (8\cdot3^{m-1}).

The total number of orbits is
[
1+\sum_{m=1}^{n}3^{m-1}=\frac{3^n+1}{2},
]
and the state count is
[
1+\sum_{m=1}^{n}3^{m-1}(8\cdot3^{m-1})
=1+8\sum_{j=0}^{n-1}9^j=9^n.
]
Reduction (R_{n+1}\to R_n) commutes with (T), because the transition matrix has integer entries. The orbit classification also gives the lift pattern: the zero orbit lifts to zero plus one 8-cycle; every nonzero orbit lifts to three cycles, each with three times the period. One canonical Ω42 depth step is two generic exponent steps.

## 5A. Canonical-depth census examples

Substitute (n=2d) into the generic census:

| Canonical depth (d) | Modulus | States | Orbits | Period distribution |
|---:|---:|---:|---:|---|
| 1 | 9 | 81 | 5 | (1\times1, 1\times8, 3\times24) |
| 2 | 81 | 6,561 | 41 | (1\times1, 1\times8, 3\times24, 9\times72, 27\times216) |
| 3 | 729 | 531,441 | 365 | (1\times1, 1\times8, 3\times24, 9\times72, 27\times216, 81\times648, 243\times1944) |

The number before each multiplication sign is the number of orbits of that period. The longest-period orbit counts are therefore 3, 27 and 243 at depths 1, 2 and 3 respectively. K2 selects the one among these that contains the frozen seed; it does not imply there is only one longest-period orbit.

### Worked invariant calculation at depth 2

At (d=2), (n=4), modulus (81):

- Seed (x=(2,5)): (r=0), (Q=4+10-25=-11), so (c=-11\pmod{81}=70\sim11). Its period is (8\cdot3^3=216).
- Scaled state (3x=(6,15)): (r=1), (Q=-99), so (Q/9=-11\pmod{27}=16\sim11). Its period is (8\cdot3^2=72).
- Zero state ((0,0)): separate fixed orbit of period 1.

These illustrate why the valuation component matters: the two nonzero states share the same reduced norm representative up to sign, but their valuation depths and periods differ.

## 6. K1/K2 criteria: precise interpretation

### K1 — first-coordinate coverage

For a unit state (u), its orbit has maximum period (8\cdot3^{n-1}). We show that its first coordinate visits every residue (t\pmod{3^n}).

Choose (\epsilon\in\{+1,-1\}) so that
[
\Delta=5t^2-4\epsilon N(u)\equiv1\pmod3.
]
Such a sign always exists: if (t\equiv0\pmod3), choose the sign making (-\epsilon N(u)=1\pmod3); if (t\not\equiv0\pmod3), the two choices give residues 0 and 1, so choose 1. Since (\Delta\equiv1\pmod3), Hensel lifting gives a square root (s\pmod{3^n}). Set
[
b=(t+s)/2\pmod{3^n}.
]
Then (Q(t,b)=\epsilon N(u)), so ((t,b)) is a unit in the same orbit as (u) by Theorem 4.3. Thus the orbit contains a state with first coordinate (t). As (t) was arbitrary, every residue occurs.

Conversely, if a state is not a unit, both coordinates are divisible by 3 and remain so throughout its orbit; its first coordinate cannot visit every residue. Therefore, for (n\geq1):
[
\text{K1 coverage}\iff\text{unit state}\iff\text{maximum-period orbit}.
]
This proves the K1 criterion for every generic exponent (n), hence every canonical depth (d).

### K2 — frozen seed (2,5)

The seed is a unit because its coordinates are not both divisible by 3. It therefore lies on a maximum-period orbit. Orbits partition the state space, so this exact state occurs once among all disjoint maximum-period orbits.

**Interpretation correction:** the implemented K2 count is a deterministic membership selector for the orbit containing (2,5). Its “exactly once” count is automatic once the seed is known to lie on a maximum-period orbit. It is not a second independent classification theorem and does not imply that there is only one maximum-period orbit. There are (3^{n-1}) maximum-period orbits modulo (3^n), and (3^{2d-1}) at canonical depth (d).

## 7. Audit findings in the existing reference scripts

The canonical scripts are valuable reference records, but their printed labels should distinguish exhaustive finite computation from sampled checks and all-depth proof.

Examples in `records/tower/arithmetic.py`:
- Section I samples norm multiplicativity at (n=3) using `S[::7]` and `S[::11]`; the output phrase “for every pair” is too broad for that run.
- Section II samples the (n=6) valuation check (every 7th (a), every 5th (b)); the section banner says `[EXACT]`.
- Section III checks the order-lifting matrix condition only for (r=0,\ldots,5); the all-(r) conclusion needs the induction, not that finite loop.
- Sections V–VII exhaust finite moduli only through (n=6); they do not themselves prove the all-depth invariant or lift theorem.
- Section X checks two moduli and a finite list of exponents, not every (n,k).
- Section XV samples the (n=4,6) norm-turnover checks.

Recommendation: label each output separately as `EXHAUSTIVE_FINITE`, `SAMPLED_FINITE`, or `SYMBOLIC_PROOF_REFERENCE`. A script banner must not promote a sampled loop to exhaustive verification. Retain the original scripts unchanged in this proposal; update labels only through Builder-approved canonical edits.

## 8. K3/K4 consistency and implementation boundaries

- K3 computes (r) from the canonical modulus (9^d=3^{2d}), and computes (c=Q/9^r\pmod{3^{2d-r}}), up to sign.
- K4 compares JavaScript and Python outputs against shared fixtures. This is cross-implementation consistency, not a proof of the formula.
- K3 finite census and K4 fixtures are computational corroboration. The all-depth force comes from Sections 2–6.
- K1/K2 selection criteria remain distinct from Λ.
- A lexicographic cycle address remains a display/indexing convention, not the classification invariant.

## 9. Builder actions

1. Compare the reconstructed lemmas with Companion Part 102 and preserve canonical wording where it is stronger or more precise.
2. Review the Hensel-lifting argument for K1 and the membership-only interpretation of K2.
3. Add explicit proof-status labels to the arithmetic script output in a separate governed change.
4. Run canonical repository CI and K2–K5 tests on the exact PR head.
5. Keep K5 proposal-only until mathematical review and governance acceptance.
6. Do not infer a proof of any physical, consciousness, temporal, or semantic interpretation from this finite-ring theorem.

## 10. What this establishes—and what it does not

This audit gives an all-depth finite-ring argument for the orbit invariant and census, conditional only on the stated algebraic definitions and standard finite-ring/Hensel arguments supplied above. It also gives an all-depth proof of K1 and clarifies K2's logical role.

It does **not** validate broader philosophical interpretations, prove a connection between the 24-position question protocol and the 3-adic tower, or certify the website/runtime implementation. Those remain separate questions.
