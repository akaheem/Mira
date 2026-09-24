# PROJECT_TRACKER.md

**This file is the single source of truth for resuming Mira development.**
If a session drops, the next one begins with: *"Read PROJECT_TRACKER.md and resume from
CURRENT DEVELOPMENT STATE."*

It is three things at once: a **development tracker**, a **decision log**, and an
**evidence ledger**. The evidence ledger matters as much as the task list — it records what
we *disproved*, so a dead claim cannot quietly return.

Last updated: **2026-09-24**

---

## 0. CURRENT DEVELOPMENT STATE

**Phase:** Day 4 — **visual redesign complete and validated. Redeploy + submission assets.**
**Current milestone:** **Visual redesign built against the owner's design references (§14h).**
Verified records are sourced (§14e, §14f) — 11 verified, target met. Deployment is complete.

**Redesign milestone — recorded 2026-09-24:**

```
REDESIGN STATUS: LIVE IN PRODUCTION

Tokens        : new palette + self-hosted type system (D31)
Navigation    : header nav + mobile tab bar + persistent Flow C action
Mobile 375px  : PASSES on production -- no horizontal overflow, all targets >= 44px
Fonts         : Inter + DM Serif Display load and apply on the public URL
Committed     : 0e09db9, pushed to origin/main, deployed and Ready
Screenshots   : captured from the deployed domain (submission-assets/screens/)
```

**The three defects this pass found, all invisible until the page was rendered at 375px:**

1. **The compiled stylesheet was stale.** `input.css` and the templates had been edited after
   the last `npm run build:css`, so `styles.css` was missing whole component families the
   markup was already using — `.tabbar`, `.fab`, `.header-nav`, `.welcome`, `.welcome-choice`,
   `.hero-greeting`. Tailwind tree-shakes the components layer, so a class it cannot find in
   `content` compiles to **nothing**: correct markup, page renders, component silently
   unstyled. The rebuild added **5,315 bytes** (31,972 → 37,287). This is the `safelist`
   warning in `tailwind.config.js` happening for real, one level out — see §14h.
2. **The footer never cleared the fixed bars.** `.main` carries `pb-32` for exactly that
   purpose, but `.site-footer` is a **sibling** of `.main`, so it inherited nothing. At the
   end of the document the footer note sat behind the tab bar and the FAB covered the footer
   link — and because it is the end of the document, **no amount of scrolling revealed it.**
   Fixed in `.site-footer`; re-measured, and the text now clears the tab bar by 71px and the
   link clears the FAB by 88px.
3. **The FAB covered the campus name on the first-visit screen.** The persistent Flow C action
   is a *floating* button, so it sits on top of content; at 375px it landed across
   "Mira Demo Campus" — the one piece of information that screen exists to convey. Now
   suppressed while no location is chosen (`base.html`). **Not on D29 grounds:** D29
   explicitly permits a deep link to fall back to a default, and the tab bar still does. The
   reason is layout, and it was measured, not felt.

All three are the same lesson as **D27** and **§8 item 20**: the defect was reachable only by
running the thing — one by building the stylesheet, two by rendering at a real phone width.
Reading the source showed nothing wrong in any of them.

**Deployment milestone — recorded 2026-09-22:**

```
DEPLOYMENT STATUS: COMPLETE

GitHub:      PUBLIC / VERIFIED
Vercel:      PUBLIC / VERIFIED
Production:  LIVE

Remaining major work:
  MOBILE VALIDATION
  SUBMISSION ASSETS
  DEVPOST
  DEMO VIDEO
```

**Verified records: 11 of 12 Flow C processes** — target was 8–12, and the bar was never
lowered to reach it. `pk-lhr-s05` (hostel) stays `unverified` on purpose: HEC publishes no
general student accommodation policy, so there is nothing to cite (§14f). Flow B remains
`illustrative` **by construction** — a washroom's opening hours at a fictional campus cannot
be sourced, and inventing a citation for one would be the exact failure the model exists to
prevent (§14c).

**Status:** **DEPLOYED AND LIVE.** Local success was never treated as evidence that production
works — that is a separate environment with its own failure modes (runtime, bundling, static
routing, cold start) — and that refusal paid for itself: production failed in two ways that no
amount of local testing could have revealed (D27).

**Last completed:**
- Backend complete: `models.py`, `repository.py`, `routing.py`, `app.py`
- Data layer migrated to three-state provenance — 21 resources, 9 support processes,
  6 routes — **36 records, 2 locations**
- All 10 templates written and **rendered successfully**
- `static/css/styles.css` **built** — 29,969 bytes, and every component class verified
  present in the compiled output
- Deployment scaffolding created: `vercel.json`, `.vercelignore`, `.gitignore`,
  pinned `requirements.txt`, `README.md`
- **19 correctness fixes applied** (§8) — 7 original, 4 from the fix pass, 4 from the
  pre-execution sweep, and 4 found only after execution, by auditing the citations themselves,
  or by reading the deployed page (items 16–19)
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
- **Submission assets.** The redesign is live and production-validated (§14h). Committing the
  FAB fix from §14h is the last engineering step before Devpost.

**Next exact action — this order is deliberate, do not reorder:**
1. ~~`git init` + push to GitHub~~ — **DONE 2026-09-21.** `origin/main` = `8943908`, 30 files
2. ~~Deploy to Vercel~~ — **DONE 2026-09-21.** Two production-only failures found and fixed (D27)
3. ~~Full production regression test (§14b)~~ — **DONE 2026-09-22.** 9 of 10 pass, one not run
4. ~~Source the prioritised verified records (§14c)~~ — **DONE 2026-09-22.** 11 verified (§14e, §14f)
5. ~~Visual redesign against the owner's design references~~ — **DONE 2026-09-24.** See §14h
6. ~~Phone-width pass at 375px~~ — **DONE 2026-09-24.** Check 9 **passes on production**;
   found and fixed three defects (§0, §14h). 375px now passes; acceptance check 9 is closed
7. ~~Commit, push and redeploy the redesign~~ — **DONE 2026-09-24.** `0e09db9` is Live
8. **Commit and redeploy the FAB fix (base.html)** ← *next action*
9. Devpost description · technology list · demo video

**Deployment chain — live state:**

| Step | State |
|---|---|
| Git identity · `gh` · Vercel auth | **VERIFIED** — all three, see §14a |
| GitHub push | **VERIFIED** — `8943908` on `main`, sole author, no attribution trailer (D26) |
| Vercel deploy | **LIVE** — one function, region iad1 |
| **Public URL** | **https://mira-student-support.vercel.app** |
| Production acceptance test (§14b) | **9 / 10 PASS** — check 9 (mobile viewport) now passes locally against the redesign (§14h); **production re-run pending redeploy** |

