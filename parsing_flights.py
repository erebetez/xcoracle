import xml.etree.ElementTree as ET
from datetime import date, timedelta

data_folder = 'flights/data/'

lu_location = {}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def parse_flights(fileName):
    tree = ET.parse(fileName)
    root = tree.getroot()
    locationDict = {}
    locationRankingList = []

    for flight in root.findall('flight'):
        if flight.find('country').text == "Switzerland":
            loc = flight.find('location').text
            currentList = locationDict.get(loc, list())
            points = [float(s) for s in flight.find('points').text.split() if is_number(s)]
            currentList.append(
                {
                    'time': flight.find('time').text,
                    'points': points[0],
                    'length': flight.find('length').text
                })
            locationDict[loc] = currentList

    for location, flightList in locationDict.items():
        count = len(flightList)
        pointList = map(lambda d: d.get('points'), flightList)
        average = sum(pointList) / count
        #print(pointList)
        #max_point = max(pointList)
        locationRankingList.append(
            {
                'location': location,
                'count': count,
                #'max': max_point,
                'average': average,
                'flights': flightList
            }
        )

    locationRankingList = sorted(locationRankingList, key=lambda loc: loc.get('average'))

    return locationRankingList

def get_best_location(locationRankingList):
    min_flights = 3
    min_points = 50

    filtered = [loc for loc in locationRankingList if (loc['count'] >= min_flights and
                                                       loc['average'] >= min_points)]
    if not filtered:
        return ''
    else:
        return filtered.pop()['location']


def best_locaction_per_day(day):
    locationRankingList = parse_flights(data_folder + day + '.xml')

    best_loc = get_best_location(locationRankingList)

    lu_location[best_loc] = 0 # make uniqe location

    return best_loc

## TODO just read files in folder...

def get_location_label_dict():
    d1 = date(2018, 5, 3)  # start date
    d2 = date(2018, 5, 19)  # end date

    delta = d2 - d1         # timedelta

    label_dict = {}

    for i in range(delta.days + 1):
        _date = d1 + timedelta(days=i)
        label_dict[_date.isoformat()] = best_locaction_per_day(_date.isoformat())

    return label_dict

def get_location_index():
    return list(enumerate(lu_location.keys()))
