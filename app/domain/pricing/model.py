from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy_utils import ChoiceType

from app.domain.common.entity_model_base import EntityModelBase as Base

OPERATORS = [
    (1, "SUM"),
    (0, "END"),
    (2, "EQUAL"),
]


class PricingCalculator(Base):
    __tablename__ = "pricing_calculators"

    name = Column(String(75), unique=True, nullable=False, index=True)
    description = Column(String(128), nullable=True)

    def __repr__(self):
        return f'<PricingCalculator(id={self.id}, name="{self.name}", description={self.description})>'


class PriceRule(Base):
    TYPES = [
        (1, "VALUE"),
        (2, "CALCULATE"),
    ]
    __tablename__ = "price_rules"

    name = Column(String(47), unique=True, nullable=False, index=True)
    type = Column(ChoiceType(TYPES), nullable=False)
    operator = Column(ChoiceType(OPERATORS), nullable=False)

    pricing_product_id = Column(
        BigInteger(), ForeignKey(f'{Base.__table_args__.get("schema")}.pricing_products.id'), nullable=True
    )
    next_price_rule_id = Column(
        BigInteger(), ForeignKey(f'{Base.__table_args__.get("schema")}.price_rules.id'), nullable=True
    )

    def __repr__(self):
        return f'<PriceRule(id={self.id}, name="{self.name}", type={self.type}, operator={self.operator})>'


class PriceStrategy(Base):
    __tablename__ = "price_strategies"

    operator = Column(ChoiceType(OPERATORS), nullable=False)

    first_rule_id = Column(
        BigInteger(), ForeignKey(f'{Base.__table_args__.get("schema")}.price_rules.id'), nullable=False
    )
    next_rule_id = Column(
        BigInteger(), ForeignKey(f'{Base.__table_args__.get("schema")}.price_rules.id'), nullable=False
    )
    pricing_calculator_id = Column(
        BigInteger(), ForeignKey(f'{Base.__table_args__.get("schema")}.pricing_calculators.id'), nullable=False
    )

    def __repr__(self):
        return f'<PriceStrategy(id={self.id}, operator="{self.operator}", first_rule_id={self.first_rule_id})>'
