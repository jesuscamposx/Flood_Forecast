import json
f = open('./data/files/EstacionesSIH.json', 'rb')
data = json.load(f)

for d in data:
    if "Cd. de" in d['Nombre']:
        print(d)
