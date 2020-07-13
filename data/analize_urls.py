from newspaper import Article
import csv


FILE_NAME = "./data/files/resultados_analisis.csv"
FILE_NAME_ERRORES = "./data/files/resultados_analisis_errores.csv"


def initiliaze_file(file):
    f = open(file, "w", newline='', encoding="utf-8")
    w = csv.writer(f)
    w.writerow(["[Fecha]", "[Titulo]", "[Texto]", "[Snippet]", "[URL]"])
    f.close()


f_urls = open("./data/files/urls_inundacion.csv", 'r', encoding="utf-8")
r = csv.reader(f_urls)
data = []
for row in r:
    data.append(row)
data = data[1:-1]
f_urls.close()

initiliaze_file(FILE_NAME)
initiliaze_file(FILE_NAME_ERRORES)
f = open(FILE_NAME, 'a+', newline='', encoding="utf-8")
w = csv.writer(f)
f_e = open(FILE_NAME_ERRORES, 'a+', newline='', encoding="utf-8")
w_e = csv.writer(f_e)
a = 1
c = 0
er = 0
for row in data:
    try:
        article = Article(row[0], 'es')
        article.download()
        article.parse()
        dt = row[2] if not article.publish_date else article.publish_date
        tt = row[1]
        txt = article.text
        sp = row[3]
        lk = row[0]
        w.writerow([dt, tt, txt, sp, lk])
        c += 1
        print("Noticia " + str(a) + " analizado. " + "Correctos: " + str(c))
    except Exception as e:
        er += 1
        w.writerow([row[2], row[1], "", row[3], row[0]])
        w_e.writerow([row[2], row[1], "", row[3], row[0]])
        print("Errores " + str(er))
    finally:
        a += 1
f.close()
f_e.close()
print("Correctos: " + str(c))
print("Errores: " + str(er))
