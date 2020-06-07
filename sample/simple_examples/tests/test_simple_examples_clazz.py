from .auger.auger_converter import converter
import simple_examples.clazz
from simple_examples.clazz import Counter
import unittest


class ClazzTest(unittest.TestCase):
    def test_add_NVET(self):
        arg_self = {}
        actual_ret = Counter.add(self=arg_self)

        # check return value
        self.assertEqual(
            None,
            actual_ret
        )
        # check parameter mutation
        expected_arg_self = {'counter': 1}
        self.assertEqual(
            expected_arg_self,
            arg_self
        )

    def test_add_KPEY(self):
        arg_self = {'counter': 1}
        actual_ret = Counter.add(self=arg_self)

        # check return value
        self.assertEqual(
            None,
            actual_ret
        )
        # check parameter mutation
        expected_arg_self = {'counter': 2}
        self.assertEqual(
            expected_arg_self,
            arg_self
        )

    def test_clear_Fh2K(self):
        arg_self = {'counter': 2}
        actual_ret = Counter.clear(self=arg_self)

        # check return value
        self.assertEqual(
            None,
            actual_ret
        )
        # check parameter mutation
        expected_arg_self = {'counter': 0}
        self.assertEqual(
            expected_arg_self,
            arg_self
        )


if __name__ == "__main__":
    unittest.main()
