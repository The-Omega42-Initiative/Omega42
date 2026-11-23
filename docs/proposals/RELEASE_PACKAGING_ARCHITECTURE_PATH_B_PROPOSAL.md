# Omega42 Release Packaging Architecture — Path B Proposal

**Status:** PROPOSAL FOR ORIGINATOR REVIEW  
**Version:** 0.1  
**Date:** 23 November 2026  
**Decision authority:** Originator, subject to applicable project governance  
**Normative status:** Non-normative proposal. This document does not amend the Main Core, Main Companion, governance instruments, release rules or CI implementation.

---

## 1. Executive proposal

Adopt a layered release architecture in which Omega42 is distributed as coordinated, versioned packages rather than requiring every repository file—regardless of function—to be embedded byte-for-byte in the Main Core Specification or Main Companion Document.

The proposed model has three release products:

1. **Omega42 Protocol Release (OPR):** the self-contained normative and executable protocol substrate.
2. **Omega42 Knowledge and Research Release (OKR):** the versioned research, discoveries, formal disclosures, governance and policy materials associated with the protocol but not necessarily required by its runtime.
3. **Omega42 Website and Applications Release (OWAR):** website source, editorial/onboarding material, applications, presentation assets and their build/deployment tooling.

A top-level release manifest binds the packages to one release identity through exact versions, immutable commit or archive identifiers, cryptographic hashes, compatibility declarations and provenance.

**Central principle:** self-containment should be defined by the needs of protocol reconstruction, execution, verification and authority—not by the fact that a file happens to exist somewhere in the repository.

This is not a proposal to weaken the Core, relax verification, or move important rules into informal website content. It is a proposal to define the boundary of the self-contained protocol release explicitly and testably.

## 2. Problem statement and evidence

The current `tools/extract_embedded.py` implements L-493 by requiring every repository file to be embedded in the Main Core or Companion, except its fixed `OUTSIDE` set, `tools/__init__.py`, bytecode/cache exclusions and the archived `archive/2025-10/` tree.

The rule is clear and mechanically enforceable. Its current scope treats files with materially different functions as if they were all part of one indivisible protocol release. Website pages, website build tooling, editorial material and session handover notes are treated as required embedded release files. A website editorial improvement can therefore require canonical Word document regeneration even when no protocol rule, mathematical definition or runtime dependency has changed.

On tested PR #3 commit `c23cb9c001297b6c11bdbeccebd55c4bfe4c338e`, L-493 reported:

- 1,619 embedded blocks;
- 1,621 required repository files;
- 12 explicitly defined outside files;
- 11 problems;
- not embedded: `HANDOVER_NEXT_SESSION.md`, `site/pages/aperture.html`;
- embedded-copy mismatches: `README.md`, `PRIOR_ART.md`, `tools/site_build.py`, `site/pages/explore.html`, `site/pages/faq.html`, `site/pages/index.html`, `site/pages/research.html`, `site/pages/symbols.html`, `docs/VISION.md`.

This is a packaging-policy result under the current rule, not a failure of the mathematical reference tests. It does not by itself prove Path B is the correct policy; it motivates the design for review.

## 3. Objectives

The release architecture should:

1. Preserve the Main Core as normative authority for protocol definitions, execution rules, mathematical foundations and mandatory constraints.
2. Preserve the Main Companion's defined explanatory/exploratory role without making it a substitute for the Core.
3. Make the Protocol Release independently reconstructible and verifiable from its declared contents.
4. Keep normative policies and rights instruments under explicit version control and authority.
5. Allow website, editorial and application development to evolve without regenerating canonical protocol documents for unrelated presentation changes.
6. Bind all coordinated packages to one release identity through a verifiable manifest.
7. Preserve reproducibility, provenance, hashes, compatibility and audit trails.
8. Keep CI strict: each package passes its own completeness and integrity checks, and the coordinated release passes cross-package checks.
9. Support independent implementations and future distribution channels.

