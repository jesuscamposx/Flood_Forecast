from sklearn.model_selection import train_test_split
from api.models import Condicion, Alcaldia
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

FILE_X_TRAIN = "./ml/files/x_train.csv"
FILE_X_TEST = "./ml/files/x_test.csv"
FILE_Y_TRAIN = "./ml/files/y_train.csv"
FILE_Y_TEST = "./ml/files/y_test.csv"

FILE_MODEL = "./ml/files/model.h5"
model = load_model(FILE_MODEL)


class PrediccionView(APIView):
    def get(self, request, format=None):
        fecha = self.request.query_params.get('fecha', None)
        colonia = self.request.query_params.get('colonia', None)

        if fecha is None:
            return Response({"id": 40001, "text": "Fecha es requerido."},
                            status=status.HTTP_400_BAD_REQUEST)
        if colonia is None:
            return Response({"id": 40001, "text": "Colonia es requerido."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            alcaldia = Alcaldia.objects.get(id_alcaldia=colonia)
        except Exception as e:
            logger.error(str(e))
            return Response({"id": 40401, "text": "Colonia Id invalido."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            url = settings.CLIMA_URL + "&lat=" + str(alcaldia.latitud) + "&lon=" + str(alcaldia.longitud)  # noqa
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
                prediccion = model.predict([[mes, rain, temp_min, temp_max]])
                return Response({
                    "inundacion": prediccion[0][0] > 0.1,
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
        if start is None:
            start = "2011"
        logger.info("Getting data from database...")
        q = "SELECT * FROM condicion WHERE YEAR(fecha) >= " + start
        for condicion in Condicion.objects.raw(q):
            x.append([condicion.fecha.month, condicion.precipitacion,
                    condicion.temp_min, condicion.temp_max])
            y.append(condicion.inundacion)
        logger.info("Spliting data...")
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 1)

        logger.info("Creating files...")
        with open(FILE_X_TRAIN, 'w', newline='') as f_x_tr:
            w_x_tr = csv.writer(f_x_tr)
            w_x_tr.writerow(["Mes", "Precipitacion","Temp Min", "Temp Max"])
            for x in x_train:
                w_x_tr.writerow(x)
        
        with open(FILE_X_TEST, 'w', newline='') as f_x_ts:
            w_x_ts = csv.writer(f_x_ts)
            w_x_ts.writerow(["Mes", "Precipitacion","Temp Min", "Temp Max"])
            for x in x_test:
                w_x_ts.writerow(x)

        with open(FILE_Y_TRAIN, 'w', newline='') as f_y_tr:
            w_y_tr = csv.writer(f_y_tr)
            w_y_tr.writerow(["Inundacion"])
            for y in y_train:
                w_y_tr.writerow([y])

        with open(FILE_Y_TEST, 'w', newline='') as f_y_ts:
            w_y_ts = csv.writer(f_y_ts)
            w_y_ts.writerow(["Inundacion"])
            for y in y_test:
                w_y_ts.writerow([y])
        
        logger.info("Completed...")
        return Response("OK", status=status.HTTP_200_OK)
