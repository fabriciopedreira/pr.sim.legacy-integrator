import traceback
from dataclasses import dataclass
from datetime import datetime

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.domain.common.exception_base import SQLAlchemyException, ValidationException
from app.domain.common.service_base import ServiceBase
from app.domain.legacy_query.repository import Repository
from app.domain.legacy_query.schemas import FormalizedFinancingResponse
from app.internal.utils import exc_info


@dataclass
class Service(ServiceBase):
    repository: Repository

    async def formalizations_by_session_data_and_product_slug(
        self, session_data: str, product_slug: str
    ) -> list[FormalizedFinancingResponse]:
        """Find formalizations by session_data and financial_product_slug
        :param session_data: Data from session
        :param product_slug: Slug from financing-product

        :return: list of FormalizedFinancingResponse
        :raises: NotFoundException or SQLAlchemyError
        """
        try:
            session_data_object = datetime.strptime(session_data, "%Y-%m-%d").date()

            result = await self.repository.find_formalizations_by_session_data_and_product_slug(
                session_data_object, product_slug
            )

            formalizations = list(
                map(
                    lambda v: FormalizedFinancingResponse(
                        ccb_number=v.numero_ccb,  # type: ignore
                        client_cpf=v.cpf,  # type: ignore
                        client_name=v.nome_completo,  # type: ignore
                        person_type=v.tipo,  # type: ignore
                        contract_date=str(v.created_at),  # type: ignore
                    ),
                    result,
                )
            )
            return self.query_result(result=formalizations)
        except SQLAlchemyError as exc:
            raise SQLAlchemyException(stacktrace=traceback.format_exception_only(*exc_info())) from exc
        except ValidationError as exc:
            raise ValidationException(stacktrace=traceback.format_exception_only(*exc_info())) from exc
