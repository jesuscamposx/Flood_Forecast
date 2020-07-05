from serializers import CondicionSerializer  # noqa


f = open('C:/Users/ANGLOBAL/python-workspace/Flood_Forecast/data/9043.txt', 'r')
txt = f.read()
txt = txt.split('\n')
txt = txt[19:-1]

c = 1
datos = []
for row in txt:
    if c == 20:
        break
    datos.append(row.split(','))
    c += 1

for row in datos:
    condicion = {
        "fecha": row[0],
        "id_alcaldia": 1,
        "precipitacion": row[1],
        "temp_min": row[3],
        "temp_max": row[4]
        }
    print(condicion)
#serializer = CondicionSerializer({ fecha = datos[0,1]})
