from hsbot.utils.wbgt import WBGT


def parse_yohou(yohou_csv_data):
    dates, degrees = yohou_csv_data.rstrip().split('\n')
    dates = dates.split(',')
    degrees = degrees.split(',')

    del(dates[0:2])
    del(degrees[0:2])
    degrees = [int(x)/10.0 for x in degrees]

    wbgt_list = []
    for date, degree in zip(dates, degrees):
        w = WBGT(date, degree)
        wbgt_list.append(w)

    return wbgt_list


def parse_jikkyou(jikkyou_csv_data):
    enum = enumerate(jikkyou_csv_data.rstrip().split('\n'))
    recent = None
    for i, line in enum:
        row = line.split(',')
        if i == 0:
            continue
        if row[2] == '':
            break
        recent = row
    if recent is None or recent[2] == '':
        raise Exception('Unexpected jikkyou_data')
    else:
        year, month, day = recent[0].split('/')
        hour = recent[1].split(':')[0]
        month = month.zfill(2)
        day = day.zfill(2)
        hour = hour.zfill(2)

        return WBGT(year + month + day + hour, float(recent[2]))
