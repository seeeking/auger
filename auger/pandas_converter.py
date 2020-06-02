import random
import string
from typing import Union

import pandas as pd

import object_converter


def _write_pickle(df: Union[pd.DataFrame, pd.Series]):
    file = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + '.pkl'
    df.to_pickle(file)
    return file


def _read_pickle(f):
    df = pd.read_pickle(f)
    print(df.head())
    return df


# I'm not very comfortable with this, but it seems okay, importing actually imports the value instead of the reference
converter = object_converter.converter
converter.register_type('pd.DataFrame',
                        pd.DataFrame,
                        lambda df: object_converter.SerializeResult(
                            'pd.DataFrame',
                            _write_pickle(df),
                            False),
                        lambda f: _read_pickle(f))

converter.register_type('pd.Series',
                        pd.Series,
                        lambda df: object_converter.SerializeResult(
                            'pd.Series',
                            _write_pickle(df),
                            False),
                        lambda f: _read_pickle(f))
