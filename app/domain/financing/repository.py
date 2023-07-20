import uuid

from app.domain.common.legacy_model import Clicksign, Cotacao, EntityModelBase, Financiamento
from app.domain.common.repository_base import RepositoryBase


class FinancingRepository(RepositoryBase):
    async def save(self, model) -> EntityModelBase:
        self.session_db.add(model)
        self.session_db.commit()
        self.session_db.refresh(model)
        return model

    async def get_financing_by_project_id(self, project_id: uuid.UUID) -> EntityModelBase | None:

        result = (
            self.session_db.query(Financiamento.etapa, Financiamento.id)
            .join(Cotacao, Financiamento.cotacao_id == Cotacao.id)
            .filter(Cotacao.external_simulation_id == str(project_id))
            .one_or_none()
        )

        return result

    async def is_contract_clicksign_by_financing_id(self, financing_id: uuid.UUID) -> bool | None:

        result = (
            self.session_db.query(Clicksign)
            .join(Financiamento, Clicksign.financiamento_id == Financiamento.id)
            .filter(Financiamento.id == str(financing_id), Clicksign.tipo_documento == "contrato")
            .count()
        )

        return result >= 1
