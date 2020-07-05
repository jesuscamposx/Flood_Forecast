from zeep import Client
from requests import Session
from zeep.transports import Transport
import xmltodict
import json
from datetime import timedelta, date


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


o = open("C:/Users/ANGLOBAL/python-workspace/Flood_Forecast/data/datos.txt", "w+")
o.write("[Fecha] [Precipitacion] [Tmin] [Tmax]\n")

wsdl = "https://correo1.conagua.gob.mx/google/Google.asmx?wsdl"
session = Session()
session.verify = False
transport = Transport(session=session)

client = Client(wsdl, transport=transport)
start_date = date(2017, 1, 1)
end_date = date(2017, 1, 30)
dr = daterange(start_date, end_date)

for single_date in dr:
    dt = single_date.strftime("%Y/%m/%d")
    tmin = ""
    tmax = ""
    precip = ""

    print(dt)
    res_temp = client.service.TemperaturaDiariaGrupo(dteFecha=dt)
    temperaturas = xmltodict.parse(res_temp)["TemperaturaDiaria"]["GrupoEstacion"]
    res_precip = client.service.PrecipitacionDiariaGrupo(dteFecha=dt)
    precipitaciones = json.loads(res_precip)

    for temperatura in temperaturas:
        if temperatura["Estacion"] == "SJADF":
            tmin = temperatura["tmin"]
            tmax = temperatura["tmax"]

    for precipitacion in precipitaciones:
        if precipitacion["Estacion"] == "SJADF":
            precip = precipitacion["Prec"]

    o.write(dt + "," + precip + "," + tmin + "," + tmax + "\n")

o.close()
