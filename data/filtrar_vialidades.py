import csv

FILE_NAME_FROM = "./data/files/atlas-de-riesgo-inundaciones.csv"
FILE_NAME_TO = "./data/files/atlas-de-riesgo-inundaciones_gam.csv"

with open(FILE_NAME_FROM, 'r', newline='', encoding="utf-8") as f_f:
    reader_f = csv.reader(f_f)
    with open(FILE_NAME_TO, 'w', newline='', encoding="utf-8") as f_t:
        writer_t = csv.writer(f_t)
        for r in reader_f:
            if r[10] == 'Gustavo A. Madero' or r[10] == 'Alcaldía':
                writer_t.writerow(r)

f_f.close()
f_t.close()
