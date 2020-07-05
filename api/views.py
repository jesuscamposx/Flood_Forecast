from api.models import Condicion
from api.serializers import CondicionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework import status
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


class CondicionView(APIView):
    def get(self, request, format=None):
        #condiciones = Condicion.objects.all()  # noqa
        #response = CondicionSerializer(condiciones, many=True)
        f = open('C:/Users/ANGLOBAL/python-workspace/Flood_Forecast/data/9043.txt', 'r')
        txt = f.read()
        txt = txt.split('\n')
        txt = txt[19:-2]

        datos = []

        for row in txt:
            datos.append(row.split(','))

        condiciones = []
        logger.info('Getting data...')
        for row in datos:
            condicion = {
                "fecha": datetime.strftime(datetime.strptime(row[0], '%d/%m/%Y'), '%Y-%m-%d'),
                "id_alcaldia": 101,
                "precipitacion": None if row[1] == 'Nulo' else row[1],
                "temp_min": None if row[3] == 'Nulo' else row[3],
                "temp_max": None if row[4] == 'Nulo' else row[4]
                }
            condiciones.append(condicion)
        serializer = CondicionSerializer(data=condiciones, many=True)
        try:
            logger.info("Validating data...")
            serializer.is_valid(raise_exception=True)
            logger.info("Saving data...")
            serializer.save()
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("OK", status=status.HTTP_200_OK)
