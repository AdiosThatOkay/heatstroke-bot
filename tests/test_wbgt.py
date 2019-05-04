import unittest
from hsbot.utils.wbgt import WBGT


class TestWBGT(unittest.TestCase):
    """
    test class of wbgt.py
    """

    def test_risk(self):
        """
        test method of wbgt.risk
        """
        wbgt0 = WBGT("46106", "2019042815", 0.1)
        self.assertEqual("ほぼ安全", wbgt0.risk())

        wbgt1 = WBGT("46106", "2019042815", 20.9)
        self.assertEqual("ほぼ安全", wbgt1.risk())

        wbgt2 = WBGT("46106", "2019042815", 21.0)
        self.assertEqual("注意", wbgt2.risk())

        wbgt3 = WBGT("46106", "2019042815", 21)
        self.assertEqual("注意", wbgt3.risk())

        wbgt4 = WBGT("46106", "2019042815", 100)
        self.assertEqual("危険", wbgt4.risk())

    def test_message(self):
        """
        test method od wbgt.message
        """
        wbgt0 = WBGT("46106", "2019042815", 0.1)
        self.assertEqual("熱中症の危険は小さいですが、運動の合間などに\
適宜水分・塩分の補給をしましょう。", wbgt0.message())

        wbgt1 = WBGT("46106", "2019042815", 24.9)
        self.assertEqual("熱中症の危険は小さいですが、運動の合間などに\
適宜水分・塩分の補給をしましょう。", wbgt1.message())

        wbgt2 = WBGT("46106", "2019042815", 25.0)
        self.assertEqual("熱中症の危険があります。運動の際には定期的に\
十分な休息を取りましょう。", wbgt2.message())

        wbgt3 = WBGT("46106", "2019042815", 25)
        self.assertEqual("熱中症の危険があります。運動の際には定期的に\
十分な休息を取りましょう。", wbgt3.message())

        wbgt4 = WBGT("46106", "2019042815", 28)
        self.assertEqual("熱中症の危険性が高いです。外出時は炎天下を避け、\
室内ではエアコンなどをつけて室温を下げましょう。", wbgt4.message())

        wbgt5 = WBGT("46106", "2019042815", 100)
        self.assertEqual("""\
熱中症の危険性がかなり高いです。外出はなるべく避け、涼しい室内に移動しましょう。
特別な場合以外は、運動を中止しましょう。特に子どもの場合は中止すべきです。""",
                         wbgt5.message())

    def test_get_year(self):
        wbgt = WBGT("46106", "2019042815", 15.0)
        self.assertEqual("2019", wbgt.get_year())

    def test_get_month(self):
        wbgt = WBGT("46106", "2019042815", 15.0)
        self.assertEqual("04", wbgt.get_month())

    def test_get_short_month(self):
        wbgt0 = WBGT("46106", "2019040506", 15.0)
        self.assertEqual("4", wbgt0.get_short_month())
        wbgt1 = WBGT("46106", "2019100506", 15.0)
        self.assertEqual("10", wbgt1.get_short_month())

    def test_get_day(self):
        wbgt = WBGT("46106", "2019042815", 15.0)
        self.assertEqual("28", wbgt.get_day())

    def test_get_short_day(self):
        wbgt0 = WBGT("46106", "2019040506", 15.0)
        self.assertEqual("5", wbgt0.get_short_day())
        wbgt1 = WBGT("46106", "2019101106", 15.0)
        self.assertEqual("11", wbgt1.get_short_day())

    def test_get_hour(self):
        wbgt = WBGT("46106", "2019042815", 15.0)
        self.assertEqual("15", wbgt.get_hour())

    def test_get_short_hour(self):
        wbgt0 = WBGT("46106", "2019040506", 15.0)
        self.assertEqual("6", wbgt0.get_short_hour())
        wbgt1 = WBGT("46106", "2019101113", 15.0)
        self.assertEqual("13", wbgt1.get_short_hour())

    def test_get_weekday(self):
        wbgt0 = WBGT("46106", "2019042815", 15.0)
        self.assertEqual("(日)", wbgt0.get_weekday())

        wbgt1 = WBGT("46106", "2019042924", 15.0)
        self.assertEqual("(月)", wbgt1.get_weekday())

    def test_get_n_days_later(self):
        wbgt0 = WBGT("46106", "2019040103", 15.0)
        self.assertEqual("2019040200", wbgt0.get_n_days_later(1).date)
        wbgt1 = WBGT("46106", "2019042803", 15.0)
        self.assertEqual("2019043000", wbgt1.get_n_days_later(2).date)
        wbgt2 = WBGT("46106", "2019042803", 15.0)
        self.assertEqual("2019050100", wbgt2.get_n_days_later(3).date)

    def test_later_than(self):
        wbgt0 = WBGT("46106", "2019042815", 15.0)
        wbgt1 = WBGT("46106", "2019042815", 16.0)
        wbgt2 = WBGT("46106", "2019042818", 15.0)
        wbgt3 = WBGT("46106", "2019043012", 15.0)
        wbgt4 = WBGT("46106", "2019050103", 15.0)
        wbgt5 = WBGT("46106", "2020010101", 15.0)
        self.assertFalse(wbgt1.later_than(wbgt0))
        self.assertTrue(wbgt2.later_than(wbgt1))
        self.assertTrue(wbgt3.later_than(wbgt2))
        self.assertTrue(wbgt4.later_than(wbgt3))
        self.assertTrue(wbgt5.later_than(wbgt4))

    def test_is_same_day(self):
        wbgt0 = WBGT("46106", "2019042815", 15.0)
        wbgt1 = WBGT("46106", "2019042818", 16.0)
        wbgt2 = WBGT("46106", "2019042918", 15.0)
        self.assertTrue(wbgt0.is_same_day(wbgt1))
        self.assertFalse(wbgt2.is_same_day(wbgt1))
