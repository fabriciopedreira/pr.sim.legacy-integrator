from loguru import logger

from app import create_app
from app.internal.config.gunicorn import LOG_DATA

# FastAPI application
application = create_app()


@application.on_event("startup")
async def startup_event():
    logger.info(f"[+] {LOG_DATA}")


@application.on_event("shutdown")
def shutdown_event():
    logger.info("[*] Application shutdown")
