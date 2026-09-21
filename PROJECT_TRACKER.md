# PROJECT_TRACKER.md

**This file is the single source of truth for resuming Mira development.**
If a session drops, the next one begins with: *"Read PROJECT_TRACKER.md and resume from
CURRENT DEVELOPMENT STATE."*

It is three things at once: a **development tracker**, a **decision log**, and an
**evidence ledger**. The evidence ledger matters as much as the task list — it records what
we *disproved*, so a dead claim cannot quietly return.

Last updated: **2026-09-21**

---

## 0. CURRENT DEVELOPMENT STATE

**Phase:** Day 1 — **core application validated under real HTTP execution. Deployment phase.**
**Current milestone:** GitHub → Vercel → **production validation.** *Then* source real records.

**Status:** Core application validated under real HTTP execution, locally. Not yet deployed.
Local success is **not** evidence that production works — that is a separate environment with
its own failure modes (runtime, bundling, static routing, cold start), and it is validated
separately below.

**Last completed:**
- Backend complete: `models.py`, `repository.py`, `routing.py`, `app.py`
- Data layer migrated to three-state provenance — 21 resources, 9 support processes,
  6 routes — **36 records, 2 locations**
- All 10 templates written and **rendered successfully**
- `static/css/styles.css` **built** — 29,969 bytes, and every component class verified
  present in the compiled output
- Deployment scaffolding created: `vercel.json`, `.vercelignore`, `.gitignore`,
  pinned `requirements.txt`, `README.md`
- **15 correctness fixes applied** (§8) — 7 original, 4 from the fix pass, 4 from the
  pre-execution sweep
- Harassment record carries **both** routes with the s.6 appeal restored (§4c)
- **FIRST EXECUTION COMPLETE.** See the verification record below.

**Verification record — what running actually proved (2026-09-21):**

| Check | Result |
|---|---|
| `import app` | OK |
| All 30 route checks (all categories, all Flow C topics, both locations, POST paths) | **200, no Jinja errors** |
| Data: 21 / 9 / 6 records, `data_warnings()` empty | ✓ |
| Provenance counts | 1 verified · 27 illustrative · 8 unverified |
| Three states render with **glyph + label + class** on `/about` | ✓ |
| Jurisdiction notice reads "Applies in Pakistan" on the harassment card | ✓ |
| Both harassment routes render; 3/7-day and 3/5-day defences **not** collapsed | ✓ |
| No "better" / "safer" / "faster" / "prefer the" in the routes | ✓ |
| `03:00` departure flags after-dark; unparseable time renders no chip | ✓ |
| Free shuttle shows "Free"; unknown-fare rickshaw shows **no fare** | ✓ |
| Share button ships `hidden`; no tracking link | ✓ |
| "Nothing you type is stored" absent from **all five** pages | ✓ |
| Demo banner on the fictional campus | ✓ |
| Router: 22/22 queries route correctly, including `"I feel unsafe"` → harassment | ✓ |
| `uvicorn` serves `/static/css/styles.css` — **200, `text/css`, 29,969 bytes** | ✓ |
| Stylesheet linked at exactly `/static/css/styles.css` (the path `vercel.json` routes) | ✓ |
| `POST /help` matched / no-match / urgent, over real HTTP | ✓ |
| Server access log: **no POST body, no problem text** | ✓ |
| After the D10 fix: `GET /help?problem=<canary>` does not echo | ✓ |

**Currently working on:**
- **The deployment chain.** GitHub → Vercel → production regression, in that order.

**Next exact action — this order is deliberate, do not reorder:**
1. `git init` + push to GitHub (Devpost requires source code)
2. Deploy to Vercel
3. **Full production regression test** — the whole checklist at §14b, against the public URL
4. Source the prioritised verified records (§14c) — only after production is proven
5. Phone-width polish → screenshots
6. Devpost description · technology list · demo video

**Why deployment precedes sourcing:** provenance cards are the most labour-intensive remaining
work, and there is no value in perfecting them if the deployed application then turns out to
have a production-only failure. Public access is a **hard submission requirement**; a richer
dataset is an improvement. Requirements outrank improvements, so the requirement is proven
first.

**Current blocker:** **Credentials only.** The user must configure a git identity, then run
`gh auth login` and `vercel login`. Nothing else is outstanding — tooling is installed, the
repo is initialised and staged, and `vercel.json` is rewritten. Live state is in §14a; the
exact commands are in §14d.

**P0:** Flow B (I need something) + Flow C (I need help)
**P1:** Flow A (Get me there) — already implemented; retain once production-proven.

**A note on what this session established:** the defects that mattered were found by *running*,
not by reading — and the worst one was **created by a fix applied to code that had never
executed** (§8 item 8). The pre-execution sweep was still worth doing (it caught a free
rickshaw, missing CSS classes and an unkept promise), but `GET /help?problem=` sat inside a
**LOCKED** decision through a full read of `app.py` and was caught in ten seconds of reading an
access log. **Treat every unexecuted change in this repo as a hypothesis until it has been
run** — which is why `vercel.json`, never executed either, is being replaced rather than
trusted (§14a, D25).

**Do NOT change without a new decision entry:**
- The three-state provenance model (`verified` / `illustrative` / `unverified`)
- `jurisdiction` as a field separate from `provenance`
- `provenance_state` as the *displayed* state, distinct from the declared one
- The "POST not GET" choice for Flow C problem text
- **There is no LLM in the deployed application** (D19) — the deterministic router is the
  whole implementation, not a fallback awaiting an upgrade
- The rule that no route carries a safety score or verdict
- The privacy wording (see §6) — it is deliberately narrower than it used to be
- Fares are omitted rather than guessed when confidence is `unknown`

---

## 1. Product definition

**Name:** Mira — Your Student Support Companion
**Tagline:** Find what you need. Know what to do. Get where you need to go.

**Target user:** A female student at a university or college, on a phone, often on a slow
connection, who needs something concrete and does not know where to start. Secondary:
any student with the same problem — nothing in Mira is women-only except the *content* of
specific records.

**Three core problems, and why they are real (see §4 for evidence):**

| Flow | Problem | Mira does |
|---|---|---|
| **I need something** | She needs a washroom, period products, water, food, first aid, a quiet place — and does not know which building, which floor, or whether it is open now | Answers with the place, the landmark, the hours, and whether it is open right now |
| **I need help with a problem** | Money, a harassment concern, a grade dispute, hostel, health. She does not know which office handles it, what to bring, or what happens in what order | Describes the process: who, what to bring, the steps in order, and the timeline — with sources |
| **Get me there** | She does not know what the trip costs, how long it takes, or whether women's transport runs when she travels | Shows the verifiable properties of the trip. Never a safety verdict |

**Scope:** 6 screens across 3 flows. Home + 2 screens per flow, plus About.

**Priority:** Flow B (I need something) P0 · Flow C (I need help) P0 · Flow A (Get me
there) P1 — *kept*, having been fully built, but with explicit fare confidence rather than
implied certainty.

