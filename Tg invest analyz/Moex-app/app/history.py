from datetime import datetime, timedelta

import apimoex
import config
import pandas as pd
import requests


class History:
    """Класс, группирующий методы для выгрузки истории торгов по тикеру."""

    def _get_prices(self, ticker: str, start: str, stop: str) -> pd.DataFrame:
        """Обращается к MOEX и возвращает историю тикера от начальной
        до конечной даты.
        Выгружает максимум 100 значений, поэтому необходимо сформировать интервалы по 100 дней
        """
        request_url = config.MOEX_URL % ticker
        params = {"from": start, "till": stop}
        with requests.Session() as session:
            iss = apimoex.ISSClient(session, request_url, params)
            data = iss.get()
            if not data["history"]:
                return None
            dd = pd.DataFrame(data["history"])[["TRADEDATE", "LOW", "HIGH", "CLOSE"]]
            return dd

    def _make_100_intervals(self, start_obj: datetime.date, end_obj: datetime.date) -> list:
        """Создает набор интервалов по 100 дней и преобразует в строки
        Принимает дату начала и дату окончания
        """
        delt = timedelta(days=100)
        intervals = []
        while end_obj - start_obj > delt:
            intervals.append((end_obj - delt, end_obj))
            end_obj -= delt

        intervals.append((start_obj, end_obj))

        def func_to_list(lst):
            lst = tuple(map(str, lst))
            return lst

        intervals = list(map(func_to_list, intervals))
        return intervals[::-1]

    def get_ticker_full_history(self, ticker: str, start: datetime.date, stop: datetime.date) -> pd.DataFrame:
        """Принимает тикер, дату начала и окончания,
        создает интервалы по 100 дней,
        объединяет историю торгов,
        отдает датафрейм
        """
        intervals = self._make_100_intervals(start, stop)
        history = pd.DataFrame()
        for interval in intervals:
            history_part = self._get_prices(ticker, *interval)
            history = pd.concat([history, history_part])
        history.drop_duplicates(inplace=True)
        history.reset_index(drop=True, inplace=True)
        return history
