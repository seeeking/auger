import random

from auger.my_magic import Magic
from mock_examples.simple import *

with Magic('mock_examples', 'auger/object_converter.py', extra_files=[], mock_modules=[random]):
    print(dice())
    # print(coin(randint))
