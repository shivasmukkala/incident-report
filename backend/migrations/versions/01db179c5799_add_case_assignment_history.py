
"""add case assignment history

Revision ID: 01db179c5799
Revises: ddf144d81728
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "01db179c5799"
down_revision: Union[str, Sequence[str], None] = "ddf144d81728"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "case_assignment_history",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("case_id", sa.Integer(), nullable=False),
        sa.Column("previous_assignee_id", sa.Integer(), nullable=True),
        sa.Column("new_assignee_id", sa.Integer(), nullable=False),
        sa.Column("assigned_by", sa.Integer(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["case_id"],
            ["cases.id"],
            name="fk_case_assignment_history_case_id_cases",
        ),
        sa.ForeignKeyConstraint(
            ["previous_assignee_id"],
            ["users.id"],
            name="fk_case_assignment_history_previous_assignee_users",
        ),
        sa.ForeignKeyConstraint(
            ["new_assignee_id"],
            ["users.id"],
            name="fk_case_assignment_history_new_assignee_users",
        ),
        sa.ForeignKeyConstraint(
            ["assigned_by"],
            ["users.id"],
            name="fk_case_assignment_history_assigned_by_users",
        ),
    )

    op.create_index(
        "ix_case_assignment_history_case_id",
        "case_assignment_history",
        ["case_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_case_assignment_history_case_id",
        table_name="case_assignment_history",
    )
    op.drop_table("case_assignment_history")
