# MOR-02b — quadratic norm classifies every primitive Fibonacci orbit modulo 3^k

**Status:** Proposal-only theorem and proof, 23 November 2026. Independent peer review pending. No website or canonical changes.

Let R_k = Z/(3^k), k >= 1, and T(a,b)=(b,a+b). Define

Q(a,b)=a^2+ab-b^2 (mod 3^k).

A vector is **primitive** if a or b is not divisible by 3.

## Theorem: complete primitive orbit invariant

For primitive vectors u,v in R_k^2,

**u and v belong to the same T-orbit if and only if Q(v) = Q(u) or Q(v) = -Q(u) modulo 3^k.**

In particular, primitive cycles are in bijection with the unit classes R_k^×/{q ~ -q}. There are 3^(k-1) such cycles, each of length 8*3^(k-1).

For arbitrary nonzero vectors modulo 3^k, first extract the common 3-adic valuation s; write (a,b)=3^s(u_1,u_2), where u is primitive modulo 3^(k-s). The pair

(s, {Q(u), -Q(u)} modulo 3^(k-s))

completely classifies its orbit. The zero vector is a separate fixed point. This is a classification of *finite dynamical orbits*, not of physical states.

## Proof

**1. Alternating norm.** Direct expansion yields

Q(T(a,b)) = b^2+b(a+b)-(a+b)^2 = -Q(a,b).

Thus {Q,-Q} is constant along every orbit.

**2. Primitive Q is a unit.** Modulo 3, the polynomial Q is anisotropic: Q(a,b)=0 implies a=b=0. For b != 0, write t=a/b. Then Q/b^2=t^2+t-1; its discriminant is 5=2 modulo 3, not a square. If b=0, Q=a^2 !=0 for a!=0. Therefore Q(u) is invertible whenever u is primitive.

**3. Every unit occurs as Q(u).** For modulus 3, Q(1,0)=1 and Q(0,1)=-1, the two units. Suppose Q(u)=q modulo 3^j with u primitive. A lift u+3^j(h,l) satisfies

Q(u+3^j(h,l)) = Q(u)+3^j[(2a+b)h+(a-2b)l] (mod 3^(j+1)).

The gradient (2a+b,a-2b) cannot vanish modulo 3 for primitive u: its coefficient matrix has determinant -5, a unit modulo 3. Therefore choosing h,l modulo 3 reaches any prescribed next base-3 digit. Induction gives surjectivity onto R_k^×.

**4. The invariant is complete.** The unit group has 2*3^(k-1) elements, and negation has no fixed unit because 2 is invertible modulo 3. Hence there are 3^(k-1) sign classes. The previously established orbit theorem (MOR-02) independently gives exactly 3^(k-1) primitive T-orbits, each of length 8*3^(k-1). Each orbit maps to one sign class by step 1; all sign classes occur by step 3. A surjection between two finite sets of equal cardinality is a bijection. This proves the claim.

**5. Nonprimitive states.** Division by the maximal common power 3^s is a bijection between valuation-s states modulo 3^k and primitive states modulo 3^(k-s), and it intertwines T. Apply the primitive classification at the reduced modulus.

## Connection with the quadratic field

Let phi=(1+sqrt(5))/2 and phi'=(1-sqrt(5))/2, so phi+phi'=1 and phi*phi'=-1. For z=a+b*phi, the field norm is

N(z)=(a+b*phi)(a+b*phi')=a^2+ab-b^2=Q(a,b).

Multiplication by phi sends a+b*phi to b+(a+b)*phi, exactly the Fibonacci transformation T. Since N(phi)=-1, the alternating norm is explained by multiplicativity of the field norm.

The polynomial x^2-x-1 is irreducible modulo 3 (discriminant 5 is nonsquare), so the quadratic algebra R_k[phi] is an unramified quadratic extension at 3. The orbit classification can therefore be read as a norm-class classification of multiplication-by-phi orbits on its underlying additive module.

**Scope caution:** the norm relation is an exact algebraic correspondence, not evidence that the recurrence generates physical existence or that a particular numerical feature is unique to Omega42.

## Reproduction and falsification

Independently enumerate every orbit for k=1..4 and compare its set of Q-values against the predicted two-element sign class. Check that different orbits within a valuation stratum have different sign classes, and that every unit sign class is represented. The test should derive cycles by applying T, not from the proposed invariant.

## Open problems

- Extend the classification to other primes and determine which primes split, ramify, or remain inert in Q(sqrt(5)).
- Characterise invariant measures and orbit closures of multiplication by phi on Z_3[phi].
- Determine which norm-based features survive observational noise or coarsening without attributing untested semantic meaning.
