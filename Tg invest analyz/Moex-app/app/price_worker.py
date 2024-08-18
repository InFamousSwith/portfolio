import datetime

import pandas as pd


class Prices:
    """Класс группирует методы для получения различных разрезов цен"""

    def get_current_price(self, history: pd.DataFrame) -> float:
        """Находит цену на дату сообщения"""
        return history.loc[0, "CLOSE"]

    def get_real_end_price(self, history: pd.DataFrame) -> float:
        """Находит цену на дату закрытия идеи"""
        return history.loc[len(history) - 1, "CLOSE"]

    def get_target_price(self, current_price: float, percentage: float, act: str) -> float:
        """Вычисляет предсказанную цену"""
        price_moving = current_price * percentage / 100
        act_mapping = {"BUY": current_price + price_moving, "SELL": current_price - price_moving}
        return act_mapping[act]

    def get_low(self, history: pd.DataFrame) -> float:
        """Находит самую низкую цену за период идеи"""
        return history["LOW"].min()

    def get_high(self, history: pd.DataFrame) -> float:
        """Находит самую высокую цену за период идеи"""
        return history["HIGH"].max()

    def get_if_good_idea(self, real_date: datetime.date) -> bool:
        """возвращает bool сбылась ли идея (достигнута ли предсказанная цена)"""
        if real_date:
            return True
        return False

    def get_real_sell_price(self, history: pd.DataFrame, target_price: float, real_date: datetime.date) -> float:
        """Возвращаяет цену закрытия сделки
        либо таргет, если достигнута,
        либо цена закрытия в последний день идеи"""
        if real_date:
            return target_price
        break_price = history["CLOSE"][len(history["CLOSE"]) - 1]
        early_stop_day = history["TRADEDATE"][len(history["TRADEDATE"]) - 1]
        early_stop_day = datetime.datetime.strptime(early_stop_day, "%Y-%m-%d").date()
        return break_price

    def get_price_sim(self, if_good_idea: bool, act: str, target_price: float, high: float, low: float) -> float:
        """Вычисляет процент, на который цена НЕ достигла таргета
        Если достигла, возвращается 0
        """
        if if_good_idea:
            return 0
        act_mapping = {
            "BUY": high - target_price,
            "SELL": target_price - low,
        }
        return act_mapping[act] / target_price * 100

    def get_absolute_profit(self, current_price: float, real_price: float, act: str) -> float:
        """Вычисляет абсолютный доход/убыток в рублях от идеи"""
        act_mapping = {"BUY": real_price - current_price, "SELL": current_price - real_price}
        return act_mapping[act]

    def get_real_percent_profit(self, absolute_profit: float, current_price: float) -> float:
        """Вычисляет доход/убыток идеи в процентах от первоначальной цены"""
        return absolute_profit / current_price * 100

    def get_year_profit(self, real_percent_profit: float, real_time: int) -> float:
        """Вычисляет доход/убыток от идеи в годовом выражении"""
        return real_percent_profit / real_time * 365

    def get_absolute_100_profit(self, real_percent_profit: float) -> float:
        """Вычисляет остаток в рублях, если в идею вложено 100 рублей
        Индикатор нужен для того, чтобы можно было посчитать доход без
        учета цены бумаги
        """
        return 100 + real_percent_profit

    # stop loss
    # def get_real_percent_profit(self, current_price, real_price, act):
    #     if act == 'BUY':
    #         absolute_profit = real_price - current_price
    #         real_percent_profit = absolute_profit / current_price * 100
    #         absolute_100_profit = 100 + real_percent_profit
    #     else:
    #         absolute_profit = current_price - real_price
    #         real_percent_profit = absolute_profit / current_price * 100
    #         absolute_100_profit = 100 + real_percent_profit
    #     return absolute_profit, real_percent_profit, absolute_100_profit

    # def get_year_profit(self, real_percent_profit, real_time):
    #     return real_percent_profit / real_time * 365

    # def _stop_loss_work(self, history, current_price, target_price, act, treshhold):
    #     price_moving = current_price * treshhold / 100
    #     act_mapping = {
    #         'BUY': {
    #             'stop_loss_price': current_price - price_moving,
    #             'break_price_func': self._find_buy_break
    #         },
    #         'SELL': {
    #             'stop_loss_price': current_price + price_moving,
    #             'break_price_func': self._find_sell_break
    #         },
    #     }
    #     stop_loss_price = act_mapping[act]['stop_loss_price']
    #     break_price, early_stop_day = act_mapping[act]['break_price_func'](history, target_price, stop_loss_price)
    #     return break_price, early_stop_day

    # def _find_buy_break(self, history, target_price, stop_loss_price):
    #     for v, x in enumerate(history['LOW']):
    #         if x <= stop_loss_price:
    #             break_price = x
    #             early_stop_day = history['TRADEDATE'][v]
    #             early_stop_day = datetime.strptime(early_stop_day, '%Y-%m-%d').date()
    #             return break_price, early_stop_day
    #     return None, None

    # def _find_sell_break(self, history, target_price, stop_loss_price):
    #     for v, x in enumerate(history['HIGH']):
    #         if x >= stop_loss_price:
    #             break_price = x
    #             early_stop_day = history['TRADEDATE'][v]
    #             early_stop_day = datetime.strptime(early_stop_day, '%Y-%m-%d').date()
    #             return break_price, early_stop_day
    #     return None, None
