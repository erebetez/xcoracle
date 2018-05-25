import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join, splitext

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
    min_flights = 5
    min_points = 50

    filtered = [loc for loc in locationRankingList if (loc['count'] >= min_flights and
                                                       loc['average'] >= min_points)]
    if not filtered:
        return 'None'
    else:
        return filtered.pop()['location']


def best_locaction_per_day(day_file):
    locationRankingList = parse_flights(data_folder + day_file)

    best_loc = get_best_location(locationRankingList)

    lu_location[best_loc] = 0 # make uniqe location

    return best_loc

def get_location_label_dict():

    label_dict = {}

    for filename, file_extension in [splitext(f) for f in listdir(data_folder) if isfile(join(data_folder, f))]:
        label_dict[filename] = best_locaction_per_day(filename + file_extension)

    return label_dict

def get_location_index():
    return list(enumerate(get_location_list()))

def get_location_list():
   return list(lu_location.keys())
