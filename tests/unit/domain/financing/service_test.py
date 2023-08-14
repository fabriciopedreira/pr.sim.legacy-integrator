from unittest.mock import Mock

import pytest

from app.domain.common.exception_base import ParamsException
from app.domain.financing.schemas import FinancingRequest
from app.domain.financing.service import FinancingService
from app.domain.legacy_query.enums import TipoPessoa


@pytest.fixture
def financing_service():
    financing_repository = Mock()

    async def async_return(value):
        return value

    financing_repository.save.side_effect = [async_return(True) for _ in range(10)]
    return FinancingService(financing_repository)


@pytest.fixture
def data_request():
    return FinancingRequest(
        project_id="2ade5cff-63f3-445b-a912-db6f24727dc7",
        partner_id=1,
        user_id=1,
        person_type=TipoPessoa.PESSOA_FISICA,
        financing_value=25000,
        down_payment=5000,
        system_power=36.08,
        grace_period=4,
        project_name="Lala Movie",
        cet="POS_FIXADO",
        ipca="mensal",
        is_combo=True,
        installments=12,
        iof=12.34,
        aliquot_iof=3.2,
        installment_value=12.23,
        taxa_de_juros=3.15,
        taxa_de_cadastro=1.99,
        commission=1.0,
        document="111.111.111-11",
        created_at="2023-07-12 14:20:00"
    )


@pytest.mark.asyncio
async def test_person_type_different_of_document(financing_service, data_request):
    personal_type_invalid = TipoPessoa.PESSOA_JURIDICA
    data_request.person_type = personal_type_invalid

    with pytest.raises(ParamsException) as exception_info:
        await financing_service.create_financing(data_request)
    assert str(exception_info.value.detail) == "Invalid person_type"


@pytest.mark.asyncio
async def test_document_invalid_format(financing_service, data_request):
    document_invalid_format_for_CNPJ = "aa.111.111/1111-11"
    data_request.document = document_invalid_format_for_CNPJ

    with pytest.raises(ParamsException) as exception_info:
        await financing_service.create_financing(data_request)
    assert str(exception_info.value.detail) == "Invalid Document"


@pytest.mark.asyncio
async def test_creating_financing_with_CPF_succes(financing_service, data_request):
    await financing_service.create_financing(data_request)

    financed_value = data_request.financing_value - data_request.down_payment
    gross_commission_value = 1 * financed_value / 100

    parcela = financing_service.repository.save.call_args_list[1][0][0]
    assert parcela.cet == data_request.cet
    assert parcela.iof == data_request.iof
    assert parcela.aliquota_iof == data_request.aliquot_iof
    assert parcela.numero_de_parcelas == data_request.installments
    assert parcela.valor_da_parcela == data_request.installment_value
    assert parcela.valor_da_comissao == gross_commission_value

    financing = financing_service.repository.save.call_args_list[0][0][0]
    assert financing.tipo_id == 1
    assert financing.etapa == "dados_do_cliente"
    assert financing.status == "em_andamento"
    assert financing.parceiro_id == data_request.partner_id
    assert financing.user_id == data_request.user_id
    assert financing.combo_facil == data_request.is_combo
    assert financing.cliente
    assert not financing.empresa


@pytest.mark.asyncio
async def test_creating_financing_with_CNPJ_succes(financing_service, data_request):
    valid_document_for_CNPJ = "11.111.111/1111-11"
    person_type_for_CNPJ = TipoPessoa.PESSOA_JURIDICA

    data_request.person_type = person_type_for_CNPJ
    data_request.document = valid_document_for_CNPJ

    financed_value = data_request.financing_value - data_request.down_payment
    gross_commission_value = 1 * financed_value / 100

    await financing_service.create_financing(data_request)

    parcela = financing_service.repository.save.call_args_list[1][0][0]
    assert parcela.cet == data_request.cet
    assert parcela.iof == data_request.iof
    assert parcela.aliquota_iof == data_request.aliquot_iof
    assert parcela.numero_de_parcelas == data_request.installments
    assert parcela.valor_da_parcela == data_request.installment_value

    assert parcela.valor_da_comissao == gross_commission_value

    financing = financing_service.repository.save.call_args_list[0][0][0]
    assert financing.tipo_id == 2
    assert financing.etapa == "dados_do_cliente"
    assert financing.status == "em_andamento"
    assert financing.parceiro_id == data_request.partner_id
    assert financing.user_id == data_request.user_id
    assert financing.combo_facil == data_request.is_combo
    assert financing.empresa
    assert not financing.cliente
