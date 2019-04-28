import requests
import tempfile
import hsbot.parser as parser


def get_yohou(code):
    url = f"http://www.wbgt.env.go.jp/prev15WG/dl/yohou_{code}.csv"
    res = requests.get(url)
    res.raise_for_status()
    with tempfile.TemporaryFile(mode='w+') as tmp:
        tmp.write(res.text)
        tmp.seek(0)
        wbgt_list = parser.parse_yohou(tmp)

    return wbgt_list


def get_jikkyou(code, ym):
    url = f"http://www.wbgt.env.go.jp/est15WG/dl/wbgt_{code}_{ym}.csv"
    res = requests.get(url)
    if res.status_code != 200:
        ym = str(int(ym) - 1)
        url = f"http://www.wbgt.env.go.jp/est15WG/dl/wbgt_{code}_{ym}.csv"
        res = requests.get(url)
        res.raise_for_status()

    with tempfile.TemporaryFile(mode='w+') as tmp:
        tmp.write(res.text)
        tmp.seek(0)
        wbgt = parser.parse_jikkyou(tmp)

    return wbgt
