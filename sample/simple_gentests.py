from auger.my_magic import Magic
from simple_examples.funcs import *
from simple_examples.clazz import *


with Magic('simple_examples', 'auger/object_converter.py'):
    add("hello", "world")
    origin = {'a': 'hello', 'b': 'world'}
    to_update = {'a': 'Hallo', 'b': ' ', 'c': 'Welt'}
    update_dict(origin, to_update)

    # update_dict_ref(to_update)

    counter = Counter()
    counter.add()
    counter.add()
    counter.clear()

    print(fib(3))
