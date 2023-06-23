from sqlalchemy import select

from app.domain.common.legacy_model import Contato, EntityModelBase, Users
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
