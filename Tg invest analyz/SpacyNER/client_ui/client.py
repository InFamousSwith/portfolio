import requests

URL = "http://....:8560/recognize"

resp = requests.post(
    URL,
    json={"text": "🛢 Роснефть: топ-выбор в нефтянке на 2023 Рекомендация — Покупать 🔹"},
)

resp_text = resp.text
print(resp_text)
