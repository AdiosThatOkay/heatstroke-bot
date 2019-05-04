from hsbot import db
from hsbot.models.observatories import Observatory
import sys


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

def get_observatory_name(observatory_code):
    observatory = db.session.query(Observatory).filter(
            Observatory.code == observatory_code).first()
    return observatory.name
