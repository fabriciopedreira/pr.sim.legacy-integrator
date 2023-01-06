from dataclasses import dataclass
from datetime import datetime

from app.domain.common.service_base import ServiceBase, try_query_except
from app.domain.legacy_query.repository import Repository
from app.domain.legacy_query.schemas import FormalizedResponse


@dataclass
class Service(ServiceBase):
    repository: Repository

    @try_query_except
    async def formalizations_by_session_data_and_product_slug(
        self, session_data: str, product_slug: str
    ) -> list[FormalizedResponse]:
        session_data_object = datetime.strptime(session_data, "%Y-%m-%d").date()

        result = await self.repository.find_formalizations_by_session_data_and_product_slug(
            session_data_object, product_slug
        )
        formalizations = list(
            map(
                lambda v: FormalizedResponse(
                    ccb_number=v.ccb_number,
                    banking_name=v.banking_name,
                    client_document=v.client_document,
                    client_name=v.client_name,
                    person_type=v.person_type,
                    slug=str(v.slug),
                    contract_date=str(v.contract_date),
                ),
                result,
            )
        )
        return self.query_result(result=formalizations)
