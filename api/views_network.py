from api.models import Sensor, Medicion
from api.serializers import SensorSerializer, MedicionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework import status
from datetime import datetime, date
import logging


def is_valid_date(string):
        try: 
            datetime.strptime('%Y-%m-%d')
            return True

        except ValueError:
            return False
        

class SensorView(APIView):
    def get(self, request, format=None):
        sensors = Sensor.objects.all()
        serializer = SensorSerializer(sensors, many=True)
        return Response(serializer.data)

class MedicionView(APIView):
    def get(self, request, format=None):
        sensor_id = self.request.query_params.get('sensor', None)
        if sensor_id is None:
            return Response({"id": 40001, "text": "Sensor Id es necesario."},
                            status=status.HTTP_400_BAD_REQUEST)
        fecha = self.request.query_params.get('fecha', None)
        if fecha is None:
            fecha = date.today().strftime('%Y-%m-%d')
        else:
            if not is_valid_date(fecha):
                return Response({"id": 40002, "text": "Formato incorrecto de fecha."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            meds = Medicion.objects.raw("SELECT * FROM medicion WHERE creado >= " + fecha)
            serializer = MedicionSerializer(meds, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({"id": 40401, "text": "No se encontraron registros"},
                            status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request, format=None):
        serializer = SensorSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
