from typing import Any, Optional

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


class FormalizedFinancingRequest(BaseModel):
    financings: list[int]

    class Config:
        schema_extra = {"example": {"financings": [678510, 372639, 372661]}}


class Guarantor(BaseModel):
    id: Optional[int]
    name: Optional[str]
    document: Optional[str]
    address: Optional[str]
    address_number: Optional[str]
    address_complement: Optional[str]
    neighborhood: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]


class Address(BaseModel):
    city: Optional[str]
    complement: Optional[str]
    id: Optional[int]
    neighborhood: Optional[str]
    number: Optional[str]
    state: Optional[str]
    street: Optional[str]
    zipcode: Optional[str]


class BankData(BaseModel):
    account: Optional[str]
    account_digit: Optional[str]
    account_type: Optional[str]
    agency: Optional[str]
    description: Optional[str]
    id: Optional[int]
    name: Optional[str]
    number: Optional[str]
    pix_key: Optional[str]


class Contact(BaseModel):
    cellphone: Optional[str]
    email: Optional[str]
    id: Optional[int]
    phone_number: Optional[str]


class Customer(BaseModel):
    address: Optional[str]
    address_complement: Optional[str]
    address_number: Optional[str]
    birthdate: Optional[str]
    city: Optional[str]
    cpf_cnpj: Optional[str]
    district: Optional[str]
    email: Optional[str]
    id: Optional[int]
    mobile_number: Optional[str]
    monthly_income: Optional[int]
    name: Optional[str]
    occupation: Optional[str]
    phone_number: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]


class File(BaseModel):
    is_guarantor: bool = False
    type: str
    url: str


class Profession(BaseModel):
    id: Optional[int]
    name: Optional[str]


class LegalRepresentative(BaseModel):
    address: Optional[Address]
    attribution_term_signature: Optional[bool]
    contact: Optional[Contact]
    document: Optional[str]
    id: Optional[int]
    isolated_signature: Optional[bool]
    marital_status: Optional[str]
    name: Optional[str]
    profession: Optional[dict[str, str]]
    signature_endorsement: Optional[bool]


class FinancialProduct(BaseModel):
    address: Optional[Address]
    balance: Optional[int]
    bank_data: Optional[BankData]
    cnab: Optional[str]
    contact: Optional[dict[str, str]]
    corporate_name: Optional[str]
    document: Optional[str]
    external_slug: Optional[str]
    id: Optional[int]
    legal_representatives: Optional[list[LegalRepresentative]]
    name: Optional[str]
    slug: Optional[str]
    template: Optional[str]


class Financing(BaseModel):
    annual_interest_rate: Optional[float]
    banking: Optional[str]
    ccb: Optional[str]
    ccb_cession: Optional[str]
    ccb_date: Optional[str]
    cet: Optional[str]
    files: Optional[list[File]]
    financial_product: Optional[FinancialProduct]
    first_installment_date: Optional[str]
    formalized_at: Optional[str]
    grace_period: Optional[int]
    gross_amount: Optional[int]
    id: Optional[int]
    installment_amount: Optional[float]
    installments_number: Optional[int]
    interest_fee: Optional[float]
    iof: Optional[float]
    ipca_type: Optional[str]
    last_installment_date: Optional[str]
    rate_type: Optional[str]
    registration_fee: Optional[float]
    securitization: Optional[str]
    status: Optional[str]
    type: Optional[str]


class Partner(BaseModel):
    id: Optional[int]
    name: Optional[str]


class Insurance(BaseModel):
    additional_installment_amount: Optional[float]
    name: Optional[str]
    type: Optional[str]


class FormalizedFinancing(BaseModel):
    customer: Customer
    financing: Financing
    guarantor: Guarantor
    insurances: list[Insurance]
    partner: Partner

    class Config:
        orm_mode = True


class FormalizedFinancingResponse(BaseModel):
    data: list[FormalizedFinancing]


class Document(BaseModel):
    client_documento_de_identidade: Optional[str]
    client_documentos_adicionais: Optional[list[dict[str, str]]]
    client_comprovante_de_residencia: Optional[str]
    client_comprovante_de_renda: Optional[str]
    client_titularidade_do_imovel: Optional[str]
    client_comprovante_faturamento: Optional[str]
    client_contrato_social: Optional[str]
    client_dap: Optional[str]
    client_comprovante_propriedade_rural: Optional[str]
    client_contrato_assinado: Optional[str]
    avalista_documento_de_identidade: Optional[str]
    avalista_documentos_adicionais: Optional[list[dict[str, str]]]
    avalista_comprovante_de_residencia: Optional[str]
    avalista_comprovante_de_renda: Optional[str]
    avalista_titularidade_do_imovel: Optional[str]
    avalista_contrato_social: Optional[str]
    avalista_dap: Optional[str]
    avalista_comprovante_propriedade_rural: Optional[str]