---

## 2. Decision log

| # | Decision | Status | Reason | Do not revisit unless |
|---|---|---|---|---|
| D1 | Stack: FastAPI + Jinja2 + Tailwind, deployed on Vercel | **LOCKED** | Mobile-first product needing real UX control; not a Streamlit demo | A concrete deployment blocker appears |
| D2 | JSON files are the MVP data layer, not a stopgap | **LOCKED** | A cold start reads a few KB once; faster than a DB round trip. Data curation is the real work, not storage | A concrete requirement needs writes |
| D3 | Supabase deferred behind `repository.py` | **LOCKED** | No requirement forces it; do not add a DB to say we used one | The app needs to persist user data |
| D4 | Brand: Mira | **LOCKED** | Chosen by owner against 6 naming criteria | — |
| D5 | International framing — not Pakistan-specific | **LOCKED** | It is a global hackathon; the architecture is location-parameterised | — |
| D6 | Three flows, 6 screens | **LOCKED** | Coherent product surface | — |
| D7 | Excluded: Accessibility Analyzer, HerPath, study marketplace, Lost & Found | **LOCKED** | Scope discipline | — |
| D8 | No route carries a safety score or verdict | **LOCKED** | We cannot verify safety; a number would hide that. Present properties, let her judge | — |
| D9 | ~~The LLM is never the authority — it picks a `problem_key` from a closed vocabulary, never authors a process~~ **Superseded by D19** | **SUPERSEDED** | A generated procedure is a guess, and a guess is worse than nothing. The principle held; the mechanism changed | — |
| D10 | `POST` not `GET` for Flow C problem text | **LOCKED** | Query strings land in browser history, server logs and proxies. For a harassment concern that is unacceptable | — |
| D11 | **Three-state provenance**: `verified` / `illustrative` / `unverified`, as an explicit data field | **LOCKED** | Absence of a source does not tell us *why* it is absent. Deriving state from `source_url` conflated "fictional" with "unsourced" | — |
| D12 | `jurisdiction` is a field **separate from** `provenance` | **LOCKED** | A verified Pakistani legal process must never read as a universal rule for students worldwide | — |
| D13 | Campus is fictional: **Mira Demo Campus** | **LOCKED** | A real institution's name next to invented facilities is misattribution. A generic placeholder reads as unfinished | — |
| D14 | Flow A kept, with explicit `fare_confidence` | **LOCKED** | Already fully built; cost of cutting exceeded benefit. Fares are labelled by confidence, and omitted where unknown | — |
| D15 | Journey sharing is **client-side only** | **LOCKED** | No server call, no account, no stored journey. Keeps the privacy claim true | — |
| D16 | No crowdsourced reports in the MVP | **LOCKED** | User reports imply DB + moderation + abuse handling + staleness. Far too much for the remaining time. Curated sourced conditions instead; crowdsourcing listed as future work | — |
| D17 | **Validate before recommending, and before building** | **LOCKED** | An attractive recommendation can become fabricated or outdated. Sequence: Hypothesis → Validate → Compare → Present → Choose → Build | — |
| D18 | Privacy wording must not exceed what the implementation guarantees | **LOCKED** | Server logs, platform logs and the AI request path sit between the user and any absolute claim | — |
| D19 | **There is no LLM in the deployed application at all** | **LOCKED** | The only call site (`routing.route_with_claude`) imported `ai/router.py`, **which does not exist** — verified by search. It could never have fired. `anthropic` was shipped in `requirements.txt` while being entirely unused. Removed both. An integration that looks wired but is not is worse than no integration, and D3's principle ("don't add Supabase just to say we used Supabase") applies identically to an AI dependency | A validated need for LLM routing appears, and it is implemented and tested — it would go *in front of* `route_by_keywords`, which stays as the fallback |
| D20 | `provenance_state` — the **displayed** state — is distinct from the declared `provenance` field | **LOCKED** | A record declaring `verified` with no citation is a data error. It renders as `unverified`, because the safe direction to fail is toward under-claiming. Every label, marker and hint keys off `provenance_state`, so there is no path by which an unsourced record shows a tick | — |
| D21 | Where fare confidence is `unknown`, **omit the fare** rather than show a range | **LOCKED** | Owner's instruction: "where confidence is too low, simply omit the fare." A wrong number is worse than an absent one, and a stated zero is information, not a missing value — so `is_free` is its own property, since `0` is falsy and was silently hiding every free route | — |
| D22 | Flow C records with no supporting source are `unverified`, **not** `illustrative` | **LOCKED** | These are real-world claims about real processes. `illustrative` means deliberately fictional; using it here would mislabel a real claim as invented and let it dodge the honesty requirement. `unverified` is the honest label: a real claim we cannot presently substantiate | — |
| D23 | **Removed the "arriving by" field from Flow A** | **OPEN — owner may overrule** | It promised to compute "the last departure that still gets you there in time" and computed nothing; it echoed the value back. Mira has no timetable, so it cannot honestly answer that question, and the failure mode (trusting an implied leave-by, missing the last bus) is a real harm. **Validated, not guessed:** the sweep confirmed `journey_plan` did no arithmetic with it. Removing a field is reversible; shipping a wrong time is not | The owner wants it back **and** real schedule data exists to implement it against. Re-adding the *input* without the computation would restore the false promise |
| D24 | **`fare_is_free` is an explicit data field, never derived from the numbers** | **LOCKED** | Deriving it from `currency + 0/0` made a genuinely free shuttle and an unestablished rickshaw fare indistinguishable, and the app announced the rickshaw as free. Same error as D11 — a proxy that cannot tell "deliberately zero" from "don't know" must not be the source of truth. The derivation was wrong twice in opposite directions before the field existed, which is the argument for the field | — |
| D25 | **`vercel.json` replaced: legacy `builds` → `functions.includeFiles`, relying on zero-config FastAPI detection** | **LOCKED** | The original config used `builds` + `@vercel/python` + `@vercel/static`, which is the pre-FastAPI-support mechanism. It appears nowhere in the current Vercel docs (checked 2026-09-21; the FastAPI page was updated 2026-08-27) and, critically, it **bypasses automatic CDN promotion of `app.mount()`**. Under the documented path, Vercel detects the `app` instance in `app.py` and promotes the `StaticFiles` mount to the CDN at build time — which is exactly the deployment contract `templates/base.html` already assumes. `includeFiles` stays, because Vercel traces Python *imports* and would otherwise bundle neither `data/` nor `templates/`. This was **not** reasoned into correctness: it removes an undocumented mechanism in favour of a documented one, and §14b is the gate that decides whether it works | Production validation (§14b) fails on runtime, bundling or static routing — then the fallback is an explicit `api/index.py` entrypoint with `rewrites`, not a return to `builds` |
| D26 | **No co-author, contributor or "generated with" attribution anywhere in this repository** | **LOCKED** | Owner's direct instruction, 2026-09-21: *"i don't want any co-author nor contributor on the repository."* This is a judged solo submission; a second name in the commit history or the GitHub contributor list changes how the work is attributed. It also overrides the harness's default commit-trailer guidance, which defers to the owner's own instruction | Never. This is not a technical decision open to a better argument |

