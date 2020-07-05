import json
f = open('C:/Users/ANGLOBAL/python-workspace/Flood_Forecast/data/EstacionesSIH.json', 'rb')
data = json.load(f)

for d in data:
    if "Cd. de" in d['Nombre']:
        print(d)
