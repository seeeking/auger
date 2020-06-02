from collections import defaultdict, namedtuple

FuncAndImports = namedtuple('Comparator', ['function_name', 'additional_imports'])

comparator = defaultdict(lambda :FuncAndImports('self.assertEqual', []))

comparator['pd.DataFrame'] = FuncAndImports('assert_frame_equal', ['pandas.util.testing', 'assert_frame_equal'])
comparator['pd.Series'] = FuncAndImports('assert_series_equal', ['pandas.util.testing', 'assert_series_equal'])