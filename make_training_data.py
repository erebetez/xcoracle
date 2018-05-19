import csv
import parsing_flights as pf
import parsing_weather as pw


weater_features = pw.get_weater_features()

location_label = pf.get_location_label_list()

##enumerate locations

print(location_label)

with open('training/train.csv', 'w') as csvfile:
    training_writer = csv.writer(csvfile, delimiter=',')
    for day, data in weater_features.items():
        label = location_label[day]
        row = list()
        for feature in data.values():
            row = row + feature

        row.append(label)
        training_writer.writerow(row)
