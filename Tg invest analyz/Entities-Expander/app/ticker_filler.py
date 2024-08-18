import config
import pandas as pd
import db_connection as db
from fuzzy_searcher import FuzziSearcher


ticker_data = db.simple_pandas_select(connection_string=config.connection_string, sql_query=config.sql_query_get_tickers)

fuzzi_searcher = FuzziSearcher(ticker_data)

def check(row_index: int, df: pd.DataFrame):
    if df["ticker"].iloc[row_index] in ticker_data["ticker"]:
        return df["ticker"].iloc[row_index]
    elif pd.isnull(df["org"].iloc[row_index]):
        return "Error"
    elif df["org"].iloc[row_index] in ticker_data["name"]:
        return ticker_data[ticker_data["name"] == df["org"].iloc[row_index]]["ticker"].iloc[0]
    else:
        ticker = fuzzi_searcher.get_one_ticker(df["org"].iloc[row_index])
        return ticker

def fill_ticker(df: pd.DataFrame):
    df.reset_index(drop=True, inplace=True)
    for row, col in df.iterrows():
        df["ticker"].iloc[row] = check(row, df)
    return df
