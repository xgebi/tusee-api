import unittest

from app.db.column import Column


class ColumnTestCase(unittest.TestCase):
    def test_column_creation(self):
        c = Column(
            data_type=str,
        )
        self.assertEqual(Column, type(c))

    def test_column_creation_fails(self):
        self.assertRaises(TypeError, Column)

    def test_column_creation_default_value(self):
        c = Column(
            data_type=str,
            default="test"
        )
        self.assertEqual("test", c.value)

    def test_column_creation_primary_value(self):
        c = Column(
            data_type=str,
            primary_key=True
        )
        self.assertEqual(True, c.primary_key)

    def test_create_null_value_nullable(self):
        self.assertRaises(Exception, Column, data_type=str, nullable=False)

    def test_set_value_not_none(self):
        c = Column(data_type=int, nullable=False, value=1)
        c.set(3)
        self.assertEqual(3, c.value)

    def test_set_value_none(self):
        c = Column(data_type=int, nullable=True, value=1)
        c.set(None)
        self.assertEqual(None, c.value)

    def test_set_value_fails(self):
        c = Column(data_type=int, nullable=False, value=1)
        self.assertRaises(Exception, c.set, None)


if __name__ == '__main__':
    unittest.main()
