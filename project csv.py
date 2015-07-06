from csv import DictReader
from math import radians, cos, sin, asin, sqrt
from dominate import document
from dominate.tags import *
from collections import defaultdict

import os

try:
    os.mkdir('Countries')
except OSError:
    pass
try:
    os.mkdir('Continents')
except OSError:
    pass


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def continentLongName(con):
    continents = {'AS': 'Asia', 'AF': 'Africa', 'AN': 'Antarctica', 'EU': 'Europe', 'NA': 'North America',
                  'OC': 'Oceania', 'SA': 'South and Central America'}
    return continents[con]


doctype = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd>"
s = '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="he">'
continents = defaultdict(list)
ISRAEL_LON, ISRAEL_LAT = 34.75, 31.5
countries = {}
l = []
l2 = defaultdict(list)
# l10=defaultdict(list)
with open('countries.csv') as f:
    reader = DictReader(f)
    for d in reader:
        countries[d['name']] = d
        l.append([d['name'], [float(d['lon']), float(d['lat']), int(d['population'])]])

for i, v in l:
    l2[i].append(haversine(ISRAEL_LON, ISRAEL_LAT, v[0], v[1]))
    l2[i].append(v[2])
    l10 = sorted(l2.items(), key=lambda x: x[1][1], reverse=True)

    with document(title='index', doctype=doctype) as doc:
        ul(a(li('{}: {:,.0f}'.format(i, v[0])), href='Countries/{}.html'.format(i)) for i, v in l10)

    with open('{}.html'.format('index'), 'w') as f:
        f.write(doc.render())


def closest_coutries(v):
    l_coutries = [(i, (haversine(float(c[0]), float(c[1]), float(v['lon']), float(v['lat'])))) for i, c in l]
    return sorted(l_coutries, key=lambda x: x[1])[1:16]


for k, v in countries.items():
    closest_coutries15 = closest_coutries(v)

    continents[v['continent']].append(v['name'])
    with document(title='{}'.format(k), doctype=doctype) as doc:
        h1(k)
        dl('\n', dt('capital'), dd(v['capital']), '\n', dt('population'),
           dd('{:,d}'.format(int(v['population']))), '\n'
           , dt('Land Area'), dd('{:,d}'.format(int(v['land']) if v['land'].isdigit() else 0)), '\n'
           , dt('Continent'), dd(v['continent']), '\n')
        h2('closest coutries')
        ul(a(li(i), href='{}.html'.format(i)) for i, _ in closest_coutries15)

        a(v['continent'], href='../Continents/{}.html'.format(v['continent']))
        a('index', href='../index.html')

    with open('Countries/{}.html'.format(v['name']), 'w') as f:
        f.write(doc.render())

for k, v in continents.items():
    with document(title='{}'.format(k), doctype=doctype) as doc:
        h1(k)
        ul(a(li(i), href='../Countries/{}.html'.format(i)) for i in v)

    with open('Continents/{}.html'.format(k), 'w') as f:
        f.write(doc.render())