## 4. Non-goals and safeguards

Path B must not weaken mathematical verification; change canonical mathematics or protocol semantics; allow a website page to override the Core; move mandatory rules into an unreferenced optional location; mistake a hash for proof of public accessibility or legal validity; create broad discretionary checker exemptions; or authorise merging/deployment of PR #3.

A file being outside OPR does **not** make it non-normative or legally unimportant. Its authority and dependencies must be declared. Changes to normative status, legal obligations or governance remain subject to the appropriate approval process and legal advice where required.

## 5. Proposed package model

### 5.1 Omega42 Protocol Release (OPR)

**Purpose:** provide everything required to understand, reconstruct, execute and verify the protocol.

Candidate contents:

- Main Core Specification and exact version;
- Main Companion Document and its declared explanatory status;
- canonical reference implementation and required runtime tools;
- mathematical definitions, constants, schemas, algorithms and execution contracts;
- mandatory conformance fixtures and test vectors;
- protocol-level safety, permission, integrity and verification requirements;
- normative policy texts required to determine conformance or implementation obligations;
- package manifest, file inventory, hashes and reconstruction instructions.

**Self-containment test:** a clean environment holding only the declared OPR package and its documented prerequisites can reconstruct the required protocol working tree and run all mandatory protocol verification tests without fetching undeclared project files.

The OPR must state which documents are normative, explanatory, informative or illustrative. The Core remains the final authority where documents conflict, subject to the explicitly defined constitutional hierarchy.

### 5.2 Omega42 Knowledge and Research Release (OKR)

**Purpose:** distribute the versioned knowledge, research and stewardship record associated with Omega42 but not required by protocol runtime execution.

Candidate contents:

- research and working papers;
- mathematical investigations and discovery records;
- formal prior-art disclosures and immutable evidence packages;
- research registers and open problems;
- governance/legal instruments not embedded in OPR, where their authority and relationship to OPR are explicit;
- contributor and licensing information;
- provenance, decision and change records;
- research datasets, subject to rights, privacy and consent controls.

Each item carries a declared status: for example, normative policy, executed legal instrument, formal disclosure, research record, explanatory material or provisional proposal.

Where a policy is required for conformance or contributor obligations, OPR must either include it or identify an exact, immutable, mandatory dependency and define what happens if it is unavailable or version-mismatched. A website link alone is insufficient.

Personal readings, private material, redacted records and formal prior-art disclosures retain their separate consent, withdrawal, privacy and permanence rules. This packaging proposal does not resolve those policy questions.

### 5.3 Omega42 Website and Applications Release (OWAR)

**Purpose:** distribute the public-facing and application layer.

Candidate contents:

- website HTML, CSS, JavaScript and media assets;
- site generator and website build tooling;
- public onboarding and editorial pages;
- application source, user-interface assets and application-specific connectors;
- accessibility/responsive-design tests;
- deployment configuration and site-generation instructions.

OWAR may explain and link to canonical releases. It may not silently redefine protocol semantics or legal obligations. The website identifies the exact OPR and OKR versions it presents. If website explanation conflicts with a normative release, the normative release controls and the discrepancy must be corrected.

### 5.4 Development and operational records

Temporary handover notes, internal session records, scratch material, caches and non-release working files are classified separately. They are not public release components by default. A handover or decision record intended as permanent governance/provenance must be promoted through explicit review and classification.

## 6. Release manifest and binding

Each coordinated release has a top-level manifest, for example `release/OMEGA42_RELEASE_MANIFEST.json`.

Illustrative schema only:

