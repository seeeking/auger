import pandas as pd


def fill_zero(df: pd.DataFrame):
    return df.fillna(0)


def sum_df(df: pd.DataFrame):
    # can't re-assign
    # df = fill_zero(df)
    return fill_zero(df).sum()
