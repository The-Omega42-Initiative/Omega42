# Path B Command-Specific File-Read and Data-Dependency Audit

**Status:** Working technical audit  
**Version:** 0.1  
**Prepared:** 23 November 2026  
**Source baseline:** `main` at `423102f52d31a1ab7590efdee820da486ce97d17`  
**Inspection ref:** `proposal/path-b-release-packaging` (the audited source files were compared with the stated baseline where applicable)  
**Authority:** Non-normative. This document proposes no canonical amendment and changes no extractor, CI, release rule or package boundary.

## 1. Purpose and scope

This is the next Path B technical work item after the import/dynamic-loading audit. It follows the actual command paths through the candidate Profile C and Profile D tools and identifies files read from the repository, distinguishing those reads from imports, in-memory fixtures, user-supplied inputs, generated temporary files and privileged subprocess execution.

The audit covers:

- `scripts/canonical_reference.py`;
- `tools/format_check.py` and its normal-check and skeleton paths;
- `tools/output_form.py` and its form-specific dispatch;
- `tools/srcas_check.py`, `tools/certify.py` and `tools/intro_output.py`;
- `tools/handshake.py` and its identity manifest;
- `tools/conformance.py` and the command-specific paths it exercises;
- the relevant transitive helpers, including `congruence.py`, `bashar_lens.py`, `manifestation.py`, `aperture_audit.py`, `frame_audit.py`, `consciousness.py`, `output_id.py`, `adaptors.py` and `adaptor_rules.py`.

This is a source-level static trace. It is not a clean-room execution, a complete trace of every possible input, or a final normative package manifest.

## 2. Executive findings

1. **The canonical arithmetic reference is a compact executable unit.** Its CLI commands use internal constants, algorithms and built-in test vectors. Every invocation computes the script's own source digest, so the script file must be present and readable. No Core/Companion DOCX or research register is read by its ordinary command paths.
2. **The identity manifest has a small, exact current digest closure.** `tools/handshake.py manifest` reads `omega42.identity.json`, the digest list named there, and exactly the two files named in that list: the stable Core DOCX and stable Companion DOCX.
3. **A normal format check is substantially smaller than skeleton generation.** Existing-output checking dynamically loads the canonical reference and `scripts/m193_m225.py`. For modern dated outputs it also attempts an adaptor-route check. That route can require `records/adaptors/registry.json` for a non-English/adapted input. Skeleton generation is a distinct path: it runs the canonical script as a subprocess and imports `tools/utility.py`, whose wider dependency closure remains to be traced.
4. **Output-form verification is a dispatcher, not one indivisible dependency bundle.** Navigation/findings, SR-CAS/SNCA, certificates and Introductions use different checkers. Several other forms are checked internally by markers or field order and do not require every specialised checker.
5. **The conformance command's active data closure is narrower than its import graph.** The ordinary `--check` path reads the practice set and the navigation files supplied by the caller. It uses pure computations from the imported analytical modules; it does not invoke their register, atlas, pilot, theory or lens-corpus modes. The adaptor registry is conditional on a modern non-English/adapted navigation.
6. **The conformance self-test adds a Core DOCX dependency.** It executes `tools/core_sample.py`, which extracts the embedded sample from the stable Core DOCX. This is a self-test dependency, not a dependency of ordinary `--check`.
7. **No evidence supports making the entire records tree a universal runtime dependency.** Several records are required for named specialised commands, but not for the small arithmetic engine or ordinary per-navigation conformance.

## 3. Profile C — canonical arithmetic reference

### 3.1 Command behaviour

The CLI in `scripts/canonical_reference.py` supports ordinary navigation and a set of named commands, including `--navigate`, `--echo`, `--mathgate`, `--calibrate`, `--test`, `--version`, `--hash`, `--complexity`, `--canonical-selection`, `--acs`, `--neda`, and the M230 analysis commands.

The implementation uses standard-library modules and frozen in-source constants. Its test vectors and worked examples are declared in the Python source. The command paths inspected do not open a repository data file.

