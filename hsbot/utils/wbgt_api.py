import requests
import hsbot.utils.parser as parser


def get_yohou(code):
    url = f"http://www.wbgt.env.go.jp/prev15WG/dl/yohou_{code}.csv"
    res = requests.get(url)
    res.raise_for_status()
    wbgt_list = parser.parse_yohou(res.text)
    return wbgt_list


def get_jikkyou(code, ym):
    url = f"http://www.wbgt.env.go.jp/est15WG/dl/wbgt_{code}_{ym}.csv"
    res = requests.get(url)
    if res.status_code != 200:
        ym = str(int(ym) - 1)
        url = f"http://www.wbgt.env.go.jp/est15WG/dl/wbgt_{code}_{ym}.csv"
        res = requests.get(url)
        res.raise_for_status()
    wbgt = parser.parse_jikkyou(res.text)
    return wbgt
