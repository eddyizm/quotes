"""remove old views

Revision ID: a49237b86595
Revises: 925dfb3860f2
Create Date: 2023-05-19 22:12:44.925191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a49237b86595'
down_revision = '925dfb3860f2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('DROP VIEW IF EXISTS emailtoSend;')
    op.execute('DROP VIEW IF EXISTS quoteCounts;')


def downgrade() -> None:
    op.execute('DROP VIEW IF EXISTS emailtoSend;')
    op.execute('DROP VIEW IF EXISTS quoteCounts;')