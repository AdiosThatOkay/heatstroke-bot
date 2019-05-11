from datetime import (
    datetime, timedelta
)
from hsbot import db
from hsbot.models.observatories import Observatory


class WBGT:
    weekday = {0: '(月)', 1: '(火)', 2: '(水)', 3: '(木)',
               4: '(金)', 5: '(土)', 6: '(日)'}

    def __init__(self, observatory_code, date, degree):
        self.observatory_code = observatory_code
        self.date = date
        self.degree = degree

    def risk(self):
        if self.degree < 21:
            return "ほぼ安全"
        elif 21 <= self.degree < 25:
            return "注意"
        elif 25 <= self.degree < 28:
            return "警戒"
        elif 28 <= self.degree < 31:
            return "厳重警戒"
        else:
            return "危険"

    def message(self):
        if self.degree < 25:
            msg = ("熱中症の危険は小さいですが、"
                   "運動の合間などに適宜水分・塩分の補給をしましょう。")
        elif 25 <= self.degree < 28:
            msg = ("熱中症の危険があります。"
                   "運動の際には定期的に十分な休息を取りましょう。")
        elif 28 <= self.degree < 31:
            msg = ("熱中症の危険性が高いです。"
                   "外出時は炎天下を避け、"
                   "室内ではエアコンなどをつけて室温を下げましょう。")
        else:
            msg = ("熱中症の危険性がかなり高いです。"
                   "外出はなるべく避け、涼しい室内に移動しましょう。\n"
                   "特別な場合以外は、運動を中止しましょう。"
                   "特に子どもの場合は中止すべきです。")
        return msg

    def get_year(self):
        return self.date[0:4]

    def get_month(self):
        return self.date[4:6]

    def get_short_month(self):
        if self.get_month()[0] == "0":
            return self.get_month()[1]
        else:
            return self.get_month()

    def get_day(self):
        return self.date[6:8]

    def get_short_day(self):
        if self.get_day()[0] == "0":
            return self.get_day()[1]
        else:
            return self.get_day()

    def get_hour(self):
        return self.date[8:10]

    def get_short_hour(self):
        if self.get_hour()[0] == "0":
            return self.get_hour()[1]
        else:
            return self.get_hour()

    def get_weekday(self):
        datetime_obj = datetime.strptime(
            (self.get_year() + self.get_month() + self.get_day()), '%Y%m%d')
        weekday_num = datetime_obj.weekday()
        return self.weekday[weekday_num]

    def get_n_days_later(self, n):
        datetime_str = self.get_year() + self.get_month() + self.get_day()
        datetime_obj = datetime.strptime(datetime_str, '%Y%m%d')
        later_datetime_obj = datetime_obj + timedelta(days=n)
        return WBGT(self.observatory_code,
                    str(later_datetime_obj.year) +
                    str(later_datetime_obj.month).zfill(2) +
                    str(later_datetime_obj.day).zfill(2) + '00', self.degree)

    def later_than(self, other):
        if isinstance(other, self.__class__):
            return (self.get_year() + self.get_month() +
                    self.get_day() + self.get_hour() >
                    other.get_year() + other.get_month() +
                    other.get_day() + other.get_hour())
        else:
            return False

    def is_same_day(self, other):
        if isinstance(other, self.__class__):
            return (self.get_year() + self.get_month() +
                    self.get_day() ==
                    other.get_year() + other.get_month() +
                    other.get_day())
        else:
            return False

    def get_observatory_name(self):
        observatory = db.session.query(Observatory).filter(
                Observatory.code == self.observatory_code).first()
        return observatory.name
