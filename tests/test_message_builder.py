import unittest
from hsbot.utils.message_builder import MessageBuilder
from hsbot.utils.parser import (
    parse_yohou, parse_jikkyou
)
from hsbot.utils.wbgt import WBGT


class TestMessageBuilder(unittest.TestCase):
    """
    test class of message_builder.py
    """

    def setUp(self):
        with open('./tests/sample/jikkyou_normal.csv') as jikkyou_csv:
            jikkyou_wbgt = parse_jikkyou(jikkyou_csv.read())
        with open('./tests/sample/yohou.csv') as yohou_csv:
            yohou_wbgt = parse_yohou(yohou_csv.read())
        self.mbuilder = MessageBuilder(jikkyou_wbgt, yohou_wbgt)

        with open('./tests/sample/jikkyou_24.csv') as jikkyou_csv_24:
            jikkyou_wbgt_24 = parse_jikkyou(jikkyou_csv_24.read())
        with open('./tests/sample/yohou_24.csv') as yohou_csv_24:
            yohou_wbgt_24 = parse_yohou(yohou_csv_24.read())
        self.mbuilder24 = MessageBuilder(jikkyou_wbgt_24, yohou_wbgt_24)

        with open('./tests/sample/jikkyou_1.csv') as jikkyou_csv_1:
            jikkyou_wbgt_1 = parse_jikkyou(jikkyou_csv_1.read())
        with open('./tests/sample/yohou_1.csv') as yohou_csv_1:
            yohou_wbgt_1 = parse_yohou(yohou_csv_1.read())
        self.mbuilder1 = MessageBuilder(jikkyou_wbgt_1, yohou_wbgt_1)

    def test_get_message_builder(self):
        """
        not implemented tests using User model
        """
        pass

    def test_build_message_today(self):
        actual = self.mbuilder.build_message_today()
        self.assertEqual("""\
4月28日(日)の暑さ指数
観測地点: 熊谷(43056)

○現在の状況
13時現在 14.9℃(ほぼ安全)
熱中症の危険は小さいですが、運動の合間などに適宜水分・塩分の補給をしましょう。

○今後の予測
15時の予測: 14℃(ほぼ安全)
18時の予測: 10℃(ほぼ安全)
21時の予測: 10℃(ほぼ安全)
24時の予測: 11℃(ほぼ安全)

※暑さ指数の単位は℃ですが、気温とは異なります。詳しくは環境省熱中症予防情報サイトへ(http://www.wbgt.env.go.jp/)""", actual)

    def test_build_message_1_day_later(self):
        actual = self.mbuilder.build_message_later_date(1)
        self.assertEqual("""\
4月29日(月)の暑さ指数の予測
観測地点: 熊谷(43056)

3時: 11℃(ほぼ安全)
6時: 12℃(ほぼ安全)
9時: 15℃(ほぼ安全)
12時: 17℃(ほぼ安全)
15時: 15℃(ほぼ安全)
18時: 13℃(ほぼ安全)
21時: 14℃(ほぼ安全)
24時: 15℃(ほぼ安全)

※暑さ指数の単位は℃ですが、気温とは異なります。詳しくは環境省熱中症予防情報サイトへ(http://www.wbgt.env.go.jp/)""", actual)

    def test_build_message_2_days_later(self):
        actual = self.mbuilder.build_message_later_date(2)
        self.assertEqual("""\
4月30日(火)の暑さ指数の予測
観測地点: 熊谷(43056)

3時: 14℃(ほぼ安全)
6時: 15℃(ほぼ安全)
9時: 16℃(ほぼ安全)
12時: 17℃(ほぼ安全)
15時: 17℃(ほぼ安全)
18時: 17℃(ほぼ安全)
21時: 16℃(ほぼ安全)
24時: 17℃(ほぼ安全)

※暑さ指数の単位は℃ですが、気温とは異なります。詳しくは環境省熱中症予防情報サイトへ(http://www.wbgt.env.go.jp/)""", actual)

    def test_build_message_today_24(self):
        actual = self.mbuilder24.build_message_today()
        self.assertEqual("""\
4月29日(月)の暑さ指数
観測地点: 横浜(46106)

○現在の状況
24時現在 13.5℃(ほぼ安全)
熱中症の危険は小さいですが、運動の合間などに適宜水分・塩分の補給をしましょう。

○今後の予測
本日分の予測情報はありません

※暑さ指数の単位は℃ですが、気温とは異なります。詳しくは環境省熱中症予防情報サイトへ(http://www.wbgt.env.go.jp/)""", actual)

    def test_build_message_1_day_later_24(self):
        actual = self.mbuilder24.build_message_later_date(1)
        self.assertEqual("""\
4月30日(火)の暑さ指数の予測
観測地点: 横浜(46106)

3時: 13℃(ほぼ安全)
6時: 13℃(ほぼ安全)
9時: 14℃(ほぼ安全)
12時: 15℃(ほぼ安全)
15時: 14℃(ほぼ安全)
18時: 13℃(ほぼ安全)
21時: 14℃(ほぼ安全)
24時: 13℃(ほぼ安全)

※暑さ指数の単位は℃ですが、気温とは異なります。詳しくは環境省熱中症予防情報サイトへ(http://www.wbgt.env.go.jp/)""", actual)

    def test_build_message_2_days_later_24(self):
        actual = self.mbuilder24.build_message_later_date(2)
        self.assertEqual("""\
5月1日(水)の暑さ指数の予測
観測地点: 横浜(46106)

3時: 14℃(ほぼ安全)
6時: 15℃(ほぼ安全)
9時: 20℃(ほぼ安全)
12時: 19℃(ほぼ安全)
15時: 16℃(ほぼ安全)
18時: 17℃(ほぼ安全)
21時: 17℃(ほぼ安全)
24時: 16℃(ほぼ安全)

※暑さ指数の単位は℃ですが、気温とは異なります。詳しくは環境省熱中症予防情報サイトへ(http://www.wbgt.env.go.jp/)""", actual)

    def test_build_message_today_1(self):
        actual = self.mbuilder1.build_message_today()
        self.assertEqual("""\
4月30日(火)の暑さ指数
観測地点: 横浜(46106)

○現在の状況
1時現在 13.6℃(ほぼ安全)
熱中症の危険は小さいですが、運動の合間などに適宜水分・塩分の補給をしましょう。

○今後の予測
3時の予測: 13℃(ほぼ安全)
6時の予測: 13℃(ほぼ安全)
9時の予測: 14℃(ほぼ安全)
12時の予測: 15℃(ほぼ安全)
15時の予測: 14℃(ほぼ安全)
18時の予測: 13℃(ほぼ安全)
21時の予測: 14℃(ほぼ安全)
24時の予測: 13℃(ほぼ安全)

※暑さ指数の単位は℃ですが、気温とは異なります。詳しくは環境省熱中症予防情報サイトへ(http://www.wbgt.env.go.jp/)""", actual)

    def test_build_message_1_day_later_1(self):
        actual = self.mbuilder1.build_message_later_date(1)
        self.assertEqual("""\
5月1日(水)の暑さ指数の予測
観測地点: 横浜(46106)

3時: 14℃(ほぼ安全)
6時: 15℃(ほぼ安全)
9時: 20℃(ほぼ安全)
12時: 19℃(ほぼ安全)
15時: 16℃(ほぼ安全)
18時: 17℃(ほぼ安全)
21時: 17℃(ほぼ安全)
24時: 16℃(ほぼ安全)

※暑さ指数の単位は℃ですが、気温とは異なります。詳しくは環境省熱中症予防情報サイトへ(http://www.wbgt.env.go.jp/)""", actual)

    def test_build_message_2_days_later_1(self):
        actual = self.mbuilder1.build_message_later_date(2)
        self.assertEqual("""\
5月2日(木)の暑さ指数の予測
観測地点: 横浜(46106)

予測情報はまだありません

※暑さ指数の単位は℃ですが、気温とは異なります。詳しくは環境省熱中症予防情報サイトへ(http://www.wbgt.env.go.jp/)""", actual)

    def test_get_warning_message(self):
        wbgt = WBGT("46106", "2019042815", 31.0)
        self.assertEqual("""\
【注意】熱中症の危険性がとても高くなっています
観測地点: 横浜(46106)

15時現在の暑さ指数 31.0℃(危険)

※暑さ指数の単位は℃ですが、気温とは異なります。詳しくは環境省熱中症予防情報サイトへ(http://www.wbgt.env.go.jp/)""", MessageBuilder.get_warning_message(wbgt))
