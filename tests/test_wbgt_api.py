import unittest
from hsbot.utils.wbgt_api import (
    get_yohou, get_jikkyou
)
from hsbot.utils.wbgt import WBGT
from requests.exceptions import HTTPError
from datetime import (
    datetime, timedelta
)


class TestWbgtApi(unittest.TestCase):
    """
    test class of http_client.py
    """

    def test_get_yohou(self):
        """
        test method for get_yohou
        """
        actual = get_yohou('46106')
        self.assertEqual(list, type(actual))
        self.assertEqual(WBGT, type(actual[-1]))
        self.assertEqual(str, type(actual[-1].date))
        self.assertEqual(float, type(actual[-1].degree))

    def test_get_jikkyou_normal(self):
        """
        (normal)
        test method for get_jikkyou
        """
        actual = get_jikkyou('46106', '201904')
        self.assertEqual(WBGT, type(actual))
        self.assertEqual(str, type(actual.date))
        self.assertEqual(float, type(actual.degree))

    def test_get_jikkyou_normal_too_early(self):
        """
        (normal)
        test method for get_jikkyou
        just a month has changed
        """
        today = datetime.now()
        later_date = datetime.now() + timedelta(days=1)
        while (today.month == later_date.month):
            later_date += timedelta(days=1)
        later_ym = later_date.strftime('%Y%m')
        actual = get_jikkyou('46106', later_ym)
        self.assertEqual(WBGT, type(actual))
        self.assertEqual(str, type(actual.date))
        self.assertEqual(int(today.strftime('%Y%m')),
                         int(actual.date[0:6]))
        self.assertEqual(float, type(actual.degree))

    def test_get_jikkyou_abnormal(self):
        """
        (abnormal)
        test method for get_jikkyou
        """
        with self.assertRaises(HTTPError):
            get_jikkyou('46106', '201903')
