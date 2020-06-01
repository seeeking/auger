import json
from typing import Tuple


# csv.field_size_limit(sys.maxsize)


class FileNameGenerator:
    """
    Simple name generator to generate unique names
    """
    def __init__(self, prefix=''):
        self.start = 0
        self.prefix = prefix

    def _helper(self):
        self.start += 1
        while True:
            yield self.start

    def get_name(self) -> str:
        return f'{self.prefix}_{next(self._helper())}.csv'

    def get_entry(self):
        return f'{self}_entry.csv'

    def reset(self):
        self.start = 0


class Converter:
    def __init__(self):
        self.supported_types = {}

    def register_type(self, type_name, type_type: type, serializer, deserializer):
        """
        Add extra type support, or overwrite the default serializer/deserializer
        Args:
            type_name:
            type_type:
            serializer: a serializer that takes an object of certain type, and returns the type name and string representation of the object
            deserializer: deserializer takes a string and returns the object of specified type
        """
        self.supported_types[type_name] = (type_type, serializer, deserializer)

    def serialize(self, object_data) -> Tuple[type, str]:
        for type_name, funcs in self.supported_types.items():
            if isinstance(object_data, funcs[0]):
                return funcs[1](object_data)

        raise Exception(f'Unsupported data type {type(object_data)}')

    def deserialize(self, type_name, string_data: str):
        funcs = self.supported_types[type_name]
        return funcs[2](string_data)


converter = Converter()
converter.register_type('str', str, lambda a: ('str', a), lambda a: a)
converter.register_type('None', type(None), lambda a: ('None', ''), lambda s: None)
converter.register_type('dict', dict, lambda a: ('dict', json.dumps(a)), lambda a: json.loads(a))