---

## 3. How we work (process rule)

**Never:** Idea → Choose → discover the premise was wrong.

**Always:** Hypothesis → **Validate** → Compare → Present → **Owner chooses** → Build.

Before presenting options, each must be checked for: the exact claim being made; credible
supporting evidence; whether the evidence supports *that* claim or merely a related one;
what already exists; practical feasibility including privacy and safety; and whether the
target user would actually encounter the problem.

Record the outcome here as `Claim → Evidence → Validation status → Decision → Reason`.

Corollary that has already earned its place: **demo/fictional data is never presented as
real-world evidence**, and impact claims in the Devpost submission must clearly separate
*what the prototype demonstrates* from *what real-world evidence supports*.

---

## 4. Evidence ledger

### 4a. Validated — safe to build on

| # | Claim | Evidence | Status |
|---|---|---|---|
| V1 | Students do not know what support exists, where it is, or how to reach it — and this awareness gap, not absence of need, drives non-use | Sharjah: **62.5%** did not know counselling existed; top barrier "didn't know the location" **44.4%**, "didn't know how to contact" **36.1%**; only 10.2% ever used it. Makerere: **47.2%** knew neither location nor availability. Zimbabwe: those with a mental-health condition were **28.9% less likely** to be aware of services. Trellis: **24%** of financially vulnerable students didn't know if services existed vs **17%** of secure peers — while reporting far higher distress | **High** |
| V2 | Female students face transport safety barriers that constrain mobility and academic participation | Cuenca (n=368): insecurity from harassment and poor lighting/surveillance limits mobility and forces schedule changes. Auckland (n=29): "safety work" — pre-planning, vigilance, avoiding travel after 21:00. Algiers (n=434 + 120 interviews): pervasive harassment. Kashmir (n=50), Johannesburg, Sapienza Rome, India FGDs: same direction | **High** |
| V3 | Students **already** share journey details with trusted people as a coping behaviour | Auckland study lists existing strategies: travelling in groups, **sharing location via technology**, communicating with family throughout journeys. Authors frame these as reactive, not solutions | **High** |
| V4 | Period poverty measurably disrupts attendance, and campus provision fails on awareness even where it exists | Purdue: **~1 in 5** college women experienced period poverty in the past year; 81.7% aware of the free-product programme, yet authors call for better promotion. UIC (n=106): **1 in 6** couldn't afford products, **over half** missed class, **~1 in 2** avoided changing products on campus. Ecuador: **39.6%** blocked by inadequate WASH. Cardoso: 14.2% past-year prevalence | **High** |
| V5 | Both harassment routes, their timelines, and student coverage under the 2022 amendment | Verified against the **Pakistan Code** text updated through 22 Aug 2022, plus FOSPAH material. The 2022 amendment explicitly includes **students** within "employee" and **educational institutions** within "organization" | **High** |
| V6 | SDG target wording | **4.3** equal access to affordable quality tertiary education · **4.5** eliminate gender disparities in education · **5.1** end all discrimination against all women and girls everywhere · **5.2** eliminate all forms of violence against all women and girls · **10.2** promote social/economic inclusion irrespective of sex or economic status · **11.2** safe, affordable, accessible transport **"with special attention to the needs of those in vulnerable situations, women, children…"** | **High** — verbatim from UN metadata |

**Strongest SDG mapping:** 11.2 names women explicitly for transport (Flow A). 5.2 for the
harassment flow (Flow C). 4.5 and 10.2 for an awareness gap that falls hardest on the
least-advantaged — which is the whole premise. 4.3 for tertiary access.

### 4b. Retracted or narrowed — do not reintroduce

| # | Claim we were drifting toward | What validation found | Corrected position |
|---|---|---|---|
| R1 | That Mira is a novel campus resource finder | **False.** Beacon (Staffordshire), OPALE (Lyon 1), CampusGo (Windsor), Arizona Mobile, SUU, UP Mobile, VSU-SmartMap all ship campus directories, several with wayfinding; VSU-SmartMap ships an AI chat | Mira is **not** novel as a *directory of places*. State differentiation narrowly: **provenance-first records** (source + verification date + jurisdiction per record) and **process navigation** (what to bring, what happens in what order, statutory timelines). No reviewed source showed per-record sourcing or staleness flagging |
| R2 | That the 3/7/30-day timelines sit in Section 3 | Section **3** governs *constituting* the Inquiry Committee (3 members, ≥1 woman); the timelines are Section **4** | `jurisdiction_note` citing Section 3 for composition is correct. Add the Section 4 reference to the timeline |
| R3 | ~~2022 Amendment + HEC Policy require implementation~~ | **Resolved** — the 2022 amendment does cover students and institutions | Now V5. Cite Pakistan Code / FOSPAH |

### 4c. Correction C1 — a legal misstatement caught before shipping

**What I proposed:** *"Ombudsperson route — 5-day defence, appeal within 30 days."*

**Why that is wrong:** it collapses two different procedural steps.
- **Section 6**'s 30 days = appeal from a **Competent Authority** decision to the Ombudsperson.
- **Section 9**'s 30 days = a representation by a person aggrieved by an **Ombudsperson**
  decision to the **President or Governor**.

Different steps, different actors. Shipping that wording would have misstated the law inside
the one feature whose entire value is that it does not misstate things. **Recorded here so it
cannot be reintroduced.**

**Also corrected:** the two routes are **parallel choices**, not internal-then-external. The
Act lets a complainant file directly with either.

**Independently confirmed afterwards.** A search pass returned *"The search results do not
confirm a '5 days defence' timeline specifically"*, with other secondary sources saying 7 or
15 days. Rather than ship an unsupported day-count, the statute text was checked directly and
**the owner's specification was confirmed correct**:
- **s.8(2)** — Ombudsperson route: 3-day show-cause notice, **five-day** written defence.
- **s.4** — Inquiry Committee route: charges within 3 days, **seven-day** defence.

This simultaneously re-confirmed the C1 error above (collapsing s.6 with s.9) that the owner
had already caught. **The lesson recorded here: when secondary sources disagree about a
specific number, go to the primary text or drop the number.** A plausible-looking day-count
from a summary is exactly how a legal misstatement gets shipped.

**Sources attached to the record — every one fetched and confirmed to resolve (2026-09-21):**

| Source | URL | Status |
|---|---|---|
| Pakistan Code — Act text **as updated 22 Aug 2022** | `https://pakistancode.gov.pk/pdffiles/administratorc22e81f4add9ea3dc023086953ca2b4f.pdf` | **200**, `application/pdf`, 191,668 bytes |
| FOSPAH — Laws and Rules Book | `https://www.fospah.gov.pk/SiteImage/Misc/FOSPAH%20Laws%20and%20Rules.pdf` | **200**, `application/pdf`, 811,952 bytes |
| FOSPAH — official complaints portal | `https://complaints.fospah.gov.pk/` | **200** |

