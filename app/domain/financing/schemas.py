import uuid
from enum import Enum
from random import randint
from typing import Optional

from pydantic import UUID4, BaseModel, confloat

from app.domain.legacy_query.enums import TipoPessoa


class AddonType(str, Enum):
    insurance = "insurance"
    ampera = "ampera"


class Addon(BaseModel):
    product_name: str
    product_external_id: Optional[uuid.UUID]
    simulation_id: uuid.UUID
    type: AddonType
    product_slug: Optional[str]
    applied: bool
    partner_commission: float
    installment_price: float
    total_price: float


class FinancingRequest(BaseModel):
    project_id: UUID4
    partner_id: int
    user_id: int
    person_type: str
    financing_value: float
    down_payment: float
    system_power: float
    grace_period: int
    project_name: str
    cet: str
    ipca: str
    is_combo: bool
    installments: int
    iof: float
    aliquot_iof: float
    installment_value: float
    taxa_de_juros: float
    taxa_de_cadastro: float
    commission: float
    document: str
    addons: Optional[list[Addon]] = None
    created_at: str

    class Config:
        schema_extra = {
            "example": {
                "project_id": uuid.uuid4(),
                "partner_id": 1,
                "user_id": 1,
                "person_type": TipoPessoa.PESSOA_FISICA,
                "financing_value": 25000,
                "down_payment": 5000,
                "system_power": 36.08,
                "grace_period": 4,
                "project_name": "Lala Movie",
                "cet": "POS_FIXADO",
                "ipca": "mensal",
                "is_combo": True,
                "installments": 12,
                "iof": 12.34,
                "aliquot_iof": 3.2,
                "installment_value": 12.23,
                "taxa_de_juros": 3.15,
                "taxa_de_cadastro": 1.99,
                "commission": 1.0,
                "document": "111.111.111-11",
                "created_at": "2023-08-12 14:20:00",
            }
        }


class FinancingResponse(BaseModel):
    financing_id: int
    message: str
    code: int

    class Config:
        schema_extra = {
            "example": {"financing_id": randint(1000, 9999), "message": "Financing created successfully!", "code": 201}
        }


class PermissionUpdateFinancingResponse(BaseModel):
    project_id: uuid.UUID
    can_update_values: bool
    code: int

    class Config:
        schema_extra = {"example": {"project_id": uuid.uuid4(), "can_update_values": False, "code": 200}}


class FinancingUpdateResponse(BaseModel):
    financing_id: int
    message: str
    code: int

    class Config:
        schema_extra = {
            "example": {"financing_id": randint(1000, 9999), "message": "Financing updated successfully!", "code": 200}
        }


class FinancingUpdateRequest(BaseModel):
    project_id: uuid.UUID
    system_power: float = None
    financing_value: float
    down_payment: float
    grace_period: int
    cet: str
    ipca: str
    is_combo: bool
    installments: int
    iof: float
    aliquot_iof: float
    installment_value: float
    taxa_de_juros: float
    taxa_de_cadastro: float
    commission: confloat(ge=0.0, le=5.0)
    addons: Optional[list[Addon]] = None

    class Config:
        schema_extra = {
            "example": {
                "project_id": "152f1729-6bb9-4efa-a409-c499557087fc",
                "system_power": 300.0,
                "financing_value": 25000,
                "down_payment": 5000,
                "grace_period": 4,
                "cet": "POS_FIXADO",
                "ipca": "mensal",
                "is_combo": True,
                "installments": 12,
                "iof": 12.34,
                "aliquot_iof": 3.2,
                "installment_value": 12.23,
                "taxa_de_juros": 3.15,
                "taxa_de_cadastro": 1.99,
                "commission": 1.0,
            }
        }


class FinancingCotationDTO(BaseModel):
    financing_id: int
    quotation_id: int
    has_combo_facil: bool
    commission_id: Optional[int]


class InstallmentData(BaseModel):
    cet: str
    iof: float
    aliquota_iof: float
    numero_de_parcelas: int
    valor_da_parcela: float
    taxa_de_juros: float
    taxa_de_cadastro: float
    valor_da_comissao: float
    cotacao_id: int
