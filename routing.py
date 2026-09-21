"""Problem text -> problem_key routing for Flow C.

There is exactly one router here, and it is deterministic. That is a design decision
rather than an unfinished one:

  * It cannot hallucinate a process. The whole value of Flow C is that the answer is
    curated and verifiable, so the only thing routing does is choose BETWEEN records that
    already exist. It never describes a process, names an office, or lists documents.
  * It cannot fail on stage because a network call timed out, a key expired, or a quota
    ran out. A demo that breaks when the network hiccups is worse than a demo that is
    slightly less clever on unusual phrasing.
  * It costs nothing per request, and adds no dependency to the deployed function.

An LLM-backed router that maps free phrasing onto the same closed vocabulary is a
reasonable future improvement -- it would make the router better at unusual phrasing
while leaving it equally unable to invent an answer, because it would still only return a
key. It is not built, and it is not stubbed out here, because an integration that looks
wired but is not is worse than no integration at all. If it is added, it goes in front of
`route_by_keywords`, which stays as the fallback.

The keyword sets are keyed to the shared problem vocabulary rather than to any location's
data, so the same router works in every country.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

# Keyword sets are keyed to the shared problem vocabulary, not to any location's data, so
# the same router works in every country. Roman Urdu terms are included because that is
# how a large share of students actually type.
KEYWORDS: dict[str, tuple[str, ...]] = {
    "cant_pay_fees": (
        "fee", "fees", "fees nahi", "fee nahi", "semester fee", "tuition", "afford",
        "affordable", "paisa", "paise", "paison", "qist", "installment", "installments",
        "arrears", "can't pay", "cant pay", "unable to pay",
    ),
    "scholarship_support": (
        "scholarship", "scholarships", "wazifa", "wazifay", "bursary", "grant", "grants",
        "financial aid", "financial help", "stipend", "funding",
    ),
    "harassment_concern": (
        "harass", "harassment", "harassed", "chhed", "chhedna", "misbehave",
        "misconduct", "inappropriate", "unsafe", "assault", "abuse", "complaint",
        "report someone", "teasing", "stalking",
    ),
    "academic_dispute": (
        "grade", "grades", "marks", "result", "results", "recheck", "re-check",
        "appeal", "appeals", "unfair marking", "transcript", "fail", "failed", "expelled",
    ),
    "hostel_problem": (
        "hostel", "dorm", "dormitory", "room", "warden", "roommate", "mess",
        "accommodation", "hall",
    ),
    "health_concern": (
        "health", "doctor", "medical", "clinic", "counsel", "counselling", "counseling",
        "counsellor", "counselor", "therapist", "mental", "depress", "depression",
        "depressed", "anxiety", "stress", "sick", "unwell", "sehat", "ilaaj", "dawai",
    ),
}

# Phrases that indicate the student is describing an emergency rather than an
# administrative problem. We do not try to route these -- we surface the caveat.
URGENT_MARKERS: tuple[str, ...] = (
    "emergency", "right now", "immediately", "danger", "unsafe right now", "help me now",
)

# Terms are matched as WHOLE WORDS. The vocabulary lists its own variants rather than
# relying on stemming, because every near-miss here routes a student to the wrong office.
#
# Two versions of this were wrong, in ways worth recording so they are not retried:
#
#   * Plain substring matching (`term in haystack`) matched "hall" inside "challenge",
#     "mess" inside "message", and "room" inside "washroom".
#
#   * A leading boundary only (`\bterm`) fixed "hall"/"challenge" but not the others:
#     "mess" still matches "message", because "mess" does begin a word. Worse, "fee"
#     matches "feel" -- so **"I feel unsafe" routed to the fees record**, the single
#     worst miss available, since it is the harassment record she would have needed.
#
# So both boundaries are required, and "fees", "harassment", "depression", "results" and
# the rest are listed explicitly. A word list is longer than a stem list; it is also
# checkable, and this is not a place where a cleverer rule is worth the risk.
#
# Compiled once at import: rebuilding ~150 patterns per request would be pointless work
# on the one path a student is waiting on.
_TERM_PATTERNS: dict[str, tuple[tuple[str, re.Pattern[str]], ...]] = {
    key: tuple((term, re.compile(rf"\b{re.escape(term)}\b")) for term in terms)
    for key, terms in KEYWORDS.items()
}


@dataclass(frozen=True)
class Route_:
    """Result of routing. `confidence` is deliberately coarse: low / medium / high."""

    problem_key: Optional[str]
    confidence: str
    method: str
    alternatives: list[str]

    @property
    def matched(self) -> bool:
        return self.problem_key is not None

    @property
    def confident(self) -> bool:
        return self.confidence in ("medium", "high")


def _normalise(text: str) -> str:
    return " ".join(text.lower().split())


def route_by_keywords(text: str, allowed: list[str]) -> Route_:
    """Score every allowed key by keyword hits and take the best.

    Returns no match rather than a weak guess when nothing scores. Saying "I am not sure
    which of these you mean" and showing the list is a better answer than a confident
    wrong route to the wrong office.
    """
    haystack = _normalise(text)
    if not haystack:
        return Route_(None, "low", "keywords", [])

    scores: dict[str, int] = {}
    for key in allowed:
        # A match is worth 1 plus its word count, so a two-word phrase ("financial aid")
        # outranks a single word ("doctor"), and a key matching several terms outranks a
        # key matching one. The thresholds below are calibrated against that scale:
        #
        #     single word        2   -> medium, on its own
        #     two-word phrase    3   -> medium
        #     three-word phrase  4   -> medium
        #     several terms      5+  -> high
        #
        # An earlier version scored a single word as 1 against a medium threshold of 2, so
        # "I need a doctor" matched nothing at all. The fix raised the score to 2 but also
        # raised the threshold to 3, which left it failing -- the scale and the thresholds
        # have to be set together, which is what this comment is here to prevent.
        score = sum(
            1 + len(term.split())
            for term, pattern in _TERM_PATTERNS.get(key, ())
            if pattern.search(haystack)
        )
        if score:
            scores[key] = score

    if not scores:
        return Route_(None, "low", "keywords", [])

    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    best_key, best_score = ranked[0]
    alternatives = [k for k, _ in ranked[1:3]]

    if best_score >= 5:
        confidence = "high"
    elif best_score >= 2:
        confidence = "medium"
    else:
        confidence = "low"

    if confidence == "low":
        return Route_(None, "low", "keywords", [best_key, *alternatives])

    return Route_(best_key, confidence, "keywords", alternatives)


def is_urgent(text: str) -> bool:
    haystack = _normalise(text)
    return any(marker in haystack for marker in URGENT_MARKERS)


def route(text: str, allowed: list[str]) -> Route_:
    """Route a problem description to one key from `allowed`.

    `allowed` is the set of keys that actually exist at the selected location, so the
    router can never return a key with no record behind it.
    """
    if not text or not text.strip() or not allowed:
        return Route_(None, "low", "none", [])
    return route_by_keywords(text, allowed)
