from fastapi import APIRouter, Depends

from app.dependencies import access_validation, get_repository
from app.domain.user.repository import UserRepository
from app.domain.user.schema import UsersResponse
from app.domain.user.service import UserService
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
    user_info = await UserService(repository).get_user(request_user_id)

    return user_info
