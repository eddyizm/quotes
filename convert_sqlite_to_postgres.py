import pandas as pd
import sqlalchemy

from core.schema import dal

sqlite_db = sqlalchemy.create_engine('sqlite:///core/schema/quotes_app.sqlite3')

TABLES = ['users', 'quotes', 'quotes_staging', 'quote_history']


def dump_to_csv(table):
    print(f'reading table: {table}')
    df = pd.read_sql_table(table, con=sqlite_db)
    print(f'dumping data to file')
    df.to_csv(f'data/{table}.csv', index=False, sep='|')

def main():
    for table in TABLES:
        dump_to_csv(table)


if __name__ == '__main__':
    main()