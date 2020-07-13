from sklearn.model_selection import train_test_split
from api.models import Condicion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
import csv

logger = logging.getLogger(__name__)
FILE_X_TRAIN = "./ml/files/x_train.csv"
FILE_X_TEST = "./ml/files/x_test.csv"
FILE_Y_TRAIN = "./ml/files/y_train.csv"
FILE_Y_TEST = "./ml/files/y_test.csv"

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
