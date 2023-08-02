from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    confirmed: bool
    parceiro_id: int
    nome_completo: str
    perfil: str
    contato_id: int
    contato_celular: str
    contato_email: str


class PartnerResponse(BaseModel):
    id: int


class ContactResponse(BaseModel):
    id: int
    email: str
    phone: str


class UsersResponse(BaseModel):
    id: int
    confirmed: bool
    contact: ContactResponse
    partner: PartnerResponse
    complete_name: str
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


class FinancingStore(BaseModel):
    financing_id: int
    client_name: str
    client_cpf: str
    project_name: str
    project_value: float
    financing_stage: str
    financing_status: str


class FinancingStoreResponse(BaseModel):
    data: list[FinancingStore]
    user_id: int
    error: bool
    code: int
