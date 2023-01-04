"""create price_strategies table

Revision ID: 85ffbec7af9e
Revises: ceb9d755c585
Create Date: 2023-01-04 12:03:25.981656

"""
import sqlalchemy as sa

from alembic import op
from app.internal.config import DATABASE_SCHEMA

# revision identifiers, used by Alembic.
revision = "85ffbec7af9e"
down_revision = "ceb9d755c585"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "price_strategies",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column("operator", sa.Integer, nullable=True),
        sa.Column("first_rule_id", sa.BigInteger(), sa.ForeignKey(f"{DATABASE_SCHEMA}.price_rules.id"), nullable=False),
        sa.Column("next_rule_id", sa.BigInteger(), sa.ForeignKey(f"{DATABASE_SCHEMA}.price_rules.id"), nullable=False),
        sa.Column(
            "pricing_calculator_id",
            sa.BigInteger(),
            sa.ForeignKey(f"{DATABASE_SCHEMA}.pricing_calculators.id"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("price_strategies")
