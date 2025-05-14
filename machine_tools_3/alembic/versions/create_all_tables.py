"""create all tables with relationships

Revision ID: create_all_tables
Revises: None
Create Date: 2024-05-14 10:44:45.984336

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "create_all_tables"
down_revision: Union[str, None] = None  # Изменили с 'initial_migration' на None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем таблицу machine_tools с уникальным name
    op.create_table(
        "machine_tools",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("group", sa.Float(), nullable=True),
        sa.Column("type", sa.Float(), nullable=True),
        sa.Column("power", sa.Float(), nullable=True),
        sa.Column("efficiency", sa.Float(), nullable=True),
        sa.Column("accuracy", sa.String(), nullable=True),
        sa.Column("automation", sa.String(), nullable=True),
        sa.Column("specialization", sa.String(), nullable=True),
        sa.Column("weight", sa.Float(), nullable=True),
        sa.Column("weight_class", sa.String(), nullable=True),
        sa.Column("length", sa.Integer(), nullable=True),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("overall_diameter", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("manufacturer", sa.String(), nullable=True),
        sa.Column("machine_type", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_machine_tools_name"),
    )

    # Создаем таблицу technical_requirements
    op.create_table(
        "technical_requirements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("machine_name", sa.String(), nullable=False),
        sa.Column("requirement", sa.String(), nullable=False),
        sa.Column("value", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["machine_name"],
            ["machine_tools.name"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("technical_requirements")
    op.drop_table("machine_tools")
