import unittest

from app.db.filters import Condition


class ConditionTestCase(unittest.TestCase):
    def test_condition_is_created(self):
        cond = Condition(name="column", value=3, operator=">")
        self.assertEqual(cond.name, "column")

    def test_condition_is_created_between(self):
        cond = Condition(name="column", value=3, secondary_value=6, operator="between")
        self.assertEqual(cond.name, "column")

    def test_condition_is_not_created_operator(self):
        self.assertRaises(Exception, Condition, "abc", 1, "nope")

    def test_condition_is_not_created_name(self):
        self.assertRaises(Exception, Condition, None, 1, ">")

    def test_condition_is_not_created_value(self):
        self.assertRaises(Exception, Condition, "abc", None, ">")

    def test_condition_is_not_created_between_no_secondary_value(self):
        self.assertRaises(Exception, Condition, name="column", value=3, operator="between")

    def test_to_query_string(self):
        cond = Condition(name="column", value=3, operator=">")
        self.assertEqual(cond.to_query_string(), "column > %s")

    def test_to_query_string_between(self):
        cond = Condition(name="column", value=3, secondary_value=6, operator="BETWEEN")
        self.assertEqual(cond.to_query_string(), "column BETWEEN %s AND %s")

    def test_query_values(self):
        cond = Condition(name="column", value=3, operator=">")
        self.assertListEqual(cond.query_values(), [3])

    def test_query_values_between(self):
        cond = Condition(name="column", value=3, secondary_value=6, operator="BETWEEN")
        self.assertListEqual(cond.query_values(), [3, 6])


if __name__ == '__main__':
    unittest.main()
