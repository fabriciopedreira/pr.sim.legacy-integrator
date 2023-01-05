from dataclasses import dataclass
from typing import Any, Type

from pydantic import BaseModel

from app.domain.legacy_query.exceptions import NotFoundException


@dataclass
class ServiceBase:
    @classmethod
    def query_result(cls, result: list[Any] | dict[str, Any] | Type[BaseModel]) -> Any:
        """return result of query
        :param: result: any query result
        :param: model_name: name of the model used in the query

        :return: result
        :raise: NotFoundException
        """
        if result:
            return result

        raise NotFoundException()
