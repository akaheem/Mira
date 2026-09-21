"""Mira -- Your Student Support Companion.

Find what you need. Know what to do. Get where you need to go.

FastAPI application. Deployed to Vercel as a Python function, so two rules apply
throughout and should not be undone:

  * Nothing loads data in a startup/lifespan hook. Serverless invocations are stateless
    and startup handlers do not fire reliably -- `repository` uses lru_cache instead.
  * Nothing runs long. The Hobby plan caps a request at 10 seconds, so every route here
    is a short query against in-memory data.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import repository as repo
import routing

BASE_DIR = Path(__file__).parent

app = FastAPI(title="Mira", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

LOCATION_COOKIE = "mira_location"


# --------------------------------------------------------------------------------------
# Location handling
# --------------------------------------------------------------------------------------

def current_location(request: Request):
    """The selected location, from a cookie, validated against the data.

    Falls back to the first location present. A cookie naming a location that no longer
    exists must not 500 the app -- it just falls back.
    """
    slug = request.cookies.get(LOCATION_COOKIE)
    if slug:
        found = repo.get_location(slug)
        if found:
            return found
    return repo.default_location()


def location_slug(request: Request) -> Optional[str]:
    loc = current_location(request)
    return repo.location_id(loc.country, loc.city, loc.campus) if loc else None


def _has_illustrative(slug: Optional[str]) -> bool:
    """True when this location contains deliberately fictional records.

    Drives the demo-environment banner. This is not decoration: it is the mechanism that
    stops fictional campus data from being read as a description of a real place.

    Replaces an earlier heuristic that asked "does any record here have a source?" and
    answered badly in both directions -- one sourced record in a mostly-unsourced dataset
    suppressed the banner entirely, while a fully-unsourced set showed it. Whether data is
    fictional is a property of the data, so it is now a field, not an inference.
    """
    return bool(repo.provenance_counts(slug).get(repo.ILLUSTRATIVE, 0))


def base_context(request: Request, **extra) -> dict:
    loc = current_location(request)
    slug = repo.location_id(loc.country, loc.city, loc.campus) if loc else None
    return {
        "request": request,
        "location": loc,
        "location_slug": slug,
        "locations": repo.get_locations(),
        "is_demo": _has_illustrative(slug),
        **extra,
    }


@app.get("/set-location/{slug}")
def set_location(slug: str, request: Request):
    target = repo.get_location(slug)
    response = RedirectResponse(url=str(request.query_params.get("next", "/")), status_code=303)
    if target:
        response.set_cookie(
            LOCATION_COOKIE, slug, max_age=60 * 60 * 24 * 180, httponly=True, samesite="lax"
        )
    return response


# --------------------------------------------------------------------------------------
# Home
# --------------------------------------------------------------------------------------

@app.get("/")
def home(request: Request):
    slug = location_slug(request)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=base_context(
            request,
            counts=repo.count_by_category(slug),
            resource_count=len(repo.get_resources(slug)),
            support_count=len(repo.get_support_processes(slug)),
            area_count=len(repo.get_from_areas(slug)),
        ),
    )


# --------------------------------------------------------------------------------------
# Flow B -- I need something
# --------------------------------------------------------------------------------------

@app.get("/needs")
def needs(request: Request):
    slug = location_slug(request)
    counts = repo.count_by_category(slug)

    # Tiles are prepared here rather than assembled in Jinja. The template should render
    # a list it is given, not decide what the vocabulary is or how a category is drawn.
    tiles = [
        {
            "key": key,
            "label": label,
            "icon": repo.CATEGORY_ICONS.get(key, "\U0001f4cd"),
            "count": counts.get(key, 0),
        }
        for key, label in repo.RESOURCE_CATEGORIES.items()
    ]

    return templates.TemplateResponse(
        request=request,
        name="needs.html",
        context=base_context(
            request,
            tiles=[t for t in tiles if t["count"]],
            gaps=[t["label"] for t in tiles if not t["count"]],
        ),
    )


@app.get("/needs/{category}")
def needs_results(category: str, request: Request):
    slug = location_slug(request)
    label = repo.RESOURCE_CATEGORIES.get(category, category)
    return templates.TemplateResponse(
        request=request,
        name="needs_results.html",
        context=base_context(
            request,
            category=category,
            category_label=label,
            results=repo.get_resources(slug, category),
        ),
    )


# --------------------------------------------------------------------------------------
# Flow C -- I need help
# --------------------------------------------------------------------------------------

@app.get("/help")
def help_form(request: Request):
    """The problem-description form.

    Deliberately takes no `problem` parameter. One used to be accepted as a query string
    so the box could be re-populated, and it quietly undid the whole point of submitting
    by POST: `GET /help?problem=...` puts the text in the address bar, the browser history,
    any proxy log, and the `Referer` header of every subsequent request -- and the server's
    own access log, which was confirmed by running one. FastAPI ignores the parameter now,
    so a crafted URL carries nothing.

    Nothing is lost: the only path that needs to echo the text back is the no-match branch
    of `help_submit`, and that renders straight from the POST body without a redirect.
    """
    slug = location_slug(request)
    return templates.TemplateResponse(
        request=request,
        name="help.html",
        context=base_context(
            request,
            processes=repo.get_support_processes(slug),
            submitted=None,
        ),
    )


@app.post("/help")
def help_submit(request: Request, problem: str = Form(...)):
    """Route a free-text problem.

    POST rather than GET on purpose: a problem description in a query string ends up in
    browser history, server logs, and any proxy in between. For a harassment concern that
    is unacceptable.

    Privacy is stated only as far as the implementation supports it. Mira requires no
    account, and the submitted text is used to select a topic and then discarded: it is
    not written to any store Mira controls, and this application never puts it in a log
    line, an analytics event, or a model request (routing is deterministic).

    We deliberately do NOT claim "nothing is stored". The platform this runs on keeps its
    own request logs, which we do not control. The About page states exactly what happens,
    technically, rather than making a broader promise than the system can keep.
    """
    slug = location_slug(request)
    text = (problem or "").strip()
    allowed = repo.problem_keys(slug)
    result = routing.route(text, allowed)

    if not result.matched:
        return templates.TemplateResponse(
            request=request,
            name="help.html",
            context=base_context(
                request,
                processes=repo.get_support_processes(slug),
                submitted=text,
                unmatched=True,
                suggestions=[repo.get_support_process(k, slug) for k in result.alternatives],
                urgent=routing.is_urgent(text),
            ),
        )

    process = repo.get_support_process(result.problem_key, slug)
    return templates.TemplateResponse(
        request=request,
        name="help_result.html",
        context=base_context(
            request,
            process=process,
            confidence=result.confidence,
            method=result.method,
            submitted=text,
            urgent=routing.is_urgent(text),
        ),
    )


@app.get("/help/topic/{problem_key}")
def help_topic(problem_key: str, request: Request):
    """Direct route for a student who picks from the list instead of typing."""
    slug = location_slug(request)
    process = repo.get_support_process(problem_key, slug)
    if process is None:
        return RedirectResponse(url="/help", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="help_result.html",
        context=base_context(
            request, process=process, confidence="high", method="list", submitted=None
        ),
    )


# --------------------------------------------------------------------------------------
# Flow A -- Get me there
# --------------------------------------------------------------------------------------

@app.get("/journey")
def journey(request: Request):
    slug = location_slug(request)
    return templates.TemplateResponse(
        request=request,
        name="journey.html",
        context=base_context(request, areas=repo.get_from_areas(slug)),
    )


@app.get("/journey/plan")
def journey_plan(request: Request, area: str = ""):
    """Routes from a starting area.

    There is no `arrive_by` parameter. One was accepted and echoed into the page while
    nothing computed with it, so the form promised a "last departure that still gets you
    there in time" that the application never worked out. Mira has no timetable data -- a
    last-departure time and a duration range are not a schedule -- so the honest move is
    to not ask the question than to answer it with arithmetic that could be wrong.
    """
    slug = location_slug(request)
    routes = repo.get_routes_from(area, slug) if area else []
    return templates.TemplateResponse(
        request=request,
        name="journey_results.html",
        context=base_context(
            request, area=area, routes=routes, areas=repo.get_from_areas(slug),
        ),
    )


# --------------------------------------------------------------------------------------
# About / sources
# --------------------------------------------------------------------------------------

@app.get("/about")
def about(request: Request):
    """How Mira works, and where every fact came from.

    The provenance counts are published rather than summarised. "12 of 15 records verified"
    tells a reader exactly how much of this build they can rely on, which is more useful
    than a paragraph of reassurance -- and it is the claim we can actually substantiate.
    """
    slug = location_slug(request)
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context=base_context(
            request,
            counts=repo.provenance_counts(slug),
            warnings=repo.data_warnings(),
        ),
    )
