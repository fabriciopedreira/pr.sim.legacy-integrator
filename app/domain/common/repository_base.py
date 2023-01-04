from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Type

from sqlalchemy.orm import Session

from app.domain.common.entity_model_base import EntityModelBase


@dataclass
class RepositoryBase:
    __abstract__ = True

    session_db: Session
    entity_model: Type[EntityModelBase]

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[tuple[Any]]:
        """Get all item from database, aplay pagination
        :param: skip: number of pagna to skip
        :param: limit: number of items to fetch

        :return: List[tuple[Any]]
        """
        return self.session_db.query(self.entity_model).offset(skip).limit(limit).all()

    async def get_by_id(self, model_id: int) -> Type[EntityModelBase] | None:
        """Get item by id
        :param: model_id: ID of the model

        :return: EntityModelBase or None
        :raises ``sqlalchemy.orm.exc.NoResultFound´´ or ``sqlalchemy.orm.exc.MultipleResultsFound``
        """
        return self.session_db.query(self.entity_model).filter_by(id=model_id).one()

    async def find_by_id(self, model_id: int) -> tuple[Any] | None:
        """Find first item by id
        :param: model_id: ID of the model

        :return: tuple[Any] or None
        """
        return self.session_db.query(self.entity_model).filter_by(id=model_id).first()

    async def get_all_by_create_at_range(self, from_datetime: datetime, to_datetime: datetime) -> List[tuple[Any]]:
        """Get all by created_at range
        :param: from_datetime: Init datatime
        :param: to_datetime: Ended datatime

        :return: List[tuple]
        """
        return (
            self.session_db.query(self.entity_model)
            .filter(self.entity_model.created_at >= from_datetime, self.entity_model.created_at <= to_datetime)
            .all()
        )

    async def save(self, model) -> EntityModelBase:
        """Save BaseModel into database
        :param: model: Model to save

        :return: Refresh model object
        """
        self.session_db.add(model)
        self.session_db.commit()
        self.session_db.refresh(model)

        return model

    async def update(self, model_id: int, values: Dict[str, Any], commit: Optional[bool] = True) -> tuple[Any] | None:
        """Update BaseModel in database
        :param model_id: ID of the model
        :param values: Dictionary values of the model to be updated
        :param commit: Optional commit in database

        :return: None
        """
        self.session_db.query(self.entity_model).filter_by(id=model_id).update(values)

        if commit:
            self.session_db.commit()
            return await self.find_by_id(model_id)

        return None

    async def delete(self, model: Optional[Type[EntityModelBase]]) -> None:
        """Delete row from database
        :param model: BaseModel to delete

        :return: None
        """
        self.session_db.delete(model)
        self.session_db.commit()
