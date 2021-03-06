from .auger.auger_converter import converter
import simple_examples.funcs
from simple_examples.funcs import add
from simple_examples.funcs import fib
from simple_examples.funcs import update_dict
import unittest


class FuncsTest(unittest.TestCase):
    def test_add_2cdD(self):
        arg_a = 'hello'
        arg_b = 'world'
        actual_ret = simple_examples.funcs.add(a=arg_a,b=arg_b)

        # check return value
        self.assertEqual(
            'helloworld',
            actual_ret
        )
        # check parameter mutation
        expected_arg_a = 'hello'
        self.assertEqual(
            expected_arg_a,
            arg_a
        )
        expected_arg_b = 'world'
        self.assertEqual(
            expected_arg_b,
            arg_b
        )

    def test_fib_gADd(self):
        arg_n = 3
        actual_ret = simple_examples.funcs.fib(n=arg_n)

        # check return value
        self.assertEqual(
            3,
            actual_ret
        )
        # check parameter mutation
        expected_arg_n = 3
        self.assertEqual(
            expected_arg_n,
            arg_n
        )

    def test_fib_llPQ(self):
        arg_n = 1
        actual_ret = simple_examples.funcs.fib(n=arg_n)

        # check return value
        self.assertEqual(
            1,
            actual_ret
        )
        # check parameter mutation
        expected_arg_n = 1
        self.assertEqual(
            expected_arg_n,
            arg_n
        )

    def test_fib_wffY(self):
        arg_n = 2
        actual_ret = simple_examples.funcs.fib(n=arg_n)

        # check return value
        self.assertEqual(
            2,
            actual_ret
        )
        # check parameter mutation
        expected_arg_n = 2
        self.assertEqual(
            expected_arg_n,
            arg_n
        )

    def test_fib_y9XG(self):
        arg_n = 0
        actual_ret = simple_examples.funcs.fib(n=arg_n)

        # check return value
        self.assertEqual(
            1,
            actual_ret
        )
        # check parameter mutation
        expected_arg_n = 0
        self.assertEqual(
            expected_arg_n,
            arg_n
        )

    def test_fib_6Vcv(self):
        arg_n = 1
        actual_ret = simple_examples.funcs.fib(n=arg_n)

        # check return value
        self.assertEqual(
            1,
            actual_ret
        )
        # check parameter mutation
        expected_arg_n = 1
        self.assertEqual(
            expected_arg_n,
            arg_n
        )

    def test_update_dict_WwYZ(self):
        arg_origin = {'a': 'hello', 'b': 'world'}
        arg_to_update = {'a': 'Hallo', 'b': ' ', 'c': 'Welt'}
        actual_ret = simple_examples.funcs.update_dict(origin=arg_origin,to_update=arg_to_update)

        # check return value
        self.assertEqual(
            None,
            actual_ret
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
