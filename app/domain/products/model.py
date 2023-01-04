from sqlalchemy import Column, Float, String

from app.domain.common.entity_model_base import EntityModelBase as Base


class PricingProduct(Base):
    __tablename__ = "pricing_products"

    name = Column(String(75), unique=True, nullable=False, index=True)
    description = Column(String(128), nullable=True)
    value = Column(Float(asdecimal=True), default=0, nullable=False)

    def __repr__(self):
        return (
            f'<PricingProduct(id={self.id}, name="{self.name}", description="{self.description}", value={self.value})>'
        )
