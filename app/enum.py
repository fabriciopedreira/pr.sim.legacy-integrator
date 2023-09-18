from enum import Enum


class FinancingStage(str, Enum):
    contract_signing = "assinatura_do_contrato"


class BuildEnvironment(str, Enum):
    dev = "DEV"
    prd = "PRD"
    tst = "TST"
    hml = "HML"


class FinancingType(str, Enum):
    cnpj = "PJ"
    cpf = "PF"
