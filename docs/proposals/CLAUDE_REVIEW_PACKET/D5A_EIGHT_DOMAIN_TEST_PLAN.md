# D5a — Eight-Domain Fixture Coverage Test Plan

**Status:** Path B strict wrapper and isolated D5a package validation passed; raw M314 duplicate defect remains isolated by the wrapper  
**Prepared:** 23 November 2026  
**Target profile:** D5a ordinary Navigator conformance  
**Canonical practice-set source:** `records/conformance/practice_set.txt`

## 1. Objective

Extend the current D5a smoke test from one historical navigation outside the public practice set to a complete, reproducible test containing one valid navigation for each of the eight public domains.

The test must distinguish:
- successful arithmetic recomputation;
- successful per-navigation required checks;
- complete domain coverage;
- text-only versus script-capable compatibility;
- advisory review outcomes versus required conformance failures.

A test must never infer full compatibility from a passing individual file.

## 2. The eight required domains

The practice set currently defines:

| Tag | Verbatim domain |
|---|---|
| CF-01 | What is time? |
| CF-02 | Explore the golden ratio connection |
| CF-03 | Is the protocol a computer application? If so, what kind of application will it be? |
| CF-04 | Why does $x^2 = x + 1$ have no root modulo 9? |
| CF-05 | Should I follow my excitement or my plan? |
| CF-06 | What is the boundary between the seen and the unseen? |
| CF-07 | A small coastal town has lost its only bookshop, its ferry runs twice a week, and the young people leave for the city; what would it take for the town to want to stay itself and still change? |
| CF-08 | How does a question change when it is asked a second time? |

The test must read these values from the practice-set file at runtime. The table above is a human-readable snapshot, not a second authority.

## 3. Canonical recomputation path

The existing `tools/conformance.py` defines the required arithmetic path:

1. Read the exact domain text from the practice set.
2. Call `canonical_reference.navigate(domain)`.
3. Recompute the anchor using `determine_anchor(n1, n2, n3)`.
4. Recompute four arms using offsets Yang 5, Yin 18, 4D 8 and Antipode 12 modulo 24.
5. Recompute the layer-one state as the residues of the second and third canonical coordinates modulo 9.
6. Recompute the norm and its stratum/half classification through `manifestation.py`.
7. Recompute the voice through `congruence.sig(domain)`.

The fixture generator should call these canonical functions. It must not copy precomputed expected values from an existing navigation or independently reimplement the same algorithm in a way that can share the same mistake.

## 4. Fixture acquisition hierarchy

Use this order:

1. **Existing exact-domain navigation:** inspect historical `submissions/navigations/*.txt` and paired JSON metadata. Reuse only if the domain line matches the practice-set text exactly and the file passes all required checks.
2. **Canonical Core sample/template:** use `tools/core_sample.py` and the canonical skeleton generator as structural references. Do not simply replace the domain line in a sample while leaving stale arithmetic or semantic content.
3. **Synthetic conformance fixture:** if no valid historical fixture exists, generate a clearly labelled synthetic fixture in the isolated test workspace. Populate all required arithmetic and structural fields from the canonical recomputation path. Synthetic fixtures are test artefacts, not accepted research submissions or prior-art disclosures.

Do not modify or relabel historical navigation records to manufacture domain coverage.

## 5. Required assertions

For each of the eight fixtures:

- Exactly one `DOMAIN VERBATIM` value matches the exact practice-set domain.
- A1 anchor passes against independent canonical recomputation.
- A2 all four arms pass.
- A3 format has no required format failures.
- A4 layer-one state, voice, norm, stratum and half all match recomputation.
- The conformance report associates the fixture with the correct CF tag.
- The fixture is counted toward coverage only when every required check passes.

For the complete set:

- Exactly eight required domains are present.
- Coverage is 8/8.
- No domain is missing.
- No domain is duplicated in a way that masks another missing domain.
- Overall result is `COMPATIBLE (TEXT-ONLY)` or `COMPATIBLE (SCRIPT-CAPABLE)`, according to the actual execution-status and output-ID evidence. Do not hardcode the level.
- The report's coverage and verdict agree.

## 6. Negative controls

The experimental harness has exercised ten controls, each of which returned `NOT YET COMPATIBLE`:

1. One domain fixture removed.
2. One fixture's domain changed to a non-practice-set domain.
3. Anchor changed.
4. One arm changed.
5. Required layer-one state changed.
6. Required format marker removed.
7. One domain duplicated while another is absent.
8. Empty fixture.
9. Malformed fixture.
10. Valid fixture with wrong exact wording in `DOMAIN VERBATIM`.

An additional control supplied nine passing files while all eight domains remained represented. The current report returned `COMPATIBLE (SCRIPT-CAPABLE)`, contrary to the exact-one-file-per-domain acceptance criterion. This is a reproduced M314 defect. The report also emits no dedicated duplicate-domain diagnostic. See the [validation report](D5A_EIGHT_DOMAIN_VALIDATION_REPORT.md).

