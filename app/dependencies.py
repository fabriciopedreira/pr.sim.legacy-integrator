from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request

from app.database import SessionLocal
from app.domain.common.exception_base import AnauthorizedException
from app.internal.keycloak.auth import Auth
from app.internal.utils import latency


def get_session_db() -> SessionLocal:
    """Get database session.
    Returns:
        - SessionLocal
    """
    session_local = SessionLocal()
    try:
        yield session_local
    finally:
        session_local.close()


auth_scheme = HTTPBearer()


@latency
async def access_validation(
    _request: Request, authorization: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> None:
    """Validate token via SSO
    :param _request: Request
    :param authorization: HTTPAuthorizationCredentials

    :return None
    :raise HTTPException
    """
    if not await Auth().token_validation(token=authorization.credentials):
        raise AnauthorizedException(stacktrace=["access_validation"], kid=Auth.get_kid(authorization.credentials))
