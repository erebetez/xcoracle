from datetime import date, timedelta
import parsing_flights as pf

data_folder = 'flights/data/'



def best_locaction_per_day(day):
    locationRankingList = pf.parseFlights(data_folder + day + '.xml')

    #print(locationRankingList)

    best_loc = pf.getBestLocation(locationRankingList)

    return best_loc

#print(best_locaction_per_day('2018-05-06'))

## TODO just read files in folder...

def get_label_list():
    d1 = date(2018, 5, 3)  # start date
    d2 = date(2018, 5, 16)  # end date

    delta = d2 - d1         # timedelta

    label_list = list()

    for i in range(delta.days + 1):
        _date = d1 + timedelta(days=i)
        label_list.append({_date.isoformat(): best_locaction_per_day(_date.isoformat())})
    return label_list

print(get_label_list())
