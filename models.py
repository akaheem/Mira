"""Domain models for Mira.

Plain dataclasses rather than pydantic: the schema is small and fixed, pydantic adds a
version-compatibility surface we do not need, and these are converted straight into
template context.

Design notes:
  * Every record carries its own country/city/campus. That is what makes the product
    location-aware without any schema change -- a new location is new rows, not new code.

  * `provenance` is an EXPLICIT field, not something derived from whether a source URL
    happens to be present. The absence of a source does not tell us WHY it is absent, and
    those reasons are not equivalent:

        verified      a real-world claim, and the cited source supports THIS claim
        illustrative  deliberately fictional demo data -- not a real-world claim at all
        unverified    a real-world claim we do not yet have adequate evidence for

    Deriving state from `source_url` collapsed "fictional" and "unsourced" into one label,
    which invited exactly the wrong question: did they invent this, or just not check it?

  * `jurisdiction` is separate from `provenance`, deliberately. A verified Pakistani legal
    process must never read as a universal rule for students worldwide. Provenance answers
    "how sure are we"; jurisdiction answers "where does this apply".

  * `source_url` and friends remain as the CITATION. They are no longer the state.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

# The fixed category vocabulary. Locations supply records; they never extend this list,
# because a free-form vocabulary would not survive translation across countries.
RESOURCE_CATEGORIES: dict[str, str] = {
    "menstrual_support": "Menstrual products",
    "womens_facilities": "Women's washroom",
    "drinking_water": "Drinking water",
    "first_aid": "First aid",
    "food_support": "Food support",
    "health_services": "Health services",
    "study_space": "Quiet study space",
    "support_desk": "Someone to talk to",
}

# How each category is presented on the "what do you need" screen.
CATEGORY_ICONS: dict[str, str] = {
    "menstrual_support": "\U0001fa78",  # drop of blood
    "womens_facilities": "\U0001f6ba",  # women's symbol
    "drinking_water": "\U0001f4a7",  # droplet
    "first_aid": "\U0001fa79",  # adhesive bandage
    "food_support": "\U0001f35b",  # curry rice
    "health_services": "\U0001f3e5",  # hospital
    "study_space": "\U0001f4da",  # books
    "support_desk": "\U0001f4ac",  # speech balloon
}


# --------------------------------------------------------------------------------------
# Provenance -- the trust vocabulary
# --------------------------------------------------------------------------------------

VERIFIED = "verified"
ILLUSTRATIVE = "illustrative"
UNVERIFIED = "unverified"

PROVENANCE_STATES: tuple[str, ...] = (VERIFIED, ILLUSTRATIVE, UNVERIFIED)

PROVENANCE_LABELS: dict[str, str] = {
    VERIFIED: "Verified",
    ILLUSTRATIVE: "Illustrative",
    UNVERIFIED: "Not yet verified",
}

# Markers are distinct GLYPHS, not colours. The three states must be distinguishable
# without relying on colour perception.
PROVENANCE_MARKERS: dict[str, str] = {
    VERIFIED: "✓",  # check
    ILLUSTRATIVE: "◇",  # open diamond
    UNVERIFIED: "!",
}

PROVENANCE_HINTS: dict[str, str] = {
    VERIFIED: "",
    ILLUSTRATIVE: "Demo resource for a fictional campus. Not a real-world fact.",
    UNVERIFIED: "Mira has not established a source for this. Confirm before relying on it.",
}

# One-line meanings, for the trust strip on the home page.
#
# Deliberately separate from PROVENANCE_HINTS above. A hint explains the state of one
# *particular card*, and is empty for verified because "Verified" sitting next to a source
# link is already self-explanatory there. The home page strip is doing the opposite job:
# teaching the vocabulary to someone who has not seen a card yet, so it needs the
# definition rather than the caveat. The illustrative wording is kept identical to the
# hint, since both are stating the same fact.
PROVENANCE_MEANINGS: dict[str, str] = {
    VERIFIED: "A source supports this exact claim, in this jurisdiction.",
    ILLUSTRATIVE: "Demo resource for a fictional campus. Not a real-world fact.",
    UNVERIFIED: "No source yet — confirm before relying on it.",
}

# Fare confidence. Fares are the one part of Flow A we cannot reliably cite, so rather
# than implying a precision we do not have, we label the confidence -- and omit the
# figure entirely when we cannot characterise it at all.
FARE_VERIFIED = "verified"
FARE_ESTIMATED = "estimated"
FARE_USER_REPORTED = "user_reported"
FARE_UNKNOWN = "unknown"

FARE_CONFIDENCE_LABELS: dict[str, str] = {
    FARE_VERIFIED: "Fare verified",
    FARE_ESTIMATED: "Estimated fare",
    FARE_USER_REPORTED: "User-reported fare",
    FARE_UNKNOWN: "",
}

FARE_CONFIDENCE_NOTES: dict[str, str] = {
    FARE_VERIFIED: "",
    FARE_ESTIMATED: "Confirm before travel.",
    FARE_USER_REPORTED: "Reported by students, not officially confirmed. Confirm before travel.",
    FARE_UNKNOWN: "",
}


def slugify(*parts: str) -> str:
    """Normalise a location triple into a URL-safe slug.

    Defined here, next to Location, so there is exactly one implementation. The URL a
    link points at and the lookup that resolves it must agree, and a second copy of this
    rule living in a template or a route is precisely how location switching breaks
    silently -- the link keeps rendering, and 404s, or worse, redirects to the wrong place.
    """
    raw = "-".join(parts).lower()
    return re.sub(r"[^a-z0-9]+", "-", raw).strip("-")


# --------------------------------------------------------------------------------------
# Shared building blocks
# --------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Source:
    """A citation. `name` is what a student sees; the URL is where it came from."""

    name: str
    url: str = ""
    date: str = ""


@dataclass(frozen=True)
class Condition:
    """A curated, sourced transport condition.

    Deliberately NOT crowdsourced. User-submitted reports would imply storage, moderation,
    abuse handling and staleness management -- a different product with different privacy
    consequences. These are conditions Mira has a source for.
    """

    text: str
    source_name: str = ""
    provenance: str = UNVERIFIED

    @property
    def verified(self) -> bool:
        return self.provenance == VERIFIED and bool(self.source_name)


@dataclass(frozen=True)
class SupportOption:
    """One of several parallel routes for the same problem.

    Exists because some processes genuinely offer a choice. Under the Pakistani harassment
    statute a complainant may file with the institution's Inquiry Committee OR directly
    with the Ombudsperson. Flattening those into one numbered list would misrepresent the
    law, and collapsing their different deadlines into a single "appeal by" date would be
    straightforwardly wrong -- Section 6's 30 days (appeal from a Competent Authority to
    the Ombudsperson) and Section 9's 30 days (representation against an Ombudsperson
    decision to the President or Governor) are different steps with different actors.
    """

    name: str
    summary: str = ""
    filed_with: str = ""
    steps: list[str] = field(default_factory=list)
    timeline: str = ""
    documents: list[str] = field(default_factory=list)


def _as_conditions(value) -> tuple[Condition, ...]:
    return tuple(c if isinstance(c, Condition) else Condition(**c) for c in (value or ()))


def _as_options(value) -> tuple[SupportOption, ...]:
    return tuple(o if isinstance(o, SupportOption) else SupportOption(**o) for o in (value or ()))


def _as_sources(value) -> tuple[Source, ...]:
    return tuple(s if isinstance(s, Source) else Source(**s) for s in (value or ()))


# --------------------------------------------------------------------------------------
# Entities
# --------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Location:
    """A place Mira knows about. Derived from the records themselves."""

    country: str
    city: str
    campus: str

    @property
    def id(self) -> str:
        return f"{self.country}|{self.city}|{self.campus}"

    @property
    def slug(self) -> str:
        """The URL form of this location. Templates use this and never build their own."""
        return slugify(self.country, self.city, self.campus)

    @property
    def label(self) -> str:
        return f"{self.campus}, {self.city}"


class _Provenanced:
    """Mixin for the three-state trust vocabulary.

    `verified` is deliberately CONJUNCTIVE: it requires both the declared state AND a real
    citation. A record marked `verified` with no source is a data error, and the safe
    direction to fail is toward under-claiming -- never over-claiming. `data_warnings()`
    in the repository surfaces these rather than letting them pass unnoticed.
    """

    provenance: str
    source_url: Optional[str]
    source_name: str

    @property
    def provenance_state(self) -> str:
        """The state that is actually DISPLAYED, which is not always the declared one.

        A record declaring `verified` with no citation is a data error. It renders as
        unverified, because the safe direction to fail is toward under-claiming -- never
        over-claiming. Every label, marker and hint below keys off this rather than off
        the raw field, so there is no path by which an unsourced record shows a tick.
        """
        if self.provenance == VERIFIED and not self.source_url:
            return UNVERIFIED
        if self.provenance not in PROVENANCE_STATES:
            return UNVERIFIED
        return self.provenance

    @property
    def verified(self) -> bool:
        return self.provenance_state == VERIFIED

    @property
    def provenance_label(self) -> str:
        return PROVENANCE_LABELS.get(self.provenance_state, self.provenance_state)

    @property
    def provenance_marker(self) -> str:
        return PROVENANCE_MARKERS.get(self.provenance_state, "")

    @property
    def provenance_hint(self) -> str:
        return PROVENANCE_HINTS.get(self.provenance_state, "")

    @property
    def is_illustrative(self) -> bool:
        return self.provenance_state == ILLUSTRATIVE

    @property
    def source_label(self) -> str:
        """What to call the citation in the UI. Prefer a name over a bare URL."""
        return self.source_name or self.source_url or ""


@dataclass(frozen=True)
class Resource(_Provenanced):
    """A physical thing a student might need: Flow B."""

    id: str
    name: str
    category: str
    country: str
    city: str
    campus: str
    building: str = ""
    landmark: str = ""
    hours: str = ""
    price: str = ""
    women_only: bool = False
    wheelchair_accessible: bool = False
    last_verified: str = ""
    source_url: Optional[str] = None
    source_name: str = ""
    source_date: str = ""
    additional_sources: list[Source] = field(default_factory=list)
    provenance: str = UNVERIFIED
    jurisdiction: str = ""
    notes: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "additional_sources", _as_sources(self.additional_sources))

    @property
    def category_label(self) -> str:
        return RESOURCE_CATEGORIES.get(self.category, self.category)

    @property
    def icon(self) -> str:
        return CATEGORY_ICONS.get(self.category, "\U0001f4cd")

    @property
    def stale_days(self) -> Optional[int]:
        """Days since last verification, or None if we cannot tell."""
        if not self.last_verified:
            return None
        try:
            checked = date.fromisoformat(self.last_verified)
        except ValueError:
            return None
        return (date.today() - checked).days

    @property
    def is_stale(self) -> bool:
        """Silently rotting data is the failure mode of every directory. Surface it."""
        days = self.stale_days
        return days is not None and days > STALE_AFTER_DAYS

    @property
    def open_now(self) -> Optional[bool]:
        """None means 'we do not know' -- which is different from 'closed'."""
        return _hours_contain_now(self.hours)


@dataclass(frozen=True)
class SupportProcess(_Provenanced):
    """How to get help with a problem: Flow C.

    `jurisdiction` and `jurisdiction_note` exist because process is the part that genuinely
    differs between countries -- and because a jurisdiction-specific rule presented without
    its jurisdiction reads as a universal one. `source_url` and `source_name` are required
    in spirit: the whole value of this flow is that the answer is verifiable rather than
    generated.

    `options` carries parallel routes where the law offers a genuine choice. When it is
    populated the card renders the routes instead of the flat `steps`.
    """

    id: str
    problem_key: str
    display_name: str
    country: str
    city: str
    campus: str
    office_name: str = ""
    office_contact: str = ""
    documents: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
    timeline: str = ""
    options: list[SupportOption] = field(default_factory=list)
    choice_note: str = ""
    jurisdiction: str = ""
    jurisdiction_note: str = ""
    source_url: Optional[str] = None
    source_name: str = ""
    source_date: str = ""
    additional_sources: list[Source] = field(default_factory=list)
    provenance: str = UNVERIFIED

    def __post_init__(self) -> None:
        object.__setattr__(self, "options", _as_options(self.options))
        object.__setattr__(self, "additional_sources", _as_sources(self.additional_sources))


@dataclass(frozen=True)
class Route(_Provenanced):
    """Getting to or from campus: Flow A.

    Deliberately stores *properties* -- fare range and how confident we are in it,
    transfers, final walk distance, whether women's transport runs at that hour. It never
    stores or computes a safety score. See the honesty constraint: we present verifiable
    properties and let her judge, because we cannot verify safety and she knows her own
    context better than we do.
    """

    id: str
    country: str
    city: str
    campus: str
    from_area: str
    modes: list[str] = field(default_factory=list)
    fare_min: float = 0.0
    fare_max: float = 0.0
    currency: str = ""
    fare_confidence: str = FARE_UNKNOWN
    # Explicit, because 0/0 is ambiguous between "free" and "we do not know". See is_free.
    fare_is_free: bool = False
    duration_min: int = 0
    duration_max: int = 0
    transfers: int = 0
    womens_transport: bool = False
    womens_hours: str = ""
    final_walk_m: int = 0
    entry_point: str = ""
    last_departure: str = ""
    conditions: list[Condition] = field(default_factory=list)
    note: str = ""
    source_url: Optional[str] = None
    source_name: str = ""
    source_date: str = ""
    additional_sources: list[Source] = field(default_factory=list)
    provenance: str = UNVERIFIED
    jurisdiction: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "conditions", _as_conditions(self.conditions))
        object.__setattr__(self, "additional_sources", _as_sources(self.additional_sources))

    @property
    def is_free(self) -> bool:
        """Whether the fare is *stated* to be zero, as an explicit data field.

        This is deliberately NOT derived from `fare_min == fare_max == 0`. Two records in
        the demo data both hold 0/0, and they mean opposite things:

            pk-lhr-r03  a university shuttle that is genuinely free
            pk-lhr-r02  a rickshaw whose fare we could not establish

        Deriving the answer from the numbers made those indistinguishable, so the app
        announced a *free rickshaw* -- and a student who believed it would board expecting
        no charge. It is the same mistake as deriving provenance from the presence of a
        source URL (see PROJECT_TRACKER.md D11): absence and a stated zero are different
        facts, and collapsing them inverts the meaning.

        So "free" is a claim Mira either makes or does not, held in the data.
        """
        return self.fare_is_free

    @property
    def show_fare(self) -> bool:
        """Whether to display a fare at all.

        When we cannot characterise our confidence, we omit the figure rather than present
        a number whose standing we cannot describe. An absent fare is honest; a bare
        number with no provenance is not.

        A free route is a different case and must not be swallowed by that rule: "Free" is
        a fact we either state or do not, not an estimate, so it does not depend on
        fare_confidence.
        """
        if self.is_free:
            return True
        if self.fare_confidence == FARE_UNKNOWN:
            return False
        return bool(self.fare_min or self.fare_max)

    @property
    def fare_label(self) -> str:
        if not self.show_fare:
            return ""
        if self.is_free:
            return "Free"
        if self.fare_min == self.fare_max:
            return f"{self.currency} {self.fare_min:g}"
        return f"{self.currency} {self.fare_min:g}–{self.fare_max:g}"

    @property
    def fare_confidence_label(self) -> str:
        if self.is_free:
            return ""  # labelling "Free" as an estimate would only muddy it
        return FARE_CONFIDENCE_LABELS.get(self.fare_confidence, "")

    @property
    def fare_note(self) -> str:
        return FARE_CONFIDENCE_NOTES.get(self.fare_confidence, "")

    @property
    def duration_label(self) -> str:
        if not self.duration_min and not self.duration_max:
            return "unknown"
        if self.duration_min == self.duration_max:
            return f"{self.duration_min} min"
        return f"{self.duration_min}–{self.duration_max} min"

    @property
    def arrives_after_dark(self) -> Optional[bool]:
        """Whether the last departure lands after dark. Computed, not stored."""
        return _last_departure_after_dark(self.last_departure)


# --------------------------------------------------------------------------------------
# Derived properties
# --------------------------------------------------------------------------------------

# A directory rots quietly. Past this many days we say so on the card rather than
# presenting a stale fact with the same confidence as a fresh one.
STALE_AFTER_DAYS = 90

# Dark window. The upper bound is the important one: a night bus departing at 03:00 is
# obviously after dark, and a bare `>= 18:30` test reported it as daylight. That is a
# factual error of exactly the kind the honesty model cannot afford.
DARK_START_MINUTES = 18 * 60 + 30  # 18:30
DARK_END_MINUTES = 6 * 60  # 06:00, exclusive -- 06:00 is dawn, not night


def _parse_hhmm(value: str) -> Optional[tuple[int, int]]:
    """Parse 'HH:MM' or 'HH:MM-HH:MM' start. Returns (hour, minute) or None."""
    if not value:
        return None
    start = value.split("-")[0].strip()
    parts = start.split(":")
    if len(parts) != 2:
        return None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


def _hours_contain_now(spec: str) -> Optional[bool]:
    """Is `now` inside the 'HH:MM-HH:MM' window? None if the spec is unparseable.

    Returns None rather than False when we cannot tell, because 'closed' and 'unknown'
    are different claims and the UI must not conflate them.
    """
    if not spec or "-" not in spec:
        return None
    try:
        start_s, end_s = spec.split("-", 1)
        sh, sm = (int(x) for x in start_s.strip().split(":"))
        eh, em = (int(x) for x in end_s.strip().split(":"))
    except (ValueError, TypeError):
        return None

    now = datetime.now()
    minutes_now = now.hour * 60 + now.minute
    start = sh * 60 + sm
    end = eh * 60 + em
    if end < start:  # window crosses midnight
        return minutes_now >= start or minutes_now <= end
    return start <= minutes_now <= end


def _last_departure_after_dark(spec: str) -> Optional[bool]:
    """Is the last departure inside the dark window? None if we cannot tell.

    Dark is 18:30 or later, OR before 06:00. The second half is not decoration: without
    it a 03:00 night service reports as daytime.
    """
    parsed = _parse_hhmm(spec)
    if parsed is None:
        return None
    minutes = parsed[0] * 60 + parsed[1]
    return minutes >= DARK_START_MINUTES or minutes < DARK_END_MINUTES
