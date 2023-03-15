import traceback
from dataclasses import dataclass

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, OperationalError

from app.domain.common.exception_base import InsertDBException, SQLAlchemyException, ValidationException
from app.domain.common.legacy_model import Cotacao, Financiamento, Parcela
from app.domain.common.service_base import ServiceBase
from app.domain.financing.repository import FinancingRepository
from app.internal.config import DEFAULT_CALCULATOR, DEFAULT_CITY, DEFAULT_PROVIDER
from app.internal.utils import exc_info, parse_ipca, parser_person_type


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
            cotacao=Cotacao(
                external_simulation_id=data_request.simulation_id,
                valor_do_projeto=data_request.financing_value,
                entrada=data_request.down_payment,
                carencia=data_request.grace_period,
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

        return financing

    async def save_parcela(self, financing, data_request):
        parcela = Parcela(
            cotacao_id=financing.cotacao_id,
            cet=data_request.cet,
            iof=data_request.iof,
            aliquota_iof=data_request.aliquot_iof,
            numero_de_parcelas=data_request.installments,
            valor_da_parcela=data_request.installment_value,
            taxa_de_juros=data_request.taxa_de_juros,
            taxa_de_cadastro=data_request.taxa_de_cadastro,
            valor_da_comissao=data_request.commission,
        )

        await self.repository.save(parcela)
