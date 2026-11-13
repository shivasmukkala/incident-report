"""add case ownership fields

Revision ID: ddf144d81728
Revises: 83618569416d
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ddf144d81728"
down_revision: Union[str, Sequence[str], None] = "83618569416d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("cases") as batch_op:
        batch_op.add_column(
            sa.Column("reporter_user_id", sa.Integer(), nullable=True)
        )

        batch_op.add_column(
            sa.Column("assigned_to_user_id", sa.Integer(), nullable=True)
        )

        batch_op.create_index(
            "ix_cases_reporter_user_id",
            ["reporter_user_id"],
            unique=False,
        )

        batch_op.create_index(
            "ix_cases_assigned_to_user_id",
            ["assigned_to_user_id"],
            unique=False,
        )

        batch_op.create_foreign_key(
            "fk_cases_reporter_user_id_users",
            "users",
            ["reporter_user_id"],
            ["id"],
        )

        batch_op.create_foreign_key(
            "fk_cases_assigned_to_user_id_users",
            "users",
            ["assigned_to_user_id"],
            ["id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("cases") as batch_op:
        batch_op.drop_constraint(
            "fk_cases_assigned_to_user_id_users",
            type_="foreignkey",
        )

        batch_op.drop_constraint(
            "fk_cases_reporter_user_id_users",
            type_="foreignkey",
        )

        batch_op.drop_index("ix_cases_assigned_to_user_id")
        batch_op.drop_index("ix_cases_reporter_user_id")

        batch_op.drop_column("assigned_to_user_id")
        batch_op.drop_column("reporter_user_id")
