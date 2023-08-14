from dataclasses import dataclass
from datetime import datetime

from app.domain.common.service_base import ServiceBase, try_query_except
from app.domain.legacy_query.repository.formalized import FormalizedRepository
from app.domain.legacy_query.schemas import FormalizedFinancingResponse, FormalizedResponse


@dataclass
class FormalizedService(ServiceBase):
    repository: FormalizedRepository

    @try_query_except
    async def formalizations_by_cessao_date_and_product_slug(
        self, cessao_date: str, product_slug: str
    ) -> list[FormalizedResponse]:
        cessao_date_object = datetime.strptime(cessao_date, "%Y-%m-%d").date()

        result = await self.repository.find_formalizations_by_cessao_date_and_product_slug(
            cessao_date_object, product_slug
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
                    formalization_at=str(v.formalization_at),
                ),
                result,
            )
        )
        return self.query_result(result=formalizations)

    async def get_formalized_financing(self, financing_ids: list[int]) -> FormalizedFinancingResponse:
        formalized_financing = await self.repository.get_formalized_financing(financing_ids)
        return formalized_financing
