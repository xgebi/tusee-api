import unittest
from unittest.mock import patch

from app.db.filters import Condition, Filter


class FilterTestCase(unittest.TestCase):
    def test_create_filter(self):
        f = Filter()
        self.assertEqual(Filter, type(f))

    def test_and_filter_single_value_query_fragments(self):
        with patch.object(Condition, 'to_query_string', return_value="abc > %s"):
            af = Filter()
            cond = Condition(name="abc", value=3, operator=">")
            af.add_condition(condition=cond)
            res = af.collect_query_fragments()
            self.assertEqual("abc > %s", res)

    def test_and_filter_single_value(self):
        af = Filter()
        cond = Condition(name="abc", value=3, operator=">")
        af.add_condition(condition=cond)
        self.assertEqual(len(af.conditions), 1)
        self.assertListEqual(af.conditions, [cond])

    def test_and_filter_two_value(self):
        af = Filter()
        cond1 = Condition(name="abc", value=3, operator=">")
        cond2 = Condition(name="abc", value=3, operator="<")
        af.add_condition(condition=cond1)
        af.add_condition(condition=cond2)
        self.assertEqual(len(af.conditions), 2)
        self.assertListEqual(af.conditions, [cond1, cond2])

    def test_and_filter_single_value_query_values(self):
        with patch.object(Condition, 'query_values', return_value=[3]):
            af = Filter()
            cond = Condition(name="abc", value=3, operator=">")
            af.add_condition(condition=cond)
            res = af.collect_values()
            self.assertListEqual([3], res)

    def test_and_filter_two_value_query_values(self):
        with patch.object(Condition, 'query_values', return_value=[3]):
            af = Filter()
            cond1 = Condition(name="abc", value=3, operator=">")
            cond2 = Condition(name="abc", value=3, operator="<")
            af.add_condition(condition=cond1)
            af.add_condition(condition=cond2)
            self.assertListEqual([3, 3], af.collect_values())


if __name__ == '__main__':
    unittest.main()
