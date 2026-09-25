# Mira — Your Student Support Companion

**Find what you need. Know what to do. Get where you need to go.**

Mira is a mobile-first web app for students who need something concrete and do not know
where to start: which building has the washroom, which office handles a fee problem, what
to bring, how long it takes, and how to get across campus after dark.

Built for the **Acodemic X G.I.R.L.S. Global SDG Hackathon**.

---

## The three flows

| Flow | The question | What Mira answers |
|---|---|---|
| **I need something** | *"Where can I find a washroom / period products / water / first aid right now?"* | The place, the landmark, the hours, whether it is open now, and whether it is women-only |
| **I need help** | *"I can't pay my fees. Who do I talk to, and what happens?"* | The process: who to contact, what to bring, the steps in order, the statutory timeline — with sources |
| **Get me there** | *"How do I get across campus, what does it cost, does it run after dark?"* | The verifiable properties of a trip. Fare confidence, service hours, walking distance. **Never a safety verdict** |

Six screens, three flows, plus an About page that states exactly what the app does and does
not claim.

---

## The thing that makes it different: every record carries its own truth status

Most directories tell you a thing exists. Mira tells you **how it knows** — per record, in
the interface, not in a footnote.

| Marker | State | Meaning |
|---|---|---|
| `✓` | **Verified** | A cited source supports *the specific claim displayed*, within the stated jurisdiction and time period |
| `◇` | **Illustrative** | Deliberately fictional demo data, created to demonstrate the product. Not a real-world fact |
| `!` | **Unverified** | A real-world claim Mira cannot currently substantiate. Shown as a lead to confirm, never as settled fact |

Supporting rules, enforced in the data model and in the UI:

- **A source must support the actual claim, not something related to it.** A government page
  proving a scholarship scheme exists does not verify our statements about eligibility,
  deadline, or amount. Each material claim is sourced separately, or the record drops to
  `unverified`.
- **`jurisdiction` is a separate field from `provenance`.** "How sure are we" and "where does
  this apply" are different questions. A verified Pakistani legal process must never read as
  a universal rule for students worldwide, so jurisdiction is tagged and rendered on the card.
- **Verified is conjunctive.** A record declaring `verified` with no citation is a data error,
  and it renders as `unverified`. The safe direction to fail is toward under-claiming.
- **Markers are not colour-only.** `✓ ◇ !` carry the state as text, because roughly 1 in 12
  men has a colour vision deficiency.

This is the whole premise: the awareness gap that keeps students from using support services
is documented, but awareness is not the same as *trust*, and a directory that cannot say how
it knows something is asking to be taken on faith.

---

## What Mira deliberately does not do

- **No safety score, rating, or verdict on any route.** We cannot verify safety, and a number
  would hide that. Mira presents properties — lighting, service hours, whether a route runs
  after dark, walking distance — and leaves the judgement with the reader.
- **No crowdsourced reports.** User-submitted transport conditions imply a database,
  moderation, abuse handling and staleness management. Curated, sourced conditions instead;
  crowdsourcing is future work, not a hidden half-feature.
- **No account, and no stored problem description or journey.** See *Privacy* below.
- **No AI-authored content.** There is no LLM in the deployed application. Flow C routes
  free-text descriptions to curated records using a deterministic keyword scorer. It cannot
  hallucinate a process because it never writes one — it only chooses between records that
  already exist.

---

## Privacy — what actually happens

The claim is deliberately narrow, because a broader one would be false.

- Mira requires **no account**.
- Flow B is read-only. There is no input at all.
- Flow C problem text is submitted by **`POST`, never `GET`** — so it does not land in the
  browser's address bar, browser history, or a proxy's URL logs. It is used for the current
  request and written to no store of ours.
- Flow A journey sharing happens **entirely in the browser**. The summary is assembled
  client-side and handed to the Web Share API or the clipboard. No server call, no tracking
  link, no stored journey.

**One honest limit, stated in the product:** Mira runs on a hosting platform that keeps its
own standard request logs, which this project does not control. We therefore do not claim
that *nothing is recorded anywhere* — only that **Mira itself** stores nothing.

---

## Running it locally

