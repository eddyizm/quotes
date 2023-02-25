import sqlalchemy
from datetime import datetime
from databases import Database
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.sql import func, expression

DATABASE_URL = 'sqlite:///./core/schema/quotes_app.sqlite3'

database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
    DATABASE_URL, echo = True, connect_args={'check_same_thread': False}
)

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True,
    autoincrement=True),
    sqlalchemy.Column('email', sqlalchemy.String, unique=True),
    sqlalchemy.Column('password', sqlalchemy.String),
    sqlalchemy.Column('is_active', sqlalchemy.Boolean, 
    server_default=sqlalchemy.sql.expression.false(), nullable=False)
    ) 

quotes = sqlalchemy.Table(
    'quotes',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True,
    autoincrement=True),
    sqlalchemy.Column('category', sqlalchemy.String(25)),
    sqlalchemy.Column('quote', sqlalchemy.String(2000)),
    sqlalchemy.Column('author', sqlalchemy.String(50)),
    sqlalchemy.Column('date_added', sqlalchemy.DATE(), default=datetime.now, nullable=False)
    )

quotes_staging = sqlalchemy.Table(
    'quotes_staging',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True,
    autoincrement=True),
    sqlalchemy.Column('category', sqlalchemy.String(25)),
    sqlalchemy.Column('quote', sqlalchemy.String(2000)),
    sqlalchemy.Column('author', sqlalchemy.String(50)),
    sqlalchemy.Column('added_to_quotes', sqlalchemy.BOOLEAN, server_default=expression.false()),
    sqlalchemy.Column('added_by', sqlalchemy.String(50)),
    sqlalchemy.Column('date_created', sqlalchemy.DATE(), server_default=func.now())
    )

quote_history = sqlalchemy.Table(
    'quote_history',
    metadata,
    sqlalchemy.Column('date_sent', sqlalchemy.DATE(), primary_key=True, nullable=False),
    sqlalchemy.Column('quote_id_fk', sqlalchemy.Integer, nullable=False),
    ) 

metadata.create_all(engine)