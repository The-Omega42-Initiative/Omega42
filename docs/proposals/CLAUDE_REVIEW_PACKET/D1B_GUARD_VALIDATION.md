# D1b Experimental Guard — Validation Report

**Date:** 23 November 2026  
**Tested commit:** `4c96b226f8389e05554fc6d6f8cf1bc633ac9151`  
**Workflow:** [Path B prototype-isolation run 45152494717](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45152494717)  
**Result:** PASS

## Scope

The isolated D1b profile validates navigation and findings skeleton generation with a disposable package. It excludes repository research registers, canonical DOCX documents and the identity manifest.

The tested package contains:
- `scripts/canonical_reference.py`
- `scripts/m193_m225.py` (combined checker profile only)
- `tools/format_check.py`
- `tools/utility.py`
- `tools/manifestation.py`
- `tools/path_b_d1b_guard.py`

A second generation-only package omits M193/M225 and verifies that the scanner is not an active skeleton-rendering dependency.

## Executed assertions

The successful workflow executed these tests:

1. Original navigation skeleton contains the verbatim domain and MATH-GATE block.
2. Original findings skeleton contains FINDINGS BY AVENUE.
3. Guarded navigation generation succeeds with the complete four-file generation closure.
4. Guarded findings generation succeeds.
5. Combined format/skeleton self-test succeeds with the checker scanner present.
6. Generation-only guard succeeds without the optional M193/M225 scanner.
7. Guard rejects a package missing `utility.py`, with expected exit code 2 and required-file diagnostic.
8. Guard rejects a package missing `scripts/canonical_reference.py`, with expected exit code 2 and required-file diagnostic.
9. Negative control confirms the original generator still silently substitutes generic request placeholders when `utility.py` is missing.
10. Negative control confirms the original generator still exits successfully without canonical generated blocks when the canonical subprocess target is missing.

## Interpretation

**FORMALLY/EXPERIMENTALLY SUPPORTED:** The experimental wrapper prevents the two specific degraded-generation modes reproduced in the original generator, for the tested commands and package layouts.

**NOT ESTABLISHED:** This is not a proof that every D1b input branch, malformed file, filesystem error, subprocess failure mode, platform or future source revision is handled safely. It is not a canonical checker repair. It does not make the original generator fail closed when invoked directly.

The guard's passing tests should therefore be described as an isolated prototype validation, not as a universal guarantee of D1b correctness.

## Remaining technical review

Claude is asked to challenge:

- Whether the wrapper duplicates logic that should instead be refactored into a shared strict API.
- Whether its output checks are sufficient to detect truncated or semantically incomplete generated blocks.
- Whether it binds the exact source set and Core version strongly enough for a distributable package.
- Whether error handling is fail-closed for permission errors, timeouts, malformed subprocess output and unexpected exceptions.
- Whether findings generation truly has the same minimal source closure as navigation generation.
- Whether the four-file generation profile and five/six-file combined profile should be separate package manifests.

## Governance boundary

No canonical file, release extractor, CI policy, L-493 rule, main branch, PR, merge or deployment was changed by this validation. The wrapper remains proposal-branch experimental code.
