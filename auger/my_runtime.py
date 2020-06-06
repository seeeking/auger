import sys
import types


class Function(object):
    def __init__(self, converter, mock_module_names):
        self.converter = converter
        self.calls = []
        self.work = []
        self.mocks = []
        self.mock_module_names = mock_module_names

    def set_converter(self, converter):
        self.converter = converter

    def handle_call(self, code, args):
        before_args = {p:args[p] for p in list(code.co_varnames)[:code.co_argcount]}
        self.work.append(self._serialize_args(before_args))

    def handle_return(self, code, args, ret):
        before_args = self.work.pop()
        after_args = {p:args[p] for p in list(code.co_varnames)[:code.co_argcount]}
        self.calls.append((before_args, self.converter.serialize(ret), self._serialize_args(after_args)))

    # preserve the value
    def _serialize_args(self, args):
        serialized = {
            key: self.converter.serialize(value)
            for key, value in args.items()
            if getattr(value, '__module__', '').split('.')[0] not in self.mock_module_names
        }
        # serialized.update({
        #     key: self._write_mock(value)
        #     for key, value in args.items()
        #     if hasattr(value, '__module__') and getattr(value, '__module__') not in self.mock_module_names
        # })
        return serialized

    def add_mock(self, code, function):
        if (code, function) not in self.mocks:
            self.mocks.append((code, function))

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
