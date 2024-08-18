import json

import pandas as pd


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as file:
        obj = json.load(file)
    return obj


obj = load_json("metrics.json")
df = pd.DataFrame(obj[1], index=obj[0]["index"])
print(df)
