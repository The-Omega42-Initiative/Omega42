# Path B Import and Dynamic-Loading Audit — Candidate Protocol and Conformance Tools

**Status:** Working technical audit  
**Version:** 0.1  
**Audit baseline:** `main` at `423102f52d31a1ab7590efdee820da486ce97d17`  
**Prepared:** 23 November 2026  
**Authority:** Non-normative. No canonical document, release rule, extractor, CI workflow or package boundary is amended.

## 1. Scope

This document advances technical work item 2 of the Path B Dependency Audit: tracing Python imports, dynamic module loading and subprocess invocation for the candidate Profile C and Profile D tools.

The audit inspected the source of:
- `scripts/canonical_reference.py`;
- `tools/format_check.py`;
- `tools/output_form.py`;
- `tools/handshake.py`;
- `tools/conformance.py`;
- the modules they import or load dynamically, including `m193_m225.py`, `congruence.py`, `manifestation.py`, `consciousness.py`, `srcas_check.py`, `intro_output.py`, `certify.py`, `frame_audit.py`, `claimcheck.py`, and related helpers.

This is a source-level dependency trace, not an execution in a clean environment. It does not yet establish that every path listed below is required in every command mode, nor does it include a full file-read closure for all imported modules.

## 2. Executive findings

1. **Profile C has a genuinely small arithmetic kernel.** `scripts/canonical_reference.py` uses Python standard-library modules only. Its direct imports are `hashlib`, `html`, `re`, `sys`, `unicodedata`, `collections.Counter`; additional standard-library imports occur inside selected functions. The ordinary navigation and arithmetic functions do not import another Omega42 Python module.
2. **Profile D is not one tool with one dependency closure.** Format checking, output-form checking, identity handshake and full conformance are distinct capabilities, with different loaders and data dependencies.
3. **Dynamic loading is material.** `format_check.py` loads the canonical reference and `m193_m225.py` through `importlib.util.spec_from_file_location`. `output_form.py` loads the checker appropriate to the detected output form. A file inventory based only on top-level `import` statements would miss these dependencies.
4. **The conformance suite imports a broad analytical stack.** `conformance.py` imports `congruence`, `format_check`, `aperture_audit`, `frame_audit`, `output_id`, `manifestation` and `consciousness`, in addition to the canonical reference. The transitive stack is much larger than Profile C.
5. **A non-standard dependency appears on an optional branch.** `congruence.py` attempts to import `networkx` inside its one-to-one matching routine, and has a fallback if it is absent. This should not be made a mandatory OPR dependency unless the declared profile requires that routine and its exact matching guarantee.
6. **Several modules combine pure checks with repository-data or operational modes.** The package must be split by command/capability, not simply by copying every imported module and every record directory.

## 3. Profile C — canonical arithmetic reference

### 3.1 Direct import closure

`scripts/canonical_reference.py` imports only standard-library modules:

- `hashlib`
- `html`
- `re`
- `sys`
- `unicodedata`
- `collections.Counter`

Selected functions import standard-library `datetime`, `fractions.Fraction`, `itertools.product`, `math.lcm` and `math` locally. No third-party package or other Omega42 Python module is directly imported by this script.

### 3.2 File-system dependency

The script's `script_sha256()` function reads its own source file (or an explicitly supplied path) to calculate the canonical source digest. This means the source file itself is required for that verification function. The ordinary `navigate` arithmetic does not require a separate data file.

### 3.3 Proposed Profile C closure

For the command family implemented by this script, the candidate executable closure is:

- `scripts/canonical_reference.py`;
- Python 3 runtime;
- the exact Core release that defines the semantics;
- test vectors/known-answer cases selected for the Profile C conformance contract.

The script's own `--test` and `--calibrate` options should be included in the next execution audit. This source trace does not claim that the current test command has been run in a clean-room package.

**Finding:** Profile C can likely be packaged as a small, standard-library-only runtime. This is the strongest evidence so far that OPR need not contain the entire `tools/` directory merely to support canonical arithmetic.

## 4. Profile D — format verification

### 4.1 Direct and dynamic imports

`tools/format_check.py` imports standard-library modules and dynamically loads:

- `scripts/canonical_reference.py`, under module name `cr`, to use its mathematical-token trigger;
- `scripts/m193_m225.py`, under module name `m193`, to use its jargon scanner.

If either dynamic load fails, the module falls back: its mathematical trigger becomes a local regular-expression scan, and the jargon scanner is disabled. This fallback is operationally significant. A checker can still run while silently losing part of its intended coverage. A release profile should therefore distinguish **full checker mode** from **degraded fallback mode**, and mandatory conformance must fail closed if the required scanner is unavailable.

