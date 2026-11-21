# Ω42 K3 — Research Infrastructure and Compatibility Layer

**Status:** proposal implementation on `navigator-performance-kernel-v1`; non-canonical pending Builder review.

## Why K3 exists

K1/K2 added a generic (3^k) orbit utility. The canonical Ω42 tower, however, is indexed by depth (d) with modulus (9^d=3^{2d}). K2's `k=2` sample at modulus 9 is therefore Ω42 depth 1. K3 adds explicit Ω42-depth wrappers and preserves the generic utility without changing its semantics.

## Canonical orbit classification

For (S_d=(\mathbb Z/9^d\mathbb Z)^2), let (n=2d), (Q(a,b)=a^2+ab-b^2), and
(r=\min(v_3(a),v_3(b),n)). For nonzero states define
(c=Q(a,b)/9^r\pmod{3^{n-r}}). The orbit invariant identifies (c) with (-c), choosing the smaller residue as its canonical encoding. The zero state is separate.

This is the invariant already encoded by `records/tower/arithmetic.py` and described by the canonical mathematical record. K3's implementation is an additional executable check; it does not amend that proof or replace the canonical Python reference.

## K3 components

- `site/omega42-research.mjs`: canonical Ω42 depth/modulus adapter, exact BigInt Λ computation, exhaustive finite orbit census, typed research-graph validation.
- `schemas/research-graph-k3.schema.json`: machine-readable graph schema with provenance and three distinct verification levels.
- `tests/omega42-research.test.mjs`: depth mapping, sample orbit, invariant preservation, zero state, exhaustive depth-1 and depth-2 census, graph integrity.
- `site/navigator_workbench_k3.html`: browser-facing invariant explorer and research-graph validator.
- `.github/workflows/omega42-k3-tests.yml`: Node test workflow.

## Compatibility contract

1. Existing Core, Companion, M296 anchor/arms, M327 trigger register and all canonical instruments remain authoritative.
2. K3 is additive. It does not change a trigger, instrument selection, coordinate, anchor, arm, output skeleton or proof criterion.
3. Generic K2 `analyzeOrbit({k})` remains a (3^k) utility. Ω42 users should call `analyzeOmega42Orbit({depth})`, which uses (9^{depth}).
4. The lexicographic cycle address is secondary. The canonical invariant Λ is the classification key.
5. The census routine is an exhaustive finite computation subject to a state-space cap. It is not, by itself, a proof for all depths.
6. The repository's arithmetic proof remains the source of the all-depth theorem. K3 checks selected finite depths and detects implementation divergence.
7. New graph records preserve claim status, provenance, dependencies and independent review state. No AI consensus is treated as mathematical proof.

## Existing instrument impact

| Existing component | K3 impact |
|---|---|
| Canonical question coordinate / M296 | None; K3 does not calculate or replace it |
| M327 instrument triggers | None; K3 does not add or override triggers |
| Four-arm navigation and output | None |
| Existing Construct X instruments | None; no existing tool file is overwritten |
| Canonical arithmetic scripts | None; they remain reference implementations |
| Knowledge Register | K3 proposes a typed research graph alongside it; migration is optional and must preserve existing records |
| Orbit Explorer | K3 adds an Ω42-depth mode and Λ display; generic K2 mode remains available |
| Uniqueness/classification proof | No alteration; K3 supplies finite computational cross-checks only |

## What the uniqueness proof says—and what K3 does not claim

The repository's tower arithmetic states that the loop is completely determined by the valuation depth (r) and the norm (Q/9^r) up to sign. The proof and its hypotheses live in the canonical mathematical document and are represented in `records/tower/arithmetic.py`. K3's exhaustive enumeration at depths 1 and 2 checks that:
- Λ is constant along each computed orbit;
- distinct computed orbits have distinct Λ values;
- every state is visited exactly once;
- orbit counts agree with the canonical finite census (5 and 41).

These are finite checks. They do not prove the general classification theorem. The theorem's all-depth force comes from its mathematical derivation, not from passing a test suite.

K3 also reproduces the separate frozen depth-uniqueness criteria K1/K2 recorded in `records/tower/nested.py` (SEQ 49; Core MATH-32 to MATH-40, L-523):
- K1: the first coordinate visits every residue; the qualifying loops are exactly the longest-period loops.
- K2: after selecting the longest-period loops, the frozen seed (2,5) occurs exactly once.
The implementation reports these as finite checks at depths 1–3 (expected longest periods 24, 216, 1944; 3, 27, 243 longest loops respectively). These criteria are distinct from the complete orbit invariant Λ. They are not changed, redefined, or promoted by K3.

## Three verification levels

- **Level 1 — computational reproduction:** implementation agrees with specified finite cases.
- **Level 2 — mathematical review:** definitions, proof, edge cases and all-depth argument reviewed independently.
- **Level 3 — application validation:** instrument improves a declared operational task against suitable controls.

A pass at Level 1 never automatically promotes Level 2 or Level 3.

## Builder acceptance gates

- Review the depth convention and adapter names.
- Compare K3 results with `records/tower/arithmetic.py` and `records/tower/nested.py`.
- Run full canonical CI and independent review of the all-depth proof.
- Review graph schema, claim status vocabulary and migration policy.
- Browser accessibility/security review before deployment.
- Keep this proposal separate until formally adopted.
