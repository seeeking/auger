import csv
import json
import os
import pathlib
import sys
from typing import Tuple

import numpy as np
import pandas as pd

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
            if type(object_data) is funcs[0]:
                return funcs[1](object_data)

        raise Exception(f'Unsupported data type {type(object_data)}')

    def deserialize(self, type_name, string_data: str):
        funcs = self.supported_types[type_name]
        return funcs[2](string_data)


converter = Converter()
converter.register_type('str', str, lambda a: ('str', a), lambda a: a)
converter.register_type('dict', dict, lambda a: ('dict', json.dumps(a)), lambda a: json.loads(a))

# class ObjectFileConverter(BaseConverter):
#     """
#         Output a given object to a folder, mainly created to save/load test payload
#         Some information like index will be lost for pandas dataframe
#         A couple of predefined serializer/deserializers have already been included, if you need a type which is not covered, call register_type
#     """
#
#     def __init__(self, file_name_generator: FileNameGenerator):
#         super().__init__()
#         self.register_type('str', str, lambda a: ('str', a), lambda a: a)
#         self.register_type('None', type(None), lambda a: ('None', ''), lambda s: None)
#         self.register_type('pandas.DataFrame', pd.DataFrame, self._pd_serializer, self._pd_deserializer)
#         self.register_type('dict', dict, self._dict_serializer, self._dict_deserializer)
#         self._register_iter_type('list', list)
#         self._register_iter_type('tuple', tuple)
#         self._register_iter_type('set', set)
#         self._register_iter_type('frozenset', frozenset)
#         self.register_type('numpy.ndarray', np.ndarray,
#                            lambda a: self._iterable_json_serializer('numpy.ndarray', a),
#                            lambda s: self._ndarray_deserializer(s))
#         self.register_type('bool', bool, lambda b: ('bool', str(b)), lambda s: s == 'True')
#         self.register_type('numpy.bool', np.bool_, lambda b: ('numpy.bool', str(b)), lambda s: np.bool_(s == 'True'))
#         self._register_basic_type('int', int)
#         self._register_basic_type('float', float)
#         self._register_basic_type('complex', complex)
#         self._register_basic_type('numpy.float64', np.float64)
#         self._register_basic_type('numpy.int64', np.int64)
#         self.file_name_generator = file_name_generator
#
#     def _register_basic_type(self, type_name: str, type_type: type):
#         self.register_type(type_name, type_type, lambda a: (type_name, str(a)), lambda s: type_type(s))
#
#     def _register_iter_type(self, type_name, type_type: type):
#         self.register_type(type_name, type_type,
#                            lambda a: self._iterable_json_serializer(type_name, a),
#                            lambda s: self._iterable_json_deserializer(type_type, s))
#
#     def to_file(self, object_data, directory_absolute: str):
#         """
#         get an object of any kind, and save it to the given directory
#         the directory must NOT exist so we won't accidentally overwrite data
#         Args:
#             object_data:
#             directory_absolute:
#
#         Returns:
#
#         """
#         pathlib.Path(directory_absolute).mkdir(parents=True, exist_ok=False)
#         self.file_name_generator.reset()
#
#         cwd = os.getcwd()
#         os.chdir(directory_absolute)
#
#         type_name, value = self.serialize(object_data)
#         with open(self.file_name_generator.get_entry(), 'x') as csv_file:
#             writer = csv.writer(csv_file)
#             writer.writerow(['type', 'value'])
#             writer.writerow([type_name, value])
#
#         os.chdir(cwd)
#
#     def from_file(self, directory_absolute: str):
#         """
#         Args:
#             directory_absolute:
#
#         Returns: object
#
#         """
#         cwd = os.getcwd()
#         os.chdir(directory_absolute)
#         with open(self.file_name_generator.get_entry(), 'r') as csv_file:
#             reader = csv.DictReader(csv_file)
#             row = next(reader)
#             result = self.deserialize(row['type'], row['value'])
#             os.chdir(cwd)
#             return result
#
#     def _dict_serializer(self, dict_data: dict):
#         csv_dicts = []
#         keys = list(dict_data.keys())
#         # sort here so it's easier to do diff
#         keys.sort()
#         for key in keys:
#             type_name, string_value = self.serialize(dict_data[key])
#             csv_dicts.append({
#                 'key': str(key),
#                 'type': type_name,
#                 'value': string_value
#             })
#
#         file_name = self.file_name_generator.get_name()
#         with open(file_name, 'x') as csv_file:
#             writer = csv.DictWriter(csv_file, fieldnames=['key', 'type', 'value'])
#             writer.writeheader()
#             for data in csv_dicts:
#                 writer.writerow(data)
#
#         return 'dict', file_name
#
#     def _dict_deserializer(self, string_data):
#         reader = csv.DictReader(open(string_data, 'r'))
#         data = {}
#         for row in reader:
#             data[row['key']] = self.deserialize(row['type'], row['value'])
#
#         return data
#
#     def _iterable_json_serializer(self, iter_type_name, iter_data):
#         data = []
#         for value in iter_data:
#             type_name, string_value = self.serialize(value)
#             data.append({
#                     'type': type_name,
#                     'value': string_value
#                 })
#
#         return iter_type_name, json.dumps(data, separators=(',', ':'))
#
#     def _iterable_json_deserializer(self, iter_type: type, string_data: str):
#         data_raw = json.loads(string_data)
#         data = [self.deserialize(row['type'], row['value']) for row in data_raw]
#         return iter_type(data)
#
#     def _ndarray_deserializer(self, string_data: str):
#         data_raw = json.loads(string_data)
#         data = [self.deserialize(row['type'], row['value']) for row in data_raw]
#         return np.asarray(data)
#
#     def _iterable_csv_serializer(self, iter_type_name, iter_data):
#         file_name = self.file_name_generator.get_name()
#         with open(file_name, 'x') as csv_file:
#             writer = csv.DictWriter(csv_file, fieldnames=['type', 'value'])
#             writer.writeheader()
#             for value in iter_data:
#                 type_name, string_value = self.serialize(value)
#                 writer.writerow({
#                     'type': type_name,
#                     'value': string_value
#                 })
#         return iter_type_name, file_name
#
#     def _iterable_csv_deserializer(self, iter_type: type, string_data: str):
#         reader = csv.DictReader(open(string_data, 'r'))
#         data = [self.deserialize(row['type'], row['value']) for row in reader]
#         return iter_type(data)
#
#     def _pd_serializer(self, pd_data: pd.DataFrame):
#         file_name = self.file_name_generator.get_name()
#         pd_data.to_csv(file_name)
#         return 'pandas.DataFrame', file_name
#
#     @staticmethod
#     def _pd_deserializer(string_data: str):
#         return pd.read_csv(string_data, index_col=False, keep_default_na=False, na_values='')
#
#
# converter = ObjectFileConverter(FileNameGenerator())
