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
    functionPrincipal: str
    complete_name: str
    perfil: str

    class Config:
        schema_extra = {
            "id": 1,
            "confirmed": True,
            "contact": {"id": 1, "email": "testes@solfacil.com.br", "phone": "(11) 99999-9999"},
            "partner": {"id": 1},
            "functionPrincipal": "Testes",
            "complete_name": "Testes",
            "perfil": "admin",
        }
