import traceback
from dataclasses import dataclass

from pydantic import ValidationError
from sqlalchemy.exc import OperationalError

from app.domain.common.exception_base import NotFoundException, SQLAlchemyException, ValidationException
from app.domain.common.service_base import ServiceBase
from app.domain.user.repository import UserRepository
from app.domain.user.schema import ContactResponse, PartnerResponse, UsersResponse
from app.internal.utils import exc_info


@dataclass
class UserService(ServiceBase):
    repository: UserRepository

    async def get_user(self, user_id: int):
        try:
            user = await self.repository.get_information_user_by_id(user_id)

            if user is None:
                raise NotFoundException(f"Client_id {user_id} not found")

            contact = ContactResponse(
                id=user.contato_id,
                email=user.contato_email,
                phone=user.contato_celular,
            )

            partner = PartnerResponse(
                id=user.parceiro_id,
            )

            user_info = UsersResponse(
                id=user.id,
                confirmed=user.confirmed,
                contact=contact,
                partner=partner,
                functionPrincipal="loading...",
                complete_name=user.nome_completo,
                perfil=user.perfil,
            )

            return user_info

        except OperationalError as exc:
            raise SQLAlchemyException(stacktrace=traceback.format_exception_only(*exc_info())) from exc
        except ValidationError as exc:
            raise ValidationException(stacktrace=traceback.format_exception_only(*exc_info())) from exc
