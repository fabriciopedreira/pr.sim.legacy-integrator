"""create product_pricing table

Revision ID: 07367e1e46ab
Revises: pass
Create Date: 2023-01-04 08:28:54.272358

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "07367e1e46ab"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "pricing_products",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column("name", sa.String(75), unique=True, nullable=False, index=True),
        sa.Column("description", sa.String(128), nullable=True),
        sa.Column("value", sa.Float(asdecimal=True)),
    )


def downgrade() -> None:
    op.drop_table("pricing_products")
