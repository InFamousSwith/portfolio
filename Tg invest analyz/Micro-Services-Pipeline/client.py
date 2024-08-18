import requests


TELEGRAM_CHANNEL ="https://t.me/bcsinvestidea"

json_for_parser = {
    "channel_url": TELEGRAM_CHANNEL, 
    "image_job": True, 
    "if_train_dataset": False
    }

json_for_expander = {"start_date": "", "end_date": ""}

request = requests.post(
    "http://127.0.0.1:5000/all_serv",
    json={"json_for_parser": json_for_parser, "json_for_expander": json_for_expander},
)

print(request.text)
