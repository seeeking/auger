from __future__ import print_function
import os
import sys

file_to_module_name = dict()


def init_module_names():
    modules = [item for item in sys.modules.items()]
    file_to_module_name.update(dict(
        (getattr(mod, '__file__').replace('.pyc', '.py'), name)
        for name, mod in modules
        if hasattr(mod, '__file__') and getattr(mod, '__file__') is not None
    ))

def get_module_name(filename):
    path = os.path.normpath(filename)
    return file_to_module_name.get(path, filename)

class Generator(object):
    def __init__(self):
        init_module_names()
        self.substitues = {}
        self.imports = []

    def set_mock_substitutes(self, substitutes):
        self.substitues = substitutes

    def set_extra_imports(self, imports):
        self.imports = imports

    def get_declared_module_name(self, runtime_module_name):
        return self.substitues.get(runtime_module_name, runtime_module_name)

    def dump(self, module, functions):
        pass
