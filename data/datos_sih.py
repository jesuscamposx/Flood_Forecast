from zeep import Client
from requests import Session
from zeep.transports import Transport
import xmltodict
import json
from datetime import timedelta, date


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


o = open("C:/Users/ANGLOBAL/python-workspace/Flood_Forecast/data/SJADF.txt", "w+")
o.write("ESTACION  : SJADF\n")
o.write("NOMBRE    : San Juan de Aragón, Cd. de Méx.\n")
o.write("ESTADO    : DISTRITO FEDERAL\n")
o.write("MUNICIPIO : GUSTAVO A. MADERO\n")
o.write("SITUACION : OPERANDO\n")
o.write("ORGANISMO : CONAGUA-SIH\n")
o.write("LATITUD   : 19.466667\n")
o.write("LONGITUD  : -99.066667\n\n")
o.write("           PRECIP   TMAX   TMIN\n")
o.write("FECHA      (MM)     (°C)  (°C)\n")

wsdl = "https://correo1.conagua.gob.mx/google/Google.asmx?wsdl"
session = Session()
session.verify = False
transport = Transport(session=session)

client = Client(wsdl, transport=transport)
start_date = date(2017, 1, 2)
end_date = date(2020, 7, 2)
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

    fecha = (single_date + timedelta(days=-1)).strftime("%Y/%m/%d")
    print(fecha)
    o.write(fecha + "," + precip + "," + tmin + "," + tmax + "\n")

o.close()
