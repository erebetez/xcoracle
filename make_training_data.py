import csv
import parsing_flights as pf
import parsing_weather as pw


weater_features = pw.get_weater_features()

location_label = pf.get_location_label_dict()

with open('training/train.csv', 'w') as train_csvfile, \
     open('training/test.csv', 'w') as test_csvfile:


    train_writer = csv.writer(train_csvfile, delimiter=',')
    test_writer = csv.writer(test_csvfile, delimiter=',')

    header = weater_features.pop('header')
    header.append('Location')

    #print(len(header))
    #print(weater_features.keys())

    train_writer.writerow(header)
    test_writer.writerow(header)

    count = 0

    for day, data in weater_features.items():
        label = location_label.get(day,False)
        if label:
            row = list()
            for feature in data.values():
                row = row + feature

            row.append(label)
            #print(len(row))
            if (count % 10) == 0: ## TODO decrese number as data pool gets bigger
                test_writer.writerow(row)
            else:
                train_writer.writerow(row)

            count += 1

