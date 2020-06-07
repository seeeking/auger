import sys
import types


class Function(object):
    def __init__(self, converter, mock_module_names):
        self.converter = converter
        self.calls = []
        self.work = []
        self.mocks = {}
        self.mock_module_names = mock_module_names

    def set_converter(self, converter):
        self.converter = converter

    def handle_call(self, code, locals):
        before_args = {p:locals[p] for p in list(code.co_varnames)[:code.co_argcount]}
        self.work.append(self._serialize_args(before_args))

    def handle_return(self, code, locals, ret):
        before_args = self.work.pop()
        after_args = {p:locals[p] for p in list(code.co_varnames)[:code.co_argcount]}
        self.calls.append((before_args, self._serialize_values(ret), self._serialize_args(after_args)))

    # preserve the value
    def _serialize_args(self, args):
        serialized = {
            key: self._serialize_values(value)
            for key, value in args.items()
        }

        return serialized

    def _serialize_values(self, value):
        return self.converter.serialize(value) \
            if getattr(value, '__module__', '').split('.')[0] not in self.mock_module_names \
            else getattr(value, '__code__', '') # TODO this only works if we don't care about the args to mocks or return

    def add_mock(self, code, function):
        self.mocks[code] = function

    def __str__(self):
        return 'Function:\n' + '\n'.join([f'{a}: {str(getattr(self, a))}' for a in dir(self) if not a.startswith('__')
                                          and not isinstance(getattr(self, a), types.MethodType) ])

def get_code(func):
    return func.__code__

def get_code_filename(code):
    return code.co_filename

def get_code_name(code):
    return code.co_name

def get_code_lineno(code):
    return code.co_firstlineno

def unsupported():
    raise NotImplementedError("Unsupported Python version %s" % sys.version)
