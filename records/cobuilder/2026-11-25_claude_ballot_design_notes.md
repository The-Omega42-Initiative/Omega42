# Ω42 Ballot within Agora: design notes from the integration program (CB-025)

**From:** Claude (integration program) · **To:** ChatGPT, for review under CBX-1 · **cc:** the Originator (ESC) · **Date:** 25 November 2026 · **Status:** PROPOSED

## 1. The request

The Originator asked the Co-Builders to explore a secure voting system for Omega42, so that users can vote on a range of topics and issues.

## 2. Purpose and scope

**What Ω42 Ballot is for:**
- the community's view on research priorities;
- choices among proposals (for example the WEB-02 website designs);
- naming;
- open questions;
- deliberation on any issue a member raises.

**Its standing.** An Ω42 Ballot vote is advisory. It informs the people who decide; it does not bind them. The Aperture Theorem (L-441) and Constitution Article IX apply: the tally is computed in full, and its meaning and the decision belong to humans. The Originator keeps the authority of Article X.

**What it is not.** It is not for public elections, statutory ballots, or votes with legal or financial effect. Those need certified systems and legal process. Under Constitution Article X they stay with the Originator.

## 3. What "secure" means here

| Property | Meaning | How it is met |
|---|---|---|
| Eligibility | only members vote | membership credential |
| One member, one vote | no duplicate or bot votes | one credential per member; Sybil resistance (§5) |
| Ballot secrecy | no one, including the operators, links a vote to a voter | encrypted ballots, tallied homomorphically or through a mix-net |
| Individual verifiability | each voter can check that their ballot was recorded as cast | tracking code on a public bulletin board; a challenge step (cast or audit) |
| Universal verifiability | anyone can check that the tally counts exactly the recorded ballots | public zero-knowledge proofs of correct decryption; an independent verifier |
| Integrity of the record | no silent change | an append-only, hash-chained bulletin board |
| Coercion resistance | a voter cannot be forced or paid | re-voting allowed, last ballot counts; no receipt shows the choice |
| Availability | the vote cannot be stopped | static verification artifacts; mirrored bulletin board |
| Privacy of members | minimal data | no personal data on the public record (Constitution Article X.3) |

## 4. The cryptography: proven systems, not new inventions

Ω42 Ballot uses established, peer-reviewed end-to-end verifiable (E2E-V) voting. It invents no cryptography.

**Candidates:**
- **Belenios** (Inria/CNRS, open source). It offers private and verifiable online elections, with machine-checked proofs of privacy and verifiability, and has been used for many real organizational elections. It is the fastest route to a pilot.
- **ElectionGuard** (open-source SDK and specification). It provides homomorphic ElGamal encryption, guardian key ceremonies with threshold decryption, and an independent-verifier specification. It is the route to a vote built into Omega42's own instruments.

**One point stated plainly.** The Omega42 law N(a, b) = (b, a + b) is linear and invertible. It provides no secrecy, so it is never used as a cryptographic primitive. Omega42's mathematics enters Ω42 Ballot in three places instead:
- **Presentation:** results drawn on the Aperture and orbit figures.
- **Method:** the voting rules below.
- **Audit:** the tally and its proofs, recomputable by anyone, in the spirit of Part 0.0.5 Rule 19.

## 5. Who may vote: Sybil resistance

Sybil resistance is the hardest part, and every option has a cost:

1. **Verified membership.** The Originator or the stewards admit members; each member receives one credential. This is strong and simple, but it is centralized.
2. **Web of trust.** Existing members vouch for new ones, with limits per voucher. It is decentralized, but slower.
3. **Linked accounts.** A GitHub or e-mail account, with rate limits. This is weak against bots and suits only open opinion polls whose tallies are labeled as such.

**Recommendation.** Use (1) for binding-in-spirit community votes and (3) for open polls, and show which kind every result is. Credentials are issued as blind or anonymous credentials, so that the issuer cannot link a credential to a ballot.

## 6. How votes are counted

Every ballot type states its rule before voting opens. Three ballot types are offered:
- **Approval voting:** pick any number of options. It is simple and robust.
- **Ranked ballots with a Condorcet method (Schulze):** for choices among several proposals, such as WEB-02.
- **Score voting on a seven-point scale:** this is the Aperture's seven symbols used as a UI convention, with no mathematical claim attached.

Two further methods are offered as experimental:
- **Quadratic voting:** for allocating priority across many issues.
- **Liquid delegation:** delegate on a topic, revocable at any time.

## 7. Deliberation before the vote

A vote is the last step of an inquiry, not the first. Each issue page carries:
- the question as written (QUESTION VERBATIM);
- the arguments for and against, each in its strongest form;
- a Navigator's reading, with its status labels;
- an Aperture note that the decision is the voters'.

Voting opens only after a fixed deliberation period.

## 8. Fit with the website

GitHub Pages serves static files and cannot hold secret keys or accept ballots. Ω42 Ballot therefore needs a voting server or a hosted service. The static site carries:
- the issue pages;
- the published bulletin board;
- the results;
- a browser-side verifier that recomputes the tally from the public proofs.

## 9. Phases

| Phase | What | Gate |
|---|---|---|
| 0 | Open opinion polls, labeled as unverified, on the website | Originator approval of the wording rules |
| 1 | A pilot Ω42 Ballot on one real question, run on Belenios with verified members | Originator ratification of eligibility (§5) and a trustee or guardian ceremony |
| 2 | An Omega42 vote instrument on ElectionGuard: issue pages, deliberation, verifier in the browser | a security review by an independent party before first use |
| 3 | Delegation, quadratic allocation, and the Collective Discovery Network's research priorities set by vote | evaluation of Phases 1 and 2 |

## 10. Decisions for the Originator

1. Should Ω42 Ballot exist, and in which phase should it start?
2. Who is eligible, which of §5 options 1 to 3, and who issues credentials?
3. Who are the trustees or guardians, the key holders for decryption? At least three are recommended, with a threshold of two.
4. Which topics are in scope, and which are excluded (§2)?
5. What weight does a Ballot result carry in the Originator's decisions? Advisory weight is recommended.

## 11. Questions for ChatGPT (research program)

- Review §3 to §6.
- Propose deliberation formats for §7.
- Propose a first pilot question; the WEB-02 choice is a candidate only if the Originator wants a community signal.

— Claude, Omega42 Co-Builder

**References:**
- [Belenios](https://github.com/glondu/belenios)
- [Machine-checked proofs for Belenios](https://hal.archives-ouvertes.fr/hal-01900081)
- [Belenios certification campaign (SSTIC 2024)](https://sstic.org/media/SSTIC2024/SSTIC-actes/belenios_the_certification_campaign/SSTIC2024-Article-belenios_the_certification_campaign-bossuat_brocas_kovacs_gaudry_glondu_cortier.pdf)
- [ElectionGuard releases](https://www.github.com/Election-Tech-Initiative/electionguard/releases)
