import inspect
import random
import sys
import traceback

from auger import runtime
from auger.generator.generator import Generator
from auger.generator.generator import get_module_name


# TODO change indent
def indent(n):
    return ' ' * 4 * n


class DefaultGenerator(Generator):
    def __init__(self, configs):
        Generator.__init__(self)
        self.output_ = []
        self.imports_ = {('unittest',)}
        self.instances = {}
        self.configs = configs
        self.converter = 'converter'

    def set_extra_imports(self, imports):
        for imp in imports:
            self.imports_.add(imp)


    def dump(self, filename, functions):
        self.output_ = []
        self.dump_tests(filename, functions)
        for line in open(filename):
            line = line.replace('\n', '')
            if line.startswith('import '):
                self.add_import(line.replace('import ', ''))
            if line.startswith('from '):
                module  = line.replace('from ', '').split(' import')[0]
                imports = [import_.strip() for import_ in line.split('import ')[1].split(',')]
                for import_ in imports:
                    self.add_import(module, import_)
        return '\n'.join(self.format_imports() + self.output_)

    def format_imports(self):
        imports = sorted(self.imports_)

        def format(imp):
            mod = self.get_declared_module_name(imp[0])
            if len(imp) == 2:
                if mod != '__main__':
                    return 'from %s import %s' % (mod, imp[1])
            return 'import %s' % mod
        return list(map(format, imports))

    def collect_instances(self, functions):
        for code, function in filter(lambda fn: runtime.get_code_name(fn[0]) == '__init__', functions):
            for (args, _, _) in function.calls[:1]:
                func_self = args['self']
                func_self_type = func_self.__class__
                for base in func_self.__class__.__bases__:
                    for _, init in filter(lambda member: member[0] == '__init__', inspect.getmembers(base)):
                        if getattr(init, "__code__", None) == code:
                            func_self_type = base
                mod = func_self_type.__module__
                self.add_import(mod, func_self_type.__name__)
                self.instances[self.get_object_id(type(func_self), func_self)] = (func_self_type.__name__, code, args)

    def find_module(self, code):
        for modname, mod in sys.modules.items():
            file = getattr(mod, '__file__').replace('.pyc', '.py') \
                if hasattr(mod, '__file__') and getattr(mod, '__file__') is not None else ''
            if file == runtime.get_code_filename(code):
                if modname == "__main__":
                    modname = file.replace(".py", "").replace("/", ".")
                self.add_import(modname)
                return modname, mod

    def get_defining_item(self, code):
        filename = runtime.get_code_filename(code)
        lineno = runtime.get_code_lineno(code)
        modname, mod = self.find_module(code)
        print(filename, lineno, modname, mod)

        for _,clazz in inspect.getmembers(mod, predicate=inspect.isclass):
            print(clazz)
            for _,member in inspect.getmembers(clazz, predicate=inspect.ismethod):
                member_code = runtime.get_code(member)
                member_filename = runtime.get_code_filename(member_code)
                member_lineno = runtime.get_code_lineno(member_code)
                print(indent(1), member_filename, member_lineno)
                if filename == member_filename and lineno == member_lineno:
                    self.add_import(modname, clazz.__name__)
                    return clazz, member
            for _,member in inspect.getmembers(clazz, predicate=lambda member: isinstance(member, property)):
                self.add_import(modname, clazz.__name__)
                print(indent(4), member_filename, member_lineno)
                return clazz, member
            for _,member in inspect.getmembers(clazz, predicate=inspect.isfunction):
                member_code = runtime.get_code(member)
                member_filename = runtime.get_code_filename(member_code)
                member_lineno = runtime.get_code_lineno(member_code)
                print(indent(2), member_filename, member_lineno)
                if filename == member_filename and lineno == member_lineno:
                    self.add_import(modname, clazz.__name__)
                    return clazz, member

        # TODO this is most likely not correct or not necessary
        for _,member in inspect.getmembers(mod, predicate=inspect.isfunction):
            # Module-level function support, note the difference in return statement
            member_code = runtime.get_code(member)
            member_filename = runtime.get_code_filename(member_code)
            member_lineno = runtime.get_code_lineno(member_code)
            print(indent(3), member_filename, member_lineno)
            if filename == member_filename and lineno == member_lineno:
                self.add_import(modname, member.__name__)
                return mod, member
        if modname != '__main__':
            self.add_import(modname)
        return mod, mod

    def get_initializer(self, typename, code=None, init_args=None):
        if code and init_args:
            args, varargs, kwargs = inspect.getargs(code)
            params = ', '.join(
                [repr(init_args[arg]) for arg in args[1:]] +
                [repr(arg) for arg in init_args.get(varargs, [])] +
                ['%s=%s' % (k, repr(v)) for k, v in init_args.get(kwargs, {})]
            )
        else:
            params = ""
        return '%s(%s)' % (typename, params)

    def get_instance(self, instances, func_self):
        _type = type(func_self)
        return instances.get(self.get_object_id(_type, func_self)) or (func_self.__class__.__name__, _type, {})

    def dump_call(self, filename, code, call):
        definer, member = self.get_defining_item(code)
        print(call)
        before_args, return_value, after_args = call

        self.add_import(filename)
        target = definer.__name__

        # Useful for debugging
        print('-' * 80)
        print('call:   ', call)
        print('definer:', definer)
        print('member: ', member)
        print('target: ', target)
        print('name:   ', runtime.get_code_name(code))
        print('-' * 80)

        for k, v in before_args.items():
            self.output_.append(indent(2) + f'arg_{k} = {self._write_descrialize(v)}')

        call = indent(2) + 'actual_ret = %s.%s' % (target, runtime.get_code_name(code))
        call += '(%s)' % (
            ','.join([f'{k}=arg_{k}' for k in before_args.keys()]),
        )
        self.output_.append(call)

        self.output_.append('')
        self.output_.append(indent(2) + '# check return value')
        self.output_.append(self._assert_equals('actual_ret', self._write_descrialize(return_value)))

        self.output_.append(indent(2) + '# check parameter mutation')
        for k, v in after_args.items():
            self.output_.append(indent(2) + f'expected_arg_{k} = {self._write_descrialize(v)}')
            self.output_.append(self._assert_equals(f'expected_arg_{k}', f'arg_{k}'))

        self.output_.append('')

    @staticmethod
    def _assert_equals(expected_str, actual_str):
        return ''.join([
            indent(2),
            'self.assertEquals(\n',
            indent(3),
            f'{expected_str},\n',
            indent(3),
            f'{actual_str}\n',
            indent(2),
            ')\n'
        ])

    def _write_descrialize(self, v):
        return f'{self.converter}.deserialize({DefaultGenerator._quote(v[0])}, {DefaultGenerator._quote(v[1])})'

    @staticmethod
    def _quote(string_value):
        return '"' + string_value.replace('"', '\\"') + '"'

    def dump_tests(self, filename, functions):
        self.collect_instances(functions)
        self.output_.append('')
        self.output_.append('')
        self.output_.append('class %s(unittest.TestCase):' % self.get_testname(filename))
        functions = filter(lambda fn: runtime.get_code_name(fn[0]) != '__init__', functions)
        functions = sorted(functions, key=lambda fn: runtime.get_code_name(fn[0]))
        for code, function in functions:
            print("=" * 80)
            print("processing...")
            print(code)
            print(function)
            if function.calls:
                self.output_.append(indent(1) + 'def test_%s(self):' % (runtime.get_code_name(code)))
                try:
                    self.dump_call(filename, code, random.choice(function.calls))
                except:
                    traceback.print_exc()

        self.output_.append('if __name__ == "__main__":')
        self.output_.append(indent(1) + 'unittest.main()\n')

    def add_import(self, module_name, part_name=None):
        module_name = self.get_declared_module_name(self.get_modname(module_name))
        if part_name:
            if module_name in sys.modules:
                mod = sys.modules[module_name]
                if not hasattr(mod, part_name):
                    return

        print(module_name, part_name)
        self.imports_.add((module_name, part_name) if part_name else (module_name,))

    @staticmethod
    def get_filename(code):
        return DefaultGenerator.shorten_filename(runtime.get_code_filename(code))

    @staticmethod
    def shorten_filename(filename):
        return filename.split('/')[-1].split('\\')[-1]

    @staticmethod
    def get_lineno(code):
        return code.co_firstlineno

    @staticmethod
    def get_location(code):
        return '%s:%s' % (DefaultGenerator.get_filename(code), DefaultGenerator.get_lineno(code))

    @staticmethod
    def get_testname(filename):
        return DefaultGenerator.shorten_filename(filename).replace('.py', '').capitalize() + 'Test'

    @staticmethod
    def get_object_id(obj_type, obj):
        return '%s:%s' % (obj_type.__name__, id(obj))

    def get_modname(self, filename):
        return get_module_name(filename)

    @staticmethod
    def is_object(obj):
        return hasattr(obj, '__dict__')

    @staticmethod
    def get_assert(value):
        return 'IsInstance' if DefaultGenerator.is_object(value) else 'Equal'

    @staticmethod
    def get_full_class_name(value):
        return value.__class__.__module__ + "." + value.__class__.__name__

    @staticmethod
    def get_assert_value(value):
        value = DefaultGenerator.get_full_class_name(value) if DefaultGenerator.is_object(value) else repr(value)
        return value.replace("<type '", '').replace("'>", '')


