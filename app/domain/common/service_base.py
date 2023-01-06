import traceback
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Type

from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.domain.common.exception_base import NotFoundException, SQLAlchemyException, ValidationException
from app.internal.utils import exc_info


@dataclass
class ServiceBase:
    @classmethod
    def query_result(cls, result: list[Any] | dict[str, Any] | Type[BaseModel]) -> Any:
        if result:
            return result
        raise NotFoundException()


def try_query_except(func: Callable):
    @wraps(func)
    async def wrapped_func(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except SQLAlchemyError as exc:
            raise SQLAlchemyException(stacktrace=traceback.format_exception_only(*exc_info())) from exc
        except ValidationError as exc:
            raise ValidationException(stacktrace=traceback.format_exception_only(*exc_info())) from exc
        else:
            return result

    return wrapped_func
