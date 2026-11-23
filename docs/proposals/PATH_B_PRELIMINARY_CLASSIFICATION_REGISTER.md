# Path B — Preliminary Repository Classification Register

**Status:** WORKING INVENTORY — NOT COMPLETE; FOR ORIGINATOR REVIEW  
**Version:** 0.1  
**Date:** 23 November 2026  
**Authority:** Non-normative planning artifact  
**Basis:** Known repository paths and targeted inspection of current main. This is not a complete Git tree export and is not a final file manifest.

## 1. Purpose

This register begins the classification work required by Path B. It assigns provisional package destinations to known files, records their apparent function and authority, and flags decisions requiring review.

It does not change any file's normative status, release status, licensing, publication status or CI treatment. Existing L-493 remains in force.

## 2. Important baseline finding

The current main version of tools/extract_embedded.py explicitly describes the Core and Companion as "the whole release" and says every repository file is embedded except a narrow OUTSIDE set. Path B therefore requires a formal amendment to the normative release contract, not merely a revised file list or extractor.

The extractor's opening comment identifies the intended exceptions as the two canonical documents, their two hash lists and sealed keys of the two open blind tests. The actual OUTSIDE and EXEMPT definitions must be inspected in full during implementation planning.

## 3. Provisional classification register

| Repository path | Proposed class | Proposed package | Reason / dependency | Decision or verification required |
|---|---|---|---|---|
| docs/Omega42_Core_Specification_V335_Rev450_STABLE.docx | P-NORM | OPR | Main normative specification and protocol authority | Confirm exact canonical version and embedded-source relationship |
| docs/Omega42_Companion_Document_V335_Rev450_STABLE.docx | P-NORM / P-INFO (mixed) | OPR initially | Companion is part of current reconstruction and explanatory design | Decide whether it remains in OPR or becomes a separately versioned mandatory companion |
| tools/extract_embedded.py | P-RUNTIME / P-TEST | OPR during transition | Implements current extraction and L-493 verification | Do not change until replacement is approved and tested |
| README.md | W-SITE / W-INFO | OWAR, unless normative portions identified | Public entry point and introduction | Identify any mandatory instructions; do not assume README is protocol authority |
| WELCOME.md | W-SITE | OWAR | Public onboarding and discovery content | Verify whether it contains normative instructions |
| IDENTITY.md | P-NORM / W-INFO (unresolved) | OPR if identity/handshake is normative; otherwise OWAR or OKR | Described by README as technical identity and handshake | Inspect Core references and conformance dependencies |
| docs/VISION.md | W-SITE | OWAR | Public introductory paper; current text identifies itself as non-normative | Confirm no mandatory requirements are embedded |
| GOVERNANCE.md | K-NORM | OKR, with explicit mandatory reference if Core relies on it | Roles, decision rights, stewardship and governance | Determine constitutional authority and incorporation into OPR |
| ENTITY.md | K-NORM | OKR | Intended legal entity architecture and institutional roles | Confirm adopted versus proposed status; legal review |
| PATENT_PLEDGE.md | K-NORM | OKR, with explicit contributor/release dependency | Company/project patent commitments and rights implications | Clarify Company-only versus contributor obligations; legal review |
| CONTRIBUTING.md | K-NORM / K-INFO | OKR | Contributor intake, publication and contribution terms | Separate binding terms from explanatory submission guidance |
| PRIOR_ART.md | K-NORM / K-INFO | OKR | Prior-art process and disclosure conditions | Separate adopted policy from explanation; verify evidence requirements and obtain legal review |
| PRIVACY.md | K-NORM | OKR | Privacy statements and processing commitments | Link to hosted-service release; privacy/legal review |
| COMMERCIAL.md | K-NORM | OKR | Commercial/service terms and operational commitments | Determine service dependencies |
| TRADEMARK.md | K-NORM | OKR | Brand and mark ownership/licensing rules | Legal review; distinguish policy from executed registrations |
| MODERATION.md | K-NORM | OKR | Moderation, removal and appeal rules | Reconcile with withdrawal, privacy and permanent-record provisions |
| tools/site_build.py | W-SITE | OWAR | Website build tooling | Website package build dependency |
| site/pages/index.html | W-SITE | OWAR | Homepage presentation and navigation | Verify generated-site dependencies |
| site/pages/explore.html | W-SITE | OWAR | Discovery and Co-Builder review experience | No protocol execution dependency identified |
| site/pages/aperture.html | W-SITE | OWAR | Human Aperture explanatory page | No protocol execution dependency identified |
| site/pages/faq.html | W-SITE | OWAR | Public explanatory content | Policy statements should link to canonical policy |
| site/pages/research.html | W-SITE | OWAR | Public research presentation | Research records themselves belong in OKR |
| site/pages/symbols.html | W-SITE | OWAR | Public symbol reference/presentation | Determine whether definitions are normative and duplicate canonical definitions |
| site/pages/ (remaining pages/assets) | W-SITE | OWAR | Website source and presentation assets | Full tree inventory required |
| HANDOVER_NEXT_SESSION.md | D-DEV | Not public by default | Session handover and development coordination | Promote only if deliberately adopted as permanent record |
| records/release_documents_SHA256.txt | P-TEST / release metadata | OPR | Current release integrity records | Confirm relationship to future manifest |
| SHA256SUMS | P-TEST / release metadata | OPR or top-level manifest | Integrity inventory | Avoid competing sources of truth |
| Sealed blind-test keys | P-TEST / restricted | Controlled OPR test artifact or separate controlled release | Existing extractor identifies these as special exceptions | Preserve secrecy and test validity; inspect exact paths/access |
| ai/manifest.json, ai/*.md, llms.txt | W-INFO / derived distribution | OWAR or generated distribution | AI-oriented rendered editions and discovery metadata | Record parent release and reproducible generation process |
| archive/2025-10/ | A-ARCHIVE | Archive | Historical preserved material | Preserve immutable references and reconstruction rules |
| tools/__init__.py | P-RUNTIME or D-DEV (unresolved) | OPR if imported at runtime; otherwise non-runtime | Current checker reportedly treats it as exempt | Inspect imports and execution dependencies |
| submissions/prior-art/ | K-RESEARCH / formal disclosure | OKR | Formal public disclosure packages | Rights clearance, immutable evidence and status per record |
| records/prior_art/ledger.jsonl | K-RESEARCH / K-NORM (unresolved) | OKR | Disclosure ledger and provenance record | Define authority and evidence for public-access dates |
| submissions/navigations/, submissions/ape/, submissions/reviews/ | K-RESEARCH | OKR | Submitted research/navigation material | Consent, moderation, retention and acceptance status |
| examples/corpus/ | K-RESEARCH / P-TEST (unresolved) | OKR or OPR fixtures | May support examples and/or conformance | Separate required test vectors from optional corpus |
| apps/ | W-APP | OWAR | Application source | Full inventory and dependency mapping required |
| contrib/ | W-APP / K-RESEARCH (unresolved) | OWAR or OKR | Community contributions | Classify each artifact by purpose, licence and dependency |

## 4. Classification rules

1. Normative authority takes precedence over file location. A file is not OWAR merely because it is linked from the website.
2. Runtime necessity is not the only form of normativity. Governance and contributor instruments can be binding without being runtime dependencies.
3. Explanatory duplication must not create a second authority. Website pages should identify and link to canonical definitions.
4. Mixed files must be split or explicitly typed.
5. Tests are package dependencies when they define conformance; optional examples are not automatically P-TEST.
6. Derived files must identify their source release and reproducible generation process.
7. Privacy and rights restrictions override packaging convenience.
8. Classification does not itself change current policy or L-493.

## 5. Priority ambiguities

### A. Main Companion boundary

Current design treats Core and Companion together as the complete release. Decide whether both remain OPR or whether Companion becomes a separately versioned, tightly bound explanatory package. If separate, specify whether it is required for Navigator reconstruction, onboarding or neither.

### B. Governance and legal instruments

Distinguish constitutional project rules, executed legal instruments, contributor terms binding by acceptance, operational policies, and explanatory descriptions/proposals. A K-NORM document may sit outside runtime packaging, but its authority and dependencies must remain explicit.

### C. README and identity material

README is a public entry point. IDENTITY is described as technical identity and handshake. Inspect whether IDENTITY is an execution contract or descriptive onboarding; split mixed responsibilities if needed.

### D. Prior-art record and ledger

Formal disclosures and the authoritative ledger belong in OKR, but require criteria for enabling disclosure, immutable version, public accessibility date, rights clearance and archival evidence. A hash alone does not prove public accessibility.

### E. Tests, corpus and sealed keys

Separate public test fixtures, required conformance vectors, optional examples and sealed challenge material. Preserve current security and test-integrity properties.

## 6. Work required for a complete register

1. Enumerate every tracked file at a fixed commit SHA, including hidden configuration and workflow files.
2. Read the full current OUTSIDE and EXEMPT definitions and all L-493/Core references.
3. Trace imports, build inputs, runtime reads and test references to identify actual dependencies.
4. Identify generated files, archives, third-party assets, secrets and restricted data.
5. Assign each file a classification, package, authority status, maintainer, licence, provenance and dependency set.
6. Mark classifications CONFIRMED, PROVISIONAL or DISPUTED.
7. Produce machine-readable inventory and human-readable review table.
8. Build package prototypes without changing L-493 or canonical documents.
9. Compare clean-room reconstruction and verification against the current release process.

## 7. Current status

- Path B proposal: prepared, awaiting Originator review.
- This register: preliminary seed inventory only.
- Full repository enumeration: not completed.
- Dependency tracing: not completed.
- Package prototypes: not started.
- Canonical documents: unchanged.
- L-493 extractor and CI: unchanged.
- Release policy: unchanged.

The current main-branch extractor still defines the Core and Companion as the whole release. This register does not supersede that rule.
