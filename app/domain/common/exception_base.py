from typing import Any, Optional

from fastapi import HTTPException
from loguru import logger
from starlette import status


class APIException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "Operation error",
        stacktrace=None,
        severity: int = 0
    ):
        self.status_code = status_code
        self.detail = detail
        log_detail = f"[-] {detail} - Status=[{status_code}]"

        if stacktrace:
            log_detail += f" Stacktrace=[{stacktrace}]"

        # https://loguru.readthedocs.io/en/stable/api/logger.html
        match severity:
            case 20:  # INFO
                logger.info(log_detail)
            case 30:  # WARNING
                logger.warning(log_detail)
            case 50:  # CRITICAL
                logger.critical(log_detail)
            case _:
                logger.opt(exception=True).error(log_detail)

        super().__init__(status_code, detail)


class UniqueException(APIException):
    def __init__(self, stacktrace: list):
        detail = "Unique constraint - the value already exists in the database"
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail, stacktrace, severity=30)


class SQLAlchemyException(APIException):
    def __init__(self, stacktrace: list):
        detail = "SQLAlchemy - error detected in the ORM or database"
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail, stacktrace, severity=50)


class LaunchDarklyException(APIException):
    def __init__(self, reason: dict):
        detail = "Error connecting to LaunchDarkly"

        if reason:
            detail += f" - Reason=[{reason}]"

        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)


class AuthtenticationException(APIException):
    def __init__(self, stacktrace: list):
        detail = "Authtentication - error detected in the authtentication process"
        super().__init__(status.HTTP_403_FORBIDDEN, detail, stacktrace, severity=50)


class AnauthorizedException(APIException):
    def __init__(self, stacktrace: list, kid: Optional[Any] = ""):
        detail = "Anauthorized - Invalid or expired token"

        if kid:
            detail += f" - Kid=[{kid}]"

        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, stacktrace, severity=30)


class ValidationException(APIException):
    def __init__(self, stacktrace: list):
        detail = "Validation error - some value of the response model is not a valid type"
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail, stacktrace)


class NotFoundException(APIException):
    def __init__(self, model: str = "Values"):
        detail = f"{model} not found"
        super().__init__(status.HTTP_404_NOT_FOUND, detail, severity=20)
