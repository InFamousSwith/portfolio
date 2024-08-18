import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from parser import parse_channel_job

import config
import db_uploader as db

# import xlsxwriter
# import pandas as pd
from clean_data import DataCleaner
from concat_image_text import Concatenator
from flask import Flask, request

FLASK_DEBUG = False
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

app = Flask("Parser")

LOGFILENAME = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "parser.log")
simlog = logging.getLogger("ParserLogger")
simlog.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(module)-16s - %(levelname)-4s %(message)s", "%d-%m-%Y %H:%M:%S")
handler = RotatingFileHandler(LOGFILENAME, maxBytes=20485760, backupCount=10, encoding="utf-8")
handler.setFormatter(formatter)
simlog.addHandler(handler)


@app.route("/parse_channel", methods=["POST"])
def parse_job():
    """Принимает url канала, флаги, нужна ли обработка изображений и нужен ли датасет для разметки,
    Запускает парсинг и загрузку в базу
    Возвращает сообщение об успешности загрузки в случае успеха"""
    keys = {"channel_url", "image_job", "if_train_dataset"}

    content = request.get_json()
    if not keys.issubset(set(content.keys())):
        exeption = "Keys were not recieved: " + (", ").join(keys.difference(content.keys()))
        simlog.debug(f"{exeption}")
        return exeption
    simlog.info("request completed")

    channel_url = content["channel_url"]
    all_messages = parse_channel_job(channel_url, content["image_job"])
    df_with_imgs_text = Concatenator().concat_with_images(all_messages, content["image_job"])
    query = config.QUERY_EXIST % df_with_imgs_text["peer_id"][0]  # Таблица точно не пустая
    exist_rows = db.load_exist_rows(config.dbname, config.host, config.user, config.port, query)
    full_df = DataCleaner(config.TRAIN_DS_PATH).clean_messages(
        channel_url, df_with_imgs_text, exist_rows, content["if_train_dataset"]
    )
    if full_df.empty:
        simlog.info("Database is NOT updated, df is empty")
        return "Database is NOT updated, df is empty"
    db_columns = db.select_db_cols(config.dbname, config.host, config.user, config.port, config.QUERY_COLUMNS)
    db.check_columns(full_df, db_columns)
    db.load_raw_data(config.CONNECTION_STRING, full_df)
    return f"Database is updated with channel {channel_url}"


if __name__ == "__main__":
    simlog.info("-" * 50)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG, threaded=False)
    simlog.removeHandler(handler)
    del simlog

    # ---------Закомментировать все строки сверху, если необходимо проверить результат работы сервиса в таблице excel--------
    # ---------Раскоментировать все строки снизу, если необходимо проверить результат работы сервиса в таблице excel---------

    # writer = pd.ExcelWriter('df.xlsx', engine='xlsxwriter')
    # all_messages = parse_channel_job('https://t.me/inv_put', True)
    # df_with_imgs_text = Concatenator().concat_with_images(all_messages, False)
    # query = config.QUERY_EXIST % df_with_imgs_text["peer_id"][0]
    # exist_rows = db.load_exist_rows(config.dbname, config.host, config.user, config.port, query)
    # full_df = DataCleaner(config.TRAIN_DS_PATH).clean_messages(
    #     'https://t.me/Russia_Stocks', df_with_imgs_text, exist_rows, False)
    # full_df.to_excel(writer)
    # writer.close()
