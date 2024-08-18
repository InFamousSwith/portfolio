import requests

URL = "http://....:8599/expand_ideas"

test = {"start_date": "", "end_date": ""}

resp = requests.post(URL, json=test)
print(resp.text)
