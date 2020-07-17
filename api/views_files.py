from api.models import Condicion, Medicion
from api.serializers import CondicionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from rest_framework.serializers import ValidationError
from rest_framework import status
from datetime import datetime
import logging
import csv


logger = logging.getLogger(__name__)


class ArchivoInundacionView(APIView):
    def get(self, request, format=None):
        years = self.request.query_params.get('years', None)
        for y in years.split("-"):
            if not y.isdigit():
                return Response("Invalid years format", status=status.HTTP_400_BAD_REQUEST)
        ub = "./files/"
        f_name = "Fflood_Registros_Inundacion" + years.replace('-', '_') + ".csv"
        with open(ub + f_name, 'w+', newline='') as f:
            w = csv.writer(f)
            w.writerow(["Fecha", "Alcaldía", "Precipitación", "Temperatura Mínima",
                       "Temperatura Máxima", "Inundación",
                       "Creación", "Actualización"])
            q = "SELECT * FROM condicion WHERE YEAR(fecha) in (" + years.replace("-", ", ") + ")"
            print(q)
            for c in Condicion.objects.raw(q):
                w.writerow([c.fecha, c.id_alcaldia, c.precipitacion,
                            c.temp_min, c.temp_max, c.inundacion,
                            c.creado, c.actualizado])
        csv_file = open(ub + f_name, 'rb')
        response = HttpResponse(FileWrapper(csv_file), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % f_name
        return response


class ArchivoNivelView(APIView):
    def get(self, request, format=None):
        years = self.request.query_params.get('years', None)
        for y in years.split("-"):
            if not y.isdigit():
                return Response("Invalid years format", status=status.HTTP_400_BAD_REQUEST)
        ub = "./files/"
        f_name = "Fflood_Registros_Nivel_Agua" + years.replace('-', '_') + ".csv"
        with open(ub + f_name, 'w+', newline='') as f:
            w = csv.writer(f)
            w.writerow(["Fecha Hora", "Sensor", "Latitud", "Longitud", "Nivel Agua[cm]"])
            q = "SELECT * FROM medicion WHERE YEAR(creado) in (" + years.replace("-", ", ") + ")"
            for m in Medicion.objects.raw(q):
                w.writerow([m.creado, m.sensor.id_sensor, m.sensor.latitud, 
                            m.sensor.longitud, m.nivel_agua])
        csv_file = open(ub + f_name, 'rb')
        response = HttpResponse(FileWrapper(csv_file), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % f_name
        return response


class CatInundacion(APIView):
    def get(self, request, format=None):
        condiciones = Condicion.objects.raw("SELECT * FROM condicion WHERE YEAR(fecha) > 2009")
        years = set()
        for c in condiciones:
            years.add(c.fecha.year)
        return Response({"catalogo": years})


class CatMedicion(APIView):
    def get(self, request, format=None):
        mediciones = Medicion.objects.all()
        years = set()
        for m in mediciones:
            years.add(m.creado.year)
        return Response({"catalogo": years})