from enum import Enum


class FinancingStage(str, Enum):
    contract_signing = "assinatura_do_contrato"


class BuildEnvironment(str, Enum):
    dev = "dev"
    prd = "prd"
    tst = "tst"
    hml = "hml"


class FinancingType(str, Enum):
    cnpj = "PJ"
    cpf = "PF"
