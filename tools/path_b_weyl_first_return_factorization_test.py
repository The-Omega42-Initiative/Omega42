#!/usr/bin/env python3
"""Exact symbolic first-return determinant certificates for syndrome cycle blocks.

Requires sympy. Run: python tools/path_b_weyl_first_return_factorization_test.py
"""
from sympy import Matrix, diag, symbols
z = symbols("z")
for L in (1, 4, 12):
    for d in (1, 2, 3):
        B = diag(*([2, -3, 5][:d]))
        U = Matrix.zeros(L*d)
        for j in range(L-1):
            for a in range(d):
                U[(j+1)*d+a, j*d+a] = 1
        for a in range(d):
            U[a, (L-1)*d+a] = B[a,a]
        expected = 1
        for a in range(d):
            expected *= z**L-B[a,a]
        assert U.charpoly(z).as_expr().expand() == expected.expand()
        assert U**L == diag(*([B]*L))
        print(f"PASS L={L}, d={d}: exact determinant and first-return powers")
