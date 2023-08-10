import traceback
from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError
from sqlalchemy.exc import OperationalError

from app.domain.common.exception_base import NotFoundException, SQLAlchemyException, ValidationException
from app.domain.common.service_base import ServiceBase
from app.domain.user.repository import UserRepository
from app.domain.user.schema import ContactResponse, PartnerResponse, UsersResponse
from app.enum import FinancingType
from app.internal.utils import exc_info


@dataclass
class UserService(ServiceBase):
    repository: UserRepository

    async def get_user(self, user_id: int) -> UsersResponse:
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
                complete_name=user.nome_completo,
                perfil=user.perfil,
            )

            return user_info

        except OperationalError as exc:
            raise SQLAlchemyException(stacktrace=traceback.format_exception_only(*exc_info())) from exc
        except ValidationError as exc:
            raise ValidationException(stacktrace=traceback.format_exception_only(*exc_info())) from exc

    async def get_eligible_store_financing(
        self, user_id: int, document: str = None, document_type: FinancingType = FinancingType.cpf
    ) -> Any:

        try:
            validate_user = await self.repository.valid_user(user_id=user_id)

            if not validate_user:
                raise NotFoundException(f"user_id {user_id}")

            if not document:
                return await self.repository.get_financing_MR_stage(user_id=user_id, document_type=document_type)

            return await self._get_financing_client(user_id=user_id, document=document, document_type=document_type)

        except OperationalError as exc:
            raise SQLAlchemyException(stacktrace=traceback.format_exception_only(*exc_info())) from exc
        except ValidationError as exc:
            raise ValidationException(stacktrace=traceback.format_exception_only(*exc_info())) from exc

    async def _get_financing_client(self, user_id: int, document: str, document_type: str) -> Any:
        valid_document = await self.repository.valid_document(document_type=document_type, document=document)

        if not valid_document:
            raise NotFoundException(f"Document {document} and {document_type}")
        return await self.repository.get_financing_MR_stage(
            user_id=user_id, document=document, document_type=document_type
        )
