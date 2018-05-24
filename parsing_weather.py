import csv
from os import listdir
from os.path import isfile, join

data_folder = 'weather/meteoblue/'

daily_wather_dict = {}

def parse_meteoblue_csv(file_name):
    with open(file_name) as csvfile: #, newline=''
        weather = csv.reader(csvfile, delimiter=';')
        city = ''
        headers = []
        for row in weather:
            if row and row[3] == '12': ## NOTE only get data at 12 o'clock.
                today = row[0] + '-' + row[1] + '-' + row[2]

                daily_dict = daily_wather_dict.get(today,{})
                daily_dict[city] = row[5:]
                daily_wather_dict[today] = daily_dict

            if row and row[0] == 'NAME':
                daily_wather_dict['header'] = row[5:]

            if row and row[0] == 'CITY':
                city = row[5]


def get_weater_features():
    weather_files = [f for f in listdir(data_folder) if isfile(join(data_folder, f))]

    for f in weather_files:
        parse_meteoblue_csv(data_folder + f)

    return daily_wather_dict


#for city, data in daily_wather_dict['2018-05-03'].items():
   #print(city + ': ' + ", ".join(data))
   
#for city, data in daily_wather_dict['2018-05-03'].items():
   #print("\t ".join(data))