### 4.2 Subprocess dependency

The skeleton-generation path in `format_check.py` invokes `scripts/canonical_reference.py --navigate` using `subprocess.run`. This is a separate execution path from checking an existing output.

The skeleton path also imports `tools/utility.py` locally to build additional content. That utility module has a much larger dependency surface (including `manifestation`, `crc60_and_m267`, `congruence`, `adaptors`, and `consciousness`) and reads multiple records. It should not be included in a minimal format-check package unless skeleton generation is part of the declared Profile D capability.

### 4.3 Proposed format-check closure

For the full existing-output check, the source-level candidate is:

- `tools/format_check.py`;
- `scripts/canonical_reference.py`;
- `scripts/m193_m225.py`;
- Python 3 standard library.

For skeleton generation, add the canonical script as an executable subprocess and trace the specific `utility.py` functions actually invoked, including their imports and record reads. Do not assume the entire utility module's data corpus is required for the basic format check.

## 5. Profile D — output-form verification

### 5.1 Dynamic checker routing

`tools/output_form.py` identifies a form from markers and then dynamically loads a checker according to the form:

| Output form | Dynamically loaded checker |
|---|---|
| NAVIGATION | `tools/format_check.py` |
| FINDINGS PRESENTATION | `tools/format_check.py` |
| SR-CAS / SNCA ASSESSMENT | `tools/srcas_check.py` |
| CERTIFICATE | `tools/certify.py` |
| INTRODUCTION | `tools/intro_output.py` |

Other forms are checked internally by `output_form.py` through markers and field-order rules. This makes output-form checking a dispatcher over multiple optional checker packages, not a single indivisible runtime.

### 5.2 Form-specific dependencies

- **NAVIGATION / FINDINGS:** inherit the full format-check closure above.
- **SR-CAS / SNCA:** use `srcas_check.py`, which is standard-library-only for the report check itself. Its `--owed` mode additionally reads the SR-CAS records and APE submission files.
- **CERTIFICATE:** uses `certify.py`. Its static certificate-field checker is standard-library-based; separate procedure-execution functionality invokes a shell command from certificate data and must be treated as a privileged operational capability, not bundled into a passive reader/checker by default.
- **INTRODUCTION:** uses `intro_output.py`, which reads `records/introduction/introduction.json` for the standard output-form check. Other command modes additionally read `philosophy.json`, `legitimacy.json`, and in some modes the Core DOCX.

The output-form dispatcher itself also imports `datetime`, `importlib.util`, `os`, `re` and `sys`, all standard library.

### 5.3 Proposed packaging

Do not make every specialized checker and every associated register mandatory for every user. Define subprofiles, for example:

- OPR-D1: navigation and findings format;
- OPR-D2: SR-CAS/SNCA report format;
- OPR-D3: certificate document syntax only;
- OPR-D4: Introduction form;
- OPR-D5: privileged certificate procedure execution, if formally authorised.

A profile claiming all registered forms must include and test every corresponding checker and its exact data dependencies. A profile claiming only navigation-format verification need not include the SR-CAS, certificate or Introduction datasets.

## 6. Profile D — identity and release handshake

`tools/handshake.py` imports only standard-library modules: `hashlib`, `json`, `os`, `random`, `sys`.

The live mathematical challenge is implemented in the module itself. The manifest-check path reads:

- `omega42.identity.json`;
- the digest file named by `release.digests` in that JSON;
- every file enumerated by that digest file, to recompute its SHA-256.

Therefore the identity handshake is not just a Python script: its manifest and all digest-listed artifacts are part of the claimed identity profile. The exact digest closure must be extracted from the pinned manifest rather than manually guessed.

**Packaging implication:** keep this as a distinct OPR integrity/identity profile. Do not make it a hidden prerequisite for ordinary text-only navigation. A missing or mismatched digest-listed file must fail the identity claim; it must not silently downgrade to an ordinary navigation.

## 7. Full conformance suite — broad transitive closure

### 7.1 Direct imports

`tools/conformance.py` imports:

- `scripts/canonical_reference.py`;
- `tools/congruence.py`;
- `tools/format_check.py`;
- `tools/aperture_audit.py`;
- `tools/frame_audit.py`;
- `tools/output_id.py`;
- `tools/manifestation.py`;
- `tools/consciousness.py`.

It reads `records/conformance/practice_set.txt` by default. Its self-test also executes `tools/core_sample.py` as a subprocess and creates a temporary navigation file.

### 7.2 Important transitive imports and conditional branches

