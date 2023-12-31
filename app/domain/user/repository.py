from typing import Any

from sqlalchemy import and_, or_

from app.domain.common.legacy_model import Cliente, Contato, Cotacao, Empresa, Financiamento, Users, Projeto
from app.domain.common.repository_base import RepositoryBase
from app.domain.user.schema import UserDTO
from app.enum import FinancingType


class UserRepository(RepositoryBase):
    async def get_information_user_by_id(self, user_id: int) -> UserDTO or None:
        """Get information of user by id
        :param: user_id: ID of the model

        :return: UserDTO or None
        """
        result = (
            self.session_db.query(
                Users.id,
                Users.confirmed,
                Users.parceiro_id,
                Users.nome_completo,
                Users.perfil,
                Contato.id,
                Contato.celular,
                Contato.email,
            )
            .filter_by(id=user_id)
            .join(Contato, Users.contato_id == Contato.id)
            .one_or_none()
        )

        if result:
            result = UserDTO(
                id=result[0],
                confirmed=result[1],
                parceiro_id=result[2],
                nome_completo=result[3],
                perfil=result[4],
                contato_id=result[5],
                contato_celular=result[6],
                contato_email=result[7],
            )

        return result

    async def get_financing_MR_stage(
        self, user_id: int, document_type: FinancingType, document: str = None
    ) -> list[Any]:
        """
        Retrieves the financing stage for a given user and document.

        Args:
            user_id (int): The ID of the user.
            document_type (str): The type of document (CPF or CNPJ).
            document (str, optional): The document number. Defaults to None.

        Returns:
            list[EntityModelBase]: A list of EntityModelBase objects representing the financing stage.
        """

        dynamic_document_filter = (
            (Cliente.cpf == document if document_type == FinancingType.cpf else Empresa.cnpj == document)
            if document
            else True
        )

        query_dynamic_join = (
            (Cliente, Cliente.id == Financiamento.cliente_id)
            if document_type == FinancingType.cpf
            else (Empresa, Empresa.id == Financiamento.empresa_id)
        )

        query_client_name = Cliente.nome_completo if document_type == FinancingType.cpf else Empresa.nome_fantasia
        query_client_document = Cliente.cpf if document_type == FinancingType.cpf else Empresa.cnpj

        result = (
            self.session_db.query(
                Financiamento.id.label("financing_id"),
                Financiamento.etapa.label("financing_stage"),
                Financiamento.status.label("financing_status"),
                Cotacao.nome_do_projeto.label("project_name"),
                Cotacao.valor_do_projeto.label("project_value"),
                Projeto.potencia_original_do_sistema.label("project_system_potency"),
                query_client_name.label("client_name"),
                query_client_document.label("document"),
            )
            .join(Cotacao, Cotacao.id == Financiamento.cotacao_id)
            .join(Projeto, Projeto.id == Financiamento.projeto_id)
            .join(query_dynamic_join)
            .filter(
                Financiamento.user_id == user_id,
                dynamic_document_filter,
                or_(
                    and_(Financiamento.etapa == "analise_do_contrato", Financiamento.status == "aprovado"),
                    and_(Financiamento.etapa == "recebimento", Financiamento.status == "em_andamento"),
                ),
            )
            .all()
        )

        return result

    async def valid_user(self, user_id: int) -> bool:
        query = self.session_db.query(Users.id).filter_by(id=user_id).first()

        return query is not None

    async def valid_document(self, document_type: str, document: str) -> bool:
        if document_type == FinancingType.cpf:
            query = self.session_db.query(Cliente.cpf).filter_by(cpf=document).first()

        elif document_type == FinancingType.cnpj:
            query = self.session_db.query(Empresa.cnpj).filter_by(cnpj=document).first()

        else:
            return False

        return query is not None
