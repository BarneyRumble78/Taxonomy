# Taxonomy: promotion and marketing plan

Owner: Chris Townsend. Version 1, 9 October 2026. Companion files: `marketing/emails/`, `marketing/content/`, `marketing/TARGETS.md`.

## 1. The one-line position
**Taxonomy is the first standard that classifies knowledge claim by claim, with the evidence each claim needs, starting from mathematics.** For AI builders, analysts and researchers who must know what a statement is and what would make it true.

Unique selling proposition (Reeves test: specific, unique, strong enough to switch):
- Subject schemes (MSC, Dewey, ANZSRC, MeSH) file documents by topic. Taxonomy files sentences by owner and warrant.
- One ownership rule and 984 stable IDs join 25 fields into one registry.
- It runs: a Python engine, a live website tool, and an API under construction.

## 2. What must be true before the big push
Credibility with mathematicians and universities is lost once and rarely regained. Three things should exist before cold outreach to senior academics:
1. **A public repository and a public website.** Make `BarneyRumble78/Taxonomy` public with a licence (CC BY 4.0 for the standard, MIT for code). Put the site on its own domain.
2. **A short paper.** 8–12 pages: the standard, the mathematics framework (63/63 MSC classes), the warrant list, the pilot method and an honest results section. Post to arXiv (cs.DL primary, math.HO cross-list) or SSRN. A link to a paper is what a busy academic will open.
3. **A working API demo.** `/classify` and `/whole_view` live, with a free key. Claude Code can build this from `engine/` (see BACKLOG).

The human placement study (three human coders) can follow, but say plainly in every academic email that it is planned, not done.

## 3. Audiences, in priority order

| # | Audience | What they want | What we offer | Channel |
|---|---|---|---|---|
| 1 | AI and RAG developers | Better retrieval, fewer hallucinations, agent routing | API, MCP server, warrant-aware RAG pattern | GitHub, Hacker News, X, Discord communities, dev newsletters |
| 2 | Policy and intelligence analysts | Briefs that separate evidence from judgement | Whole-view briefs, policy template | LinkedIn, Substack, RealClearDefense-style outlets, think tanks |
| 3 | Cyber security teams | Separate indicators from attribution; RAG-poisoning defence | STIX warrant mapping, rogue-AI signals | Security conferences (CFPs), r/netsec, Kiwicon-style local events |
| 4 | Mathematicians and knowledge-organisation scholars | Rigour, correct MSC use, novelty | The mathematics framework and the paper | zbMATH Open, AMS, ISKO, Lean/Zulip, direct email |
| 5 | Universities and research offices | Research mapping, teaching epistemic literacy | ANZSRC crosswalk, curriculum module | Research offices, library services, teaching-and-learning centres |
| 6 | Māori and Indigenous researchers | Respect, control, benefit | Invitation to lead the review, with payment | Through proper channels only (see section 8) |

## 4. Phased plan (13 weeks)

### Phase 1 (weeks 1–3): foundations
- Make the repo public; add LICENSE, CITATION.cff, Zenodo DOI.
- Buy a domain; deploy the site and API (Claude Code task).
- Write and post the paper.
- Record the 60-second and 3-minute videos (scripts in `content/VIDEO_SCRIPTS.md`).
- Set up a mailing list with double opt-in (Buttondown, Substack or Mailchimp).
- Prepare a one-page PDF brief for each audience.

### Phase 2 (weeks 4–6): soft launch to warm contacts
- Email 20–40 people who already know you: Substack readers, contacts from the Syracuse programme, editors you send pieces to, AI-policy contacts. Ask for honest criticism, not praise. Use `emails/05_warm_contact.md`.
- Publish the Substack launch essay (`content/LAUNCH_ESSAY.md`).
- Fix what they find. Collect any quotes they offer *in writing, with permission*.

### Phase 3 (weeks 7–9): public launch
- Show HN post on a Tuesday or Wednesday morning US Eastern (`content/SOCIAL.md`).
- LinkedIn and X threads; YouTube video on both of your channels; Spotify podcast episode.
- Press release to NZ tech and science media (`content/PRESS_RELEASE.md`).
- Developer posts: a worked "warrant-aware RAG in 50 lines" notebook.

### Phase 4 (weeks 10–13): academic and institutional outreach
- Individual emails to mathematicians and KO scholars (`emails/01_mathematician.md`), five a week, each personalised.
- University research offices and libraries (`emails/02_university.md`).
- Government policy units and think tanks (`emails/03_policy.md`).
- Security CFP submissions: a talk on "warrant mismatch as a hallucination and poisoning signal".
- Invitation to the Māori-led review (`emails/06_maori_review_invitation.md`), through institutions.

