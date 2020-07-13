import csv

FILE_NAME = "./data/files/metricas.csv"
LUGAR = ["CDMX", "D.F.", "DF", "Distrito Federal", "Ciudad de México", "Ciudad de Mexico"]
INUNDACION = ["Inundacion", "Inundación", "Encharcamiento"]
LLUVIA = ["Lluvia", "Granizo", "Precipitación", "Precipitacion"]
DELEGACION = ["Gustavo A. Madero", "GAM", "G.A.M.", "Gustavo Adolfo Madero"]
HORARIO = ["Mañana", "Tarde", "Noche"]
COLONIA = ["Lindavista", "San Juan de Aragon", "Ticomán", "Vallejo", "Ticoman", "San Juan de Aragón",
           "Martin Carrera", "Martín Carrera", "Villa de Aragón", "Villa de Aragon"]

def initiliaze_file(file):
    f = open(file, "w", newline='', encoding="utf-8")
    w = csv.writer(f)
    w.writerow(["El número bajo las columnas CDMX, INUNDACION, LLUVIA, " +
                "GAM indica el numero de noticias que contien esas palabras"])
    w.writerow(["Y las palabras bajo HORARIO y COLONIA son las palabras encontradas en las noticias"])
    w.writerow(["[Fecha]", "[Conteo]", "[CDMX]", "[INUNDACION]", "[LLUVIA]", 
                "[GAM]", "HORARIO", "COLONIA"])
    f.close()

def contiene_palabras(opciones, titulo, texto, snippet):
    c = False
    if texto:
        txt = texto.lower()
        for o in opciones:
            if o.lower() in txt:
                c = True
                break
    
    if not c and titulo:
        tl = titulo.lower()
        for o in opciones:
            if o.lower() in tl:
                c = True
                break
    
    if not c and snippet:
        sp = snippet.lower()
        for o in opciones:
            if o.lower() in sp:
                c = True
                break
    return c


def obtener_palabra(opciones, titulo, texto, snippet):
    r = ""
    if texto:
        txt = texto.lower()
        for o in opciones:
            if o.lower() in txt:
                r = o
                break
    
    if not r and titulo:
        tl = titulo.lower()
        for o in opciones:
            if o.lower() in tl:
                r = o
                break

    if not r and snippet:
        sp = snippet.lower()
        for o in opciones:
            if o.lower() in sp:
                r = o
                break

    return r


f_urls = open("./data/files/resultados_analisis_c.csv", 'r', encoding="utf-8")
r = csv.reader(f_urls)
data = []
for row in r:
    data.append(row)
data = data[1:-1]
f_urls.close()

results = dict()
#cont = 0
for row in data:
    dt = row[0]
    titulo = row[1]
    texto = row[2]
    snippet = row[3]

    if results.get(dt) is None:
        results[dt] = {
            "conteo": 1,
            "cdmx": 1 if contiene_palabras(LUGAR, titulo, texto, snippet) else 0,
            "inundacion": 1 if contiene_palabras(INUNDACION, titulo, texto, snippet) else 0,
            "lluvia": 1 if contiene_palabras(LLUVIA, titulo, texto, snippet) else 0,
            "gam": 1 if contiene_palabras(DELEGACION, titulo, texto, snippet)
            or contiene_palabras(COLONIA, titulo, texto, snippet) else 0,
            "horario": obtener_palabra(HORARIO, titulo, texto, snippet),
            "colonia": obtener_palabra(COLONIA, titulo, texto, snippet)
        }
    else:
        results[dt]["conteo"] += 1
        if contiene_palabras(LUGAR, titulo, texto, snippet):
            results[dt]["cdmx"] += 1
        if contiene_palabras(INUNDACION, titulo, texto, snippet):
            results[dt]["inundacion"] += 1
        if contiene_palabras(LLUVIA, titulo, texto, snippet):
            results[dt]["lluvia"] += 1
        if contiene_palabras(DELEGACION, titulo, texto, snippet) or contiene_palabras(COLONIA, titulo, texto, snippet):
            results[dt]["gam"] += 1
        h = obtener_palabra(HORARIO, titulo, texto, snippet)
        col = obtener_palabra(COLONIA, titulo, texto, snippet)
        if h and h not in results[dt]["horario"]:
            results[dt]["horario"] += ", " + h if results[dt]["horario"] else h
        if col and col not in results[dt]["colonia"]:
            results[dt]["colonia"] += ", " + col if results[dt]["colonia"] else col
    #print(dt + ": " + str(results[dt]))
    #cont += 1
    #if cont == 100:
    #   break

initiliaze_file(FILE_NAME)
f = open(FILE_NAME, 'a+', newline='', encoding="utf-8")
w = csv.writer(f)
for k in results.keys():
    row = [k, results[k]["conteo"], results[k]["cdmx"], results[k]["inundacion"],
           results[k]["lluvia"], results[k]["gam"], results[k]["horario"],
           results[k]["colonia"]]
    w.writerow(row)
f.close()

