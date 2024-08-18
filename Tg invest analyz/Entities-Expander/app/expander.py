import itertools

import config
import pandas as pd
from normalizer import Normalizer

normalizer = Normalizer()


class TableEditor:
    def get_expanded_df(self, df: pd.DataFrame):
        df = self.correct_data_type(df)
        entities_df = self.create_df_from_entities(df)
        expanded_data = self.expand_entities(entities_df)
        expanded_df = self.create_expanded_df(expanded_data, df)
        return expanded_df

    def correct_data_type(self, df: pd.DataFrame) -> pd.DataFrame:
        assert "entities" in df.columns
        df.dropna(subset=["entities"], inplace=True)
        df.reset_index(drop=True, inplace=True)
        df["entities"] = df["entities"].apply(lambda x: str(x))
        return df

    def create_df_from_entities(self, df):
        assert "entities" in df.columns
        normed_entities = df["entities"].apply(lambda x: normalizer.norm_entities(x))
        entities_df = pd.DataFrame(list(normed_entities))
        entities_df = entities_df[list(config.entities_naming.keys())]
        entities_df = entities_df.rename(config.entities_naming, axis=1)
        entities_df.fillna(value="", inplace=True)
        return entities_df

    def expand_entities(self, entities_df: pd.DataFrame) -> list:
        data = []
        for row, col in entities_df.iterrows():
            for z, x, c, v, b, n in list(itertools.zip_longest(col[0], col[1], col[2], col[3], col[4], col[5])):
                lst = [row, z, x, c, v, b, n]
                data.append(lst)
        return data

    def create_expanded_df(self, expanded_data: list, df: pd.DataFrame):
        df.reset_index(inplace=True)
        temp_df = pd.DataFrame(expanded_data, columns=["indx"] + list(config.entities_naming.values()))
        expanded_df = temp_df.merge(df, left_on="indx", right_on="index")
        return expanded_df
