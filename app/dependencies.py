from typing import Callable, Generator, Type

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.database import SessionLocal
from app.domain.common.exception_base import AnauthorizedException
from app.domain.common.repository_base import RepositoryBase
from app.internal.keycloak.auth import Auth
from app.internal.utils import latency


def get_session_db() -> Generator:
    """Get database session.
    Returns:
        - SessionLocal
    """
    session_local = SessionLocal()
    try:
        yield session_local
    finally:
        session_local.close()


def get_repository(repo_type: Type[RepositoryBase]) -> Callable[[Session], RepositoryBase]:
    """Get repository
    :param: repo_type: Type of repository

    :return: Repository
    """

    def __get_repo(session_db: Session = Depends(get_session_db)) -> RepositoryBase:
        return repo_type(session=session_db)

    return __get_repo


@latency
async def access_validation(
    _request: Request, authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> None:
    """Validate token via SSO
    :param _request: Request
    :param authorization: HTTPAuthorizationCredentials

    :return None
    :raise HTTPException
    """
    if not await Auth().token_validation(token=authorization.credentials):
        raise AnauthorizedException(stacktrace=["access_validation"], kid=Auth.get_kid(authorization.credentials))
