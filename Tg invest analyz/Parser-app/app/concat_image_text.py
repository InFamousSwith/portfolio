import base64
import json
import logging
import os
from parser import clean_images

import pandas as pd
import requests
from config import IMGS_PATH

simlog = logging.getLogger("ParserLogger")


class Concatenator:
    """
    Класс преобразует json с сообщениями в таблицу с распознанными изображениями
    Методы
    ------
    concat_with_images(messages: list):
        Создает таблицу с нужными колонками, добавляет к ней текст с изображений
    """

    def concat_with_images(self, messages: list, image_job: bool) -> pd.DataFrame:
        """Создает таблицу с нужными колонками, добавляет к ней текст с изображений"""
        df = self._make_table_from_json(messages)
        df = self._add_text_of_idea(df, image_job)
        assert not df.empty, simlog.info("Text from images was NOT added")
        return df

    def _make_table_from_json(self, messages: list) -> pd.DataFrame:
        """Создает таблицу с нужными колонками из полученного в ходе парсинга json"""
        KEYS = ["peer_id", "id", "date", "message"]  # 'peer_id': {'_': 'PeerChannel', 'channel_id': 1083086642}

        def get_need_keys(message: dict) -> dict:
            new_message = {key: value for key, value in message.items() if key in KEYS}
            new_message["peer_id"] = new_message["peer_id"]["channel_id"]
            return new_message

        messages = list(map(get_need_keys, messages))
        df = pd.DataFrame(messages)
        simlog.info("table_from_json was created")
        return df

    def _extract_text(self, id: int) -> str:
        """Передает изображение по id в тессеракт
        возвращает текст изображения"""
        img_path = os.path.join(IMGS_PATH, f"parsed_jpg_{id}.jpg")
        try:
            img = base64.b64encode(open(img_path, "rb").read())
            response = requests.post("http://....:7777/extract_text", data={"img": img, "format": "jpg"})
            response = json.loads(response.text)
        except Exception:
            response = ""
        return response

    def _add_text_of_idea(self, df: pd.DataFrame, image_job: bool) -> pd.DataFrame:
        """Добавляет в таблицу колонку с распознанным текстом с изображений"""
        if image_job:
            simlog.info("Extracting text from images")
            df["image_text"] = df["id"].apply(lambda x: self._extract_text(x))
            clean_images(IMGS_PATH)
        else:
            df["image_text"] = ""
        return df
