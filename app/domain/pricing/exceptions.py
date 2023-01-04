from starlette import status

from app.domain.common.exception_base import APIException


class NotFoundException(APIException):
    def __init__(self, model: str = ""):
        detail = f"{model} not found"
        super().__init__(status.HTTP_404_NOT_FOUND, detail, severity=20)
