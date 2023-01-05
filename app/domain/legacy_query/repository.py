from datetime import datetime, time
from typing import Any, List

from app.domain.common.legacy_model import (
    Cessao,
    CessaoFormalizacao,
    Cliente,
    Contrato,
    Emprestimo,
    Financiamento,
    Formalizacao,
    ProdutoFinanceiro,
    TipoDeFinanciamento,
)
from app.domain.common.repository_base import RepositoryBase


class Repository(RepositoryBase):
    async def find_formalizations_by_session_data_and_product_slug(
        self, session_data, product_slug
    ) -> List[tuple[Any]]:
        """Find all formalization
        :param: session_data: create_at from session
        :param: product_slug: slug from financial product

        :return: query result
        """
        return (
            self.session_db.query(
                Financiamento,
                Emprestimo.numero_ccb,
                Cliente.cpf,
                Cliente.nome_completo,
                TipoDeFinanciamento.tipo,
                Contrato.created_at,
            )
            .join(Contrato, Contrato.id == Financiamento.contrato_id)
            .join(Emprestimo, Emprestimo.id == Financiamento.emprestimo_id)
            .join(Cliente, Cliente.id == Financiamento.cliente_id)
            .join(ProdutoFinanceiro, ProdutoFinanceiro.id == Contrato.produto_financeiro_id)
            .join(TipoDeFinanciamento, TipoDeFinanciamento.id == Financiamento.tipo_id)
            .join(Formalizacao, Formalizacao.financiamento_id == Financiamento.id)
            .join(CessaoFormalizacao, CessaoFormalizacao.formalizacao_id == Formalizacao.id)
            .join(Cessao, Cessao.id == CessaoFormalizacao.cessao_id)
            .filter(
                Cessao.created_at >= datetime.combine(session_data, time.min),
                Cessao.created_at <= datetime.combine(session_data, time.max),
                ProdutoFinanceiro.slug == product_slug,
            )
            .all()
        )
