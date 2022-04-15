import unittest
from unittest.mock import patch

from app.db.filters import Condition, OrFilter


class OrFilterTestCase(unittest.TestCase):
    def test_create_filter(self):
        of = OrFilter()
        self.assertEqual(OrFilter, type(of))

    def test_and_filter_single_value_query_fragments(self):
        with patch.object(Condition, 'to_query_string', return_value="abc > %s"):
            of = OrFilter()
            cond = Condition(name="abc", value=3, operator=">")
            of.add_condition(condition=cond)
            res = of.collect_query_fragments()
            self.assertEqual("abc > %s", res)

    def test_and_filter_two_value_query_fragments(self):
        with patch.object(Condition, 'to_query_string', return_value="abc > %s"):
            of = OrFilter()
            cond = Condition(name="abc", value=3, operator=">")
            of.add_condition(condition=cond)
            of.add_condition(condition=cond)
            res = of.collect_query_fragments()
            self.assertEqual("abc > %s OR abc > %s", res)


if __name__ == '__main__':
    unittest.main()
