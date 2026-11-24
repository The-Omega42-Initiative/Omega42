# RST-01 — Recursive Spectral Transform research instrument
24 November 2026. Proposal only; no canonical or deployment change.

At each level define a=J*psi and d=psi-Ja. Since J*J=I, J*d=0, psi=d+Ja, and ||psi||²=||d||²+||a||². Recursively apply to a until dimension 1 or 3. This yields a reversible orthogonal layer decomposition; stored ambient detail vectors are redundant, not compressed coefficients. Independent spectral mode uses Pi_j psi = L^(-1) sum_m exp(-2πijm/L)V^m psi. All components reconstruct psi. Neither filtering nor discarding components is generally reversible.

Prototype executed locally with deterministic complex inputs (seed 42). Dimensions 3,9,27,81,243: reconstruction errors 0,2.7972e-17,1.4305e-17,2.4885e-17,1.9983e-17; energy errors <=2.23e-16. Spectral mode tested at 3,9,27,81: reconstruction errors <=4.46e-16, energy errors <=4.14e-14. These are actual numerical checks of the local prototype, not CI. Next: compact orthonormal layer coordinates and independent spectral classification audit. Prior numerical claims lacking recorded execution must be rerun. RST is a research instrument, not demonstrated advantage over FFT or conventional transforms.
