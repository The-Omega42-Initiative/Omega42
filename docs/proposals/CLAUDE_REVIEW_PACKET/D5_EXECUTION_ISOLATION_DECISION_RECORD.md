# D5 certificate execution — isolation decision record (proposal only)

**23 November 2026 — NOT APPROVED FOR EXECUTION.** This record distinguishes implemented *pure validation* from the safeguards needed before any certificate command can run.

## Existing evidence

Canonical `tools/certify.py::run_procedure` currently invokes `subprocess.run(procedure, shell=True, cwd=..., capture_output=True, text=True)` with no timeout, command allowlist or sandbox. `verify()` compares the stdout digest but does not require `returncode == 0`. REGISTERED/WITHDRAWN skip execution and may return a success-like result. These are observed semantics, not authorized changes.

Proposal-only, non-executing modules:

- `tools/path_b_d5_execution_preflight.py`: rejects shell metacharacters, unsafe CWD and non-executable statuses, but cannot establish whether an executable has side effects.
- `tools/path_b_d5_execution_contract.py`: checks supplied approval record against certificate, procedure digest, argv, CWD, scope, expiry and expected digest. The `approved_by` field is untrusted self-asserted text, **not** authenticated authorization.
- Synthetic tests for both. **No certificate procedure has been executed.**

## Threats and required controls

| Threat | Required control | Current status |
| --- | --- | --- |
| Shell chaining, expansion, injection | `shell=False` plus strict argv parser; never evaluate shell strings | Preliminary parser only |
| Executable can write/delete/phone home even without shell syntax | Separate low-privilege sandbox with read-only mounted inputs, no network, no credentials, writable ephemeral output only | Not implemented |
| Path traversal, symlinks, cwd race | Resolve against pinned immutable checkout; reject escape; avoid TOCTOU by sandbox mount policy | Static preflight only |
| Unlimited CPU, memory, file writes, output | Hard wall-clock timeout, CPU/memory/process/file/output quotas; kill process group | Not implemented |
| Exit failure producing expected stdout | Require exit code 0 **and** matching byte-level stdout digest | Not implemented |
| Encoding/newline ambiguity | Define exact bytes hashed, stdout/stderr capture limits and canonical digest version | Not decided |
| False or replayed approval | Originator-authenticated, signed, scoped, time-bounded, single-use authorization bound to repository commit, certificate bytes, command, inputs and sandbox profile | Not implemented |
| REGISTERED/WITHDRAWN misleading success | Distinguish SKIPPED, VERIFIED, FAILED, WITHDRAWN statuses and audit evidence | Not implemented |
| Compromised dependencies or PATH hijack | Pin interpreter/executable image and dependencies by digest, fixed PATH and environment | Not implemented |
| Procedure-specific non-determinism | Record deterministic inputs and permitted environmental variables; rerun in hermetic environment | Not implemented |
| Audit and repudiation | Immutable run ID, signed authorization reference, complete bounded result metadata, no secrets in logs | Not implemented |

## Proposed fail-closed gate sequence (design, not implementation)

1. Confirm Originator approval of the execution *policy itself*. No implicit approval from a green CI test.
2. Authenticate a separately issued single-use approval against trusted authority; bind to certificate content digest, repository commit, exact argv, input digests, sandbox image, CWD, output contract and expiration.
3. Validate certificate syntax, status and preflight; reject unsupported procedures.
4. Run only in a dedicated isolated worker with no ambient secrets/network, read-only inputs and quotas.
5. Compare bounded **raw stdout bytes** to approved SHA-256, require exit code 0, record stderr/exit/timeout separately.
6. Produce a signed auditable result; never mutate canonical certificate status automatically.

## Approval questions for Originator and Claude

- Is executable verification allowed at all in the proposed Path B architecture, or should D5 remain static/externally attested?
- Which deterministic executable images and procedure families are allowed?
- What authenticated approval mechanism and single-use replay prevention is acceptable?
- What exact byte/output/exit semantics should replace the current `stdout.encode('utf-8')` interpretation?
- How should REGISTERED/WITHDRAWN be represented without treating skipped procedures as reproduced?

**Decision:** Pending. The safest present behavior is **no execution**. Do not modify `tools/certify.py`, canonical documents or release gate without explicit Originator approval.
