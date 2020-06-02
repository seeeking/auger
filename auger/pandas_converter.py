import random
import string
import pandas as pd

import object_converter
from pandas.util.testing import assert_frame_equal


def _write_pickle(df):
    file = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + '.pkl'
    df.to_pickle(file)
    return file


def _read_pickle(f):
    df = pd.read_pickle(f)
    df.head()
    return df


# I'm not very comfortable with this, but it seems okay, importing actually imports the value instead of the reference
converter = object_converter.converter
converter.register_type('pd.DataFrame',
                        pd.DataFrame,
                        lambda df: object_converter.SerializeResult(
                            'pd.DataFrame',
                            _write_pickle(df),
                            False,
                            assert_frame_equal),
                        lambda f: _read_pickle(f))