import unittest
from hsbot.models.observatories import Observatory


class TestObservatory(unittest.TestCase):
    def setUp(self):
        self.obs = Observatory("11101", "宗谷", "宗谷岬", "ｿｳﾔﾐｻｷ",
                               "稚内市宗谷岬", 45, 31.2, 141, 56.1)

    def test_lat60tolat10(self):
        expect = 45 + 31.2 / 60
        self.assertEqual(expect, self.obs.lat60tolat10())

    def test_lon60tolon10(self):
        expect = 141 + 56.1 / 60
        self.assertEqual(expect, self.obs.lon60tolon10())
