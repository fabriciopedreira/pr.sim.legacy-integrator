import uuid

from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies import access_validation, access_validation_fixed_token, get_repository
from app.domain.financing.repository import FinancingRepository
from app.domain.financing.schemas import (
    FinancingRequest,
    FinancingResponse,
    FinancingUpdateRequest,
    FinancingUpdateResponse,
    PermissionUpdateFinancingResponse,
)
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


@financing_router.put(
    "/financing/",
    summary="Update financing",
    response_model=FinancingUpdateResponse,
)
async def update_financing(
    data_request: FinancingUpdateRequest,
    repository: FinancingRepository = Depends(get_repository(repo_type=FinancingRepository)),
):
    result = await FinancingService(repository).update_financing(
        project_id=data_request.project_id,
        project_value=data_request.financing_value,
        down_payment=data_request.down_payment,
        grace_period=data_request.grace_period,
        cet=data_request.cet,
        ipca=data_request.ipca,
        is_combo=data_request.is_combo,
        installments=data_request.installments,
        iof=data_request.iof,
        aliquot_iof=data_request.aliquot_iof,
        installment_value=data_request.installment_value,
        taxa_de_juros=data_request.taxa_de_juros,
        registration_fee=data_request.taxa_de_cadastro,
        commission=data_request.commission,
        system_power=data_request.system_power,
    )

    return FinancingUpdateResponse(
        financing_id=result, message="Financing updated successfully!", code=status.HTTP_200_OK
    )
