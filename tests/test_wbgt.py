import unittest
from datetime import datetime
from lib.wbgt import WBGT


class TestWBGT(unittest.TestCase):
    """
    test class of wbgt.py
    """

    def test_guideline(self):
        """
        test method of wbgt.guideline
        """
        wbgt0 = WBGT(datetime.now(), 0.1)
        self.assertEqual("ほぼ安全", wbgt0.guideline())

        wbgt1 = WBGT(datetime.now(), 20.9)
        self.assertEqual("ほぼ安全", wbgt1.guideline())

        wbgt2 = WBGT(datetime.now(), 21.0)
        self.assertEqual("注意", wbgt2.guideline())

        wbgt3 = WBGT(datetime.now(), 21)
        self.assertEqual("注意", wbgt3.guideline())

        wbgt4 = WBGT(datetime.now(), 100)
        self.assertEqual("危険", wbgt4.guideline())

    def test_message(self):
        """
        test method od wbgt.message
        """
        wbgt0 = WBGT(datetime.now(), 0.1)
        self.assertEqual("熱中症の危険は小さいですが、運動の合間などに\
適宜水分・塩分の補給をしましょう。", wbgt0.message())

        wbgt1 = WBGT(datetime.now(), 24.9)
        self.assertEqual("熱中症の危険は小さいですが、運動の合間などに\
適宜水分・塩分の補給をしましょう。", wbgt1.message())

        wbgt2 = WBGT(datetime.now(), 25.0)
        self.assertEqual("熱中症の危険があります。運動の際には定期的に\
十分な休息を取りましょう。", wbgt2.message())

        wbgt3 = WBGT(datetime.now(), 25)
        self.assertEqual("熱中症の危険があります。運動の際には定期的に\
十分な休息を取りましょう。", wbgt3.message())

        wbgt4 = WBGT(datetime.now(), 28)
        self.assertEqual("熱中症の危険性が高いです。外出時は炎天下を避け、\
室内ではエアコンなどをつけて室温を下げましょう。", wbgt4.message())

        wbgt5 = WBGT(datetime.now(), 100)
        self.assertEqual("""\
熱中症の危険性がかなり高いです。外出はなるべく避け、涼しい室内に移動しましょう。
特別な場合以外は、運動を中止しましょう。特に子どもの場合は中止すべきです。""",
                         wbgt5.message())
