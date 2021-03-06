import unittest
from hsbot.utils.parser import (
    parse_yohou, parse_jikkyou
)
from hsbot.utils.wbgt import WBGT


class TestParser(unittest.TestCase):
    """
    test class of parser.py
    """

    def test_parse_yohou(self):
        """
        test method of parser.parse_yohou
        """
        with open('./tests/sample/yohou.csv') as csv:
            actual = parse_yohou(csv.read())
            self.assertEqual(list, type(actual))
            self.assertEqual(WBGT, type(actual[0]))
            self.assertEqual("46106", actual[0].observatory_code)
            self.assertEqual("2019042815", actual[0].date)
            self.assertEqual(14.0, actual[0].degree)

    def test_parse_jikkyou_normal(self):
        """
        (normal)
        test method of parser.parse_jikkyou
        """
        with open('./tests/sample/jikkyou_normal.csv') as csv:
            actual = parse_jikkyou(csv.read())
            self.assertEqual(WBGT, type(actual))
            self.assertEqual("43056", actual.observatory_code)
            self.assertEqual("2019042813", actual.date)
            self.assertEqual(14.9, actual.degree)

    def test_parse_jikkyou_full(self):
        """
        (normal) full_degree
        test method of patser.parse_jikkyou
        """
        with open('./tests/sample/jikkyou_full_degree.csv') as csv:
            actual = parse_jikkyou(csv.read())
            self.assertEqual(WBGT, type(actual))
            self.assertEqual("43056", actual.observatory_code)
            self.assertEqual("2019042824", actual.date)
            self.assertEqual(14.9, actual.degree)

    def test_parse_jikkyou_no_degree(self):
        """
        (abnormal) no_degree
        It doesn't actually happen
        test method of parser.parse_jikkyou
        """
        with self.assertRaises(Exception):
            with open('./tests/sample/jikkyou_no_degree.csv') as csv:
                parse_jikkyou(csv.read())
