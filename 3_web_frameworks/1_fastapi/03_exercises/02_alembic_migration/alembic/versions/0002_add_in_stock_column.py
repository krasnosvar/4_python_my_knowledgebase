"""add in_stock column to items

Revision ID: 0002
Revises: 0001
Create Date: 2026-01-02 00:00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # TODO: добавь колонку in_stock (Boolean, NOT NULL) к таблице items.
    # Важно: у уже существующих строк нет значения для новой NOT NULL колонки,
    # поэтому нужен server_default (значение по умолчанию на стороне БД) —
    # без него для существующих строк добавление NOT NULL колонки упадёт.
    #
    # op.add_column(
    #     "items",
    #     sa.Column("in_stock", sa.Boolean(), nullable=False, server_default="1"),
    # )
    pass


def downgrade() -> None:
    # TODO: удали колонку in_stock (обратная операция к upgrade()).
    # op.drop_column("items", "in_stock")
    pass