Both FOSPAH URLs were **corrected on 2026-09-21**; the originals are recorded in §8 items 17
and 18 so they are not restored by accident.

**A second omission, found later in the pre-execution sweep.** Correcting the C1 wording
removed the *misstatement* of Section 6 — but the **correct** step never got added back.
Route 1 ended at "penalty imposed within one week", with no mention that a Competent
Authority decision can be appealed to the Ombudsperson within 30 days. So a student reading
the internal route had no way to learn that remedy exists.

This is the failure mode C1 was *about*, arriving from the other direction: first we said two
different 30-day periods were the same step, then we dropped one of them entirely. Neither is
acceptable in a record whose entire value is that it does not misstate the law.

**Fixed:** the appeal step is restored under **Route 1** — where it belongs, because it is an
appeal from a Competent Authority decision, not a first-instance complaint — and Route 1's
summary timeline now states it. **Route 2 still carries only its own 30-day-adjacent decision
timeline.** The two periods remain distinct and correctly placed, which was the whole point.

**Rule recorded:** when a correction *removes* a wrong statement, check that the right
statement is actually present afterwards. A deletion is not a fix.

### 4c-bis. Primary-source verification of the harassment record (2026-09-21)

**What was done:** the Pakistan Code PDF was downloaded (191,668 bytes), its text extracted
(12 pages, 26,977 chars), whitespace-normalised, and every factual claim the harassment card
displays was then matched against it **section by section**. This had never been done — the
earlier pass had located the URLs but never re-fetched them, and never read the text.

**Document identity confirmed:** *"THE PROTECTION AGAINST HARASSMENT OF WOMEN AT THE
WORKPLACE ACT, 2010"*, header reads **"Updated Till 22.8.2022"** — which is the version the
record's `jurisdiction_note` claims.

| Claim displayed in Mira | Primary text | Section |
|---|---|---|
| Committee: three members, at least one a woman | *"The Committee shall consist of three members of whom at least one member shall be a woman. One member shall be from senior management and one shall be a senior representative of the employees"* | **s.3(2)** |
| Charges communicated within 3 days | *"The Inquiry Committee, within three days of receipt of a written complaint, shall (a) communicate to the accused the charges…"* | **s.4(1)(a)** |
| **Route 1** defence: **7 days** | *"require the accused within seven days from the day the charge is communicated to him to submit a written defense"* | **s.4(1)(b)** |
| Findings to the Competent Authority within 30 days | *"shall submit its findings and recommendations to the Competent Authority within thirty days of the initiation of inquiry"* | **s.4** |
| **Route 1** appeal: **30 days** to the Ombudsperson | *"Any party aggrieved by decision of the Competent Authority… may within thirty days of written communication of decision prefer an appeal to an Ombudsperson established under section 7"*; *"A complainant aggrieved by the decision of the Competent Authority may also prefer appeal within thirty days"* | **s.6(1), s.6(2)** |
| **Route 2** defence: **5 days** | *"shall submit written defense to the Ombudsperson within five days"* | **s.8** |
| Representation to President/Governor within 30 days | *"Any person aggrieved by a decision of Ombudsperson under subsection (5) of section 8, may, within thirty days of decision, make a representation to the President or Governor"* | **s.9** |
| 2022 amendment covers **students** | *"shall include a student, a performer, an artist, a sportsperson, an intern, trainee…"* | **s.2, "employee"** |
| 2022 amendment covers **educational institutions** | *"Educational Institutes, Medical facilities…"*; *"including educational institutions, gigs, concerts, studios…"* | **s.2, "organization" / "workplace"** |

**Result: every claim in the record is supported by the specific section cited, and the two
30-day periods (s.6 appeal, s.9 representation) are confirmed as genuinely different steps —
the C1 error is now closed against the primary text rather than against a summary of it.**

Two things this confirms that a summary could not:
1. The **five-day / seven-day distinction is real**, which is the exact number secondary
   sources disagreed about (§4c). Had the record been built on those summaries it would have
   been wrong.
2. The PDF **is** the amended version, not the 2010 original — the student and educational-
   institution wording appears in it. The record's central claim about scope therefore rests
   on the text, not on an inference about which version was downloaded.

**Still not done:** the FOSPAH Laws and Rules Book PDF was confirmed to resolve but its text
was **not** read. It is attached as a corroborating source only; nothing in the record depends
on it. Marked here so the distinction between "link works" and "claim verified against it" is
not blurred.



- Whether students want **one** app for all three flows. No evidence found either way.
- Whether LLM routing beats keyword search for this vocabulary. Untested. The
  deterministic-first design means we ship safely either way.
- Whether women's-transport hours are obtainable from citable sources per city.
- **Demand-side evidence for a provenance-first directory.** The *awareness* gap is proven;
  that *citing sources* is the fix remains **our hypothesis**, not a finding. Do not claim
  otherwise in the submission.

---

## 5. Provenance rules — BINDING

> **Verified** — the cited source supports the **specific factual claim displayed in Mira**,
> within the stated jurisdiction and relevant time period.
>
> **Illustrative** — intentionally fictional/demo information created to demonstrate Mira,
> not presented as a real-world fact.
>
> **Unverified** — a real-world claim for which Mira currently lacks sufficient authoritative
> evidence. Must not be presented as established fact.

**Supporting rule — the "exact claim" bar.** A source must support the **actual claim**, not
merely something related to it. A source proving a government offers a scholarship does
**not** verify our statements about eligibility, deadline, amount, or application route. Each
material claim needs its own sourcing.

**Prohibited inference.** Never promote an illustrative campus record to Verified because a
similar service exists in the real world. A real source establishes the scheme exists *there*,
not that it exists at our fictional campus.

**Applied default:** campus records are `illustrative`; real-world processes are `verified`
(with a real citation) or `unverified`. Jurisdiction tag always visible on
jurisdiction-specific records.

**UI requirement:** the three states must be distinguishable **without relying on colour
alone** — `✓ Verified` · `◇ Illustrative` · `! Unverified`.

---

## 6. Privacy rules — BINDING

**The promise, precisely:** *"Mira does not require an account, and does not store your
problem description or your journey."*

**Do NOT use:** ~~"Nothing you type is stored."~~ — broader than the implementation can
guarantee. Server logs, platform logs and the AI request path all sit between the user and
that claim.

**By flow:**
- **Flow B** — read-only. No input.
- **Flow C** — problem text is `POST`ed (never `GET`), used for the current interaction,
  and not written to any store. Document on the About page exactly what happens technically,
  including that the text is sent to the model provider when routing is enabled.
- **Flow A** — journey sharing is built and shared **entirely in the browser**. No server
  call, no account, no stored journey.

**Never make a privacy claim broader than the implementation supports.**

---

