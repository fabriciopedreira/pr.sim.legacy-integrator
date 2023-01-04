
from pydantic import BaseModel


class FormalizedFinancingResponse(BaseModel):
    ccb_number: int
    client_cpf: str
    client_name: str
    person_type: str
    contract_date: str
