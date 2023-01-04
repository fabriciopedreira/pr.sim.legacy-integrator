"""create price_rules table

Revision ID: ceb9d755c585
Revises: 979e05ef63d8
Create Date: 2023-01-04 11:50:45.218947

"""
import sqlalchemy as sa

from alembic import op
from app.internal.config import DATABASE_SCHEMA

# revision identifiers, used by Alembic.
revision = "ceb9d755c585"
down_revision = "979e05ef63d8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "price_rules",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column("name", sa.String(47), unique=True, nullable=False, index=True),
        sa.Column("type", sa.Integer, nullable=False),
        sa.Column("operator", sa.Integer, nullable=True),
        sa.Column(
            "pricing_product_id",
            sa.BigInteger(),
            sa.ForeignKey(f"{DATABASE_SCHEMA}.pricing_products.id"),
            nullable=True,
        ),
        sa.Column(
            "next_price_rule_id", sa.BigInteger(), sa.ForeignKey(f"{DATABASE_SCHEMA}.price_rules.id"), nullable=True
        ),
    )


def downgrade() -> None:
    op.drop_table("price_rules")
