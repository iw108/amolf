"""Add v2 models

Revision ID: 3f3c30303617
Revises: feec4cef9d55
Create Date: 2024-08-22 12:28:35.945372

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3f3c30303617"
down_revision: Union[str, None] = "feec4cef9d55"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "data_archive_entries",
        sa.Column("id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("job_id", sa.Uuid(native_uuid=False), nullable=True),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "imaging_events",
        sa.Column("id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("ref_id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column(
            "type",
            sa.Enum("STITCH", "VIDEO", name="eventtype", native_enum=False),
            nullable=False,
        ),
        sa.Column("experiment_id", sa.String(), nullable=False),
        sa.Column("local_path", sa.String(), nullable=False),
        sa.Column("timestamp", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column(
            "system", sa.Enum("PRINCE", name="system", native_enum=False), nullable=True
        ),
        sa.Column("system_position", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "event_archives",
        sa.Column("id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("img_count", sa.Integer(), nullable=False),
        sa.Column("imaging_event_id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["imaging_event_id"],
            ["imaging_events.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "object_store_entries",
        sa.Column("id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("uploaded_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("imaging_event_id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["imaging_event_id"],
            ["imaging_events.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key"),
    )
    op.create_table(
        "archive_checksums",
        sa.Column("id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("hex", sa.String(), nullable=False),
        sa.Column(
            "algorithm",
            sa.Enum("SHA256", name="algorithm", native_enum=False),
            nullable=False,
        ),
        sa.Column("event_archive_id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["event_archive_id"],
            ["event_archives.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "data_archive_members",
        sa.Column("id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("member_key", sa.String(), nullable=False),
        sa.Column("src_key", sa.String(), nullable=False),
        sa.Column("data_archive_entry_id", sa.Uuid(native_uuid=False), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["data_archive_entry_id"],
            ["data_archive_entries.id"],
        ),
        sa.ForeignKeyConstraint(
            ["src_key"],
            ["object_store_entries.key"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("data_archive_members")
    op.drop_table("archive_checksums")
    op.drop_table("object_store_entries")
    op.drop_table("event_archives")
    op.drop_table("imaging_events")
    op.drop_table("data_archive_entries")
    # ### end Alembic commands ###
