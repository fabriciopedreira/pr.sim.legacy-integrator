from typing import Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    confirmed: bool
    parceiro_id: Optional[int]
    nome_completo: Optional[str]
    perfil: str
    contato_id: Optional[int]
    contato_celular: Optional[str]
    contato_email: Optional[str]


class PartnerResponse(BaseModel):
    id: Optional[int]


class ContactResponse(BaseModel):
    id: Optional[int]
    email: Optional[str]
    phone: Optional[str]


class UsersResponse(BaseModel):
    id: int
    confirmed: bool
    contact: Optional[ContactResponse]
    partner: Optional[PartnerResponse]
    complete_name: Optional[str]
    perfil: str

    class Config:
        schema_extra = {
            "id": 1,
            "confirmed": True,
            "contact": {"id": 1, "email": "testes@solfacil.com.br", "phone": "(11) 99999-9999"},
            "partner": {"id": 1},
            "complete_name": "Testes",
            "perfil": "admin",
        }


class StoreResponse(BaseModel):
    financing_id: int
    client_name: str | None
    document: str
    project_name: str
    project_value: float
    project_system_potency: float
    financing_stage: str
    financing_status: str


class FinancingStoreResponse(BaseModel):
    data: list[StoreResponse]
    user_id: int
    error: bool
    code: int

    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "financing_id": 888888,
                        "client_name": "Marta Vieira da Silva",
                        "client_cpf": "000.000.000-000",
                        "project_name": "PLACA SOLAR",
                        "project_value": 24000.0,
                        "financing_stage": "analise_do_contrato",
                        "financing_status": "aprovado",
                    }
                ],
                "user_id": 74393,
                "error": False,
                "code": 200,
            }
        }
