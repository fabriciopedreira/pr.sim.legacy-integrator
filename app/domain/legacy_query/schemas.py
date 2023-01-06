from pydantic import BaseModel


class FormalizedFinancingResponse(BaseModel):
    ccb_number: int | str
    client_cpf: str
    client_name: str
    person_type: str
    contract_date: str


class SessionDataFinancialProductSlug(BaseModel):
    session_data: str
    product_slug: str
