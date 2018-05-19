import xml.etree.ElementTree as ET

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def parseFlights(fileName):
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

def getBestLocation(locationRankingList):
    min_flights = 3
    min_points = 50

    filtered = [loc for loc in locationRankingList if (loc['count'] >= min_flights and
                                                       loc['average'] >= min_points)]
    if not filtered:
        return '' # for sake of consitency
    else:
        return filtered.pop()['location']
