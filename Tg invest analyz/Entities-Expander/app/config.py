import os

from dotenv import dotenv_values

CONFIG = dotenv_values()

fuzzy_treshhold = 0.6
spacy_port = "8560"

FAST_NAME = "server_app:app"
FAST_HOST = "0.0.0.0"
FAST_PORT = "5000"

dbname = CONFIG["dbname"]
host = CONFIG["host"]
user = CONFIG["user"]
port = CONFIG["port"]
connection_string = f"postgresql+psycopg2://{user}@{host}:{port}/{dbname}"

spacy_url = f"http://....:{spacy_port}/recognize"


def read_sql_script(name: str):
    with open(os.path.join("sql", name), "r", encoding="utf-8") as script:
        query = script.read()
    return query


sql_query_get_ideas = read_sql_script("ideas.sql")
sql_query_get_tickers = read_sql_script("tickers.sql")
sql_update = read_sql_script("update.sql")
sql_find_keys = read_sql_script("find_keys.sql")
sql_insert_in_pk = read_sql_script("insert_in_pk.sql")


entities_naming = {
    "ORG": "org",
    "PERCENT": "percentage",
    "TIME": "expectation_time",
    "ACT": "act",
    "TICKER": "ticker",
    "PRICE": "current_price",
}

result_cols = [
    "key_id",
    "key_id_ticker",
    "org",
    "ticker",
    "message_date",
    "current_price",
    "act",
    "percentage",
    "expectation_time",
]
future_cols = [
    "target_date",
    "target_price",
    "real_price",
    "real_date",
    "real_time",
    "low",
    "high",
    "if_good_idea",
    "real_sell_price",
    "real_profit",
    "absolute_100_profit",
    "year_profit",
    "price_sim",
    "real_percent_profit",
]

drop_na_cols = [
    "ticker",
    "act",
    "percentage",
    # "expectation_time"
]

"""
Ранее сохраняли наны в таблицу prices чтобы не обрабатывать несколько раз одни и те же сообщения.
Добавлена таблица processed_keys, где хранятся key_id и флаг обработано ли сообщение. Теперь нет необходимости
сохранять наны в таблицу
"""
