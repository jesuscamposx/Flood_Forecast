from api.models import Condicion
from api.serializers import CondicionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework import status
from datetime import datetime
from django.db import connection
import logging
import csv


logger = logging.getLogger(__name__)


class CargaCondicionView(APIView):
    def get(self, request, format=None):
        f = open('./data/9043.txt', 'r')
        txt = f.read()
        txt = txt.split('\n')
        txt = txt[19:-2]

        f_s = open('./data/SJADF.txt', 'r')
        txt_s = f_s.read()
        txt_s = txt_s.split('\n')
        txt_s = txt_s[376:-1]

        datos = []
        datos_s = []
        for row in txt:
            datos.append(row.split(','))
        for row in txt_s:
            datos_s.append(row.split(','))
        f.close()
        f_s.close()

        condiciones = []
        logger.info('Getting data...')
        for row in datos:
            condicion = {
                "fecha": datetime.strftime(datetime.strptime(row[0], '%d/%m/%Y'), '%Y-%m-%d'),
                "id_alcaldia": 101,
                "precipitacion": None if row[1] == 'Nulo' else row[1],
                "temp_min": None if row[4] == 'Nulo' else row[4],
                "temp_max": None if row[3] == 'Nulo' else row[3],
                "inundacion": 0
                }
            condiciones.append(condicion)
        for row in datos_s:
            condicion = {
                "fecha": datetime.strftime(datetime.strptime(row[0], '%Y/%m/%d'), '%Y-%m-%d'),
                "id_alcaldia": 101,
                "precipitacion": None if row[1] == 'None' else row[1],
                "temp_min": None if row[2] == 'None' else row[2],
                "temp_max": None if row[3] == 'None' else row[3],
                "inundacion": 0
                }
            condiciones.append(condicion)
        serializer = CondicionSerializer(data=condiciones, many=True)
        try:
            logger.info("Validating data...")
            serializer.is_valid(raise_exception=True)
            logger.info("Saving data...")
            serializer.save()
        except ValidationError as ve:
            logger.error(str(ve))
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("OK", status=status.HTTP_200_OK)


class CargaInundacionView(APIView):
    def get(self, request, format=None):
        f = open("./data/files/metricas.csv", 'r')
        r = csv.reader(f)
        data = []
        for row in r:
            data.append(row)
        data = data[3:-1]
        f.close()
        
        c_p = 0
        c_f = 0
        i = 0
        for d in data:
            cdmx = int(d[2])
            inundacion = int(d[3])
            lluvia = int(d[4])
            gam = int(d[5])
            fecha = d[0]
            if cdmx > 0 and inundacion > 0 and lluvia > 0 and gam > 0:
                c_p += 1
                try:
                    condicion = Condicion.objects.get(fecha=fecha, id_alcaldia=101)
                    if condicion.precipitacion >= 2:
                        c_f += 1
                        inundacion = 1
                    else:
                        inundacion = 0
                        logger.info("Fecha: " + fecha + " Conteo: " + str(d[1]) + " Precipitacion: " + str(condicion.precipitacion))  # noqa
                    serializer = CondicionSerializer(condicion, data={
                        "fecha": fecha,
                        "id_alcaldia": 101,
                        "inundacion": inundacion
                    })
                    if serializer.is_valid():
                        serializer.save()
                        i += 1
                    else:
                        logger.info(serializer.errors)
                except Exception:
                    logger.info("Not Found: " + str(fecha))
        logger.info("Registros de inundacion en la GAM procado por lluvia: " + str(c_p))
        logger.info("Registros de inundacion en 0la GAM procado por lluvia " + 
                    " y la precipitacion en los registros es mayor a cero: " + str(c_f))
        logger.info("Registros actualizados: " + str(i))
        return Response("OK", status=status.HTTP_200_OK)