import csv
from dateutil.parser import parse
from dateutil.parser import parserinfo


CORRECT_FILE_NAME = "./data/files/resultados_analisis_c.csv"
WRONG_FILE_NAME = "./data/files/resultados_analisis_w.csv"


class CustomParserInfo(parserinfo):

    # three months in Spanish for illustration
    MONTHS = [("ene", "Enero"), ("feb", "Febrero"), ("mar", "Marzo"),
              ("abr", "Abril"), ("may", "Mayo"), ("jun", "Junio"),
              ("jul", "Julio"), ("ago", "Agosto"), ("sep", "Septiembre"),
              ("oct", "Octubre"), ("nov", "Noviembre"), ("dic", "Diciembre")]


def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy, parserinfo=CustomParserInfo())
        return True

    except ValueError:
        return False


def initiliaze_file(file):
    f = open(file, "w", newline='', encoding="utf-8")
    w = csv.writer(f)
    w.writerow(["[Fecha]", "[Titulo]", "[Texto]", "[Snippet]", "[URL]"])
    f.close()


f_urls = open("./data/files/resultados_analisis.csv", 'r', newline='', encoding="utf-8")
r = csv.reader(f_urls)
data = []
for row in r:
    data.append(row)
data = data[1:-1]
f_urls.close()

initiliaze_file(CORRECT_FILE_NAME)
f_c = open(CORRECT_FILE_NAME, 'a+', newline='', encoding="utf-8")
w_c = csv.writer(f_c)

initiliaze_file(WRONG_FILE_NAME)
f_w = open(WRONG_FILE_NAME, 'a+', newline='', encoding="utf-8")
w_w = csv.writer(f_w)

c = 0
w = 0
for row in data:
    fecha = row[0]
    titulo = row[1]
    texto = row[2]
    snp = row[3]
    url = row[4]
    if fecha and url:
        if is_date(fecha, fuzzy=True):
            dt = parse(fecha, fuzzy=True, parserinfo=CustomParserInfo()).strftime('%Y-%m-%d')
            w_c.writerow([dt, titulo, texto, snp, url])
            c += 1     
        elif is_date(snp, fuzzy=True):
            dt = parse(snp, fuzzy=True, parserinfo=CustomParserInfo()).strftime('%Y-%m-%d')
            w_c.writerow([dt, titulo, texto, snp, url])
            c += 1
        else:
            w_w.writerow([fecha, titulo, texto, snp, url])
            w += 1
            continue
f_c.close()
f_w.close()
print("Total de registros: " + str(len(data)))
print("Registros correctos: " + str(c))
print("Registros invalidos: " + str(w))