**What deployment actually caught — and why the order was right.** Vercel reported a successful
deploy while serving a **static copy of the repository with no function at all**. The project
had been created with framework preset `Other`, so Vercel copied the directory to the CDN and
never looked for the FastAPI entrypoint: `Builds: . [0ms]`, build duration 2s. Every app route
returned Vercel's 79-byte `text/plain` 404 while `/static/css/styles.css` served perfectly —
a combination that looks like a routing bug and is not one. Nothing local could have revealed
this, because nothing local asks Vercel to choose a build mode. See **D27**.

**Why deployment preceded sourcing:** provenance cards are the most labour-intensive remaining
work, and there is no value in perfecting them if the deployed application then turns out to
have a production-only failure. Public access is a **hard submission requirement**; a richer
dataset is an improvement. Requirements outrank improvements — so the requirement was proven
first, and it did in fact fail first.

**Current blocker:** **None.** The application is public, the data layer loads in the function,
the stylesheet is a CDN asset, and the privacy canary passes against real production logs. Live
state is in §14a; the acceptance results are in §14b.

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
| D27 | **`vercel.json` reduced to `$schema` only, and the project's framework preset set explicitly to `fastapi`** — supersedes the `functions.includeFiles` half of **D25** | **LOCKED** | The first production deploy failed **twice, in two different ways, and neither was reachable locally**. **(1)** `functions: {"app.py": …}` was rejected outright: *"The pattern `app.py` defined in `functions` doesn't match any Serverless Functions inside the `api` directory."* Despite the FastAPI docs describing `functions` as keyed by *"your resolved entrypoint file"*, this platform version validates it against `api/**`. **(2)** Removing the key let the deploy report **success while building a static copy of the repository with no function at all** — `Builds: . [0ms]`, build duration 2 s — because the project had been created with preset `Other`. Every app route returned a 79-byte platform 404 while `/static/css/styles.css` served correctly, which reads like a routing bug and is not one. Fixed with `vercel project update mira-student-support --framework fastapi`; the zero-config path then bundled `data/` and `templates/` correctly with **no `includeFiles` at all** (§14b checks 1 and 2). `vercel link` reporting *"Detected FastAPI"* is a **local filesystem heuristic and is not evidence about the build** | A project is created fresh and its preset is `Other` again — set it **before** deploying. Do not re-add `functions` for a root entrypoint; do not return to `builds` |
| D28 | Flow C **echoes the student's own words back to her in the same response** (`You described: "…"`) | **LOCKED** | She has to see what she typed to judge whether the match is right; the no-match path repopulates the form for the same reason. This is text returned to *the same person, in the same response* — **not** a URL, not a query string, not a generated link, not a store. It looks like a privacy leak to a naive grep, which is exactly why it is pinned here: §14b check 7 tests it, and the echo is why a canary search returns a hit that must be **read** rather than counted | A redesign of the Flow C result page removes the echo — then §14b check 7's wording must change with it |
| D29 | **The home page does not pre-select a location** — a first visit asks where you are studying | **LOCKED** | Owner's decision, 2026-09-22, taken against keeping the Lahore default. A default presents one country's records as though they were the whole product, and the point of the record model is that the answer depends on where you are. The switcher summary rendered only the *city*, so nothing on the first screen revealed that a second country existed — it was one dropdown deep. **Deep links still fall back to a default** (`current_location`); only the front door asks, so `/help` reached directly neither 500s nor loops | The data holds only one country — then a chooser is a step with nothing to choose. Reverting must **not** restore the city-only switcher summary; that was the actual defect |
| D30 | **The three provenance states are shown on the home page, as live records rather than a legend** | **LOCKED** | Owner's instruction: *"the home page needs to show the three provenance states naturally. Not only on About. We don't want a judge to have to navigate to About just to discover the core trust mechanism."* Each row is a real record drawn from the dataset and linked to its own card, so the strip cannot drift from what the app shows — promoting a record to Verified changes it on the next request, with no second place to remember to update. A hand-written legend would be a claim *about* the app; this is the app. Where the current location has no example of a state, the strip falls back to the whole dataset: a trust explainer that silently shows two of its three states teaches the wrong lesson on the one screen that exists to teach it | A second place starts deciding how a state is *drawn* — `_macros.provenance` remains the only place that does. This decision is about where the vocabulary is *shown*, not how it renders |
| D31 | **Interface rebuilt against the owner's design references** (`designs/design 1.pdf`, `design 2.pdf`): new token palette, self-hosted type system, header nav + mobile tab bar + persistent Flow C action | **LOCKED** | The owner supplied the two design PDFs on 2026-09-22 and directed the rebuild. Two things inside it are decisions rather than styling: **(1) It reverses the earlier "system stack on purpose" rule** recorded in the committed `tailwind.config.js` — a webfont *is* 30–100KB on a connection where the student is already waiting. That cost was real and is accepted deliberately, not argued away: the owner's direction needs an editorial serif for hierarchy and a screen-tuned sans for body copy, and no system stack provides both across Windows, macOS, Android and iOS. The bill is 95KB — Inter is one variable file covering 100–900, and the serif's italic is fetched only on the one page that uses it. **The rule that survives is the one that mattered: nothing is fetched from a third party.** A `fonts.googleapis.com` request would hand a third party the reader's IP and the fact that she is reading a page about, say, harassment. **(2) The old scale names `sand` and `plum` were renamed, not redefined.** Redefining those hexes under the old names would have left `plum-700` resolving to a teal — a name that lies to the next person to read it. Provenance still renders as glyph **+** label **+** class, never colour alone, and verified stays green rather than teal so the trust marker does not read as chrome | A measured load-cost failure appears on a slow connection — then **subset further**, do not move to a CDN. The serif ships a single 400 cut, so headings must not carry `font-semibold`: a synthetic bold on a high-contrast serif is the one thing it cannot survive, and hierarchy comes from size instead |
| D32 | **Opening hours are answered on the campus's own clock; an unknown zone yields "Hours unknown", never a guess** | **LOCKED** | Follows from **§8 item 20**. Two things here are easy to undo by accident and must not be: **(1) `CITY_TIMEZONES` keys on IANA names, not numeric offsets**, because a fixed offset is a plausible-looking field that silently stops being true at the next DST boundary — Manchester is UTC+0 in winter and UTC+1 in summer. **(2) A location absent from the map gets `None`, not a default.** The tempting "fix" for blank hours is to fall back to UTC or to the server clock, and that fallback *is* the original defect — a wrong answer about a real place that a student may act on. The map is a maintenance obligation: adding a city means adding its zone, and `data_warnings()` names any location that has not been added | Every location carries a zone and the tz database is guaranteed present at runtime. Do **not** revisit to make blank cards go away — blank is the correct render when the zone is unknown |

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
- **Flow C** — problem text is `POST`ed (never `GET`), matched in-process against a fixed topic
  list, and not written to any store. The About page documents exactly what happens.
  - **Corrected 2026-09-22.** This bullet previously read *"including that the text is sent to
    the model provider when routing is enabled."* **D19 removed the LLM entirely**, so there is
    no model provider and nothing is sent to one. The About page already says the correct
    thing — *"It is never sent to an AI service or any third party"* — and **check 8 of §14b
    confirms it against real production logs**. The stale instruction is corrected here so a
    future session does not "restore" a claim that would now be false.
  - **The echo is deliberate (D28).** The result page renders `You described: "…"` so she can
    confirm the match. That is text returned to *her, in the same response* — not a URL, not a
    query string, not a generated link, not a store. It looks like a privacy leak under a naive
    grep and is not one; §14b check 7 tests it explicitly.
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

