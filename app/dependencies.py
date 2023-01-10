from typing import Callable, Generator, Type

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.database import SessionLocal
from app.domain.common.exception_base import UnauthorizedException
from app.domain.common.repository_base import RepositoryBase
from app.internal.keycloak.auth import Auth
from app.internal.utils import latency


def get_session_db() -> Generator:
    session_local = SessionLocal()
    try:
        yield session_local
    finally:
        session_local.close()


def get_repository(repo_type: Type[RepositoryBase]) -> Callable[[Session], RepositoryBase]:
    def __get_repo(session_db: Session = Depends(get_session_db)) -> RepositoryBase:
        return repo_type(session=session_db)

    return __get_repo


@latency
async def access_validation(
    _request: Request, authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> None:
    if not await Auth().token_validation(token=authorization.credentials):
        raise UnauthorizedException(stacktrace=["access_validation"], kid=Auth.get_kid(authorization.credentials))
