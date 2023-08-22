"""change data type for add to quotes field

Revision ID: eec461539c08
Revises: a49237b86595
Create Date: 2023-05-19 22:16:04.109075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eec461539c08'
down_revision = 'a49237b86595'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('quotes_staging') as batch_op:
        batch_op.drop_column('added_to_quotes')
    
    with op.batch_alter_table('quotes_staging') as batch_op:
        batch_op.add_column(table_name='quotes_staging',
                  column=sa.Column(
                    'added_to_quotes',
                    sa.Integer(),
                    nullable=False,
                    server_default='0')
                )


def downgrade() -> None:
    pass
