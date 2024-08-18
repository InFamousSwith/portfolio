import json

import config_server as config
import pandas as pd
import psycopg2
import requests
from flask import Flask, request

app = Flask("Parser")

# -----------------------------PARSER-----------------------------


def run_parser_request(input_json: dict) -> str:
    response = requests.post(config.PARSER_URL, json=input_json)
    print(response.text)


# -----------------------------EXPANDER-----------------------------


def run_expander_request(input_json: dict) -> str:
    response = requests.post(config.EXPANDER_URL, json=input_json)
    print(response.text)


# -----------------------------MOEX-----------------------------


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
    r = requests.post(config.MOEX_URL, json=json.dumps(input_json))  # , indent=4, sort_keys=True, default=str),
    return r.text


def run_moex_requests():
    results = simple_select(config.dbname, config.host, config.user, config.port, config.sql_query)
    df = make_df(results, config.cols)  # .head()
    for _, col in df.iterrows():
        req = col.to_json(orient="index")
        print(make_request(json.loads(req)))


# -----------------------------APP-----------------------------


@app.route("/all_serv", methods=["POST"])
def run_all():
    content = request.get_json()
    keys = {"json_for_parser", "json_for_expander"}
    if not keys.issubset(set(content.keys())):
        exeption = "Keys were not recieved: " + (", ").join(keys.difference(content.keys()))
        return exeption
    run_parser_request(content["json_for_parser"])
    run_expander_request(content["json_for_expander"])
    run_moex_requests()
    return "All servics have successfully shut down"


if __name__ == "__main__":
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.FLASK_DEBUG, threaded=False)
