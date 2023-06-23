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
        
        if severity == 20:  # INFO
            logger.info(log_detail)
        elif severity == 30:  # WARNING
            logger.warning(log_detail)
        elif severity == 50:  # CRITICAL
            logger.critical(log_detail)
        else:
            logger.opt(exception=True).error(log_detail)

        super().__init__(status_code, detail)


class SQLAlchemyException(APIException):
    def __init__(self, stacktrace: list):
        detail = "SQLAlchemy - error detected in the ORM or database offline"
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail, stacktrace, severity=50)

class APIError(APIException):
    def __init__(self, stacktrace: list, detail: str = "Authtentication - error detected in the authtentication process"):
        super().__init__(status.HTTP_403_FORBIDDEN, detail, stacktrace, severity=20)


class AuthenticationException(APIException):
    def __init__(self, stacktrace: list):
        detail = "Authentication - error detected in the Authentication process"
        super().__init__(status.HTTP_403_FORBIDDEN, detail, stacktrace, severity=50)


class UnauthorizedException(APIException):
    def __init__(self, stacktrace: list, kid: Optional[Any] = ""):
        detail = "Unauthorized - Invalid or expired token"

        if kid:
            detail += f" - Kid=[{kid}]"

        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, stacktrace, severity=30)

class UnprocessEntity(APIException):
    def __init__(self, stacktrace: list, detail):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail, stacktrace, severity=30)


class ValidationException(APIException):
    def __init__(self, stacktrace: list):
        detail = "Validation error - some value of the response model is not a valid type"
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail, stacktrace)


class NotFoundException(APIException):
    def __init__(self, model: str = "Values"):
        detail = f"{model} not found"
        super().__init__(status.HTTP_204_NO_CONTENT, detail, severity=20)


class InsertDBException(APIException):
    def __init__(self, stacktrace: list, message):
        detail = f"Insert or update database error {message}"
        super().__init__(status.HTTP_404_NOT_FOUND, detail, stacktrace)

class ResponseException(Exception):  
    def __init__(self, error_code, error_msg):
        self.error_code = error_code
        self.error_msg = error_msg

class ParamsException(APIException):
    def __init__(self, detail: str, model: str = "Values" ):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail, severity=20)

class ServiceBadRequestException(APIException):
    def __init__(self, stacktrace: list, detail: str = "Bad Request - error in the request"):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, stacktrace, severity=20)

class ServiceNotFoundException(APIException):
    def __init__(self, stacktrace: list):
        detail = "Not Found - resource not found"
        super().__init__(status.HTTP_404_NOT_FOUND, detail, stacktrace, severity=20)

class ServiceRequestException(APIException):
    def __init__(self, stacktrace: list, detail: str = "Bad Request - error in the request"):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, stacktrace, severity=20)

class ServiceUnauthorizedException(APIException):
    def __init__(self, stacktrace: list):
        detail = "Unauthorized - authentication credentials are missing or invalid"
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, stacktrace, severity=20)