## 7. Architecture and data model

**Stack:** FastAPI · Jinja2 · Tailwind (built to a static file, **not** the Play CDN) ·
deployed to Vercel as a Python function. `.python-version` pins 3.12; local dev is 3.14.

**Two Vercel rules that must not be "tidied":**
1. No startup/lifespan data loading. Serverless invocations are stateless and startup
   handlers do not fire reliably. `repository.py` uses `lru_cache` — one disk read per cold
   start, in-memory thereafter.
2. Nothing runs long. Hobby caps a request at 10s.

**Location-parameterisation:** every record carries `country` / `city` / `campus`. A new
location is new rows, not new code. `models.slugify()` is the single slug implementation —
`Location.slug` and `repository.location_id()` both delegate to it, so a link and its lookup
cannot drift apart.

**Repository interface** (the only module that knows where data lives):
`get_resources()` · `get_support_processes()` · `get_support_process()` · `get_routes()` ·
`get_routes_from()` · `get_from_areas()` · `count_by_category()` · `get_locations()` ·
`get_location()` · `problem_keys()` · `clear_cache()`

### Data model changes — **APPLIED** (all of them)

| Field | On | Values | Purpose |
|---|---|---|---|
| `provenance` | Resource, SupportProcess, Route | `verified` \| `illustrative` \| `unverified` | Replaces deriving state from `source_url`. `source_url` stays as the citation, not the state |
| `provenance_state` | all three — **derived property** | same three, but authoritative for display | `verified` **and** a real `source_url`, or it renders `unverified`. See D20 |
| `jurisdiction` | all three | `Pakistan` \| `United Kingdom` \| `demo environment` | Rendered as a visible tag. Keeps a local rule from reading as universal |
| `source_name` | all three | free text | Show source *name* + link + date, not a bare URL |
| `additional_sources` | SupportProcess | list of `{name, url}` | The harassment record cites the statute *and* FOSPAH material |
| `jurisdiction_note` | SupportProcess | free text | The "this is Pakistan-specific" paragraph, rendered **above** the procedure |
| `fare_confidence` | Route | `estimated` \| `unknown` \| … | Drives explicit fare labelling. Where `unknown`, **omit the fare rather than guess** |
| `fare_is_free` | Route | bool | **Explicit, not derived.** `0/0` is ambiguous between "free" and "unknown", and deriving it announced a free rickshaw. See D24 |
| `conditions` | Route | list of `{text, provenance}` | Curated, sourced conditions. **Not** crowdsourced |
| `options` / `choice_note` | SupportProcess | list of parallel routes | Renders both harassment routes side by side with no ranking language |

**Current data shape:** 21 resources, 9 support processes, 6 routes. All campus records
`illustrative`; all Flow C records `unverified` **except `pk-lhr-s03`** (harassment), which is
`verified` with three real sources and `jurisdiction: "Pakistan"`. `pk-lhr-r02` (rickshaw)
carries `fare_confidence: "unknown"` deliberately, so the omit path is visible in the demo.
`pk-lhr-009` carries an old `last_verified` so the staleness badge fires.

---

## 8. Correctness fixes — **APPLIED** (18 items)

Seven original, four found while applying those, four in a pre-execution sweep, one found by
*running* the app, and two found by auditing the sources themselves. Items 16–18 are the ones
that only appeared **after** the code was executed and the citations were fetched.

**The original 7:**

1. ✅ `models.py` → `_last_departure_after_dark`: a **03:00** departure computed as *not* after
   dark because the test was `minutes >= 18:30`. Every departure 00:00–06:00 was misreported.
   Fixed: dark window = `>= 18:30` **or** `<= 06:00`. Was mislabelling `uk-mcr-r02`.
2. ✅ `data/resources.json` → `uk-mcr-008` "Night Bus Stop" was categorised `womens_facilities`.
   **Removed entirely** — it duplicated `uk-mcr-r02` and was miscategorised.
3. ✅ `pk-lhr-014` "Women's Help Desk" moved out of `health_services` into the new
   `support_desk` category ("Someone to talk to").
4. ✅ `uk-mcr-003` retitled "Library Washrooms", `women_only: false`.
5. ✅ `app.py` → `_is_demo()` **inverted in effect**. Replaced by `_has_illustrative()`,
   which asks the data rather than inferring: whether data is fictional is a property of the
   data, so it is now a field, not a heuristic.
6. ✅ Staleness was invisible because no record was >90 days old. `pk-lhr-009` now carries
   `last_verified: "2026-05-01"`.
7. ✅ `data/support.json` → `uk-mcr-s02` "Nothing is required to make a report" moved out of
   `documents` (where it rendered inside a "What to bring" checklist) into `steps`, reworded:
   *"You do not need to prepare anything to make a report. Reporting and providing evidence
   are separate steps."*

**Four more found while applying the above:**

8. ✅ **The Flow C router was broken three times in a row, each fix wrong in a new way.**
   Recorded in full because the sequence is the lesson.

   | Attempt | Rule | What it did wrong |
   |---|---|---|
   | 1 | `term in haystack`, score = word count | A single word scored **1** against a medium threshold of **2**, so `"I need a doctor"`, `"hostel"` and `"scholarship"` all returned **no match**. Also matched `"hall"` inside *"challenge"*, `"mess"` inside *"message"*, `"room"` inside *"washroom"* |
   | 2 | score `1 + words`, thresholds 6 / 3 | Raised the score to 2 **and** the threshold to 3 — so single words *still* failed. The scale and the thresholds have to move together |
   | 3 | `\bterm` (word-start only) | Fixed `"hall"`/`"challenge"` but **created a worse bug**: `\bfee` matches `"feel"`, so **"I feel unsafe" routed to the fees record** — the single most dangerous miss available, since that is the harassment card she would have needed |

   **Final:** whole-word matching (`\bterm\b`), thresholds 5 / 2, and the vocabulary lists
   its own variants (`"fees"`, `"harassment"`, `"depression"`, `"results"`, `"appeals"`)
   instead of relying on stemming. Patterns compiled once at import.

   **The lesson, which is not the one I expected:** attempt 1's bug was found by *reading*.
   Attempt 3's bug was **created by fixing** attempt 1 while reading, and was only visible by
   **running queries**. A fix applied to code that has never been executed is a hypothesis,
   not a fix — and the second-order bugs it introduces are the ones that survive review,
   because the reviewer is looking at the thing they just changed.
9. ✅ **`show_fare` hid every free route.** `bool(self.fare_min or self.fare_max)` treats `0`
   as falsy, so the free shuttle (`pk-lhr-r03`) could never display "Free". Added an explicit
   `is_free` property — a stated zero is information, not a missing value.
10. ✅ **`m.source_link` was deleted from `_macros.html` while three templates still called
    it** — Jinja would have raised `UndefinedError` on render. Replaced with `m.sources`.
