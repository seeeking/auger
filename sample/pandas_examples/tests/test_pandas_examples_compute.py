from .auger.auger_converter import converter
import pandas as pd
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal
import pandas_examples.compute
from pandas_examples.compute import fill_zero
from pandas_examples.compute import sum_df
import unittest


class ComputeTest(unittest.TestCase):
    def test_fill_zero_JacU(self):
        arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/9HiGZ2Yf9J4i4jCY.pkl")
        actual_ret = pandas_examples.compute.fill_zero(df=arg_df)

        # check return value
        assert_frame_equal(
            actual_ret,
            converter.deserialize("pd.DataFrame", "tests/fixtures/AFVDID49GmJfHd97.pkl")
        )
        # check parameter mutation
        expected_arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/UnrS01Cq8vOmon2W.pkl")
        assert_frame_equal(
            expected_arg_df,
            arg_df
        )

    def test_sum_df_EZ3Y(self):
        arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/GnlJyHkJ6CzsUbJz.pkl")
        actual_ret = pandas_examples.compute.sum_df(df=arg_df)

        # check return value
        assert_series_equal(
            actual_ret,
            converter.deserialize("pd.Series", "tests/fixtures/mlukK1muG8Ztw4Ko.pkl")
        )
        # check parameter mutation
        expected_arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/kF9TGTaTnr8hCSUb.pkl")
        assert_frame_equal(
            expected_arg_df,
            arg_df
        )


if __name__ == "__main__":
    unittest.main()
