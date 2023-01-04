"""create pricing_calculators table

Revision ID: 979e05ef63d8
Revises: 07367e1e46ab
Create Date: 2023-01-04 11:49:00.536790

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "979e05ef63d8"
down_revision = "07367e1e46ab"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "pricing_calculators",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column("name", sa.String(75), unique=True, nullable=False, index=True),
        sa.Column("description", sa.String(128), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("pricing_calculators")
