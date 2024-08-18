import datetime
import json

import config
import db_uploader as db
from dates_worker import Dates
from flask import Flask, request
from history import History
from price_worker import Prices

app = Flask("Moexer")


dates_adder = Dates()
prices_adder = Prices()
history_loader = History()


class Row_from_db:
    def __init__(self, input_json) -> None:
        self.key_id_ticker = input_json["key_id_ticker"]
        self.ticker = input_json["ticker"]
        self.message_date = datetime.datetime.strptime(input_json["message_date"], "%Y-%m-%d").date()
        self.act = input_json["act"]
        self.percentage = input_json["percentage"]
        self.expectation_time = input_json["expectation_time"]
        self.target_date = dates_adder.get_target_day(self.message_date, self.expectation_time)

    def run(self) -> tuple:
        if self.target_date > datetime.datetime.today().date():
            key_id_ticker = self.key_id_ticker
            target_date = self.target_date
            self.__dict__ = {}
            return self.__dict__, f"Дата окончания идеи {key_id_ticker} {target_date} не наступила"

        self.history_df = history_loader.get_ticker_full_history(self.ticker, self.message_date, self.target_date)
        if self.history_df.empty:
            ticker = self.ticker
            self.__dict__ = {}
            return self.__dict__, f"Тикер {ticker} не найден"

        self.current_price = prices_adder.get_current_price(self.history_df)
        self.target_price = prices_adder.get_target_price(self.current_price, self.percentage, self.act)
        self.real_price = prices_adder.get_real_end_price(self.history_df)
        self.real_date = dates_adder.get_real_date(self.history_df, self.target_price, self.act)
        self.low = prices_adder.get_low(self.history_df)
        self.high = prices_adder.get_high(self.history_df)
        self.if_good_idea = prices_adder.get_if_good_idea(self.real_date)
        self.real_sell_price = prices_adder.get_real_sell_price(self.history_df, self.target_price, self.real_date)
        self.real_time = dates_adder.get_real_time(self.real_date, self.message_date, self.expectation_time)
        self.real_profit = prices_adder.get_absolute_profit(self.current_price, self.real_sell_price, self.act)
        self.real_percent_profit = prices_adder.get_real_percent_profit(self.real_profit, self.current_price)
        self.absolute_100_profit = prices_adder.get_absolute_100_profit(self.real_percent_profit)
        self.year_profit = prices_adder.get_year_profit(self.real_percent_profit, self.real_time)
        self.price_sim = prices_adder.get_price_sim(self.if_good_idea, self.act, self.target_price, self.high, self.low)
        self.__dict__.pop("history_df")
        return self.__dict__, "Успешно"


@app.route("/add_moex_data", methods=["POST"])
def add_moex_data():
    """Принимает одну инвестидею с ключами
        'key_id_ticker': '123-12-NVTK',
        'ticker': 'NVTK',
        'message_date': date(2023, 3, 27),
        'act': 'BUY',
        'percentage': 93.0,
        'expectation_time': 90.0,
    Обновляет БД.
    Отдает сообщение об успешном или неуспешном обновлении базы."""
    content = request.get_json()
    content = json.loads(content)
    row_from_db = Row_from_db(content)
    full_json, message = row_from_db.run()
    if not full_json:
        return f"Database is NOT updated: {message}"
    try:
        db.update_db(config.dbname, config.host, config.user, config.port, full_json)
        key = full_json["key_id_ticker"]
        return json.dumps(full_json, indent=4, sort_keys=True, default=str)
        # return f"Database is updated with the key {key}"
    except Exception as ex:
        key = full_json["key_id_ticker"]
        return f"Database is NOT updated with the key {key}. Exception {ex}"


if __name__ == "__main__":
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.FLASK_DEBUG, threaded=False)
