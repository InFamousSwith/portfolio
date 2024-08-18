import config
import db_connection as db
import pandas as pd
from expander import TableEditor
from fastapi import FastAPI
from pydantic import BaseModel
from spacy_request import DataRecognizer
from ticker_filler import fill_ticker

app = FastAPI()


def download_from_db(sql_query: str = config.sql_query_get_ideas) -> pd.DataFrame:
    df = db.simple_pandas_select(connection_string=config.connection_string, sql_query=sql_query)
    return df


def update_all_processed(keys: list, sql_query: str = config.sql_update) -> None:
    for key in keys:
        db.run_sql(config.dbname, config.host, config.user, config.port, sql_query, key)


def insert_processed_keys():
    keys = db.simple_pandas_select(
        connection_string=config.connection_string,
        sql_query=config.sql_find_keys
        ).values.T[0]
    update_all_processed(keys, config.sql_insert_in_pk)


def add_entities(df):
    recognizer = DataRecognizer()
    df = recognizer.add_str_entities(df)
    df.dropna(subset=["entities"], inplace=True)
    return df


def expand(df):
    df = TableEditor().get_expanded_df(df)
    df.dropna(subset=["org"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def add_tickers(df):
    df = fill_ticker(df)
    return df


def add_primary_key(df):
    df.dropna(subset=config.drop_na_cols, inplace=True)
    df["key_id_ticker"] = df["key_id"] + "-" + df["ticker"]
    return df


def post_process(df):
    df = df[config.result_cols]
    df.drop_duplicates(subset=["key_id_ticker"], inplace=True)
    df["org"] = df["org"].apply(lambda x: x[:90])
    df.reset_index(drop=True, inplace=True)
    df[config.future_cols] = None
    return df


def fill_expectation_time(df: pd.DataFrame):
    for row, col in df.iterrows():
        if pd.isnull(df["expectation_time"].iloc[row]):
            df["expectation_time"][row] = 360
    return df


class book(BaseModel):
    start_date: str
    end_date: str


@app.get("/")
def test_job():
    return "Server is started"


@app.post("/expand_ideas")
def base(arg: book):
    insert_processed_keys()
    df = download_from_db()
    while not df.empty:
        keys = df["key_id"].unique()
        df = add_entities(df)
        df = expand(df)
        df = add_tickers(df)
        df = add_primary_key(df)
        df = post_process(df)
        df = fill_expectation_time(df)
        print(df.head())
        db.load_raw_data(table_name="prices", connection_string=config.connection_string, data=df)
        update_all_processed(keys)
        df = download_from_db()
    return "All ideas are recognized"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        config.FAST_NAME,
        host=config.FAST_HOST,
        port=config.FAST_PORT,
        # reload=True
    )