Requires Python 3.12+.

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows
# source .venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
uvicorn app:app --reload
```

Then open <http://127.0.0.1:8000>.

### Rebuilding the stylesheet

The compiled `static/css/styles.css` **is committed**, so neither local development nor the
deployed build needs Node. You only need this if you change templates or `static/css/input.css`:

```bash
npm install
npm run build:css
```

Tailwind is built to a static file rather than loaded from the Play CDN. The CDN is explicitly
not for production, and a build that compiles CSS in the browser is the wrong trade for a
product whose target user is on a slow connection.

---

## Architecture

```
app.py            FastAPI routes; the only place that knows about HTTP
repository.py     The only module that knows where data lives (the swap point for a database)
models.py         Frozen dataclasses; provenance, freshness and fare logic live here
routing.py        Deterministic free-text -> problem_key router for Flow C
data/
  resources.json    Places and facilities
  support.json      Processes and what they require
  transport.json    Routes and their verifiable properties
templates/        Jinja2 — base, _macros, and one file per screen
static/
  css/styles.css    Compiled Tailwind (committed)
  js/app.js         Location switcher, journey sharing. Imports nothing from the server
```

**Stack:** FastAPI · Jinja2 · Tailwind · deployed as a Python function on Vercel.

Three decisions worth knowing:

- **JSON files are the MVP data layer, not a stopgap.** A cold start reads a few kilobytes
  once and caches it in memory (`lru_cache`). Data curation is the real work here, not
  storage. Swapping in a database means rewriting `repository.py` and nothing else.
- **No startup or lifespan data loading.** Serverless invocations are stateless and startup
  handlers do not fire reliably. `lru_cache` is the correct mechanism, not a workaround.
- **Location is a parameter, not a branch.** Every record carries `country` / `city` /
  `campus`. Adding a country means adding rows, not code. The same keyword router serves
  every location because its vocabulary is keyed to problems, not to places.

---

## Data provenance in this repository

The bundled dataset is a **demo environment**:

- Campus records (places, facilities, transport routes) are `illustrative` — a fictional
  **Mira Demo Campus** with invented buildings and hours, so the product can be demonstrated
  without misattributing facilities to a real institution.
- Real-world **processes** are `verified` where a genuine source supports the specific claim
  displayed, and `unverified` otherwise. Across the two demo locations there are **12
  documented Flow C processes: 11 verified against a cited source, 1 not.** Source URLs in
  the data were located in primary or official sources and are never invented or inferred.

The app surfaces this itself: the About page renders live counts by provenance state, and
warns on any record whose declared state and citation disagree.

---

## SDG alignment

Target-level, not theme-level:

| Target | How Mira relates |
|---|---|
| **4.3** Equal access to affordable quality tertiary education | Removing the navigation cost of finding support that already exists |
| **4.5** Eliminate gender disparities in education | The awareness gap falls hardest on students with the least social capital to ask around |
| **5.1** End all discrimination against women and girls | Verified reporting routes, stated with their jurisdiction |
| **5.2** Eliminate all forms of violence against women and girls | The harassment process flow — routes, timelines and sources, with no interpretation added |
| **10.2** Social and economic inclusion irrespective of sex or economic status | Financial-aid and fee processes documented in the same place as everything else |
| **11.2** Safe, affordable, accessible transport, *"with special attention to the needs of those in vulnerable situations, women, children…"* | Journey planning that surfaces service hours, fare confidence and after-dark status |

### What this prototype demonstrates vs. what evidence supports

Stated plainly, because the distinction matters more than the pitch:

- **Evidence supports** that the awareness gap is real and consequential: students do not know
  what support exists, where it is, or how to reach it, across multiple countries and studies.
- **Evidence supports** that female students face transport barriers that constrain mobility
  and academic participation, and that students already share journey details with trusted
  people as a coping behaviour.
- **Mira's specific claim** — that *citing sources per record* is what closes the gap — is a
  **hypothesis**. It is not yet validated, and this submission does not claim otherwise.

---

## Limitations

- **Coverage is thin by design.** A small number of well-sourced records was chosen over a
  large thinly-sourced dataset. Of the 39 records in the bundle, 11 are verified, 1 is
  unverified, and 27 are illustrative by construction.
- **Counts are per location, not per bundle.** The About page reports the state counts for
  the location currently selected, so its numbers are smaller than the totals above. The two
  demo locations hold 24 records (Pakistan/Lahore — 5 verified, 18 illustrative, 1
  unverified) and 15 records (United Kingdom/Manchester — 6 verified, 9 illustrative, 0
  unverified) respectively.
- **Two demo locations**, both fictional campuses, chosen to prove the location model works
  across countries rather than to serve either.
- **Fares are estimates or omitted.** Where Mira cannot establish a fare, it shows nothing
  rather than guessing.
- **Keyword routing is literal.** Unusual phrasing falls through to "I am not sure which of
  these you mean" plus the list — which is the correct failure, but it is a failure.

---

## License

Source is provided for the hackathon submission. See the repository for details.
