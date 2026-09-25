"""Regression tests for the Flow C router.

Run directly (`python tests/test_routing.py`) or under pytest. Deliberately written
against the stdlib `assert` so that adding tests costs the deployed function no new
dependency -- `requirements.txt` is what ships to Vercel.

WHY THIS FILE EXISTS. The router was verified by running 22 queries by hand, and that
evidence is recorded in PROJECT_TRACKER.md sec 14b. A hand-run is evidence but not a
guard: nothing stopped the same regression from returning on the next edit to KEYWORDS.
Every case below is either a documented failure that was fixed, or a false match that
would send a student to the wrong office -- so each one is a bug that has already
happened once, or the near-miss that would cause it.

The two rules under test, both from `routing.py`:

  1. Terms match as WHOLE WORDS, requiring a boundary on BOTH sides.
  2. A weak score returns NO match rather than a confident wrong one.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import routing  # noqa: E402

ALLOWED = list(routing.KEYWORDS)


def routed(text: str):
    return routing.route(text, ALLOWED).problem_key


# ---------------------------------------------------------------------------------
# The regression that matters most.
#
# With a leading boundary only, `\bfee` matches "feel", so "I feel unsafe" routed to
# the FEES record -- the single worst miss available, because the harassment record is
# the one she actually needed. This is the case the router must never fail.
# ---------------------------------------------------------------------------------

FALSE_MATCHES = [
    ("I feel unsafe", "harassment_concern"),
    ("i feel really unsafe right now", "harassment_concern"),
    ("I am not feeling safe", None),          # "safe" is not in the vocabulary
    ("this is a challenge for me", None),     # "hall" inside "challenge"
    ("I sent a message", None),               # "mess" inside "message"
    ("where is the washroom", None),          # "room" inside "washroom"
]

# ---------------------------------------------------------------------------------
# Real queries. Covers the categories sec 9 names, plus the synonyms and the Roman
# Urdu terms the vocabulary carries because that is how many students actually type.
# ---------------------------------------------------------------------------------

TRUE_MATCHES = [
    # fees
    ("I cannot pay my tuition this term", "cant_pay_fees"),
    ("I can't pay my fees", "cant_pay_fees"),
    ("fees", "cant_pay_fees"),                        # single word
    ("mere paise nahi hain", "cant_pay_fees"),        # Roman Urdu
    ("I need an installment plan for my semester fee", "cant_pay_fees"),
    # scholarship
    ("I want to apply for a scholarship", "scholarship_support"),
    ("is there a wazifa I can apply for", "scholarship_support"),
    ("financial aid", "scholarship_support"),
    # harassment
    ("I want to report harassment", "harassment_concern"),
    ("someone is stalking me", "harassment_concern"),
    ("I was harassed by a senior", "harassment_concern"),
    # academic
    ("my grades are unfair", "academic_dispute"),
    ("I want a recheck of my result", "academic_dispute"),
    ("I failed and I want to appeal", "academic_dispute"),
    # health
    ("I need a doctor", "health_concern"),            # the scoring-scale regression
    ("I have been feeling depressed", "health_concern"),
    ("counselling", "health_concern"),
    ("meri sehat theek nahi", "health_concern"),      # Roman Urdu
    # hostel
    ("problem with my hostel warden", "hostel_problem"),
    ("my roommate is an issue in the dorm", "hostel_problem"),
]

# ---------------------------------------------------------------------------------
# The router must decline rather than guess, and must never return a key that does
# not exist at the selected location.
# ---------------------------------------------------------------------------------

NO_MATCH = [
    "",
    "   ",
    "hello",
    "what is the weather",
]

URGENT = [
    ("I am in danger right now", True),
    ("this is an emergency", True),
    ("I cannot pay my fees", False),
]


def test_false_matches():
    """A near-miss must never reach the wrong office."""
    for text, expected in FALSE_MATCHES:
        got = routed(text)
        assert got == expected, f"{text!r} -> {got!r}, expected {expected!r}"


def test_true_matches():
    for text, expected in TRUE_MATCHES:
        got = routed(text)
        assert got == expected, f"{text!r} -> {got!r}, expected {expected!r}"


def test_no_match_declines():
    for text in NO_MATCH:
        result = routing.route(text, ALLOWED)
        assert not result.matched, f"{text!r} matched {result.problem_key!r}, expected no match"


def test_never_returns_unavailable_key():
    """`allowed` is the location's real key set; the router may not exceed it."""
    for text, _ in TRUE_MATCHES:
        result = routing.route(text, ["hostel_problem"])
        assert result.problem_key in (None, "hostel_problem"), (
            f"{text!r} returned {result.problem_key!r}, which is not in the allowed set"
        )


def test_urgent_markers():
    for text, expected in URGENT:
        assert routing.is_urgent(text) is expected, f"{text!r} urgent != {expected}"


def main() -> int:
    failures = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_") or not callable(fn):
            continue
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as exc:
            failures += 1
            print(f"  FAIL  {name}: {exc}")

    total = len([n for n in globals() if n.startswith("test_")])
    cases = len(FALSE_MATCHES) + len(TRUE_MATCHES) + len(NO_MATCH) + len(URGENT)
    print()
    print(f"{total - failures}/{total} test functions passed ({cases} query cases)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
