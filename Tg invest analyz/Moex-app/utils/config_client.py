from dotenv import dotenv_values

CONFIG = dotenv_values()

SERVER_HOST = "...."
SERVER_PORT = "9877"

dbname = CONFIG["dbname"]
host = CONFIG["host"]
user = CONFIG["user"]
port = CONFIG["port"]

cols = ["key_id_ticker", "ticker", "message_date", "act", "percentage", "expectation_time"]

sql_query = f"""select {', '.join(cols)}
from prices p
where ticker is not null
and message_date is not null
and act is not null
and percentage is not null
and expectation_time is not null
and target_date isnull"""