```json
{
  "release_id": "Omega42-YYYY.MM",
  "release_date": "YYYY-MM-DD",
  "status": "candidate",
  "packages": {
    "protocol": {
      "version": "x.y.z",
      "commit": "<immutable-commit-sha>",
      "archive_sha256": "<sha256>",
      "manifest_path": "protocol/MANIFEST.json"
    },
    "knowledge_research": {
      "version": "x.y.z",
      "commit": "<immutable-commit-sha>",
      "archive_sha256": "<sha256>",
      "manifest_path": "knowledge/MANIFEST.json"
    },
    "website_applications": {
      "version": "x.y.z",
      "commit": "<immutable-commit-sha>",
      "archive_sha256": "<sha256>",
      "manifest_path": "website/MANIFEST.json"
    }
  },
  "compatibility": {
    "protocol_api": "declared-version",
    "minimum_website_protocol": "declared-version",
    "minimum_knowledge_release": "declared-version"
  },
  "provenance": {
    "source_repository": "The-Omega42-Initiative/Omega42",
    "release_commit": "<immutable-commit-sha>",
    "builder": "<declared-build-process>",
    "verification_record": "<immutable-record-reference>"
  }
}
```

The placeholders are illustrative; this does not claim that these packages, versions, archives or signatures already exist.

Integrity and authenticity requirements:

- SHA-256 or a successor approved by the project binds exact bytes to a manifest entry.
- A hash establishes integrity relative to the recorded digest; it does not independently establish authorship, public accessibility, disclosure date or legal validity.
- Provenance records the source commit, build process, materially relevant toolchain and verification results.
- Where practicable, the manifest is signed by an authorised release key. Key ownership, rotation, revocation and recovery must be documented.
- Published archives use immutable version identifiers. Corrections create a new version rather than silently replacing a prior artifact.
- Manifests and verification records are retained for independent audit.

## 7. Repository file classification

Every tracked file intended for distribution receives an explicit classification:

| Class | Meaning | Default package |
|---|---|---|
| P-NORM | Normative protocol requirement or conformance dependency | OPR |
| P-RUNTIME | Required executable/runtime component | OPR |
| P-TEST | Mandatory conformance fixture or verification asset | OPR |
| K-NORM | Normative governance/legal/contributor instrument not required for runtime | OKR, with explicit mandatory reference if applicable |
| K-RESEARCH | Research, discovery, formal disclosure or knowledge record | OKR |
| W-SITE | Website source, editorial content and presentation assets | OWAR |
| W-APP | Application source and application-specific assets | OWAR |
| D-DEV | Development-only, temporary or internal operational material | Not public by default |
| A-ARCHIVE | Preserved historical artifact | Archive package or immutable archive reference |

Classification is based on function and authority, not file extension, directory or convenience. A policy can be in OKR yet remain a mandatory OPR dependency; the manifest must represent that relationship explicitly.

## 8. Proposed CI architecture

### Gate 1 — Protocol package completeness

- Enumerate every file required by the OPR manifest.
- Fail on missing, unlisted, ambiguous or hash-mismatched files.
- Reconstruct OPR in a clean temporary environment using only declared contents and prerequisites.
- Run all mandatory mathematical, reference, execution and conformance tests.
- Verify byte-identical embedded blocks where the Core continues to require them.
- Verify mandatory normative dependencies and version constraints.

### Gate 2 — Knowledge and Research integrity

- Verify inventory and hashes.
- Verify status, version, provenance and classification metadata.
- Check formal disclosures for required immutable evidence and publication metadata.
- Ensure restricted, personal or consent-controlled material is excluded from public archives.
- Check cross-references to the applicable OPR version.

### Gate 3 — Website and Applications

- Build from declared source.
- Run link, navigation, accessibility and responsive-layout checks where available.
- Verify that public pages identify the intended OPR/OKR versions.
- Check that website content does not silently contradict or replace normative protocol text.
- Run application-specific tests.

### Gate 4 — Coordinated release

- Verify the top-level manifest.
- Confirm every package reference resolves to an immutable artifact.
- Confirm compatibility declarations.
- Verify hashes and, if adopted, signatures.
- Produce machine-readable and human-readable verification reports.
- Fail the release if any package or cross-package dependency fails.

### Gate 5 — Repository hygiene

- Ensure every tracked file is classified.
- Ensure no unclassified file silently enters a release.
- Ensure development-only material is not accidentally published.
- Enforce archive and retention rules.

