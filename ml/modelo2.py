from keras.models import Sequential
from keras.layers import Dense
import csv


FILE_X_TRAIN = "./ml/files/x_train.csv"
FILE_X_TEST = "./ml/files/x_test.csv"
FILE_Y_TRAIN = "./ml/files/y_train.csv"
FILE_Y_TEST = "./ml/files/y_test.csv"
FILE_MODEL = "./ml/files/model2.h5"

with open(FILE_X_TRAIN, 'r', newline='') as f_x_train:
    reader = csv.reader(f_x_train)
    next(reader, None)
    x_train = []
    for r in reader:
        # "Mes", "Precipitacion","Temp Min", "Temp Max"
        x_train.append([int(r[0]), float(r[1]),
                        float(r[2]), float(r[3])])
    print(len(x_train))

with open(FILE_X_TEST, 'r', newline='') as f_x_test:
    reader = csv.reader(f_x_test)
    next(reader, None)
    x_test = []
    for r in reader:
        # "Mes", "Precipitacion","Temp Min", "Temp Max"
        x_test.append([int(r[0]), float(r[1]),
                       float(r[2]), float(r[3])])
    print(len(x_test))

with open(FILE_Y_TRAIN, 'r', newline='') as f_y_train:
    reader = csv.reader(f_y_train)
    next(reader, None)
    y_train = []
    for r in reader:
        # "Inundacion"
        y_train.append(int(r[0]) if r[0] == "1" else -1)
    print(len(y_train))

with open(FILE_Y_TEST, 'r', newline='') as f_y_test:
    reader = csv.reader(f_y_test)
    next(reader, None)
    y_test = []
    for r in reader:
        # "Inundacion"
        y_test.append(int(r[0]) if r[0] == "1" else -1)
    print(len(y_test))

print(y_test)
# define the keras model
model = Sequential()
model.add(Dense(12, input_dim=4, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.summary()
# compile the keras model
model.compile(loss='squared_hinge', optimizer='adam', metrics=['accuracy'])  # noqa
# fit the keras model on the dataset
model.fit(x_train, y_train, epochs=150, batch_size=10)
# evaluate the keras model
result = model.evaluate(x_test, y_test)
print(model.metrics_names)
print(result)
model.save(FILE_MODEL)
