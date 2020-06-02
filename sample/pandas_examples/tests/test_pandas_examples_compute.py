from .auger.auger_converter import converter
import pandas as pd
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal
import pandas_examples.compute
from pandas_examples.compute import fill_zero
from pandas_examples.compute import sum_df
import unittest


class ComputeTest(unittest.TestCase):
    def test_fill_zero_hgoF(self):
        arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/Yh0KKozaoZKY6Iyx.pkl")
        actual_ret = pandas_examples.compute.fill_zero(df=arg_df)

        # check return value
        assert_frame_equal(
            actual_ret,
            converter.deserialize("pd.DataFrame", "tests/fixtures/0csVGRhXILoY7xKb.pkl")
        )
        # check parameter mutation
        expected_arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/p6BnryNUrQ8o8OWQ.pkl")
        assert_frame_equal(
            expected_arg_df,
            arg_df
        )

    def test_sum_df_egMc(self):
        arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/e38Ke5Zm2qdNOPK8.pkl")
        actual_ret = pandas_examples.compute.sum_df(df=arg_df)

        # check return value
        assert_series_equal(
            actual_ret,
            converter.deserialize("pd.Series", "tests/fixtures/BNzWbGa4e7YYSrQw.pkl")
        )
        # check parameter mutation
        expected_arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/t5pl9LcxcfWY1a6P.pkl")
        assert_frame_equal(
            expected_arg_df,
            arg_df
        )

if __name__ == "__main__":
    unittest.main()
