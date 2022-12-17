from collections import namedtuple

with open('olympics.txt', 'rt', encoding='utf-8') as file:
    olympics = file.read()

medal = namedtuple('medal', ['City', 'Edition', 'Sport', 'Discipline', 'Athlete', 'NOC', 'Gender',
                             'Event', 'Event_gender', 'Medal'])

# Complete this - medals is a list of medal namedtuples
medals = [medal(*line.split(';')) for line in olympics.splitlines()]


def get_medals(**kwargs):
    '''Return a list of medal namedtuples '''
    ret = []
    for med in medals:
        match = True
        for k, v in kwargs.items():
            match = match & (med.__getattribute__(k) == v)
        if match:
            ret.append(med)
    return ret
