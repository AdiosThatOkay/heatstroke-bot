from hsbot import db
from hsbot.models.observatories import Observatory
import sys
import urllib.parse


def get_nearest_observatory(lat10, lon10):
    query_results = db.session.query(Observatory).all()
    nearest = None
    min_distance = sys.float_info.max
    for result in query_results:
        distance = get_distance(lat10, lon10,
                                result.lat60tolat10(), result.lon60tolon10())
        if min_distance > distance:
            nearest = result
            min_distance = distance

    if nearest is None:
        raise Exception("Can't get nearest observatory")

    return nearest


def get_distance(lat1, lon1, lat2, lon2):
    return ((abs(lat1 - lat2))**2 + (abs(lon1 - lon2))**2)**0.5


def postback_data_to_dict(data):
    parsed = urllib.parse.parse_qs(data)
    ret = {}
    ret['change'] = bool(int(parsed['change'][0]))
    if ret['change']:
        ret['code'] = str(parsed['code'][0])
    return ret