- `congruence.py` imports `bashar_lens.py`, `aperture_audit.py`, `frame_audit.py` and `format_check.py`; it uses the canonical reference and reads a congruence register and framework/lens data in its register/atlas functions.
- `manifestation.py` imports the canonical reference.
- `consciousness.py` imports `manifestation.py` and the canonical reference. Its wider theory, pilot, conjecture, baseline and correspondence commands read separate `records/consciousness/` files; the conformance typing scan must be traced to determine the subset it actually reads.
- `frame_audit.py` dynamically imports `claimcheck.py` when arithmetic identities are routed for checking.
- `congruence.py` imports `construct_x.py` inside its orbit/matching path; it attempts to use third-party `networkx` for maximum-cardinality matching and falls back to a greedy matching algorithm if that import is unavailable. This conditional path is not necessarily exercised by the conformance suite's per-navigation check.
- `format_check.py` dynamically loads `m193_m225.py` and the canonical reference, as described above.

### 7.3 What this means

The full conformance tool is not an appropriate definition of the minimal arithmetic kernel. It is a higher assurance profile with a larger, partly conditional closure.

A clean-room implementation must test the exact command being claimed. In particular, it must not accidentally include atlas/register functionality and its large research corpus when only per-navigation conformance is required; conversely, it must not omit a module or record that the declared conformance command actually reads.

## 8. Import graph summary

The following is the source-level graph established in this pass. Arrows indicate an import, dynamic load or subprocess invocation; they do not mean every branch is executed by every command.

```text
Profile C
  scripts/canonical_reference.py
    └── Python standard library only

Profile D: format check
  tools/format_check.py
    ├── dynamic: scripts/canonical_reference.py
    ├── dynamic: scripts/m193_m225.py
    ├── subprocess (skeleton path): scripts/canonical_reference.py
    └── local (skeleton path): tools/utility.py
          ├── manifestation.py
          ├── congruence.py
          ├── adaptors.py
          ├── consciousness.py
          └── additional record readers

Profile D: output-form dispatcher
  tools/output_form.py
    ├── format_check.py
    │     ├── canonical_reference.py
    │     └── m193_m225.py
    ├── srcas_check.py
    ├── certify.py
    └── intro_output.py
          └── records/introduction/*.json (mode-dependent)

Profile D: identity handshake
  tools/handshake.py
    ├── omega42.identity.json
    ├── release digest list
    └── every file named in that digest list

Profile D: full conformance
  tools/conformance.py
    ├── canonical_reference.py
    ├── congruence.py
    │     ├── bashar_lens.py
    │     ├── aperture_audit.py
    │     ├── frame_audit.py
    │     │     └── claimcheck.py (dynamic)
    │     ├── format_check.py
    │     │     ├── canonical_reference.py
    │     │     └── m193_m225.py
    │     └── construct_x.py (conditional path)
    │           └── networkx (optional; fallback exists)
    ├── manifestation.py
    ├── consciousness.py
    ├── aperture_audit.py
    ├── frame_audit.py
    └── output_id.py
```

## 9. Packaging decisions suggested by this trace

1. **Keep Profile C small.** The canonical reference script is a strong candidate for a compact standard-library runtime.
2. **Separate conformance profiles by function.** Format, output-form, identity and full conformance are not one mandatory dependency bundle.
3. **Fail closed on required dynamic loads.** Where a profile claims a checker, a missing scanner must not silently fall back to reduced coverage and still report full conformance.
4. **Treat subprocess and shell execution as explicit capabilities.** A package that only checks a file should not implicitly grant the ability to run arbitrary certificate procedures.
5. **Bind runtime code to Core version.** Each script's source digest, parent Core release, Python version and command profile should be declared in the package manifest.
6. **Do not bundle optional research datasets without a profile reason.** Registers and atlases used only by optional commands belong in OKR unless they are declared conformance fixtures.
7. **Record optional third-party dependencies explicitly.** `networkx` is presently optional in one branch; if the fallback changes result quality or determinism, the profile must state which algorithm is used and what claim it supports.

## 10. Limitations and next audit stage

This pass has not yet:
- executed the candidate commands in a clean environment;
- enumerated every file read by each command and each dynamic branch;
- resolved all imports inside the utility, lens, adaptor and consciousness modules;
- verified the exact digest-list closure of `omega42.identity.json`;
- determined whether the conformance suite's optional branches are required by the adopted certification claim;
- tested whether `networkx` absence changes a claimed result or only its matching heuristic;
- traced every CI invocation and its environment/toolchain.

The next technical item should be **command-specific file-read and data-dependency tracing** for Profiles C and D. This will turn the source-level graph into a testable package manifest. No canonical files or L-493 have been changed by this audit.