The proposal replaces one universal repository-wide embedding test with explicit package-boundary tests. It does not replace strict verification with discretionary judgement.

## 9. Relationship to current L-493

The existing L-493 rule remains authoritative unless and until the Originator and applicable governance authority approve a formal amendment and canonical documents are updated.

If Path B is approved, the amendment must:

1. Define OPR boundaries and protocol self-containment.
2. Define Core, Companion, normative policy and mandatory external dependency relationships.
3. Define OKR and OWAR and their authority limits.
4. Define manifest and compatibility mechanisms.
5. Define package-level and coordinated CI gates.
6. Define file classification and approval of classification changes.
7. Define historical release reconstruction.
8. Define behavior when a mandatory external package is unavailable, withdrawn, superseded or erroneous.
9. Define provenance and signing requirements, if adopted.
10. Update extractor/checker, tests, release instructions and embedded copies in one controlled change.

The old checker must not simply be weakened. It should be replaced only when package tests demonstrate equivalent or stronger assurance for OPR and clear assurance for the other release products.

## 10. Migration plan

**Phase 0 — Originator decision**
- Review, approve, reject or amend the architecture.
- Confirm package boundaries and mandatory policy dependency principle.
- Decide whether signing is required for the first implementation.
- No canonical documents or CI rules change.

**Phase 1 — Inventory and classification**
- Inventory all tracked files.
- Assign proposed classification and package.
- Identify embedded files and whether each is a protocol, policy, knowledge, website/application or development dependency.
- Produce a dependency graph and submit ambiguous cases for decision.

Deliverable: reviewed classification register and dependency map.

**Phase 2 — Package prototypes**
- Build OPR from current canonical documents and required protocol files.
- Build OKR and OWAR as separately versioned packages.
- Generate a top-level manifest.
- Do not make the new model authoritative.

Deliverable: reproducible prototypes and comparison report.

**Phase 3 — Parallel verification**
- Run existing L-493 unchanged.
- Run proposed package validators.
- Compare assurance.
- Demonstrate OPR reconstruction without OWAR or undeclared dependencies.
- Demonstrate that mandatory policy dependencies remain available and unambiguous.
- Record assurance gaps.

Deliverable: verification evidence and independent review.

**Phase 4 — Canonical amendment (only after explicit approval)**
- Amend/version Main Core and Companion as required.
- Amend release/governance documentation through proper process.
- Update extractor and CI workflow in the same controlled change.
- Update hashes, manifests, instructions and fixtures.
- Preserve exact reconstruction of historical releases.

Deliverable: new canonical release with approved packaging contract.

**Phase 5 — First coordinated release**
- Publish package artifacts and top-level manifest.
- Publish verification report.
- Verify external retrieval and independent reconstruction.
- Announce compatibility and version policy.

No release is complete until every required gate passes.

## 11. Governance and authority

Proposed responsibility allocation:

- **Originator/Overseer:** decides architectural direction and changes reserved to the Originator under existing governance.
- **Stewardship Committee:** exercises only authority actually granted by adopted instruments.
- **Company Board or relevant corporate body:** handles corporate release operations and legal obligations within its authority.
- **Protocol maintainers:** implement approved technical changes and maintain CI evidence.
- **Independent reviewers/Co-Builders:** challenge, identify omissions and recommend alternatives; review does not confer approval authority.
- **Contributors:** comply with applicable versioned contributor terms and licences.

This proposal does not assume that any proposed committee, company, certification body or legal instrument is already incorporated, operational or authorised beyond current canonical records.

