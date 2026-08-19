"""create animals table

Revision ID: a53b4133082e
Revises: f3d313e6cae7
Create Date: 2026-08-20 00:03:50.579258

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a53b4133082e"
down_revision: Union[str, Sequence[str], None] = "f3d313e6cae7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "animals",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column(
            "species",
            sa.Enum("cane", "gatto", name="species_enum"),
            nullable=False,
        ),
        sa.Column("breed", sa.String(length=100), nullable=True),
        sa.Column(
            "size",
            sa.Enum(
                "piccola",
                "media",
                "grande",
                "gigante",
                name="size_enum",
            ),
            nullable=True,
        ),
        sa.Column(
            "coat_type",
            sa.Enum(
                "corto",
                "medio",
                "lungo",
                "riccio_doppio_strato",
                name="coat_type_enum",
            ),
            nullable=True,
        ),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["clients.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_animals_client_id"),
        "animals",
        ["client_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_animals_client_id"),
        table_name="animals",
    )
    op.drop_table("animals")

    op.execute("DROP TYPE IF EXISTS coat_type_enum")
    op.execute("DROP TYPE IF EXISTS size_enum")
    op.execute("DROP TYPE IF EXISTS species_enum")