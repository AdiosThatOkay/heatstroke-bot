class MessageBuilder:
    MSG_FOOTER = """
※暑さ指数の単位は℃ですが、気温とは異なります。詳しくは環境省熱中症予防情報サイトへ(http://www.wbgt.env.go.jp/)"""

    def __init__(self, now_wbgt, yohou_wbgt):
        self.now_wbgt = now_wbgt
        self.yohou_wbgt = yohou_wbgt

    def build_message_today(self):
        msg = f"""\
{self.now_wbgt.get_short_month()}月{self.now_wbgt.get_short_day()}日{self.now_wbgt.get_weekday()}の暑さ指数

○現在の状況
{self.now_wbgt.get_short_hour()}時現在 {self.now_wbgt.degree}℃({self.now_wbgt.risk()})
{self.now_wbgt.message()}

○今後の予測
"""
        yosoku_list = [w for w in self.yohou_wbgt
                       if w.is_same_day(self.now_wbgt)
                       and w.later_than(self.now_wbgt)]
        if len(yosoku_list) == 0:
            msg += "本日分の予測情報はありません\n"
        else:
            for w in yosoku_list:
                msg += f"{w.get_short_hour()}時の予測: {int(w.degree)}℃({w.risk()})\n"

        msg += self.MSG_FOOTER

        return msg

    def build_message_later_date(self, n):
        later_wbgt = self.now_wbgt.get_n_days_later(n)
        msg = f"""\
{later_wbgt.get_short_month()}月{later_wbgt.get_short_day()}日{later_wbgt.get_weekday()}の暑さ指数の予測

"""
        yosoku_list = [w for w in self.yohou_wbgt
                       if w.later_than(later_wbgt)
                       and w.is_same_day(later_wbgt)]
        if len(yosoku_list) == 0:
            msg += "予測情報はまだありません\n"
        else:
            for w in yosoku_list:
                msg += f"{w.get_short_hour()}時: {int(w.degree)}℃({w.risk()})\n"

        msg += self.MSG_FOOTER

        return msg
