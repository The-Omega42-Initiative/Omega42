# Depth-r Fibonacci–shear exact orbit census

**Mathematics-only proposal, 23 November 2026.** Explicit enumerative corollary of canonical MF-43; the foundational orbit invariant is not new.

Let R_k=Z/(3^k), A(a,b)=(b,a+b), and B_r(a,b)=(a,b+3^r a), for 1<=r<=k. The existing register MF-43 establishes that the complete orbit invariant of a nonzero state x=3^j u, where u is primitive modulo 3^(k-j), is (j,Q(u)^2 mod 3^min(r,k-j)), with Q(a,b)=a²+ab−b².

## Theorem — complete orbit-size census

Fix a nonzero valuation shell j, 0<=j<k, and put n=k-j, h=min(r,n).

- The shell contains exactly **3^(h-1)** orbits.
- Every orbit in that shell contains exactly **8*3^(2n-h-1)** states.
- Zero is a singleton orbit.
- The total number of orbits is

\[
\boxed{\mathcal C(k,r)=\frac{3^r+1}{2}+(k-r)3^{r-1}}.
\]

At r=1 this gives k+1 orbits (MF-42); at r=k it gives (3^k+1)/2, the unsheared Fibonacci census.

## Proof

Division by 3^j identifies shell j with primitive vectors modulo 3^n. Reduction to 3^h is surjective, with 3^(2(n-h)) lifts of each primitive vector. MF-39 gives exactly 4*3^(h-1) primitive vectors per unit norm value modulo 3^h. The square of the norm identifies exactly the two unit values q and −q: if q²=q'² mod 3^h, then (q−q')(q+q')=0; exactly one factor is a unit modulo 3, hence the other must vanish modulo 3^h. There are 2*3^(h-1) units, so exactly 3^(h-1) unit norm-square classes.

Each class has 2*4*3^(h-1)*3^(2(n-h)) = 8*3^(2n-h-1) primitive lifts. The **completeness** of MF-43's invariant identifies each class with exactly one orbit. Summing the counts over n=1..k, plus the zero orbit, gives

\[
1+\sum_{n=1}^{k}3^{\min(r,n)-1}
=1+\frac{3^r-1}{2}+(k-r)3^{r-1}.
\]

QED, conditional on the already established MF-43 theorem.

## Concrete finite checks

For k=4, the orbit-count sequence at r=1,2,3,4 is **5,11,23,41**. A full multiset of orbit sizes is obtained by including one singleton and, for each n=1..k, exactly 3^(min(r,n)-1) copies of size 8*3^(2n-min(r,n)-1).

Independent breadth-first orbit enumeration using the **lower** shear B_r(a,b)=(a,b+3^r a) was executed locally for every pair 1<=r<=k<=4. All ten orbit-size multisets agreed exactly with the formula; the norm-square invariant was constant on each enumerated orbit. A committed independent checker is provided in tools/path_b_depth_shear_census_test.py. No GitHub CI result is claimed.

## Interpretation boundary

This theorem quantifies how a depth-r shear coarsens the Fibonacci orbit partition: for k>r, the orbit count grows linearly in k with slope 3^(r-1), rather than exponentially. This is finite algebra, not a physical probability or semantic selection law. The website, canonical Core and Companion remain unchanged.
