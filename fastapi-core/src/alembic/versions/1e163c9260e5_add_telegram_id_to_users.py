"""add_telegram_id_to_users

Revision ID: 1e163c9260e5
Revises: 05038ce22d2a
Create Date: 2026-06-21 17:15:23.296345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1e163c9260e5'
down_revision: Union[str, Sequence[str], None] = '05038ce22d2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Добавляем колонку telegram_id в таблицу users
    op.add_column('users', sa.Column('telegram_id', sa.BigInteger(), nullable=True))

    # Создаем ограничение уникальности, чтобы один аккаунт ТГ нельзя было привязать к двум юзерам
    op.create_unique_constraint('uq_users_telegram_id', 'users', ['telegram_id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Если захотим откатить миграцию — просто удаляем это поле и ограничение
    op.drop_constraint('uq_users_telegram_id', 'users', type_='unique')
    op.drop_column('users', 'telegram_id')