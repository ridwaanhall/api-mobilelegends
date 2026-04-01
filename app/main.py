from __future__ import annotations

from copy import deepcopy

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from app.core.config import DEBUG, API_VERSION


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

    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
    },

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
            "name": "user",
            "description": "Authentication and player-related data.",
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
            "name": "addon",
            "description": "Utility tools and extra features.",
        },
    ]
)

def _inline_enum_defaults_in_parameters(schema: dict[str, object]) -> None:
    components = schema.get("components", {})
    if not isinstance(components, dict):
        return

    component_schemas = components.get("schemas", {})
    if not isinstance(component_schemas, dict):
        return

    paths = schema.get("paths", {})
    if not isinstance(paths, dict):
        return

    for path_item in paths.values():
        if not isinstance(path_item, dict):
            continue

        for operation in path_item.values():
            if not isinstance(operation, dict):
                continue

            parameters = operation.get("parameters", [])
            if not isinstance(parameters, list):
                continue

            for parameter in parameters:
                if not isinstance(parameter, dict):
                    continue

                param_schema = parameter.get("schema", {})
                if not isinstance(param_schema, dict):
                    continue

                ref = param_schema.get("$ref")
                has_default = "default" in param_schema
                if not isinstance(ref, str) or not has_default:
                    continue

                prefix = "#/components/schemas/"
                if not ref.startswith(prefix):
                    continue

                component_name = ref[len(prefix):]
                component_schema = component_schemas.get(component_name, {})
                if not isinstance(component_schema, dict) or "enum" not in component_schema:
                    continue

                inlined_schema = {
                    "type": component_schema.get("type", "string"),
                    "enum": deepcopy(component_schema.get("enum", [])),
                }

                for key in ("title", "description", "default"):
                    if key in param_schema:
                        inlined_schema[key] = deepcopy(param_schema[key])

                parameter["schema"] = inlined_schema


def custom_openapi() -> dict[str, object]:
    if app.openapi_schema is not None:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        summary=app.summary,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )

    _inline_enum_defaults_in_parameters(openapi_schema)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# api routers
app.include_router(root_router)
app.include_router(mlbb_router)
app.include_router(academy_router)
app.include_router(user_router)
app.include_router(addon_router)

# web routes


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
