from pydantic import BaseModel


class FormalizedResponse(BaseModel):
    ccb_number: int | str
    banking_name: str
    client_document: str
    client_name: str
    person_type: str
    slug: str
    contract_date: str
    formalization_at: str
