from .auger.auger_converter import converter
import pandas as pd
from pandas.util.testing import assert_frame_equal
import pandas_examples.impute
from pandas_examples.impute import fill_zero
import unittest


class ImputeTest(unittest.TestCase):
    def test_fill_zero_TbdB(self):
        arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/9v5ip5vlbwsO8RM3.pkl")
        actual_ret = pandas_examples.impute.fill_zero(df=arg_df)

        # check return value
        assert_frame_equal(
            actual_ret,
            converter.deserialize("pd.DataFrame", "tests/fixtures/3zw7Xy7meDZdggHE.pkl")
        )
        # check parameter mutation
        expected_arg_df = converter.deserialize("pd.DataFrame", "tests/fixtures/MYY8umK11jqFmiSt.pkl")
        assert_frame_equal(
            expected_arg_df,
            arg_df
        )

if __name__ == "__main__":
    unittest.main()