## 5. Content calendar (repeatable weekly rhythm)

| Day | Output |
|---|---|
| Monday | One Substack post: a "whole view" of a news topic through all 25 fields |
| Wednesday | One short video (60–90 s): one field, one warrant, or one use case |
| Thursday | One developer post or notebook |
| Friday | Five personalised outreach emails; log replies in `TARGETS.md` |

Series ideas that reuse the engine:
- **"25 Views"**: each week, run a topical subject (AI sunglasses, a budget, a court ruling) through Whole View and publish the result.
- **"Who owns this sentence?"**: viral-format quiz posts using the 50 pilot claims.
- **"Warrant check"**: take a viral AI answer and tag every claim with its warrant.

## 6. Video and explainer set
See `content/VIDEO_SCRIPTS.md`:
- 60-second teaser
- 3-minute explainer
- 10-minute talk: "Mathematics first: a standard for knowing in the age of AI"
- 5-minute developer demo: classify, whole view, API call

Production: narrate with your cloned voice, using screen recordings of the site and engine. Keep diagrams to the pyramid and the ownership table.

## 7. Measures of success (week 13 targets, adjust after week 6)

| Measure | Target |
|---|---|
| Mailing-list sign-ups | 500 |
| GitHub stars | 300 |
| API keys issued | 100 |
| Substantive replies from academics | 10 |
| Pilot partners (an organisation using it on real work) | 3 |
| Reviewers recruited for fields | 10 |
| Māori-led review panel convened or formally declined | 1 decision |

Track weekly in `TARGETS.md`.

## 8. Rules for the campaign
- **No fake accounts, bought followers, bot amplification or undisclosed paid posts.** They break platform rules and NZ advertising law. If academics or journalists find them, they end the project's credibility.
- **No invented endorsements.** Quote people only with written permission.
- **Email law.** New Zealand's Unsolicited Electronic Messages Act 2007 requires consent for commercial electronic messages. Consent can be inferred where an address is conspicuously published and the message relates to the person's role (UNVERIFIED in detail: check the Department of Internal Affairs guidance). Every message must identify you and offer an unsubscribe. Academic one-to-one emails asking for comment are lower risk than marketing blasts. Never buy lists.
- **Senior academics such as Terence Tao.** Tao receives very large volumes of unsolicited mail and is unlikely to reply. If you write, send one short, specific note with the paper link and the mathematics framework. Ask one answerable question, and do not follow up more than once. Better routes to mathematicians:
  - zbMATH Open (who co-maintain MSC2020)
  - the AMS (Mathematical Reviews)
  - the Lean community on Zulip
  - an arXiv paper they can find themselves
- **Māori and Indigenous engagement.** Approach through institutions (a university Māori research unit, Te Mana Raraunga) with payment and data control agreed first. Never use Māori content in promotion before the review.
- **Claims.** State the pilot as a pilot. State the API as "in beta" until it is. Mark unverified facts.

## 9. Budget (lean)

| Item | Cost (approx., NZD) |
|---|---|
| Domain and hosting | 50–300 / year |
| Mailing list tool | 0–50 / month |
| API hosting (small) | 20–100 / month |
| Video tools | existing |
| Reviewer and Māori panel payments | budget first, amount set with reviewers |
| Optional: conference travel | as available |

## 10. Risks

| Risk | Mitigation |
|---|---|
| Academics dismiss it as over-ambitious | Lead with the narrow, checkable mathematics result and the paper |
| "AI-generated" perception | Show your own voice, reasoning and decisions; be open that Claude helped build it |
| Classifier errors in public demos | Show confidence and alternatives; offer deep analysis; keep a known-issues list |
| Indigenous misrepresentation | Review gate before any promotion of IK content |
| Overpromising security benefits | Present as hypotheses with a red-team plan |

## 11. Tasks for Claude Code
1. Build the API: FastAPI service exposing `/classify`, `/whole_view`, `/relate`, `/lookup/{id}`, with API keys, rate limits and an OpenAPI page.
2. Build an MCP server exposing the same three tools.
3. Add LICENSE, CITATION.cff and a Zenodo release workflow.
4. Export the registry as SKOS/JSON-LD.
5. Produce a Jupyter notebook: "Warrant-aware RAG in 50 lines".
6. Generate the "25 Views" weekly post from `engine --view` plus model analysis.
