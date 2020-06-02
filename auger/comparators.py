from collections import defaultdict, namedtuple

Comparator = namedtuple('Comparator', ['function_name', 'additional_imports'])

comparator = defaultdict(lambda :Comparator('self.assertEqual', []))

comparator['pd.DataFrame'] = Comparator('assert_frame_equal', ['pandas.util.testing', 'assert_frame_equal'])
comparator['pd.Series'] = Comparator('assert_series_equal', ['pandas.util.testing', 'assert_series_equal'])