

import xml.etree.ElementTree as ET


tree = ET.parse('cleaned_flights.xml')
root = tree.getroot()

locationDict = {}

for flight in root.findall('flight'):
     loc = flight.find('location').text
     currentList = locationDict.get(loc, list())
     currentList.append(
         {
             'time': flight.find('time').text,
             'points': flight.find('points').text,
             'length': flight.find('length').text
         })
     locationDict[loc] = currentList

print(locationDict)
