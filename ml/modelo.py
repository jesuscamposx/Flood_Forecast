from keras.models import Sequential
from keras.layers import Dense
from keras import metrics
import tensorflow as tf
import csv
import datetime
import sys


FILE_X_TRAIN = "./ml/files/x_train_"
FILE_X_TEST = "./ml/files/x_test_"
FILE_Y_TRAIN = "./ml/files/y_train_"
FILE_Y_TEST = "./ml/files/y_test_"
FILE_MODEL = "./ml/files/model_"
LOGS_FOLDER = "./ml/logs/fit/"

colonia = sys.argv[1]
print("Se procesará para la colona: " + colonia)
FILE_X_TRAIN += colonia + ".csv"
FILE_X_TEST += colonia + ".csv"
FILE_Y_TRAIN += colonia + ".csv"
FILE_Y_TEST += colonia + ".csv"
FILE_MODEL += colonia + ".h5"

with open(FILE_X_TRAIN, 'r', newline='') as f_x_train:
    reader = csv.reader(f_x_train)
    next(reader, None)
    x_train = []
    for r in reader:
        # "Mes", "Precipitacion","Temp Min", "Temp Max"
        x_train.append([int(round(float(r[0]))), float(r[1]),
                        float(r[2]), float(r[3])])
    print(len(x_train))

with open(FILE_X_TEST, 'r', newline='') as f_x_test:
    reader = csv.reader(f_x_test)
    next(reader, None)
    x_test = []
    for r in reader:
        # "Mes", "Precipitacion","Temp Min", "Temp Max"
        x_test.append([int(round(float(r[0]))), float(r[1]),
                       float(r[2]), float(r[3])])
    print(len(x_test))

with open(FILE_Y_TRAIN, 'r', newline='') as f_y_train:
    reader = csv.reader(f_y_train)
    next(reader, None)
    y_train = []
    for r in reader:
        # "Inundacion"
        y_train.append(int(r[0]))
    print(len(y_train))

with open(FILE_Y_TEST, 'r', newline='') as f_y_test:
    reader = csv.reader(f_y_test)
    next(reader, None)
    y_test = []
    for r in reader:
        # "Inundacion"
        y_test.append(int(r[0]))
    print(len(y_test))

# Definición del modelo
model = Sequential()
model.add(Dense(12, input_dim=4, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.summary()
# Compilar el modelo
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', metrics.TruePositives(),
              metrics.TrueNegatives(), metrics.FalsePositives(), metrics.FalseNegatives(),
              metrics.Recall(), metrics.Precision()])  # noqa

log_dir = LOGS_FOLDER + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

# Entrenar el model
model.fit(x_train, y_train, epochs=5000, batch_size=10, callbacks=[tensorboard_callback])

# evaluate the keras model
result = model.evaluate(x_test, y_test)
[loss, accuracy, truePositives, trueNegatives, falsePositives, falseNegatives, recall, precision] = result
h1 = 2 * (recall * precision) / (recall + precision)
model.save(FILE_MODEL)
print(model.metrics_names)
print(result)
print("H1: " + str(h1))
