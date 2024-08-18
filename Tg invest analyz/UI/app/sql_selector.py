from typing import List, Text, Tuple

import pandas as pd
import psycopg2


class BaseSelector:
    "Выполняет sql запрос, метод simple_select"

    def __init__(self, dbname: Text, host: Text, user: Text, port: Text) -> None:
        self.dbname = dbname
        self.host = host
        self.user = user
        self.port = port

    def simple_select(self, sql_query: Text) -> List[Tuple]:
        "Возвращает лист тюплов без названия колонок"
        with psycopg2.connect(dbname=self.dbname, host=self.host, user=self.user, port=self.port) as conn:
            cur = conn.cursor()
            cur.execute(sql_query)
            results = cur.fetchall()
        return results


class SelectorDF(BaseSelector):
    "Класс для выполнения запроса, в который переданы параметры пользователем"

    def __init__(self, dbname: Text, host: Text, user: Text, port: Text) -> None:
        super().__init__(dbname, host, user, port)

    def _select_cols(self, sql_columns) -> List[Text]:
        "Находит список названий колонок в БД"
        columns = self.simple_select(sql_query=sql_columns)
        assert columns
        columns = [col[0] for col in columns]
        return columns

    def _cols_to_query(self, columns: List) -> Text:
        "Преобразовывает названия так, чтобы работал запрос"
        p_cols = ["p." + col for col in columns] + ["t.branch"] + ["i.channel_name"]
        return ", ".join(p_cols)

    def _channels_to_query(self, channel_names: List[Text]) -> Tuple[Text]:
        "Преобразовывает названия каналов в синтакис SQL"
        if len(channel_names) == 1:
            return f"('{channel_names[0]}')"
        return tuple(channel_names)

    def _build_query(self, sql_columns: Text, sql_data: Text, channel_names: List[Text]):
        "Создает запрос с выбранными колонками и каналами"
        columns = self._select_cols(sql_columns)
        cols_str = self._cols_to_query(columns)
        channels_tuple = self._channels_to_query(channel_names)
        query_df = sql_data % (cols_str, channels_tuple)
        return query_df

    def build_df(self, sql_columns: Text, sql_data: Text, channel_names: List[Text]):
        "Создает датафрейм по заданным каналам"
        query_df = self._build_query(sql_columns, sql_data, channel_names)
        columns = self._select_cols(sql_columns) + ["branch"] + ["channel_name"]
        df = pd.DataFrame(data=self.simple_select(query_df), columns=columns)
        df["branch"].fillna(df=df[~df['branch'].isna()], inplace=True)
        return df
