import unittest
from lib.http_client import (
    get_yohou, get_jikkyou
)


class TestHttpClient(unittest.TestCase):
    """
    test class of http_client.py
    """

    def test_get_yohou(self):
        """
        test method for get_yohou
        """
        actual = get_yohou(46106)
        self.assertEqual(
            "http://www.wbgt.env.go.jp/prev15WG/dl/yohou_46106.csv", actual)

    def test_get_jikkyou(self):
        """
        test method for get_jikkyou
        """
        actual = get_jikkyou("kanagawa", "201904")
        self.assertEqual(
            "http://www.wbgt.env.go.jp/est15WG/dl/wbgt_kanagawa_201904.csv",
            actual)
