from app.domain.common.legacy_model import EntityModelBase
from app.domain.common.repository_base import RepositoryBase


class FinancingRepository(RepositoryBase):
    async def save(self, model) -> EntityModelBase:
        self.session_db.add(model)
        self.session_db.commit()
        self.session_db.refresh(model)
        return model
