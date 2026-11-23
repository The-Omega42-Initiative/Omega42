# Path B Dependency Audit — Protocol Reconstruction and Operation

**Status:** Working proposal / preliminary audit  
**Version:** 0.1  
**Audit baseline:** `main` at `423102f52d31a1ab7590efdee820da486ce97d17`  
**Prepared:** 23 November 2026  
**Authority:** Non-normative. This document does not amend the Core, Companion, L-493, release policy, licences, governance instruments, or CI.

## 1. Purpose and scope

This audit advances Path B by distinguishing what a person or AI Navigator needs to **understand, execute, verify, extend, publish, or administer** Omega42. These are different dependency classes. A local navigation should not require the hosted-service governance stack; operating a public submission service should.

The audit is a first-pass dependency analysis based on:
- the complete, non-truncated Git tree at the baseline commit (1,644 tracked files);
- direct inspection of `tools/extract_embedded.py`, which defines the current L-493 whole-repository embedding rule and its OUTSIDE/EXEMPT sets;
- the public README, AI access and setup instructions, identity statement, Navigator Pack, and selected runtime, release, licensing, privacy, governance and certification files;
- selected implementation files, including `tools/handshake.py`, `tools/output_form.py` and `tools/release_manifest.py`.

It is **not yet** a complete call-graph, import-graph, runtime-read, build-input or test-dependency trace. Every classification below is therefore provisional unless marked otherwise.

## 2. Baseline facts that constrain Path B

1. At the audited commit, the repository contains **1,644 tracked files**. The tree is not truncated.
2. The current extractor describes the Core and Companion as “the whole release” and requires every repository file to be embedded, except its explicit OUTSIDE, EXEMPT and archived categories. This is a repository-wide contract, not merely a CI convenience.
3. The extractor's OUTSIDE set contains 12 paths: the two source DOCX documents, two checksum files, two sealed/lost test-key paths, four AI reading editions/manifest entries plus the Existential Framework edition, and `llms.txt`. `tools/__init__.py` is EXEMPT; `archive/2025-10/` is excluded by prefix.
4. The README's user-facing local route is to attach the Core and Companion to an AI conversation and say **Welcome Navigator**. Its script route names `scripts/canonical_reference.py`. The AI Navigator Pack describes itself as the compact-in-context navigation subset rendered from the Core; it explicitly directs the reader to the full AI Core/Companion editions for indexed material and to the documents/repository to run tools.
5. `tools/handshake.py` makes a concrete distinction between a mathematical fingerprint, a live challenge, and a manifest check. It reads `omega42.identity.json` and `records/release_documents_SHA256.txt`; this is a real dependency chain for that identity handshake, not a universal requirement for every text-only navigation.
6. `tools/output_form.py` dynamically loads checkers and reads protocol data such as the Introduction JSON. Output-form verification therefore has a larger dependency closure than arithmetic navigation alone.
7. `tools/release_manifest.py` reads the rendered Core edition, amendment register, STP registry, SNCA report directory and correction register. It is a release/governance function, not a minimal Navigator execution dependency.
8. Legal and governance files define conditions for contributions, publication, privacy, moderation, branding, certification and hosted services. They are not all prerequisites to a private local navigation, but some become mandatory when the corresponding project function is offered.

## 3. Dependency model: five operational profiles

Path B should define packages against explicit **profiles**, rather than pretending there is one universal list of files every user needs.

### Profile A — Read and understand the protocol

Minimum:
- the exact, immutable Core release;
- the exact, immutable Companion release, identified as explanatory and subordinate to the Core;
- a release identity/version record and integrity digests;
- a short human/AI entry instruction (including the applicable Opening and Navigator identity requirements).

The Companion is not a second normative authority. The Core controls where they differ. A Navigator Pack can be supplied as a context-window aid, but it must identify its parent Core version and digest and must not silently replace the Core.

**Provisional package:** OPR normative documents plus a bound Companion edition or separately versioned explanatory dependency. Whether Companion is inside OPR or a mandatory, version-bound companion package remains an Originator decision.

### Profile B — Perform a text-only navigation

Minimum:
- Profile A;
- sufficient Core material to follow the exact counting, state, direction/arm, Aperture, output and signature rules;
- the user's exact question and the Navigator's disclosed model identity;
- an instruction that no tool or external permission is granted merely by an activation phrase.

