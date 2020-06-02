from .auger.auger_converter import converter
import simple_examples.simple
from simple_examples.simple import Counter
from simple_examples.simple import add
from simple_examples.simple import update_dict
import unittest


class SimpleTest(unittest.TestCase):
    def test_add_iEFz(self):
        arg_a = "hello"
        arg_b = "world"
        actual_ret = simple_examples.simple.add(a=arg_a,b=arg_b)

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

    def test_add_vkGn(self):
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

    def test_clear_a1b5(self):
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

    def test_update_dict_CaN5(self):
        arg_origin = {'a': 'hello', 'b': 'world'}
        arg_to_update = {'a': 'Hallo', 'b': ' ', 'c': 'Welt'}
        actual_ret = simple_examples.simple.update_dict(origin=arg_origin,to_update=arg_to_update)

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
