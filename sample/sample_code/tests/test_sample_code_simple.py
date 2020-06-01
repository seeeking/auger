from .auger.auger_converter import converter
from builtins import tuple
import sample_code.simple
from sample_code.simple import Counter
from sample_code.simple import add
from sample_code.simple import update_dict
import unittest


class SimpleTest(unittest.TestCase):
    def test_add(self):
        arg_a = converter.deserialize("str", "hello")
        arg_b = converter.deserialize("str", "world")
        actual_ret = sample_code.simple.add(a=arg_a,b=arg_b)

        # check return value
        self.assertEquals(
            actual_ret,
            converter.deserialize("str", "helloworld")
        )

        # check parameter mutation
        expected_arg_a = converter.deserialize("str", "hello")
        self.assertEquals(
            expected_arg_a,
            arg_a
        )

        expected_arg_b = converter.deserialize("str", "world")
        self.assertEquals(
            expected_arg_b,
            arg_b
        )


    def test_add(self):
        arg_self = converter.deserialize("dict", "{}")
        actual_ret = Counter.add(self=arg_self)

        # check return value
        self.assertEquals(
            actual_ret,
            converter.deserialize("None", "")
        )

        # check parameter mutation
        expected_arg_self = converter.deserialize("dict", "{\"counter\": 1}")
        self.assertEquals(
            expected_arg_self,
            arg_self
        )


    def test_clear(self):
        arg_self = converter.deserialize("dict", "{\"counter\": 2}")
        actual_ret = Counter.clear(self=arg_self)

        # check return value
        self.assertEquals(
            actual_ret,
            converter.deserialize("None", "")
        )

        # check parameter mutation
        expected_arg_self = converter.deserialize("dict", "{\"counter\": 0}")
        self.assertEquals(
            expected_arg_self,
            arg_self
        )


    def test_update_dict(self):
        arg_origin = converter.deserialize("dict", "{\"a\": \"hello\", \"b\": \"world\"}")
        arg_to_update = converter.deserialize("dict", "{\"a\": \"Hallo\", \"b\": \" \", \"c\": \"Welt\"}")
        actual_ret = sample_code.simple.update_dict(origin=arg_origin,to_update=arg_to_update)

        # check return value
        self.assertEquals(
            actual_ret,
            converter.deserialize("None", "")
        )

        # check parameter mutation
        expected_arg_origin = converter.deserialize("dict", "{\"a\": \"Hallo\", \"b\": \" \", \"c\": \"Welt\"}")
        self.assertEquals(
            expected_arg_origin,
            arg_origin
        )

        expected_arg_to_update = converter.deserialize("dict", "{\"a\": \"Hallo\", \"b\": \" \", \"c\": \"Welt\"}")
        self.assertEquals(
            expected_arg_to_update,
            arg_to_update
        )


if __name__ == "__main__":
    unittest.main()
