import parsing_flights as pf
import parsing_weather as pw
import json

wf = pw.get_weater_features()
#print(wf.keys())

row = list()
header = wf['header']



for feature in wf['2018-06-01'].values():
    row = row + feature

test_data = dict(zip(header,[[r] for r in row])) #

with open('training/data.json', 'w') as f:
  json.dump(test_data, f, ensure_ascii=False)

print(pf.get_location_label_dict())

print(pf.get_location_index())

loc_list = pf.get_location_list()

with open('training/labels.json', 'w') as f:
  json.dump(loc_list, f, ensure_ascii=False)
