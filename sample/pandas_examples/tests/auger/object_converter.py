import json
from collections import namedtuple

# csv.field_size_limit(sys.maxsize)


# direct means you have a representation that can appear directly in code
SerializeResult = namedtuple('SerializeResult', ['type_name', 'value', 'direct', 'comparator'])


def _quote(a):
    return '"' + a.replace('"', '\\"') + '"'

class Converter:
    def __init__(self):
        self.supported_types = {}

    def register_type(self, type_name, type_type: type, serializer, deserializer):
        """
        Add extra type support, or overwrite the default serializer/deserializer
        We register a certain type name to avoid possible trouble from serializing & deserializing a type object
        Args:
            type_name:
            type_type:
            serializer: a serializer that takes an object of certain type, and returns the type name and string representation of the object
            deserializer: deserializer takes a string and returns the object of specified type
        """
        self.supported_types[type_name] = (type_type, serializer, deserializer)

    def serialize(self, object_data) -> SerializeResult:
        for type_name, funcs in self.supported_types.items():
            if isinstance(object_data, funcs[0]):
                return funcs[1](object_data)

        print(object_data)
        raise Exception(f'Unsupported data type {type(object_data)}, {object_data}')

    def deserialize(self, type_name, value):
        funcs = self.supported_types[type_name]
        return funcs[2](value)


converter = Converter()
converter.register_type('str', str, lambda a: SerializeResult('str', a, True, None), lambda a: _quote(a))
converter.register_type('None', type(None), lambda a: SerializeResult('None', '', True, None), lambda s: None)
converter.register_type('dict', dict, lambda a: SerializeResult('dict', json.dumps(a), True, None), lambda a: json.loads(a))