There is one file read common to command execution: the CLI prints `SCRIPT SHA-256` before dispatch, and `script_sha256()` opens the script source (defaulting to `__file__`) to calculate its canonical digest. The script therefore must be present as a file, not merely imported as an opaque compiled object, for this check to operate as written.

### 3.2 Candidate package closure

| Component | Required for |
|---|---|
| `scripts/canonical_reference.py` | All Profile C commands, including the source-digest check |
| Python 3 standard library | Runtime |
| Version binding to the applicable Core release | Normative interpretation and provenance |
| Declared known-answer tests | Independent package verification |

**Not required by the inspected command paths:** the Companion DOCX, research registers, framework atlases, conformance practice set, adaptors registry, or other `tools/` modules.

**Candidate classification:** OPR-C1 — canonical arithmetic and navigation kernel.

## 4. Profile D1 — existing-output format checking

### 4.1 Full checker mode

For an existing navigation, `tools/format_check.py FILE` reads the supplied output file and checks its contents. Its dynamic loads are:

- `scripts/canonical_reference.py`, used for the protocol's mathematical-token trigger and position names;
- `scripts/m193_m225.py`, used for the full lexical jargon scan.

The jargon scanner is a source-defined lexical procedure; its active scan path receives the output text and the loaded canonical module. It does not need the M225 corpus, a repository navigation archive or an external research dataset for the ordinary format check.

The checker includes a conditional adaptor-route check for dated outputs from 18 October 2026. For a modern output whose domain routes to a non-canonical adaptor, `tools/adaptors.py` is imported and the adaptor's registry entry is consulted. `adaptors.py` imports the pure `tools/adaptor_rules.py` rules. When the domain is a supported non-English/adapted script or a declared adapted language, `adaptors.adaptor()` reads:

- `records/adaptors/registry.json`.

For ordinary English/EN-CANON navigation, this registry lookup is not required by the route check. For an unsupported script routed to ZERO-COUNT, the route decision is derived from the rules module and does not require a registered adaptor record.

### 4.2 Important degraded-mode issue

Both dynamic loads at the top of `format_check.py` are wrapped in broad exception handlers. If the canonical reference fails to load, the mathematical-token trigger falls back to a local regular expression. If `m193_m225.py` fails to load, the full jargon scanner is disabled. The adaptor-route check also catches exceptions and returns without reporting a failure.

Therefore a process may produce a result with reduced coverage while appearing to have run the same checker. A package claiming full Profile D1 conformance must not treat these fallbacks as equivalent to the full checker. The release contract should require an explicit checker-capability declaration and fail closed when a required component is missing. This is a proposed packaging requirement, not a change made to current code.

### 4.3 Skeleton generation is a separate capability

The `--skeleton` path is not the same as checking an existing output. It invokes `scripts/canonical_reference.py --navigate` through `subprocess.run` to generate canonical blocks and imports `tools/utility.py` to call only `utility.request_of()` for request classification and avenue selection.

The command-specific trace is now documented in [PATH_B_SKELETON_GENERATION_CLOSURE_AUDIT.md](PATH_B_SKELETON_GENERATION_CLOSURE_AUDIT.md). Its generation-only closure is `format_check.py`, `utility.py`, `manifestation.py` and `scripts/canonical_reference.py`; M193/M225 is additionally required only when full format-check coverage is also claimed. The other record-reading utility functions are not active on the skeleton path.

The skeleton path also has fail-open behaviour: it catches utility import failures and substitutes generic request labels, and it ignores the canonical subprocess return code. The isolated negative controls reproduce both gaps.

**Candidate profiles:**
- OPR-D1a — existing-output format check;
- OPR-D1b — skeleton generation, separately declared with its utility/data dependencies and subprocess capability.

## 5. Profile D2 — output-form verification

### 5.1 Dispatch map

`tools/output_form.py` identifies a form from markers and dispatches as follows:

| Detected form | Active check path | Repository data read by the ordinary form check |
|---|---|---|
| NAVIGATION | `tools/format_check.py.check` | Same conditional adaptor-registry dependency as D1a |
| FINDINGS PRESENTATION | `tools/format_check.py.findings_check` | No additional register identified in the active findings check |
| SR-CAS ASSESSMENT / SNCA ASSESSMENT | `tools/srcas_check.py.check` | None for checking a supplied report |
| CERTIFICATE | `tools/certify.py.check` | None for checking the supplied certificate text |
| INTRODUCTION | `tools/intro_output.py.check` | `records/introduction/introduction.json` |
| ANSWER | Internal line/frame checks | None |
| CONVERSATION | Internal frame checks | None |
| APPLIED PROTOCOL EXPLORATION | Internal marker/field-order checks | None |
| APA | Internal marker/field-order checks | None |
| SR-CAS REPLICATION PACKAGE / COMPARATIVE EXPLORATION REPORT | Marker recognition | None identified in this dispatcher |

The `NAVIGATOR'S ACCOUNT` entry names an account checker in the form register, but the inspected `form_checks()` dispatcher does not dynamically load that checker; it falls through to the generic marker result. This is a code/register alignment item for later review, not a package dependency to assume.

### 5.2 SR-CAS / SNCA

The ordinary `srcas_check.py REPORT.txt` path reads the supplied report file and checks its content. Its `--owed` command is a different operational profile and reads:

- all `records/srcas/*.txt` files;
- all `submissions/ape/APE-*.md` files at or above the configured trigger sequence, to identify received submissions requiring assessment records.

Do not make these two directories mandatory for every individual report check. They are required for the repository-wide owed-assessment audit.

### 5.3 Certificates

The static `certify.py --check FILE` path reads the supplied certificate text and applies field/frame checks. The checker function called by `output_form.py` is also static and needs no certificate register.

Other commands have different dependencies:

- `--list` reads `records/certificates/CERT-*.txt`;
- `--check` with no explicit files defaults to those same registered certificate files;
- `--verify` re-runs the procedure supplied inside each certificate using `subprocess.run(..., shell=True)`.

**Security boundary:** certificate procedure execution is a privileged capability. It must not be implied by installing or invoking a passive certificate syntax checker. A future package must explicitly authorise commands, working directories, environment, filesystem/network access and expected output handling before enabling this execution path. The current source accepts shell procedure text from the certificate; this audit does not endorse running untrusted certificates.

### 5.4 Candidate output-form packages

- OPR-D2a — dispatcher and internal frame checks;
- OPR-D2b — SR-CAS/SNCA report checker;
- OPR-D2c — repository-wide SR-CAS owed audit, with the two record/submission directories;
- OPR-D2d — static certificate syntax checker;
- OPR-D2e — privileged certificate procedure execution, separately authorised;
- OPR-D2f — Introduction form checker, with its exact JSON dependency.

## 6. Profile D3 — Introduction verification

`tools/intro_output.py` has several distinct modes:

| Command mode | Files read |
|---|---|
| `--render`, `--check`, `--first-render`, `--first`, `--terms` | `records/introduction/introduction.json` |
| `--core CORE.docx` | Supplied Core DOCX and `introduction.json` |
| `--legitimacy CORE.docx` | Supplied Core DOCX, `introduction.json`, `records/introduction/legitimacy.json` |
| `--philosophy CORE.docx` | Supplied Core DOCX, `records/introduction/philosophy.json` |

The Core DOCX is parsed as a ZIP archive and its `word/document.xml` is read. The Introduction, Philosophical and Legitimacy JSON registers are separate data dependencies for their respective audit modes; they are not all required for the ordinary output-form Introduction check.

**Candidate profiles:**
- OPR-D3a — render/check/first-session/terms, with `introduction.json`;
- OPR-D3b — Core-opening reconciliation, with Core DOCX;
- OPR-D3c — legitimacy reconciliation, with Core DOCX and `legitimacy.json`;
- OPR-D3d — philosophy-register reconciliation, with Core DOCX and `philosophy.json`.

## 7. Profile D4 — identity and release handshake

### 7.1 Command separation

`tools/handshake.py` has three materially different modes:

- `fingerprint`: recomputes the mathematical fingerprint from the implementation;
- `challenge`: runs live challenge/response rounds using the implementation;
- `manifest`: validates the identity record and release digest closure.

The fingerprint and challenge paths use the arithmetic in the module and do not read repository data files. The manifest path reads:

1. `omega42.identity.json`;
2. the digest file named by `release.digests` in that JSON: `records/release_documents_SHA256.txt`;
3. every file listed in that digest file.

### 7.2 Exact current digest closure

The current digest list contains exactly two entries:

| File | SHA-256 |
|---|---|
| `docs/Omega42_Core_Specification_V335_Rev450_STABLE.docx` | `76126213a1b0a646c12ba86e81613b6f85ba0893d20979d675485794f8ef0f67` |
| `docs/Omega42_Companion_Document_V335_Rev450_STABLE.docx` | `0e2e7a71c2110b028e23e1a7f8cc22ac4e0ebbbc12d5fb8e6d9a936833dc9973` |

A missing or mismatched file prevents the manifest check from establishing the declared release identity. It must not silently degrade to a fingerprint-only or challenge-only result.

**Candidate profile:** OPR-D4 — identity/fingerprint/challenge, with a separate manifest-integrity subprofile binding the identity JSON, digest list and two DOCX artifacts.

## 8. Profile D5 — conformance command and active read closure

### 8.1 Ordinary `--check` path

`tools/conformance.py --check DIR [SET]` imports a broad set of modules, but the active per-navigation path is specific:

- `canonical_reference.navigate()` and `determine_anchor()`;
- `congruence.sig()`, which uses the pure `bashar_lens.frequency()` calculation;
- `manifestation.classify()`;
- `format_check.check()`;
- `aperture_audit.audit()`;
- `frame_audit.scan()`;
- `consciousness.typing_scan()`;
- `output_id.verify()`.

The command reads:

- the caller-supplied navigation files in `DIR`;
- `records/conformance/practice_set.txt`, or the caller-supplied replacement SET, to establish the expected public set and coverage.

The public practice set currently contains eight tagged domains. It is a conformance fixture, not a general runtime database.

The imported modules do not cause their optional record modes to execute merely because they are imported. In this command path:

- `congruence.sig()` does not load the congruence register, framework atlases or lens relevance registry;
- `manifestation.classify()` is arithmetic and does not read the positive-geometry corpus;
- `consciousness.typing_scan()` is a lexical in-memory scan and does not read the theory, pilot, conjecture or correspondence registers;
- `frame_audit.scan()` is an in-memory lexical scan and does not invoke the separate M323 identity-routing function or `claimcheck.py`;
- `aperture_audit.audit()` is an in-memory lexical scan;
- the optional orbit/matching path that may load `construct_x.py` and `networkx` is not used by this per-navigation path.

The format checker can add one conditional data dependency: for a modern dated navigation whose domain routes to an adapted script/language, `format_check.adaptor_checks()` may load `records/adaptors/registry.json`. For canonical English navigation, this read is not required.

### 8.2 Other conformance commands

| Command | Additional file reads |
|---|---|
| `--key [SET]` | The selected practice-set file; computes the expected key in memory |
| `--check DIR [SET]` | Practice-set file plus each navigation file in DIR |
| `--selftest` | Runs `tools/core_sample.py`, which reads the stable Core DOCX; also uses the default practice set and a temporary navigation file |

The self-test creates a temporary navigation file. It does not require the full research corpus. Its Core DOCX dependency exists because the sample is extracted from Core Part 8.5 at runtime.

### 8.3 Candidate conformance closure

**OPR-D5a — ordinary conformance check:**
- `tools/conformance.py`;
- the active imported modules listed above;
- `scripts/canonical_reference.py`;
- `scripts/m193_m225.py`;
- `tools/adaptor_rules.py` and `tools/adaptors.py` plus `records/adaptors/registry.json` only if adapted-domain checking is part of the declared supported input profile;
- `records/conformance/practice_set.txt` (or an explicitly bound alternative set);
- Python 3 standard library.