11. ✅ **`help_result.html` match-note tested `method == 'keyword'`** but the router emits
    `'keywords'`, so the honesty note about the match being a guess never rendered. Changed to
    `method != 'list'`, which is also more correct: the note belongs whenever Mira did the
    matching, which is now always except an explicit list pick.

Also corrected: `pk-lhr-r03` carried `womens_transport: true` on a **free university shuttle**,
which is not a women's-only service — the same class of self-contradiction as #4. Set to
`false`.

**Three more found in a pre-execution sweep (cross-checking every template against the
context `app.py` actually passes, since nothing had ever been rendered):**

12. ✅ **`journey.html` made a promise the code did not keep.** The form asked for an arrival
    time and told the student it would be *"used to show you the last departure that still
    gets you there in time."* `journey_plan` accepted the parameter, passed it to the
    template, and the template printed it back in a sentence. **Nothing computed anything.**
    The failure mode is a student trusting an implied "leave by" and missing the last bus —
    and Mira has no timetable data to compute one from (a last-departure time and a duration
    range are not a schedule). **Removed the field entirely** rather than implement arithmetic
    that could be wrong, and replaced the promise with an explicit statement that Mira has no
    timetable. Restoring it means implementing it against real schedule data, not re-adding
    the input. Recorded as **OPEN** in the decision log, not locked.
13. ✅ **Tailwind would never have generated the provenance classes.** Tailwind emits a class
    only when it appears as a **literal string** in `content`. Three sites in `_macros.html`
    build the name by interpolation — `chip-{{ record.provenance_state }}`,
    `prov-note-{{ record.provenance_state }}`, `chip-mark-{{ condition.provenance }}` — so the
    scanner saw `chip-` and never the finished name. Those three families would have compiled
    to **nothing**, and the failure is quiet: markup correct, page renders, and the provenance
    chips — the single visual element this product is built around — come out unstyled. Two of
    the three states happen to appear literally in `about.html`, which is exactly what would
    have made it hard to catch in a spot check. Fixed with a `safelist` in
    `tailwind.config.js`, with a note to extend it if `PROVENANCE_STATES` ever grows.
14. ✅ **`repository.problem_keys()` documented a component that no longer exists.** Its
    docstring still read *"The closed vocabulary the LLM router is allowed to choose from. The
    model never invents a process…"* — describing the architecture D19 removed. Rewritten.
    Stale documentation that contradicts the decision log is how a dropped design comes back.
15. 🚨 **The app would have told students a rickshaw was free.** `is_free` derived "free" from
    `currency` being set and both fares being `0`. But **two** routes hold `0/0` and they mean
    opposite things:

    | Route | Reality | `0/0` meant |
    |---|---|---|
    | `pk-lhr-r03` | a university shuttle that genuinely is free | free |
    | `pk-lhr-r02` | a rickshaw whose fare we could not establish | *unknown* |

    The property could not tell them apart, so it announced **"Free" for the rickshaw**. A
    student who believed that boards expecting no charge.

    This is the **same mistake as D11, in a different field**: deriving a state from a proxy
    that cannot distinguish "deliberately zero" from "we don't know". The original bug fixed
    this session (`bool(fare_min or fare_max)` hiding free routes) was the *first* attempt at
    the derivation, and it was wrong in the opposite direction. Two wrong answers from one
    proxy is the argument for the field.

    **Fixed** by making it explicit: `fare_is_free` is now a data field (D24), set `true` on
    the shuttle and `false` on the rickshaw. The rickshaw now renders "Not shown" with the
    omit-path explanation, which is what the record was always meant to demonstrate.
16. 🚨 **A query-string hole that undid D10 — found only by reading the server's access log.**
    `help_form` accepted `problem` as a **query parameter**. Nothing linked to it and the POST
    path renders its own echo, so it was dead code — but it left a working route by which
    problem text travels in a URL:

    ```
    POST /help HTTP/1.1  200 OK        <- body never logged. Correct.
    GET  /help?problem=secret          <- the text, in the access log.
    ```

    D10 is marked **LOCKED** precisely because a query string lands in the address bar,
    browser history, proxy logs and the `Referer` header of every later request. One unused
    parameter reopened all of it. **Removed**, verified with a canary: `GET
    /help?problem=SECRETCANARY` no longer echoes, and the POST no-match echo still works.

    **Why this is worth its own entry:** the decision was correct, documented, and locked —
    and still had a hole, because a *decision* is not an *implementation*. The sweep that
    read the code did not catch this. Running the server for ten seconds and looking at its
    log did. That is the argument for §15.
17. 🚨 **A dead source URL had been shipped as a citation, and fetching it is the only thing
    that could have found it.** The harassment record's second source pointed at
    `https://www.fospah.gov.pk/SiteImage/Misc/files/FOSPAH%20(LAWS%20AND%20RULES%20BOOK).PDF`
    — **HTTP 404**. FOSPAH has rebuilt its site; the entire `SiteImage/Misc/files/` tree is
    gone, and the file now lives at `SiteImage/Misc/FOSPAH Laws and Rules.pdf`. Search engines
    still index the **old** path, which is exactly why this looked fine: the URL was located
    by search in an earlier pass and never fetched, so a stale index entry was indistinguishable
    from a working link.

    **Why this matters more than a broken link:** this record is the *only* `verified` record
    in the entire dataset, and it carries the whole provenance story. One of its two citations
    pointed at nothing. In a product whose entire claim is "we cite our sources and you can
    check us", a citation that 404s is not a cosmetic defect — it is the failure mode the
    product exists to prevent, occurring inside the product.

    **Rule recorded:** a URL that has been *located* is not a URL that has been *verified*.
    Locating happens through a search index that may be months stale. Every citation must be
    **fetched** before it is published, and re-fetched before a demo. See §14b check 5.
18. 🚨 **A source was labelled "official complaints portal" while pointing at the homepage.**
    The same record's third source carried the name *"FOSPAH - official complaints portal"* and
    the URL `https://www.fospah.gov.pk/` — the landing page. The actual portal is
    `https://complaints.fospah.gov.pk/` (confirmed 200). The label made a claim the URL did
    not support.

    Same shape as everything else in this list: **the name asserted one thing and the data
    said another.** Fixing only the 404 would have left this one in place, because a working
    URL is not the same as a *correct* one. Checking that a link resolves does not check that
    it goes where its label says.

---

## 9. Milestones

| Day | Date | Target | Status |
|---|---|---|---|
| 1 | 21 Sep | Repo · FastAPI skeleton · templates · Tailwind build · **deployed to Vercel** | **In progress** — backend, templates and CSS build done; **app runs and all 30 route checks pass locally**; deployment chain under way (GitHub → Vercel → production regression) |
| 2 | 22 Sep | Flow B complete · provenance states rendering · campus renamed | Not started |
| 3 | 23 Sep | Flow C complete · both harassment routes · sources · privacy wording | Not started |
| 4 | 24 Sep | Journey sharing · curated conditions · sourced records (8–12) | Not started |
| 5 | 25 Sep | Second-country dataset · submission assets begin | Not started |
| 6 | 26 Sep | Polish · screenshots · description · video · **submit early** | Not started |