## 12. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Normative rule accidentally moved outside OPR | Mandatory dependency register, conformance tests and Core precedence |
| Website becomes unofficial protocol truth | Version banners, immutable Core references and automated cross-checks |
| Package versions drift | Top-level manifest and compatibility constraints |
| Package disappears | Immutable archives, mirrors, retention and reconstruction instructions |
| Hash mistaken for proof of public disclosure | Separate timestamped public-access evidence and archival records |
| More packages increase complexity | Automated manifests/builders and one coordinated report |
| Classification becomes an exemption loophole | Narrow taxonomy, approval, audit trail and CI completeness check |
| Historical release becomes irreproducible | Preserve manifests, artifacts, toolchains and verification records |
| Privacy-controlled material is published | Rights/consent classification and pre-release review |

## 13. Open design questions

1. Should the Main Companion be part of OPR or separately versioned as a companion package?
2. Which governance/legal policies are mandatory protocol dependencies, and which belong only in OKR?
3. Should OKR distinguish executed legal instruments, adopted governance policy, formal prior-art disclosures and non-normative research?
4. Should website and applications be one OWAR package or separate packages?
5. Should signing be required from the first release, and what key custody/recovery model is appropriate?
6. Should versions use semantic versioning, date-based releases or a hybrid?
7. What minimum archival and mirroring requirements apply?
8. Who approves classification and package-boundary changes under existing governance?
9. What happens if a mandatory OKR policy dependency is unavailable?
10. How is the current promise—that a Navigator holding the Core and Companion can reconstruct the working tree—preserved or deliberately revised?

## 14. Recommended design principles for Originator consideration

- **R1 — Functional self-containment:** OPR contains everything required to reconstruct and verify the protocol, not automatically every file in the project repository.
- **R2 — No silent demotion:** separate packaging does not make a normative rule or legal obligation optional.
- **R3 — Explicit boundaries:** every distributed file has a declared package, classification and authority status.
- **R4 — Coordinated immutable releases:** packages are bound by one manifest, exact versions, hashes and provenance.
- **R5 — Strict independent CI:** every package and the coordinated release pass completeness and integrity gates.
- **R6 — No ad hoc exemptions:** boundary changes are reviewed and recorded; CI cannot be made green by unexplained exclusions.
- **R7 — Canonical-first migration:** existing L-493 remains authoritative until the approved replacement is reflected in canonical documents and CI.
- **R8 — Historical reproducibility:** prior releases remain reconstructible under the rules that governed them.

## 15. Independent review requested from Claude Opus 5.5

Claude is invited to challenge this proposal on:

1. Whether three packages are the right abstraction or another decomposition is cleaner.
2. Whether OPR can be self-contained while normative governance/legal dependencies are separately distributed.
3. Whether manifest and dependency design is sufficient for independent reconstruction, verification and preservation.
4. Whether proposed CI gives assurance equivalent to or stronger than current L-493.
5. Whether authority of Core, Companion, policies and website remains unambiguous.
6. Whether a simpler migration preserves integrity while allowing website evolution.
7. Exact changes required to extractor, tests, Core, Companion and release workflow.

Requested response: executive recommendation; blocking/major/minor findings; alternative architecture if preferred; proposed schema/test cases; explicit disagreements; migration plan. Distinguish technical conclusions from governance/legal questions requiring the Originator or qualified counsel.

## 16. Approval record

No decision is recorded by this proposal.

- Originator decision: **PENDING**
- Governance review: **PENDING, if required**
- Legal review: **NOT YET OBTAINED**
- Technical implementation: **NOT STARTED**
- Canonical document amendments: **NONE**
- CI rule amendments: **NONE**
- Production release: **NOT AUTHORISED**

---

**OMEGA42 | THE NAVIGATOR**  
*First principles. Mathematical structure. Recursive discovery. The unknown.*


## 17. Supporting preliminary classification register

A preliminary, explicitly incomplete repository classification register has been prepared at [PATH_B_PRELIMINARY_CLASSIFICATION_REGISTER.md](PATH_B_PRELIMINARY_CLASSIFICATION_REGISTER.md). It is a seed inventory for review, not a complete tree export or approved package manifest. It records known file classifications, unresolved boundaries and the work required to complete dependency tracing. It does not amend L-493 or canonical documents.
