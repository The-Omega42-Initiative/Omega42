# Omega42 Legal and Governance Reconciliation

**Status:** Working audit for the Originator and South African legal counsel. This is not legal advice, an adopted policy, or an amendment to any canonical document.
**Audit basis:** Current `main` branch files inspected on 23 November 2026.
**Purpose:** Identify internal inconsistencies and unresolved design decisions before the Company is incorporated or the public open-commons commitments are relied upon.

## Executive conclusion

The canonical documents express a coherent and distinctive intention: establish a durable steward for Omega42, keep the protocol and accepted knowledge openly available, permit commercial use, prevent the Company from enclosing the intellectual commons through patents, and preserve human judgment and Originator oversight.

The documents are not yet sufficiently reconciled to serve as a single set of incorporation instructions. The most important issues are:

1. The legal form and relationship between the stewardship entity and commercial operations are not finally selected.
2. The publication/withdrawal rules conflict with the Overseer's open-record reserve and the permanence of prior-art disclosures.
3. The Company-level patent pledge is not an individual contributor-wide no-patent covenant.
4. The Certification Body's legal separation, ownership, mark ownership and decision independence are not fully specified consistently.
5. The Board, Stewardship Committee and Overseer powers need to be translated into legally valid company documents without purporting to override directors' statutory duties.
6. The trademark trust and transfer mechanism needs precise legal drafting.
7. The hosted web-app exchange and redacted personal-reading record need a complete privacy and consent design.

**Recommendation:** Do not incorporate or sign a patent pledge yet. First resolve the decisions in Section 8, then ask South African counsel to produce a written structure recommendation and draft the legal instruments.

---

## 1. What is already clear and should be preserved

These are the project's stated design intentions, not yet all enforceable legal outcomes.

- Omega42 is intended to remain an open intellectual and mathematical commons.
- The Company is a steward and operational vehicle, not the owner of the underlying ideas, inventions, methods, software contributions or discoveries.
- The Company will not seek, acquire, assert or use patents to restrict Omega42 subject matter.
- Contributors are not required to assign their copyright or patent rights to the Company.
- Published text and data are intended to use CC BY 4.0; code is intended to use Apache-2.0.
- Commercial use of openly licensed material is permitted, subject to the applicable licence and trademark rules.
- Omega42's name, logo and authenticity/certification badges may be protected as marks without claiming ownership of the underlying knowledge.
- The public protocol and open record are not to be made conditional on payment.
- Human judgment remains with the person; AI systems are contributors/instruments, not project sovereigns.
- The Originator retains a defined constitutional reserve after the stewardship transition.

These principles should be expressed consistently in the MOI or equivalent founding instrument, contracts, contributor terms, licences, trademark rules and operational policies.

## 2. Findings requiring resolution

### LG-01 — Legal form and entity architecture

**Severity: HIGH**

**Sources:** `ENTITY.md`, “Choosing the form”; `GOVERNANCE.md`, §§1–2 and 6; `COMMERCIAL.md`, “Money”.

`ENTITY.md` describes one principal Company and says a trading company may be owned by the non-profit body if needed. It lists a non-profit company, company limited by guarantee, foundation or company with an entrenched public-benefit purpose as possible forms. `GOVERNANCE.md` places commercial receipts, grants and sponsorship with the Company or a temporary fiscal host.

The earlier lawyer brief's Stewardship NPC plus Operations (Pty) Ltd is therefore an option, not the settled canonical design.

**Resolution required:** Counsel should compare:
- one South African NPC conducting permitted trading activity;
- one private company with suitable constitutional and contractual restrictions;
- a stewardship NPC owning an Operations (Pty) Ltd subsidiary;
- any legally suitable trust/foundation or guarantee structure, including its governance, tax and enforcement consequences.

The comparison must cover who owns shares, who controls appointments, whether profits may be distributed, how trading risk is isolated, grant/donation eligibility, tax, reporting, continuity and cross-border activity. Do not assume PBO approval follows automatically from NPC registration.

### LG-02 — Board and Stewardship Committee authority

**Severity: HIGH**

**Sources:** `ENTITY.md`, “How it is governed” and “Locked provisions”; `GOVERNANCE.md`, §§1–5.

