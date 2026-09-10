"""add person_id and target_object to sensors

Revision ID: 5233d8cd47e0
Revises: 0001_create_sensors
Create Date: 2026-09-10 21:11:54.481294
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5233d8cd47e0"
down_revision: Union[str, None] = "0001_create_sensors"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "sensors",
        sa.Column("person_id", sa.BigInteger(), nullable=True),
    )
    op.add_column(
        "sensors",
        sa.Column("target_object", sa.String(length=100), nullable=True),
    )

    # 기존 센서 데이터가 있어도 마이그레이션이 실패하지 않도록 임시 값 설정
    op.execute(
        "UPDATE sensors SET person_id = 0 WHERE person_id IS NULL"
    )
    op.execute(
        "UPDATE sensors SET target_object = 'UNKNOWN' WHERE target_object IS NULL"
    )

    op.alter_column(
        "sensors",
        "person_id",
        existing_type=sa.BigInteger(),
        nullable=False,
    )
    op.alter_column(
        "sensors",
        "target_object",
        existing_type=sa.String(length=100),
        nullable=False,
    )


def downgrade() -> None:
    op.drop_column("sensors", "target_object")
    op.drop_column("sensors", "person_id")