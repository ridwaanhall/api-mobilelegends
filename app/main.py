from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import DEBUG,  TITLE, SUMMARY, DESCRIPTION, API_VERSION, CONTACT_FORM_LINK


from app.api.routers.root import router as root_router
from app.api.routers.mlbb import router as mlbb_router
from app.api.routers.academy import router as academy_router
from app.api.routers.addon import router as addon_router
from app.api.routers.identity import router as identity_router

from app.core.errors import AppError, app_error_handler, safe_error_payload, unhandled_error_handler

app = FastAPI(
    debug=DEBUG,
    title=TITLE,
    summary=SUMMARY,
    description=DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "RoneAI Founder",
        "url": CONTACT_FORM_LINK,
        "email": "founder@rone.dev",
    },
    license_info={
        "name": "BSD 3-Clause License",
        "url": "https://github.com/ridwaanhall/api-mobilelegends/blob/main/LICENSE",
    },
    openapi_tags=[
        {
            "name": "root",
            "description": "General endpoints for API metadata, documentation, and service utilities."
        },
        {
            "name": "mlbb",
            "description": "Main endpoints for Mobile Legends: Bang Bang game data and analytics."
        },
        {
            "name": "academy",
            "description": "Endpoints for MLBB Academy resources and educational content."
        },
        {
            "name": "addon",
            "description": "Addon endpoints for supplementary tools and additional features."
        }
    ]
)

app.include_router(root_router)
app.include_router(mlbb_router)
app.include_router(academy_router)
app.include_router(identity_router)
app.include_router(addon_router)

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
