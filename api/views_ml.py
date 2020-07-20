from sklearn.model_selection import train_test_split
from api.models import Condicion, Colonia
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from keras.models import load_model
from django.conf import settings
from datetime import datetime, date
import logging
import csv
import requests

logger = logging.getLogger(__name__)

FILE_X = "./ml/files/x_"
FILE_Y = "./ml/files/y_"

FILE_MODEL_1 = "./ml/files/model_1.h5"
FILE_MODEL_2 = "./ml/files/model_2.h5"
model_1 = load_model(FILE_MODEL_1)
model_2 = load_model(FILE_MODEL_2)


class PrediccionView(APIView):
    def get(self, request, format=None):
        fecha = self.request.query_params.get('fecha', None)
        id_colonia = self.request.query_params.get('colonia', None)

        if fecha is None:
            return Response({"id": 40001, "text": "Fecha es requerido."},
                            status=status.HTTP_400_BAD_REQUEST)
        if id_colonia is None:
            return Response({"id": 40001, "text": "Colonia es requerido."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            colonia = Colonia.objects.get(id_colonia=id_colonia)
        except Exception as e:
            logger.error(str(e))
            return Response({"id": 40401, "text": "Colonia Id invalido."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            hoy = date.today()
            fecha_d = datetime.strptime(fecha, '%Y-%m-%d').date()
            if fecha_d >= hoy:
                clima = getWeatherFromAPI(colonia, fecha)
            else:
                clima = getWeatherFromDB(colonia,fecha)
            print(clima)
            if clima is None:
                return Response({"id": 40902, "text": "Fecha invalida"},
                            status=status.HTTP_409_CONFLICT)
            if id_colonia == "1":
                prediccion = model_1.predict(clima)
            elif id_colonia == "2":
                prediccion = model_2.predict(clima)
            return Response({
                "inundacion": prediccion[0][0] > 0.5,
                "value": prediccion[0][0]
                }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({"id": 40901, "text": "Proceso de prediccion con fallas."},
                            status=status.HTTP_409_CONFLICT)
        return Response("OK", status=status.HTTP_200_OK)


class ConjuntosView(APIView):
    def get(self, request, format=None):
        x = []
        y = []
        start = self.request.query_params.get('start', None)
        colonia = self.request.query_params.get('colonia', None)

        if start is None:
            start = "2011"
        if colonia is None:
            return Response({"id": 40001, "text": "Colonia es requerido."},
                            status=status.HTTP_400_BAD_REQUEST)

        logger.info("Getting data from database...")
        q = "SELECT * FROM condicion WHERE YEAR(fecha) >= " + start + " and idColonia = "+ colonia
        for condicion in Condicion.objects.raw(q):
            x.append([condicion.fecha.month, condicion.precipitacion,
                    condicion.temp_min, condicion.temp_max])
            y.append(condicion.inundacion)

        logger.info("Creating files...")
        with open(FILE_X + str(colonia) + ".csv", 'w', newline='') as f_x:
            w_x = csv.writer(f_x)
            w_x.writerow(["Mes", "Precipitacion","Temp Min", "Temp Max"])
            for xe in x:
                w_x.writerow(xe)

        with open(FILE_Y + str(colonia) + ".csv", 'w', newline='') as f_y:
            w_y = csv.writer(f_y)
            w_y.writerow(["Inundacion"])
            for ye in y:
                w_y.writerow([ye])

        logger.info("Completed...")
        return Response("OK", status=status.HTTP_200_OK)

def getWeatherFromAPI(colonia, fecha):
    try:
        url = settings.CLIMA_URL + "&lat=" + str(colonia.latitud) + "&lon=" + str(colonia.longitud)  # noqa
        dt_in = datetime.strptime(fecha, '%Y-%m-%d').date()
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            clima = {}
            for d in response["daily"]:
                dt_out = date.fromtimestamp(d["dt"])
                if dt_in == dt_out:
                    clima = d
                    break
            rain = clima.get("rain", None)
            if rain is None:
                rain = 0.0
            else:
                rain = float(rain)
            temp = clima.get("temp", None)
            if temp is None:
                raise Exception("Temp is None")
            temp_min = temp["min"]
            temp_max = temp["max"]
            temp_min = (float(temp_min) - 273.15)
            temp_max = (float(temp_max) - 273.15)
            mes = int(dt_in.month)
            return [[mes, rain, temp_min, temp_max]]
    except Exception:
        return None


def getWeatherFromDB(colonia, fecha):
    try:
        condicion = Condicion.objects.get(id_colonia=colonia.id_colonia, fecha=fecha)
        temp_min = float(condicion.temp_min)
        temp_max = float(condicion.temp_max)
        mes = int(condicion.fecha.month)
        precipitacion = float(condicion.precipitacion)
        return [[mes, precipitacion, temp_min, temp_max]]
    except Exception:
        return None
