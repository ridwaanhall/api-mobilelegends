from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

from app.core.config import DEBUG, API_VERSION
from app.core.docs import build_swagger_ui_html, swagger_auth_script


from app.api.routers.root import router as root_router
from app.api.routers.mlbb import router as mlbb_router
from app.api.routers.academy import router as academy_router
from app.api.routers.addon import router as addon_router
from app.api.routers.user import router as user_router

from app.core.errors import AppError, app_error_handler, safe_error_payload, unhandled_error_handler

app = FastAPI(
    debug=DEBUG,
    title="MLBB Public Data API",

    summary="Public API for Mobile Legends: Bang Bang providing hero data, analytics, academy resources, user endpoints, and utility tools.",

    description=(
        "MLBB Public Data API is a comprehensive public API for Mobile Legends: Bang Bang, built for developers, analysts, and fans who need structured and reliable game data. "
        "It provides access to hero information including listings, rankings, positions, detailed statistics, performance trends, skill combos, counters, compatibility, and hero relationships. "
        "In addition, the API includes academy resources such as roles, equipment, emblems, spells, builds, lane distribution, win rate timelines, and performance ratings to support deeper analysis and game understanding. "
        "User-related endpoints are available for authentication, profile data, match history, and player statistics, while utility tools such as win rate calculators and IP lookup enhance integration capabilities. "
        "The API is designed with a consistent and RESTful structure, supports flexible hero identifiers using either ID or name, and delivers standardized responses optimized for seamless integration into applications, dashboards, and analytics systems."
    ),

    version=API_VERSION,

    docs_url=None,
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",

    contact={
        "name": "RoneAI",
        "url": "https://rone.dev/#Contact",
        "email": "founder@rone.dev",
    },

    license_info={
        "name": "BSD 3-Clause License",
        "url": "https://github.com/ridwaanhall/api-mobilelegends/blob/main/LICENSE",
    },

    openapi_tags=[
        {
            "name": "root",
            "description": "API status, index, and crawler-related files.",
        },
        {
            "name": "mlbb",
            "description": "Hero data, stats, and in-game analytics.",
        },
        {
            "name": "academy",
            "description": "Game guides, builds, and reference data.",
        },
        {
            "name": "user",
            "description": "Authentication and player-related data.",
        },
        {
            "name": "addon",
            "description": "Utility tools and extra features.",
        },
    ]
)

# api routers
app.include_router(root_router)
app.include_router(mlbb_router)
app.include_router(academy_router)
app.include_router(user_router)
app.include_router(addon_router)

# web routes


@app.get("/api/docs", include_in_schema=False)
def custom_swagger_ui_html() -> HTMLResponse:
    return build_swagger_ui_html(
        openapi_url=app.openapi_url or "/api/openapi.json",
        title=f"{app.title} - Swagger UI",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get("/api/docs/auth.js", include_in_schema=False)
def swagger_auth_js() -> PlainTextResponse:
    return PlainTextResponse(swagger_auth_script(), media_type="application/javascript")


# exception handlers
app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(Exception, unhandled_error_handler)  # type: ignore[arg-type]


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException) -> JSONResponse:
    payload = safe_error_payload(str(exc.detail), exc.status_code)
    return JSONResponse(status_code=exc.status_code, content=payload)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError) -> JSONResponse:
    payload = safe_error_payload("Validation failed.", 422, exc.errors())
    payload["code"] = "VALIDATION_ERROR"
    return JSONResponse(status_code=422, content=payload)
