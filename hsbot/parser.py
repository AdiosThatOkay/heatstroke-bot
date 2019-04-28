import csv
from hsbot.wbgt import WBGT


def parse_yohou(yohou_csv_stream):
    dates = yohou_csv_stream.readline().strip().split(',')
    degrees = yohou_csv_stream.readline().strip().split(',')

    del(dates[0:2])
    del(degrees[0:2])
    degrees = [int(x)/10.0 for x in degrees]

    wbgt_list = []
    for date, degree in zip(dates, degrees):
        w = WBGT(date, degree)
        wbgt_list.append(w)

    return wbgt_list


def parse_jikkyou(jikkyou_csv_stream):
    reader = csv.reader(jikkyou_csv_stream)
    recent = None
    for row in reader:
        if reader.line_num == 1:
            continue
        if row[2] == '':
            break
        recent = row
    if recent is None or recent[2] == '':
        return None
    else:
        year, month, day = recent[0].split('/')
        hour = recent[1].split(':')[0]
        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day
        if len(hour) == 1:
            hour = "0" + hour

        return WBGT(year + month + day + hour, float(recent[2]))
