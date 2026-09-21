"""The single data interface for Mira.

Nothing outside this module knows whether data comes from JSON files, Supabase, or
anything else. Swapping the backend means rewriting this file and nothing else --
that is the entire point of the abstraction.

Two Vercel-specific decisions are baked in and should not be "tidied" away:

  1. No FastAPI startup/lifespan hook loads this data. Serverless invocations are
     stateless and startup handlers do not fire reliably. `lru_cache` is the correct
     mechanism: it populates on first use per cold start and costs nothing thereafter.

  2. Files are read once per cold start, not per request. A cold start therefore pays
     one small disk read (a few KB) and every request after it is in-memory. This is
     deliberately faster than a per-request database round trip, which is why the MVP
     is file-backed rather than on Supabase.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Optional

# RESOURCE_CATEGORIES is re-exported rather than imported by callers directly, so that
# the application only ever talks to this module for data and vocabulary.
from models import (  # noqa: F401
    CATEGORY_ICONS,
    FARE_CONFIDENCE_LABELS,
    ILLUSTRATIVE,
    PROVENANCE_HINTS,
    PROVENANCE_LABELS,
    PROVENANCE_MARKERS,
    PROVENANCE_STATES,
    RESOURCE_CATEGORIES,
    STALE_AFTER_DAYS,
    UNVERIFIED,
    VERIFIED,
    Location,
    Resource,
    Route,
    SupportProcess,
    slugify,
)

DATA_DIR = Path(__file__).parent / "data"


# --------------------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------------------

def _read(name: str) -> list[dict]:
    path = DATA_DIR / name
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        payload = json.load(fh)
    if isinstance(payload, dict):  # allow {"records": [...]} or a bare list
        payload = payload.get("records", [])
    return payload if isinstance(payload, list) else []


@lru_cache(maxsize=1)
def _resources() -> tuple[Resource, ...]:
    return tuple(Resource(**row) for row in _read("resources.json"))


@lru_cache(maxsize=1)
def _support() -> tuple[SupportProcess, ...]:
    return tuple(SupportProcess(**row) for row in _read("support.json"))


@lru_cache(maxsize=1)
def _routes() -> tuple[Route, ...]:
    return tuple(Route(**row) for row in _read("transport.json"))


def clear_cache() -> None:
    """Drop the in-memory copies. Used by tests and by the admin reload path."""
    _resources.cache_clear()
    _support.cache_clear()
    _routes.cache_clear()


def data_warnings() -> list[str]:
    """Records whose declared provenance is not backed by a citation.

    A record marked `verified` with no source is a data error. The model downgrades it to
    unverified on render, which is the safe direction to fail -- but silently under-claiming
    is still a bug worth surfacing, because the record was *meant* to be verified and the
    citation is simply missing.

    This exists because the alternative is discovering it during a demo.
    """
    warnings: list[str] = []
    for record in (*_resources(), *_support(), *_routes()):
        if record.provenance not in PROVENANCE_STATES:
            warnings.append(f"{record.id}: unknown provenance {record.provenance!r}")
        elif record.provenance == VERIFIED and not record.source_url:
            warnings.append(f"{record.id}: provenance=verified but no source_url")
    return warnings


def provenance_counts(slug: Optional[str] = None) -> dict[str, int]:
    """How many records sit in each provenance state, for the About page.

    Publishing these numbers is deliberate. "12 of 37 records verified" tells a reader
    exactly how much of this build they can rely on, which is more useful than a paragraph
    of reassurance.
    """
    counts = {state: 0 for state in PROVENANCE_STATES}
    for record in (*_resources(), *_support(), *_routes()):
        if _matches_slug(record, slug):
            # Displayed state, not declared state: a verified-but-unsourced record is a
            # data error, and counting it as verified would overstate exactly the number
            # this function exists to publish honestly.
            state = record.provenance_state
            counts[state] = counts.get(state, 0) + 1
    return counts


# --------------------------------------------------------------------------------------
# Locations
# --------------------------------------------------------------------------------------

def location_id(country: str, city: str, campus: str) -> str:
    """A URL-safe identifier derived from the location triple.

    Derived rather than stored so a new location needs only new data rows -- never a
    schema change or a registry edit. Delegates to models.slugify so that this and
    Location.slug can never disagree.
    """
    return slugify(country, city, campus)


@lru_cache(maxsize=1)
def get_locations() -> tuple[Location, ...]:
    """Every location present in the data, in stable order."""
    seen: dict[str, Location] = {}
    for record in (*_resources(), *_support(), *_routes()):
        loc = Location(record.country, record.city, record.campus)
        seen.setdefault(loc.id, loc)
    return tuple(sorted(seen.values(), key=lambda l: (l.country, l.city, l.campus)))


def get_location(slug: str) -> Optional[Location]:
    for loc in get_locations():
        if location_id(loc.country, loc.city, loc.campus) == slug:
            return loc
    return None


def default_location() -> Optional[Location]:
    """The first location in the data, used when no location is selected."""
    locations = get_locations()
    return locations[0] if locations else None


def _matches_slug(record, slug: Optional[str]) -> bool:
    if not slug:
        return True
    return location_id(record.country, record.city, record.campus) == slug


# --------------------------------------------------------------------------------------
# Flow B -- essentials
# --------------------------------------------------------------------------------------

def get_resources(
    slug: Optional[str] = None, category: Optional[str] = None
) -> list[Resource]:
    """Resources at a location, optionally filtered to one category.

    Sorted so that verified records come first, then the most recently verified. A
    record we cannot point a source at should never outrank one we can.
    """
    rows = [r for r in _resources() if _matches_slug(r, slug)]
    if category:
        rows = [r for r in rows if r.category == category]

    def sort_key(r: Resource):
        days = r.stale_days
        freshness = days if days is not None else 10_000
        return (not r.verified, freshness, r.name.lower())

    return sorted(rows, key=sort_key)


def count_by_category(slug: Optional[str] = None) -> dict[str, int]:
    """How many of each category exist, so the need-picker can hide empty ones."""
    counts: dict[str, int] = {}
    for record in _resources():
        if _matches_slug(record, slug):
            counts[record.category] = counts.get(record.category, 0) + 1
    return counts


# --------------------------------------------------------------------------------------
# Flow C -- support navigation
# --------------------------------------------------------------------------------------

def get_support_processes(slug: Optional[str] = None) -> list[SupportProcess]:
    rows = [p for p in _support() if _matches_slug(p, slug)]
    return sorted(rows, key=lambda p: p.display_name.lower())


def get_support_process(
    problem_key: str, slug: Optional[str] = None
) -> Optional[SupportProcess]:
    for process in _support():
        if process.problem_key == problem_key and _matches_slug(process, slug):
            return process
    return None


def problem_keys(slug: Optional[str] = None) -> list[str]:
    """The closed vocabulary a problem description can be routed to.

    This is what keeps Flow C from inventing an answer: the router picks one of these keys
    and Mira then displays the curated record behind it. It never composes a process.

    The vocabulary is scoped to the location, so the router can never return a key with no
    record behind it -- that would render an empty answer for a matched problem, which is
    worse than not matching at all.

    (An earlier version of this docstring described an LLM choosing from this list. There
    is no LLM in the application; routing is deterministic. See PROJECT_TRACKER.md D19.)
    """
    return [p.problem_key for p in get_support_processes(slug)]


# --------------------------------------------------------------------------------------
# Flow A -- journeys
# --------------------------------------------------------------------------------------

def get_routes(slug: Optional[str] = None) -> list[Route]:
    rows = [r for r in _routes() if _matches_slug(r, slug)]
    return sorted(rows, key=lambda r: (r.from_area.lower(), r.duration_min))


def get_from_areas(slug: Optional[str] = None) -> list[str]:
    seen: list[str] = []
    for route in get_routes(slug):
        if route.from_area not in seen:
            seen.append(route.from_area)
    return seen


def get_routes_from(area: str, slug: Optional[str] = None) -> list[Route]:
    return [r for r in get_routes(slug) if r.from_area == area]
