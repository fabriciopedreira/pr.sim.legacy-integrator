from fastapi import APIRouter, Depends

from app.dependencies import access_validation, get_repository
from app.domain.legacy_query.repository import Repository
from app.domain.legacy_query.schemas import FormalizedFinancingResponse
from app.domain.legacy_query.service import Service
from app.internal.utils import latency

router = APIRouter(prefix="/legacy", dependencies=[Depends(access_validation)])


@router.get(
    path="/financing-formalized/formalizations/{session_data}/{product_slug}",
    summary="Find formalizations by session_data and financial_product_slug.",
    response_model=list[FormalizedFinancingResponse],
    status_code=200,
)
@latency
async def find_formalizations_by_session_data_and_product_slug(
    session_data: str, product_slug: str, repository: Repository = Depends(get_repository(repo_type=Repository))
):
    """Find formalizations by session_data and financial_product_slug
    * **param**: session_data: Data from session
    * **param**: product_slug: Slug from financing-product
    * **param**: repository: Repository to make query on database

    **return**: BaseModel
    """

    return await Service(repository=repository).formalizations_by_session_data_and_product_slug(
        session_data, product_slug
    )
