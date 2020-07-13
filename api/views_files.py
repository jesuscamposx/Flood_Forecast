from api.models import Condicion
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


class ArchivoView(APIView):
    def get(self, request, format=None):
        years = self.request.query_params.get('years', None)
        for y in years.split("-"):
            if not y.isdigit():
                return Response("Invalid years format", status=status.HTTP_400_BAD_REQUEST)
        ub = "./files/"
        f_name = "Fflood_Registros_" + years.replace('-', '_') + ".csv"
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
