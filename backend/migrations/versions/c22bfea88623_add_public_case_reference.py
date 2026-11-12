
"""add public case reference

Revision ID: c22bfea88623
Revises: 42880f547cc3
"""

import secrets
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "c22bfea88623"
down_revision: Union[str, Sequence[str], None] = "42880f547cc3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add the column as nullable temporarily.
    op.add_column(
        "cases",
        sa.Column("reference", sa.String(length=19), nullable=True),
    )

    # 2. Populate references for existing cases.
    connection = op.get_bind()

    existing_ids = connection.execute(
        sa.text("SELECT id FROM cases")
    ).scalars().all()

    for case_id in existing_ids:
        reference = f"IR-{secrets.token_hex(8).upper()}"

        connection.execute(
            sa.text(
                "UPDATE cases SET reference = :reference WHERE id = :case_id"
            ),
            {"reference": reference, "case_id": case_id},
        )

    # 3. Enforce NOT NULL and uniqueness.
    with op.batch_alter_table("cases") as batch_op:
        batch_op.alter_column(
            "reference",
            existing_type=sa.String(length=19),
            nullable=False,
        )
        batch_op.create_unique_constraint(
            "uq_cases_reference",
            ["reference"],
        )


def downgrade() -> None:
    with op.batch_alter_table("cases") as batch_op:
        batch_op.drop_constraint(
            "uq_cases_reference",
            type_="unique",
        )
        batch_op.drop_column("reference")
