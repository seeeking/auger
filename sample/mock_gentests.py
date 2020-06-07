import random

from auger.my_magic import Magic
from mock_examples.simple import *
from mock_examples.web import *

with Magic('mock_examples', 'auger/object_converter.py', extra_files=[], mock_modules=[random, requests]):
    print(dice())
    print(coin(randint)) # TODO this shows the current relationship between functions is not correct, there's no direct hirachy, need to change
    # print(get('hello ')) # TODO this doesn't work, don't know why
