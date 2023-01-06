from fastapi import APIRouter, Depends

from app.dependencies import access_validation, get_repository
from app.domain.legacy_query.repository.formalized import FormalizedRepository
from app.domain.legacy_query.schemas import FormalizedResponse
from app.domain.legacy_query.service.formalized import FormalizedService
from app.internal.utils import latency

router = APIRouter(prefix="/legacy", dependencies=[Depends(access_validation)])


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
