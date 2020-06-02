import sys
import types


class Function(object):
    def __init__(self, converter):
        self.converter = converter
        self.calls = []
        self.work = []

    def set_converter(self, converter):
        self.converter = converter

    def handle_call(self, code, args):
        before_args = {p:args[p] for p in list(code.co_varnames)[:code.co_argcount]}
        self.work.append(self._serialize_args(before_args))

    def handle_return(self, code, args, ret):
        before_args = self.work.pop()
        after_args = {p:args[p] for p in list(code.co_varnames)[:code.co_argcount]}
        print("=" * 10, 'AFTER')
        print(args)
        print(after_args)
        self.calls.append((before_args, self.converter.serialize(ret), self._serialize_args(after_args)))

    def _serialize_args(self, args):
        return {
            key: self.converter.serialize(value)
            for key, value in args.items()
        }


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
