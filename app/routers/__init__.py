from fastapi import APIRouter

from app.internal.config import PROJECT_DESCRIPTION_API

welcome = APIRouter()


@welcome.get("/", include_in_schema=False)
async def start_welcome():
    """Welcome to API"""
    return f"Welcome to the {PROJECT_DESCRIPTION_API}. For more information, read the documentation in /docs or /redoc"