## 8. Correctness fixes — **APPLIED** (19 items)

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

19. ✅ **Flow C stated the jurisdiction twice.** A `jurisdiction_tag` chip and a `notice-title`,
    one line apart, both rendering "Applies in Pakistan" on every Flow C result. Found by
    reading the rendered page during the §14b acceptance test; a grep for the phrase surfaced it
    only because the count was **3** where the prose accounted for **1**. The notice block is
    the deliberate treatment — it carries the explanatory note and renders *before* the
    procedure — so the chip was removed. Re-verified on production: exactly one occurrence.

    Worth noting how it was missed for so long: every earlier check asked *"is the jurisdiction
    shown?"* and the answer was always yes. Nobody asked whether it was shown **once**. Presence
    checks pass on duplicates.

    Note also that the framework-preset failure that made the first deploy serve no application
    is recorded in **§14a + D27**, not here — it is a deployment configuration defect, not a
    code-correctness one.

20. 🚨 **"Open now" was answered on the server's clock, not the campus's.** `_hours_contain_now`
    compared a record's opening hours against `datetime.now()` — the clock of whatever machine
    ran the code, which is UTC on Vercel and the developer's laptop locally. **"Open until
    17:00" is a claim about a place, and the place keeps its own time.** At 02:00 UTC a Lahore
    campus open 07:00–22:00 reported *"Closed now"* while it was 07:00 and open; the same page
    opened from a laptop in Pakistan reported it correctly. Invisible in local testing, wrong
    in production — the same shape as **D27**, and caught the same way: by asking what the
    deployed environment does that the dev machine does not.

    Fix: `CITY_TIMEZONES` maps `(country, city)` → IANA zone, and `open_now` answers on that
    clock. **IANA names, not fixed offsets** — Manchester is UTC+0 in winter and UTC+1 in
    summer, so a hardcoded `+1` would be correct in September and quietly wrong from November,
    which is the "plausible field that stops being true" failure the whole provenance model
    exists to prevent.

    The honesty rule survives in the failure branch, and that is the part that matters: an
    unlisted city, an unparseable window, or a **missing tz database** all return `None`, so the
    card reads *"Hours unknown"* — never the server's clock. `_local_now` catches
    `ZoneInfoNotFoundError` rather than falling back, because Windows and trimmed container
    images ship no tz database; `tzdata==2025.2` is pinned for that reason. `data_warnings()`
    now names any location absent from the map, so a whole campus cannot silently go blank.

    `open_state_label` moved the wording into the model for the same reason `provenance_label`
    exists: *"Closed now"* and *"Hours unknown"* are the two strings that must never be
    confused, and two templates phrasing them independently is how that happens.

    **Verified by running, not by reading:** both configured locations resolve; Lahore and
    Manchester render from clocks 4 hours apart and each agrees with its own local time;
    `_hours_contain_now` returns `None` (**not** `False`) for no-tz, bad-tz, empty and
    unparseable specs; `_local_now(None)` → `None`; `data_warnings()` empty.

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
| Git identity | **VERIFIED** — `akaheem` | `git config --get user.name` · `git config --get user.email` |
| Git repository | **VERIFIED** — `main`, 30 files committed as `8943908` | `git status` · `git log --oneline` |
| GitHub auth | **VERIFIED** — logged in as `akaheem` (scopes: gist, read:org, repo, workflow) | `gh auth status` |
| GitHub remote | **VERIFIED** — `https://github.com/akaheem/Mira` | `git remote -v` |
| Vercel auth | **VERIFIED** — `mibraheem45846-8692` | `vercel whoami` |
| Deployment | **DEPLOYED** — production, function region `iad1`, CLI 59.23.2 | `vercel ls mira-student-support` |
| Public URL | **https://mira-student-support.vercel.app** | `curl -sI https://mira-student-support.vercel.app/` |
| Production acceptance test (§14b) | **9 / 10 PASS** — check 9 needs a browser | §14b results table |

**Project settings that are load-bearing and must not be reset to defaults:**

| Setting | Value | Why it matters |
|---|---|---|
| Framework Preset | `fastapi` | **Not cosmetic.** At `Other`, Vercel builds the repo as a static site and never runs the Python entrypoint — a "successful" deploy that serves no application at all (D27) |
| Node.js Version | 24.x | Irrelevant to the Python runtime; the Tailwind build is pre-committed |
| Root Directory | `.` | — |

**Identity was supplied by the owner, never assumed.** Git's `user.name` and `user.email`
populate the author and committer metadata on every commit, so inventing them would attribute
the work to someone who does not exist — and D26 requires this repo to read as the owner's
alone. Each state above was set by the owner and then confirmed by running the command in the
right-hand column. None was inferred from tooling output that merely looked plausible.

**Two things that looked like failures and were not.** (1) `git config --global user.name` and
`user.email` *print* the stored value; they do not set it. The first attempt used the read form,
returned empty, and looked like a broken configuration. (2) `gh auth login` stores its token in
the **Windows Credential Manager keyring** by default, so `~/.config/gh/hosts.yml` does not
exist even when logged in — *file absent* is not evidence of *not authenticated*. `gh auth
status` is the only authoritative check; a filesystem check would have sent us chasing a login
that was already working.

**The remote was not empty, and was not force-pushed over.** `origin/main` already carried
`9f56e42 Initial commit` by the owner, holding GitHub's 6-byte auto-generated `README.md`.
Rather than overwrite it, the local branch was reconciled onto it (`git fetch` → `git reset
--mixed origin/main`, which clears the index but leaves the working tree untouched), then the
30 project files were committed on top as `8943908`, with our 10,546-byte `README.md`
superseding the placeholder. The owner's commit remains in history.

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

