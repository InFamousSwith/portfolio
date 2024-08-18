import logging

import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import Date, Integer

simlog = logging.getLogger("ParserLogger")


class UseDatabase:
    "Класс инициализирует подключение к БД"

    def __init__(self, config: str) -> None:
        self.configuration = config

    def __enter__(self):  # -> create_engine:
        self.connection = create_engine(self.configuration).connect()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.connection.close()


def load_raw_data(CONNECTION_STRING: str, data: pd.DataFrame) -> None:
    "Загружает pd.DataFrame в БД"
    if data.empty:
        return None
    table_name = "ideas"
    simlog.info("Loading data in database ...")
    with UseDatabase(CONNECTION_STRING) as cnxn:
        data.to_sql(
            table_name,
            con=cnxn,
            schema="public",
            if_exists="append",
            index=False,
            method="multi",
            dtype={"channel_id": Integer(), "message_id": Integer(), "date": Date()},
        )
        cnxn.commit()
    simlog.info("Database is updated")


def simple_select(dbname: str, host: str, user: str, port: str, query: str) -> list:
    "Возвращает лист тюплов без названия колонок"
    with psycopg2.connect(dbname=dbname, host=host, user=user, port=port) as conn:
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
    return results


def load_exist_rows(dbname: str, host: str, user: str, port: str, query: str) -> pd.Series:
    results = simple_select(dbname, host, user, port, query)
    df = pd.DataFrame(data=results, columns=["key_id"])
    simlog.info("Existing rows were downloaded")
    return df["key_id"]


def select_db_cols(dbname: str, host: str, user: str, port: str, query: str) -> set:
    cols = simple_select(dbname, host, user, port, query)
    cols = set([el[0] for el in cols])
    return cols


def check_columns(df: pd.DataFrame, cols: set) -> None:
    assert set(cols).issubset(df.columns), simlog.error(f"NO column {set(cols).difference(df.columns)} in database")
