from .auger.auger_converter import converter
import simple_examples.clazz
from simple_examples.clazz import Counter
import unittest


class ClazzTest(unittest.TestCase):
    def test_add_X9Jd(self):
        arg_self = {'counter': 1}
        actual_ret = Counter.add(self=arg_self)

        # check return value
        self.assertEqual(
            actual_ret,
            None
        )
        # check parameter mutation
        expected_arg_self = {'counter': 2}
        self.assertEqual(
            expected_arg_self,
            arg_self
        )

    def test_clear_TcNn(self):
        arg_self = {'counter': 2}
        actual_ret = Counter.clear(self=arg_self)

        # check return value
        self.assertEqual(
            actual_ret,
            None
        )
        # check parameter mutation
        expected_arg_self = {'counter': 0}
        self.assertEqual(
            expected_arg_self,
            arg_self
        )


if __name__ == "__main__":
    unittest.main()
