# Omega42 Co-Builder Collaboration Protocol

**Status:** Working proposal for Originator review; not yet a constitutional or governance amendment.

## 1. Collaboration model

Omega42 development may use a three-party working arrangement:

- **Originator:** establishes foundational intent, sets priorities, resolves strategic questions and retains final human authority.
- **Navigator / Integrator (ChatGPT in the current workflow):** maintains project continuity, coordinates tasks, inspects the repository, integrates work, implements approved changes and reports status.
- **Independent Co-Builder (Claude Opus 5.5, when actually available to the Originator):** provides independent design, mathematical, philosophical, architectural and editorial analysis; proposes alternatives; challenges assumptions; and reviews work independently.

This is a project workflow, not a claim that an external model has been connected or has performed work. A model is considered to have participated in a task only when its output has actually been received and recorded.

## 2. Authority and decision rights

1. The Originator retains final authority over Omega42's foundational intent, priorities, interpretation and approval of material changes.
2. AI systems are instruments and contributors. Neither AI system can appoint itself as project authority, alter its mandate, approve its own work or merge its own pull request.
3. The Co-Builder's review is independent input, not a veto. The Integrator must not suppress a Co-Builder disagreement merely because it conflicts with an earlier assistant conclusion.
4. The Integrator's synthesis is also not automatically authoritative. Where material disagreement remains, present the alternatives and their consequences to the Originator.
5. Repository governance, branch protection, CI, legal requirements and the project's canonical Core remain applicable.

## 3. Work allocation

- **Exploration:** Co-Builder and Integrator may independently generate models, mathematical routes, architectures and interpretations.
- **Formal analysis:** each may derive or recompute results independently. Proofs and computations should be reproducible and assumptions explicit.
- **Critique:** the Co-Builder should be encouraged to challenge the Integrator's reasoning, and vice versa.
- **Integration:** the Integrator reconciles contributions, checks compatibility with canonical documents and prepares proposed repository changes.
- **Decision:** the Originator chooses between materially different directions and approves consequential changes.

Parallel independent analysis is preferred for foundational mathematics, legal architecture, epistemological governance and major website positioning.

## 4. Epistemic and status integrity

Use distinctions appropriate to the work: STIPULATED, DEFINED, FORMALLY DERIVED, PROVED, COMPUTED, RECONSTRUCTED, CONJECTURED, INTERPRETIVE, ANALOGICAL, CORRESPONDENCE, EMPIRICALLY OBSERVED, DISPUTED, OPEN and PROVISIONAL.

Do not demote a valid internal mathematical result because it lacks empirical correspondence. Do not upgrade a conjecture, analogy or interpretation into a theorem or physical fact without support. Bold exploration is encouraged; status clarity must not become a mechanism for suppressing it.

The Scientific Appendix is the designated home for detailed scientific methodology and epistemic qualifications. Public-facing material should lead with Omega42's purpose, ambition, capabilities and possibilities, while remaining accurate about what is implemented.

## 5. Provenance for AI-assisted contributions

For each substantive Co-Builder contribution, record:
- model/provider and exact model identifier as reported by the provider;
- date received;
- task or question;
- source materials and repository commit/PR reviewed;
- full response or an archived reference to it;
- whether the content is analysis, code, mathematical derivation, review or editorial proposal;
- independent checks performed;
- accepted, modified, deferred or rejected disposition and reason.

Do not invent model identifiers, claim an AI review occurred when it did not, or describe an output as independently verified merely because another model produced it.

## 6. GitHub workflow

1. Work on feature branches, not protected branches.
2. Keep unrelated work in separate pull requests.
3. AI systems may prepare issues, branches, commits and pull requests only where connected tools and permissions actually allow it.
4. No AI approves or merges its own proposal.
5. Require CI and the repository's normal review requirements.
6. Material changes to the Core, constitutional provisions, legal commitments, patent policy or ownership arrangements require explicit Originator approval and any governance approvals specified by canonical documents.
7. Keep PRs draft until relevant review is complete.
8. Never bypass release gates or weaken tests merely to make a change pass.

## 7. Disagreement protocol

When builders disagree:
1. State the exact proposition on which they differ.
2. Separate factual, mathematical, interpretive, architectural and strategic disagreement.
3. Identify shared premises and differing assumptions.
4. Give the strongest case for each position.
5. Recompute or source-check where possible.
6. Identify what remains unresolved.
7. Present a recommendation, but preserve alternatives for the Originator.

Do not manufacture consensus. Productive disagreement can reveal a new line of inquiry.

## 8. Confidentiality and rights

Only provide the Co-Builder with material the Originator is entitled to share. Do not submit third-party confidential information, personal data or unpublished material subject to employment, university, client or contractual restrictions without authority.

Before accepting external AI-generated code, designs or text into the public repository, check applicable provider terms, third-party rights, licence compatibility and provenance. AI contribution does not automatically make material rights-free or patent-free.

## 9. First collaboration cycle

The initial Co-Builder task packet is CO_BUILDER_TASK_PACKET_CLAUDE_OPUS_5_5.md. It requests an independent review of the current website PR, canonical legal/governance architecture and immediate Public Foundation Release sequence. The packet is a request for review, not a claim that Claude has completed it.

## 10. Review and adoption

This protocol remains a working proposal until the Originator approves it. If adopted, align it with GOVERNANCE.md, ENTITY.md, CONTRIBUTING.md, AI_ACCESS.md and the Core's provisions for AI agents. It must not silently override those documents.
