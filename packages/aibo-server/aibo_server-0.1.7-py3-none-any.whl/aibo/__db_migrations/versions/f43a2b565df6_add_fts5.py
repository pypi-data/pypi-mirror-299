"""
Summary: add fts5

Migration information:
- Version: f43a2b565df6
- Previous version: 112ef53baf2c
- Created at: 2024-09-08 20:54:21.963289

"""
from typing import Any, Optional

import sqlalchemy as sa
from alembic import op

# ---[ Alembic ]-----------------------------------
revision: str = "f43a2b565df6"
down_revision: Optional[str] = "112ef53baf2c"
branch_labels: Optional[Any] = None
depends_on: Optional[Any] = None


# ---[ Migration ]---------------------------------
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("messages", schema=None) as batch_op:
        batch_op.alter_column("contents", existing_type=sa.VARCHAR(), nullable=False)

    # Create the FTS5 virtual table
    op.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS message_content_search
        USING fts5(message_id, conversation_id, content_text);
    """
    )

    # Backfill
    op.execute(
        """
        INSERT INTO message_content_search (message_id, conversation_id, content_text)
        SELECT id, conversation_id, content_text FROM messages;
    """
    )

    # Create triggers
    op.execute(
        """
        CREATE TRIGGER messages_on_insert AFTER INSERT ON messages
        BEGIN
            INSERT INTO message_content_search (message_id, conversation_id, content_text)
            VALUES (new.id, new.conversation_id, new.content_text);
        END;
    """
    )
    op.execute(
        """
        CREATE TRIGGER messages_on_update AFTER UPDATE ON messages
        WHEN old.content_text <> new.content_text
        BEGIN
            UPDATE message_content_search
            SET content_text = new.content_text
            WHERE message_id = old.id;
        END;
    """
    )
    op.execute(
        """
        CREATE TRIGGER messages_on_delete AFTER UPDATE OF deleted_at ON messages
        WHEN new.deleted_at IS NOT NULL
        BEGIN
            DELETE FROM message_content_search
            WHERE message_id = old.id;
        END;
    """
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Drop the triggers
    op.execute("DROP TRIGGER IF EXISTS messages_on_insert;")
    op.execute("DROP TRIGGER IF EXISTS messages_on_update;")
    op.execute("DROP TRIGGER IF EXISTS messages_on_delete;")

    # Drop the FTS5 table
    op.execute("DROP TABLE IF EXISTS message_content_search;")

    with op.batch_alter_table("messages", schema=None) as batch_op:
        batch_op.alter_column("contents", existing_type=sa.VARCHAR(), nullable=True)

    # ### end Alembic commands ###
