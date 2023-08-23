from fastapi import FastAPI

from app.enum import BuildEnvironment
from app.internal.config import (
    MODE,
    PROJECT_CONTACT_API,
    PROJECT_DESCRIPTION_API,
    PROJECT_NAME_API,
    PROJECT_VERSION_API,
    set_up_ddtrace,
    set_up_logger,
    set_up_sentry_sdk,
)
from app.routers import financing, healthcheck, legacy_reading_query, store, user, welcome

__version__ = PROJECT_VERSION_API


def create_app() -> FastAPI:
    # Set custom logger configurations (loguru)
    set_up_logger()

    openapi_url = "/openapi.json"

    if MODE == BuildEnvironment.prd:
        # Configure ddtrace integration (Tracer)
        set_up_ddtrace()
        # Configure sentry_sdk integration (sentry_sdk)
        set_up_sentry_sdk()
        # Deny docs access in PRD environment
        openapi_url = None

    # Create web framework app
    app = FastAPI(
        title=PROJECT_DESCRIPTION_API,
        description=f"Flexible and dynamic pricing - ({PROJECT_NAME_API})",
        version=PROJECT_VERSION_API,
        contact=PROJECT_CONTACT_API,
        openapi_url=openapi_url,
    )
    app.include_router(router=welcome)
    app.include_router(router=legacy_reading_query.router, tags=["Legacy"])
    app.include_router(router=financing.financing_router, tags=["Financing"])
    app.include_router(router=user.router, tags=["User"])
    app.include_router(router=store.store_router, tags=["Store"])
    app.include_router(router=healthcheck.router, tags=["Health"])

    return app
