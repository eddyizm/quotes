"""drop and create random quote view

Revision ID: 925dfb3860f2
Revises: 
Create Date: 2023-05-05 10:42:56.946017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '925dfb3860f2'
down_revision = None
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
                WHERE quotes.id = (SELECT ABS(RANDOM()) % (5208 - 1) + 1);
            '''
    )


def downgrade() -> None:
    op.execute('DROP VIEW IF EXISTS randomQview;')
