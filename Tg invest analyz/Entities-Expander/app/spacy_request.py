import config
import pandas as pd
import requests


class DataRecognizer:
    def __init__(self) -> None:
        self.url = config.spacy_url

    def get_one_service_response(self, one_new: str) -> dict:
        try:
            response = requests.post(self.url, json={"text": one_new})
            return response.text
        except Exception:
            print(f"no responce {one_new}")
            return ""

    def add_str_entities(self, df: pd.DataFrame) -> pd.DataFrame:
        print("add_str_entities works ...")
        df["entities"] = df["full_text"].apply(lambda x: self.get_one_service_response(x))
        return df
