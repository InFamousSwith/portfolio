import difflib

import config
import pandas as pd
from nltk.stem.snowball import SnowballStemmer


class FuzziSearcher:
    def __init__(self, ticker_data: pd.DataFrame, treshhold: float = config.fuzzy_treshhold) -> None:
        self.stemmer = SnowballStemmer("russian")
        self.treshhold = treshhold
        self.ticker_data = ticker_data
        self.ticker_data["stemmed"] = self.ticker_data["name"].apply(lambda x: self._preproc_some_word(x))

    def _preproc_some_word(self, word):
        word = str(word)
        word = word.lower()
        tokens = [self.stemmer.stem(tok) for tok in word.split()]
        word = " ".join(tokens)
        return word

    def _calc_sim(self, string1, string2):
        temp = difflib.SequenceMatcher(None, string1, string2)
        return temp.ratio()

    def _get_stemmed_name(self, name) -> str:
        res = {norm: self._calc_sim(name, norm) for norm in self.ticker_data["stemmed"] if self._calc_sim(name, norm) > self.treshhold}
        if not res:
            return None
        stemmed_name = sorted(res.items(), key=lambda x: x[1], reverse=True)[0][0]
        return stemmed_name

    def get_one_ticker(self, name):
        name = self._preproc_some_word(name)
        stemmed_name = self._get_stemmed_name(name)
        if not stemmed_name:
            return None
        ticker = self.ticker_data[self.ticker_data["stemmed"] == stemmed_name]["ticker"].iloc[0]
        return ticker