The proposed Company Board has five directors: the Originator (or Overseer's nominee), two Committee appointees and two independent directors. The Stewardship Committee has seven members and controls protocol revisions, acceptance and record stewardship. Before the Committee exists, ESC appoints the directors who would otherwise be appointed by it.

Potential ambiguity:
- `GOVERNANCE.md` says the Originator decides “everything” during founding, while `ENTITY.md` gives the Company Board responsibility for strategy, budgets, contracts, commercial operations and the brand.
- The documents do not fully explain how Committee powers interact with the Company's directors' duties and powers under applicable company law.
- The Board's composition, appointment/removal process, vacancies, quorum, deadlock, conflicts and reserved matters need incorporation-ready detail.
- The transition from Originator-led founding to Committee-led stewardship needs a precise trigger, record and effective date.

**Resolution required:** Counsel should draft a decision-rights matrix separating (a) corporate powers and fiduciary duties, (b) protocol/stewardship powers, (c) reserved constitutional consent, and (d) operational delegations. The documents must not purport to relieve directors of statutory duties or create an invalid shadow-director arrangement.

### LG-03 — Locked provisions and succession

**Severity: HIGH**

**Sources:** `ENTITY.md`, “Locked provisions”; `GOVERNANCE.md`, §§2 and 4.

Locked provisions require both Overseer consent and five Stewardship Committee votes. Yet the Committee may not exist at incorporation, and the Overseer may later name a successor or allow the role to lapse into the Committee.

Unresolved:
- Who can approve an amendment before the Committee is constituted?
- What happens if the Committee has vacancies and cannot reach five votes?
- What happens if the Overseer dies, becomes incapacitated, resigns, cannot be contacted or declines to appoint a successor?
- If the Overseer role lapses, how is the constitutional reserve exercised?
- How are emergency legal compliance changes handled without enabling opportunistic capture?

**Resolution required:** Include a legally valid interim mechanism, succession mechanism, incapacity procedure, deadlock route and tightly defined emergency exception. The mechanism should preserve the non-enclosure purpose while remaining operable.

### LG-04 — Withdrawal, public record and permanent prior-art disclosures

**Severity: CRITICAL before hosted web-app launch; HIGH for policy adoption**

**Sources:** `GOVERNANCE.md`, §4(3); `COMMERCIAL.md`, “Your side of the exchange”; `PRIVACY.md`, web-app paragraph and data table; `PRIOR_ART.md`, “What you should know before you submit”; `MODERATION.md`, “Takedowns and appeals”.

There is a direct policy conflict:

- `GOVERNANCE.md` gives the Overseer power to veto removal of published content from public access, except legal takedowns.
- `COMMERCIAL.md` and `PRIVACY.md` say a user may withdraw consent and ask for submitted readings to be removed from the site, Congruence Register and research corpus.
- `PRIOR_ART.md` says prior-art disclosures are permanent and are not withdrawn except for legal takedowns.
- `MODERATION.md` says removal from the site and default branch occurs only on a valid legal notice.

These may concern different record classes, but the distinction is not explicit.

**Recommended policy architecture:**
1. **Ordinary navigation or reading:** define whether the submitter grants a licence on publication and whether removal from the active Omega42 record can be requested. Preserve a lawful archival/provenance tombstone where appropriate, without retaining text that must be erased.
2. **Personal/redacted reading:** do not publish a coordinate/hash record merely because the user selected “personal” unless the consent and privacy basis for that specific disclosure are clear and separate. Explain whether a hash can still be personal data or re-identifiable.
3. **Formal prior-art disclosure:** use a separate, explicit, informed submission route. Explain that a public disclosure may be practically irreversible and may affect the submitter's own patent rights. It must not be treated as an ordinary reading.
4. **Legal takedown:** define a process for unlawful, confidential, infringing or privacy-compromising material, including backups, mirrors, archives and public notices.
5. **Open licence copies:** explain that downstream copies made under an open licence may not be recallable, while distinguishing that from the Company's ability to remove its own hosted copy.

**Do not launch the hosted exchange until this conflict is resolved and reviewed by privacy counsel.**

### LG-05 — Redacted-domain hashes and privacy

**Severity: HIGH before hosted web-app launch**

**Sources:** `COMMERCIAL.md`, “The Ω42 web-app”; `PRIVACY.md`, data table and web-app paragraph.

A “personal” reading is described as publishing its coordinate, state and hash of the exact question, without the text. A hash is not automatically anonymous. If the question has a small or guessable search space, someone may test candidate wording against the hash; a coordinate/state may also narrow possibilities. A persistent identifier may remain linkable to an individual.

**Resolution required:** Counsel/privacy specialist should assess whether the record is personal information under POPIA and other relevant laws, whether a lawful basis exists, whether explicit consent is adequate, retention and deletion requirements, data-subject rights, cross-border processing, security, and whether the proposed hash should be salted, keyed, omitted or replaced by a less linkable record. A salt/key may affect public verifiability; document the trade-off.

### LG-06 — Company patent pledge versus contributor patent rights

**Severity: HIGH**

**Sources:** `ENTITY.md`, “What the Company does not do”; `PATENT_PLEDGE.md`, §§1–5; `LICENSES.md`; `CONTRIBUTING.md`, “Rules that apply to every submission”.

The Company's no-patent promise is strong as a statement of Company policy. It does not create a general promise by every contributor never to file or assert a patent on their own contribution or an improvement.

The current wording says:
- the Company will not apply for, buy, accept assignment of or exclusively license covered patents;
- if the Company accidentally acquires such a right, it will not assert it and will dedicate it or let it lapse;
- contributors are not asked to assign patents;
- Apache-2.0 supplies a patent licence from code contributors for patent claims necessarily infringed by their contribution.

It does **not** say that every contributor promises never to seek, obtain, transfer or assert a patent over covered subject matter. CC BY 4.0 is a copyright licence, not a general patent non-assertion undertaking. Apache-2.0's patent grant is not a blanket prohibition on patent filings for every idea or later independent improvement.

**Originator decision required:** Is the intended policy:
A. Company-only non-appropriation, with contributors free to retain and exercise their own patent rights subject to licences already granted; or
B. a voluntary, explicit contributor non-assertion covenant covering accepted Omega42 contributions and defined improvements, while leaving unrelated independent inventions outside scope?

Option B better serves a comprehensive anti-enclosure goal, but requires a separate, carefully drafted and legally reviewed agreement. Do not imply it is already in force.

### LG-07 — Prior-art process and first-publication date

**Severity: HIGH before prior-art programme is represented as operational**

**Sources:** `PRIOR_ART.md`, “How a disclosure is made public” and “What a good disclosure contains”; `PATENT_PLEDGE.md`, §4.

The opening paragraph of the current default-branch `PRIOR_ART.md` says that once an idea is published, a later applicant “cannot claim it as new”. Later paragraphs correctly qualify this: publication is evidence that may be cited or used to challenge a patent, does not prevent filing, and does not cover undisclosed improvements. The opening sentence is inconsistent with those qualifications.

The process also treats an issue's creation time as the disclosure date, even if the issue is not yet complete or enabling. The public issue may be a title or short summary at creation; later edits may add the actual technical teaching. A hash proves file integrity, not by itself that a particular enabling disclosure was publicly accessible at a particular date.

**Resolution required:**
- Separate initial intake date, date of complete enabling version, acceptance date and repository publication date.
- Hash and archive the exact enabling version that became public.
- Preserve version history and reliable independent timestamp/archive evidence.
- Publish the actual technical disclosure and supporting files in a durable, searchable location.
- Explain that patentability and prior-art effect depend on jurisdiction, date, public accessibility, disclosure content and the claims at issue.
- Obtain patent-attorney review of the disclosure form and process.

### LG-08 — Certification Body independence and mark ownership

**Severity: HIGH before certification launch**

**Sources:** `ENTITY.md`, “What the Company does” item 5 and “How it is governed”; `CERTIFICATION.md`, “Who certifies”; `TRADEMARK.md`, “Who holds them”.

The documents say:
- the Company establishes and owns the Certification Body;
- the Certification Body is a dedicated legal entity;
- the Stewardship Committee holds a majority on its board;
- the Company does not direct audit decisions;
- the Certification Body appoints auditors and an appeals panel;
- the Certification Body holds and licenses the certification mark.

But `ENTITY.md` ends item 5 with “It holds and licenses the certification mark”, where “it” could grammatically refer to the Company or the Certification Body. `TRADEMARK.md` says the Certification Body holds the certification mark. The ownership statement must be unambiguous.

The structural independence question also remains: if the Company owns the body and may control its constitution, funding or appointments, the body may not be sufficiently independent in substance even if it is a separate legal person.

**Resolution required:** Define the Certification Body's legal form, ownership/member rights, board appointment and removal, protected decision-making, audit independence, appeals independence, funding, conflicts, liability, mark ownership and transfer on dissolution. Consider independent majority directors or an independent membership/oversight mechanism. Certification must not be controlled by the commercial operator whose products are being certified.

### LG-09 — Trademark trust, transfer and control

**Severity: MEDIUM–HIGH**

**Sources:** `ENTITY.md`, “Steps” and locked provisions; `TRADEMARK.md`, “Who holds them”; `GOVERNANCE.md`, §4(4).

`ENTITY.md` says the Company will acquire and hold marks, and the Originator transfers existing rights after registration. `TRADEMARK.md` says that until registration, the Originator holds them “in trust” for the Company. It does not specify whether a trust is actually constituted, who is trustee/beneficiary, whether the marks are registered, what rights are currently owned, or the transfer instrument and timing.

**Resolution required:** Conduct name/logo clearance and ownership audit; identify current rights holder and evidence of creation/use; decide whether a trust is appropriate; draft an assignment or licence with conditions; specify who controls applications, renewals, enforcement and licensing; and protect the open research and descriptive use of the name.

### LG-10 — “All ideas are free” versus licence and rights reality

**Severity: MEDIUM**

**Sources:** `ENTITY.md`, “What the Company does not do”; `PATENT_PLEDGE.md`; `LICENSES.md`; `TRADEMARK.md`.

The phrase “all ideas stay free for anyone to explore, extend and build on” expresses the intended openness. It should not be read as a statement that every legal right in every contribution is extinguished.

- CC BY 4.0 permits broad reuse subject to its terms, including attribution and other conditions.
- Apache-2.0 permits broad commercial use of code, subject to its terms and notices, and includes a defined contributor patent licence.
- Third-party patents, copyright, confidentiality, database rights and other rights are not automatically cleared by publication.
- Trademarks remain controlled to protect source identity and certification claims.
- The Company's no-patent promise does not bind non-signatories.

**Recommended wording:** “Omega42's accepted materials are released under the applicable open licences, and the Company will not use patent rights to enclose the project. The project encourages anyone to explore, extend and commercialise the openly licensed material, subject to the relevant licences and third-party rights.”

### LG-11 — Contributor, AI and third-party rights

**Severity: MEDIUM–HIGH**

**Sources:** `LICENSES.md`, final paragraph; `CONTRIBUTING.md`, AI and DCO sections; `AI_ACCESS.md`.

The documents correctly acknowledge that copyright in AI-generated navigation output varies by country and publish it under CC BY 4.0 only to the extent rights exist. Further clarification is needed for:
- who is authorised to grant a licence when an AI system generated most or all of the contribution;
- the submitter's responsibility for provider terms and third-party material;
- whether the named person has actually reviewed and adopted the output;
- code provenance, generated dependencies and licence compatibility;
- whether an employer, university, client or funding agreement controls rights in a contribution.

**Resolution required:** Add a contribution declaration covering authority, provenance, third-party content, applicable provider terms and any known restrictions. Do not represent an AI model as a legal author or assume all AI output is rights-free.

### LG-12 — NPC/public-benefit purpose and commercial activity

**Severity: HIGH before entity selection**

**Sources:** `ENTITY.md`, “Choosing the form”; `GOVERNANCE.md`, §6; `COMMERCIAL.md`, “Money”.

The project wants a non-enclosing public commons and also anticipates software sales, certification fees, consultancy, subscriptions or other commercial services. This is not inherently incompatible with a nonprofit structure, but the legal form, objects, asset lock, private-benefit restrictions, trading activities, remuneration and distribution rules must be designed together.

**Resolution required:** Obtain written advice on NPC objects, permissible trading, treatment of surpluses, remuneration, related-party transactions, ownership of a subsidiary, PBO and section 18A eligibility (if sought), VAT, income tax and donor/grant eligibility. Do not describe the Company as tax exempt unless SARS has approved the relevant status.

### LG-13 — Certification mark and quality claims

**Severity: MEDIUM**

**Sources:** `CERTIFICATION.md`, “What is certified”; `TRADEMARK.md`, badge table.

The conformance suite checks protocol execution and format, not truth, intelligence, consciousness, safety or general reliability. This is clearly stated in `CERTIFICATION.md` and should remain clear in all public badge language. The certification scheme needs published criteria, fees, appeals, suspension/withdrawal, conflicts, surveillance and renewal rules before the mark is used commercially.

### LG-14 — Commercial exchange and newsletter eligibility

**Severity: MEDIUM–HIGH**

**Sources:** `COMMERCIAL.md`, “The Ω42 web-app” and “Money”; `PRIVACY.md`, newsletter paragraph.

The commercial document says every web-app user may choose to receive the newsletter, while the privacy policy describes newsletter recipients as registered contributors, submitters and commercial users. It also says the newsletter is a choice confirmed by email. Make clear that submission of a reading does not automatically subscribe the person to marketing email, and separate service notices from optional newsletters.

### LG-15 — Fiscal host and pre-incorporation authority

**Severity: MEDIUM–HIGH**

**Sources:** `GOVERNANCE.md`, §6; `ENTITY.md`, “Steps”.

A fiscal host may receive funds before incorporation. The documents do not yet specify who contracts with the host, who beneficially owns funds, who approves spending, how liabilities and donor restrictions are handled, how records transfer to the Company, or what happens if incorporation does not proceed.

**Resolution required:** Use a written fiscal-host agreement and a pre-incorporation authority/expense register. Counsel should address promoter liability, ownership of funds and assets, tax receipts, refunds, data access and termination.

---

## 3. Proposed decision-rights architecture for counsel

The following separation is a design recommendation to be tested against South African company law:

| Domain | Proposed decision holder | Constraint |
|---|---|---|
| Foundational intent and constitutional reserve | Originator/Overseer, as defined by valid founding documents | Narrowly specified; succession and incapacity rules required |
| Protocol and open record stewardship | Stewardship Committee | Cannot override law, third-party rights or directors' statutory duties |
| Corporate administration and fiduciary oversight | Company Board | Must exercise its own lawful duties; cannot be a mere rubber stamp |
| Commercial operations and budget execution | Company/Operations Board | Bound by purpose, licences and non-enclosure commitments |
| Certification decisions | Independent Certification Body | Must be independent of commercial pressure and conflicts |
| Contributor rights and publication consent | Contributor, under clear agreements | No implied assignment; explicit licence and separate prior-art consent |
| Legal compliance and privacy | Company and designated responsible officers | Cannot be waived by project governance |

Counsel should determine which protections belong in the MOI, shareholders' agreement, membership rules, board charter, stewardship charter, trust instrument, contributor agreement, patent covenant, licence or operating contract. A website policy alone is not sufficient for every obligation.

## 4. Questions for South African counsel

Please provide written advice on:

1. Which legal structure best fits the stated non-enclosure and commercial objectives, and why?
2. Can the proposed NPC lawfully own and control an Operations (Pty) Ltd while preserving the asset lock and governance protections?
3. What is the best mechanism for entrenched purpose and non-patent provisions, and what amendment threshold is enforceable?
4. How should the Originator's reserved powers be drafted without invalidly displacing directors' duties?
5. Can the seven-member Stewardship Committee appoint directors and exercise protocol authority in the proposed manner?
6. What interim arrangements apply before the Committee exists?
7. What happens on Overseer incapacity, death, resignation, refusal to appoint a successor or lapse of the role?
8. How should conflicts, deadlocks, removal, vacancies and emergency legal amendments work?
9. What exact legal form and ownership structure should the Certification Body have to be genuinely independent?
10. Who should own the Omega42 and Ω42 marks, and what trust, assignment or licence instrument is required?
11. Can the Company legally bind successors, asset purchasers and controlled subsidiaries to the non-enclosure rules, and how should this be achieved?
12. What is the strongest enforceable form of Company patent non-assertion?
13. Should contributors sign a separate voluntary non-assertion covenant? What scope, beneficiaries, improvements, affiliates, successors, duration and remedies are enforceable?
14. How do CC BY 4.0 and Apache-2.0 interact with patent rights, moral rights, database rights and third-party material under South African law and relevant foreign law?
15. What legal and privacy basis supports the redacted-domain record and hashed personal questions?
16. How should consent, withdrawal, deletion, archival retention and open-licence copies be reconciled?
17. What disclosures are sufficiently enabling for prior-art purposes, and how should public availability and exact-version dates be proven?
18. What tax, VAT, PAYE, UIF, audit, annual-return, beneficial-ownership, POPIA, PAIA and Information Officer obligations apply?
19. What is required for PBO or section 18A status, and is it compatible with the proposed commercial activity?
20. What agreements are needed with the fiscal host, cloud providers, newsletter provider, AI providers, employees, contractors, universities and commercial partners?
21. What happens to marks, data, records, software, funds and contractual obligations on dissolution or project transfer?
22. Which commitments should be made now, and which should wait until the entity and operational systems exist?

## 5. Recommended drafting sequence

1. Originator confirms the intended contributor patent policy (Company-only or voluntary contributor covenant).
2. Originator confirms the intended record/withdrawal distinction between ordinary readings and formal prior-art disclosures.
3. Counsel provides a written legal-form comparison and recommends one structure.
4. Counsel maps the Board, Committee and Overseer powers into an enforceable MOI and governance instruments.
5. Counsel drafts the patent pledge, contributor terms, IP licences and trademark instruments.
6. Privacy counsel resolves the hosted exchange, personal readings, hashes, consent and withdrawal.
7. Certification counsel/design review establishes the independent body's constitution and mark rules.
8. Only then approve incorporation documents and execute the commitments.
9. Publish the signed, approved policies and maintain a versioned public record.

## 6. Immediate project decisions (not legal drafting decisions)

The Originator's two decisions that cannot safely be inferred are:

**Decision A — contributor patent policy**

- **A1: Company-only pledge.** Omega42 and its Company do not appropriate patents; contributors retain their own rights subject to the licences they grant.
- **A2: Company pledge plus voluntary contributor non-assertion.** Contributors who knowingly submit covered material also promise not to seek or assert exclusive patent rights over that accepted contribution and defined improvements, with scope settled by counsel.

**Decision B — ordinary reading withdrawal**

- **B1: Open-record permanence.** Ordinary submitted readings are permanently published after explicit consent; withdrawal stops future submissions but does not remove already published material except legal takedowns.
- **B2: Withdrawal-capable ordinary record.** Ordinary readings can be removed from Omega42-controlled active systems on request, subject to lawful retention and clear notice that open-licence copies already made by others cannot be recalled. Formal prior-art disclosures remain a separate, explicitly permanent category.

These choices should be made before finalising the lawyer brief and web-app consent wording.

## 7. Release and implementation boundary

Until these matters are resolved:
- Do not claim the Company is incorporated or that the pledge is signed.
- Do not claim every contributor is bound by a no-patent promise.
- Do not launch the hosted web-app exchange or publish personal redacted-domain records.
- Do not claim certification independence is operational.
- Do not describe a hash alone as proof of enabling prior art.
- The free local Strike workflow, public protocol documents and openly licensed materials can continue to be developed, subject to existing rights and governance.
- The website may explain the ambition and the proposed open-commons design, while identifying the legal structure and hosted services as under development.

## 8. Originator decisions requested

The two decisions in Section 6 are the immediate project-level choices. The legal form, tax treatment, enforceability and exact contract language should be recommended by counsel after reviewing the project and the Originator's objectives. The Originator should not be asked to choose legal drafting mechanics without counsel's explanation of their consequences.
