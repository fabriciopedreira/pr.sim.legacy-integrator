import uuid
from random import randint

from pydantic import UUID4, BaseModel, Field


class FinancingRequest(BaseModel):
    project_id: UUID4
    partner_id: int
    user_id: int
    person_type: str
    financing_value: float
    down_payment: float
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
    geracao_mensal: int = Field(default=15)

    class Config:
        schema_extra = {
            "example": {
                "project_id": uuid.uuid4(),
                "partner_id": 1,
                "user_id": 1,
                "person_type": "PF",
                "financing_value": 25000,
                "down_payment": 5000,
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
                "commission": 0.12,
                "geracao_mensal": 15,
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
