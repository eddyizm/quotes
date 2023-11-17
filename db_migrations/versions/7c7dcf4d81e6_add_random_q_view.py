"""add random q view

Revision ID: 7c7dcf4d81e6
Revises: 
Create Date: 2023-11-16 19:51:53.405137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c7dcf4d81e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('''
        CREATE view randow_quote_view  AS
            select quotes.quote AS quote, 
                quotes.author as author,			
                quotes.id AS id,
                quotes.category as category
            from quotes offset random() * (select count(*) from quotes) limit 1;
            ''')

def downgrade() -> None:
    op.execute('DROP VIEW [IF EXISTS] randow_quote_view')
