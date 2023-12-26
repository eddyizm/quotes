import sqlalchemy
from datetime import datetime
from databases import Database
from sqlalchemy.sql import func

from src.core.config import settings

DATABASE_URL = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'

database = Database(DATABASE_URL, min_size=5, max_size=20)
engine = sqlalchemy.create_engine(
    DATABASE_URL, echo = True
)
metadata = sqlalchemy.MetaData()



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
    'quotes_staging', # TODO add unique constraint for quote/author
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True,
    autoincrement=True, index=True),
    sqlalchemy.Column('category', sqlalchemy.String(25)),
    sqlalchemy.Column('quote', sqlalchemy.String(2000)),
    sqlalchemy.Column('author', sqlalchemy.String(50)),
    sqlalchemy.Column('added_to_quotes', sqlalchemy.Integer, nullable=False, server_default='0'),
    sqlalchemy.Column('added_by', sqlalchemy.String(50)),
    sqlalchemy.Column('date_created', sqlalchemy.DATE(), server_default=func.now())
    )

quote_history = sqlalchemy.Table(
    'quote_history',
    metadata,
    sqlalchemy.Column('date_sent', sqlalchemy.DATE(), primary_key=True, nullable=False),
    sqlalchemy.Column('quote_id_fk', sqlalchemy.Integer, nullable=False),
    ) 


async def connect_to_db():
    try:
        # TODO log this 
        print('trying to connect')
        return await database.connect()
    except:
        raise Exception('Unable to connect to database')
