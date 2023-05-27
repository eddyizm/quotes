"""update random quote view

Revision ID: 56969752d52a
Revises: eec461539c08
Create Date: 2023-05-27 12:16:30.046331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56969752d52a'
down_revision = 'eec461539c08'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # drop view if it exists in order to overwrite it
    op.execute('DROP VIEW IF EXISTS randomQview;')
    # then recreate the latest version
    op.execute('''
        CREATE VIEW `randomQview` AS select quotes.quote AS quote, 
                quotes.author as author,			
                quotes.id AS id,
                quotes.category as category
                from quotes
                WHERE quotes.id = (SELECT ABS(RANDOM()) % (select count(*) -1 from quotes q) + 1);
            '''
    )


def downgrade() -> None:
    op.execute('DROP VIEW IF EXISTS randomQview;')
