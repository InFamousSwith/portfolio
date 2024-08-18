from dotenv import dotenv_values

CONFIG = dotenv_values()

MOEX_URL = "https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/%s.json"

FLASK_DEBUG = False
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

dbname = CONFIG["dbname"]
host = CONFIG["host"]
user = CONFIG["user"]
port = CONFIG["port"]


SQL_UPDATE_QUERY = """UPDATE prices
            SET
            target_date = %s,
            current_price = %s,
            target_price = %s,
            real_price = %s,
            real_date = %s,
            real_time = %s,
            low = %s,
            high = %s,
            if_good_idea = %s,
            real_sell_price = %s,
            real_profit = %s,
            real_percent_profit = %s,
            absolute_100_profit = %s,
            year_profit = %s,
            price_sim = %s
            WHERE key_id_ticker = %s"""