**Deadline: 2026-09-27 09:45 GMT+5.**

---

## 10. Known risks

- **Schedule.** 6 days, and validation now sits on the critical path. Sourcing 8–12 records
  is real work. If it slips, the honest fallback is **fewer** verified records — never
  invented ones.
- ~~**One verified record is load-bearing** for the entire provenance story, and its URL could
  not be re-fetched this pass.~~ **CLOSED 2026-09-21 — and it was worth doing.** All three
  source URLs were fetched. The Pakistan Code PDF resolves (200, `application/pdf`, 191,668
  bytes), **and its text was extracted and read**, confirming every claim in the harassment
  record section by section (§4c-bis). The FOSPAH "Laws and Rules Book" URL **404'd** and was
  replaced (§8 item 17). Had this shipped, the single record carrying the entire verified
  story would have had one of its two citations pointing at nothing.
- **Sourcing time.** The "exact claim" bar is deliberately strict, which makes each verified
  record slower. This is the correct trade but it must be planned for.

---

## 11. Cut lines

Cut, in this order, if time runs short:
1. Flow A entirely (P1, already built — cutting wastes the work, so only if genuinely needed)
2. Curated transport conditions
3. Second demo location
4. Journey sharing

**Never cut:** the provenance states · the sources · the privacy wording · the "no safety
verdict" rule.

---

## 12. Demo plan

- **Primary journey to screenshot:** home → *I need help* → type a problem → routed process
  with sources → *Get me there* → journey with share.
- **Show both provenance states side by side** — this is the differentiator, and it is
  invisible if the demo only shows one.
- **Show the jurisdiction tag** on the harassment card.
- Screenshots at phone width; the product is mobile-first.

---

## 13. Devpost requirements

### 13a. Required submission items

Public link · description · **3+ screenshots** · optional 1–5 min video · tech list · source
code (GitHub — **repo initialised 2026-09-21**, not yet pushed).

### 13b. Submission-critical facts (preserved from `notes/` before it left the repo — §16)

| Fact | Value |
|---|---|
| **Deadline** | **2026-09-27 04:45 UTC** — 26 Sep 23:45 CDT (UTC−5) and 27 Sep 09:45 GMT+5 (UTC+5) are the **same instant**, not a conflict |
| Organiser / scale | Hack Club · online · public · **55 participants** · prizes total **$35** |
| Eligibility | Ages **13+**, **students only**; companies and professional orgs excluded; all countries |
| Tags | Education · Social Good · Beginner Friendly |
| Teams | Solo and teams both allowed (up to 4) — **this entry is solo** (D26) |
| ⚠️ **Open, unconfirmed** | The listing URL path showed `/submissions/1189961/edit`, suggesting a **Devpost draft submission may already be started**. Never confirmed. **Check before the final submission step** — submitting to a different draft would fragment the entry |

### 13c. Judging, and what it implies

Scored on **SDG Impact & Relevance · Creativity & Originality · Execution & Functionality.**

The organisers' own wording, worth holding onto:
- *"Most hackathons stop at 'what can you build?' This one asks 'what can you build that
  matters?'"*
- *"The judging is based primarily on SDG impact, creativity, and execution. **Technical
  complexity is optional.** A simple, well-thought-out idea can outperform a highly technical
  one."*
- The criteria ask how **clearly** the idea is communicated and how **complete and functional**
  the build is — *"no dead links, no placeholder screens."*
- **No criterion references technical complexity, code volume, or team size.**

**This is why the remaining time goes to sourced records and honest presentation rather than
more features.** The rubric explicitly does not reward the thing we would be tempted to add.

### 13d. Framing discipline for the writeup

Separate *what the prototype demonstrates* from *what real-world evidence supports*. Do not
claim novelty as a directory (R1). Do not claim the citation model is proven to work (§4d).

---

## 14. Deployment

### 14a. Configuration and tooling

**Authentication / deployment state — status only, never credentials.**
No tokens, keys or passwords are recorded anywhere in this repository. Only whether each
step has happened, so a dropped session knows exactly where it stands.

| Step | State | How to verify |
|---|---|---|
| Git identity | **PENDING — user configuration** | `git config --get user.name` · `git config --get user.email` |
| Git repository | **INITIALISED** — `main`, 30 files staged, **no commit yet** | `git status` |
| GitHub auth | **PENDING** — `gh` installed (2.101.0), not logged in | `gh auth status` |
| GitHub remote | **NOT CREATED** | `git remote -v` |
| Vercel auth | **PENDING** — CLI installed (59.23.2), not logged in | `vercel whoami` |
| Deployment | **NOT ATTEMPTED** | — |
| Public URL | *— none yet —* | — |
| Production acceptance test (§14b) | **PENDING** | — |

**Identity is deliberately not guessed.** Git's `user.name` and `user.email` populate the
author and committer metadata on every commit, so inventing them would attribute the work to
someone who does not exist — and D26 requires this repo to read as the owner's alone.

**Tooling confirmed present:** `git` 2.55.0 · `gh` 2.101.0 · Vercel CLI 59.23.2 (minimum for
FastAPI support is 48.1.8) · Node 24.21.0. Vercel CLI installed via `npm install -g vercel`.

- Target: Vercel (Python runtime). `.python-version` = 3.12.
- **`vercel.json` — REPLACED (D25).** It now contains only:
  `functions: { "app.py": { "includeFiles": "{data,templates}/**" } }`.
  Routing and static serving are left to Vercel's zero-config FastAPI support, which detects
  the `app` instance in `app.py` and **promotes the `app.mount("/static", StaticFiles(...))`
  to the CDN at build time**. `includeFiles` is retained because Vercel traces Python
  *imports*, and neither the JSON data nor the Jinja templates are imported — without it the
  deployed function would find no data and no templates.
  The previous `builds` + `@vercel/python` + `@vercel/static` config is gone: it is absent
  from current Vercel documentation and bypasses CDN promotion.
- **Tooling present:** `git` 2.55.0, `gh` 2.101.0, Vercel CLI **59.23.2** (minimum for
  FastAPI support is 48.1.8). Vercel CLI was installed with `npm install -g vercel`.
- **`.vercelignore`:** excludes `.venv/` and `node_modules/` — the latter alone is **6,227
  files**. Also excludes the tracker, README, `notes/` and Tailwind tooling.
- `static/css/styles.css` is committed, so the deployed build needs **no Node step**.
- Do not ship both `pyproject.toml` and `requirements.txt` — no lockfile, and it breaks the
  build. Only `requirements.txt` exists, pinned: `fastapi==0.115.6`, `uvicorn==0.34.0`,
  `jinja2==3.1.5`, `python-multipart==0.0.20`. **`anthropic` was removed** — see D19.
- Environment variables: **Mira requires none.** There are no secrets, no API keys, no
  database URL. A missing-key failure is therefore not a possible production failure mode,
  and the deployed function reads only bundled files.

