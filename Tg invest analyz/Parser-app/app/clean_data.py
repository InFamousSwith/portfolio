import json
import logging
import re

import emoji
import pandas as pd

simlog = logging.getLogger("ParserLogger")


class DataCleaner:
    """
    Класс для очистки текста от тех. символов, дубликатов и емодзи.
    Атрибуты
    --------
    separator : str
        Техническая строка для объединения и разделения текстов, по умолчанию '+++'
    train_dataset_path : str
        Путь в который будет сохранен датасет для разметки в Label Studio.

    Методы
    ------
    clean_messages(channel_url: str, df: pd.DataFrame, need_train_dataset: bool = False):
        Обрабатывает текстовые колонки в таблице, возвращает таблицу
    """

    def __init__(self, train_dataset_path: str) -> None:
        self.train_dataset_path = train_dataset_path
        self.df = pd.DataFrame()
        self.first_keys = {"id", "peer_id", "date", "message", "image_text"}

    def clean_messages(
        self, channel_url: str, df: pd.DataFrame, exist_rows: pd.Series, need_train_dataset: bool = False
    ) -> pd.DataFrame:
        """Обрабатывает текстовые колонки в таблице, возвращает отредактированную таблицу"""
        assert self.first_keys == set(df.columns), simlog.error(
            f"Can't create df, no parsed keys: {self.first_keys.difference(set(df.columns))}"
        )
        self.df = df
        self._add_key_id()
        self.df.reset_index(drop=True, inplace=True)
        self._drop_exist_rows(exist_rows)
        if self.df.empty:
            return self.df
        self.df.dropna(subset=["message"], inplace=True)
        self.df.fillna("", inplace=True)
        self._encode_text_cols("message")
        self._encode_text_cols("image_text")
        self._add_channel_name(channel_url)
        self._edit_full_text()
        self._rename_cols()
        self._convert_date()
        simlog.info(f"{self.df.columns}")
        self.df.drop_duplicates(inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        simlog.info("Full dataframe was created")

        if need_train_dataset:
            self._make_train_dataset(self.df)
        return self.df

    def _drop_exist_rows(self, exist_rows: pd.Series) -> None:
        simlog.info("_drop_exist_rows works ...")
        exist_rows.name = "exist_keys"
        self.df = self.df[
            self.df.merge(
                exist_rows, how="left", left_on="key_id", right_on="exist_keys", left_index=False, right_index=False
            )["exist_keys"].isna()
        ]

    def _add_key_id(self) -> None:
        simlog.info("_add_key_id works ...")
        self.df["key_id"] = self.df["peer_id"].astype(str) + "-" + self.df["id"].astype(str)

    def _convert_date(self) -> None:
        simlog.info("_convert_date works ...")
        self.df["message_date"] = self.df["message_date"].apply(lambda x: x.date())

    def _encode_text_cols(self, colanme: str) -> None:
        simlog.info("_encode_text_cols works ...")
        self.df[colanme] = self.df[colanme].apply(lambda x: self._encode_decode(x))

    def _edit_full_text(self) -> None:
        simlog.info("_edit_full_text works ...")
        self.df["full_text"] = (
            self.df["message"] + " " + self.df["image_text"] if not self.df["image_text"].empty else self.df["message"]
        )
        self.df["full_text"] = self.df["full_text"].apply(lambda x: self._remove_emoji(x))
        self.df["full_text"] = self.df["full_text"].apply(lambda x: self._replace_n(x))
        self.df["full_text"] = self.df["full_text"].apply(lambda x: self._encode_decode(x))
        self.df = self.df[self.df["full_text"] != " "]

    def _add_channel_name(self, channel_url: str) -> None:
        """Вырезает имя канала из url"""
        simlog.info("_add_channel_name works ...")
        assert channel_url, "Incorrect channel_url"
        channel_name = channel_url.split("/")[-1]
        self.df["channel_name"] = channel_name

    def _rename_cols(self) -> None:
        """Переименовывает колонки как в БД"""
        simlog.info("_rename_cols works ...")
        self.df = self.df.rename(columns={"id": "message_id", "peer_id": "channel_id", "date": "message_date"})
        self.df = self.df[
            ["channel_name", "channel_id", "message_id", "message_date", "message", "image_text", "full_text", "key_id"]
        ]

    def _make_train_dataset(self, df: pd.DataFrame) -> None:
        """Сохраняет json для разетки в Label Studio"""
        simlog.info("_make_train_dataset works ...")
        data = [{"text": text} for text in df["full_text"]]
        with open(self.train_dataset_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def _remove_emoji(self, text: str) -> str:
        """Удаляет emoji"""
        if not text:
            return text
        text = emoji.demojize(text)
        text = re.sub(r":\w+-*\w+:", " ", text)
        return text

    def _replace_n(self, text: str) -> str:
        """Удаляет переносы строк, ссылки и технические символы"""
        if not text:
            return text
        text = re.sub(r"\n", " ", text)
        text = re.sub("_x000C_", " ", text)
        text = re.sub(r"https:\/\/[^,\s]+,?", " ", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"■", " ", text)
        return text

    def _encode_decode(self, text: str) -> str:
        text = text.encode("utf-8", errors="ignore")
        text = text.decode("utf-8", errors="ignore")
        return text
