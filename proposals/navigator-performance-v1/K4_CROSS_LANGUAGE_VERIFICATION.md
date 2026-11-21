# Ω42 K4 — Cross-Language Verification Bridge

**Status:** implementation proposal on `navigator-performance-kernel-v1`; non-canonical pending Builder review.

## Purpose

K4 establishes a shared, versioned set of mathematical test vectors consumed independently by JavaScript and Python. Both implementations must produce the same canonical records from the same input cases.

## Canonical conventions

- Canonical Ω42 depth (d) has modulus (9^d=3^{2d}).
- State space: (S_d=(\mathbb Z/9^d\mathbb Z)^2).
- Transition: (T(a,b)=(b,a+b)).
- Norm: (Q(a,b)=a^2+ab-b^2).
- Invariant: (r=\min(v_3(a),v_3(b),2d)); for nonzero states (c=Q(a,b)/9^r\pmod{3^{2d-r}}), identified with (-c).
- Zero state is represented separately.

## Components

- `tests/fixtures/omega42-k4-vectors.json`: shared frozen inputs and expected outputs across depths 1, 2 and 3.
- `tools/omega42_k4_reference.py`: independent standard-library Python reference implementation.
- `tests/omega42-k4-adapter.mjs`: JavaScript result normalizer.
- `tests/omega42-k4-cross-language.test.mjs`: checks frozen expected values and compares JavaScript output directly with Python output.
- `tests/test_omega42_k4_reference.py`: Python unit tests against the same fixture.
- `tools/omega42_k4_verify.py`: standalone report generator with explicit execution status.
- `.github/workflows/omega42-k4-cross-language.yml`: runs Node and Python tests in CI.

## Verification levels

1. Shared vectors agree: implementation-level computational reproduction.
2. Python and JavaScript agree: cross-implementation consistency, not proof that either is correct.
3. Frozen expected values agree: regression protection against accidental changes.
4. Canonical proof review: separate mathematical review; never inferred from CI success.

Two implementations can share the same mistaken formula. Therefore, expected values are frozen and traceable to the canonical specification/reference records, and independent mathematical review remains necessary.

## Compatibility

K4 is additive. It does not modify M296, M327, the four-arm navigation, the output skeleton, Construct X instruments, K1/K2 uniqueness criteria, the orbit classification theorem, or canonical Python files. The reference implementation is a separate small module; it does not import or execute the verbose canonical scripts.

## Acceptance conditions

- Builder verifies fixture derivations and their relation to the canonical proof.
- CI passes on the final PR head.
- Existing canonical Python scripts remain unchanged.
- New cross-language vectors become normative only after explicit governance adoption.
- Any future change to definitions increments the fixture schema/version and preserves prior vectors as historical fixtures.