**OPR-D5b — conformance self-test:**
- all D5a code and fixtures;
- `tools/core_sample.py`;
- stable Core DOCX;
- temporary-file capability.

The Companion DOCX, the entire records tree, framework atlases, consciousness registers, the congruence register and `networkx` are not demonstrated dependencies of the ordinary `--check` command path.

## 9. Consolidated package candidate matrix

| Capability | Minimal source/data closure identified | Conditional or separate dependencies |
|---|---|---|
| C1 canonical arithmetic | `scripts/canonical_reference.py` | Core version binding; script self-read |
| D1a format check | `format_check.py`, canonical reference, `m193_m225.py` | Adaptors + registry for adapted modern inputs |
| D1b skeleton generation | D1a plus `utility.py` and canonical subprocess | Further utility imports/records; not fully traced |
| D2a output-form dispatcher | `output_form.py` and selected checker | Form-specific modules below |
| D2b SR-CAS/SNCA check | `srcas_check.py` | Supplied report input |
| D2c SR-CAS owed audit | `srcas_check.py` | `records/srcas/*.txt`, `submissions/ape/APE-*.md` |
| D2d certificate syntax | `certify.py` | Supplied certificate input |
| D2e certificate execution | `certify.py` | Explicitly authorised shell procedure execution |
| D3a Introduction check | `intro_output.py` | `records/introduction/introduction.json` |
| D3b/c/d Introduction audits | `intro_output.py` | Core DOCX and the corresponding legitimacy/philosophy JSON |
| D4 identity manifest | `handshake.py`, `omega42.identity.json`, digest list | Two DOCX artifacts listed in §7 |
| D5a conformance check | conformance toolchain + practice set + supplied navigation files | Adaptors registry for adapted-domain cases |
| D5b conformance self-test | D5a plus `core_sample.py` | Stable Core DOCX; temporary files |

This matrix is a candidate classification, not a complete machine-readable manifest and not a decision that any of these profiles is already an adopted OPR release.

## 10. Packaging and verification recommendations

1. **Define capability-specific closures.** A user who wants arithmetic recomputation should not have to install research registers or a website. A user who wants an Introduction audit should receive its exact JSON and Core dependencies.
2. **Separate imports from active reads.** A module's optional register-reading functions do not make their records mandatory for every command that imports the module. The package manifest should describe command profiles and branch conditions.
3. **Fail closed for declared full checks.** Dynamic-loader fallbacks must be surfaced as degraded capability, never reported as equivalent full conformance.
4. **Separate passive validation from execution.** Certificate syntax checking and certificate procedure execution must be separate permissions and packages.
5. **Bind every profile to normative versions.** Record the Core version, source digests, Python version, exact command, input fixtures and verification result.
6. **Make conditional data explicit.** Adapted-language checks should declare their supported script/adaptor set and corresponding registry closure.
7. **Do not silently include broad corpora.** Congruence atlases, philosophical registers, consciousness datasets, historical submissions and prior-art materials belong in the package that actually reads them.
8. **Keep L-493 intact until a formal amendment is approved.** This audit identifies candidate boundaries; it does not authorise exclusions, alter the extractor or weaken CI.

## 11. Limitations and next work

This audit has not yet:

- executed each command in a clean temporary environment;
- traced every `tools/utility.py` skeleton-generation branch and its record reads;
- tested all adapted-script routes against a minimal registry package;
- checked whether the `format_check.py` degraded fallbacks are observable in every host environment;
- executed the output-form self-test and every specialised checker against a clean package;
- validated the manifest digest list against the actual DOCX bytes in a clean checkout;
- traced every CI workflow command and environment into a release profile;
- produced a complete machine-readable package manifest.

The next recommended technical step is to build **minimal package prototypes for C1, D1a, D4 and D5a**, then run the declared commands in isolated temporary workspaces with deliberately omitted optional files. This will test whether the static closures are sufficient and whether missing required components fail clearly. Skeleton generation, specialised audit modes and privileged certificate execution should remain separate follow-on profiles.

No canonical files, `tools/extract_embedded.py`, L-493, CI workflow, release policy, PR, merge or deployment has been changed by this audit.
