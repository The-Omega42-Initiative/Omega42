# Path B D1b Skeleton-Generation Dependency and Failure-Mode Audit

**Status:** Source-level trace with isolated prototype testing  
**Version:** 0.1  
**Prepared:** 23 November 2026  
**Source baseline:** `main` at `423102f52d31a1ab7590efdee820da486ce97d17`  
**Inspection branch:** `proposal/path-b-release-packaging`  
**Authority:** Non-normative. No canonical document, extractor, release rule or production checker has been changed.

## 1. Purpose

The earlier command-specific audit separated ordinary existing-output format checking (D1a) from skeleton generation (D1b), but left the latter's exact dependency closure unresolved. This document traces both navigation and findings skeleton generation, identifies the active utility functions and subprocess path, and records fail-open behaviour discovered by isolated tests.

## 2. Active call graph

### Navigation skeleton

`tools/format_check.py --skeleton "QUESTION"` executes:

1. `format_check.py` imports standard-library modules.
2. At module import it dynamically loads:
   - `scripts/canonical_reference.py` as `_CR`;
   - `scripts/m193_m225.py` as `_M193`, exposing `_JS`.
3. `skeleton()` imports `tools/utility.py` and calls only `utility.request_of(question, declared)` to classify the request and select the avenues printed in the skeleton.
4. `utility.py` imports:
   - `scripts/canonical_reference.py`;
   - `tools/manifestation.py`.
5. `manifestation.py` imports the canonical reference. Its active import path does not open the positive-geometry or other research corpora.
6. `skeleton()` calls `_script_blocks()`, which invokes `scripts/canonical_reference.py --navigate QUESTION --session N` through `subprocess.run`.
7. The canonical script computes its own source digest and generates the navigation blocks. The format checker filters the script output and combines it with the fixed skeleton fields.

The active `utility.request_of()` function uses in-source regular expressions and a fixed mapping from request type to avenues. It does not call `utility.strike()`, `utility.rates()`, `utility.register()`, `utility.sources()`, `utility.holistic_text()`, or the record-backed utility commands.

### Findings skeleton

`tools/format_check.py --skeleton findings "QUESTION"` executes `findings_skeleton()`, which imports `utility.py` and calls the same `request_of()` function. It does not call the canonical navigation subprocess. The module-level dynamic loads in `format_check.py` still occur at import time, so the package should retain the same declared module closure unless the code is refactored to split checker and skeleton components.

## 3. Exact candidate D1b source closure

| File | Why required |
|---|---|
| `tools/format_check.py` | CLI, skeleton rendering, findings rendering, canonical block assembly |
| `tools/utility.py` | Active `request_of()` call; request classification and avenue selection |
| `tools/manifestation.py` | Imported by `utility.py`; currently no record read on this import path |
| `scripts/canonical_reference.py` | Dynamic import and subprocess-generated navigation blocks; source self-digest |
| `scripts/m193_m225.py` | Module-level dynamic load by `format_check.py`; full lexical scanner for checker capability |

**Runtime prerequisites:** Python 3 standard library, subprocess execution of the local canonical script, filesystem read access to the package source files.

**No active file-data dependency identified for these skeleton commands:** Core DOCX, Companion DOCX, `records/utility/register.json`, `records/congruence/`, `records/frameworks/`, `records/sources/`, `records/enrichment/`, `records/provenance/`, `records/consciousness/`, `records/adaptors/registry.json`, positive-geometry data or navigation archives.

The fact that `utility.py` contains functions that read these records does not make them dependencies of the active `request_of()` call. The same distinction applies to `manifestation.py`: its optional atlas command imports framework comparison and research data, but the import path used by utility request classification does not run that command.

## 4. Isolated package prototype

The dedicated prototype harness creates a D1b temporary package containing only the five source files in §3. It asserts that `records/`, `docs/` and `omega42.identity.json` are absent, then runs:

- `python tools/format_check.py --skeleton "What is time?"`;
- `python tools/format_check.py --skeleton findings "What is time?"`;
- `python tools/format_check.py --selftest`.

The navigation skeleton is checked for the verbatim domain and generated MATH-GATE block. The findings skeleton is checked for its FINDINGS BY AVENUE structure. The combined checker/skeleton self-test exercises the package without the repository research corpus.

The workflow result is recorded in the Path B prototype results document and linked from the packaging proposal.

## 5. Fail-open behaviour — blocking package-design issue

The current implementation has several paths where a missing dependency does not cause a hard failure:

### 5.1 Missing `utility.py`

The `skeleton()` and `findings_skeleton()` functions wrap the utility import and `request_of()` call in a broad exception handler. On failure, they substitute generic request-kind and avenue placeholders and continue generating output.

This output is not equivalent to a correctly classified skeleton, but the CLI returns success.

### 5.2 Missing canonical reference subprocess

`_script_blocks()` calls `subprocess.run()` but does not check the return code or raise on failure. If the canonical script is missing or fails, its stdout may be empty; `skeleton()` can still continue and the CLI still returns success, producing an incomplete skeleton without the generated canonical blocks.

### 5.3 Missing dynamic scanner

At module import, the full M193/M225 scanner is dynamically loaded inside a broad exception handler. Failure sets `_JS = None`; the checker continues without the full scanner. The D1a negative-control test has already demonstrated that the checker self-test still exits successfully in this reduced mode.

### 5.4 Missing dynamic canonical module

Failure to dynamically load the canonical reference causes the mathematical-token trigger to fall back to a local regular expression. That fallback may be useful for a limited diagnostic mode, but it is not equivalent to the full canonical trigger and must not be represented as full conformance.

## 6. Proposed future D1b package contract

A future package that declares full navigation or findings skeleton generation should:

1. Preflight all five required source files before invoking the generator.
2. Verify the canonical reference subprocess exits successfully.
3. Require non-empty, structurally complete canonical block output before assembling the skeleton.
4. Treat utility import/request-classification failure as a hard error or explicitly mark the result as degraded and non-conforming.
5. Require the full M193/M225 scanner for any checker result that claims full coverage.
6. Bind the package to the exact Core version and source digests.
7. Keep the skeleton generator's dependency declaration separate from utility's other optional commands and their record closures.
8. Keep generated output as an artifact, not as a hidden runtime dependency.

This proposal does not authorise changing the canonical checker. Such a change requires a separately reviewed implementation, test coverage and the appropriate canonical/release approval.

## 7. Classification recommendation

- **D1b-NAV:** navigation skeleton generation, with the five-file closure in §3.
- **D1b-FINDINGS:** findings presentation skeleton generation, with the same installed module closure under the current module layout, but without an active canonical subprocess.
- **D1b-CHECK:** checker capability layered on the same package, with required dynamic scanners and fail-closed preflight.
- Record-backed utility operations (alignment, holistic response, source survey, provenance, register and enrichment commands) remain separate profiles and must not be silently pulled into D1b.

## 8. Limitations and next work

This audit does not trace every record-backed command in `utility.py`, run every optional skeleton date/request branch, or establish that the five-file closure is the final normative package. The isolated test proves the selected commands execute in the tested package shape. A later refactor could split `format_check.py` into independent modules and reduce the findings-only closure.

The next technical task is to add the missing-utility and missing-canonical negative controls to the isolated workflow, then decide whether the future packaging contract should enforce fail-closed behaviour through a wrapper or require a canonical code change.

No canonical documents, `tools/extract_embedded.py`, L-493, existing CI rules, release policy, main branch, PR, merge or deployment has been changed by this audit.
