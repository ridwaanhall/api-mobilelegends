from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import API_VERSION

from app.api.routers.academy import router as academy_router
from app.api.routers.mlbb import router as mlbb_router
from app.api.routers.root import router as root_router
from app.core.errors import AppError, app_error_handler, safe_error_payload, unhandled_error_handler

app = FastAPI(title="API Mobile Legends", version=API_VERSION, docs_url="/docs", redoc_url="/redoc")

app.include_router(root_router)
app.include_router(mlbb_router)
app.include_router(academy_router)

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
