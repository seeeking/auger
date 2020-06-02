import pandas as pd


def fill_zero(df: pd.DataFrame):
    return df.fillna(0)
