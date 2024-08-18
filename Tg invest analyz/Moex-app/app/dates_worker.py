import datetime
from datetime import timedelta

import pandas as pd


class Dates:
    def make_date_from_ts(self, ts_date: pd.Timestamp) -> datetime.date:
        """Преобразует формат даты из pd.Timestamp в datetime.date"""
        return ts_date.date()

    def make_timedelta(self, num_days: int) -> timedelta:
        """Преобразует срок в днях (int) в timedelta"""
        return timedelta(days=num_days)

    def get_target_day(self, message_date: datetime.date, expectation_time: int) -> datetime.date:
        """Вычисляет дату окончания идеи"""
        return message_date + self.make_timedelta(expectation_time)

    def get_real_date(self, history, target_price, act) -> datetime.date:
        """Находит дату досрочного закрытия идеи
        если цена пробила предсказанную цену"""
        price_mapping = {
            "BUY": history[history["HIGH"] >= target_price],
            "SELL": history[history["LOW"] <= target_price],
        }
        if len(price_mapping[act]):
            return datetime.datetime.strptime(price_mapping[act].iloc[0, 0], "%Y-%m-%d").date()
        return None

    def get_real_time(self, real_date: datetime.date, message_date: datetime.date, expectation_time: int) -> int:
        """Вычисляет количество дней, затраченное на идею
        Если идея успешная, то от даты начала до пробития цены
        Если идея не успешная, то весь срок идеи"""
        if not real_date:
            return expectation_time
        else:
            return (real_date - message_date).days + 1