No repository checkout, website, hosted service, legal entity, newsletter, research corpus or public register is inherently required to perform a private text-only navigation.

The exact set of Core provisions required for this profile should be declared as a named profile within the normative release. The Navigator Pack is a candidate distribution artifact, but it must be proven complete against that profile.

### Profile C — Execute and independently recompute the arithmetic

Minimum:
- Profile A/B;
- a pinned reference implementation, presently `scripts/canonical_reference.py`;
- its language/runtime requirements (currently Python 3; standard-library-only claim to be verified against the pinned source);
- canonical fixtures and known-answer tests;
- a version/hash binding between the implementation and the protocol release.

The canonical script is the clearest candidate for the **minimal executable arithmetic kernel**. It must not be conflated with the entire `tools/` directory, which contains many research, application, curation and release utilities.

### Profile D — Audit, validate and identify a Navigator implementation

Minimum depends on the conformance claim:
- arithmetic reference implementation and fixtures;
- the relevant output-format checker(s);
- identity/manifest handshake materials where that profile is claimed;
- all transitive checker dependencies and the data files those checkers read;
- conformance-suite definitions and public practice fixtures;
- a declared verification profile and reproducible commands.

Candidate files include `tools/format_check.py`, `tools/output_form.py`, `tools/handshake.py`, `tools/conformance.py`, `omega42.identity.json`, and their actual transitive dependencies. This is a candidate list, **not a certified complete closure**. The Certification Body and certification mark are not required to run the checks locally; they are required only if the project offers formal certification.

### Profile E — Operate the public Omega42 service and commons

This profile adds function-specific dependencies:
- contribution and intake rules, issue forms, bot/workflow code and permissions;
- licence and contributor terms;
- privacy, consent, retention, withdrawal and takedown procedures;
- moderation, appeals and Code of Conduct;
- prior-art disclosure procedure and immutable public-access evidence;
- governance authority and decision records;
- brand/trademark rules and certification rules where those services are actually offered;
- hosting, newsletter and archive configuration, contracts and security procedures.

These materials belong in OKR or an explicit Governance/Operations dependency package, not in the minimal arithmetic kernel. However, the service must not be deployed without the applicable policy and legal dependencies. A manifest reference alone is insufficient if the referenced document is missing, ambiguous or not yet approved.

## 4. Preliminary dependency classification

| Area / representative paths | Profile(s) | Proposed package | Preliminary disposition |
|---|---|---|---|
| Core DOCX and its normative rules | A–E | OPR | Normative root; immutable release identity required |
| Companion DOCX | A–E as explanatory context | OPR-bound or OKR dependency | Mandatory explanatory companion in current onboarding; subordinate to Core |
| `ai/Omega42_Navigator_Pack.md` | B | OPR distribution artifact | Generated context-window aid; bind to exact Core digest and test completeness |
| `ai/Omega42_Core_V335_Rev450.md`, Companion edition, `ai/manifest.json` | A, D, release tooling | OPR/OKR derived editions | Generated renderings; retain hashes and renderer provenance; not independent normative sources |
| `scripts/canonical_reference.py` | C–D | OPR runtime | Candidate minimal executable arithmetic reference |
| `tools/format_check.py`, `output_form.py`, `handshake.py`, `conformance.py` | D | OPR conformance | Include only after transitive dependency closure and fixtures are established |
| `omega42.identity.json`, release-document digest file | C–D | OPR manifest/integrity | Identity and integrity dependencies for declared handshake profile |
| `records/math/results.json` and canonical test fixtures | C–D | OPR conformance data | Include only the subset required by the normative profile; preserve provenance |
| Other `tools/*.py`, `scripts/*.py` | varies | OPR, OKR or OWAR by demonstrated role | No blanket inclusion or exclusion; trace each tool's role and dependencies |
| `records/**` navigation, APE, review, research, history, source and result corpus | Usually not A–C; selected files for D/E | OKR | Research and evidence corpus; only normative fixtures or runtime-read data move into OPR |
| `GOVERNANCE.md`, `ENTITY.md`, `PATENT_PLEDGE.md` | E | OKR / Governance dependency | Mandatory for institutional operation and stated commitments; not private local navigation |
| `CONTRIBUTING.md`, `LICENSES.md`, `CODE_OF_CONDUCT.md`, `MODERATION.md` | E | OKR / Commons Operations | Mandatory for accepting, licensing and moderating contributions |
| `PRIVACY.md`, `COMMERCIAL.md` | E | OKR / Service Operations | Mandatory before operating relevant hosted or commercial services; reconcile consent/withdrawal claims |
| `PRIOR_ART.md`, `records/prior_art/**`, submission templates | E | OKR / Disclosure Operations | Separate formal disclosure function; dates and public-access evidence need legal-grade review |
| `CERTIFICATION.md`, certification records and suite | D/E when certification offered | OKR / Certification dependency | Local conformance is possible without an institution; formal certification requires governance, independence and legal status |
| `TRADEMARK.md`, brand assets | E/public distribution | OKR / Brand dependency | Not a mathematical/runtime dependency; controls use of marks and badges |
| `site/**`, `tools/site_build.py`, pages, styles, assets | website only | OWAR | Presentation and web application; not required for local navigation |
| `.github/workflows/**`, issue/discussion templates | repository service | OKR or OWAR operations | Development/hosting automation; only release-critical workflows belong in release verification contract |
| `tools/build/**`, `tools/ai_edition.py`, release builder scripts | release engineering | Development/Release tooling | Build inputs and reproducibility tools; do not classify as Navigator runtime without evidence |
| `HANDOVER_NEXT_SESSION.md`, working notes, session-specific handovers | none for runtime | Development records | Exclude from released runtime packages; preserve in repository history where appropriate |
| `archive/2025-10/**` | historical reference | OKR archive | Historical edition, separately indexed and integrity-bound |
| sealed blind-test keys | blind-test administration only | restricted test operations | Never package with public Navigator or conformance runtime; keep access-controlled and hash-committed |

