import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text


class UseDatabase:
    def __init__(self, config) -> None:
        self.configuration = config

    def __enter__(self):
        self.connection = create_engine(self.configuration).connect()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.connection.close()


def load_raw_data(table_name: str, connection_string: str, data: pd.DataFrame) -> None:
    "Загружает новые данные в таблицу"
    with UseDatabase(connection_string) as cnxn:
        data.to_sql(table_name, con=cnxn, schema="public", if_exists="append", index=False, method="multi")
        cnxn.commit()


def simple_pandas_select(connection_string: str, sql_query: str) -> pd.DataFrame:
    "Принимает SQL запрос, Обращается к БД, возвращает пандас таблицу"
    with UseDatabase(connection_string) as cnxn:
        df = pd.read_sql(text(sql_query), con=cnxn)
    return df


def run_sql(dbname, host, user, port, sql_query, *args):
    "Обновляет таблицу с обработанными ключами"
    sql_query = sql_query % args
    with psycopg2.connect(dbname=dbname, host=host, user=user, port=port) as conn:
        cur = conn.cursor()
        cur.execute(sql_query)
        conn.commit()
    return None
