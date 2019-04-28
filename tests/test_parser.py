import unittest
from lib.parser import (
    parse_yohou, parse_jikkyou
)
from lib.wbgt import WBGT


class TestParser(unittest.TestCase):
    """
    test class of parser.py
    """

    def test_parse_yohou(self):
        """
        test method of parser.parse_yohou
        """
        actual = parse_yohou('./tests/sample/yohou.csv')
        self.assertEqual(list, type(actual))
        self.assertEqual(WBGT, type(actual[0]))
        self.assertEqual("2019042815", actual[0].date)
        self.assertEqual(14.0, actual[0].degree)

    def test_parse_jikkyou_normal(self):
        """
        (normal)
        test method of parser.parse_jikkyou
        """
        actual = parse_jikkyou('./tests/sample/jikkyou_normal.csv')
        self.assertEqual(WBGT, type(actual))
        self.assertEqual("2019042813", actual.date)
        self.assertEqual(14.9, actual.degree)

    def test_parse_jikkyou_full(self):
        """
        (normal) full_degree
        test method of patser.parse_jikkyou
        """
        actual = parse_jikkyou('./tests/sample/jikkyou_full_degree.csv')
        self.assertEqual(WBGT, type(actual))
        self.assertEqual("2019042824", actual.date)
        self.assertEqual(14.9, actual.degree)

    def test_parse_jikkyou_no_degree(self):
        """
        (abnormal) no_degree
        test method of parser.parse_jikkyou
        """
        actual = parse_jikkyou('./tests/sample/jikkyou_no_degree.csv')
        self.assertIsNone(actual)
