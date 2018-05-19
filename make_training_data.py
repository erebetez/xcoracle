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
    for day, data in weater_features.items():
        label = location_to_index(location_label.get(day,''))
        row = list()
        for feature in data.values():
            row = row + feature

        row.append(label)
        #print(len(row))
        training_writer.writerow(row)
