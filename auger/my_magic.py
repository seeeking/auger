import importlib.util
import inspect
import logging
import os
import sys
from collections import defaultdict
from shutil import copy2, rmtree

import my_runtime
from my_generator import DefaultGenerator, get_module_name
from comparators import comparator

logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(level=logging.DEBUG)


class Magic(object):
    def __init__(self, source_path, converter_init_file, extra_files=None,
                 source_file_to_exclude=None,
                 verbose=False, mock_substitutes=None):
        self._caller = inspect.stack()[1][1]

        self.output_path = os.path.join(source_path, 'tests')
        if os.path.exists(self.output_path):
            rmtree(self.output_path)

        self._file_names = Magic._list_module_files(source_path, source_file_to_exclude)
        logger.info(f'Included files are {",".join(self._file_names)}')

        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(os.path.join(self.output_path, 'fixtures'), exist_ok=True)

        self._copy_and_get_converter(converter_init_file)
        if extra_files:
            for file in extra_files:
                copy2(file, os.path.join(self.output_path, 'auger'))

        self.mock_substitutes = mock_substitutes
        self.extra_imports = [('.auger.auger_converter', 'converter')]
        self.verbose = verbose
        self.configs = {
            'converter_init_file': self.converter_path,
            'converter': self.converter,
            'output_path': self.output_path,
            'extra_imports': self.extra_imports,
            'comparators': comparator
        }
        self._calls = defaultdict(self._empty_function)

    def _copy_and_get_converter(self, converter_init_file):
        os.makedirs(os.path.join(self.output_path, 'auger'), exist_ok=True)
        self.converter_path = copy2(converter_init_file, os.path.join(self.output_path, 'auger', 'auger_converter.py'))
        spec = importlib.util.spec_from_file_location('auger_converter', self.converter_path)
        converter_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(converter_module)
        self.converter = converter_module.converter

    def _empty_function(self):
        return my_runtime.Function(self.converter)

    @staticmethod
    def _list_module_files(source_path, source_file_to_exclude):
        if source_file_to_exclude:
            source_file_to_exclude = map(os.path.abspath, source_file_to_exclude)
        else:
            source_file_to_exclude = []

        logger.debug(source_file_to_exclude)
        files = []
        for (dirpath, dirnames, filenames) in os.walk(source_path):
            for name in filenames:
                if name.endswith('.py') and name not in source_file_to_exclude:
                    files.append(os.path.abspath(os.path.join(dirpath, name)))
        return files

    def _handle_call(self, code, args, ret, caller=None):
        print("call", code, args, ret, caller)
        function = self._calls[code]
        # if caller:
        #     self._calls[caller].add_mock(code, function)
        function.handle_call(code, args)

    def _handle_return(self, code, args, ret, caller=None):
        print("return", code, args, ret, caller)
        self._calls[code].handle_return(code, args, ret)

    def _handle_line(self, code, locals_dict, args, caller=None):
        pass

    def _handle_exception(self, code, locals_dict, args, caller=None):
        pass

    def __enter__(self):
        sys.setprofile(self._trace)

    def __exit__(self, exception_type, value, tb):
        sys.setprofile(None)
        for filename, functions in self.group_by_file(self._file_names, self._calls).items():
            _generator = DefaultGenerator(self.configs)
            test = _generator.dump(filename, functions)
            if self.verbose:
                print('=' * 47 + ' Auger ' + '=' * 46)
                print(test)
                print('=' * 100)
            else:
                modname = get_module_name(filename)
                if modname == '__main__':
                    modname = filename.replace('.py', '').capitalize()
                root = filename
                for _ in modname.split('.'):
                    root = os.path.dirname(root)
                output = os.path.join(self.output_path, f"test_{modname.replace('.', '_')}.py")
                dir = os.path.dirname(output)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                with open(output, 'w') as f:
                    f.write(test)
                print('Auger: generated test: %s' % output)

    def group_by_file(self, file_names, function_calls):
        file_names = set(file_names)
        files = defaultdict(list)
        for code, function in function_calls.items():
            file_name = os.path.normpath(code.co_filename)
            if file_name in file_names:
                files[file_name].append((code, function))
        return files

    def _trace(self, frame, event, ret):
        if not hasattr(self, '_handle_' + event):
            logger.info(f'Ignoring event {event}')
            return
        handler = getattr(self, '_handle_' + event)
        top = frame.f_code.co_filename
        # caller = frame.f_back.f_code.co_filename

        # To filter out builtins, see https://stackoverflow.com/a/53404188/4237785
        if top in self._file_names and not any(x in frame.f_code.co_name for x in ['<']):
            handler(frame.f_code, frame.f_locals, ret)
        # if caller in self._file_names and top != caller:
        #     handler(frame.f_code, frame.f_locals, ret, frame.f_back.f_code)
