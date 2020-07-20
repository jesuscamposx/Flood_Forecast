from keras.models import load_model
import csv
import sys

FILE_X_TRAIN = "./ml/files/x_train_"
FILE_X_TEST = "./ml/files/x_test_"
FILE_Y_TRAIN = "./ml/files/y_train_"
FILE_Y_TEST = "./ml/files/y_test_"
FILE_MODEL = "./ml/files/model_"

colonia = sys.argv[1]
print("Se procesará para la colona: " + colonia)
FILE_X_TRAIN += colonia + ".csv"
FILE_X_TEST += colonia + ".csv"
FILE_Y_TRAIN += colonia + ".csv"
FILE_Y_TEST += colonia + ".csv"
FILE_MODEL += colonia + ".h5"


with open(FILE_X_TEST, 'r', newline='') as f_x_test:
    reader = csv.reader(f_x_test)
    next(reader, None)
    x_test = []
    for r in reader:
        # "Mes", "Precipitacion","Temp Min", "Temp Max"
        x_test.append([int(round(float(r[0]))), float(r[1]),
                       float(r[2]), float(r[3])])
    print(len(x_test))
    
with open(FILE_Y_TEST, 'r', newline='') as f_y_test:
    reader = csv.reader(f_y_test)
    next(reader, None)
    y_test = []
    for r in reader:
        # "Inundacion"
        y_test.append(int(r[0]))
    print(len(y_test))

model = load_model(FILE_MODEL)

i = 0
for x in x_test:
    if y_test[i] == 1:  
        pred = model.predict([x])
        print("X: " + str(x) + " Y: " + str(y_test[i]) + " Pred: " + str(pred[0][0]))
    i += 1
