import traceback

from fastapi import APIRouter, Depends
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.dependencies import get_session_db
from app.domain.common.exception_base import SQLAlchemyException
from app.internal.utils import exc_info

router = APIRouter()


@router.get("/healthcheck", summary="API is active?")
async def live(session_db: Session = Depends(get_session_db)) -> dict:
    """Check if API is Alive

    * **param**: session_db: Session from database.

    **return**: dict.
    """
    try:
        session_db.execute("SELECT 1")
    except OperationalError as err:
        raise SQLAlchemyException(stacktrace=traceback.format_exception_only(*exc_info())) from err

    return {"status": "alive"}
