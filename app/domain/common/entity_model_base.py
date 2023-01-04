from sqlalchemy import BigInteger, Column, DateTime
from sqlalchemy.sql import func

from app.database import Base
from app.internal.config import DATABASE_SCHEMA


class EntityModelBase(Base):
    __abstract__ = True
    __table_args__ = {"schema": DATABASE_SCHEMA}

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
