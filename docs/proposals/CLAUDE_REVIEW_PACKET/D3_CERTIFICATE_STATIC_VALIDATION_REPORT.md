# D3 — Static Certificate Validation Report

**Status:** Static checker and experimental strict wrapper passed isolated validation.  
**Prepared:** 23 November 2026  
**Branch:** `proposal/path-b-release-packaging`  
**Canonical checker:** `tools/certify.py`  
**Experimental guard:** `tools/path_b_d3_certificate_guard.py`  
**Harness:** `tools/path_b_d3_certificate_test.py`  
**Workflow:** `.github/workflows/path-b-d3-certificate.yml`  
**Latest workflow:** [45174322889](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45174322889) — PASS

## 1. Capability boundary

D3 is static certificate validation. It may inspect the certificate frame, field order, declared kind/status, digest syntax, statement and declared CWD. It must not execute the certificate's `PROCEDURE` field.

D5 is procedure execution and digest reproduction. It is a separate privileged capability and is not part of this test.

The harness deliberately does not run `certify.py --selftest`. The canonical self-test calls `verify()`, which invokes `run_procedure()` and executes a shell command. D3 uses `--check`, `--list`, and direct calls to the static `check()` function only.

## 2. Canonical checker and package profile

The isolated package contains:

- `tools/certify.py`;
- `records/certificates/CERT-*.txt` (10 archived certificate records).

The harness checks the complete archived certificate corpus with `certify.py --check`, invokes the non-executing inventory command `--list`, and tests a filled synthetic certificate.

It also places a synthetic side-effect command in the `PROCEDURE` field and verifies that `--check` does not create the side-effect file. This is a direct static/execution boundary control.

## 3. Canonical checker weaknesses reproduced by source and controls

The canonical `certify.check()` validates field presence/order and several content constraints, but it does not enforce field uniqueness or reject every blank field. The harness probes:

- blank `SUBJECT`;
- duplicate `SUBJECT`.

The current canonical checker accepts those malformed cases. The canonical checker is not modified.

## 4. Experimental Path B strict guard

The separate `tools/path_b_d3_certificate_guard.py` delegates to canonical `certify.check()` and adds package-profile checks:

- exactly one balanced certificate block per file;
- exactly one line for each required certificate field;
- nonblank required identity/content fields;
- `CERTIFICATE` identifier format `CERT-####`;
- relative CWD confined by rejecting absolute paths and `..` path segments, including normalized Windows path forms;
- lowercase 64-character SHA-256 unless the status is `REGISTERED`;
- nonempty finding after the phrase `Ω42 certifies`.

The guard is experimental. It is not canonical policy and does not execute the procedure.

## 5. Strict negative controls

The harness requires the strict guard to reject:

1. blank SUBJECT;
2. duplicate SUBJECT;
3. malformed certificate identifier;
4. parent-directory CWD traversal;
5. Windows UNC CWD;
6. invalid result digest;
7. duplicate certificate block;
8. an unmatched extra opening marker;
9. an unmatched extra closing marker.

The canonical checker may accept some of these controls; that difference is recorded rather than hidden. The strict guard must reject all nine.

## 6. Execution safety

- No archived certificate procedure is run by this D3 harness.
- No `--verify` command is invoked.
- No shell command from a certificate is executed.
- No procedure output digest is recomputed.
- D5 remains unimplemented and unauthorised for this work.
- The D5 boundary audit remains the source for the threat model and future execution contract.

The static package does not prove that future procedure execution is safe. CWD lexical checks do not establish filesystem sandboxing, symlink containment, network isolation, resource limits or process isolation.

## 7. Workflow and authority

The latest isolated workflow [45163029395](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45163029395) was queued at last check. No result is assumed.

- Path B remains a proposal.
- Canonical `certify.py`, Core, Companion, CI policy and L-493 are unchanged.
- The strict guard is experimental.
- No certificate procedure has been executed by this work.
- No certificate has been re-certified or withdrawn.
- No package has been released.
- This report is a review artefact, not a message to Claude. No Claude communication has occurred.
