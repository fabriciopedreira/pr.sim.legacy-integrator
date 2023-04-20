import traceback
from dataclasses import dataclass

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, OperationalError

from app.domain.common.exception_base import (
    InsertDBException,
    ParamsException,
    SQLAlchemyException,
    ValidationException,
)
from app.domain.common.legacy_model import Cliente, Cotacao, Empresa, Financiamento, Parcela
from app.domain.common.service_base import ServiceBase
from app.domain.financing.financial_calcs import (
    convert_annual_to_monthly_rate,
    convert_registration_fee_to_total_amount,
    pgto,
)
from app.domain.financing.repository import FinancingRepository
from app.internal.config import DEFAULT_CALCULATOR, DEFAULT_CITY, DEFAULT_PROVIDER
from app.internal.utils import exc_info, format_document, parse_ipca, parser_person_type, sanitize_document


@dataclass
class FinancingService(ServiceBase):
    repository: FinancingRepository

    async def create_financing(self, data_request):
        try:
            financing_data = await self.financing_data(data_request)

            financing = await self.repository.save(financing_data)
            await self.save_parcela(financing_data, data_request)
        except OperationalError as exc:
            raise SQLAlchemyException(stacktrace=traceback.format_exception_only(*exc_info())) from exc
        except ValidationError as exc:
            raise ValidationException(stacktrace=traceback.format_exception_only(*exc_info())) from exc
        except IntegrityError as exc:
            raise InsertDBException(stacktrace=traceback.format_exception_only(*exc_info()), message=exc) from exc

        return financing

    async def financing_data(self, data_request):
        financing = Financiamento(
            tipo_id=parser_person_type(data_request.person_type),
            etapa="dados_do_cliente",
            status="em_andamento",
            parceiro_id=data_request.partner_id,
            user_id=data_request.user_id,
            combo_facil=data_request.is_combo,
            cotacao=Cotacao(
                external_simulation_id=data_request.project_id,
                valor_do_projeto=data_request.financing_value,
                entrada=data_request.down_payment,
                carencia=data_request.grace_period - 1,
                nome_do_projeto=data_request.project_name,
                cet=data_request.cet,
                ipca=parse_ipca(data_request.cet, data_request.ipca),
                ipca_vigente=data_request.ipca,
                numero_de_parcelas=data_request.installments,
                calculadora_id=DEFAULT_CALCULATOR,
                cidade_id=DEFAULT_CITY,
                geracao_mensal=data_request.geracao_mensal,
            ),
        )

        if data_request.is_combo:
            financing.cotacao.fornecedor_id = DEFAULT_PROVIDER

        return await self.save_document(financing, data_request)

    async def save_document(self, financing, data_request):
        document_sanetized = sanitize_document(data_request.document)
        size_document = len(document_sanetized)

        CPF_LENGTH = 11
        CNPJ_LENGTH = 14

        valid_sizes = [CPF_LENGTH, CNPJ_LENGTH]
        if not size_document in valid_sizes:
            raise ParamsException(model=Financiamento.__tablename__, detail="Invalid Document")

        document_parsed = format_document(size_document, document_sanetized)

        if data_request.person_type == "PF" and size_document == CPF_LENGTH:
            financing.cliente = Cliente(cpf=document_parsed)
        elif data_request.person_type == "PJ" and size_document == CNPJ_LENGTH:
            financing.empresa = Empresa(cnpj=document_parsed)
        else:
            raise ParamsException(model=Financiamento.__tablename__, detail="Invalid person_type")

        return financing

    async def save_parcela(self, financing, data_request):
        # TODO valor_financiado and taxa_de_cadastro_bruta needs to come from Product-pricing
        valor_financiado = data_request.financing_value - data_request.down_payment

        taxa_de_cadastro_bruta = convert_registration_fee_to_total_amount(
            valor_financiado, data_request.taxa_de_cadastro
        )

        taxa_de_juros_mensalisada = convert_annual_to_monthly_rate(data_request.taxa_de_juros)

        parcela = Parcela(
            cotacao_id=financing.cotacao_id,
            cet=data_request.cet,
            iof=data_request.iof,
            aliquota_iof=data_request.aliquot_iof,
            numero_de_parcelas=data_request.installments,
            valor_da_parcela=data_request.installment_value,
            taxa_de_juros=taxa_de_juros_mensalisada,
            taxa_de_cadastro=taxa_de_cadastro_bruta,
            valor_da_comissao=data_request.commission,
        )

        await self.repository.save(parcela)

        parcela_144x = await calculate_144x_installment(
            financing, valor_financiado, taxa_de_juros_mensalisada, taxa_de_cadastro_bruta
        )

        await self.repository.save(parcela_144x)


async def calculate_144x_installment(
    financing,
    financed_amount: float,
    monthly_interest_rate: float,
    total_registration_fee: float,
    commission: float = 0,
) -> Parcela:
    """
    Nogord analysis requires a 144x installment to calculate energy saving.
    Otherwise, Nogord rejects the project with "PROJETO RUIM" flag.

    This should be removed as soon as they remove that Nogord rule.

    """

    total_financed_amount = financed_amount + total_registration_fee

    estimated_iof_quota = 3.25

    iof_total_amount = total_financed_amount * estimated_iof_quota / 100

    installment_value = abs(pgto(monthly_interest_rate, 144, total_financed_amount, iof_total_amount))

    legacy_cet = "PRE_FIXADO"

    return Parcela(
        cotacao_id=financing.cotacao_id,
        cet=legacy_cet,
        iof=iof_total_amount,
        aliquota_iof=estimated_iof_quota,
        numero_de_parcelas=144,
        valor_da_parcela=installment_value,
        taxa_de_juros=monthly_interest_rate,
        taxa_de_cadastro=total_registration_fee,
        valor_da_comissao=commission,
    )
