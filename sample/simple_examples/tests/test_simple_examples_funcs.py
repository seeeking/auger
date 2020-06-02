from .auger.auger_converter import converter
import simple_examples.funcs
from simple_examples.funcs import add
from simple_examples.funcs import update_dict
import unittest


class FuncsTest(unittest.TestCase):
    def test_add_l55m(self):
        arg_a = "hello"
        arg_b = "world"
        actual_ret = simple_examples.funcs.add(a=arg_a,b=arg_b)

        # check return value
        self.assertEqual(
            actual_ret,
            "helloworld"
        )
        # check parameter mutation
        expected_arg_a = "hello"
        self.assertEqual(
            expected_arg_a,
            arg_a
        )
        expected_arg_b = "world"
        self.assertEqual(
            expected_arg_b,
            arg_b
        )

    def test_update_dict_BKHD(self):
        arg_origin = {'a': 'hello', 'b': 'world'}
        arg_to_update = {'a': 'Hallo', 'b': ' ', 'c': 'Welt'}
        actual_ret = simple_examples.funcs.update_dict(origin=arg_origin,to_update=arg_to_update)

        # check return value
        self.assertEqual(
            actual_ret,
            None
        )
        # check parameter mutation
        expected_arg_origin = {'a': 'Hallo', 'b': ' ', 'c': 'Welt'}
        self.assertEqual(
            expected_arg_origin,
            arg_origin
        )
        expected_arg_to_update = {'a': 'Hallo', 'b': ' ', 'c': 'Welt'}
        self.assertEqual(
            expected_arg_to_update,
            arg_to_update
        )

if __name__ == "__main__":
    unittest.main()
