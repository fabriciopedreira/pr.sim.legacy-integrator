from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies import access_validation, access_validation_fixed_token, get_repository
from app.domain.store.repository import StoreRepository
from app.domain.store.schema import KitsPurchase, StoreResponse
from app.domain.store.service import StoreService
from app.internal.config.settings import ACCESS_VALIDATION
from app.internal.utils import latency

store_router = (
    APIRouter(dependencies=[Depends(access_validation)])
    if not ACCESS_VALIDATION
    else APIRouter(dependencies=[Depends(access_validation_fixed_token)])
)


@store_router.post(
    "/store/recebimento",
    summary="create receipt model",
    response_model=StoreResponse,
    status_code=status.HTTP_201_CREATED,
)
@latency
async def create_receipt(
    data: KitsPurchase,
    repository: StoreRepository = Depends(get_repository(repo_type=StoreRepository)),
):

    response = await StoreService(repository).create_recebimento(
        order_id=data.order_id,
        items=data.items,
        shipping=data.shipping,
        subtotal=data.subtotal,
        total=data.total,
        power=data.power,
        financing_id=data.financing_id,
    )

    return StoreResponse(data=response, code=status.HTTP_201_CREATED, error=False)
