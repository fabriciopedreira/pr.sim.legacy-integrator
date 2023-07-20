import uuid

from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies import access_validation, access_validation_fixed_token, get_repository
from app.domain.financing.repository import FinancingRepository
from app.domain.financing.schemas import FinancingRequest, FinancingResponse, PermissionUpdateFinancingResponse
from app.domain.financing.service import FinancingService
from app.internal.config.settings import ACCESS_VALIDATION
from app.internal.utils import latency

financing_router = (
    APIRouter(dependencies=[Depends(access_validation)])
    if not ACCESS_VALIDATION
    else APIRouter(dependencies=[Depends(access_validation_fixed_token)])
)


@financing_router.post(
    "/financing/create",
    summary="Create financing",
    response_model=FinancingResponse,
    status_code=status.HTTP_201_CREATED,
)
@latency
async def create_financing(
    data_request: FinancingRequest,
    repository: FinancingRepository = Depends(get_repository(repo_type=FinancingRepository)),
):

    new_financing = await FinancingService(repository).create_financing(data_request)

    return FinancingResponse(
        financing_id=new_financing.id, message="Financing created successfully!", code=status.HTTP_201_CREATED
    )


@financing_router.get(
    "/financing/{project_id}/status-update",
    summary="Get financing update eligibility status by project id",
    response_model=PermissionUpdateFinancingResponse,
)
@latency
async def get_contract_generation_status(
    project_id: uuid.UUID,
    repository: FinancingRepository = Depends(get_repository(repo_type=FinancingRepository)),
):
    response = await FinancingService(repository).can_update_financing(project_id=project_id)

    return PermissionUpdateFinancingResponse(project_id=project_id, can_update_values=response, code=status.HTTP_200_OK)
