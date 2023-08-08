from sqlalchemy import and_, or_

from app.domain.common.legacy_model import Cliente, Contato, Cotacao, EntityModelBase, Financiamento, Users
from app.domain.common.repository_base import RepositoryBase
from app.domain.user.schema import UserDTO


class UserRepository(RepositoryBase):
    async def get_information_user_by_id(self, user_id: int) -> UserDTO or None:
        """Get information of user by id
        :param: user_id: ID of the model

        :return: EntityModelBase or None
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

    async def get_financing_MR_stage_by_user_id(self, user_id: int) -> list[EntityModelBase]:
        """Get financing in Modelo de Recebimento of user by id
        :param: user_id: ID of the model

        :return: list[EntityModelBase]
        """
        result = (
            self.session_db.query(
                Financiamento.id.label("financing_id"),
                Financiamento.etapa.label("financing_stage"),
                Financiamento.status.label("financing_status"),
                Cotacao.nome_do_projeto.label("project_name"),
                Cliente.nome_completo.label("client_name"),
                Cotacao.valor_do_projeto.label("project_value"),
                Cliente.cpf.label("client_cpf"),
            )
            .join(Cotacao, Cotacao.id == Financiamento.cotacao_id)
            .join(Cliente, Cliente.id == Financiamento.cliente_id)
            .filter(
                Financiamento.user_id == user_id,
                or_(
                    and_(Financiamento.etapa == "analise_do_contrato", Financiamento.status == "aprovado"),
                    and_(Financiamento.etapa == "recebimento", Financiamento.status == "em_andamento"),
                ),
            )
            .all()
        )

        return result

    async def get_financing_by_user_id_and_client_document(
        self, user_id: int, client_cpf: int
    ) -> list[EntityModelBase]:
        """Get financing data by user_id and cpf of client
        :param:
            user_id: ID of the model
            document: cpf of client in financing
        :return: list[EntityModelBase]
        """
        result = (
            self.session_db.query(
                Financiamento.id.label("financing_id"),
                Financiamento.etapa.label("financing_stage"),
                Financiamento.status.label("financing_status"),
                Cotacao.nome_do_projeto.label("project_name"),
                Cliente.nome_completo.label("client_name"),
                Cotacao.valor_do_projeto.label("project_value"),
                Cliente.cpf.label("client_cpf"),
            )
            .join(Cotacao, Cotacao.id == Financiamento.cotacao_id)
            .join(Cliente, Cliente.id == Financiamento.cliente_id)
            .filter(
                Financiamento.user_id == user_id,
                Cliente.cpf == client_cpf,
            )
            .all()
        )

        return result

    async def valid_user(self, user_id: int) -> bool:
        user = self.session_db.query(Users.id).filter_by(id=user_id).one_or_none()

        return user is not None

    async def valid_document(self, client_cpf: str) -> bool:
        cpf = self.session_db.query(Cliente.cpf).filter_by(cpf=client_cpf).one_or_none()

        return cpf is not None
