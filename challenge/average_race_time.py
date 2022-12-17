# Source of data: https://www.arrs.run/
# This dataset has race times for women 10k runners from the Association of Road Racing Statisticians

import re
import datetime


def get_data():
    """Return content from the 10k_racetimes.txt file"""
    with open('10k_racetimes.txt', 'rt') as file:
        content = file.read()
    return content


runner_name_pat = re.compile(r'(\w+\s?)*\w+')
# Handle milliseconds properly in time_str2timedelta()
time_pat = re.compile(
    r'(?P<minutes>\d{2}):(?P<seconds>\d{2})\.?(?P<milliseconds>\d*)?')


def time_str2timedelta(time_str):
    time_dict = time_pat.match(time_str).groupdict()
    if time_dict['milliseconds'] == '':
        time_dict['milliseconds'] = '0'
    else:
        time_dict['milliseconds'] = '{:0<3}'.format(time_dict['milliseconds'])
    return datetime.timedelta(**{k: int(v) for k, v in time_dict.items()})


def line2dict(line: str) -> dict:
    ret = dict(time=line[3:14].rstrip(),
               athlete=runner_name_pat.match(line[14:56].rstrip()).group(),
               race_date=line[56:67], dob=line[73:84], location=line[87:])
    ret['timedelta'] = time_str2timedelta(ret['time'])
    return ret


def contents2records(content: str,) -> dict:
    res = dict()
    for line in content.splitlines()[1:]:
        try:
            race_dict = line2dict(line)
        except AttributeError:  # no match
            print(line)
        try:
            res[race_dict['athlete']].append(race_dict)
        except KeyError:
            res[race_dict['athlete']] = [race_dict]
    return res


def mean_time(athlete, records):
    tds = [rec['timedelta'] for rec in records[athlete]]
    td_sum = datetime.timedelta(seconds=0)
    for td in tds:
        td_sum += td
    return str(td_sum / len(tds))


def get_rhines_times():
    """Return a list of Jennifer Rhines' race times"""
    races = contents2records(get_data())
    return [rec['time'] for rec in races['Jennifer Rhines']]


def get_average():
    """Return Jennifer Rhines' average race time in the format:
       mm:ss:M where :
       m corresponds to a minutes digit
       s corresponds to a seconds digit
       M corresponds to a milliseconds digit (no rounding, just the single digit)"""
    racetimes = get_rhines_times()
    tds = [time_str2timedelta(time_str) for time_str in racetimes]
    td_sum = datetime.timedelta(seconds=0)
    for td in tds:
        td_sum += td
    return str(td_sum / len(tds))[2:9]