**Results — run against the public URL, 2026-09-22:**

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Routes | **PASS** | `/`, `/needs`, `/help`, `/journey`, `/about` all `200 text/html`; `/needs` 5,533 B and `/about` 11,890 B, so the JSON data layer loaded *inside* the function |
| 2 | CSS is a CDN asset | **PASS** | Stylesheet: `X-Vercel-Cache: HIT`, `Age: 111`, ETag, and **no execution region** in `X-Vercel-Id`. The function response for `/` shows `sin1::iad1::…` with `MISS`. Provably different paths. 29,969 bytes |
| 3 | Provenance rendering | **PASS** | `✓ Verified`, `◇ Illustrative`, `! Not yet verified` each render as glyph **and** label; every `chip-*` class used in the HTML is present in the **deployed** stylesheet — the §8-item-13 safelist regression is fixed in production, not merely locally |
| 4 | Harassment record | **PASS** | Both routes render; 3/7-day (institutional) and 3/5-day (Ombudsperson) defences **not** collapsed; 30-day appeal and 90-day decision both shown; `Applies in Pakistan` present; zero occurrences of "better", "safer" or "faster" |
| 5 | Forms | **PASS** | `POST /help` over HTTPS: matched; no-match (gibberish re-renders the form gracefully); urgent (`is_urgent` true, with an honest "not an emergency service" banner) |
| 6 | Router | **PASS** | `"Mere paas fee ke paise nahi hain"` → `cant_pay_fees`, confidence `medium`, method `keywords` — exactly as specified |
| 7 | **Privacy canary** | **PASS** | Method is POST; the text appears in **no URL or query string** and in **no generated link** (checked `href`/`action`/`src`); `GET /help?problem=<canary>` returns the plain 4,909-byte form with **zero** echo, so D10 holds in production |
| 8 | Request-body logging | **PASS** | Fired a unique token through `POST /help`, then read real runtime logs: the only line is `λ POST /help`. Token 0 · "paise" 0 · request body 0 |
| 9 | Mobile viewport at 375px | **PASS** — was the last check outstanding | Measured on the **deployed domain** with a real 375×812 mobile viewport (Playwright + Edge, `isMobile`, touch): **all 13 pages return 200 with `scrollWidth` exactly 375 and zero overflowing elements.** Not a screenshot judgement — every element's `getBoundingClientRect().right` was compared against `innerWidth`, excluding deliberate scrollers. Pages covered: home (first visit and chosen), both flows' indexes and results, the Flow C form, four verified cards across both jurisdictions, the unverified card, and About |
| 10 | Development-only assumptions | **PASS** | Zero occurrences of `localhost`, `127.0.0.1`, `Traceback`, `jinja2`, `werkzeug` or a source path across all five pages |

**One finding from check 4, since fixed — §8 item 19.** Flow C rendered jurisdiction **twice**:
a `jurisdiction_tag` chip and a `notice-title`, one line apart, both reading "Applies in
Pakistan". The notice block is the deliberate treatment — it carries the explanatory note and
renders *before* the procedure — so the redundant chip was removed. Re-verified on production:
exactly **one** occurrence.

**A note on how a false alarm was avoided.** An early grep showed `Mira Demo Campus Manchester,
United Kingdom` on the Pakistan harassment card, which looked like exactly the record/location
mismatch this flow most needs to avoid. It was **not**: that string is the second `<option>` of
the location selector, and the selected location was `Mira Demo Campus Lahore, Pakistan` —
correct. A 140-character window around a grep match is not evidence. This is why §12 asks for
screenshots rather than greps.

**A second false alarm, avoided the same way — and the more useful one.** The first attempt at
check 9 used headless Edge directly (`--headless=new --window-size=375,900 --screenshot`). The
capture came back with **every line of text sliced off at the right edge** — the heading read
"What do you need right no". That is exactly what a horizontal-overflow bug looks like, and it
would have been easy to "fix" CSS that was never broken. It was not a bug: `--window-size` sets
the *window*, and the capture is clipped to it while the page lays out wider. **The tell is
that the CSS was already mobile-first** — only `min-width` media queries, no fixed widths above
375px, and a correct viewport meta — so an overflow would have had nothing to cause it.

The check was therefore run the only way that actually decides it: a real mobile viewport with
`isMobile: true`, reading `scrollWidth` and comparing every element's right edge against
`innerWidth`. Result: **375 exactly, on all 13 pages, zero offenders.** *A screenshot can be
evidence of how a page was captured rather than of how it renders.* This is the same lesson as
the grep above, one level down: the first false alarm was a grep standing in for a render, and
this one was a render standing in for a measurement.

**The AI question, answered accurately:** the problem text is **not** sent to any external AI
service, because there is no LLM in the application at all (D19). Routing is deterministic and
in-process. So §6's privacy wording — that the text is used to select a topic and then
discarded, and that we do **not** claim "nothing is stored" because the platform keeps its own
request logs — is the accurate description **provided check 8 holds**. If check 8 fails, the
About page wording is wrong and must be corrected rather than the finding explained away.

### 14c. Sourcing priorities — **UNBLOCKED: §14b passed 2026-09-22**

The gate is satisfied. Nine of ten production checks pass against the public URL, and check 9
is the same browser work as step 5. **This batch may now begin.**

```
VERIFIED RECORD TARGET: 8-12

Minimum quality — every one of these, or the record stays unverified:
  Exact claim supported        the source supports the specific claim on the card
  Correct jurisdiction         the source governs the jurisdiction the card states
  Actual URL fetch succeeds    the final URL was fetched, not merely found in search
  Source is authoritative      primary/regulatory/official, not a blog or aggregator
  Record renders correctly     re-render the card and read it, not just the JSON
  Validation recorded          the check is written into this tracker
```

Not an arbitrary quota, and **never** relax §5 to raise the count. A record the source does
not specifically support stays `unverified` no matter how plausible it is. **8 genuinely
supported records beat 12 loosely-attributed ones** — the count is a by-product of the
quality bar, never a reason to lower it.

**Correction — the three-bullet plan below was wrong, and reading the data model is what
disproved it (2026-09-22).**

The original plan split the target across all three flows. But look at what a Flow B record
*is*: `building`, `landmark`, `campus`, `hours`, `price`. Every one is a property of a
**specific fictional building at Mira Demo Campus**. There is no source on earth that
verifies the opening hours of a washroom at a campus we invented — and there should not be.
A citation for it would be a fabrication by construction.

The same holds for Flow A's six routes: they are journeys *from* the demo campus.

So the honest structural position is:

| Flow | Records | Verifiable? | Why |
|---|---|---|---|
| B — resources | 21 | **No, structurally** | Properties of an invented campus. `illustrative` is not a placeholder — it is the correct final state |
| A — transport | 6 | **No, structurally** | Routes from that same invented campus |
| C — support processes | 9 | **Yes** | Real-world statutory/administrative processes that exist independently of any campus |

