from datetime import date, datetime, time
from typing import Any, List

from sqlalchemy import case

from app.domain.common.legacy_model import (
    Bancarizadora,
    Cessao,
    CessaoFormalizacao,
    Cliente,
    Contrato,
    Empresa,
    Emprestimo,
    Financiamento,
    Formalizacao,
    ProdutoFinanceiro,
    TipoDeFinanciamento,
)
from app.domain.common.repository_base import RepositoryBase


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
                        (TipoDeFinanciamento.tipo == "PF", Cliente.cpf),
                        (TipoDeFinanciamento.tipo == "PR", Cliente.cpf),
                        (TipoDeFinanciamento.tipo == "PJ", Empresa.cnpj),
                    ]
                ).label("client_document"),
                case(
                    [
                        (TipoDeFinanciamento.tipo == "PF", Cliente.nome_completo),
                        (TipoDeFinanciamento.tipo == "PR", Cliente.nome_completo),
                        (TipoDeFinanciamento.tipo == "PJ", Empresa.nome_fantasia),
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
