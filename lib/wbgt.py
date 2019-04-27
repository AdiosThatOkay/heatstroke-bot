class WBGT:
    def __init__(self, date, wbgt):
        self.date = date
        self.wbgt = wbgt

    def guideline(self):
        if self.wbgt < 21:
            return "ほぼ安全"
        elif 21 <= self.wbgt < 25:
            return "注意"
        elif 25 <= self.wbgt < 28:
            return "警戒"
        elif 28 <= self.wbgt < 31:
            return "厳重警戒"
        else:
            return "危険"

    def message(self):
        if self.wbgt < 25:
            msg = ("熱中症の危険は小さいですが、"
                   "運動の合間などに適宜水分・塩分の補給をしましょう。")
        elif 25 <= self.wbgt < 28:
            msg = ("熱中症の危険があります。"
                   "運動の際には定期的に十分な休息を取りましょう。")
        elif 28 <= self.wbgt < 31:
            msg = ("熱中症の危険性が高いです。"
                   "外出時は炎天下を避け、"
                   "室内ではエアコンなどをつけて室温を下げましょう。")
        else:
            msg = ("熱中症の危険性がかなり高いです。"
                   "外出はなるべく避け、涼しい室内に移動しましょう。\n"
                   "特別な場合以外は、運動を中止しましょう。"
                   "特に子どもの場合は中止すべきです。")
        return msg
