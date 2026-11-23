# D5 — Certificate Procedure Execution: Privilege Boundary Audit

**Status:** Source audit and design recommendations only. No certificate procedure has been executed by the Path B work.  
**Prepared:** 23 November 2026  
**Branch:** `proposal/path-b-release-packaging`  
**Source:** `tools/certify.py`  
**Authority:** Non-canonical proposal. No changes to `certify.py`, Core, Companion, CI or release policy.

## 1. D3 and D5 are separate capabilities

D3 validates certificate syntax and static fields. It can inspect:
- the certificate frame and field order;
- certificate kind and status;
- statement form;
- recorded result digest;
- scope and declared procedure text.

D3 must not execute the procedure named in the certificate.

D5 reruns a procedure and compares its output with the recorded result digest. This is a different privilege profile because certificate content can specify executable commands and a working directory.

The Path B D3 harness deliberately avoids `certify.py --selftest`: the current self-test calls `verify()`, which invokes `run_procedure()` and executes a test shell command. The D3 harness instead calls the static `check()` function and CLI `--check` only.

## 2. Current implementation findings

Source inspection of `tools/certify.py` establishes:

1. `run_procedure(f)` passes the certificate's `PROCEDURE` string to `subprocess.run(..., shell=True)`.
2. It captures stdout and stderr but has no timeout.
3. The procedure inherits the host's available filesystem, environment, network and process permissions; no sandbox is established in this function.
4. The working directory is formed from `ROOT` and the certificate's `CWD` value. There is no explicit resolved-path containment check preventing a relative `..` path from escaping the repository.
5. `verify()` compares the SHA-256 of stdout with the recorded digest, but currently does not include the subprocess return code in its `ok` decision. A command that emits the expected stdout and exits nonzero can therefore be reported as reproduced.
6. `REGISTERED` and `WITHDRAWN` certificates are treated as not rerun and return a successful status from `verify()`; that is a lifecycle decision, not evidence that the procedure was reproduced in this invocation.

These findings describe the current implementation. They do not establish that any archived certificate is malicious or unsafe.

## 3. Execution threat model

The certificate record is data, not a trusted executable manifest. A certificate may be contributed, imported or altered. Executing its `PROCEDURE` string with the host's ordinary shell privileges would permit the procedure to perform any action available to that account.

Risks include:
- reading or modifying files outside the package;
- network access and external data retrieval;
- long-running or non-terminating commands;
- process creation and resource exhaustion;
- shell metacharacter interpretation and command chaining;
- working-directory escape;
- a nonzero exit being treated as success if stdout matches.

The risk is not confined to third-party certificates. A locally authored certificate can contain an incorrect command, an unsafe path or a procedure whose behaviour changes over time.

## 4. Proposed D5 execution contract

Before any general D5 execution profile is adopted, define a separate execution contract with at least:

1. **Explicit authorisation:** execution is a distinct permission, not implied by reading a certificate or running D3.
2. **Structured command representation:** executable plus argument array; do not interpret a free-form shell string.
3. **Executable allow-list:** only approved interpreters and tools, pinned to known versions or digests.
4. **Path confinement:** resolve CWD and all declared inputs; reject paths outside the isolated package.
5. **Sandbox:** no ambient credentials, no host secrets, restricted filesystem, and network disabled by default.
6. **Resource limits:** timeout, memory/CPU limits, process limits and output-size limits.
7. **Deterministic environment:** explicit locale, timezone, environment variables and dependency versions.
8. **Exit semantics:** require exit code zero unless a certificate kind defines a different, explicit success mapping.
9. **Digest verification:** hash the precisely specified output stream and record stdout/stderr, exit code, command identity, environment and package digest.
10. **Reproducibility status:** distinguish reproduced, not reproduced, execution denied, timeout, procedure error and environment mismatch.
11. **No silent status mutation:** a failed reproduction may produce a withdrawal recommendation or status transition only through the authority defined by the canonical governance process; the runner itself must not silently rewrite a certificate.

A safer command schema is a structured executable/argument list. If backwards compatibility requires existing shell-string certificates, they should be treated as a legacy execution class and run only in a separately isolated, explicitly authorised environment.

## 5. Safe D5 boundary characterization — no procedure execution

A separate test script, `tools/path_b_d5_certificate_semantics_test.py`, has been added to characterize the current implementation without running any certificate procedure.

It:
- monkeypatches `certify.run_procedure()` to return the expected stdout digest together with exit code 17, then checks whether `verify()` still reports REPRODUCED;
- monkeypatches the procedure runner to raise if called while checking REGISTERED and WITHDRAWN lifecycle handling;
- inspects the source of `run_procedure()` for `shell=True`, absence of a timeout, and repository-root-relative CWD construction.

The test is designed to reproduce and report known implementation boundaries. It does not execute `PROCEDURE` text, invoke a shell, run an archived certificate, or implement a sandbox. It is included in the existing Path B prototype-isolation workflow so that the test can run without introducing an unregistered workflow file.

## 6. D5 test plan — not yet executed

When the Originator authorises a sandboxed D5 profile, its test suite should include:

- a known command that exits zero and reproduces the expected stdout digest;
- a command that emits the same stdout but exits nonzero;
- a command that emits a different stdout;
- a command that writes outside the package;
- a CWD traversal attempt;
- a timeout and process-tree termination test;
- network access denied by default;
- output-size and resource-limit violations;
- a missing executable or changed executable digest;
- REGISTERED and WITHDRAWN lifecycle behaviour;
- a certificate whose procedure changes after certification.

The negative controls must prove containment and denial, not merely that a benign command runs.

## 7. Current decision boundary

- D3 static syntax checking may proceed without procedure execution.
- D5 procedure execution has not been run as part of this work; the new safe characterization test uses a monkeypatched runner only.
- No archived certificate has been verified by this Path B D5 work.
- No canonical code has been modified.
- No shell command from a certificate has been executed by the D3 harness.
- The proposed sandbox/allow-list contract is not implemented or adopted.
- Any future execution requires explicit authorisation of the execution profile and its host boundary.

This audit is a technical review artefact, not legal advice, a certification result or a message to Claude.