**This is not a defect to fix. It is the model working.** The demo's strongest possible
statement is a single screen showing `◇` on the campus washroom and `✓` on the national
ombudsperson process, with the reader able to see *why* they differ. Promoting a Flow B
record to `verified` would destroy exactly that.

**Consequence for the target: verified records can only come from Flow C, and Flow C
currently holds only 9.** The reachable ceiling was 9, so the target of 8–12 required either
a loosened bar or a wider Flow C. The bar does not move — so Flow C widens instead.

**The widening is the demonstration the owner asked for.** Pakistan documents six problem
types; the United Kingdom documents three. Adding the three missing UK types gives the
**same six problems in two jurisdictions**, each with its own process and its own
jurisdiction tag — which is precisely "Mira's data model can represent jurisdiction-specific
support without pretending one country's rules apply everywhere," shown rather than claimed.

New UK records are written only from what an authoritative UK source actually states. If a
process cannot be sourced, the record is created `unverified` — or not created at all. **A
new record is not a new verified record.**

Prioritise in this order:

1. **Flow C, Pakistan** — 5 currently `unverified`; the legally sensitive and high-consequence
   ones first
2. **Flow C, United Kingdom** — 3 currently `unverified`, plus the 3 new types
3. Nothing else. Flow B and Flow A are complete as `illustrative`.

Current state is **1 verified of 36**, which means the trust model works but is nearly
invisible. That is the submission-quality bottleneck, not the feature count.

> **COMPLETE — 2026-09-22.** Both batches are done and recorded: **UK in §14e** (6 records,
> 6 verified) and **Pakistan in §14f** (5 records, 4 verified, 1 deliberately left
> `unverified`). The project stands at **11 verified of 12 Flow C processes** — inside the
> 8–12 target, reached without relaxing the bar. The order above was followed as written;
> note that the *reason* it named Flow C alone did not hold up, and §14c's original plan had
> to be corrected before it could push anyone toward fabrication — see the structural finding
> recorded earlier in this section.

**Method — the owner's sequence, followed exactly, per record:**

```
Candidate claim -> Find primary/authoritative source -> Open/fetch the actual final URL
-> Check exact claim against source -> Check jurisdiction -> Check current/relevant date
-> Store citation + provenance -> Re-run rendered card test -> Record validation here
```

**Do not mark something `verified` merely because an official-looking website exists.** The
FOSPAH incident (§8 item 17) is the standing proof: a plausible, official-looking URL that
had been cited as a source returned **404** when actually fetched. Every candidate URL in
this batch is fetched and its text read before the record is promoted.


### 14d. Credential handoff — **COMPLETE 2026-09-21**

These three steps needed the owner's own environment, and **no part of them was guessed or
automated**. They are retained as the record of what was asked, now that all three are done:

```
1.  git config --global user.name  "Your Name"        <- done
    git config --global user.email "you@example.com"  <- done

2.  gh auth login          # GitHub CLI device/browser flow   <- done

3.  vercel login           # Vercel CLI device OAuth flow      <- done
```

**The sequence that followed, now complete:** verify all three states (§14a table) → create the
commit → push the GitHub remote → deploy → run the §14b acceptance test against the **public
URL**. That final step is where both production-only failures surfaced (D27) — which is the
entire argument for having ordered it before the sourcing batch rather than after.

**Do not record any token, key or session secret in this tracker or anywhere in the repo.**
State is recorded as `PENDING` / `VERIFIED` / `DEPLOYED` / `PASS` / `FAIL`, plus the public URL,
and nothing else. `.gitignore` already excludes `.env*` and `.vercel/`.

**The §14b gate on the §14c sourcing batch is now satisfied** (2026-09-22). Public access was a
hard submission requirement; a richer dataset is an improvement. Requirements outrank
improvements — and here the requirement failed first, exactly as that ordering predicted.

---

### 14e. Sourcing batch 1 — United Kingdom Flow C — **VALIDATION RECORD 2026-09-22**

**Result: 6 records written, 6 verified. Project verified count: 1 → 7.**

Every URL below was **fetched and its text read in this session**. A research pass located
candidates, but nothing was promoted on a research pass's word — the FETCH step in the §14c
sequence is the one that caught the FOSPAH 404, and it is not skippable.

| Record | The exact claim on the card | Source, fetched | Verdict |
|---|---|---|---|
| `uk-mcr-s01` cant_pay_fees | Contact the student services department; they decide if you qualify; the amount is decided by the university, not nationally; lump sum or instalments; not usually repaid | GOV.UK — *Extra money from your university or college to study* | ✓ every step is the page's own statement |
| `uk-mcr-s04` scholarship_support | **There is no national scholarship scheme**; each institution sets its own rules for who qualifies, how much, and how to apply | GOV.UK — same page | ✓ verified as a *negative* — see Correction C |
| `uk-mcr-s02` harassment_concern | Raise it with your provider first; the provider must publish a single comprehensive source covering how to report and its timescales; then the provider's complaints process; then the OIA | OfS — *Condition E6* + *A guide for students: Raising an issue* | ✓ |
| `uk-mcr-s03` academic_dispute | Complete internal procedures first; Completion of Procedures Letter; **12 months** from the provider's final decision; MyOIA, email or post; never charged | OIA — *How to complain to us* + *Who can complain to us* | ✓ |
| `uk-mcr-s05` hostel_problem | Deposit protected within **30 days**; returned within **10 days** of agreement; free dispute resolution, both sides must agree, decision final; no published dispute deadline; county court if never protected | GOV.UK — *Tenancy deposit protection* + *…disputes and problems* | ✓ |
| `uk-mcr-s06` health_concern | Free and confidential counselling for undergraduates and postgraduates; mental health adviser; reasonable adjustments; NHS talking therapies self-referral; DSA needs evidence of a long-term condition | NHS — *Student mental health and counselling* + *Find NHS talking therapies* | ✓ |

**Three corrections this batch forced. Each was a real error, not a tidy-up.**

**A. `jurisdiction` was too coarse to pass its own test.** Every source above is
**England**-scoped (OfS registers English providers; NHS and GOV.UK student finance pages are
the England ones; the tenancy deposit route is England housing law), and the OIA scheme covers
**England and Wales**. The pre-existing UK records said `United Kingdom`. That fails the §14c
criterion *"correct jurisdiction — the source governs the jurisdiction the card states"*:
higher education, health and housing are all devolved, so an England-only process labelled
"United Kingdom" is precisely the overreach this field exists to prevent. Records now carry
their true scope. **The asymmetry with Pakistan — national there, England here — is not an
inconsistency; it is what the two jurisdictions actually look like**, and it is a better
demonstration of the model than uniform country labels would be.

