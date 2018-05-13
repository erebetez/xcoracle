import xml.etree.ElementTree as ET
import re


tree = ET.parse('cleaned_flights.xml')
root = tree.getroot()

number = re.compile("[0-9]+(\.[0-9])?")
result = number.match("my123.232 test")
print(result)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

locationDict = {}

for flight in root.findall('flight'):
     loc = flight.find('location').text
     currentList = locationDict.get(loc, list())
     points = [float(s) for s in flight.find('points').text.split() if is_number(s)]
     print(points)
     currentList.append(
         {
             #'count': (len(currentList) + 1),
             'time': flight.find('time').text,
             'points': points[0],
             'length': flight.find('length').text
         })
     locationDict[loc] = currentList

print(locationDict)

locationRankingList = []

for location, flightList in locationDict.items():
    count = len(flightList)
    pointList = map(lambda d: d.get('points'), flightList)
    average = sum(pointList) / count
    locationRankingList.append(
          {
            'location': location,
            'count': count,
        #   'max': max(pointList),
            'average': average
          }
        )


locationRankingList = sorted(locationRankingList, key=lambda loc: loc.get('average'), reverse=True)

print(locationRankingList)