## 5. Governance and legal documents: when are they mandatory?

A key Path B distinction is **conditional mandatory dependency**:

- A person privately using a released copy does not need the Company's governance constitution, commercial terms, newsletter rules or certification-body documents to calculate a coordinate or conduct a local navigation.
- A contributor submitting material to the Commons does need clear licence, attribution, submission, privacy and moderation terms before submission.
- The project accepting or publishing that material needs operational authority, a valid moderation process, rights clearance, a privacy/withdrawal policy and a functioning takedown route.
- The project publishing formal prior-art disclosures needs a disclosure-specific consent and publication procedure, reliable date/public-access evidence, and explicit warnings about patent consequences.
- The project operating a hosted Navigator needs a privacy notice, consent model, retention/deletion rules, security controls, service terms and a clear record of what is submitted.
- The project offering paid services or certification needs the applicable commercial, entity, governance, mark, independence, appeal and financial controls to be legally established and operational.

**Important:** the presence of these documents in the repository does not prove that the legal entity exists, that a pledge has been signed, that a Certification Body is constituted, or that a hosted service is legally ready. Documents currently describing future steps remain design documents until the stated steps are completed.

## 6. Architecture consequence for Path B

The Protocol Release should not be defined as “all files needed for every Omega42 activity.” It should be defined as the smallest **normative and executable protocol substrate**, with declared profiles and dependencies.

Recommended release graph:

- **OPR — Omega42 Protocol Release:** normative Core, mandatory explanatory binding, protocol identity, minimal runtime, canonical fixtures, conformance profile and all transitive dependencies required by those declared functions.
- **OKR — Omega42 Knowledge and Research Release:** research corpus, prior-art disclosures, governance/legal/commons policies, historical material, non-runtime registers and evidence records. It can contain subprofiles such as Commons Operations, Prior-Art Operations and Certification Operations.
- **OWAR — Omega42 Website and Applications Release:** website, apps, presentation assets, editorial onboarding and their build/runtime dependencies.
- **Release Engineering Kit:** build, packaging, signing, validation and publication tools. This may be a tooling layer attached to coordinated releases rather than a fourth public product package.

A top-level release manifest must declare:
- exact package versions and immutable commit/archive IDs;
- file-level digests and licence/provenance;
- normative authority and status;
- profiles each package supports;
- mandatory and optional dependencies;
- compatibility constraints;
- build and verification commands;
- generated-artifact source and reproducibility data;
- restricted material that must never enter public packages.

## 7. Findings and risks requiring resolution

