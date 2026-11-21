# Ω42 K2 Instrument Engine

**Status:** proposal implementation; not canonical or independently certified.

## Services

- `modulus3(k)`: exact BigInt construction of 3^k, bounded to k=1..30.
- `fibonacciStep(state, modulus)`: exact modular Fibonacci transition.
- `analyzeOrbit({k,state,maxStates})`: computes transient and cycle, records states, and emits a deterministic cyclic-rotation address.
- `verifyOrbitResult(result)`: checks metadata, representative consistency and each cycle transition.
- `validateOmegaSL(record)`: validates a deliberately small typed-envelope vocabulary.
- `temporalDifferences(values,lag)`: computes finite first, lagged and second-lag differences.

## Address convention

For a computed cycle, select the lexicographically least cyclic rotation using numeric pair ordering. This creates a deterministic address for a cycle already found. It does not prove the project's general orbit-classification theorem and must not replace the canonical invariant Λ without Builder approval.

## Limits

- Modular arithmetic uses JavaScript BigInt.
- k is limited to 1–30; orbit enumeration has an explicit state cap.
- Temporal calculations use IEEE-754 numbers, not exact rational arithmetic.
- OmegaSL is a small K2 envelope validator, not a complete parser/compiler.
- Verification checks the supplied cycle; it is not a cryptographic signature or proof certificate.

## Run tests

Node.js 18+: `node --test tests/omega42-engine.test.mjs`

## Builder acceptance criteria

1. Compare k=1..4 periods and orbit counts against canonical reference code.
2. Add exhaustive state-space tests for k=1..3.
3. Verify canonical address consistency for every starting state on each cycle.
4. Freeze the OmegaSL schema and add positive/negative fixtures.
5. Define exact-number policy for temporal operations before proof-bearing use.
6. Add browser integration, accessibility and security tests.