**B. A record can be promoted only after the unsupported parts are removed.** The three
pre-existing UK records named **fictional campus places** ("Student Hub, ground floor",
"Student Money Advice Team") and asserted an unsourced timescale ("Hardship fund decisions
typically take 2-4 weeks"). Under a ✓ chip that is a fabricated fact sitting under a trust
marker. The verified PK record already showed the correct pattern — a generic, real office
("Your institution's Inquiry Committee, or the Ombudsperson"). Rewritten to what the sources
state. **Where a source states no timescale or no document list, the field is now empty**;
`uk-mcr-s01`, `-s04` and `-s06` have no timeline for exactly that reason. An empty field is
honest; a plausible one under a ✓ is not.

**C. A verified negative is still a verified claim.** The UK has no national scholarship
scheme — GOV.UK's own position is that institutions set their own rules. `uk-mcr-s04` states
that, and cites the page that says it. This is not a thin record with a gap in it; the absence
*is* the finding, and a student who learns it stops hunting for an application form that does
not exist.

**Also worth recording, because it is the kind of thing that slips through:**

- **Condition E6 imposes no fixed deadlines.** It requires providers to *publish* their
  timescales. A record claiming a national UK harassment timeline would have been invented, and
  the honest version is more useful: the timescale is the provider's, and it must be published.
- **`nhs.uk/mental-health/where-to-get-urgent-help-for-mental-health/` returns HTTP 404** — do
  not cite it. The live urgent-help page is under `/nhs-services/`.
- **The NHS student mental health page is past its own review date** ("last reviewed 29 March
  2023, next review due 29 March 2026"). It is live and remains the NHS's own guidance, and the
  claims taken from it are structural rather than time-sensitive, so it stands — but the fact is
  recorded here rather than hidden, and `source_date` on the card records **when we checked**,
  not when NHS last reviewed it. Those are different dates and the card does not conflate them.

**Still open in this batch:** *(closed by §14f — the Pakistan pass completed and is recorded
below.)*

---

### 14f. Sourcing batch 2 — Pakistan Flow C — **VALIDATION RECORD 2026-09-22**

**Result: 5 records re-sourced, 4 verified, 1 deliberately left `unverified`.
Project verified count: 7 → 11. The 8–12 target is met.**

Every URL below was **fetched in this session** and its content read — the four PDFs were
downloaded and their text extracted, so the quotes come from the documents, not from search
snippets or a research pass's summary. **The PBM requirements notice is an Urdu poster, so it
was read as an image directly** rather than relied on through anyone's translation.

| Record | The exact claim on the card | Source, fetched | Verdict |
|---|---|---|---|
| `pk-lhr-s01` cant_pay_fees | Applications go **through the institution**, addressed to the MD, PBM; the Bonafide Certificate is rejected if altered; **government institutions only**, private/self-finance excluded; not eligible if a parent is a government employee or other government assistance is received; named fee heads covered; first semester/year reimbursed to the student on a paid receipt, the rest paid to the institution; failing a subject ends eligibility | PBM — *How to Get Assistance* + form **PBM-QMS-IFA(Edu)F-01** + the Urdu requirements notice | ✓ every element is the form's own text |
| `pk-lhr-s02` scholarship_support | For the HEC Need-Based Scholarship the form comes **from** and is submitted **to** the university's Financial Aid Office; **"HEC will not accept any application form directly"**; funds are not transferred to students by HEC; undergraduate 4–5 year programmes; self-finance admission **not** eligible | HEC — *Need-Based Scholarship: How to Apply* + *Eligibility Criteria* | ✓ |
| `pk-lhr-s04` academic_dispute | Five-member grievance committee headed by the Controller of Examinations; written grievance to the Head of Department within **7 working days** of the grade; committee must hear both sides; decision within **5 working days** or before registration, whichever is earlier; decision final and binding; answer book **not re-assessed** under any circumstances; re-checking covers only listed clerical points; marks may **decrease** | HEC — *Policy Guidelines for Implementation of Uniform Semester System in HEIs of Pakistan* §19, §28 + *Students Grievance Redressal Portal* | ✓ verbatim, both section numbers confirmed |
| `pk-lhr-s06` health_concern | The policy is **binding on all HEIs, public and private**; each institution must appoint a Focal Person; a student needing medical or mental health assistance may reach out to the Focal Person; an on-campus counsellor/psychologist/psychiatrist must exist and any student with anxiety, depression or PTSD may seek them; every institution must run a helpline; support is confidential | HEC — *Policy on Drug and Tobacco Abuse in Higher Education Institutions* §1.5, §3.4, §5.2, §5.4, §5.5, §8.3 + *National Youth Helpline* | ✓ mental-health provisions are general in wording; see Correction E |
| `pk-lhr-s05` hostel_problem | **No source exists.** Stays `unverified`. | — | ✗ see below |

**Two corrections this batch forced.**

**D. A source's own scope is a limit on the card, not a footnote.** PBM's assistance is for
students in **government** institutions: the form's own title says "STUDYING IN GOVERNMENT
INSTITUTIONS" and note 3 excludes private and self-finance students. The record as written
before this pass would have sent a private-university student to an office that cannot help
her. The card now states the restriction as one of its steps, not in small print. **A source
can support a claim and still not support it for the person reading the card.**

**E. Binding and non-binding are different claims and must be carried.** HEC's drug and
tobacco policy states in §1.5 that it is binding on all HEIs under the HEC Ordinance 2002.
The semester-system examination guidelines state no such thing — they are written as guidance
("All HEIs *should* have…"). Both cards now say which they are. Flattening the two into
"national policy" would have overstated one of them, and the distinction is exactly what a
student deciding whether to rely on it needs.

**Also worth recording, because each of these is a live risk if forgotten:**

- **`pbm.gov.pk/orders/ifapolicy.pdf` returns HTTP 404.** That is the document behind the
  widely-quoted PBM income thresholds (e.g. Rs 17,500/month). **No income threshold appears on
  the card**, because the document that states it could not be retrieved. Third-party pages
  repeat the figure; they are not good enough.
- **`peef.org.pk` fails TLS verification** — certificate `CN=peef.org.pk`, Sectigo DV, expired
  **26 May 2026**. The site is live and maintained (footer "Last Updated: Sep 14, 2026") but
  unreachable without disabling certificate validation. PEEF is the most-cited Pakistani
  scholarship source, and **we could not verify it at source, so nothing from PEEF is on any
  card.** University and consultancy pages quoting PEEF deadlines were found and deliberately
  **not** used as substitutes.
- **`ehsaas.hec.gov.pk` refuses connections.** This is the portal HEC's own Benazir
  Undergraduate Scholarship page directs applicants to. Confirmed directly (21s, no response).
  Rather than omit the scheme or pretend the route works, the currency caveat is on the card
  itself, in `jurisdiction_note`, dated.
- **HEC publishes no general student accommodation policy.** HEC's full published policy index
  (25 policies) and student-services index (14 services) were read; neither contains a hostel
  or residence policy. The closest provision is in HEC's disability policy and is scoped to
  students with disabilities. `pk-lhr-s05` therefore **stays `unverified`**, and its
  `jurisdiction_note` says why. *This is the point of the state existing:* the record a student
  most wants a national answer for is the one that does not have one.
- **HEC's Benazir FAQ page is stale** — it still lists eligible admission sessions as Spring
  2020 and Fall 2020. The award-process page does not carry that problem, but the fact is
  recorded so the scheme's currency is not overstated anywhere.

**Verification run: 67 checks, 0 failures.** Render-level, in-process via `TestClient` so a
stale reloader cannot flatter the result. Covers: all 15 routes × 3 location states; every
verified record rendering its ✓ marker, source name and jurisdiction tag; every verified
record asserted free of invented campus detail ("Administration Block", "Room 12", "2-4
weeks"); `pk-lhr-s05` rendering `!` with no source URL; the trust strip rendering all three
states on **both** locations; the neutral first screen on a genuinely fresh client; and POST
routing for eight phrasings across both jurisdictions. **No verified record lacks a source
URL; no verified record carries a timescale its source does not state.**

**Multi-jurisdiction coverage — the thing this was for.** Both locations now answer the same
six problems, and the answers differ because the jurisdictions differ: fees route through
PBM's institutional channel in Pakistan and through the university's hardship fund in England;
grades go to a statutory-deadline committee in Pakistan and to the OIA after internal
procedures in England and Wales; a scholarship is a national HEC programme in Pakistan and
**does not exist nationally** in England. That is the model demonstrated rather than asserted.

### 14g. Redeploy and production re-validation — **2026-09-22**

**Commit `20e4da6` pushed to `main`; production redeployed and re-verified.** The live site had
been running the pre-trust-strip build, so local and production had diverged — the strip and
the neutral first screen existed only on disk until this deploy.

| Check, against `https://mira-student-support.vercel.app` | Result |
|---|---|
| All routes (`/`, `/help`, two topic cards, `/needs`, `/journey`, `/about`) | **200** |
| `/static/css/styles.css` | **200, `text/css`, 30,664 B** — a static CDN asset, not routed through the Python function |
| Neutral first screen | **live** — chooser present, no resolved-location line |
| Trust strip | **3 rows**, all three chips (`chip-verified` / `chip-illustrative` / `chip-unverified`) |
| PK cards: PBM source, HEC scholarship route, 7/5-working-day deadline, binding policy, hostel `!` | **all rendering** |
| UK cards: OIA + 12 months, verified negative, hardship fund | **all rendering** |
| Jurisdiction tags differ by card | **Pakistan vs England** |

**Two deployment facts worth keeping, because both cost time and would cost it again:**

- **A preview deployment is behind Vercel Authentication by default.** Fetching a preview URL
  returns `200 text/html` at ~341 KB on *every* path — including the `.css` path — with title
  `Login – Vercel`. That signature looks alarming (it resembles D27: every route a 200 serving
  the wrong thing) but is **not** an application fault. **Only the production domain is
  publicly readable**, so a content check must run against `mira-student-support.vercel.app`,
  never a `*-<hash>-*.vercel.app` preview URL.
- **`vercel deploy --prod` returned `{"reason": "deploy_failed", "message": "Not authorized"}`
  on its first attempt, and succeeded on retry with no change to the command or the login.**
  Treat it as transient once; do not start re-authenticating on the first refusal.

**Still open, and deliberately not fixed by guesswork:** `git push` does **not** trigger a
deploy — the project is not git-connected, so a push that looks successful leaves production
on the previous build. Vercel suggests `vercel git connect` to close this. Until that is run,
**deploying is a separate manual step after every push**, and the two can silently diverge.

---

### 14h. Visual redesign + mobile pass — **VALIDATION RECORD 2026-09-24**

**What was built.** The interface was rebuilt against the owner's design references
(`designs/design 1.pdf`, `design 2.pdf`): a new token palette, a self-hosted type system, and
header-nav / mobile-tab-bar / persistent-Flow-C-action navigation. Rationale and the two
reversed sub-decisions are in **D31**; the opening-hours correctness fix that landed in the
same working tree is **§8 item 20** and **D32**.

**The stylesheet was stale, and that failure is silent.** `input.css` and the templates had
been edited after the last `npm run build:css`, so `static/css/styles.css` was missing entire
component families the markup was already using. Tailwind **tree-shakes the components
layer**: a class it cannot find as a literal in `content` compiles to nothing, so the page
renders with correct markup and an unstyled component. The rebuild added **5,315 bytes**
(31,972 → 37,287).

The classes that were absent — and each one is a visible part of the product, not a nicety:

| Missing class | What it is | What its absence looked like |
|---|---|---|
| `.tabbar` | the mobile navigation | four unstacked text links at the page foot |
| `.fab` | the persistent Flow C action | an unstyled link sitting on the content |
| `.header-nav` | desktop navigation | four bare links in the header |
| `.welcome` | the first-visit screen | no gradient, no card |
| `.welcome-choice` | the two campus choices | two plain links, no tappable card |
| `.hero-greeting` | the time-of-day greeting | a bare line of text above the heading |

This is the same class of defect the `safelist` comment in `tailwind.config.js` was written
to prevent — **one level out.** That comment anticipates interpolated class names being
invisible to the scanner; this was simpler and worse: the whole file was out of date, so
*every* newly-added class was invisible. **A compiled artifact in the repo makes staleness a
state the repo can be in.** There is no build step at deploy time to catch it, because the
compiled file *is* the deploy artifact. Rule: **after any edit to `input.css` or to a
template's class attributes, rebuild before looking at a page — and rebuild before trusting a
screenshot.**

**The footer never cleared the fixed bars.** `.main` carries `pb-32` so body copy does not run
under the tab bar. `.site-footer` is a **sibling** of `.main`, so it inherited nothing: at the
end of the document the footer note sat behind the tab bar and the FAB covered the footer
link. Because it is the end of the document, **scrolling could not reveal it** — the content
was simply unreachable. Measured at 375px: footer bottom at the viewport bottom (812) while
the tab bar began at 755. Fixed in `.site-footer` (`pt-6 pb-32 sm:pb-6`); re-measured, and the
last line now clears the tab bar by **71px** and the link clears the FAB by **88px**.

Note how this one was found: not by reading the CSS, which looks correct in isolation, and
not by the `fullPage` screenshot, which renders `position: fixed` elements at their viewport
offset and so showed the bars floating mid-page as a **capture artifact**. It was found by
measuring element bounding boxes against the bars **at the true viewport**, at the bottom of
the document. The artifact and the defect look similar in a screenshot and are not the same
thing.

**And the FAB covered the campus name on the first-visit screen.** The redirect above fixed
the *footer*, but the FAB is `position: fixed` too and floats over content everywhere — at
375px it came to rest across "Mira Demo Campus" on the welcome screen. That screen exists to
get her to read one of two campus names, and the button was sitting on one of them. Fixed by
suppressing the FAB while no location is chosen (`base.html`).

This one is worth being precise about, because the easy justification is the wrong one.
It is **not** D29 forbidding a Flow C link before a location is known — D29 explicitly permits
a deep link to fall back to a default, and the tab bar still does exactly that. The reason is
layout: the FAB is an **overlay** and the tab bar is a **bar the layout reserves room for**,
and only one of those can cover the answer it is sitting next to. Re-measured after the fix:
FAB absent, both campus names `covered=false`.

**Production validation — 2026-09-24, after redeploy.** Deployed `0e09db9`; project framework
preset confirmed `FastAPI` **before** deploying, so the D27 failure mode was not re-entered.

| Check | Result |
|---|---|
| Deployment | ● Ready, Production, 13s |
| All routes on the public URL | **200** |
| Deployed `styles.css` | 200, `text/css`, **37,362 bytes** (local 37,303 + 59 CRLF bytes) |
| New classes present in the deployed CSS | ✓ `.tabbar` `.fab` `.header-nav` `.welcome` `.welcome-choice` `.hero-greeting` `.site-footer` |
| All three fonts on the public URL | 200, `font/woff2` |
| **Acceptance check 9 on production**, 7 pages @ 375×812 | **PASSES** — no horizontal overflow, every touch target ≥ 44px |
| Serif/sans actually applied on production | `h1` → DM Serif Display, body → Inter, both loaded |
| Greeting on production | "Good evening." from the reader's own clock |
| FAB on production | present on home/needs/journey/about; **absent** on `/help` and on the first-visit screen |

**The hours fix demonstrated itself on live data.** At the moment of verification it was
**23:08 in Lahore and 18:08 UTC**. `pk-lhr-003` (08:00–20:00) rendered **"Closed now"** — and
by hand, 23:08 is minute 1388 against a window ending at 1200, so closed is right. The old code
compared against the server's clock, so at 18:08 UTC it would have reported **"Open until
20:00"** for a campus that had closed three hours earlier. That is the defect, reproduced on
production data rather than argued from the source.

**Submission screenshots were then regenerated from the deployed domain** (`§9`,
`submission-assets/screens/`), as viewport captures rather than `fullPage` — the artifact
described above makes a `fullPage` capture of this app look broken to anyone who does not know
it is fixed-position behaviour.

**Verification record — what running actually proved:**

| Check | Result |
|---|---|
| `npm run build:css` | ✓ 37,303 bytes after all fixes |
| All six previously-missing classes now emit | ✓ `.tabbar` `.fab` `.header-nav` `.welcome` `.welcome-choice` `.hero-greeting` |
| All 13 routes render (`/`, `/needs`, `/help`, `/journey`, `/about`, 6 categories, 2 location-sets) | **200, no Jinja errors** |
| `styles.css` over HTTP | 200, `text/css; charset=utf-8`, 37,287 bytes |
| All three font files over HTTP | 200, `font/woff2` |
| `h1` / body font at 375px | **DM Serif Display** / **Inter** |
| Fonts actually loaded (not just declared) | Inter 100–900, DM Serif Display 400 |
| Horizontal overflow, 7 pages @ 375×812 | **none** — `scrollWidth` == `clientWidth` == 375 |
| Touch targets ≥ 44px | ✓ after fixing `.loc-summary`, which measured **42px** |
| `.tabbar` / `.fab` | `flex`; FAB correctly **absent** on `/help` (D30-adjacent: no button reloads its own page) |
| `nav_section` — tab bar and header nav agree | ✓ correct item marked on all 5 sections |
| First visit vs returning | first visit asks for location; hero **and** greeting appear only after |
| Greeting | "Good afternoon." computed from the browser's clock; element absent with JS off |
| Home prov-strip | three **real** records, one per state, glyphs ✓ ◇ ! |
| `/about` | all three state blocks render |
| Flow C `POST /help` | match and urgent echo her words + `verified` chip; **no-match does not echo** |
| Privacy canary | `GET /help?problem=<canary>` does not echo — D10/D28 hold |
| `data_warnings()` | empty |
| Timezone fix (§8 item 20) | Lahore and Manchester answer on clocks **4 hours apart**, each agreeing with its own local time |
| Unknown degradation | `None` (**not** `False`) for no-tz, bad-tz, empty and unparseable specs; `_local_now(None)` → `None` |
| Footer clearance @ 375px | text clears tab bar by 71px; link clears FAB by 88px |

**What this pass did NOT prove.** Acceptance check 9 passing **locally** is not check 9 passing
**on production** — production still serves `9349a35`, the pre-redesign build. Check 9 had in
fact already passed against that build on 2026-09-22; **the redesign replaces the stylesheet
wholesale, so that result does not carry over.** The mobile check must be re-run against the
deployed domain once the redesign is deployed, for the same reason §14b exists at all: local
success has never been evidence about production in this project, and the two production-only
failures in D27 were both invisible locally.

**Method note — a real viewport, not a captured window.** `9349a35` records that its first
attempt drove headless Edge with `--window-size` and came back with every line sliced off at
the right edge, which looks exactly like a horizontal-overflow bug and is not one. This pass
avoided that trap by using Playwright's viewport emulation (`viewport` + `isMobile` +
`hasTouch`), which lays the page out at 375 CSS px rather than clipping a wider layout — and
then **measured** `scrollWidth` against `clientWidth` and compared element bounding boxes,
rather than judging from the image. The `fullPage` captures were used only to *look* at the
page; the two defects reported above came from the numbers. The footer defect in particular
was **invisible in the fullPage screenshot**, because fixed elements render at their viewport
offset there and the bars appear to float mid-page — a capture artifact that reads as a bug
and, on this page, was hiding a real one underneath it.

**Evidence kept:** `submission-assets/mobile/` — 7 full-page captures, 3 viewport-truth
captures, and `audit.json` with the measured numbers. Not committed (`.gitignore`), and the
submission screenshots will be regenerated **from the deployed domain** after redeploy, per §9.

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
3. **Nothing local can validate a deployment *configuration*.** Both production failures (D27)
   were config, not code: a rejected `functions` key, and a project preset of `Other`. Local
   `uvicorn` cannot observe either, and `vercel link` printing *"Detected FastAPI"* is a
   filesystem heuristic that reads like a build confirmation. **The only test of a deploy
   config is a deploy** — which is why §14b runs against the public URL, and why *"Deployment
   successful"* was never accepted as the criterion. It was in fact reported for a deployment
   that served no application.

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
