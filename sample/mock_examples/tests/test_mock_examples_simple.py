from .auger.auger_converter import converter
import mock_examples.simple
from mock_examples.simple import coin
from mock_examples.simple import dice
import unittest
from unittest.mock import patch


class SimpleTest(unittest.TestCase):
    @patch('mock_examples.simple.randint')
    def test_coin(self, mock_randint):
        mock_randint.return_value = 1
        arg_rand = mock_randint
        actual_ret = mock_examples.simple.coin(rand=arg_rand)

        # check return value
        self.assertEqual(
            2,
            actual_ret
        )
        # check parameter mutation

    @patch('mock_examples.simple.choice')
    @patch('mock_examples.simple.randint')
    def test_dice(self, mock_randint, mock_choice):
        mock_randint.return_value = 1
        mock_choice.return_value = 'super lucky'
        actual_ret = mock_examples.simple.dice()

        # check return value
        self.assertEqual(
            'Dice shows 1 and you are super lucky',
            actual_ret
        )


if __name__ == "__main__":
    unittest.main()
