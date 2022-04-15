import unittest
from unittest.mock import patch

from app.db.filters import AndFilter, Condition


class AndFilterTestCase(unittest.TestCase):
    def test_create_and_filter(self):
        af = AndFilter()
        self.assertListEqual(af.conditions, [])

    def test_and_filter_single_value_query_fragments(self):
        with patch.object(Condition, 'to_query_string', return_value="abc > %s"):
            af = AndFilter()
            cond = Condition(name="abc", value=3, operator=">")
            af.add_condition(condition=cond)
            res = af.collect_query_fragments()
            self.assertEqual("abc > %s", res)

    def test_and_filter_two_value_query_fragments(self):
        with patch.object(Condition, 'to_query_string', return_value="abc > %s"):
            af = AndFilter()
            cond = Condition(name="abc", value=3, operator=">")
            af.add_condition(condition=cond)
            af.add_condition(condition=cond)
            res = af.collect_query_fragments()
            self.assertEqual("abc > %s AND abc > %s", res)


if __name__ == '__main__':
    unittest.main()
