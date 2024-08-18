import json
import re

import config


class Normalizer:
    def __init__(self) -> None:
        self.COMPANY_TAGS = ("companyName", "ORG")
        self.NUMBER_TAGS = ("targetPrice", "PRICE")
        self.SIGN_TAGS = ("sign",)
        self.PERCENT_TAGS = ("targetPercent", "PERCENT")
        self.DATE_TAGS = ("targetTime", "TIME")
        self.TICKER_TAGS = ("ticker", "TICKER")
        self.ACTION_TAGS = "ACT"
        self.tag2normalizer = {
            self.COMPANY_TAGS: self.normalize_company,
            self.PERCENT_TAGS: self.normalize_percent,
            self.DATE_TAGS: self.normalize_target_date,
            self.NUMBER_TAGS: self.normalize_number,
            self.TICKER_TAGS: self.normalize_ticker,
            self.ACTION_TAGS: self.normalize_action,
        }

    def norm_entities(self, entities: str) -> dict:
        if not entities:
            return {key: [] for key in config.entities_naming.keys()}
        dict_data = json.loads(entities)
        norm_dict = {}
        for element in dict_data:
            for k, v in element.items():
                if k not in norm_dict.keys():
                    norm_dict[k] = [self.normalize_all(k, v, self.tag2normalizer)]
                else:
                    norm_dict[k].append(self.normalize_all(k, v, self.tag2normalizer))
        norm_dict = self.normalize_dict(norm_dict)
        return norm_dict

    @staticmethod
    def join_list(lst: list) -> str:
        return ", ".join(map(str, lst))

    @staticmethod
    def try_parse_number(raw_value: str):
        try:
            return float(raw_value)
        except ValueError:
            return None

    @staticmethod
    def normalize_company(company: str):
        company = re.sub(r"[«»]|\n+", "", company)
        company = company.strip().upper()
        return company

    def normalize_percent(self, raw_value: str):
        if not raw_value:
            return None
        raw_value = re.sub(",", ".", raw_value)
        m = re.search(r"\d+\.?\d*", raw_value)
        if m:
            return self.try_parse_number(m.group(0))

    @staticmethod
    def normalize_target_date(row_date: str):
        row_date = row_date.lower()
        re_days = re.compile(r"(дн|ден).*")
        re_weeks = re.compile(r"(недел).*")
        re_months = re.compile(r"(mec|мес).*")
        re_years = re.compile(r"(год|лет).*")
        # re_digits = re.compile(r"\d+")

        re_compiles = [re_days, re_weeks, re_months, re_years]
        coefficients = [1, 7, 30, 365]

        if re.findall(r"\d+", row_date):
            num_list = re.findall(r"\d+", row_date)
            d = max([int(num) for num in num_list])
        else:
            return None

        for regex, coef in zip(re_compiles, coefficients):
            if regex.search(row_date):
                return int(d) * coef
        return None

    def normalize_number(self, raw_value: str):
        raw_value = raw_value.lower().strip()
        raw_value = raw_value.replace(",", ".").lower()
        raw_value = re.sub(r"\s", "", raw_value)
        return self.try_parse_number(raw_value)

    @staticmethod
    def normalize_ticker(raw_value: str):
        try:
            ticker = re.search(r"\w+", raw_value).group().upper()
            return ticker
        except Exception:
            return None

    @staticmethod
    def normalize_action(raw_value: str):
        value = raw_value.lower()
        if re.search(r"покуп|buy|long|доход", value):
            return "BUY"
        elif re.search(r"прод|sel|short|убыт", value):
            return "SELL"
        return None

    @staticmethod
    def normalize_other(raw_value: str) -> str:
        return raw_value.strip()

    def normalize_dict(self, norm_dict: dict):
        for col in list(config.entities_naming.keys()):
            if col not in norm_dict.keys():
                norm_dict[col] = [None]
        return norm_dict

    def normalize_all(self, tag: str, raw_value: str, tag2normalizer: dict):
        for tags_group, func in tag2normalizer.items():
            if tag in tags_group:
                return func(raw_value)
        return self.normalize_other(raw_value)
