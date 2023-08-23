import math
from datetime import date, datetime, time
from typing import Any, List

from dateutil.relativedelta import relativedelta
from sqlalchemy import case, text

from app.domain.common.legacy_model import (
    Bancarizadora,
    Cessao,
    CessaoFormalizacao,
    Cliente,
    Contrato,
    Cotacao,
    Documento,
    Empresa,
    Emprestimo,
    Financiamento,
    FinanciamentoSeguroTaxa,
    Formalizacao,
    Parcela,
    ProdutoFinanceiro,
    Projeto,
    Seguro,
    SeguroEmprestimo,
    SeguroTaxa,
    SeguroTipo,
    TipoDeFinanciamento,
    Validacao,
)
from app.domain.common.repository_base import RepositoryBase
from app.domain.legacy_query.enums import TipoPessoa, ValidacaoEtapa, ValidacaoStatus
from app.domain.legacy_query.schemas import (
    Address,
    BankData,
    Contact,
    Customer,
    Document,
    File,
    FinancialProduct,
    Financing,
    FormalizedFinancing,
    FormalizedFinancingResponse,
    Guarantor,
    Insurance,
    LegalRepresentative,
    Partner,
)
from app.internal.utils import get_month_by_number


class FormalizedRepository(RepositoryBase):
    async def find_formalizations_by_cessao_date_and_product_slug(
        self, cessao_date_object: date, product_slug: str
    ) -> List[tuple[Any]]:
        return (
            self.session_db.query(
                Financiamento,
                Emprestimo.numero_ccb.label("ccb_number"),
                Bancarizadora.nome.label("banking_name"),
                case(
                    [
                        (TipoDeFinanciamento.tipo == TipoPessoa.PESSOA_FISICA, Cliente.cpf),
                        (TipoDeFinanciamento.tipo == TipoPessoa.PRODUTOR_RURAL, Cliente.cpf),
                        (TipoDeFinanciamento.tipo == TipoPessoa.PESSOA_JURIDICA, Empresa.cnpj),
                    ]
                ).label("client_document"),
                case(
                    [
                        (TipoDeFinanciamento.tipo == TipoPessoa.PESSOA_FISICA, Cliente.nome_completo),
                        (TipoDeFinanciamento.tipo == TipoPessoa.PRODUTOR_RURAL, Cliente.nome_completo),
                        (TipoDeFinanciamento.tipo == TipoPessoa.PESSOA_JURIDICA, Empresa.razao_social),
                    ]
                ).label("client_name"),
                TipoDeFinanciamento.tipo.label("person_type"),
                ProdutoFinanceiro.slug,
                Contrato.created_at.label("contract_date"),
                Contrato.upload_drive_data.label("formalization_at"),
            )
            .join(Contrato, Contrato.id == Financiamento.contrato_id)
            .join(Emprestimo, Emprestimo.id == Financiamento.emprestimo_id)
            .join(Bancarizadora, Bancarizadora.id == Financiamento.bancarizadora_id)
            .join(Cliente, Cliente.id == Financiamento.cliente_id)
            .join(Empresa, Empresa.id == Financiamento.empresa_id, isouter=True)  # left join
            .join(ProdutoFinanceiro, ProdutoFinanceiro.id == Contrato.produto_financeiro_id)
            .join(TipoDeFinanciamento, TipoDeFinanciamento.id == Financiamento.tipo_id)
            .join(Formalizacao, Formalizacao.financiamento_id == Financiamento.id)
            .join(CessaoFormalizacao, CessaoFormalizacao.formalizacao_id == Formalizacao.id)
            .join(Cessao, Cessao.id == CessaoFormalizacao.cessao_id)
            .filter(
                Cessao.created_at >= datetime.combine(cessao_date_object, time.min),
                Cessao.created_at <= datetime.combine(cessao_date_object, time.max),
                ProdutoFinanceiro.slug == product_slug,
            )
            .all()
        )

    async def get_formalized_financing(self, financing_ids: list[int]) -> FormalizedFinancingResponse:
        formalized_financing = (
            self.session_db.query(Financiamento)
            .join(Cotacao, Cotacao.id == Financiamento.cotacao_id)
            .join(Contrato, Contrato.id == Financiamento.contrato_id)
            .join(Projeto, Projeto.id == Financiamento.projeto_id)
            .join(Parcela, Parcela.cotacao_id == Cotacao.id)
            .join(ProdutoFinanceiro, ProdutoFinanceiro.id == Contrato.produto_financeiro_id)
            .join(Emprestimo, Emprestimo.id == Financiamento.emprestimo_id)
            .join(Bancarizadora, Bancarizadora.id == Financiamento.bancarizadora_id)
            .join(Cliente, Cliente.id == Financiamento.cliente_id)
            .join(Empresa, Empresa.id == Financiamento.empresa_id, isouter=True)
            .join(Validacao, Validacao.financiamento_id == Financiamento.id)
            .filter(
                Validacao.etapa == ValidacaoEtapa.ANALISE_DO_CONTRATO.value,
                Validacao.status == ValidacaoStatus.APROVADO.value,
                Financiamento.id.in_(financing_ids),
            )
            .all()
        )

        formalized_financing_response = FormalizedFinancingResponse(data=[])
        if not formalized_financing:
            return formalized_financing_response

        formalized_financing_response.data = [
            FormalizedFinancing(
                customer=self._get_customer(financing),
                financing=self._get_financing(financing),
                guarantor=self._get_guarantor(financing),
                insurances=self._get_insurance(financing.id),
                partner=self._get_partner(financing),
            )
            for financing in formalized_financing
        ]

        return formalized_financing_response

    def _get_customer(self, financiamento: Any) -> Customer:
        customer = Customer()
        if not financiamento.cliente:
            return customer

        user = self._get_user(financiamento.cliente_id)

        if user.data_de_nascimento:
            customer.birthdate = user.data_de_nascimento.strftime("%Y-%m-%d")

        if user.profissao:
            customer.occupation = user.profissao.nome_profissao

        if user.contato:
            customer.email = user.contato.email
            if user.contato.celular:
                customer.mobile_number = user.contato.celular[4:]
            customer.phone_number = user.contato.telefone_fixo or ""

        customer.address = financiamento.projeto.endereco.rua
        customer.address_complement = financiamento.projeto.endereco.complemento or ""
        customer.address_number = financiamento.projeto.endereco.numero
        customer.city = financiamento.projeto.endereco.cidade.nome
        customer.cpf_cnpj = user.cpf
        customer.district = financiamento.projeto.endereco.bairro
        customer.id = user.id
        customer.monthly_income = user.renda_mensal
        customer.name = user.nome_completo
        customer.state = financiamento.projeto.endereco.cidade.estado.sigla
        customer.zip_code = financiamento.projeto.endereco.cep
        return customer

    def _get_guarantor(self, financiamento: Any) -> Guarantor:
        guarantor = Guarantor()
        if not financiamento.avalista_id:
            return guarantor

        avalista = self._get_user(financiamento.avalista_id)
        if not avalista or not avalista.endereco:
            return guarantor

        guarantor.name = avalista.nome_completo
        guarantor.document = avalista.cpf
        guarantor.address = avalista.endereco.rua
        guarantor.address_number = avalista.endereco.numero
        guarantor.address_complement = avalista.endereco.complemento
        guarantor.neighborhood = avalista.endereco.bairro
        guarantor.city = avalista.endereco.cidade.nome
        guarantor.state = avalista.endereco.cidade.estado.sigla
        guarantor.zipcode = avalista.endereco.cep
        guarantor.id = avalista.id
        return guarantor

    def _get_financial_product_address(self, financiamento: Any) -> Address:
        financial_product_address = Address()
        if not financiamento.contrato.produto_financeiro:
            return financial_product_address

        financial_product_address.street = financiamento.contrato.produto_financeiro.endereco.rua
        financial_product_address.complement = financiamento.contrato.produto_financeiro.endereco.complemento
        financial_product_address.number = financiamento.contrato.produto_financeiro.endereco.numero
        financial_product_address.city = financiamento.contrato.produto_financeiro.endereco.cidade.nome
        financial_product_address.neighborhood = financiamento.contrato.produto_financeiro.endereco.bairro
        financial_product_address.state = financiamento.contrato.produto_financeiro.endereco.cidade.estado.sigla
        financial_product_address.zipcode = financiamento.contrato.produto_financeiro.endereco.cep
        financial_product_address.id = financiamento.contrato.produto_financeiro.endereco.id
        return financial_product_address

    def _get_financial_product_bank_data(self, financiamento: Any) -> BankData:
        financial_product_bank_data = BankData()
        if not financiamento.contrato.produto_financeiro:
            return financial_product_bank_data

        if not financiamento.contrato.produto_financeiro.dado_bancario:
            return financial_product_bank_data

        financial_product_bank_data.account = financiamento.contrato.produto_financeiro.dado_bancario.conta
        financial_product_bank_data.account_digit = financiamento.contrato.produto_financeiro.dado_bancario.conta_digito
        financial_product_bank_data.account_type = financiamento.contrato.produto_financeiro.dado_bancario.tipo_conta
        financial_product_bank_data.agency = financiamento.contrato.produto_financeiro.dado_bancario.agencia
        financial_product_bank_data.description = financiamento.contrato.produto_financeiro.dado_bancario.descricao
        financial_product_bank_data.id = financiamento.contrato.produto_financeiro.dado_bancario.id
        financial_product_bank_data.name = financiamento.contrato.produto_financeiro.dado_bancario.banco
        financial_product_bank_data.number = financiamento.contrato.produto_financeiro.dado_bancario.numero_do_banco
        financial_product_bank_data.pix_key = financiamento.contrato.produto_financeiro.dado_bancario.chave_pix
        return financial_product_bank_data

    def _get_financial_product_contact(self, financiamento: Any) -> Contact:
        financial_product_contact = Contact()
        if not financiamento.contrato.produto_financeiro:
            return financial_product_contact

        if not financiamento.contrato.produto_financeiro.contato:
            return financial_product_contact

        financial_product_contact.cellphone = financiamento.contrato.produto_financeiro.contato.celular
        financial_product_contact.email = financiamento.contrato.produto_financeiro.contato.email
        financial_product_contact.id = financiamento.contrato.produto_financeiro.contato.id
        financial_product_contact.phone_number = financiamento.contrato.produto_financeiro.contato.telefone_fixo
        return financial_product_contact

    def _get_financial_product_legal_representatives(self, financiamento: Any) -> list[LegalRepresentative]:
        legal_representatives = []
        if (
            _legal_representatives := financiamento.contrato.produto_financeiro.representante_legal_produto_financeiro_collection
        ):
            for legal_representative in _legal_representatives:

                legal_representative_address = Address()
                if financiamento.contrato.produto_financeiro.endereco:
                    legal_representative_address = Address(
                        street=financiamento.contrato.produto_financeiro.endereco.rua,
                        complement=financiamento.contrato.produto_financeiro.endereco.complemento,
                        number=financiamento.contrato.produto_financeiro.endereco.numero,
                        city=financiamento.contrato.produto_financeiro.endereco.cidade.nome,
                        neighborhood=financiamento.contrato.produto_financeiro.endereco.bairro,
                        state=financiamento.contrato.produto_financeiro.endereco.cidade.estado.sigla,
                        zipcode=financiamento.contrato.produto_financeiro.endereco.cep,
                        id=financiamento.contrato.produto_financeiro.endereco.id,
                    )

                legal_representative_contact = Contact()
                if legal_representative.representante_legal.contato:
                    legal_representative_contact = Contact(
                        cellphone=legal_representative.representante_legal.contato.celular,
                        email=legal_representative.representante_legal.contato.email,
                        id=legal_representative.representante_legal.contato.id,
                        phone_number=legal_representative.representante_legal.contato.telefone_fixo,
                    )

                financial_product_legal_representative = LegalRepresentative()
                if legal_representative.representante_legal:
                    financial_product_legal_representative = LegalRepresentative(
                        address=legal_representative_address,
                        attribution_term_signature=legal_representative.representante_legal.atribuicao_termo_assinatura,
                        contact=legal_representative_contact,
                        document=legal_representative.representante_legal.documento,
                        id=legal_representative.representante_legal.id,
                        isolated_signature=legal_representative.representante_legal.assinatura_isolada,
                        marital_status=legal_representative.representante_legal.estado_civil,
                        name=legal_representative.representante_legal.nome,
                        profession={},
                        signature_endorsement=legal_representative.representante_legal.assinatura_endosso,
                    )
                legal_representatives.append(financial_product_legal_representative)

        return legal_representatives

    def _get_financial_product(self, financiamento: Any) -> FinancialProduct:
        financial_product = FinancialProduct()
        if not financiamento.contrato.produto_financeiro:
            return financial_product

        financial_product.address = self._get_financial_product_address(financiamento)
        financial_product.balance = financiamento.contrato.produto_financeiro.saldo
        financial_product.bank_data = self._get_financial_product_bank_data(financiamento)
        financial_product.cnab = financiamento.contrato.produto_financeiro.cnab
        financial_product.contact = {}
        financial_product.corporate_name = financiamento.contrato.produto_financeiro.razao_social
        financial_product.document = financiamento.contrato.produto_financeiro.cnpj
        financial_product.external_slug = financiamento.contrato.produto_financeiro.external_slug
        financial_product.id = financiamento.contrato.produto_financeiro.id
        financial_product.legal_representatives = self._get_financial_product_legal_representatives(financiamento)
        financial_product.name = financiamento.contrato.produto_financeiro.nome
        financial_product.slug = financiamento.contrato.produto_financeiro.slug
        financial_product.template = financiamento.contrato.produto_financeiro.template
        return financial_product

    def _get_financing(self, financiamento: Any) -> Financing:
        financing = Financing()
        if not financiamento.contrato:
            return financing

        if financiamento.cotacao.cet:
            financing.cet = financiamento.cotacao.cet
            financing.rate_type = financiamento.cotacao.cet[:3]

        financing.ccb_cession = financiamento.emprestimo.numero_ccb
        if financiamento.tipo_de_financiamento.tipo == TipoPessoa.PRODUTOR_RURAL:
            financing.ccb_cession = f"SFPR{financiamento.contrato.id}"

        if financiamento.emprestimo.data_geracao_ccb:
            financing.ccb_date = financiamento.emprestimo.data_geracao_ccb.strftime("%Y-%m-%d")

        if financiamento.emprestimo.data_de_vencimento:
            financing.first_installment_date = str(financiamento.emprestimo.data_de_vencimento)

        installment = self._get_installment(financiamento.cotacao.id)
        financing.annual_interest_rate = self._get_annual_interest_rate(installment.taxa_de_juros)
        financing.banking = financiamento.bancarizadora.nome
        financing.ccb = financiamento.emprestimo.numero_ccb
        financing.files = self._get_files(financiamento.id)
        financing.financial_product = self._get_financial_product(financiamento)
        financing.formalized_at = financiamento.emprestimo.created_at.strftime("%Y-%m-%d")
        financing.grace_period = financiamento.cotacao.carencia + 1
        financing.gross_amount = financiamento.cotacao.valor_do_projeto
        financing.id = financiamento.id
        financing.installment_amount = financiamento.emprestimo.parcela_contrato
        financing.installments_number = financiamento.cotacao.numero_de_parcelas
        financing.interest_fee = installment.taxa_de_juros
        financing.iof = financiamento.emprestimo.iof
        financing.ipca_type = self._get_ipca_type(financiamento.cotacao.ipca)
        financing.last_installment_date = self._get_last_installment_date(
            financiamento.emprestimo.data_de_vencimento, financiamento.cotacao.numero_de_parcelas
        )
        financing.registration_fee = installment.taxa_de_cadastro
        financing.securitization = financiamento.contrato.produto_financeiro.nome
        financing.status = self._get_validation_status(financiamento.id)
        financing.type = financiamento.tipo_de_financiamento.tipo

        return financing

    def _get_partner(self, financiamento: Any) -> Partner:
        partner = Partner()
        if financiamento.parceiro:
            partner = Partner(id=financiamento.parceiro.id, name=financiamento.parceiro.razao_social)

        return partner

    def _get_insurance(self, financiamento_id: int) -> list[Insurance]:
        seguros = (
            self.session_db.query(SeguroEmprestimo.valor_adicional_parcela, Seguro.nome, SeguroTipo.nome)
            .select_from(Financiamento)
            .join(Emprestimo, Emprestimo.id == Financiamento.emprestimo_id)
            .join(SeguroEmprestimo, SeguroEmprestimo.emprestimo_id == Emprestimo.id)
            .join(FinanciamentoSeguroTaxa, FinanciamentoSeguroTaxa.id == SeguroEmprestimo.financiamento_seguro_taxa_id)
            .join(SeguroTaxa, SeguroTaxa.id == FinanciamentoSeguroTaxa.seguro_taxa_id)
            .join(Seguro, Seguro.id == SeguroTaxa.seguro_id)
            .join(SeguroTipo, SeguroTipo.id == Seguro.tipo_id)
            .filter(Financiamento.id == financiamento_id)
            .all()
        )
        if seguros:
            result: list[Insurance] = []

            for seguro in seguros:
                result.append(Insurance(additional_installment_amount=seguro[0], name=seguro[1], type=seguro[2]))
            return result
        return []

    def _get_files_path(self, financiamento_id: int) -> str:
        path = (
            self.session_db.query(
                ProdutoFinanceiro.nome,
                Bancarizadora.nome,
                Contrato.upload_drive_data,
                TipoDeFinanciamento.tipo,
                Emprestimo.numero_ccb,
                Cliente.nome_completo,
                Empresa.razao_social,
            )
            .select_from(Financiamento)
            .join(Contrato, Financiamento.contrato_id == Contrato.id)
            .join(ProdutoFinanceiro, ProdutoFinanceiro.id == Contrato.produto_financeiro_id)
            .join(Bancarizadora, Bancarizadora.id == Financiamento.bancarizadora_id)
            .join(Emprestimo, Emprestimo.id == Financiamento.emprestimo_id)
            .join(TipoDeFinanciamento, TipoDeFinanciamento.id == Financiamento.tipo_id)
            .join(Empresa, Empresa.id == Financiamento.empresa_id, isouter=True)
            .join(Cliente, Cliente.id == Financiamento.cliente_id)
            .filter(Financiamento.id == financiamento_id)
            .first()
        )

        final_path = ""

        if path:
            produto_financeiro, bancarizadora, formalization_at, type, ccb_number, client_name, company_name = path
            finantial_product = "-".join(produto_financeiro.split())
            bank_name = bancarizadora.upper()
            year = formalization_at.year
            month = str(formalization_at.month)
            day = formalization_at.day

            name = ""
            if client_name:
                name = "_".join(client_name.lower().split())

            company = ""
            if company_name:
                company = "_".join(company_name.lower().split())

            month_name = get_month_by_number(formalization_at.month)
            final_path = f"{finantial_product}-{bank_name}/{year}/{month.zfill(2)}-{month_name}/{day}/{type}/{ccb_number}_{name}{company}"

        return final_path

    def _get_installment(self, cotacao_id: Any) -> Any:
        installment = (
            self.session_db.query(Parcela)
            .join(Cotacao, Cotacao.id == Parcela.cotacao_id)
            .filter(Parcela.cet == Cotacao.cet, Parcela.numero_de_parcelas == Cotacao.numero_de_parcelas)
            .filter(Parcela.cotacao_id == cotacao_id)
            .first()
        )
        return installment

    def _get_annual_interest_rate(self, interest_fee: float) -> float:
        value = (math.pow(1 + interest_fee / 100, 12) - 1) * 100
        return float(f"{value:.2f}")

    def _get_ipca_type(self, ipca: Any) -> str:
        if not ipca:
            return "annual"
        if ipca == "mensal":
            return "monthly"
        if ipca == "anual":
            return "annual"

    def _get_last_installment_date(self, first_installment_date: datetime, installments_number: int) -> str:
        final_date = first_installment_date + relativedelta(months=installments_number - 1)
        return final_date.strftime("%Y-%m-%d")

    def _get_user(self, user_id: int) -> Any:
        return self.session_db.query(Cliente).filter(Cliente.id == user_id).first()

    def _get_documents(self, financiamento_id: int) -> list[dict[str, Any]]:
        documents: list[dict[str, Any]] = []
        documents_: list[Document] = self._get_all_docs(financiamento_id)

        if documents_:
            for document in documents_:
                tipos = list(document.__dict__.keys())

                for tipo in tipos:
                    value = getattr(document, tipo)
                    is_guarantor = True if "avalista" in tipo else False

                    if value and isinstance(value, str):
                        comprovantes_documento_de_identidade = value.split("|")
                        for comprovante in comprovantes_documento_de_identidade[1:]:
                            try:
                                documento, financiamento_id_, tipo_comprovante, nome_arquivo = comprovante.split("/")
                            except ValueError:
                                pass

                            finally:
                                documents.append(
                                    {
                                        "is_guarantor": is_guarantor,
                                        "documento": documento,
                                        "financiamento_id": financiamento_id_,
                                        "tipo_comprovante": tipo_comprovante,
                                        "nome_arquivo": nome_arquivo,
                                    }
                                )

                    if value and isinstance(value, list):
                        for item in value:
                            try:
                                documento, financiamento_id_, _, tipo_comprovante, nome_arquivo = item["value"].split(
                                    "/"
                                )
                                documents.append(
                                    {
                                        "is_guarantor": is_guarantor,
                                        "documento": documento,
                                        "financiamento_id": financiamento_id_,
                                        "tipo_comprovante": tipo_comprovante,
                                        "nome_arquivo": nome_arquivo,
                                    }
                                )
                            except ValueError:
                                pass

        return documents

    def _get_files(self, financiamento_id: int) -> list[File]:
        documents = self._get_documents(financiamento_id)
        path = self._get_files_path(financiamento_id)

        files: list[File] = []
        if not documents:
            return files

        for document in documents:
            file = File(
                type=document["tipo_comprovante"],
                url=f"{path}/{document['nome_arquivo']}",
                is_guarantor=document["is_guarantor"],
            )
            files.append(file)

        return files

    def _get_validation_status(self, financiamento_id: int) -> str:
        validation = self.session_db.query(Validacao).filter(Validacao.financiamento_id == financiamento_id).first()
        if validation:
            return validation.status
        return ""

    def _get_all_docs(self, financiamento_id: int) -> list[Document]:
        query = text(
            f"""
                SELECT 
                    d.documento_de_identidade               client_documento_de_identidade,
                    d.documentos_adicionais                 client_documentos_adicionais,
                    d.comprovante_de_residencia             client_comprovante_de_residencia,
                    d.comprovante_de_renda                  client_comprovante_de_renda,
                    d.titularidade_do_imovel                client_titularidade_do_imovel,
                    d.comprovante_faturamento               client_comprovante_faturamento,
                    d.contrato_social                       client_contrato_social,
                    d.dap                                   client_dap,
                    d.comprovante_propriedade_rural         client_comprovante_propriedade_rural,
                    co.contrato_assinado                    client_contrato_assinado,

                    d2.documento_de_identidade              avalista_documento_de_identidade,
                    d2.documentos_adicionais                avalista_documentos_adicionais,
                    d2.comprovante_de_residencia            avalista_comprovante_de_residencia,
                    d2.comprovante_de_renda                 avalista_comprovante_de_renda,
                    d2.titularidade_do_imovel               avalista_titularidade_do_imovel,
                    d2.contrato_social                      avalista_contrato_social,
                    d2.dap                                  avalista_dap,
                    d2.comprovante_propriedade_rural        avalista_comprovante_propriedade_rural

                FROM financiamento f
                LEFT JOIN parceiro p    ON p.id = f.parceiro_id
                LEFT JOIN contrato co   ON co.id = f.contrato_id
                LEFT JOIN documento d   ON co.documento_cliente_id = d.id
                LEFT JOIN documento d2  ON co.documento_avalista_id = d2.id
                WHERE f.id = {financiamento_id}
               """
        )

        if financimento_info := self.session_db.execute(query).fetchall():
            return [Document(**financimento._mapping) for financimento in financimento_info]

        return []