### 14b. Production acceptance test — run against the public URL, not localhost

Vercel reporting "Deployment successful" is **not** the acceptance criterion. It only means
the build step exited zero. Deployment is a **new environment** and is validated exactly as
local execution was.

Walk the full path in order: public URL → landing → every primary route → every form/action →
static CSS → router → provenance rendering → harassment process → privacy.

| # | Check | Pass condition |
|---|---|---|
| 1 | Landing page and every primary route | HTTP **200**, no Jinja/template error, no Vercel error page |
| 2 | `/static/css/styles.css` | 200, `text/css`, **29,969 bytes**, and served as a **CDN asset** — not through the Python function |
| 3 | Provenance rendering | ✓ / ◇ / ! glyphs, labels and chip styling all present and **styled** (this is the safelist regression — see §8) |
| 4 | Harassment record | Both routes render; 3/7-day and 3/5-day defences **not** collapsed; "Applies in Pakistan" visible |
| 5 | Forms | `POST /help` works over real HTTPS: match, no-match and urgent paths |
| 6 | Router | `"Mere paas fee ke paise nahi hain"` → `cant_pay_fees`, medium confidence |
| 7 | **Privacy canary** | Submit that phrase. Verify: request is a **POST**; the text appears in **no URL or query string**; it appears in **no generated link**; `GET /help?problem=<canary>` still does not echo |
| 8 | Request-body logging | No problem text in any log surface we can inspect |
| 9 | Mobile viewport | Renders correctly **on the deployed domain** at 375px, not just locally |
| 10 | Development-only assumptions | No localhost URL, no debug output, no traceback leaked to the user |

**The AI question, answered accurately:** the problem text is **not** sent to any external AI
service, because there is no LLM in the application at all (D19). Routing is deterministic and
in-process. So §6's privacy wording — that the text is used to select a topic and then
discarded, and that we do **not** claim "nothing is stored" because the platform keeps its own
request logs — is the accurate description **provided check 8 holds**. If check 8 fails, the
About page wording is wrong and must be corrected rather than the finding explained away.

### 14c. Sourcing priorities — only after 14b passes

Not an arbitrary quota, and **never** relax §5 to raise the count. A record the source does
not specifically support stays `unverified` no matter how plausible it is.

Prioritise records the demo journey actually walks through, so a judge *encounters* the
provenance model rather than reading a statistic:

- **Flow B — 3–4 verified** essential/support resources
- **Flow C — 4–5 verified** support processes, **especially the legally sensitive or
  high-consequence ones**
- **Flow A — 1–2 verified** transport/service records, where a reliable primary source exists

Current state is **1 verified**, which means the trust model works but is nearly invisible.
That is the submission-quality bottleneck, not the feature count.

### 14d. Credential handoff — the exact next three commands

Everything else is done. These three steps need the owner's own environment, and **no part of
them should be guessed or automated**:

```
1.  git config --global user.name  "Your Name"
    git config --global user.email "you@example.com"

2.  gh auth login          # GitHub CLI device/browser flow

3.  vercel login           # Vercel CLI device OAuth flow
```

**Then, in order:** verify all three states (§14a table) → create the commit → create and push
the GitHub remote → deploy → run the §14b acceptance test against the **public URL**.

**Do not record any token, key or session secret in this tracker or anywhere in the repo.**
State is recorded as `PENDING` / `VERIFIED` only. `.gitignore` already excludes `.env*` and
`.vercel/`.

**Do not start the §14c sourcing batch until §14b passes.** Public access is a hard submission
requirement; a richer dataset is an improvement. Requirements outrank improvements.

---

## 15. Development environment note

**Execution has happened.** The paragraph that used to sit here predicted that the first
`uvicorn` run would surface integration errors review could not catch. It did — see §8 items
8, 15, 16, 17 and 18. The rule now stands as: *a change that has not been executed is a
hypothesis, and the second-order bugs it introduces are the ones that survive review.*

**Two local-dev gotchas, neither of which affects production:**

1. **`repository` caches data on first read (`lru_cache`), and `uvicorn --reload` watches
   `.py` files only.** Editing a file in `data/` therefore does **not** change what a running
   dev server serves — it keeps serving the old records until the process restarts. Found by
   editing `support.json`, reloading the harassment page, and still seeing the two old FOSPAH
   URLs. *This is worth recording because the failure is silent and misleading in both
   directions: it would be easy to "verify" a data fix against a stale server and conclude
   either that the fix had failed, or — worse — that it had succeeded.* **Restart the server
   after any `data/` edit.**
2. It does **not** affect Vercel: each cold start is a new process with a fresh cache, and a
   new deployment is a new function version. Recorded so local behaviour is not mistaken for a
   production risk.

**The shell-safety classifier remains intermittent**, blocking `Bash` and `PowerShell` for
stretches at a time; the work above was done in the windows when it was up. Read-only tools
and web search are unaffected, which is why the §4c-bis source audit was still possible during
an outage.

---

## 16. Archived development notes — `notes/`

**Status: retained on disk, REMOVED from the git repository, excluded from deployment.**

`notes/` holds 8 files (`00-intake` … `07-stack-and-flows`) written during intake and option
generation. They are genuine working history and are **not deleted** — but they are no longer
tracked by git, and `.vercelignore` already kept them out of the deployment.

**Why they left the repository.** They describe directions Mira deliberately does **not**
pursue, at length and in the present tense as though they were the plan. A reviewer reading
`notes/03-options.md` finds a full specification for an accessibility auditor and could
reasonably conclude we did not know which product we built. The repository is a *submission
artifact*; private reasoning history that contradicts the shipped product does not belong in
it. `.gitignore` now excludes it, so it cannot be re-added by a careless `git add -A`.

**What was preserved before it left.** Anything submission-critical or decision-bearing was
lifted into this tracker first — the deadline instant, eligibility, judging wording and the
unconfirmed draft submission are now in §13b and §13c. The evidence ledger (§4) and decision
log (§2) were always richer than the notes.

**Worth recording, because it is the honest history:** Mira was **not the first idea.**
`notes/03-options.md` recommends a different project — *"OPTION 1 — Accessibility Auditor for
education websites ★ RECOMMENDED"* — and the directions below were all generated and explored
before being cut by owner decision (D7):

| Direction | Disposition |
|---|---|
| Accessibility analyzer for education websites | **Excluded** — was the initially recommended option |
| HerPath opportunity engine | **Excluded** |
| Study-material marketplace | **Excluded** |
| Lost & Found | **Excluded** |

*(The per-direction reasoning for those cuts lives in the notes and in the conversation
history, not here. Only the dispositions are recorded, deliberately — an invented rationale
would be worse than a missing one.)*

**What this section is for:** if a dropped session finds a `notes/` directory absent from
`git status` and wonders whether it was deleted by mistake — it was not. It was moved out of the
submission deliberately, on 2026-09-21, and its load-bearing content is above.
