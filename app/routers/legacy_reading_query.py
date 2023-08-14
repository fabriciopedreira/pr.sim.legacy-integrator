from fastapi import APIRouter, Depends

from app.dependencies import access_validation, access_validation_fixed_token, get_repository
from app.domain.legacy_query.repository.formalized import FormalizedRepository
from app.domain.legacy_query.schemas import FormalizedFinancingRequest, FormalizedFinancingResponse, FormalizedResponse
from app.domain.legacy_query.service.formalized import FormalizedService
from app.internal.config.settings import ACCESS_VALIDATION
from app.internal.utils import latency


router = (
    APIRouter(prefix="/legacy", dependencies=[Depends(access_validation)])
    if not ACCESS_VALIDATION
    else APIRouter(prefix="/legacy", dependencies=[Depends(access_validation_fixed_token)])
)


@router.get(
    path="/financing-formalized/formalizations/{cessao_date}/{product_slug}",
    summary="Find formalizations by cessao date and financial_product_slug.",
    response_model=list[FormalizedResponse],
    status_code=200,
)
@latency
async def find_formalizations_by_cessao_date_and_product_slug(
    cessao_date: str,
    product_slug: str,
    repository: FormalizedRepository = Depends(get_repository(repo_type=FormalizedRepository)),
):
    """
    * **param**: cessao_date: Data from session
    * **param**: product_slug: Slug from financing-product
    """
    return await FormalizedService(repository=repository).formalizations_by_cessao_date_and_product_slug(
        cessao_date, product_slug
    )


@router.post(
    path="/financing-formalized/",
    summary="Find formalized financing by ids",
    response_model=FormalizedFinancingResponse,
    status_code=200,
)
@latency
async def get_formalized_financing_by_ids(
    financing_ids: FormalizedFinancingRequest,
    repository: FormalizedRepository = Depends(get_repository(repo_type=FormalizedRepository)),
):
    """
    * **body**: financing_ids: List of financing ids
    * **return**: List of formalized financing
    """
    return await FormalizedService(repository=repository).get_formalized_financing(
        financing_ids=financing_ids.financings
    )
