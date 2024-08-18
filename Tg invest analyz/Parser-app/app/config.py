import os

from dotenv import dotenv_values

CONFIG = dotenv_values()

API_ID = CONFIG["API_ID"]
API_HASH = CONFIG["API_HASH"]
PHONE = CONFIG["PHONE"]
CONNECTION_STRING = CONFIG["CONNECTION_STRING"]

dbname = CONFIG["dbname"]
host = CONFIG["host"]
user = CONFIG["user"]
port = CONFIG["port"]

IMGS_PATH = os.path.join("..", "data", "imgs")
TRAIN_DS_PATH = os.path.join("..", "data", "data_for_ls.json")

QUERY_EXIST = "select key_id from ideas i where channel_id = %d"
QUERY_COLUMNS = """select column_name
from information_schema.columns
where table_schema='public' and table_name='ideas'"""
