import traceback
from dataclasses import dataclass
from typing import Any

from fastapi.encoders import jsonable_encoder
from loguru import logger
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.domain.common.exception_base import (
    InsertDBException,
    NotFoundException,
    SQLAlchemyException,
    UnprocessEntity,
    ValidationException,
)
from app.domain.common.legacy_model import Financiamento, Recebimento
from app.domain.common.service_base import ServiceBase
from app.domain.store.repository import StoreRepository
from app.domain.store.schema import Product, Shipping
from app.internal.config.settings import DEFAULT_EMAIL_PROVIDER, DEFAULT_STORE_PROVIDER
from app.internal.utils import exc_info


@dataclass
class StoreService(ServiceBase):
    repository: StoreRepository

    async def create_recebimento(
        self,
        order_id: int,
        items: list[Product],
        shipping: Shipping,
        subtotal: float,
        total: float,
        power: float,
        financing_id: int,
    ) -> Any:
        try:
            data = await self.repository.get_financing_data_by_financing_id(financing_id=financing_id)

            if not data:
                raise NotFoundException(f"financind_id {financing_id}")

            if not (
                (data.financing_stage == "analise_do_contrato" and data.financing_status == "aprovado")
                or (data.financing_stage == "recebimento" and data.financing_status == "em_andamento")
            ):
                raise UnprocessEntity(
                    stacktrace=[],
                    detail=f"financing_id {financing_id} does not have an approved analise_do_contrato or out of the recebimento stage",
                )

            marketplace_product_details = {
                "order_id": order_id,
                "items": items,
                "shipping": shipping,
                "subtotal": subtotal,
                "total": total,
                "power": power,
                "financing_id": financing_id,
            }

            receipt_model = Recebimento(
                marketplace_product_details=jsonable_encoder(marketplace_product_details),
                email_contato_fornecedor=DEFAULT_EMAIL_PROVIDER,
                fornecedor_id=DEFAULT_STORE_PROVIDER,
                valor_do_equipamento=total,
                integration_store=True,
                valor_diferenca_vkit=0,
            )

            if total > data.financing_value:
                receipt_model.valor_diferenca_vkit = total - data.financing_value

            recebimento_insert = await self.repository.save(receipt_model)

            logger.info(f"Receipt created: {recebimento_insert}")

            await self.repository.update(
                model=Financiamento, model_id=financing_id, values={"recebimento_id": recebimento_insert.id}
            )

            return {"mensage": f"Receipt created {recebimento_insert.id} for financing: {financing_id}"}

        except ValidationError as exc:
            raise ValidationException(stacktrace=traceback.format_exception_only(*exc_info())) from exc
        except IntegrityError as exc:
            raise InsertDBException(stacktrace=traceback.format_exception_only(*exc_info()), message=exc) from exc
        except SQLAlchemyError as exc:
            raise SQLAlchemyException(stacktrace=traceback.format_exception_only(*exc_info())) from exc
