from dotenv import dotenv_values

CONFIG = dotenv_values()

PARSER_URL = "http://....:9876/parse_channel"
EXPANDER_URL = "http://....:8599/expand_ideas"
MOEX_URL = "http://....:9877/add_moex_data"

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


FLASK_HOST = "0.0.0.0"
FLASK_PORT = "5000"
FLASK_DEBUG = False
