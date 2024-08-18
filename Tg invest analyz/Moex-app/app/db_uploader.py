import config
import numpy as np
import psycopg2
from psycopg2.extensions import AsIs, register_adapter

register_adapter(np.int64, AsIs)


def update_db(dbname: str, host: str, user: str, port: str, full_json: dict) -> None:
    "Обновляет таблицу"
    with psycopg2.connect(dbname=dbname, host=host, user=user, port=port) as conn:
        cur = conn.cursor()
        cur.execute(
            config.SQL_UPDATE_QUERY,
            (
                full_json["target_date"],
                full_json["current_price"],
                full_json["target_price"],
                full_json["real_price"],
                full_json["real_date"],
                full_json["real_time"],
                full_json["low"],
                full_json["high"],
                full_json["if_good_idea"],
                full_json["real_sell_price"],
                full_json["real_profit"],
                full_json["real_percent_profit"],
                full_json["absolute_100_profit"],
                full_json["year_profit"],
                full_json["price_sim"],
                full_json["key_id_ticker"],
            ),
        )
        conn.commit()
    return None
