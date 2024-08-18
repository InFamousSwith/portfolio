import os
import sys

from dotenv import dotenv_values

CONFIG = dotenv_values()
CURRENT_PATH = "/".join(sys.path[0].split("/")[:-1])
SQL_DIR = os.path.join(CURRENT_PATH, "..", "sql_scripts")


dbname = CONFIG["dbname"]
host = CONFIG["host"]
user = CONFIG["user"]
port = CONFIG["port"]


with open(os.path.join(SQL_DIR, "channel_names.sql"), "r", encoding="utf-8") as f:
    channels_query = f.read()
with open(os.path.join(SQL_DIR, "col_names.sql"), "r", encoding="utf-8") as f:
    sql_columns = f.read()
with open(os.path.join(SQL_DIR, "main_data.sql"), "r", encoding="utf-8") as f:
    sql_data = f.read()
