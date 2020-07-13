import csv

c_y_train = 0
t_train = -1
with open("./ml/files/y_train.csv", 'r', newline='') as y_train:
    reader = csv.reader(y_train)
    for r in reader:
        t_train += 1
        if r[0] == "1":
            c_y_train += 1

p_train_inund = (c_y_train / t_train) * 100
print("Total registros de entrenamiento: " + str(t_train))
print("Registros con inundacion: " + str(c_y_train))
print("Porcentaje de registros con inundacion: " + str(p_train_inund) + "%")

c_y_test = 0
t_test = -1
with open("./ml/files/y_test.csv", 'r', newline='') as y_test:
    reader = csv.reader(y_test)
    for r in reader:
        t_test += 1
        if r[0] == "1":
            c_y_test += 1

p_test_inund = (c_y_test / t_test) * 100
print("Total registros de prueba: " + str(t_test))
print("Registros con inundacion: " + str(c_y_test))
print("Porcentaje de registros con inundacion: " + str(p_test_inund) + "%")
