# L-493 failure — verified log-based root-cause analysis

**Date:** 23 November 2026  
**Status:** Evidence-based diagnosis, **not** authorization to amend the release contract.  
**Source:** [omega42-ci run 45183240439, verify job 137722152058](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45183240439/job/137722152058), branch commit `de297e3de70c0c920b52578564f37fb7bbf57838`. Full job log retrieved with the GitHub Actions job-logs connector; relevant output timestamp 2026-11-23T13:40:03Z.

## Direct evidence

The failing step 68, **Self-contained release -- every required file embedded in the two documents, identical, and runnable from them alone (Core L-493, Appendix R)**, printed:

```text
SELF-CONTAINMENT (L-493): 1619 blocks embedded | 1657 files required (every file of the repository) | 12 outside, each because it cannot be inside | problems 38
RESULT: FAIL
Process completed with exit code 1.
```

All **38** problem lines were `not embedded: <path>`; there were **zero** reported `embedded copy differs`, `embedded but not in the repository`, or `embedded but required to stay outside` problems. Therefore the failure at this commit is **missing embeddings**, not existing-block byte drift. `tools/extract_embedded.py::required()` enumerates repository files except its fixed `OUTSIDE` and `EXEMPT` sets and archive/cache exceptions; its `blocks()` reads embedded blocks from the two canonical DOCX files. Experimental branch files are counted by the unchanged release contract.

## Complete 38-path inventory

```text
.github/workflows/path-b-d2-srcas.yml
.github/workflows/path-b-d3-certificate.yml
.github/workflows/path-b-d4-introduction.yml
.github/workflows/path-b-d5a-fixtures.yml
.github/workflows/path-b-prototype-isolation.yml
HANDOVER_NEXT_SESSION.md
docs/proposals/CLAUDE_REVIEW_PACKET/CHATGPT_COBUILDER_PROGRESS_2026-11-23.md
docs/proposals/CLAUDE_REVIEW_PACKET/CURRENT_TECHNICAL_STATUS.md
docs/proposals/CLAUDE_REVIEW_PACKET/D1B_GUARD_VALIDATION.md
docs/proposals/CLAUDE_REVIEW_PACKET/D2B_OUTPUT_FORM_DISPATCH_AUDIT.md
docs/proposals/CLAUDE_REVIEW_PACKET/D2_SR_CAS_SNCA_VALIDATION_REPORT.md
docs/proposals/CLAUDE_REVIEW_PACKET/D3_CERTIFICATE_STATIC_VALIDATION_REPORT.md
docs/proposals/CLAUDE_REVIEW_PACKET/D4_INTRODUCTION_VALIDATION_REPORT.md
docs/proposals/CLAUDE_REVIEW_PACKET/D5A_EIGHT_DOMAIN_TEST_PLAN.md
docs/proposals/CLAUDE_REVIEW_PACKET/D5A_EIGHT_DOMAIN_VALIDATION_REPORT.md
docs/proposals/CLAUDE_REVIEW_PACKET/D5A_FIXTURE_SOURCE_ASSESSMENT.md
docs/proposals/CLAUDE_REVIEW_PACKET/D5_CERTIFICATE_EXECUTION_BOUNDARY_AUDIT.md
docs/proposals/CLAUDE_REVIEW_PACKET/PROJECT_CONTEXT_AND_OPEN_TASKS_2026-11-23.md
docs/proposals/CLAUDE_REVIEW_PACKET/README.md
docs/proposals/PATH_B_COMMAND_SPECIFIC_READ_CLOSURE_AUDIT.md
docs/proposals/PATH_B_DEPENDENCY_AUDIT.md
docs/proposals/PATH_B_IMPORT_AND_DYNAMIC_LOADING_AUDIT.md
docs/proposals/PATH_B_MINIMAL_PACKAGE_PROTOTYPE_RESULTS.md
docs/proposals/PATH_B_PRELIMINARY_CLASSIFICATION_REGISTER.md
docs/proposals/PATH_B_SKELETON_GENERATION_CLOSURE_AUDIT.md
docs/proposals/RELEASE_PACKAGING_ARCHITECTURE_PATH_B_PROPOSAL.md
tools/path_b_d1b_guard.py
tools/path_b_d2_srcas_guard.py
tools/path_b_d2_srcas_test.py
tools/path_b_d2b_form_registry_contract_test.py
tools/path_b_d2b_local_dispatch_test.py
tools/path_b_d3_certificate_guard.py
tools/path_b_d3_certificate_test.py
tools/path_b_d4_introduction_test.py
tools/path_b_d5_certificate_semantics_test.py
tools/path_b_d5a_fixture_test.py
tools/path_b_d5a_guard.py
tools/path_b_prototype_test.py
```

At this pinned commit the categories are **5 workflows, 1 root handover, 20 proposal/review Markdown files, and 12 Path B Python files**. This is a point-in-time inventory; subsequent commits add files (e.g., `tools/path_b_l493_release_diagnostic.py`) and may change counts.

## Root cause and boundaries

**Established:** Under the unchanged L-493 rule, all repository files not expressly exempt must appear byte-identically in the Core/Companion embedded blocks. The experimental Path B branch adds unembedded files. This is sufficient to explain the observed 38-problem failure.

**Not established:** That all future L-493 failures have only this cause; that the main/default branch is affected; or that the experimental files ought to become part of a canonical release. Recheck each relevant branch and commit.

**Do not do without Originator approval:** edit canonical DOCX, update hash lists, weaken `required()`, add blanket exclusions, skip/neutralize the failing gate, merge or deploy.

## Architectural decision for review (not adopted)

A. **Canonical release branch remains frozen:** keep the existing self-contained Core/Companion release intact, perform Path B work in a separate proposal branch with explicit proposal-only CI. The full canonical release gate may be expected to fail on this experimental branch; communicate it as such, not as a passing release.

B. **Explicit experimental overlay / separate repository:** isolate proposal artifacts outside the canonical release tree, while preserving provenance and separate validation. Requires an approved release-boundary specification and repository governance decision.

C. **Approved future canonical release:** only after review, deliberately embed each approved release artifact, regenerate hashes and run complete release tests. This is a release change, not a workaround.

**Recommendation for review:** choose A as the current working posture and design B as a possible future packaging solution. No policy change or deployment has been made.

## Follow-up

1. Compare default-branch release CI with proposal-branch CI to avoid attributing branch-specific failure to canonical release.
2. Document intended CI semantics for proposal branches versus canonical release branches without changing the canonical verifier.
3. Continue Path B experimental tests, D2-B form coverage and D5 safety design.
4. Keep `HANDOVER_NEXT_SESSION.md` and Claude's progress note synchronized with verified evidence.
