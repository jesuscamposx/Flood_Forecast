import csv
# Oversample with SMOTE and random undersample for imbalanced dataset
from collections import Counter
from sklearn.datasets import make_classification
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from matplotlib import pyplot
from numpy import where
from sklearn.model_selection import train_test_split
import sys

FILE_X_TRAIN = "./ml/files/x_train_"
FILE_X_TEST = "./ml/files/x_test_"
FILE_Y_TRAIN = "./ml/files/y_train_"
FILE_Y_TEST = "./ml/files/y_test_"
FILE_X = "./ml/files/x_"
FILE_Y = "./ml/files/y_"
 
colonia = sys.argv[1]
print("Se procesará para la colona: " + colonia)
FILE_X_TRAIN += colonia + ".csv"
FILE_X_TEST += colonia + ".csv"
FILE_Y_TRAIN += colonia + ".csv"
FILE_Y_TEST += colonia + ".csv"
FILE_X += colonia + ".csv"
FILE_Y += colonia + ".csv"

with open(FILE_X, 'r', newline='') as f_x:
    reader = csv.reader(f_x)
    next(reader, None)
    x = []
    for r in reader:
        # "Mes", "Precipitacion","Temp Min", "Temp Max"
        x.append([int(r[0]), float(r[1]),
                        float(r[2]), float(r[3])])
    print(len(x))

with open(FILE_Y, 'r', newline='') as f_y:
    reader = csv.reader(f_y)
    next(reader, None)
    y = []
    for r in reader:
        # "Inundacion"
        y.append(int(r[0]))
    print(len(y))

# define pipeline
over = SMOTE(sampling_strategy=0.1)
under = RandomUnderSampler(sampling_strategy=0.5)
steps = [('o', over), ('u', under)]
pipeline = Pipeline(steps=steps)
# transform the dataset
x, y = pipeline.fit_resample(x, y)
# summarize the new class distribution
counter = Counter(y)
print(counter)
# create train and test datasets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 1)
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
# save datasets
# scatter plot of examples by class label
#for label, _ in counter.items():
#	row_ix = where(y == label)[0]
#	pyplot.scatter(x[row_ix, 0], x[row_ix, 1], label=str(label))
#pyplot.legend()
#pyplot.show()