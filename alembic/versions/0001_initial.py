"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-05-27
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # sessions must be created before messages (messages.session_id FK references sessions.id)
    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("chat_id", sa.BigInteger(), nullable=False),
        sa.Column("tg_msg_ids", ARRAY(sa.BigInteger()), default=list),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, default="queued"),
        sa.Column("notion_page_id", sa.String(64), unique=True),
        sa.Column("github_file_path", sa.String(256)),
        sa.Column("structured_json", JSONB()),
        sa.Column("retry_count", sa.Integer(), default=0),
        sa.Column("last_error", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_sessions_status", "sessions", ["status"])

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("msg_id", sa.BigInteger(), nullable=False, unique=True),
        sa.Column("chat_id", sa.BigInteger(), nullable=False),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("text", sa.Text()),
        sa.Column("author_id", sa.BigInteger()),
        sa.Column("author_name", sa.String(256)),
        sa.Column("has_media", sa.Boolean(), default=False),
        sa.Column("media_type", sa.String(64)),
        sa.Column("grouped_id", sa.BigInteger()),
        sa.Column("reply_to_msg_id", sa.BigInteger()),
        sa.Column("transcription", sa.Text()),
        sa.Column("ocr_text", sa.Text()),
        sa.Column("link_metadata", JSONB()),
        sa.Column("session_id", sa.Integer(), sa.ForeignKey("sessions.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_messages_msg_id", "messages", ["msg_id"])
    op.create_index("ix_messages_chat_id", "messages", ["chat_id"])
    op.create_index("ix_messages_grouped_id", "messages", ["grouped_id"])
    op.create_index("ix_messages_session_id", "messages", ["session_id"])

    op.create_table(
        "knowledge_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.Integer(), sa.ForeignKey("sessions.id"), nullable=False),
        sa.Column("item_type", sa.String(32), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("owner", sa.String(256)),
        sa.Column("tags", ARRAY(sa.String()), default=list),
        sa.Column("status", sa.String(32), nullable=False, default="open"),
        sa.Column("notion_page_id", sa.String(64), unique=True),
        sa.Column("extra", JSONB()),
        sa.Column("date", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_knowledge_items_session_id", "knowledge_items", ["session_id"])

    op.create_table(
        "processing_logs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.Integer(), sa.ForeignKey("sessions.id")),
        sa.Column("stage", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("error", sa.Text()),
        sa.Column("details", JSONB()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_processing_logs_session_id", "processing_logs", ["session_id"])


def downgrade() -> None:
    op.drop_table("processing_logs")
    op.drop_table("knowledge_items")
    op.drop_table("messages")
    op.drop_table("sessions")
