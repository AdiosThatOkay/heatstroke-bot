import requests

def get_yohou(code):
    url = f"http://www.wbgt.env.go.jp/prev15WG/dl/yohou_{code}.csv"
    return url

def get_jikkyou(pref, ym):
    url = f"http://www.wbgt.env.go.jp/est15WG/dl/wbgt_{pref}_{ym}.csv"
    return url
