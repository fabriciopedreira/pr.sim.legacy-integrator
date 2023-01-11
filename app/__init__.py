from fastapi import FastAPI

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
from app.routers import healthcheck, legacy_reading_query, welcome

__version__ = PROJECT_VERSION_API


def create_app() -> FastAPI:
    # Set custom logger configurations (loguru)
    set_up_logger()

    if MODE == "PRD":
        # Configure ddtrace integration (Tracer)
        set_up_ddtrace()
        # Configure sentry_sdk integration (sentry_sdk)
        set_up_sentry_sdk()

    # Create web framework app
    app = FastAPI(
        title=PROJECT_DESCRIPTION_API,
        description=f"Flexible and dynamic pricing - ({PROJECT_NAME_API})",
        version=PROJECT_VERSION_API,
        contact=PROJECT_CONTACT_API,
    )
    app.include_router(router=welcome)
    app.include_router(router=legacy_reading_query.router, tags=["Legacy"])
    app.include_router(router=healthcheck.router, tags=["Health"])

    return app