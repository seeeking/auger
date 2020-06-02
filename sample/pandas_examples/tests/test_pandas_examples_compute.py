from .auger.auger_converter import converter
import pandas as pd
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal
import pandas_examples.compute
from pandas_examples.compute import fill_zero
from pandas_examples.compute import sum_df
import unittest


class ComputeTest(unittest.TestCase):
    def test_fill_zero_egmX(self):
        arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/APuhWh8RCiDzbYsH.pkl")
        actual_ret = pandas_examples.compute.fill_zero(df=arg_df)

        # check return value
        assert_frame_equal(
            actual_ret,
            converter.deserialize("pd.DataFrame", "tests/fixtures/c9bVrb7GlkbSY0Ls.pkl")
        )
        # check parameter mutation
        expected_arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/kItX0a6KyDXiGljX.pkl")
        assert_frame_equal(
            expected_arg_df,
            arg_df
        )

    def test_sum_df_PF33(self):
        arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/jJgtw9tr2eAv2pfA.pkl")
        actual_ret = pandas_examples.compute.sum_df(df=arg_df)

        # check return value
        assert_series_equal(
            actual_ret,
            converter.deserialize("pd.Series", "tests/fixtures/DxLbCvCF5q1Oi4Yh.pkl")
        )
        # check parameter mutation
        expected_arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/lmw3NWmgK29PDA36.pkl")
        assert_frame_equal(
            expected_arg_df,
            arg_df
        )


if __name__ == "__main__":
    unittest.main()
