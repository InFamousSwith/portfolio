import json

import config_client as config
import pandas as pd
import psycopg2
import requests


def simple_select(dbname, host, user, port, sql_query) -> list:
    "Возвращает лист тюплов без названия колонок"
    with psycopg2.connect(dbname=dbname, host=host, user=user, port=port) as conn:
        cur = conn.cursor()
        cur.execute(sql_query)
        results = cur.fetchall()
    return results


def make_df(results, cols):
    df = pd.DataFrame(data=results, columns=cols)
    assert "message_date" in df.columns
    assert "ticker" in df.columns
    df["message_date"] = df["message_date"].astype(str)
    df["ticker"] = df["ticker"].astype(str)
    return df


def make_request(input_json: dict) -> str:
    r = requests.post(
        f"http://{config.SERVER_HOST}:{config.SERVER_PORT}/add_moex_data", json=json.dumps(input_json)
    )  # , indent=4, sort_keys=True, default=str),
    return r.text


def run_requests():
    results = simple_select(config.dbname, config.host, config.user, config.port, config.sql_query)
    df = make_df(results, config.cols)  # .head()
    for _, col in df.iterrows():
        req = col.to_json(orient="index")
        print(make_request(json.loads(req)))


if __name__ == "__main__":
    run_requests()

    # OR
    # # данные для тестов
    # from datetime import date
    # buy_json = {
    #     "key_id_ticker": "123-12-NVTK",
    #     "ticker": "NVTK",
    #     "message_date": date(2023, 3, 27),
    #     "act": "BUY",
    #     "percentage": 93.0,
    #     "expectation_time": 90.0,
    # }
    # sell_json = {
    #     "key_id_ticker": "123-12-HYDR",
    #     "ticker": "HYDR",
    #     "message_date": date(2022, 8, 23),
    #     "act": "SELL",
    #     "percentage": 40,
    #     "expectation_time": 120.0,
    # }

    # print(make_request(buy_json))
    # print(make_request(sell_json))
