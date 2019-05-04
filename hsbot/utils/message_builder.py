from hsbot import db
from hsbot.models.users import User
from hsbot.models.observatories import Observatory
from hsbot.utils.wbgt_api import (
    get_jikkyou, get_yohou
)
import datetime


class MessageBuilder:
    DEFAULT_MESSAGE = """\
・＋ボタンを押して位置情報を送ると、現在地に一番近い観測地点を登録します。再度位置情報を送るまで、観測地点は変わりません。
・毎日7時に、一日の暑さ指数(WBGT)の予測をお届けします。
・暑さ指数が31℃以上になったときにもお知らせします。
・「今」「明日」「明後日」(ひらがなでもOK)と話しかけると、その日の暑さ情報の予測をお知らせします。"""
    MSG_FOOTER = """
※暑さ指数の単位は℃ですが、気温とは異なります。詳しくは環境省熱中症予防情報サイトへ(http://www.wbgt.env.go.jp/)"""

    @classmethod
    def get_message_builder(cls, user_id,
                            ym=datetime.datetime.now().strftime('%Y%m')):
        user = db.session.query(User).filter(User.user_id == user_id).first()
        observatory_code = user.nearest_observatory
        now_wbgt = get_jikkyou(observatory_code, ym)
        yohou_wbgt = get_yohou(observatory_code)
        return MessageBuilder(now_wbgt, yohou_wbgt)

    @classmethod
    def get_default_message(cls):
        return cls.DEFAULT_MESSAGE

    def __init__(self, now_wbgt, yohou_wbgt):
        self.now_wbgt = now_wbgt
        self.yohou_wbgt = yohou_wbgt

    def build_message_today(self):
        msg = f"""\
{self.now_wbgt.get_short_month()}月{self.now_wbgt.get_short_day()}日{self.now_wbgt.get_weekday()}の暑さ指数
観測地点: {self.get_observatory_name()}({self.now_wbgt.observatory_code})

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
観測地点: {self.get_observatory_name()}({self.now_wbgt.observatory_code})

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

    def get_observatory_name(self):
        observatory = db.session.query(Observatory).filter(
                Observatory.code == self.now_wbgt.observatory_code).first()
        return observatory.name
