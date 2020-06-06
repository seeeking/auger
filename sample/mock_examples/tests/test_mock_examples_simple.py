from .auger.auger_converter import converter
import mock_examples.simple
from mock_examples.simple import dice
import unittest
from unittest.mock import patch


class SimpleTest(unittest.TestCase):
    @patch('mock_examples.simple.choice')
    @patch('mock_examples.simple.randint')
    def test_dice(self, mock_randint, mock_choice):
        mock_randint.return_value = 4
        mock_choice.return_value = 'lucky'
        actual_ret = mock_examples.simple.dice()

        # check return value
        self.assertEqual(
            'Dice shows 4 and you are lucky',
            actual_ret
        )


if __name__ == "__main__":
    unittest.main()
