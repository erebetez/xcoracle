import csv

daily_wather = list()

with open('weather/biel_2018-05-17T21_47_38.csv') as csvfile: #, newline=''
     weather = csv.reader(csvfile, delimiter=';')
     for row in weather:
         if row and row[3] == '12': ## NOTE only get data at 12 o'clock.
           daily_wather.append(
               {
                   row[0] + '-' + row[1] + '-' + row[2]: row[5:-1]
               })
           #print(', '.join(row)) 

print(daily_wather)
