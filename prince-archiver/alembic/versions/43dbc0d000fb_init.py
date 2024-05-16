"""Init

Revision ID: 43dbc0d000fb
Revises:
Create Date: 2024-05-16 08:40:12.847941

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "43dbc0d000fb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "prince_timestep",
        sa.Column("timestep_id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("experiment_id", sa.String(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("img_count", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("local_dir", sa.String(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("timestep_id"),
    )
    op.create_table(
        "data_archive_entry",
        sa.Column("id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("timestep_id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("job_id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("file", sa.String(), nullable=False),
        sa.Column("archive_path", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["timestep_id"],
            ["prince_timestep.timestep_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "object_store_entry",
        sa.Column("id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("timestep_id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("bucket", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["timestep_id"],
            ["prince_timestep.timestep_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "deletion_event",
        sa.Column("id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("object_store_entry_id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("job_id", sa.Uuid(native_uuid=False), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["object_store_entry_id"],
            ["object_store_entry.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("deletion_event")
    op.drop_table("object_store_entry")
    op.drop_table("data_archive_entry")
    op.drop_table("prince_timestep")
    # ### end Alembic commands ###