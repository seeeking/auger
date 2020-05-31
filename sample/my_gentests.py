from auger.my_magic import Magic
from sample_code import simple

with Magic('sample_code', 'auger/object_converter.py'):
    simple.add("hello", "world")
