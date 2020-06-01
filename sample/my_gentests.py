from auger.my_magic import Magic
from sample_code.simple import *


with Magic('sample_code', 'auger/object_converter.py'):
    add("hello", "world")
    origin = {'a': 'hello', 'b': 'world'}
    to_update = {'a': 'Hallo', 'b': ' ', 'c': 'Welt'}
    update_dict(origin, to_update)

    counter = Counter()
    counter.add()
    counter.add()
    counter.clear()