### F1 — The current “whole release” contract is explicit (CONFIRMED)
The extractor's opening text and implementation make every repository file part of the self-contained release except fixed exclusions. Path B therefore requires a formally authorised change to the release contract and Core references. It cannot be achieved by changing only CI or the extractor.

### F2 — There is no single runtime dependency profile (CONFIRMED)
The repository distinguishes at least text-only navigation, arithmetic recomputation, output auditing, identity handshake, release engineering, public commons operation and certification. Their dependency closures differ.

### F3 — Navigator Pack is a candidate profile artifact, not yet proven self-sufficient (PROVISIONAL)
It describes the Core sections needed in one context window and links to full editions and tools. A formal completeness test must compare every rule invoked during a Profile B navigation against the pack and identify every required external dependency.

### F4 — Arithmetic kernel can be narrower than the current tools corpus (PROVISIONAL)
The README identifies `scripts/canonical_reference.py` as the local Python route. Its imports, file reads, fixtures and exact command should be traced. It should not be assumed that all 156 files under `tools/` are required to navigate.

### F5 — Output verification has a larger closure (CONFIRMED)
`tools/output_form.py` dynamically loads specialized checkers and reads additional protocol data. A conformance package must include the transitive closure for each claimed checker, not just the top-level script.

### F6 — Legal/governance dependencies are service-specific (FORMALLY DERIVED FROM CURRENT DOCUMENT PURPOSES; LEGAL EFFECT OPEN)
The local navigation route and the hosted/public service route are different. Legal/commons documents should be mandatory dependencies for the services they govern, not unconditional prerequisites to private arithmetic use. Counsel must determine legal status and enforceability.

### F7 — The current document corpus contains future-state commitments (CONFIRMED)
Examples include the Company, signed pledge, Certification Body and service arrangements described as steps or future operations. Release packaging must preserve their actual status and must not imply implementation merely because a policy file exists.

### F8 — Generated AI editions need provenance and binding (CONFIRMED)
The AI editions and Navigator Pack are rendered from the DOCX sources by `tools/ai_edition.py`; their manifest records hashes and estimated token counts. They must be treated as derived artifacts, with source digest, renderer version, generation process and exact parent release.

### F9 — Whole-repository inventory is complete at the tree level, but dependency tracing is not (CONFIRMED)
The baseline tree contains 1,644 tracked files. This audit has not yet traced every import, dynamic load, path read, test reference, build input, workflow, generated artifact or secret/restricted-data boundary.

## 8. Next technical work

1. Extract the complete path inventory into a machine-readable file at the baseline commit, including hidden files and workflows.
2. Trace Python imports and dynamic loads for the candidate Profile C/D scripts.
3. Trace file reads and protocol references in the Navigator Pack and the relevant Core sections.
4. Identify the smallest test fixtures that establish arithmetic, format and identity conformance.
5. Build a clean-room Profile A/B/C/D reconstruction in a temporary workspace, without changing canonical files or L-493.
6. Run the candidate packages without the full repository and record missing-file failures.
7. Compare each profile's required files with the preliminary classification register and update confidence labels.
8. Only after that, draft the formal amendment to the release contract for Originator/ESC review. No amendment is implied by this audit.

## 9. Decisions reserved for the Originator

1. Does the Companion remain physically inside OPR, or become a separately versioned but mandatory explanatory package bound to the Core?
2. Is the initial OPR target Profile B (text-only navigation), Profile C (script-recomputable navigation), or both?
3. Should formal conformance and identity handshake be part of the minimum OPR, or a separately declared conformance profile?
4. Which governance/commons functions are intended for the first public service release, as opposed to future roadmap items?

Until these decisions are made, the package boundaries in this audit remain provisional.

## 10. Explicit non-actions

This audit does not:
- modify the Core or Companion;
- modify `tools/extract_embedded.py`, L-493 or any workflow;
- remove or reclassify files in the canonical repository;
- publish or withdraw any prior-art disclosure;
- establish legal entities, execute pledges or launch hosted services;
- claim a complete dependency graph or passing clean-room reconstruction;
- authorise a merge, release or deployment.

**Working conclusion:** Path B is technically plausible, but it is a change in the definition of what constitutes a self-contained Omega42 release. The safest design is profile-based: preserve the complete normative substrate for each declared capability, while binding research, governance, service and presentation packages through an immutable coordinated release manifest.