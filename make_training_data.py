import csv
import parsing_flights as pf
import parsing_weather as pw


weater_features = pw.get_weater_features()

location_label = pf.get_location_label_dict()

location_index = pf.get_location_index()

def location_to_index(loc):
    for pair in location_index:
        if pair[1] == loc:
            return pair[0]

#print(location_index)

with open('training/train.csv', 'w') as csvfile:
    training_writer = csv.writer(csvfile, delimiter=',')

    header = weater_features.pop('header')
    header.append('Location')

    #print(len(header))
    #print(weater_features.keys())

    training_writer.writerow(header)

    for day, data in weater_features.items():
        label = location_label.get(day,False)
        if label:
            row = list()
            for feature in data.values():
                row = row + feature

            row.append(label)
            #print(len(row))
            training_writer.writerow(row)
