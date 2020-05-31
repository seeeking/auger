from .auger.auger_converter import converter
import sample_code.simple
from sample_code.simple import add
import unittest


class SimpleTest(unittest.TestCase):
    def test_add(self):
        expected = sample_code.simple.add(a=converter.deserialize("str", "hello"),b=converter.deserialize("str", "world"))
        self.assertEqual(
            expected,
            converter.deserialize("str", "helloworld")
        )


if __name__ == "__main__":
    unittest.main()
