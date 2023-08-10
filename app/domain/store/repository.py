from typing import Any, Dict, Optional

from sqlalchemy import update

from app.domain.common.legacy_model import Cotacao, EntityModelBase, Financiamento
from app.domain.common.repository_base import RepositoryBase


class StoreRepository(RepositoryBase):
    async def save(self, model) -> EntityModelBase:
        self.session_db.add(model)
        self.session_db.commit()
        self.session_db.refresh(model)
        return model

    async def update(
        self, model: EntityModelBase, model_id: int, values: Dict[str, Any], commit: Optional[bool] = True
    ) -> tuple[Any] | None:
        """Update BaseModel in database
        :param model: Model
        :param model_id: ID of the model
        :param values: Dictionary values of the model to be updated
        :param commit: Optional commit in database
        :return: mode_id or None
        """

        stmt = update(model).where(model.id == model_id).values(values)
        self.session_db.execute(stmt)

        if commit:
            self.session_db.commit()
            return model_id

    async def get_financing_data_by_financing_id(self, financing_id: int) -> EntityModelBase:
        """Get financing_value by financing_id
        :param: financing_id: ID of the Financiamento table

        :return: EntityModelBase
        """
        result = (
            self.session_db.query(
                Financiamento.etapa.label("financing_stage"),
                Financiamento.status.label("financing_status"),
                (Cotacao.valor_do_projeto - Cotacao.entrada).label("financing_value"),
            )
            .join(Cotacao, Cotacao.id == Financiamento.cotacao_id)
            .filter(Financiamento.id == financing_id)
            .one_or_none()
        )

        return result
