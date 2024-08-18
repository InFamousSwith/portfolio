import requests

r = requests.post(
    "http://....:9876/parse_channel",
    json={"channel_url": "https://t.me/bcsinvestidea", "image_job": True, "if_train_dataset": False},
)

print(r.text)
