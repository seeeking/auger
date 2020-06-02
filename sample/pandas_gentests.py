from auger.my_magic import Magic
from pandas_examples.compute import *
import pandas as pd

with Magic('pandas_examples', 'auger/pandas_converter.py', extra_files=['auger/object_converter.py']):
    df = pd.DataFrame.from_dict({'A': [1, None, 2, None], 'B': [3, None, None, 4]})
    sum_df(df)


