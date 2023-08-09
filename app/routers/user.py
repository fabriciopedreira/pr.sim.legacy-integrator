from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies import access_validation, get_repository
from app.domain.user.repository import UserRepository
from app.domain.user.schema import FinancingStoreResponse, UsersResponse
from app.domain.user.service import UserService
from app.enum import FinancingType
from app.internal.utils import get_sub, latency

router = APIRouter()


@router.get(
    "/user/info/",
    summary="information of user",
    response_model=UsersResponse,
)
@latency
async def user_information(
    token: str = Depends(access_validation),
    repository: UserRepository = Depends(get_repository(repo_type=UserRepository)),
) -> UsersResponse:

    request_user_id = get_sub(token)
    user_info = await UserService(repository).get_user(user_id=request_user_id)

    return user_info


@router.get(
    "/user/financing-store/",
    summary="get financing data for in-store kit purchases",
    response_model=FinancingStoreResponse,
)
@latency
async def get_eligible_store_financing(
    token: str = Depends(access_validation),
    document: str = None,
    document_type: FinancingType | None = FinancingType.cpf,
    repository: UserRepository = Depends(get_repository(repo_type=UserRepository)),
) -> FinancingStoreResponse:

    request_user_id = get_sub(token)

    financing = await UserService(repository).get_eligible_store_financing(
        user_id=request_user_id, document=document, document_type=document_type
    )

    return FinancingStoreResponse(data=financing, user_id=request_user_id, code=status.HTTP_200_OK, error=False)