The canonical checker remains unchanged. A future checker correction or wrapper must reject the duplicate-extra case and preserve per-file diagnostics before D5a can be complete.

## 7. Package boundary and data exclusions

The initial D5a package should retain the active code closure already used by the smoke test:

- `scripts/canonical_reference.py`
- `scripts/m193_m225.py`
- `scripts/crc60_and_m267.py`
- `tools/conformance.py`
- `tools/congruence.py`
- `tools/bashar_lens.py`
- `tools/format_check.py`
- `tools/aperture_audit.py`
- `tools/frame_audit.py`
- `tools/output_id.py`
- `tools/manifestation.py`
- `tools/consciousness.py`
- `tools/adaptors.py`
- `tools/adaptor_rules.py`
- `tools/utility.py`
- `tools/path_b_d5a_guard.py`
- `records/conformance/practice_set.txt`
- `records/frameworks/lens_relevance.json`

The test harness `tools/path_b_d5a_fixture_test.py` is copied only to execute the isolated validation; it is test tooling, not part of the runtime package closure. The lens relevance registry is an active data dependency because `tools/congruence.py::lenses_of()` loads it even when no lens is selected.

The isolated package must exclude `docs/`, `omega42.identity.json` and unrelated research registers unless execution demonstrates an active dependency for this profile. Fixture files are copied into a dedicated temporary `inputs/` directory.

The existing profile's lack of Core/Companion documents and selected research registers should remain explicitly tested.

## 8. Reproduced duplicate-domain defect and Path B containment

Source inspection and executed controls establish:

- Raw M314 uses a set of passing domain strings to compute coverage.
- A duplicate that replaces a missing domain leaves the missing domain uncovered, so the raw verdict is non-compatible.
- A duplicate extra file alongside one passing file for each of the eight domains is accepted by raw M314: it sees 8/8 coverage and returns compatible despite nine files.
- Raw M314 emits no dedicated duplicate-domain diagnostic.

The experimental Path B guard, `tools/path_b_d5a_guard.py`, enforces exactly one file per exact practice-set domain, exactly one `DOMAIN VERBATIM` line per file, no repeated domain, and no unexpected or missing domain. It then delegates all per-file A1–A4 checks to canonical M314. The guard rejects both duplicate controls and emits an explicit diagnostic.

The Path B wrapper contains the defect at the package boundary. It does not repair or alter canonical M314, which remains unchanged.

## 9. Deliverables

- Fixture inventory identifying historical versus synthetic source.
- Deterministic fixture generator, if needed, operating only inside the temporary package.
- Independent recomputation table for the eight domains.
- Isolated D5a run log and exact commit.
- Negative-control matrix with expected and actual outcomes.
- Updated prototype results document.
- Updated Path B proposal evidence section.
- Claude review note describing unresolved checker behaviour and proposed remedies.

## 10. Acceptance criterion

D5a eight-domain coverage is complete only when the isolated package:
1. recomputes the eight-domain key;
2. validates one complete fixture for every exact practice-set domain;
3. reports 8/8 coverage and a compatible verdict at the actual supported execution level;
4. rejects each required negative control with `NOT YET COMPATIBLE` or an explicit hard error;
5. runs without the excluded Core/Companion and unrelated research files;
6. records the exact source commit and fixture provenance.

This is a profile-level test, not a full Omega42 release, not legal/governance approval and not a replacement for L-493.


## 11. Experimental implementation and validation (23 November 2026)

The harness, strict package guard and dedicated workflow are present:

- `tools/path_b_d5a_fixture_test.py`
- `tools/path_b_d5a_guard.py`
- `.github/workflows/path-b-d5a-fixtures.yml`
- [D5a validation report](D5A_EIGHT_DOMAIN_VALIDATION_REPORT.md)

Run [45157034105](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45157034105), source commit `4b1cd709627d58701a0fb6a5eaf8e80128b6e14b`:

- Eight current-date synthetic fixtures: 8/8 A1–A4 and current A3 format checks passed.
- Baseline verdict: `COMPATIBLE (SCRIPT-CAPABLE)`.
- Negative controls: 11/11 rejected, including duplicate-domain and multiple-domain-line cases.
- Duplicate extra with all eight domains otherwise covered: Path B guard returned `NOT YET COMPATIBLE`; raw M314 returned `COMPATIBLE (SCRIPT-CAPABLE)`.
- Isolated minimal package: PASS. The declared runtime closure ran without Core/Companion documents, identity JSON or unrelated research registers.

The first isolation attempt found the active `records/frameworks/lens_relevance.json` dependency; adding it resolved the failure. The validated runtime closure is listed in Section 7 and in the validation report.

The canonical M314 duplicate defect remains unchanged. The Path B wrapper contains it for this experimental package profile. Synthetic prose and trigger markers mean this is mechanical execution/format evidence, not semantic navigation-quality evidence.

**D5a status:** Path B strict-wrapper profile validation complete. This is not a full Omega42 release, not L-493 approval and not certification of a deployed system.
