import inspect
import os
import random
import string
import sys
from shutil import move
import logging

from auger import runtime
from auger.generator.generator import Generator
from auger.generator.generator import get_module_name


logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(level=logging.DEBUG)

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
        self.comparators = configs.get('comparators')
        self.converter = 'converter'
        if configs.get('extra_imports', []):
            for imp in configs.get('extra_imports', []):
                self.imports_.add(imp)

    def dump(self, filename, functions):
        self.output_ = []
        self.dump_tests(filename, functions)
        # for line in open(filename):
        #     line = line.replace('\n', '')
        #     if line.startswith('import '):
        #         self.add_import(line.replace('import ', ''))
        #     if line.startswith('from '):
        #         module  = line.replace('from ', '').split(' import')[0]
        #         imports = [import_.strip() for import_ in line.split('import ')[1].split(',')]
        #         for import_ in imports:
        #             self.add_import(module, import_)
        return '\n'.join(self.format_imports(self.imports_) + self.output_)

    def format_imports(self, imports):
        imports = sorted(imports)
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
        # logger.debug(filename, lineno, modname, mod)

        for _,clazz in inspect.getmembers(mod, predicate=inspect.isclass):
            logger.debug(clazz)
            for _,member in inspect.getmembers(clazz, predicate=inspect.ismethod):
                member_code = runtime.get_code(member)
                member_filename = runtime.get_code_filename(member_code)
                member_lineno = runtime.get_code_lineno(member_code)
                # logger.debug(indent(1), member_filename, member_lineno)
                if filename == member_filename and lineno == member_lineno:
                    self.add_import(modname, clazz.__name__)
                    return clazz, member
            for _,member in inspect.getmembers(clazz, predicate=lambda member: isinstance(member, property)):
                self.add_import(modname, clazz.__name__)
                # logger.debug(indent(4), member_filename, member_lineno)
                return clazz, member
            for _,member in inspect.getmembers(clazz, predicate=inspect.isfunction):
                member_code = runtime.get_code(member)
                member_filename = runtime.get_code_filename(member_code)
                member_lineno = runtime.get_code_lineno(member_code)
                # logger.debug(indent(2), member_filename, member_lineno)
                if filename == member_filename and lineno == member_lineno:
                    self.add_import(modname, clazz.__name__)
                    return clazz, member

        # TODO this is most likely not correct or not necessary
        for _,member in inspect.getmembers(mod, predicate=inspect.isfunction):
            # Module-level function support, note the difference in return statement
            member_code = runtime.get_code(member)
            member_filename = runtime.get_code_filename(member_code)
            member_lineno = runtime.get_code_lineno(member_code)
            # logger.debug(indent(3), member_filename, member_lineno)
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

    def dump_call(self, filename, code, call, mocks):
        output_ = []
        definer, member = self.get_defining_item(code)
        if mocks:
            output_ += self.dump_mock_decorators(mocks, definer.__name__)
            output_.append(
                indent(1) + 'def test_%s(self%s):' % (runtime.get_code_name(code), self.get_mock_args(mocks)))
            output_ += self.dump_mock_return_values(mocks)
        else:
            output_.append(indent(1) +
                       f'def test_{runtime.get_code_name(code)}_{"".join(random.choices(string.ascii_letters + string.digits, k=4))}(self):')

        before_args, return_value, after_args = call

        self.add_import(filename)
        target = definer.__name__

        # Useful for debugging
        logger.debug('-' * 80)
        logger.debug(f'call:   {call}')
        logger.debug(f'definer: {definer}')
        logger.debug(f'member: {member}')
        logger.debug(f'target: {target}')
        logger.debug(f'name:   {runtime.get_code_name(code)}')
        logger.debug('-' * 80)

        print(before_args)
        for k, v in before_args.items():
            output_.append(indent(2) + f'arg_{k} = {self._write_descrialize(v)}')

        call = indent(2) + 'actual_ret = %s.%s' % (target, runtime.get_code_name(code))
        call += '(%s)' % (
            ','.join([f'{k}=arg_{k}' for k in before_args.keys()]),
        )
        output_.append(call)

        output_.append('')
        output_.append(indent(2) + '# check return value')
        output_ += self._assert_equals(self._write_descrialize(return_value), 'actual_ret', return_value.type_name)

        if after_args.items():
            output_.append(indent(2) + '# check parameter mutation')
        for k, v in after_args.items():
            if not inspect.iscode(v):
                output_.append(indent(2) + f'expected_arg_{k} = {self._write_descrialize(v)}')
                output_ += self._assert_equals(f'expected_arg_{k}', f'arg_{k}', v.type_name)

        output_.append('')
        return output_

    def _assert_equals(self, expected_str, actual_str, type_name):
        comparator = self.comparators[type_name]

        if comparator.additional_imports:
            self.add_import(*comparator.additional_imports)
        comparator = comparator.function_name
        return [
            f'{indent(2)}{comparator}(',
            f'{indent(3)}{expected_str},',
            f'{indent(3)}{actual_str}',
            f'{indent(2)})'
        ]

    def _write_descrialize(self, v):
        if inspect.iscode(v):
            return 'mock_%s' % runtime.get_code_name(v)

        if v.direct:
            return repr(self.configs['converter'].deserialize(v[0], v[1]))
        else:
            # TODO this part is so bad, improve it using (maybe) suggestions here https://stackoverflow.com/a/38839418/4237785
            move(v[1], os.path.join(self.configs['output_path'], 'fixtures', v[1]))
            return f'{self.converter}.deserialize({DefaultGenerator._quote(v[0])}, {DefaultGenerator._quote(os.path.join("tests", "fixtures", v[1]))})'

    @staticmethod
    def _quote(string_value):
        return '"' + string_value.replace('"', '\\"') + '"'

    def dump_tests(self, filename, functions):
        self.output_.append('')
        self.output_.append('')
        self.output_.append('class %s(unittest.TestCase):' % self.get_testname(filename))
        functions = filter(lambda fn: runtime.get_code_name(fn[0]) != '__init__', functions)
        functions = sorted(functions, key=lambda fn: runtime.get_code_name(fn[0]))
        for code, function in functions:
            print("Dumping", code, function)
            for call in function.calls:
                self.output_ = self.output_ + self.dump_call(filename, code, call, function.mocks)

        self.output_.append('')
        self.output_.append('if __name__ == "__main__":')
        self.output_.append(indent(1) + 'unittest.main()\n')

    def add_import(self, module_name, part_name=None):
        module_name = self.get_declared_module_name(self.get_modname(module_name))
        if part_name:
            if module_name in sys.modules:
                mod = sys.modules[module_name]
                if not hasattr(mod, part_name):
                    return

        self.imports_.add((module_name, part_name) if part_name else (module_name,))

    def dump_mock_decorators(self, mocks, definer):
        if mocks:
            self.add_import('unittest.mock', 'patch')
        output_ = []
        for code in reversed(list(mocks.keys())):
            # print(definer, member)
            output_.append(indent(1) + f'@patch(\'{definer}.{runtime.get_code_name(code)}\')')
        return output_

    def dump_mock_return_values(self, mocks):
        output_ = []
        for (code, mock_function) in mocks.items():
            _, return_value, _ = list(mock_function.calls)[0]
            output_.append(indent(2) + 'mock_%s.return_value = %s' %
                                (runtime.get_code_name(code), self._write_descrialize(return_value)))
        return output_

    @staticmethod
    def get_mock_args(mocks):
        return ''.join([', mock_%s' % runtime.get_code_name(code) for (code, mock) in mocks.items()])

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

